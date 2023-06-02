---
title: Analysis
---

<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
<script type="application/javascript">define('jquery', [],function() {return window.jQuery;})</script>


### Fisher's exact p-value approach

### Neymans's repeated sampling approach

-   Based on Chapter 6 in IR

-   Motivating questions: What would be the difference between average outcomes if some units were assigned to a treatment and others weren't? Can we create confidence intervals for such an average treatment effect?

#### Difference in means estimator

The estimand of interest, the average treatment effect (ATE) for the sample for which we have data (the "finite sample"), is:

$$
\tau_{fs} = \frac{1}{N}\sum_{i=1}^{N}\left(Y_i(1) - Y_i(0)\right) = \bar{Y}(1) - \bar{Y}(0).
$$

Neyman's proposed estimator is:

$$
\hat{\tau}^{dif} = \frac{1}{N_t}\sum_{i:W_i = 1}Y_i^{obs} - \frac{1}{N_c}\sum_{i:W_i = 0}Y_i^{obs} =  \bar{Y}_{t}^{obs} - \bar{Y}_{c}^{obs},
$$

which can be rewritten as (useful way to think about it!):

$$
\hat{\tau}^{dif} = \frac{1}{N_t} \sum_{i=1}^N W_i Y_i(1) - \frac{1}{N_c}\sum_{i=1}^N (1 - W_i) Y_i(0) \\
= \frac{1}{N} \sum_{i=1}^N \left( \frac{N}{N_t} W_i Y_i(1) - \frac{N}{N_c} (1 - W_i) Y_i(0) \right)
$$

and shown to be an unbiased estimator of the average treatment effect.

#### Sampling variance of the difference in means estimator

The estimand is:

$$
V_w\left(\bar{Y}_t^{obs} - \bar{Y}_c^{obs}\right) = S_t^2 + S_c^2 - S_{ct}^2,
$$

where $S_t^2$ and $S_c^2$ are the variances of $Y(1)$ and $Y(0)$ in the sample, and $S_{ct}^2$ is the sample variance of the unit-level treatment effects. The reason this expression is complicated is that in a completely randomised experiment, with $N_t$ units allocated to treatment, unit-level treatment assignments are not independent (since one unit being allocated to treatment lowers the probability of being allocated to treatment for all remaining units).

Because we never observe both potential outcomes, there is no hope of estimating the sample variance of unit-level treatment effects.

A commonly used estimator (recommended in practice by IR!) is:

$$
\hat{V}^{neyman} = \frac{s_t^2}{N_t} + \frac{s_c^2}{N_c},
$$

where $s_t^2$ and $s_c^2$ are unbiased estimators of $S_t^2$ and $S_c^2$. This estimator is popular for a few reasons:

1.  If treatment effects are constant across units, then this is an unbiased estimator of the true sampling variance of $\bar{Y}_t^{obs} - \bar{Y}_c^{obs}$.

2.  If treatment effects are not constant, then this is a conservative estimator of the sampling variance (since $S_{ct}^2$ is non-negative).

3.  It is always unbiased for $\hat{\tau}^{dif}$ as an estimator of the infinite super-population average treatment effect (see below).

There are other options (see Section 6.5 in the IR book).

#### Confidence intervals and testing

-   Given $\hat{\tau}^{dif}$ and $\hat{V}^{neyman}$, we can calculate confidence intervals and test statistics in the usual way.

#### Inference for population average treatment effects

An alternative perspective is to think of the $N$ observations we observe as a random sample from a infinitely large super-population, and to think of the estimated treatment effect as an estimate of the average treatment effect for that larger population.

In this case, the estimand of interest is:

$$
\tau_{sp} = \mathop{\mathbb{E}_{sp}}[Y_i(1) - Y_i(0)],
$$

and $\hat{\tau}^{dif}$ and $\hat{V}^{neyman}$ are unbiased estimators of its mean and variance.

### Regression methods for completely randomised experiments

## Using regression

Based on Imbens and Rubin chapter 7

-   Using OLS to estimate ATE is virtually equivalent to Neyman approach of t-test for whether average difference is zero
-   With covariates, ATE only unbiased asymptotically (not major issue with large samples in tech companies)

### Unclustered example

``` python
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
```

``` python
rng = np.random.default_rng(2312)
n = 1000

df = pd.DataFrame({
    "pre": rng.normal(2, 2, n),
    "post": np.concatenate([rng.normal(2, 2, int(n/2)), rng.normal(3, 2, int(n/2))]),
    "t": [0] * int(n/2) + [1] * int(n/2)
}).assign(d=lambda df: df.post - df.pre)
df.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

|     | pre      | post      | t   | d         |
|-----|----------|-----------|-----|-----------|
| 0   | 0.208084 | -1.620337 | 0   | -1.828421 |
| 1   | 0.730465 | 3.940700  | 0   | 3.210235  |
| 2   | 3.471432 | 5.558608  | 0   | 2.087176  |
| 3   | 0.585465 | 1.881073  | 0   | 1.295608  |
| 4   | 0.961117 | 2.281668  | 0   | 1.320551  |

</div>

``` python
# t-test
stats.ttest_ind(df[df.t.eq(1)].d, df[df.t.eq(0)].d)
```

    Ttest_indResult(statistic=4.186092154991707, pvalue=3.088414843886731e-05)

``` python
# using regression
m = smf.ols('d ~ t', data=df).fit()
print(m.summary())
```

                                OLS Regression Results                            
    ==============================================================================
    Dep. Variable:                      d   R-squared:                       0.017
    Model:                            OLS   Adj. R-squared:                  0.016
    Method:                 Least Squares   F-statistic:                     17.52
    Date:                Fri, 08 Jul 2022   Prob (F-statistic):           3.09e-05
    Time:                        10:44:32   Log-Likelihood:                -2461.0
    No. Observations:                1000   AIC:                             4926.
    Df Residuals:                     998   BIC:                             4936.
    Df Model:                           1                                         
    Covariance Type:            nonrobust                                         
    ==============================================================================
                     coef    std err          t      P>|t|      [0.025      0.975]
    ------------------------------------------------------------------------------
    Intercept      0.0931      0.127      0.733      0.463      -0.156       0.342
    t              0.7514      0.179      4.186      0.000       0.399       1.104
    ==============================================================================
    Omnibus:                        0.687   Durbin-Watson:                   2.054
    Prob(Omnibus):                  0.709   Jarque-Bera (JB):                0.632
    Skew:                           0.061   Prob(JB):                        0.729
    Kurtosis:                       3.023   Cond. No.                         2.62
    ==============================================================================

    Notes:
    [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.

``` python
m.tvalues['t'], m.pvalues['t']
```

    (4.186092154991713, 3.088414843886643e-05)

## dev

``` python
num_units = 100
num_a = 20
num_b = 20

df = pd.DataFrame({
    "id": list(range(num_units)) * num_a,
    0: rng.normal(2, 2, num_units * num_a),
    1: rng.normal(2.5, 2, num_units * num_b),
}).melt(id_vars='id', var_name='t').sort_values(['id', 't']).reset_index(drop=True)
df.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

|     | id  | t   | value    |
|-----|-----|-----|----------|
| 0   | 0   | 0   | 2.156616 |
| 1   | 0   | 0   | 7.183623 |
| 2   | 0   | 0   | 2.244507 |
| 3   | 0   | 0   | 2.024742 |
| 4   | 0   | 0   | 1.231280 |

</div>

**Approach 1: calculate id-level treatment effects and use one-sample t-test to test whether average zone-level effect is non-zero.**

``` python
df_id = df.groupby(['id', 't']).mean()

data = df_id.unstack().reset_index(drop=True)
data.columns = data.columns.droplevel()
data['d'] = data[1] - data[0]

stats.ttest_1samp(data.d, popmean=0)
```

    Ttest_1sampResult(statistic=9.591436751029837, pvalue=8.51962162549687e-16)

**Approach 2: calculate zone level effects and then use OLS to calculate t-statistic**

``` python
data = df_id.reset_index()
m = smf.ols('value ~ t + id', data=data).fit()
print(m.summary())
```

                                OLS Regression Results                            
    ==============================================================================
    Dep. Variable:                  value   R-squared:                       0.330
    Model:                            OLS   Adj. R-squared:                  0.323
    Method:                 Least Squares   F-statistic:                     48.58
    Date:                Fri, 08 Jul 2022   Prob (F-statistic):           7.07e-18
    Time:                        10:59:40   Log-Likelihood:                -113.61
    No. Observations:                 200   AIC:                             233.2
    Df Residuals:                     197   BIC:                             243.1
    Df Model:                           2                                         
    Covariance Type:            nonrobust                                         
    ==============================================================================
                     coef    std err          t      P>|t|      [0.025      0.975]
    ------------------------------------------------------------------------------
    Intercept      1.9717      0.068     29.157      0.000       1.838       2.105
    t              0.5998      0.061      9.857      0.000       0.480       0.720
    id          6.865e-05      0.001      0.065      0.948      -0.002       0.002
    ==============================================================================
    Omnibus:                       11.600   Durbin-Watson:                   2.088
    Prob(Omnibus):                  0.003   Jarque-Bera (JB):               11.941
    Skew:                          -0.550   Prob(JB):                      0.00255
    Kurtosis:                       3.474   Cond. No.                         146.
    ==============================================================================

    Notes:
    [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.

-   Why is this different?

## Overall framework:

-   In experiments, assignment uncertainty matters more than sampling uncertainty. Assignment uncertainty results from randomness created by treatment assignment (different assignment will give different ATE estimates), sampling uncertainty results from randomness created by drawing a sample from a larger population for your experiment (different samples lead to different results). Which is more important depends on how large your sample is relative to population. Model integrating both: https://arxiv.org/pdf/1706.01778.pdf

-   If analysis unit is randomisation unit:

    -   Simple means estimater is unbiased.
    -   Adding covariates can lead to bias (compare with simple means estimater to determine whether this is to) and to worse inference (always interact covariates with treatment)

-   If randomisation unit is coarser than analysis unit (i.e. cluster randomisation):

    -   Simple means estimator is biased if there is a correlation between cluster total and cluster size.

    -   Solution is to use Des Raj estimator.

## Assumptions

-   Stable Unit Treatment Value Assumption (SUTVA): unit treatment value independent of treatment status of other units.

## Randomisation unit = analysis unit

-   Review OLS assumptions under sampling uncertainty (standard). What changes if we also have assignment uncertainty (e.g. in experiments?)

-   OLS no longer unbiassed with experimental data, though bias very small for large samples. Adding controls problematic (freedman2008, lin2013agnostic): always interact.

-   Use robust std errors: `cov_type=HCO` in Python (to allow for different variances in treat and control)

## Cluster randomised trial

Entire discussion based \[this\] talk by Matthias Lux, which walks through [Middleton and Aronow (2015)](https://joelmidd.github.io/papers/MiddletonAronow_Cluster%20Randomized.pdf).

Context: food delivery, randomising at the user level but analysis at order level.

Basic difference in means estimator is:

$$
\hat{\tau} = \frac{\sum_{i \in J_t}\sum_{j=1}^{n^o_i}Y_{ij}}{\sum_{i \in J_t}n^o_i}
           - \frac{\sum_{i \in J_c}\sum_{j=1}^{n^o_i}Y_{ij}}{\sum_{i \in J_c}n^o_i}
           = \frac{\sum_{i \in J_t}Y_{i}}{\sum_{i \in J_t}n^o_i}
           - \frac{\sum_{i \in J_c}Y_{i}}{\sum_{i \in J_c}n^o_i}
$$

where: $J_t$ and $J_c$ are the sets of treatment and control users, $n^o_i$ is the number of orders by user $i$, and $Y_{ij}$ is the value of order $j$ of user $i$.

Problems:
- Main difference to above case is that denominators are random variables (we don't know in advance how many orders users are going to place).
- This creates bias if there is a correlation between the cluster totals ($Y_i$) and the number of observations per cluster ($n^o_i$).
- Standard errors invalid because iid assumption violated. Can cluster, but they can be unreliable if cluster sizes are highly skewed.

Slide below:
- Distribution from simulation has two problems:
- Much more mass in tails (can largely be solved by clustering)
- Bimodal shape due to massive outlier - one mode if outlier in treatment, one if in control (solved by Des Raj estimator)

<img src="img/lux_slide.png" alt="Drawing" style="width: 500px;"/>

#### Des Raj estimator

-   Challenge is to determine k, which is a prior estimate (i.e. from data that's not in the experiment) of the correlation between cluster totals ($Y_i$) and the number of observations per cluster ($n^o_i$).
-   However, in many contexts (e.g. tech companies) we can estimate this based on historical data.

To implement in regression, use following:

Regress X on D, where X:

$$
X_i) = \frac{N}{N^o}Y_i - k\left(\frac{N}{N^o}n_i^o - 1\right)
$$

where $N$ is total number of clusters and $N^o$ is total number of orders.

And use `cov_type=HCO` std errors.

Applications:
- When randomising at city level and analysing at order level (i.e. large "gap" between randomisation and analysis unit)

Sources:

-   Rubin causal framework paper: https://www.tandfonline.com/doi/abs/10.1198/016214504000001880
