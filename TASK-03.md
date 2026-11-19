# Products: Max Items for $100

You are given a table `products` with the following structure:

```sql
create table products (
    name varchar(20) primary key,
    price integer not null,
    quantity integer not null
);
```

It represents the product types that can be bought in a shop. Each row of the table contains information about a product:

- `name` − unique key, name of the product type
- `price` − price per single item of this product in dollars
- `quantity` − number of items of this product available in the shop

What is the maximum number of items that can be bought by spending at most $100? The items bought can be of different types and their number can't exceed their availability in the shop.

Write an SQL query that finds this number. The result table should comprise one column, `quantity`, that contains an integer describing the maximum number of items that can be bought with $100.

**Examples:**

1. Given:

   ```
   +------------+-------+----------+
   | name       | price | quantity |
   +------------+-------+----------+
   | Pencil     | 3     | 30       |
   | Eraser     | 5     | 3        |
   | Notebook   | 5     | 3        |
   | Pen        | 6     | 20       |
   +------------+-------+----------+
   ```

   your query should return:

   ```
   +----------+
   | quantity |
   +----------+
   | 32       |
   +----------+
   ```

   We can buy all 30 pencils and 2 notebooks. This gives 32 products in total that will cost exactly $100.

2. Given:

   ```
   +------------+-------+----------+
   | name       | price | quantity |
   +------------+-------+----------+
   +------------+-------+----------+
   ```

   your query should return:

   ```
   +----------+
   | quantity |
   +----------+
   | 0        |
   +----------+
   ```

   There are no items.

3. Given:

   ```
   +------------+-------+----------+
   | name       | price | quantity |
   +------------+-------+----------+
   | Backpack   | 99    | 4        |
   | Jacket     | 101   | 2        |
   +------------+-------+----------+
   ```

   your query should return:

   ```
   +----------+
   | quantity |
   +----------+
   | 1        |
   +----------+
   ```

   With $100 we can only afford to buy 1 backpack.

4. Given:

   ```
   +------------+-------+----------+
   | name       | price | quantity |
   +------------+-------+----------+
   | Eraser     | 10    | 3        |
   | Jacket     | 30    | 2        |
   +------------+-------+----------+
   ```

   your query should return:

   ```
   +----------+
   | quantity |
   +----------+
   | 5        |
   +----------+
   ```

   All the items can be bought with $100.

Assume that:

- the `products` table has at most 100 rows;
- `price` column can only contain integers from 1 to 200 inclusive;
- `quantity` column can only contain integers from 1 to 100 inclusive;
- Sum of values in `quantity` column is smaller than or equal to 100.
