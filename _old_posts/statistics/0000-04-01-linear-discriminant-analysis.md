---
title: Linear discriminant analysis
---

-   hide: true
-   toc: true
-   comments: true
-   categories: \[ml, stats\]

``` python
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
```

Advantages over logistic regression:

-   More stable if responses are clearly separated.

-   More stable if featurs are all approximately normally distributed.

-   Often preferrable if response can take more than two classes.

# Sources

-   [An introduction to statistical learning](https://www.statlearning.com)
