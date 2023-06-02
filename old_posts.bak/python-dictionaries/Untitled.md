``` python
import pandas as pd

s = pd.Series([1, 2, 3, 4, 5, 6])
```

``` python
pd.cut(s, bins=4, right=False, labels=['a', 'b', 'c', 'd'])
```

    0    a
    1    a
    2    b
    3    c
    4    d
    5    d
    dtype: category
    Categories (4, object): ['a' < 'b' < 'c' < 'd']
