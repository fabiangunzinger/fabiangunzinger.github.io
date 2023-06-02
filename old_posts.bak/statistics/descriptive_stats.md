---
title: Descriptive statistics
---

<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
<script type="application/javascript">define('jquery', [],function() {return window.jQuery;})</script>


``` python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from statsmodels.api import ProbPlot

%config InlineBackend.figure_format ='retina'

sns.set_style("whitegrid")
```

### Glossary

-   *Descriptive statistics* is concerned with describing data; *inferential statistics*, with making inferences about a population based on data from a sample.

-   *Stochastic* is a synonym for random. A stochastic process is a random process. The distinction between *stochastics* and *statistics* is that stochastic processes generate the data we analyse in statistics.

### Describing raw data

Types of data and variables

-   Unstructured data

    -   Images, text, [clickstreams](https://www.wordtracker.com/blog/keyword-research/what-is-clickstream-data)

-   Structured data

    -   Numerical data (continuous or discrete, each either on interval or ratio scale)

    -   Categorical data (nominal, binary, ordinal)

-   Variables are properties of some object that can take different values, as opposed to constants.

-   Variable measurements fall into a number of fundamental categories (scales) that have certain properties.

    -   Nominal scale: no order, distances, or ratios (e.g. {'blue', 'green', 'red'})

    -   Ordinal scale: order, but no distances or ratios (e.g. {'small', 'medium', 'large'})

    -   Interval scale: order and distances, but no ratios due to absence of inherent zero point, which refers to the absence of the thing being measured (e.g. temperatures)

    -   Ratio scales: order, distances, and ratios (e.g. height)

-   The scale of measurement determines what statistics it makes sense to calculate (e.g. calculating the mean of a nominal scale makes no sense).

### Summary statistics

#### Centrality

#### Counts, percentages, and proportions

#### Quantiles, percentiles, and the five number summary

-   Quantiles are cut point that divide the range of a probability distribution into invervals with equal probability, or dividing the observations in a sample of groups of the same size ([Wikipedia](https://en.wikipedia.org/wiki/Quantile)).

-   Common quantiles have special names, such as *quartiles*, *deciles*, and *percentiles*.

-   Hence, the xth percentile is the value of a distribution that is larger than or equal to depending on the definition x percent of all values (the precise definition differs, and there are different [methods](https://en.wikipedia.org/wiki/Percentile) for calculating percentiles. But for large datasets this doesn't matter, and we can just use suitable implementations).

``` python
import numpy as np

rng = np.random.default_rng(2312)
x = rng.normal(0, 1, 50)

assert np.quantile(x, .5) == np.percentile(x, 50)
assert np.quantile(x, .1) == np.percentile(x, 10)
```

#### Spread

Variance:

$s_x^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2$

Standard deviation:

$s_x = \sqrt{s_x^2} = \sqrt{\frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2}$

#### Covariance and correlation

-   The covariance is defined as:

$$r_{xy} = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})$$

-   Note that if $y = x$, the covarinace becomes the variance.

Correlation (Pearson's correlation coefficient):

$\rho_{xy} = \frac{r_{xy}}{s_xs_y}$

-   Correlation describes (linear) relationships between variables ("tall people tend to be heavier")
-   The challenge with this is that variables are often not expressed in the same units (height in meters, weight in kg)
-   There are two common solutions to this: standardise variables (leading to the *Pearson correlation coefficient*) or use percentiles (leading to the *Spearman correlation coefficient*)

**Example**

``` python
df = sns.load_dataset('diamonds')[['carat', 'price']]
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

|     | carat | price |
|-----|-------|-------|
| 0   | 0.23  | 326   |
| 1   | 0.21  | 326   |
| 2   | 0.23  | 327   |

</div>

``` python
# Calculating covariance manually

cov = (1 / (len(df) - 1)) * sum((df.carat - df.carat.mean()) * (df.price - df.price.mean()))
cov
```

    1742.7653642651167

``` python
# Calculating variance-covariance matrix
vcm = df.cov()
vcm
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

|       | carat       | price        |
|-------|-------------|--------------|
| carat | 0.224687    | 1.742765e+03 |
| price | 1742.765364 | 1.591563e+07 |

</div>

``` python
# Calculating variance manually

cov = vcm.values[0, 1]
std_carat = np.sqrt(vcm.values[0, 0])
std_price = np.sqrt(vcm.values[1, 1])

corr = cov / (std_carat * std_price)
corr
```

    0.921591301193477

``` python
# Calculating correlation - std matrix
df.corr()
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

|       | carat    | price    |
|-------|----------|----------|
| carat | 1.000000 | 0.921591 |
| price | 0.921591 | 1.000000 |

</div>
