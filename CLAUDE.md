# CLAUDE.md

Coding-test practice repo. See [README.md](README.md) for the task list and run commands.

## Working with the user

- The user is **new to Python**. Explain Python concepts in plain terms when they come up and show the exact command to run.
- The user wants to **solve the tasks together with Claude**, not be handed answers. Guide them step by step: discuss the approach, give hints, review their code and explain mistakes. Write a full solution only when the user asks for one.
- Keep explanations short and concrete. Use small examples.

## Repo facts

- Use `python3`, not `python` (only `python3` is installed, 3.14).
- No dependencies and no test framework: test with `assert` statements or an `if __name__ == "__main__":` block.
- `task1/solution.py` must keep the signature `def solution(A, B, X, Y)`. The grader imports it.
- `python3 task-runner.py` is the entry point: `task1` runs the Task 1 tests, `seed [FILE]` loads test data, `sql [FILE]` seeds then runs `task3/TestData/solution.sql-postgres`. No argument runs `task1` then `sql`.
- Task 3 targets **PostgreSQL 9.4**, run via `docker-compose.yml` (service `postgres`, db `codetest`, user `postgres`, host port 5433). The SQL must work on 9.4. The Homebrew `postgresql@14` is not used.
- The `seed` compose service runs `task3/seed.py`, which truncates `products` and loads a data file (path relative to `task3/`). `task3/init.sql` creates the table on first start of a fresh volume.
- `task3/TestData/test-input-01.py` is SQL inserts, not Python. The seed loads it.
- psql 9.4 runs only one `-c`/`-f` per call.
- Task descriptions are in `TASK-01.md` … `TASK-04.md`. Tasks 2 and 4 are written answers about tasks 1 and 3.
- Not a git repo.
