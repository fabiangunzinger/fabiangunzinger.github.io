---
title: Power curves
---

<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
<script type="application/javascript">define('jquery', [],function() {return window.jQuery;})</script>


Based on [this](https://deliveroo.engineering/2018/12/07/monte-carlo-power-analysis.html) post from Deliveroo engineering blog.

``` python
import random

import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import bernoulli, binom, mannwhitneyu, norm, uniform
import seaborn as sns
from statsmodels.stats.weightstats import ttest_ind

sns.set_style("whitegrid")
%config InlineBackend.figure_format ='retina'
```

## Walk-through

Prepare data

``` python
# Sample data would be actual data measured over a fixed period of time prior to our
# experiment. For illustration purposes here we have generated data from a normal
# distribution.
sample_mean = 21.50
sample_sd = 12.91
sample_data = norm.rvs(loc=sample_mean, scale=sample_sd, size=20000)
sample_data
```

    array([25.46440322, 25.10002404, 31.1763618 , ..., 33.12020466,
           16.87635585, 28.2148879 ])

Specify experiment parameters

``` python
sample_sizes = range(250, 20000 + 1, 250)  # Sample sizes we will test over
alpha = 0.05  # Our fixed alpha
num_runs = 20  # The number of simulations we will run per sample size
relative_effect = 1.03   # MDES - could try multiple if unsure what to use
alternative = "two-sided"  # Is the alternative one-sided or two-sided
```

Run simulations

``` python
power_dist = np.empty((len(sample_sizes), 3))

for i, sample_size in enumerate(sample_sizes):

    # Control data is sample of pre-experiment data of specified size. To
    # Create treatment data, simply multiply by relative effect size.
    control_data = sample_data[0:sample_size]
    variant_data = control_data * relative_effect
    
    significance_t_results = []
    significance_u_results = []
    for _ in range(0, num_runs):
        
        # Create treatment assignment vector and collect data for
        # control and treatment units
        assignment = binom.rvs(1, 0.5, size=sample_size)
        control_sample = control_data[assignment == True]
        variant_sample = variant_data[assignment == False]

        # Use Welch's t-test, make no assumptions on tests for equal variances
        t_stat, p_value_welch, _ = ttest_ind(
            control_sample, variant_sample, alternative=alternative, usevar="unequal"
        )
        # Use Mann-Whitney U-test
        u_stat, p_value_mw = mannwhitneyu(
            control_sample, variant_sample, alternative=alternative
        )

        # Test for significance
        significance_t_results.append(p_value_welch <= alpha)
        significance_u_results.append(p_value_mw <= alpha)
    
    # The power is the number of times we have a significant result
    # as we are assuming the alternative hypothesis is true
    power_t = np.mean(significance_t_results)
    power_u = np.mean(significance_u_results)
    power_dist[i,] = [sample_size, power_t, power_u]
```

``` python
power_dist = pd.DataFrame(power_dist, columns=["sample_size", "tpower", "upower"])
power_dist = power_dist.melt(
    id_vars="sample_size",
    value_vars=["tpower", "upower"],
    var_name="test",
    value_name="power",
)
labels = {"tpower": "MC Simulation t-test", "upower": "MC Simulation MWW U-test"}
power_dist["test"].replace(labels, inplace=True)
power_dist.head()
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

|     | sample_size | test                 | power |
|-----|-------------|----------------------|-------|
| 0   | 250.0       | MC Simulation t-test | 0.05  |
| 1   | 500.0       | MC Simulation t-test | 0.05  |
| 2   | 750.0       | MC Simulation t-test | 0.05  |
| 3   | 1000.0      | MC Simulation t-test | 0.10  |
| 4   | 1250.0      | MC Simulation t-test | 0.10  |

</div>

Plot power distribution

``` python
dots = (
    alt.Chart(power_dist)
    .mark_point()
    .encode(
        x=alt.X("sample_size", axis=alt.Axis(title="Sample size")),
        y=alt.Y("power", axis=alt.Axis(title="Power")),
        color=alt.Color("test", legend=alt.Legend(title="")),
    )
)

hline = (
    alt.Chart(power_dist)
    .mark_rule()
    .encode(
        y=alt.Y("a:Q", axis=alt.Axis(title="")),
    )
    .transform_calculate(a="0.8")
)

(
    dots
    + dots.transform_loess("sample_size", "power", groupby=["test"]).mark_line()
    + hline
)
```

    /Users/fabian.gunzinger/.pyenv/versions/3.10.8/envs/wow/lib/python3.10/site-packages/altair/utils/core.py:317: FutureWarning: iteritems is deprecated and will be removed in a future version. Use .items instead.
      for col_name, dtype in df.dtypes.iteritems():

<div id="altair-viz-3e562e222071415fb79978a15547b6bd"></div>
<script type="text/javascript">
  var VEGA_DEBUG = (typeof VEGA_DEBUG == "undefined") ? {} : VEGA_DEBUG;
  (function(spec, embedOpt){
    let outputDiv = document.currentScript.previousElementSibling;
    if (outputDiv.id !== "altair-viz-3e562e222071415fb79978a15547b6bd") {
      outputDiv = document.getElementById("altair-viz-3e562e222071415fb79978a15547b6bd");
    }
    const paths = {
      "vega": "https://cdn.jsdelivr.net/npm//vega@5?noext",
      "vega-lib": "https://cdn.jsdelivr.net/npm//vega-lib?noext",
      "vega-lite": "https://cdn.jsdelivr.net/npm//vega-lite@4.17.0?noext",
      "vega-embed": "https://cdn.jsdelivr.net/npm//vega-embed@6?noext",
    };

    function maybeLoadScript(lib, version) {
      var key = `${lib.replace("-", "")}_version`;
      return (VEGA_DEBUG[key] == version) ?
        Promise.resolve(paths[lib]) :
        new Promise(function(resolve, reject) {
          var s = document.createElement('script');
          document.getElementsByTagName("head")[0].appendChild(s);
          s.async = true;
          s.onload = () => {
            VEGA_DEBUG[key] = version;
            return resolve(paths[lib]);
          };
          s.onerror = () => reject(`Error loading script: ${paths[lib]}`);
          s.src = paths[lib];
        });
    }

    function showError(err) {
      outputDiv.innerHTML = `<div class="error" style="color:red;">${err}</div>`;
      throw err;
    }

    function displayChart(vegaEmbed) {
      vegaEmbed(outputDiv, spec, embedOpt)
        .catch(err => showError(`Javascript Error: ${err.message}<br>This usually means there's a typo in your chart specification. See the javascript console for the full traceback.`));
    }

    if(typeof define === "function" && define.amd) {
      requirejs.config({paths});
      require(["vega-embed"], displayChart, err => showError(`Error loading script: ${err.message}`));
    } else {
      maybeLoadScript("vega", "5")
        .then(() => maybeLoadScript("vega-lite", "4.17.0"))
        .then(() => maybeLoadScript("vega-embed", "6"))
        .catch(showError)
        .then(() => displayChart(vegaEmbed));
    }
  })({"config": {"view": {"continuousWidth": 400, "continuousHeight": 300}}, "layer": [{"mark": "point", "encoding": {"color": {"field": "test", "legend": {"title": ""}, "type": "nominal"}, "x": {"axis": {"title": "Sample size"}, "field": "sample_size", "type": "quantitative"}, "y": {"axis": {"title": "Power"}, "field": "power", "type": "quantitative"}}}, {"mark": "line", "encoding": {"color": {"field": "test", "legend": {"title": ""}, "type": "nominal"}, "x": {"axis": {"title": "Sample size"}, "field": "sample_size", "type": "quantitative"}, "y": {"axis": {"title": "Power"}, "field": "power", "type": "quantitative"}}, "transform": [{"loess": "power", "on": "sample_size", "groupby": ["test"]}]}, {"mark": "rule", "encoding": {"y": {"axis": {"title": ""}, "field": "a", "type": "quantitative"}}, "transform": [{"calculate": "0.8", "as": "a"}]}], "data": {"name": "data-3360431e739b66032f069ec4932f1f79"}, "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json", "datasets": {"data-3360431e739b66032f069ec4932f1f79": [{"sample_size": 250.0, "test": "MC Simulation t-test", "power": 0.05}, {"sample_size": 500.0, "test": "MC Simulation t-test", "power": 0.05}, {"sample_size": 750.0, "test": "MC Simulation t-test", "power": 0.05}, {"sample_size": 1000.0, "test": "MC Simulation t-test", "power": 0.1}, {"sample_size": 1250.0, "test": "MC Simulation t-test", "power": 0.1}, {"sample_size": 1500.0, "test": "MC Simulation t-test", "power": 0.15}, {"sample_size": 1750.0, "test": "MC Simulation t-test", "power": 0.25}, {"sample_size": 2000.0, "test": "MC Simulation t-test", "power": 0.25}, {"sample_size": 2250.0, "test": "MC Simulation t-test", "power": 0.35}, {"sample_size": 2500.0, "test": "MC Simulation t-test", "power": 0.4}, {"sample_size": 2750.0, "test": "MC Simulation t-test", "power": 0.3}, {"sample_size": 3000.0, "test": "MC Simulation t-test", "power": 0.15}, {"sample_size": 3250.0, "test": "MC Simulation t-test", "power": 0.55}, {"sample_size": 3500.0, "test": "MC Simulation t-test", "power": 0.4}, {"sample_size": 3750.0, "test": "MC Simulation t-test", "power": 0.5}, {"sample_size": 4000.0, "test": "MC Simulation t-test", "power": 0.3}, {"sample_size": 4250.0, "test": "MC Simulation t-test", "power": 0.3}, {"sample_size": 4500.0, "test": "MC Simulation t-test", "power": 0.4}, {"sample_size": 4750.0, "test": "MC Simulation t-test", "power": 0.6}, {"sample_size": 5000.0, "test": "MC Simulation t-test", "power": 0.35}, {"sample_size": 5250.0, "test": "MC Simulation t-test", "power": 0.55}, {"sample_size": 5500.0, "test": "MC Simulation t-test", "power": 0.45}, {"sample_size": 5750.0, "test": "MC Simulation t-test", "power": 0.6}, {"sample_size": 6000.0, "test": "MC Simulation t-test", "power": 0.7}, {"sample_size": 6250.0, "test": "MC Simulation t-test", "power": 0.35}, {"sample_size": 6500.0, "test": "MC Simulation t-test", "power": 0.6}, {"sample_size": 6750.0, "test": "MC Simulation t-test", "power": 0.6}, {"sample_size": 7000.0, "test": "MC Simulation t-test", "power": 0.55}, {"sample_size": 7250.0, "test": "MC Simulation t-test", "power": 0.55}, {"sample_size": 7500.0, "test": "MC Simulation t-test", "power": 0.4}, {"sample_size": 7750.0, "test": "MC Simulation t-test", "power": 0.75}, {"sample_size": 8000.0, "test": "MC Simulation t-test", "power": 0.6}, {"sample_size": 8250.0, "test": "MC Simulation t-test", "power": 0.6}, {"sample_size": 8500.0, "test": "MC Simulation t-test", "power": 0.85}, {"sample_size": 8750.0, "test": "MC Simulation t-test", "power": 0.85}, {"sample_size": 9000.0, "test": "MC Simulation t-test", "power": 0.7}, {"sample_size": 9250.0, "test": "MC Simulation t-test", "power": 0.85}, {"sample_size": 9500.0, "test": "MC Simulation t-test", "power": 0.55}, {"sample_size": 9750.0, "test": "MC Simulation t-test", "power": 0.7}, {"sample_size": 10000.0, "test": "MC Simulation t-test", "power": 0.75}, {"sample_size": 10250.0, "test": "MC Simulation t-test", "power": 0.8}, {"sample_size": 10500.0, "test": "MC Simulation t-test", "power": 0.8}, {"sample_size": 10750.0, "test": "MC Simulation t-test", "power": 0.7}, {"sample_size": 11000.0, "test": "MC Simulation t-test", "power": 0.8}, {"sample_size": 11250.0, "test": "MC Simulation t-test", "power": 0.7}, {"sample_size": 11500.0, "test": "MC Simulation t-test", "power": 0.8}, {"sample_size": 11750.0, "test": "MC Simulation t-test", "power": 0.85}, {"sample_size": 12000.0, "test": "MC Simulation t-test", "power": 0.8}, {"sample_size": 12250.0, "test": "MC Simulation t-test", "power": 0.8}, {"sample_size": 12500.0, "test": "MC Simulation t-test", "power": 0.75}, {"sample_size": 12750.0, "test": "MC Simulation t-test", "power": 0.65}, {"sample_size": 13000.0, "test": "MC Simulation t-test", "power": 0.75}, {"sample_size": 13250.0, "test": "MC Simulation t-test", "power": 0.75}, {"sample_size": 13500.0, "test": "MC Simulation t-test", "power": 0.75}, {"sample_size": 13750.0, "test": "MC Simulation t-test", "power": 0.75}, {"sample_size": 14000.0, "test": "MC Simulation t-test", "power": 0.8}, {"sample_size": 14250.0, "test": "MC Simulation t-test", "power": 0.85}, {"sample_size": 14500.0, "test": "MC Simulation t-test", "power": 0.95}, {"sample_size": 14750.0, "test": "MC Simulation t-test", "power": 0.9}, {"sample_size": 15000.0, "test": "MC Simulation t-test", "power": 0.95}, {"sample_size": 15250.0, "test": "MC Simulation t-test", "power": 0.85}, {"sample_size": 15500.0, "test": "MC Simulation t-test", "power": 0.8}, {"sample_size": 15750.0, "test": "MC Simulation t-test", "power": 0.85}, {"sample_size": 16000.0, "test": "MC Simulation t-test", "power": 0.9}, {"sample_size": 16250.0, "test": "MC Simulation t-test", "power": 0.9}, {"sample_size": 16500.0, "test": "MC Simulation t-test", "power": 0.85}, {"sample_size": 16750.0, "test": "MC Simulation t-test", "power": 0.9}, {"sample_size": 17000.0, "test": "MC Simulation t-test", "power": 0.9}, {"sample_size": 17250.0, "test": "MC Simulation t-test", "power": 0.9}, {"sample_size": 17500.0, "test": "MC Simulation t-test", "power": 0.8}, {"sample_size": 17750.0, "test": "MC Simulation t-test", "power": 0.9}, {"sample_size": 18000.0, "test": "MC Simulation t-test", "power": 0.9}, {"sample_size": 18250.0, "test": "MC Simulation t-test", "power": 0.95}, {"sample_size": 18500.0, "test": "MC Simulation t-test", "power": 0.95}, {"sample_size": 18750.0, "test": "MC Simulation t-test", "power": 0.9}, {"sample_size": 19000.0, "test": "MC Simulation t-test", "power": 0.9}, {"sample_size": 19250.0, "test": "MC Simulation t-test", "power": 0.95}, {"sample_size": 19500.0, "test": "MC Simulation t-test", "power": 1.0}, {"sample_size": 19750.0, "test": "MC Simulation t-test", "power": 1.0}, {"sample_size": 20000.0, "test": "MC Simulation t-test", "power": 0.9}, {"sample_size": 250.0, "test": "MC Simulation MWW U-test", "power": 0.1}, {"sample_size": 500.0, "test": "MC Simulation MWW U-test", "power": 0.1}, {"sample_size": 750.0, "test": "MC Simulation MWW U-test", "power": 0.05}, {"sample_size": 1000.0, "test": "MC Simulation MWW U-test", "power": 0.15}, {"sample_size": 1250.0, "test": "MC Simulation MWW U-test", "power": 0.15}, {"sample_size": 1500.0, "test": "MC Simulation MWW U-test", "power": 0.2}, {"sample_size": 1750.0, "test": "MC Simulation MWW U-test", "power": 0.25}, {"sample_size": 2000.0, "test": "MC Simulation MWW U-test", "power": 0.3}, {"sample_size": 2250.0, "test": "MC Simulation MWW U-test", "power": 0.3}, {"sample_size": 2500.0, "test": "MC Simulation MWW U-test", "power": 0.4}, {"sample_size": 2750.0, "test": "MC Simulation MWW U-test", "power": 0.25}, {"sample_size": 3000.0, "test": "MC Simulation MWW U-test", "power": 0.15}, {"sample_size": 3250.0, "test": "MC Simulation MWW U-test", "power": 0.55}, {"sample_size": 3500.0, "test": "MC Simulation MWW U-test", "power": 0.35}, {"sample_size": 3750.0, "test": "MC Simulation MWW U-test", "power": 0.45}, {"sample_size": 4000.0, "test": "MC Simulation MWW U-test", "power": 0.35}, {"sample_size": 4250.0, "test": "MC Simulation MWW U-test", "power": 0.3}, {"sample_size": 4500.0, "test": "MC Simulation MWW U-test", "power": 0.4}, {"sample_size": 4750.0, "test": "MC Simulation MWW U-test", "power": 0.65}, {"sample_size": 5000.0, "test": "MC Simulation MWW U-test", "power": 0.35}, {"sample_size": 5250.0, "test": "MC Simulation MWW U-test", "power": 0.5}, {"sample_size": 5500.0, "test": "MC Simulation MWW U-test", "power": 0.45}, {"sample_size": 5750.0, "test": "MC Simulation MWW U-test", "power": 0.6}, {"sample_size": 6000.0, "test": "MC Simulation MWW U-test", "power": 0.7}, {"sample_size": 6250.0, "test": "MC Simulation MWW U-test", "power": 0.3}, {"sample_size": 6500.0, "test": "MC Simulation MWW U-test", "power": 0.55}, {"sample_size": 6750.0, "test": "MC Simulation MWW U-test", "power": 0.45}, {"sample_size": 7000.0, "test": "MC Simulation MWW U-test", "power": 0.6}, {"sample_size": 7250.0, "test": "MC Simulation MWW U-test", "power": 0.55}, {"sample_size": 7500.0, "test": "MC Simulation MWW U-test", "power": 0.35}, {"sample_size": 7750.0, "test": "MC Simulation MWW U-test", "power": 0.75}, {"sample_size": 8000.0, "test": "MC Simulation MWW U-test", "power": 0.65}, {"sample_size": 8250.0, "test": "MC Simulation MWW U-test", "power": 0.75}, {"sample_size": 8500.0, "test": "MC Simulation MWW U-test", "power": 0.75}, {"sample_size": 8750.0, "test": "MC Simulation MWW U-test", "power": 0.75}, {"sample_size": 9000.0, "test": "MC Simulation MWW U-test", "power": 0.7}, {"sample_size": 9250.0, "test": "MC Simulation MWW U-test", "power": 0.85}, {"sample_size": 9500.0, "test": "MC Simulation MWW U-test", "power": 0.55}, {"sample_size": 9750.0, "test": "MC Simulation MWW U-test", "power": 0.75}, {"sample_size": 10000.0, "test": "MC Simulation MWW U-test", "power": 0.75}, {"sample_size": 10250.0, "test": "MC Simulation MWW U-test", "power": 0.8}, {"sample_size": 10500.0, "test": "MC Simulation MWW U-test", "power": 0.8}, {"sample_size": 10750.0, "test": "MC Simulation MWW U-test", "power": 0.7}, {"sample_size": 11000.0, "test": "MC Simulation MWW U-test", "power": 0.85}, {"sample_size": 11250.0, "test": "MC Simulation MWW U-test", "power": 0.6}, {"sample_size": 11500.0, "test": "MC Simulation MWW U-test", "power": 0.85}, {"sample_size": 11750.0, "test": "MC Simulation MWW U-test", "power": 0.8}, {"sample_size": 12000.0, "test": "MC Simulation MWW U-test", "power": 0.8}, {"sample_size": 12250.0, "test": "MC Simulation MWW U-test", "power": 0.75}, {"sample_size": 12500.0, "test": "MC Simulation MWW U-test", "power": 0.8}, {"sample_size": 12750.0, "test": "MC Simulation MWW U-test", "power": 0.6}, {"sample_size": 13000.0, "test": "MC Simulation MWW U-test", "power": 0.75}, {"sample_size": 13250.0, "test": "MC Simulation MWW U-test", "power": 0.7}, {"sample_size": 13500.0, "test": "MC Simulation MWW U-test", "power": 0.65}, {"sample_size": 13750.0, "test": "MC Simulation MWW U-test", "power": 0.7}, {"sample_size": 14000.0, "test": "MC Simulation MWW U-test", "power": 0.8}, {"sample_size": 14250.0, "test": "MC Simulation MWW U-test", "power": 0.8}, {"sample_size": 14500.0, "test": "MC Simulation MWW U-test", "power": 0.8}, {"sample_size": 14750.0, "test": "MC Simulation MWW U-test", "power": 0.9}, {"sample_size": 15000.0, "test": "MC Simulation MWW U-test", "power": 0.95}, {"sample_size": 15250.0, "test": "MC Simulation MWW U-test", "power": 0.85}, {"sample_size": 15500.0, "test": "MC Simulation MWW U-test", "power": 0.8}, {"sample_size": 15750.0, "test": "MC Simulation MWW U-test", "power": 0.8}, {"sample_size": 16000.0, "test": "MC Simulation MWW U-test", "power": 0.85}, {"sample_size": 16250.0, "test": "MC Simulation MWW U-test", "power": 0.9}, {"sample_size": 16500.0, "test": "MC Simulation MWW U-test", "power": 0.9}, {"sample_size": 16750.0, "test": "MC Simulation MWW U-test", "power": 0.9}, {"sample_size": 17000.0, "test": "MC Simulation MWW U-test", "power": 0.85}, {"sample_size": 17250.0, "test": "MC Simulation MWW U-test", "power": 0.9}, {"sample_size": 17500.0, "test": "MC Simulation MWW U-test", "power": 0.7}, {"sample_size": 17750.0, "test": "MC Simulation MWW U-test", "power": 0.9}, {"sample_size": 18000.0, "test": "MC Simulation MWW U-test", "power": 0.95}, {"sample_size": 18250.0, "test": "MC Simulation MWW U-test", "power": 1.0}, {"sample_size": 18500.0, "test": "MC Simulation MWW U-test", "power": 0.95}, {"sample_size": 18750.0, "test": "MC Simulation MWW U-test", "power": 0.85}, {"sample_size": 19000.0, "test": "MC Simulation MWW U-test", "power": 0.9}, {"sample_size": 19250.0, "test": "MC Simulation MWW U-test", "power": 0.95}, {"sample_size": 19500.0, "test": "MC Simulation MWW U-test", "power": 1.0}, {"sample_size": 19750.0, "test": "MC Simulation MWW U-test", "power": 1.0}, {"sample_size": 20000.0, "test": "MC Simulation MWW U-test", "power": 0.9}]}}, {"mode": "vega-lite"});
</script>

### Program

``` python
def get_power_dist(
    data,
    sample_min,
    sample_max,
    stepsize,
    relative_effect=1.03,
    sims=20,
    alpha=0.05,
    alternative_t="two-sided",
    alternative_u="two-sided",
    tests=["t", "u"],
):
    """
    Calculates power for each sample size and each specified test.
    Code is adapted version of https://deliveroo.engineering/2018/12/07/monte-carlo-power-analysis.html

    Parameters
    -----------
    data: ArrayLike the historical data based on which power is being calculated (required)
    sample_min : integer (required)
        minimum sample size for which power is calculated
    sample_max : integer (required)
        maximum sample size for which power is calculated
    stepsize : integer (required)
        number of sample sized skipped between each calculation
    relative_effect : float (optional)
        relative effect size of variant, default is 3 percent
    sims : integer (optional)
        number of simulations per sample size, default is 20
    alpha : float (optional)
        probability of Type I error, default is 5 percent
    alternative_t : string (optional)
        type of t-test performed, either 'two-sided' (default), 'larger', or 'smaller'
    alternative_u : string (optional)
        type of Mann-Whitney-Wilkinson U-test performed, either 'two-sided' (default), 'more', or 'less'
    tests : list of strings (optional)
        test results plotted, either ['t', 'u'] (default), ['t'], or ['u']


    Returns
    --------
    dataframe : a dataframe containing sample size and associated power levels for each test
    """
    sample_sizes = range(sample_min, sample_max + 1, stepsize)

    power_dist = np.empty((len(sample_sizes), 3))
    for i in range(0, len(sample_sizes)):
        N = sample_sizes[i]
        control_data = data[0:N]
        variant_data = control_data * relative_effect

        significance_tresults = []
        significance_uresults = []
        for j in range(0, sims):
            # Randomly allocate the sample data to the control and variant
            rv = binom.rvs(1, 0.5, size=N)
            control_sample = control_data[rv == True]
            variant_sample = variant_data[rv == False]

            # Calculate Welch's t-test and Mann-Whitney U-test
            ttest_result = ttest_ind(
                control_sample,
                variant_sample,
                alternative=alternative_t,
                usevar="unequal",
            )
            utest_result = mannwhitneyu(
                control_sample, variant_sample, alternative=alternative_u
            )

            # Test for significance and calculate power
            significance_tresults.append(ttest_result[1] <= alpha)
            tpower = np.mean(significance_tresults)
            significance_uresults.append(utest_result[1] <= alpha)
            upower = np.mean(significance_uresults)

        # Store results for sample size i
        power_dist[i,] = [N, tpower, upower]

    # Convert to dataframe and keep results for selected tests
    power_dist = pd.DataFrame(power_dist, columns=["sample_size", "t", "u"])
    power_dist = power_dist.melt(
        id_vars="sample_size",
        value_vars=["t", "u"],
        var_name="test",
        value_name="power",
    )
    power_dist = power_dist[power_dist["test"].isin(tests)]
    labels = {"t": "MC Simulation t-test", "u": "MC Simulation MWW U-test"}
    power_dist["test"].replace(labels, inplace=True)

    return power_dist


def plot_power_graph(data, x="sample_size", y="power", color="test", hline_pos="0.8"):
    """
    Creates a standardised power graph

    Parameters
    ----------
    data : dataframe (required)
        name of dataframe
    x : string (optional)
        name of x coordinate (sample size), default is 'sample_size'
    y : string (optional)
        name of y coordinate (power), default is 'power'
    color : string (optional)
        name of variable for color encoding, default is 'test'
    hline_pos : str of float (optional)
        position of horizontal line to indicate target power level, default is '0.8'

    Returns
    -------
    Altair plot: A plot showing level of power for each sample size for each test.
    """
    dots = (
        alt.Chart(data)
        .mark_point()
        .encode(
            x=alt.X(x, axis=alt.Axis(title="Sample size")),
            y=alt.Y(y, axis=alt.Axis(title="Power")),
            color=alt.Color(color, legend=alt.Legend(title="")),
        )
    )

    loess = dots.transform_loess(x, y, groupby=[color]).mark_line()

    hline = (
        alt.Chart(data)
        .mark_rule(color="red")
        .encode(
            y=alt.Y("a:Q", axis=alt.Axis(title="")),
        )
        .transform_calculate(a=hline_pos)
    )

    return dots + loess + hline
```

``` python
sample_size = 20_000
step_size = 500
newdata = norm.rvs(loc=20, scale=12, size=sample_size)
data = get_power_dist(newdata, 100, sample_size, step_size, tests=['u'])
plot_power_graph(data)
```

    /Users/fabian.gunzinger/.pyenv/versions/3.10.8/envs/wow/lib/python3.10/site-packages/altair/utils/core.py:317: FutureWarning: iteritems is deprecated and will be removed in a future version. Use .items instead.
      for col_name, dtype in df.dtypes.iteritems():

<div id="altair-viz-016d5741ac754de986c56b56436ee047"></div>
<script type="text/javascript">
  var VEGA_DEBUG = (typeof VEGA_DEBUG == "undefined") ? {} : VEGA_DEBUG;
  (function(spec, embedOpt){
    let outputDiv = document.currentScript.previousElementSibling;
    if (outputDiv.id !== "altair-viz-016d5741ac754de986c56b56436ee047") {
      outputDiv = document.getElementById("altair-viz-016d5741ac754de986c56b56436ee047");
    }
    const paths = {
      "vega": "https://cdn.jsdelivr.net/npm//vega@5?noext",
      "vega-lib": "https://cdn.jsdelivr.net/npm//vega-lib?noext",
      "vega-lite": "https://cdn.jsdelivr.net/npm//vega-lite@4.17.0?noext",
      "vega-embed": "https://cdn.jsdelivr.net/npm//vega-embed@6?noext",
    };

    function maybeLoadScript(lib, version) {
      var key = `${lib.replace("-", "")}_version`;
      return (VEGA_DEBUG[key] == version) ?
        Promise.resolve(paths[lib]) :
        new Promise(function(resolve, reject) {
          var s = document.createElement('script');
          document.getElementsByTagName("head")[0].appendChild(s);
          s.async = true;
          s.onload = () => {
            VEGA_DEBUG[key] = version;
            return resolve(paths[lib]);
          };
          s.onerror = () => reject(`Error loading script: ${paths[lib]}`);
          s.src = paths[lib];
        });
    }

    function showError(err) {
      outputDiv.innerHTML = `<div class="error" style="color:red;">${err}</div>`;
      throw err;
    }

    function displayChart(vegaEmbed) {
      vegaEmbed(outputDiv, spec, embedOpt)
        .catch(err => showError(`Javascript Error: ${err.message}<br>This usually means there's a typo in your chart specification. See the javascript console for the full traceback.`));
    }

    if(typeof define === "function" && define.amd) {
      requirejs.config({paths});
      require(["vega-embed"], displayChart, err => showError(`Error loading script: ${err.message}`));
    } else {
      maybeLoadScript("vega", "5")
        .then(() => maybeLoadScript("vega-lite", "4.17.0"))
        .then(() => maybeLoadScript("vega-embed", "6"))
        .catch(showError)
        .then(() => displayChart(vegaEmbed));
    }
  })({"config": {"view": {"continuousWidth": 400, "continuousHeight": 300}}, "layer": [{"mark": "point", "encoding": {"color": {"field": "test", "legend": {"title": ""}, "type": "nominal"}, "x": {"axis": {"title": "Sample size"}, "field": "sample_size", "type": "quantitative"}, "y": {"axis": {"title": "Power"}, "field": "power", "type": "quantitative"}}}, {"mark": "line", "encoding": {"color": {"field": "test", "legend": {"title": ""}, "type": "nominal"}, "x": {"axis": {"title": "Sample size"}, "field": "sample_size", "type": "quantitative"}, "y": {"axis": {"title": "Power"}, "field": "power", "type": "quantitative"}}, "transform": [{"loess": "power", "on": "sample_size", "groupby": ["test"]}]}, {"mark": {"type": "rule", "color": "red"}, "encoding": {"y": {"axis": {"title": ""}, "field": "a", "type": "quantitative"}}, "transform": [{"calculate": "0.8", "as": "a"}]}], "data": {"name": "data-ab274dc619daa135a032d2b2464513d8"}, "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json", "datasets": {"data-ab274dc619daa135a032d2b2464513d8": [{"sample_size": 100.0, "test": "MC Simulation MWW U-test", "power": 0.15}, {"sample_size": 600.0, "test": "MC Simulation MWW U-test", "power": 0.1}, {"sample_size": 1100.0, "test": "MC Simulation MWW U-test", "power": 0.2}, {"sample_size": 1600.0, "test": "MC Simulation MWW U-test", "power": 0.25}, {"sample_size": 2100.0, "test": "MC Simulation MWW U-test", "power": 0.15}, {"sample_size": 2600.0, "test": "MC Simulation MWW U-test", "power": 0.15}, {"sample_size": 3100.0, "test": "MC Simulation MWW U-test", "power": 0.3}, {"sample_size": 3600.0, "test": "MC Simulation MWW U-test", "power": 0.3}, {"sample_size": 4100.0, "test": "MC Simulation MWW U-test", "power": 0.3}, {"sample_size": 4600.0, "test": "MC Simulation MWW U-test", "power": 0.35}, {"sample_size": 5100.0, "test": "MC Simulation MWW U-test", "power": 0.4}, {"sample_size": 5600.0, "test": "MC Simulation MWW U-test", "power": 0.45}, {"sample_size": 6100.0, "test": "MC Simulation MWW U-test", "power": 0.4}, {"sample_size": 6600.0, "test": "MC Simulation MWW U-test", "power": 0.45}, {"sample_size": 7100.0, "test": "MC Simulation MWW U-test", "power": 0.4}, {"sample_size": 7600.0, "test": "MC Simulation MWW U-test", "power": 0.5}, {"sample_size": 8100.0, "test": "MC Simulation MWW U-test", "power": 0.65}, {"sample_size": 8600.0, "test": "MC Simulation MWW U-test", "power": 0.65}, {"sample_size": 9100.0, "test": "MC Simulation MWW U-test", "power": 0.65}, {"sample_size": 9600.0, "test": "MC Simulation MWW U-test", "power": 0.4}, {"sample_size": 10100.0, "test": "MC Simulation MWW U-test", "power": 0.6}, {"sample_size": 10600.0, "test": "MC Simulation MWW U-test", "power": 0.85}, {"sample_size": 11100.0, "test": "MC Simulation MWW U-test", "power": 0.75}, {"sample_size": 11600.0, "test": "MC Simulation MWW U-test", "power": 0.8}, {"sample_size": 12100.0, "test": "MC Simulation MWW U-test", "power": 0.85}, {"sample_size": 12600.0, "test": "MC Simulation MWW U-test", "power": 0.65}, {"sample_size": 13100.0, "test": "MC Simulation MWW U-test", "power": 0.9}, {"sample_size": 13600.0, "test": "MC Simulation MWW U-test", "power": 0.85}, {"sample_size": 14100.0, "test": "MC Simulation MWW U-test", "power": 0.85}, {"sample_size": 14600.0, "test": "MC Simulation MWW U-test", "power": 0.85}, {"sample_size": 15100.0, "test": "MC Simulation MWW U-test", "power": 0.9}, {"sample_size": 15600.0, "test": "MC Simulation MWW U-test", "power": 0.75}, {"sample_size": 16100.0, "test": "MC Simulation MWW U-test", "power": 0.65}, {"sample_size": 16600.0, "test": "MC Simulation MWW U-test", "power": 0.9}, {"sample_size": 17100.0, "test": "MC Simulation MWW U-test", "power": 0.9}, {"sample_size": 17600.0, "test": "MC Simulation MWW U-test", "power": 0.85}, {"sample_size": 18100.0, "test": "MC Simulation MWW U-test", "power": 0.9}, {"sample_size": 18600.0, "test": "MC Simulation MWW U-test", "power": 0.8}, {"sample_size": 19100.0, "test": "MC Simulation MWW U-test", "power": 0.85}, {"sample_size": 19600.0, "test": "MC Simulation MWW U-test", "power": 0.8}]}}, {"mode": "vega-lite"});
</script>
