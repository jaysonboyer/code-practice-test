# Car Assembly: Complexity Analysis

Answer to [TASK-02](TASK-02.md) for the solution in [`solution.py`](solution.py).

Every claim below names the input it depends on, the operation that dominates the cost, and the input size it assumes. A bare "O(N)" without those is hard to check, so we always say *N of what* and *doing what*.

## The solution in one paragraph

The function keeps two running totals: `time_on_a`, the fastest time to finish the current position with the car on line A, and `time_on_b`, the same for line B. Once the car is at a position, how it got there no longer matters, only how long it took, so these two numbers are all it needs to carry forward. Each step builds the next pair from the previous one:

```python
time_on_a, time_on_b = (
    min(time_on_a, time_on_b + Y) + A[position],  # stay on A, or switch from B
    min(time_on_b, time_on_a + X) + B[position],  # stay on B, or switch from A
)
```

## Variables and assumptions

| Symbol | Meaning | Expected range | Source |
|---|---|---|---|
| N | number of positions, `len(A)` = `len(B)` | 1 to 100,000 | TASK-01 assumptions |
| A[k], B[k] | install minutes at position k | 1 to 20,000 | TASK-01 assumptions |
| X, Y | switch minutes A → B, B → A | 1 to 20,000 | TASK-01 assumptions |
| answer | the returned total | at most 100,000 × 20,000 = 2,000,000,000 | worst case: every install at the limit, no switches; a switch only ever adds time, so the optimum never exceeds staying on one line |

The values do not change the cost: each addition and `min` costs the same whatever the numbers. Python integers never overflow, so even the 2-billion total needs no special handling (in Java or C it would need a 64-bit type, since it is close to the 32-bit limit of 2,147,483,647).

## Time complexity: O(N)

| Step | Complexity | Dominant operation | Case | Notes |
|---|---|---|---|---|
| Length check | O(1) | `len()` on two lists | all | Python lists store their length |
| Value check | O(N) | one type and range test per element | all | reads 2N + 2 numbers (A, B, X, Y) |
| DP loop | O(N) | two `min` calls and two additions per position | all | runs N − 1 times |
| **`solution` total** | **O(N)** | | best = worst | there is no early exit: every position must be visited, since the last one can change the answer |

Best, typical and worst case are the same: the loop always runs N − 1 times, whatever the numbers. At N = 100,000 the measured run is about 0.05 s (in the repo's Python 3.14 container), so the "efficient" requirement in TASK-01 is met with room to spare.

Why nothing faster is possible: the answer depends on every A[k] and B[k], so any correct solution must read all 2N of them. O(N) is therefore the best achievable.

## Space complexity: O(1) extra

| Step | Complexity | Memory driver | Notes |
|---|---|---|---|
| Inputs A, B | O(N), not counted | the caller's lists | only read, never copied |
| Value check | O(1) | the two-item list `[X, Y]` and the loop variables | fixed size |
| DP loop | O(1) | `time_on_a`, `time_on_b`, `position` | a fixed number of integers, however large N is |
| **`solution` total** | **O(1) extra** | | |

The design choice that buys this: a table `dp[position][line]` would also give O(N) time, but stores 2N numbers when each step only reads the step before it. Keeping just the previous pair gives the same answer in constant memory.

## Alternatives considered

| Approach | Time | Space | Verdict |
|---|---|---|---|
| Try every route | O(2^N · N) | O(N) | correct but impossible at N = 100,000 (2^100,000 routes); used only as a test referee on N ≤ 8 |
| Greedy: cheaper line at each position | O(N) | O(1) | fast but wrong: it ignores switch costs (see the "switch costs more than it saves" test) |
| DP table of every position | O(N) | O(N) | correct, the natural first version; the extra memory buys nothing |
| **Two running totals (chosen)** | **O(N)** | **O(1)** | correct and optimal on both counts |

## Performance budget

- Time: TASK-01 asks for an "efficient" algorithm up to N = 100,000; the measured 0.05 s at that size is well inside any grader limit.
- Memory: constant beyond the inputs.
- No IO, queries, network calls or retries: the function is pure computation.

## Hotspots and benchmarks

- `solution` has no hotspot: one linear pass, no nested loops, no sorting, no recursion.
- The tests hold the only expensive code, on purpose: `brute_force` in `test_solution.py` is O(2^N · N). It runs on N ≤ 8 only (at most 256 routes), 500 times, which takes well under a second. Never call it on real input.
- The "largest input" test is the benchmark: it builds two 100,000-element lists (test-only O(N) memory) and confirms the full-size run finishes and returns 2,000,000,000.

## Test cases

The tests are in [`test_solution.py`](test_solution.py), kept apart so `solution.py` holds only what the grader needs. Run them with `python3 task_1_and_2/test_solution.py` (or `python task-runner.py task1` in the container). Each case carries a description, so a failure says which case broke.

The first four are the examples from TASK-01. The rest are my own:

| Case | Input (A, B, X, Y) | Expected | What it checks |
|---|---|---|---|
| One position | `[5]`, `[3]`, 1, 1 | 3 | N = 1: the loop never runs, so the answer is the faster line |
| A cheaper everywhere | `[1, 1, 1]`, `[5, 5, 5]`, 1, 1 | 3 | the car stays on one line |
| Switch costs more than it saves | `[1, 100, 1]`, `[100, 1, 100]`, 20000, 20000 | 102 | the case greedy gets wrong |
| Switch every position | `[1, 10, 1, 10]`, `[10, 1, 10, 1]`, 1, 1 | 7 | four installs of 1 minute plus three switches of 1 minute |
| Largest input | 100,000 values of 20,000 on each line, 20000, 20000 | 2,000,000,000 | full size runs fast and the large total is exact |
| Invalid input | nine bad inputs: lengths differ, N = 0, N too large, values out of range, a decimal, a bool | `ValueError` | input outside TASK-01's assumptions is rejected, not answered |
| Brute-force cross-check | 500 random inputs, N 1 to 8, costs 1 to 20, fixed seed | same as `brute_force` | checks the recurrence itself, not just hand-picked answers; a seeded generator makes any failure reproducible |

Why the cross-check matters: hand-picked cases only test what the author thought of. Comparing against a slow but obviously correct version tests cases nobody thought of. For example, it catches the classic mistake of updating `time_on_a` before computing `time_on_b` from it (in a trial run that bug failed 68 of the 500 random inputs).
