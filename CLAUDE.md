# CLAUDE.md

Coding-test practice repo. See [README.md](README.md) for the task list and run commands.

## Working with the user

- The user is **new to Python**. Explain Python concepts in plain terms when they come up and show the exact command to run.
- The user wants to **solve the tasks together with Claude**, not be handed answers. Guide them step by step: discuss the approach, give hints, review their code and explain mistakes. Write a full solution only when the user asks for one.
- Keep explanations short and concrete. Use small examples.

## Repo facts

- On the host use `python3`, not `python` (only `python3` is installed, 3.14). In the container both work.
- No dependencies and no test framework: test with `assert` statements or an `if __name__ == "__main__":` block.
- `task_1_and_2/solution.py` must keep the signature `def solution(A, B, X, Y)`. The grader imports it.
- All Python runs inside the `python` compose service (built from the root `Dockerfile`, which installs `psycopg2-binary`; repo mounted at `/app`): `docker compose up -d`, then `docker compose exec python bash`. On the host only the Task 1 tests work.
- `python task-runner.py` (in the container) is the entry point: `task1` runs the Task 1 tests, `seed [FILE]` loads test data, `task3 [FILE]` (alias `sql`) seeds then runs `task_3_and_4/TestData/solution.sql-postgres`. No argument runs `task1` then `sql`. The `seed` and `sql` logic lives in `task_3_and_4/execute.py`, which the runner calls; it also runs on its own (`python task_3_and_4/execute.py sql [FILE]`). It uses `psycopg2` and `DATABASE_URL`, not `docker` or `psql`.
- Task 3 targets **PostgreSQL 9.4**, run via `docker-compose.yml` (service `postgres`, db `codetest`, user `postgres`, host port 5433). The SQL must work on 9.4. The Homebrew `postgresql@14` is not used.
- `task_3_and_4/execute.py` runs `task_3_and_4/seed.py`, which truncates `products` and loads a data file. `task_3_and_4/init.sql` creates the table on first start of a fresh volume.
- `task_3_and_4/TestData/test-input-01.py` is SQL inserts, not Python. The seed loads it.
- psql 9.4 runs only one `-c`/`-f` per call.
- Each task folder holds its descriptions, code and written answer: `task_1_and_2/` has `TASK-01.md` and `TASK-02.md`, `task_3_and_4/` has `TASK-03.md` and `TASK-04.md`. Tasks 2 and 4 are written answers about tasks 1 and 3.
- It is a git repo (branch `main`).
