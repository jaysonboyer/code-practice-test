#!/usr/bin/env python3
"""Run the practice tasks. Run this inside the python container:

  docker compose up -d
  docker compose exec python bash

  python task-runner.py task1         run the Task 1 tests
  python task-runner.py seed [FILE]   load test data into the products table
  python task-runner.py task3 [FILE]  load test data, then run the Task 3 solution (also: sql)
  python task-runner.py               task1, then task3 with the default data

FILE is a test-data file (default: task_3_and_4/TestData/test-input-01.py).
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_DATA = ROOT / "task_3_and_4/TestData/test-input-01.py"


def run(*cmd):
    subprocess.run(cmd, cwd=ROOT, check=True)


def task1(_args):
    run(sys.executable, "task_1_and_2/solution.py")


def seed(args):
    task3("seed", args)


def sql(args):
    task3("sql", args)


def task3(command, args):
    # Resolve FILE here: it is relative to where the user ran this script.
    run(sys.executable, "task_3_and_4/execute.py", command,
        str(Path(args.file).resolve()))


def everything(args):
    task1(args)
    sql(args)


parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.set_defaults(func=everything, file=DEFAULT_DATA)
commands = parser.add_subparsers(title="commands")
commands.add_parser("task1", help="run the Task 1 tests").set_defaults(func=task1)
for name, func, help in [("seed", seed, "load test data"), ("task3", sql, "load test data and run the Task 3 query"), ("sql", sql, "same as task3")]:
    p = commands.add_parser(name, help=help)
    p.add_argument("file", nargs="?", default=DEFAULT_DATA)
    p.set_defaults(func=func)

args = parser.parse_args()
try:
    args.func(args)
except subprocess.CalledProcessError as e:
    sys.exit(e.returncode)  # the failing command already printed its error
