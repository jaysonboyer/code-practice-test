# Products: SQL Performance

Please answer the following questions regarding performance of your SQL solution.

- How would you change your solution to make it performant with very large tables? Which changes, if any, would you make to the query design, processing steps, or tables?

## Answer

Short version: don't sort the whole table. The answer depends only on the 100 cheapest products we can afford, so ask for exactly those (`WHERE price <= 100 ... ORDER BY price, name LIMIT 100`), and add an index on `(price, name)` so Postgres can read them straight off the index. On a million-row table that takes the query from about 3.4 seconds to about half a millisecond.

The query is in [`TestData/solution.sql-postgres`](TestData/solution.sql-postgres); [`how-it-works.md`](how-it-works.md) explains it step by step.

### 1. Measure first

Guessing about performance is how people "optimize" the wrong thing. Fill a table, then ask Postgres what it actually does:

```sql
-- A million random products. This breaks Task 3's limits (at most 100 rows) on purpose:
-- we want to see how the query grows, not whether it is correct.
TRUNCATE products;
INSERT INTO products (name, price, quantity)
SELECT 'product_' || product_number,
       1 + floor(random() * 200)::int,     -- price: $1 to $200, as Task 3 allows
       1 + floor(random() * 100)::int      -- quantity: 1 to 100
FROM generate_series(1, 1000000) AS product_number;
ANALYZE products;  -- fresh statistics, so the planner's row estimates are realistic

-- ANALYZE runs the query and reports real times; BUFFERS shows how much data it touched.
EXPLAIN (ANALYZE, BUFFERS) <the query>;
```

### 2. What the original query does on a big table

The first version ran a window function (`sum(...) OVER (ORDER BY price, name)`) over **every** row. Its plan, trimmed:

```
Aggregate  (actual time=3735.910..3735.910 rows=1)
  ->  WindowAgg  (rows=1000000)
        ->  Sort  (rows=1000000)
              Sort Key: products.price, products.name
              Sort Method: external merge  Disk: 25344kB
              ->  Seq Scan on products  (rows=1000000)
Execution time: 3738.041 ms
```

Two things to read here:

- **`Sort` over 1,000,000 rows**: sorting is O(N log N), so it grows faster than the table.
- **`external merge  Disk: 25344kB`**: the sort didn't fit in `work_mem` (4 MB by default), so Postgres spilled it to temporary files on disk. Disk is much slower than memory.

Adding an index on `(price, name)` helps a little: Postgres reads the rows in index order and skips the sort. But it still reads and computes a running total for all million rows (about 1.5 s, and 693,807 buffer accesses).

### 3. Query design: only read what can change the answer

Two facts from Task 3 bound the work:

- **A product priced over $100 can never be bought.** So `WHERE price <= 100`.
- **Every price is at least $1**, so $100 buys at most 100 items, from at most 100 products. In price order, the 101st product and every one after it can never get any money. So `ORDER BY price, name LIMIT 100`.

Neither line changes the answer. We checked: the old and new queries agree on the four test inputs, on 60 random small tables with many tied prices, and on two edge cases (150 products at $1, and 99 at $1 plus one at $2).

The processing steps change order: first **pick the 100 rows**, then run the running total over just those. If the window function ran first, it would still need the whole table sorted, which is exactly what we are trying to avoid.

With no index, the new plan reads every row once, but keeps only the 100 cheapest in memory as it goes:

```
->  Limit  (rows=100)
      ->  Sort  (rows=100)
            Sort Method: top-N heapsort  Memory: 29kB
            ->  Seq Scan on products  (rows=500274)
                  Filter: (price <= 100)
                  Rows Removed by Filter: 499726
Execution time: 137.788 ms
```

`top-N heapsort  Memory: 29kB` is the win: memory stays the same however big the table gets, and there's nothing written to disk.

### 4. Tables: an index that matches the sort

```sql
-- B-tree index in the same order as the query's ORDER BY.
-- price first: the cheapest products sit at the start of the index, and WHERE price <= 100 becomes a range read.
-- name second: it breaks price ties the same way the query does, so the index order is the query order
-- and Postgres needs no separate sort.
CREATE INDEX products_price_name_idx ON products (price, name);
```

Now Postgres walks the index from the cheapest product and stops after 100 entries:

```
->  Limit  (rows=100)
      ->  Index Scan using products_price_name_idx on products  (rows=100)
            Index Cond: (price <= 100)
            Buffers: shared hit=70
Execution time: 0.478 ms
```

It touched 70 pages instead of 5,406. The cost no longer depends on the size of the table, only on the 100 rows it reads.

After a bulk load, run `ANALYZE products` yourself (autovacuum does it too, but later), so the planner knows the table is big and picks the index.

The trade-off: every `INSERT`, and every `UPDATE` to `price` or `name`, now also updates the index. For a shop catalogue, which is read far more often than it is changed, that is a good deal.

### 5. Results on 1,000,000 rows

Execution time from `EXPLAIN ANALYZE`, PostgreSQL 9.4.26, three runs each, old and new alternating:

| | Original query | New query |
|---|---:|---:|
| No index | 3274, 3699, 3354 ms | 117, 119, 138 ms |
| Index on `(price, name)` | 1556, 1468, 1984 ms | 0.48, 0.58, 0.41 ms |

These ran on a busy laptop (load average around 8), so read them as orders of magnitude, not exact numbers.

### 6. Things I would not do, and why

- **Raise `work_mem`** so the big sort fits in memory. It hides the problem instead of removing it: the sort is still O(N log N), and `work_mem` is per sort, per connection, so a big value can run the server out of memory under load. Once the query sorts only 100 rows, it isn't needed.
- **Store a running total** in the table (a "spent so far" column) or a materialized view. Any price change would rewrite the totals for every product after it. The index already makes the query fast without it.
- **Add `quantity` to the index** to get an index-only scan. It would skip reading the table pages, but the query already touches only 70 pages; that isn't worth a wider index to maintain.
