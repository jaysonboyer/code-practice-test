#!/usr/bin/env python3
"""Run the practice tasks.

  python3 task-runner.py task1         run the Task 1 tests
  python3 task-runner.py seed [FILE]   load test data into the products table
  python3 task-runner.py sql [FILE]    load test data, then run the Task 3 solution
  python3 task-runner.py               task1, then sql with the default data

FILE is a test-data file inside task3/ (default: task3/TestData/test-input-01.py).
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_DATA = ROOT / "task3/TestData/test-input-01.py"


def run(*cmd):
    subprocess.run(cmd, cwd=ROOT, check=True)


def task1(_args):
    run(sys.executable, "task1/solution.py")


def seed(args):
    # The seed container sees task3/ as /task3 and works from there.
    try:
        data = Path(args.file).resolve().relative_to(ROOT / "task3")
    except ValueError:
        sys.exit(f"{args.file} must be inside task3/")
    run("docker", "compose", "run", "--rm", "seed", "python", "seed.py", str(data))


def sql(args):
    seed(args)
    run("docker", "compose", "exec", "-T", "postgres", "psql", "-U", "postgres", "codetest",
        "-v", "ON_ERROR_STOP=1", "-f", "/task3/TestData/solution.sql-postgres")


def everything(args):
    task1(args)
    sql(args)


parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.set_defaults(func=everything, file=DEFAULT_DATA)
commands = parser.add_subparsers(title="commands")
commands.add_parser("task1", help="run the Task 1 tests").set_defaults(func=task1)
for name, func, help in [("seed", seed, "load test data"), ("sql", sql, "load test data and run the Task 3 query")]:
    p = commands.add_parser(name, help=help)
    p.add_argument("file", nargs="?", default=DEFAULT_DATA)
    p.set_defaults(func=func)

args = parser.parse_args()
try:
    args.func(args)
except subprocess.CalledProcessError as e:
    sys.exit(e.returncode)  # the failing command already printed its error
