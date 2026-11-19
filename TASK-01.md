# Car Assembly

In a car factory there are two assembly lines, called A and B. Each of them consists of N positions numbered from 0 to N−1. In each position, some component is installed into the car being assembled. The lines are symmetric; that is, the same component is installed into the car in the corresponding positions of A and B.

In order to assemble a car, it needs to get through all of the positions on the assembly lines. It takes `A[K]` minutes to install the component in the K-th position on line A, and `B[K]` minutes to install it on line B.

After installing a component in the K-th position, the car can either be moved to the next position on the same line (which happens automatically and takes 0 minutes) or it can be moved to the other line. Switching from line A to line B takes X minutes, and switching from line B to line A takes Y minutes.

The assembly process can be started in either line.

Write a function:

```python
def solution(A, B, X, Y)
```

that, given arrays A and B consisting of N integers each, and integers X and Y, returns the minimum time required to assemble an entire car.

**Examples:**

1. Given `A = [1, 6, 2]`, `B = [3, 2, 5]`, `X = 2` and `Y = 1`, the function should return 8. The assembly of the car can start in line A. After installing the component in position number 0 (1 minute), the car can be moved to assembly line B (2 minutes) to install the component in position number 1 (2 minutes), and move the car back to line A (1 minute), where the last component would be installed (2 minutes). The total time is 1 + 2 + 2 + 1 + 2 = 8.
2. Given `A = [2, 11, 4, 4]`, `B = [9, 2, 5, 11]`, `X = 8` and `Y = 4`, the function should return 21. It is optimal to assemble the entire car on line A.
3. Given `A = [1, 10, 1]`, `B = [10, 1, 10]`, `X = 1` and `Y = 5`, the function should return 9.
4. Given `A = [8, 3, 3]`, `B = [6, 1, 10]`, `X = 4` and `Y = 3`, the function should return 13.

Write an **efficient** algorithm for the following assumptions:

- N is an integer within the range [1..100,000];
- each element of arrays A and B is an integer within the range [1..20,000];
- X and Y are integers within the range [1..20,000].
