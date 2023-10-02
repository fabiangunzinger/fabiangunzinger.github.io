---
title: Logging
---

Notes on tools and processes I use for logging and debugging.

A simple logging tool for pandas pipelines from [`scikit-lego`](https://scikit-lego.netlify.app/pandas_pipeline.html).

## Debugging

### [`snoop`](https://github.com/alexmojaki/snoop)

``` python
import snoop

@snoop
def factorial(n):
    return n * factorial(n - 1) if n > 1 else 1

factorial(3)
```

    13:09:50.81 >>> Call to factorial in File "/var/folders/xg/n9p73cf50s52twlnz7z778vr0000gn/T/ipykernel_2405/2397467807.py", line 4
    13:09:50.81 ...... n = 3
    13:09:50.81    4 | def factorial(n):
    13:09:50.81    5 |     return n * factorial(n - 1) if n > 1 else 1
        13:09:50.81 >>> Call to factorial in File "/var/folders/xg/n9p73cf50s52twlnz7z778vr0000gn/T/ipykernel_2405/2397467807.py", line 4
        13:09:50.81 ...... n = 2
        13:09:50.81    4 | def factorial(n):
        13:09:50.81    5 |     return n * factorial(n - 1) if n > 1 else 1
            13:09:50.81 >>> Call to factorial in File "/var/folders/xg/n9p73cf50s52twlnz7z778vr0000gn/T/ipykernel_2405/2397467807.py", line 4
            13:09:50.81 ...... n = 1
            13:09:50.81    4 | def factorial(n):
            13:09:50.81    5 |     return n * factorial(n - 1) if n > 1 else 1
            13:09:50.81 <<< Return value from factorial: 1
        13:09:50.81    5 |     return n * factorial(n - 1) if n > 1 else 1
        13:09:50.81 <<< Return value from factorial: 2
    13:09:50.81    5 |     return n * factorial(n - 1) if n > 1 else 1
    13:09:50.81 <<< Return value from factorial: 6

    6
