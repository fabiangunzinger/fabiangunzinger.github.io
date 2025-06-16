---
title: Another post on CUPED
date: '2023-10-10'
tags:
  - 'datascience, stats'
draft: true
---


<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous" data-relocate-top="true"></script>
<script type="application/javascript">define('jquery', [],function() {return window.jQuery;})</script>


New framing

-   Relation to other approaches

    -   Is CUPED regression adjustment? Identical to regression only in simple case (show FWL link -- have separate post on understanding FWL with relevant regression examples)

    -   Is CUPED DiD? (based on Courthoud) -- same if theta = 1

-   Features of CUPED

    -   Also permits non-linear adjustments (i.e. not reliant on linearity assumptions in OLS)

-   Variance reduction of CUPED: Add section on how CUPED reduces std error or estimator and, via rule of thumb for sample size requirement, increases power! (See my VR talk notes)

Resources:
- https://bookdown.org/ts_robinson1994/10EconometricTheorems/frisch.html
- https://www.evanmiller.org/you-cant-spell-cuped-without-frisch-waugh-lovell.html
- https://towardsdatascience.com/understanding-cuped-a822523641af
- https://en.wikipedia.org/wiki/Linear_regression

``` python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

import src.helpers as hp

%load_ext autoreload
%autoreload 2
```

    The autoreload extension is already loaded. To reload it, use:
      %reload_ext autoreload

CUPED is a re-invention of multiple linear regression. Evan Miller ([here](https://www.evanmiller.org/you-cant-spell-cuped-without-frisch-waugh-lovell.html)) and Matteo Courthoud ([here](https://towardsdatascience.com/understanding-cuped-a822523641af)) make similar points in their excellent posts on the topic, but -- given my starting point -- neither quite helped me fully understand what is going on. This post is my attempt to do that.

In particular, I think that to really understand the connection between multiple linear regression and CUPED, you have to understand the linear algebra of the Frisch-Waugh-Lowell theorem (FWL) rather than just knowing that that theorem says, and to understand that, you have to understand the concept of a projection. The latter two are both well explained in Thomas S. Robinson's wonderful online book [10 Fundamental Theorems for Econometrics](https://bookdown.org/ts_robinson1994/10EconometricTheorems/), on which I draw heavily.

So, here we go.

Load example data

``` python
df_raw = (pd.read_parquet('~/tmp/oneweb-ie.parquet')
          .set_index('date', drop=False)
          .sort_index()
)
```

``` python
df = (df_raw
      .pipe(hp.add_pre_metric_value)
      .pipe(hp.add_treat_effect, effect=1.05)
)
df.head(3)
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

|        | user_id       | order_price | order_price_pre | t   |
|--------|---------------|-------------|-----------------|-----|
| 319393 | JE:IE:1000007 | 23.146154   | 21.619444       | 0   |
| 319399 | JE:IE:1000063 | 13.440000   | 21.250000       | 1   |
| 319400 | JE:IE:1000064 | 19.245001   | 14.700000       | 0   |

</div>

## Linear regression

We generally write the linear regression model as

$$ y = X\beta + \epsilon, $$

where

$$ y = 
 \begin{pmatrix}
  y_{1}\\
  y_{2}\\
  \vdots \\
  y_{k} 
 \end{pmatrix}
$$

is a vector with $n$ outcome variables, one for each unit in the data, $X$ is an $n \times k$ matrix of the form

$$ X = 
 \begin{pmatrix}
  x_{1,1} & x_{1,2} & \cdots & x_{1,k} \\
  x_{2,1} & x_{2,2} & \cdots & x_{2,k} \\
  \vdots  & \vdots  & \ddots & \vdots  \\
  x_{n,1} & x_{n,2} & \cdots & x_{n,k} 
 \end{pmatrix},
$$

which we can think of as a matrix composed of $n$ row vectors stacked on top of each other, with each row vector corresponding to to the $k$ covariate values for a single unit in the data.

$$ \beta = 
 \begin{pmatrix}
  \beta_{1}\\
  \beta_{2}\\
  \vdots \\
  \beta_{k} 
 \end{pmatrix}
$$

is a column vector of $k$ coefficients, and

$$ \epsilon = 
 \begin{pmatrix}
  \epsilon_{1}\\
  \epsilon_{2}\\
  \vdots \\
  \epsilon_{k} 
 \end{pmatrix}
$$

a column vector containing the $n$ error terms.

In our example data, we have $y$ contains order prices, and $X$ the treatment indicator and the pre-experiment period order price. We can estimate the model using OSL. Let's first estimate a model without the pre-experiment data. Then we get:

``` python
# Simple regression model

formula = 'order_price ~ t'
result = smf.ols(formula, data=df).fit()
print(result.summary().tables[1])
print(f"{result.params.t:.10}")
```

    ==============================================================================
                     coef    std err          t      P>|t|      [0.025      0.975]
    ------------------------------------------------------------------------------
    Intercept     23.6222      0.024    972.818      0.000      23.575      23.670
    t              1.1629      0.034     33.865      0.000       1.096       1.230
    ==============================================================================
    1.162933033

We can see that treatment increase order price by about £1.3, which corresponds to the 5 percent treatment effect we created above. So all is well. We also know how to interpret the coefficient estimate of $t$: in general, the interpretation is that "for each one unit increase in t, the order price increases by £1.3 on average". In this case, this is equivalent to saying that if treatment status switches from 0 to 1 -- if a unit is treated -- the order price increases by £1.3 on average.

Now let's add the pre-experiment data.

``` python
# Full model
formula = 'order_price ~ t + order_price_pre'
result = smf.ols(formula, data=df).fit()
print(result.summary().tables[1])
print(f"{result.params.t:.10}")
```

    ===================================================================================
                          coef    std err          t      P>|t|      [0.025      0.975]
    -----------------------------------------------------------------------------------
    Intercept           9.5653      0.042    228.211      0.000       9.483       9.647
    t                   1.1693      0.029     40.341      0.000       1.113       1.226
    order_price_pre     0.6033      0.002    384.477      0.000       0.600       0.606
    ===================================================================================
    1.16933865

The treatment effect estimate is very similar, which is not surprising given that treatment assignment is random and thus uncorrelated with pre-experiment order prices. Notice, however, that the standard error of the treatment effect estimate has decreased, because the the pre-experiment data accounts for some of the variance in the outcome, which means that including it reduces the variance of the residuals.

Usually, we'd now interpret the coefficient on the treatment dummy as "given the value of pre-experiment order price, a change in treatment status from 0 to 1 increases order price by about £1.3 on average".

One way to think about where the 1.3 comes from is to think of it as a (variance) weighted average of the treatment effects of each subgroup with a given pre-experiment order price. But the Frisch-Waugh-Lovell theorem provides us with another useful way to think about this. Let's have a look.

## The Frisch-Waugh-Lovell theorem

### What the theorem says and what it means

For what follows, it will be useful to partition the covariate matrix and coefficient vector from our linear regression model, so that we can write

$$ y = X_{1}\beta_{1} + X_{2}\beta_{2} + \epsilon. $$

This simply says that we now have two sets of covariates. In our example above, for instance, we could include the intercept and the treatment indicator in the first group, and the pre-experiment data in the second group.

Now imagine that we instead estimate

$$ \tilde{y} = \tilde{X}_{1}\beta_{1}^* + \epsilon^*, $$

where $y$ and $X_1$ have been residualised so that $\tilde{y}$ is a vector of residuals from regressing $y$ on $X_2$, and $\tilde{X_1}$ is a vector of residuals from regressing $X_1$ on $X_2$.

The Frisch-Waugh-Lovell theorem (FWL) states that:

$$ \beta_1 = \beta_1^* \hspace{0.5cm}\text{and}\hspace{0.5cm} \epsilon = \epsilon^*. $$

Before we go on, let's verify this.

``` python
# Verifying FWL -- residualised outcome and treatment

order_price_res = smf.ols('order_price ~ order_price_pre', data=df).fit().resid
t_res = smf.ols('t ~ order_price_pre', data=df).fit().resid

formula = 'order_price_res ~ t_res'
result = smf.ols(formula, data=df).fit()
print(result.summary().tables[1])
print(f"{result.params.t_res:.10}")
```

    ==============================================================================
                     coef    std err          t      P>|t|      [0.025      0.975]
    ------------------------------------------------------------------------------
    Intercept   8.482e-14      0.014   5.85e-12      1.000      -0.028       0.028
    t_res          1.1693      0.029     40.341      0.000       1.113       1.226
    ==============================================================================
    1.16933865

FWL works -- the treatment estimate is identical to that estimated in the full model above, and so is the standard error.

But what does it mean? It tells us that when estimating the coefficient of a given covariate, multiple regression only considers the variation in that covariate and the outcome that is not explained by any of the other covariates in the data -- the effect of other covariates are "partialled out". We can thus think about $\beta_1$ as capturing the correlation between the outcome and the $X_1$ covariates when the effects of all $X_2$ covariates on all these variables have been removed -- for a given $X_1$ covariate, think of a scatterplot with a residualised outcome on the y-axis and a residualised covariate on the x-axis.

### Understanding the math

Now that we understand what FWL says, have convinced ourselves that it works, and understand what it means, let's dig deeper and understand the multiple algebra of the theorem, which will then help us see its connection to CUPED in a transparent way.

A more formal way to state FWL is that if we have the regression of interest that contains two separate sets of predictors

$$ y = X_{1}\beta_{1} + X_{2}\beta_{2} + \epsilon, $$

we can estimate $\beta_{1}$ using

$$ M_{2}y = M_{2}X_{1}\beta_{1} + \epsilon, $$

where

$$M_2 = I - X_2(X_2'X_2)^{-1}X_2' = I - P_2$$

is the residual-maker matrix.

## CUPED

$$
\tilde{y} = y - \theta x,
$$

where

$$
\theta = \frac{cov(y, X_2)}{var(X_2)}
$$

which is equivalent to:

$$ M_{2}y = X_{1}\beta_{1} + \mu, $$

In other words, CUPED only residualises the outcome variables instead of the outcome and the treatment indicator. Then why are the results almost identical?

If treatment is perfectly random, then

$$M_{2}T = T$$

Because, in practice, it isn't perfectly random, the results are slighlty different.

``` python
# Traditional CUPED

def cuped_adjust_y(df, y, x):
    data = df.dropna(subset=[y, x])
    cv = np.cov([data[y], data[x]])
    theta = cv[0, 1] / cv[1, 1]
    y, x = data[y], data[x]
    return (y - (x - x.mean()) * theta).fillna(y)

df['order_price_cuped'] = cuped_adjust_y(df, 'order_price', 'order_price_pre')

formula = 'order_price_cuped ~ t'
result = smf.ols(formula, data=df).fit()
print(result.summary().tables[1])
print(f"{result.params.t:.10}")
```

    ==============================================================================
                     coef    std err          t      P>|t|      [0.025      0.975]
    ------------------------------------------------------------------------------
    Intercept     23.6190      0.020   1152.333      0.000      23.579      23.659
    t              1.1693      0.029     40.341      0.000       1.113       1.226
    ==============================================================================
    1.169338264

``` python
# Regression CUPED
formula = 'order_price_res ~ t'
result = smf.ols(formula, data=df).fit()
print(result.summary().tables[1])
print(f"{result.params.t:.10}")
```

    ==============================================================================
                     coef    std err          t      P>|t|      [0.025      0.975]
    ------------------------------------------------------------------------------
    Intercept     -0.5847      0.020    -28.525      0.000      -0.625      -0.544
    t              1.1693      0.029     40.341      0.000       1.113       1.226
    ==============================================================================
    1.169338264

As expected, we get an identical coefficient estimate, and the standard error is identical, too. However, the intercept is effectively zero. This is because we have included an intercept when we created the residualised outcomes, meaning the outcome residuals have mean zero. We can recover the intercept value by adding the variables mean values to the residuals.

``` python
# Add mean values

order_price_res = smf.ols('order_price ~ order_price_pre', data=df).fit().resid + df.order_price.mean()
t_res = smf.ols('t ~ order_price_pre', data=df).fit().resid + df.t.mean()

formula = 'order_price_res ~ t_res'
result = smf.ols(formula, data=df).fit()
print(result.summary().tables[1])
print(f"{result.params.t_res:.10}")
```

    ==============================================================================
                     coef    std err          t      P>|t|      [0.025      0.975]
    ------------------------------------------------------------------------------
    Intercept     25.9690      0.023   1152.903      0.000      25.925      26.013
    t_res          1.2855      0.032     40.355      0.000       1.223       1.348
    ==============================================================================
    1.285500636

CUPED is the same for all practical purposes, but note that the coefficient estimate is not identical.

``` python
# Residualised outcome and full treatment (CUPED)
formula = 'order_price_res ~ t'
result = smf.ols(formula, data=df).fit()
print(result.summary().tables[1])
print(f"{result.params.t:.10}")
```

    ==============================================================================
                     coef    std err          t      P>|t|      [0.025      0.975]
    ------------------------------------------------------------------------------
    Intercept     25.9690      0.023   1152.903      0.000      25.925      26.013
    t              1.2855      0.032     40.355      0.000       1.223       1.348
    ==============================================================================
    1.285500216

Finally, residualised treatment estimate on full outcome has same coefficient estimate, but higher standard error because the outcome variance is larger.

``` python
# Full outcome and residualised treatment
formula = 'order_price ~ t_res'
result = smf.ols(formula, data=df).fit()
print(result.summary().tables[1])
print(f"{result.params.t_res:.10}")
```

    ==============================================================================
                     coef    std err          t      P>|t|      [0.025      0.975]
    ------------------------------------------------------------------------------
    Intercept     25.9690      0.027    972.999      0.000      25.917      26.021
    t_res          1.2855      0.038     34.058      0.000       1.212       1.359
    ==============================================================================
    1.285500636

## Linear regression

## Matrix algebra

We can think of a projection as an operation that maps a vector onto a subspace. The result of a projection is a vector that lies within the subspace and is the closest point in the subspace to the original vector.

Where does the projection matrix come from? [10 Fundamental Theorems for Econometrics](https://bookdown.org/ts_robinson1994/10EconometricTheorems/linear_projection.html#linear_projection) provides a nice example that I'm going to borrow here (the site has a useful visualisation that I'm not going to redraw here). If we have a point $x$ in two dimensional space and a line $L$ in that same space, then the projection of $x$ onto $L$, $\bar{x}$, is the point on $L$ that is closest to $x$. If we think of $L$ as being formed by a vector $v$ and a set of scalar multiples $c$, we want to find the one scalar multiple $c$ for which the Euclidian distance between $x$ and $\bar{x}$, $\sqrt{\sum_i{(\bar{x_i} - x})^2}$ (the index $i$ ranges over all dimensions), is minimised -- we're looking for $\bar{x} = c^*v$, where $c^*$ is the optimal c. Formally, we want to find

\$\$
arg min_c \\

= arg min_c \_i{({x_i} - x})^2 \\

= arg min_c *i{(cv*{i} - x})^2,
\$\$

where the first equality holds because the square root is a monotonic transformation and the second because we have defined as $\bar{x} = c^*v$. To find $c^*$, we can differentiate and setting the result equal to zero

$$
\begin{align*}
\frac{d}{dc} \sum_i{(cv_{i} - x})^2 &= \sum_i{2v_{i}(cv_{i} - x}) \\
& = 2\left(\sum_i{cv_{i}^2} - \sum_i{v_{i}x}\right) \\
&= 2(cv'v - v'x) & \text{using vector notation} \\
&= 0
\end{align*}
$$

and solve for $c$:

$$
\begin{align*}
2(cv'v - v'x) &= 0 \\
cv'v - v'x &= 0 \\
cv'v &= v'x \\
c &= (v'v)^{-1}v'x
\end{align*}
$$

Remembering that $\bar{x} = vc$, we get:

$$
\bar{x} = vc = \underbrace{v(v'v)^{-1}v'}_\text{$P_v$}x,
$$

where $P_v = v(v'v)^{-1}v'$ is the projection matrix of $x$ onto $v$. Once we understand what the projection matrix is -- the function we apply to $x$ to find the nearest point on $v$ -- and know that we define "rearest" as minimising the Euclidean distance, this intimate link between minimising the Euclidean distance and the projection matrix is no surprise.

What does this mean in the context of linear regression? In the context of linear regression, with a covariance matrix $X$, the projection matrix is $P = X(X'X)^{-1}X'$. The coefficient estimates are given by:

$$
\hat{\beta} = (X'X)^{-1}X'y.
$$

and the predicted values are given by:

$$
\hat{y} = X\hat{\beta} = X(X'X)^{-1}X'y = Py.
$$

This tells us that the fitted values in a linear regression are a projection of the vector of observed outcomes, $y$, onto the subspace spanned by $X$.

Finally, the residuals of the linear model are:

$$
\hat{\epsilon} = y - \hat{y} = y - X\hat{\beta} = y - X(X'X)^{-1}X'y = My,
$$

where $M = I - X(X'X)^{-1}X'$. Hence, $M$ is called the residual-maker matrix because it is the matrix that, when pre-multiplied to the vector $y$, returns the vector of residuals.
