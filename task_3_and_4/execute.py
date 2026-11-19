#!/usr/bin/env python3
"""Run Task 3. Run this inside the python container (it needs the database).

  python task_3_and_4/execute.py seed [FILE]   load test data into the products table
  python task_3_and_4/execute.py sql [FILE]    load test data, then run the solution

FILE is a test-data file (default: task_3_and_4/TestData/test-input-01.py).
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

TASK3 = Path(__file__).resolve().parent
DEFAULT_DATA = TASK3 / "TestData/test-input-01.py"
SOLUTION = TASK3 / "TestData/solution.sql-postgres"


def seed(file):
    subprocess.run([sys.executable, TASK3 / "seed.py", file], check=True)


def sql(file):
    seed(file)
    import psycopg2  # only installed inside the python container

    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    with conn, conn.cursor() as cur:
        cur.execute(SOLUTION.read_text())
        print(" | ".join(column.name for column in cur.description))
        for row in cur.fetchall():
            print(" | ".join(str(value) for value in row))
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["seed", "sql"])
    parser.add_argument("file", nargs="?", default=DEFAULT_DATA)
    args = parser.parse_args()
    if "DATABASE_URL" not in os.environ:
        sys.exit("No database here. Run this inside the python container:\n"
                 "  docker compose up -d\n"
                 "  docker compose exec python bash")
    try:
        {"seed": seed, "sql": sql}[args.command](str(Path(args.file).resolve()))
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)  # the failing command already printed its error
