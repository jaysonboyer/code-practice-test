# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def solution(A, B, X, Y):
    # Reject input that breaks the assumptions in TASK-01.md. Without these
    # checks, much bad input returns a wrong answer instead of failing.

    # Lengths: if B is longer than A, its extra elements are silently ignored.
    # If A is longer than B, or both are empty, the code below crashes with an
    # unhelpful IndexError.
    if len(A) != len(B) or not 1 <= len(A) <= 100_000:
        raise ValueError("A and B must be the same length, from 1 to 100,000")
    # Values: zero, negative and decimal numbers all produce an answer, but a
    # meaningless one. Text crashes with a TypeError, or with N = 1 is returned
    # as the answer. Values above 20,000 would still add up correctly (Python
    # integers do not overflow) but are outside what the task allows.
    for values in (A, B, [X, Y]):
        for value in values:
            if type(value) is not int or not 1 <= value <= 20_000:
                raise ValueError(
                    f"values must be whole numbers 1 to 20,000, got {value!r}"
                )

    # Fastest time so far, ending on line A / line B
    time_on_a, time_on_b = A[0], B[0]
    for position in range(1, len(A)):
        time_on_a, time_on_b = (
            # Stay on A, or switch over from B
            min(time_on_a, time_on_b + Y) + A[position],
            # Stay on B, or switch over from A
            min(time_on_b, time_on_a + X) + B[position],
        )
    return min(time_on_a, time_on_b)


if __name__ == "__main__":
    # The four examples from TASK-01.md
    assert solution([1, 6, 2], [3, 2, 5], 2, 1) == 8
    assert solution([2, 11, 4, 4], [9, 2, 5, 11], 8, 4) == 21
    assert solution([1, 10, 1], [10, 1, 10], 1, 5) == 9
    assert solution([8, 3, 3], [6, 1, 10], 4, 3) == 13
    # Edge case: only one position (N = 1), so pick the faster line
    assert solution([5], [3], 1, 1) == 3
    # No switching: line A is cheaper everywhere, so stay on it (1 + 1 + 1)
    assert solution([1, 1, 1], [5, 5, 5], 1, 1) == 3
    # Switching too expensive: B is cheaper at position 1, but moving there
    # costs 20,000, so stay on A (1 + 100 + 1)
    assert solution([1, 100, 1], [100, 1, 100], 20000, 20000) == 102
    # Switch at every position: 4 installs of 1 minute + 3 switches of 1 minute
    assert solution([1, 10, 1, 10], [10, 1, 10, 1], 1, 1) == 7
    # Maximum size: N = 100,000 and every value at its limit of 20,000.
    # Both lines cost the same, so never switch: 100,000 * 20,000
    N = 100_000
    assert solution([20000] * N, [20000] * N, 20000, 20000) == 2_000_000_000
    # Invalid input: each of these must raise ValueError
    bad_inputs = [
        ([1], [1, 2], 1, 1),           # A and B have different lengths
        ([], [], 1, 1),                # N = 0
        ([1] * (N + 1), [1] * (N + 1), 1, 1),  # N too large
        ([0], [1], 1, 1),              # element below 1
        ([1], [20001], 1, 1),          # element above 20,000
        ([1.5], [1], 1, 1),            # element is not a whole number
        ([1], [1], 0, 1),              # X below 1
        ([1], [1], 1, 20001),          # Y above 20,000
    ]
    for args in bad_inputs:
        try:
            solution(*args)  # *args unpacks the tuple into A, B, X, Y
            assert False, f"expected ValueError for {args}"
        except ValueError:
            pass
    print("All tests passed!")
