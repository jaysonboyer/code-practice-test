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

The query is built from named steps (`WITH ... AS (...)`, called CTEs). Each step reads the one before it like a table, and its name says what it holds. The full file, with comments, is [`solution.sql-postgres`](TestData/solution.sql-postgres):

```sql
WITH cheapest_affordable_products AS (
    SELECT name, price, quantity
    FROM products
    WHERE price <= 100
    ORDER BY price, name
    LIMIT 100
),
money_left_per_product AS (
    SELECT price,
           quantity,
           100 - (sum(price * quantity) OVER (ORDER BY price, name) - price * quantity) AS money_left
    FROM cheapest_affordable_products
),
items_bought_per_product AS (
    SELECT least(quantity, greatest(0, money_left) / price) AS items_bought
    FROM money_left_per_product
)
SELECT coalesce(sum(items_bought), 0) AS quantity
FROM items_bought_per_product;
```

### Step 1, `cheapest_affordable_products`: only the rows that can matter

- `ORDER BY price, name` puts the cheapest first. Sorting by `name` as well as `price` breaks ties. Eraser and Notebook both cost $5; with `name` added each gets its own position, so the order is the same every run. Which of two same-price items comes first does not change the count.
- `WHERE price <= 100` drops products we could never buy even one of.
- `LIMIT 100` keeps only the 100 cheapest. Every price is at least $1, so $100 pays for at most 100 items, and so at most 100 products. The 101st cheapest product can never get any money, so dropping it never changes the answer.

The answer does not change with or without the last two lines. They are there for speed on big tables: see [Cost](#cost).

### Step 2, `money_left_per_product`: money left when we reach each product

```sql
100 - (sum(price * quantity) OVER (ORDER BY price, name) - price * quantity) AS money_left
```

- `price * quantity` is the cost of buying the whole row.
- `sum(...) OVER (ORDER BY price, name)` is a **window function**. A normal `sum` collapses all rows into one number. A window function adds a column and keeps every row. With `ORDER BY` it gives a running total: for each row, the sum of that row and every row before it.
- Subtracting the row's own cost gives what was spent on the rows *before* it, and `100 -` that is the money left. It goes negative once the budget is used up.

### Step 3, `items_bought_per_product`, and the total

Read it from the inside out:

| Piece | Meaning |
|-------|---------|
| `greatest(0, money_left)` | treat negative money as 0 |
| `... / price` | how many of this item that money buys; dividing two integers rounds down |
| `least(quantity, ...)` | but never more than are in stock |
| `sum(items_bought)` | add up the items bought from every row |
| `coalesce(..., 0)` | `sum` of zero rows is `NULL` (no value); turn that into 0 |

### Why a partly bought row doesn't break the later rows

`money_left` assumes every earlier row was bought *in full*, including one that was only partly bought. That understates the money actually left, so it is fair to ask whether a later row misses out.

It doesn't. After the partly bought row, the money actually left is less than that row's price, or we could have bought one more. Every later row costs at least as much, so none of them is affordable anyway. The query gives them 0 because their `money_left` is already below 0.

## Edge cases

| Case | Example | Result |
|------|---------|-------:|
| Example 1, money runs out partway through a row | [`test-input-01.py`](TestData/test-input-01.py) | 32 |
| Empty table | [`test-input-02.py`](TestData/test-input-02.py) | 0 (thanks to `coalesce`) |
| Some items cost more than $100 | [`test-input-03.py`](TestData/test-input-03.py): Backpack $99, Jacket $101 | 1 |
| Everything is affordable | [`test-input-04.py`](TestData/test-input-04.py) | 5 |

## PostgreSQL 9.4 compatibility

Everything used here (`WITH` steps, window functions, `least`, `greatest`, `coalesce`, `LIMIT`) has been in Postgres since 8.4. The query was tested on 9.4.26.

## Cost

The task allows at most 100 rows, so any version is instant. On a big table, the work is in step 1:

- Without an index, Postgres reads every row once but keeps only the 100 cheapest in memory as it goes (a "top-N heapsort"), instead of sorting the whole table.
- With an index on `(price, name)`, it reads the first 100 entries of the index and stops, however big the table is.

Steps 2 and 3 only ever see at most 100 rows. [`sql-performance.md`](sql-performance.md) (Task 4) has the measurements on a million-row table.

## Running it

```sh
python3 task-runner.py sql                                  # example 1
python3 task-runner.py sql task_3_and_4/TestData/test-input-03.py  # any other test file
```
