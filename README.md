# Code Test

Four coding-test tasks. The task descriptions are in the `TASK-0*.md` files.

| Task | What it asks | Where the work goes |
|------|--------------|---------------------|
| [TASK-01](TASK-01.md) | Car Assembly: write `solution(A, B, X, Y)` in Python | `task1/solution.py` |
| [TASK-02](TASK-02.md) | Explain the time and space complexity of Task 1 and add your own test cases | `task1/complexity-analysis.md`, tests in `task1/solution.py` |
| [TASK-03](TASK-03.md) | SQL: the most items you can buy for $100 | `task3/TestData/solution.sql-postgres` |
| [TASK-04](TASK-04.md) | How you would make the Task 3 SQL fast on very large tables | written answer |

## Running everything: `task-runner.py`

One script runs all the tasks. Run it from the project folder:

```sh
python3 task-runner.py                                     # Task 1 tests, then seed + run the Task 3 SQL
python3 task-runner.py task1                               # Task 1 tests only
python3 task-runner.py seed                                # load task3/TestData/test-input-01.py into the products table
python3 task-runner.py sql                                 # load test-input-01.py, then run your Task 3 query
python3 task-runner.py sql task3/TestData/test-input-02.py # same, with another test-data file
python3 task-runner.py --help                              # list the commands
```

It needs `python3` and Docker. The SQL commands start Postgres in Docker for you (see [Running the SQL](#running-the-sql-task-3)). It stops with an error if a test fails, the data file is missing, or your SQL has an error.

## Running Python

On this Mac the command is `python3`. Plain `python` is not installed. To check the version:

```sh
python3 --version
```

Run all commands from the project folder:

```sh
cd ~/repos/code-practice-test
```

### Running a script

```sh
python3 task1/solution.py
```

This runs the file from top to bottom, including the `assert` tests at the bottom (the same as `python3 task-runner.py task1`). To try other inputs, either add lines to that test block or call the function from the terminal.

**Option 1: the test block at the bottom of `solution.py`:**

```python
if __name__ == "__main__":
    print(solution([1, 6, 2], [3, 2, 5], 2, 1))  # expected 8
```

The `if __name__ == "__main__":` line means "only run this when the file is run directly". The test runner on the coding site imports the file and never runs this block, so you can leave it in.

**Option 2: call the function straight from the terminal without editing the file:**

```sh
python3 -c "import sys; sys.path.insert(0, 'task1'); from solution import solution; print(solution([1, 6, 2], [3, 2, 5], 2, 1))"
```

### Checking answers with `assert`

`assert` stops the program with an error when a condition is false. That makes it a quick way to test without installing anything:

```python
assert solution([1, 6, 2], [3, 2, 5], 2, 1) == 8
assert solution([2, 11, 4, 4], [9, 2, 5, 11], 8, 4) == 21
print("all tests passed")
```

### Interactive Python

Run `python3` on its own to open a prompt (`>>>`) where you can type Python and see results immediately. Exit with `exit()` or Ctrl-D.

## Running the SQL (Task 3)

The solution must run on **PostgreSQL 9.4**. `docker-compose.yml` runs it in Docker, so nothing needs installing on the Mac.

| Service | What it does |
|---------|--------------|
| `postgres` | PostgreSQL 9.4 with a database called `codetest`. On first start `task3/init.sql` creates the empty `products` table. Host port **5433** (not 5432, so it doesn't clash with a Homebrew Postgres). |
| `seed` | A Python container that runs `task3/seed.py`: empties `products`, then loads a test-data file. Runs once on `docker compose up`, then exits. |

The easy way is `python3 task-runner.py sql`. The same steps by hand:

```sh
docker compose up -d                                       # start Postgres and seed it with test-input-01.py
docker compose run --rm seed python seed.py TestData/test-input-02.py   # re-seed from another file (path is inside task3/)
docker compose exec postgres psql -U postgres codetest -f /task3/TestData/solution.sql-postgres   # run your query
docker compose exec postgres psql -U postgres codetest     # interactive SQL prompt; exit with \q
docker compose down                                        # stop (add -v to also delete the data)
```

Notes:

- `test-input-01.py` contains SQL `insert` statements, not Python, despite the `.py` extension. The seed reads it as SQL.
- Inside the containers `task3/` is mounted at `/task3`.
- The 9.4 `psql` runs only **one** `-c` or `-f` per call. Give it two and it silently runs just the last.
- The `seed` container downloads `psycopg2-binary` each time it runs, so it needs internet access.
