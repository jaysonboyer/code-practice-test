# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def solution(A, B, X, Y):
    a, b = A[0], B[0]  # fastest time so far, ending on line A / line B
    for k in range(1, len(A)):
        a, b = min(a, b + Y) + A[k], min(b, a + X) + B[k]
    return min(a, b)


if __name__ == "__main__":
    # The four examples from TASK-01.md
    assert solution([1, 6, 2], [3, 2, 5], 2, 1) == 8
    assert solution([2, 11, 4, 4], [9, 2, 5, 11], 8, 4) == 21
    assert solution([1, 10, 1], [10, 1, 10], 1, 5) == 9
    assert solution([8, 3, 3], [6, 1, 10], 4, 3) == 13
    # Edge case: only one position (N = 1), so pick the faster line
    assert solution([5], [3], 1, 1) == 3
    print("All tests passed!")
