---
title: Penalised regression
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

-   Both are methods to penalise large coefficients.

-   Why would we want to do this? Because we know from bias-variance trade-off -- the U-Shaped curve in complexity-MSE space -- that an increase in bias will result in a reduction of the variance. Now, on some points on that curve, increasing bias by a little might lead to a comparatively large reduction in variance, and thus reduce MSE. Exploiting this possibility is the idea behind penalising large coefficients: biasing coefficients towards zero will introduce a bit of bias, but we hope to get rewarded by lower variance so that overall model performance improves.

## Difference between approaches

-   Ridge uses the sum of L2 norms as the penalty: the sum of the squared coefficients.

-   Lasso used the sum of L1 norms: the sum of absolute coefficients.

-   With lasso, some coefficients might become exactly zero and thus drop out of the model, which is why Lasso is considered a model selection approach.

-   The reason for this is shape of the penalties in coefficient size - penalty space: when we square penalties as in Ridge, that gives us a smooth U-shaped parabola that's fairly flat at teh bottom, meaning that as we move towards zero coefficient size, the reduction in the penalty gets increasingly small and will eventually hit a point where a further reduction in coefficient size is not worth it. In contrast, using absolute penalties leads to a triangle shaped curve with equal (absolute) slope on all points except zero. This means that the marginal gain of moving coefficient size to zero stays constant, so that, for some coefficients, going all the way might be worth it.

## Bayesian intuition behind difference in performance

-   Lasso and ridge regression implicitly assume a world where most coefficients are very small (or zero, in the case of lasso) and don't contribute much to our prediction capacity and only a few are helpful. As opposted to an alternative world where we think most variables we can measure contribute a little bit in equal part to our model's predictive power. Laplace vs gaussian vs uniform distribution of true coefficient values.

-   If the world is truly Laplacian, then biasing our model towards it by using penalised regression will improve the model's performance. If the world is uniform, then penalised regression will perform worse than linear regression.

# Sources

-   [The hundred-page machine learning book](http://themlbook.com)
-   [An introduction to statistical learning](https://www.statlearning.com)
