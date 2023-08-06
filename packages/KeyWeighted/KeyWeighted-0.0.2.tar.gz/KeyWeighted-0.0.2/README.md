# KeyWeighted

Integrate optional arg `key` to standard library `bisect` and `heapq`.

## Install
```bash
pip install KeyWeighted
```

## Example
```py
# ---------------------- bisect ---------------------- #
import KeyWeighted.bisect as kbisect

a = [-1, -2, -3, -4, -5, -6, -7]
print(kbisect.bisect_left(a, abs(-5), key = abs))
# 4

print(kbisect.bisect_left(None, 100, lo=0, hi=100, key = lambda x: int(x // 2) ** 2))
print(kbisect.bisect_right(None, 100, lo=0, hi=100, key = lambda x: int(x // 2) ** 2))
# 20
# 22

# ---------------------- heapq ----------------------- #

import KeyWeighted.heapq as kheapq

a = ["cat", "apple", "Bob", "SJTU"]
kheapq.heapify(a, key = lambda x: -len(x))
print(a)
# ['apple', 'SJTU', 'Bob', 'cat']

while a:
    print(kheapq.heappop(a, key = lambda x: -len(x)))
# apple
# SJTU
# cat
# Bob
```
