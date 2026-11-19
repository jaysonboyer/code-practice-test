# Car Assembly: Complexity Analysis

The solution keeps two running totals: `time_on_a`, the fastest time to finish the current position and end on line A, and `time_on_b`, the same for line B. At each position it updates both:

```python
time_on_a, time_on_b = (
    min(time_on_a, time_on_b + Y) + A[position],
    min(time_on_b, time_on_a + X) + B[position],
)
```

## Time complexity: O(N)

The loop runs once for each of the N − 1 positions after the first. Each pass does a fixed amount of work: two `min` calls and a few additions. Before the loop, the input validation reads every element of A and B once, which is also O(N). The total work therefore grows in step with N. For the maximum N = 100,000 that is about 100,000 cheap steps.

## Space complexity: O(1)

The function only keeps a few numbers (`time_on_a`, `time_on_b`, the loop index `position` and the `value` being validated), however long the input is. The only list it creates is the two-item `[X, Y]`, which has a fixed size. The input lists A and B are only read, so they are not counted as extra space.

## Test cases

The tests are `assert` statements at the bottom of `solution.py`. Run them with `python3 task_1_and_2/solution.py`.

The first four are the examples from the task description. The rest are my own:

| Case | Input (A, B, X, Y) | Expected | What it checks |
|---|---|---|---|
| One position | `[5]`, `[3]`, 1, 1 | 3 | N = 1: the loop never runs, so the answer is the faster line. |
| No switching | `[1, 1, 1]`, `[5, 5, 5]`, 1, 1 | 3 | Line A is cheaper everywhere, so the car stays on it. |
| Switching too expensive | `[1, 100, 1]`, `[100, 1, 100]`, 20000, 20000 | 102 | Line B is cheaper at position 1, but the switch costs more than it saves. |
| Switch every position | `[1, 10, 1, 10]`, `[10, 1, 10, 1]`, 1, 1 | 7 | Four installs of 1 minute plus three switches of 1 minute. |
| Maximum size | 100,000 values of 20,000 on each line, 20000, 20000 | 2,000,000,000 | The largest allowed input finishes quickly and the large total is handled. |
| Invalid input | Eight bad inputs: different lengths, N = 0, N too large, values out of range, a non-whole number | `ValueError` | Input that breaks the task's assumptions is rejected. |
