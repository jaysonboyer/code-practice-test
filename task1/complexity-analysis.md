# Car Assembly: Complexity Analysis

The solution keeps two running totals: `a`, the fastest time to finish the current position and end on line A, and `b`, the same for line B. At each position it updates both:

```python
a, b = min(a, b + Y) + A[k], min(b, a + X) + B[k]
```

## Time complexity: O(N)

The loop runs once for each of the N − 1 positions after the first. Each pass does a fixed amount of work: two `min` calls and a few additions. The total work therefore grows in step with N. For the maximum N = 100,000 that is about 100,000 cheap steps.

## Space complexity: O(1)

The function only keeps three numbers (`a`, `b` and the loop index `k`), however long the input is. It creates no new lists. The input lists A and B are only read, so they are not counted as extra space.
