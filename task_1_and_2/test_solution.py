"""Tests for the Task 1 solution. Run with: python3 task_1_and_2/test_solution.py

They live in their own file so solution.py holds only what the grader needs,
and so test-only code (brute_force) is never shipped with the answer.
"""
import itertools
import random

# Python puts this file's folder on the import path, so this finds solution.py
# next to it, the same way the grader imports it.
from solution import solution


def brute_force(A, B, X, Y):
    """Try every route and return the fastest.

    It takes 2^N time, so only small inputs, but it is so direct it is
    easy to trust. Comparing it with solution() on many random inputs
    checks the clever version against the obvious one.
    """
    def route_time(lines):  # lines is a tuple such as ("A", "B", "A")
        total = A[0] if lines[0] == "A" else B[0]
        for position in range(1, len(lines)):
            if lines[position] != lines[position - 1]:
                total += X if lines[position] == "B" else Y
            total += A[position] if lines[position] == "A" else B[position]
        return total

    every_route = itertools.product("AB", repeat=len(A))
    return min(route_time(lines) for lines in every_route)


MAX_POSITIONS = 100_000

# Each case: (what it checks, (A, B, X, Y), expected minutes)
VALID_CASES = [
    ("TASK-01 example 1", ([1, 6, 2], [3, 2, 5], 2, 1), 8),
    ("TASK-01 example 2", ([2, 11, 4, 4], [9, 2, 5, 11], 8, 4), 21),
    ("TASK-01 example 3", ([1, 10, 1], [10, 1, 10], 1, 5), 9),
    ("TASK-01 example 4", ([8, 3, 3], [6, 1, 10], 4, 3), 13),
    ("one position: the loop never runs, pick the faster line",
     ([5], [3], 1, 1), 3),
    ("A cheaper everywhere: never switch (1 + 1 + 1)",
     ([1, 1, 1], [5, 5, 5], 1, 1), 3),
    ("switch costs more than it saves: stay on A (1 + 100 + 1)",
     ([1, 100, 1], [100, 1, 100], 20_000, 20_000), 102),
    ("switch every position: 4 installs + 3 switches of 1 minute",
     ([1, 10, 1, 10], [10, 1, 10, 1], 1, 1), 7),
    ("largest input: 100,000 positions of 20,000 minutes each",
     ([20_000] * MAX_POSITIONS, [20_000] * MAX_POSITIONS, 20_000, 20_000),
     2_000_000_000),
]

# Each case: (what is wrong, (A, B, X, Y)). All must raise ValueError.
INVALID_CASES = [
    ("A and B differ in length", ([1], [1, 2], 1, 1)),
    ("no positions (N = 0)", ([], [], 1, 1)),
    ("too many positions",
     ([1] * (MAX_POSITIONS + 1), [1] * (MAX_POSITIONS + 1), 1, 1)),
    ("value below 1", ([0], [1], 1, 1)),
    ("value above 20,000", ([1], [20_001], 1, 1)),
    ("value not a whole number", ([1.5], [1], 1, 1)),
    ("value is a bool", ([True], [1], 1, 1)),
    ("X below 1", ([1], [1], 0, 1)),
    ("Y above 20,000", ([1], [1], 1, 20_001)),
]


def test_valid_cases():
    for description, (A, B, X, Y), expected in VALID_CASES:
        actual = solution(A, B, X, Y)
        assert actual == expected, f"{description}: got {actual}, want {expected}"


def test_invalid_cases():
    for description, bad_input in INVALID_CASES:
        try:
            solution(*bad_input)  # * unpacks the tuple into A, B, X, Y
        except ValueError:
            continue
        raise AssertionError(f"expected ValueError: {description}")


def test_matches_brute_force():
    # 500 small random inputs. Small costs (1 to 20) make switching worthwhile
    # often, so both branches of each min() get exercised. A fixed seed makes
    # every run test the same inputs, so a failure can be reproduced.
    random_source = random.Random(2026)
    for _ in range(500):
        size = random_source.randint(1, 8)
        random_input = (
            [random_source.randint(1, 20) for _ in range(size)],
            [random_source.randint(1, 20) for _ in range(size)],
            random_source.randint(1, 20),
            random_source.randint(1, 20),
        )
        assert solution(*random_input) == brute_force(*random_input), random_input


if __name__ == "__main__":
    # No test framework in this repo: call each test function directly.
    test_valid_cases()
    test_invalid_cases()
    test_matches_brute_force()
    print("All tests passed!")
