---
title: Test statistics
---

### A small simulation study

Based on Section 5.6 in IR

``` python
import itertools

import numpy as np
```

``` python
rng = np.random.default_rng(2312)
```

``` python
n = 1000

tau = 0.5

y0 = rng.normal(0, 1, n//2)
y1 = rng.normal(0 + tau, 1, n//2)
y = np.concatenate([y0, y1])

observed_t = abs(y[:n//2].mean() - y[n//2:].mean())

indices = np.arange(n)
treat_indices = list(itertools.combinations(indices, n//2))

test_stats = []

for treat_idx in treat_indices:
    treat_idx = list(treat_idx)
    control_idx = np.delete(indices, treat_idx)
    t = y[treat_idx].mean() - y[control_idx].mean()
    test_stats.append(t)
    
(test_stats >= observed_t).mean()
```

``` python
observed_t = abs(y[:n//2].mean() - y[n//2:].mean())
mean_actual
```

    0.5342832890637125

``` python
y[[1, 2, 3]]
```

    array([ 0.59937606, -1.30027246,  1.52444225])

``` python
np.delete(np.arange(4), [2, 3])
```

    array([0, 1])
