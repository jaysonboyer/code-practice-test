# Code Test

Four coding-test tasks. Each task folder holds the task descriptions (`TASK-0*.md`), the solution and the written answer: `task_1_and_2/` has Tasks 1 and 2, `task_3_and_4/` has Tasks 3 and 4 (Tasks 2 and 4 are questions about 1 and 3).

| Task | What it asks | Where the work goes |
|------|--------------|---------------------|
| [TASK-01](task_1_and_2/TASK-01.md) | Car Assembly: write `solution(A, B, X, Y)` in Python | `task_1_and_2/solution.py` |
| [TASK-02](task_1_and_2/TASK-02.md) | Explain the time and space complexity of Task 1 and add your own test cases | `task_1_and_2/complexity-analysis.md`, tests in `task_1_and_2/test_solution.py` |
| [TASK-03](task_3_and_4/TASK-03.md) | SQL: the most items you can buy for $100 | `task_3_and_4/TestData/solution.sql-postgres` |
| [TASK-04](task_3_and_4/TASK-04.md) | How you would make the Task 3 SQL fast on very large tables | `task_3_and_4/sql-performance.md` |

## Running everything: `task-runner.py`

The Python runs inside a Docker container, so the only thing the Mac needs is Docker. Start the containers, then open a terminal in the `python` one:

```sh
docker compose up -d              # start Postgres and the python container
docker compose exec python bash   # open a terminal inside the python container; leave it with exit
```

Inside that terminal the project folder is `/app` and the command is `python`:

```sh
python task-runner.py                                     # Task 1 tests, then seed + run the Task 3 SQL
python task-runner.py task1                               # Task 1 tests only
python task-runner.py seed                                # load task_3_and_4/TestData/test-input-01.py into the products table
python task-runner.py task3                               # Task 3: load test-input-01.py, then run your query (same as sql)
python task-runner.py task3 task_3_and_4/TestData/test-input-02.py # same, with another test-data file
python task-runner.py --help                              # list the commands
```

It stops with an error if a test fails, the data file is missing, or your SQL has an error. Files you edit on the Mac change inside the container straight away, because the project folder is shared with it.

## Running Python

Run these in the python container's terminal (see above). Both `python` and `python3` work there. On the Mac itself only `python3` is installed, and it can run the Task 1 file but not the database commands. To check the version:

```sh
python3 --version
```

Run all commands from the project folder:

```sh
cd ~/repos/code-practice-test
```

### Running a script

```sh
python3 task_1_and_2/test_solution.py
```

This runs the Task 1 tests: the file imports `solution` from `solution.py` and checks it with `assert` (the same as `python3 task-runner.py task1`). To try other inputs, either add a case to `test_solution.py`, add a block like this to `solution.py`, or call the function from the terminal.

**Option 1: a block at the bottom of `solution.py`** (run it with `python3 task_1_and_2/solution.py`):

```python
if __name__ == "__main__":
    print(solution([1, 6, 2], [3, 2, 5], 2, 1))  # expected 8
```

The `if __name__ == "__main__":` line means "only run this when the file is run directly". The test runner on the coding site imports the file and never runs this block, so you can leave it in.

**Option 2: call the function straight from the terminal without editing the file:**

```sh
python3 -c "import sys; sys.path.insert(0, 'task_1_and_2'); from solution import solution; print(solution([1, 6, 2], [3, 2, 5], 2, 1))"
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
| `postgres` | PostgreSQL 9.4 with a database called `codetest`. On first start `task_3_and_4/init.sql` creates the empty `products` table. Host port **5433** (not 5432, so it doesn't clash with a Homebrew Postgres). |
| `python` | Python 3.14, built from the `Dockerfile`, with the project folder shared at `/app`. It stays running so you can open a terminal in it and run the scripts. |

The easy way is `python task-runner.py sql` in the python container. That calls `task_3_and_4/execute.py`, which runs `task_3_and_4/seed.py` (empties `products`, then loads a test-data file) and then runs your query. `execute.py` also runs on its own (`python task_3_and_4/execute.py sql`).

To work with the database directly, from the Mac:

```sh
docker compose exec postgres psql -U postgres codetest -f /task_3_and_4/TestData/solution.sql-postgres   # run your query
docker compose exec postgres psql -U postgres codetest     # interactive SQL prompt; exit with \q
docker compose down                                        # stop (add -v to also delete the data)
```

Notes:

- `test-input-01.py` contains SQL `insert` statements, not Python, despite the `.py` extension. The seed reads it as SQL.
- Inside the `postgres` container `task_3_and_4/` is mounted at `/task_3_and_4`. Inside the `python` container the whole project is at `/app`.
- The 9.4 `psql` runs only **one** `-c` or `-f` per call. Give it two and it silently runs just the last.
- The `python` container is built from the `Dockerfile`, which installs `psycopg2-binary`. The first `docker compose up -d` builds it (needs internet once). After changing the `Dockerfile` run `docker compose up -d --build`.
