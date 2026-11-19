# Task 3: How the Query Works

The question: given a `products` table (`name`, `price`, `quantity`), what is the largest number of items you can buy while spending at most $100? See [TASK-03.md](TASK-03.md).

The solution is in [`task_3_and_4/TestData/solution.sql-postgres`](TestData/solution.sql-postgres) and runs on PostgreSQL 9.4.

## The idea: buy the cheapest items first

The question only asks *how many* items you get. A $3 pencil counts exactly as much as a $99 backpack, so every dollar should go to the cheapest item still available.

**Why this always gives the best answer:** suppose a purchase buys a more expensive item while a cheaper one is still in stock. Swap the expensive item for the cheap one. You still have the same number of items, and you spent the same or less. Repeat the swap until there are none left to make. You end up with the cheapest-first purchase, and it has at least as many items as the purchase you started with. So no purchase can beat cheapest-first.

Each product is then either:

- **bought in full**, if the money left covers all of it,
- **bought in part**, if the money runs out partway through it (this happens to at most one product), or
- **not bought at all**, once the money is gone.

## Worked example

Example 1 from the task, sorted cheapest first:

| name | price | quantity | spent before this row | money left | can afford | bought |
|------|------:|---------:|----------------------:|-----------:|-----------:|-------:|
| Pencil | 3 | 30 | 0 | 100 | 100 / 3 = 33 | **30** (only 30 in stock) |
| Eraser | 5 | 3 | 90 | 10 | 10 / 5 = 2 | **2** |
| Notebook | 5 | 3 | 105 | 0 | 0 | **0** |
| Pen | 6 | 20 | 120 | 0 | 0 | **0** |

Total: 30 + 2 + 0 + 0 = **32**.

"Spent before this row" means the cost of buying every cheaper product *in full*. It can be more than $100, like 105 for the Notebook. That row then has no money left, so it buys nothing.

## The query

```sql
SELECT coalesce(sum(least(quantity, greatest(0, 100 - spent_before) / price)), 0) AS quantity
FROM (
    SELECT price,
           quantity,
           sum(price * quantity) OVER (ORDER BY price, name) - price * quantity AS spent_before
    FROM products
) AS cheapest_first;
```

### Inner query: what was spent before each row

```sql
sum(price * quantity) OVER (ORDER BY price, name) - price * quantity AS spent_before
```

- `price * quantity` is the cost of buying the whole row.
- `sum(...) OVER (ORDER BY price, name)` is a **window function**. A normal `sum` collapses all rows into one number. A window function adds a column and keeps every row. With `ORDER BY` it gives a running total: for each row, the sum of that row and every row before it.
- Subtracting the row's own cost gives the total for the rows *before* it.
- Sorting by `name` as well as `price` breaks ties. Eraser and Notebook both cost $5. Sorted by price alone, Postgres treats them as tied, puts them both in the running total at once, and gives them the same value. With `name` added, each row gets its own position. Which of two same-price items comes first does not change the count.

### Outer query: items bought from each row, then the total

Read this part from the inside out:

| Piece | Meaning |
|-------|---------|
| `100 - spent_before` | money left when we reach this row (can be negative) |
| `greatest(0, ...)` | treat negative money as 0 |
| `... / price` | how many of this item that money buys; dividing two integers rounds down |
| `least(quantity, ...)` | but never more than are in stock |
| `sum(...)` | add up the items bought from every row |
| `coalesce(..., 0)` | `sum` of zero rows is `NULL` (no value); turn that into 0 |

`FROM ( ... ) AS cheapest_first` lets the outer query read the inner query's result as if it were a table. Postgres requires the name (`cheapest_first`), but nothing else uses it.

### Why a partly bought row doesn't break the later rows

`spent_before` assumes every earlier row was bought *in full*, including one that was only partly bought. That overstates what was actually spent, so it is fair to ask whether a later row misses out.

It doesn't. After the partly bought row, the money actually left is less than that row's price, or we could have bought one more. Every later row costs at least as much, so none of them is affordable anyway. The query gives them 0 because their `spent_before` is already above $100.

## Edge cases

| Case | Example | Result |
|------|---------|-------:|
| Example 1, money runs out partway through a row | [`test-input-01.py`](TestData/test-input-01.py) | 32 |
| Empty table | [`test-input-02.py`](TestData/test-input-02.py) | 0 (thanks to `coalesce`) |
| Some items cost more than $100 | [`test-input-03.py`](TestData/test-input-03.py): Backpack $99, Jacket $101 | 1 |
| Everything is affordable | [`test-input-04.py`](TestData/test-input-04.py) | 5 |

## PostgreSQL 9.4 compatibility

Everything used here (window functions, `least`, `greatest`, `coalesce`, subqueries in `FROM`) has been in Postgres since 8.4. The query was tested on 9.4.26.

## Cost

Postgres sorts the rows once for the window function: O(N log N) for N products. The rest is a single pass over the sorted rows. The task allows at most 100 rows, so this is instant. [TASK-04](TASK-04.md) asks what changes on very large tables.

## Running it

```sh
python3 task-runner.py sql                                  # example 1
python3 task-runner.py sql task_3_and_4/TestData/test-input-03.py  # any other test file
```
