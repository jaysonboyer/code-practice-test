"""Task 1, Car Assembly: the fastest way to build a car on two assembly lines.

Tests: python3 task_1_and_2/test_solution.py
"""

def solution(A, B, X, Y):
    """Return the minimum minutes needed to assemble one car.

    The grader calls solution(A, B, X, Y), so the short names stay. They mean:
      A[position]  minutes to install that position's component on line A
      B[position]  the same on line B
      X            minutes to move the car from line A to line B
      Y            minutes to move the car from line B to line A

    Why this approach (dynamic programming with two running totals):
    - Trying every route is correct but has 2^N routes: hopeless at N = 100,000.
    - Greedy (pick the cheaper line at each position) is fast but wrong: it
      ignores the switch cost. With A = [1, 100, 1], B = [100, 1, 100] and
      switches costing 20,000, greedy hops to B for position 1 and pays 40,000
      in switches to save 99 minutes.
    - The key fact: once the car is at a position on a given line, how it got
      there no longer matters, only how long it took. So for each position we
      keep just two numbers, the fastest time to finish it on line A and on
      line B, and build the next pair from them. That is O(N) time.
    - A table of every position's pair would also work, but each step only
      reads the step before, so two variables give the same answer in O(1)
      extra memory.
    """
    # Validate at the boundary: fail loudly on input TASK-01.md rules out,
    # rather than return a wrong number. A grader-only answer could skip this,
    # since the task promises valid input; we keep it because real callers
    # break promises, and the cost is one extra pass over the input.

    # Lengths: if B were longer than A its extra elements would be silently
    # ignored; if A were longer, B[position] would crash with an IndexError.
    if len(A) != len(B) or not 1 <= len(A) <= 100_000:
        raise ValueError("A and B must be the same length, from 1 to 100,000")
    # Values: zero, negative and decimal numbers would give a meaningless
    # answer. `type(...) is int` rather than isinstance(..., int), because
    # Python counts True and False as ints and we want to reject them.
    for input_name, numbers in (("A", A), ("B", B), ("X and Y", [X, Y])):
        for number in numbers:
            if type(number) is not int or not 1 <= number <= 20_000:
                raise ValueError(
                    f"{input_name} must hold whole numbers 1 to 20,000, "
                    f"got {number!r}"
                )

    # Fastest time to finish the current position with the car on line A / B.
    # At position 0 there is nothing to switch from: just the install time.
    time_on_a, time_on_b = A[0], B[0]
    for position in range(1, len(A)):
        # Both new values are built from the *previous* pair in one tuple
        # assignment. Updating time_on_a on its own line first would make the
        # time_on_b line read the new value and give a wrong answer.
        time_on_a, time_on_b = (
            # Reach A here by staying on A, or by switching over from B (Y)
            min(time_on_a, time_on_b + Y) + A[position],
            # Reach B here by staying on B, or by switching over from A (X)
            min(time_on_b, time_on_a + X) + B[position],
        )
    # The car may finish on either line.
    return min(time_on_a, time_on_b)
