---
title: Managing kernels
---

<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
<script type="application/javascript">define('jquery', [],function() {return window.jQuery;})</script>


My Jupyter cheatsheet.

List available kernels

``` python
!jupyter kernelspec list
```

    Available kernels:
      python3    /Users/fabian.gunzinger/.pyenv/versions/3.10.8/envs/base/share/jupyter/kernels/python3
      wow-env    /Users/fabian.gunzinger/.pyenv/versions/3.10.8/envs/base/share/jupyter/kernels/wow-env
      test       /Users/fabian.gunzinger/Library/Jupyter/kernels/test
      wow        /Users/fabian.gunzinger/Library/Jupyter/kernels/wow

``` python
# show python that's being run by default?

!which python
```

    /Users/fabian.gunzinger/.pyenv/versions/base/bin/python

``` python
# list all python installations

!which -a python
```

    /Users/fabian.gunzinger/.pyenv/versions/base/bin/python
    /Users/fabian.gunzinger/.pyenv/shims/python

## Exporting notebook to pdf

-   This can be a pain if xelatex is not installed properly (which happened to me on Jet-mac).
-   An easy way around it (once you know), is to convert to pdf via webpdf and allowing for Chromium install the first time (from \[here\])(https://mljar.com/blog/jupyter-notebook-pdf/). Use the below:

<!-- -->

    pip install nbconvert
    pip install pyppeteer
    jupyter nbconvert --to webpdf --allow-chromium-download your-notebook-file.ipynb

Check nbconvert docs for additional options like hiding code or specific cells or changing template.

# Options

Below a list of options I frequently use (and often forget).

``` python
# pandas settings
pd.set_option("display.max_rows", 120)
pd.set_option("display.max_columns", 120)
pd.set_option("max_colwidth", None)
pd.set_option("precision", 4)

# seaborn settings
sns.set_context("notebook")
sns.set(rc={"figure.figsize": (16, 9.0)})
sns.set_style("whitegrid")

# ipython magic
%load_ext snakeviz
%load_ext line_profiler
%load_ext memory_profiler
%config InlineBackend.figure_format = 'retina'
%load_ext autoreload
%autoreload 2
```

# IPython / notebook shortcuts

``` python
clean_nb = !ls *2*
clean_nb
```

    ['2.0-fgu-clean-and-split-data.ipynb']

``` python
%%timeit
a = range(1000)
```

    174 ns ± 4.23 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)

``` python
%%writefile pythoncode.py

import numpy
def append_if_not_exists(arr, x):
    if x not in arr:
        arr.append(x)

def some_useless_slow_function():
    arr = list()
    for i in range(10000):
        x = numpy.random.randint(0, 10000)
        append_if_not_exists(arr, x)
```

    Writing pythoncode.py

``` python
%pycat pythoncode.py
```

<pre><span class="ansi-green-fg">import</span> numpy
<span class="ansi-green-fg">def</span> append_if_not_exists<span class="ansi-blue-fg">(</span>arr<span class="ansi-blue-fg">,</span> x<span class="ansi-blue-fg">)</span><span class="ansi-blue-fg">:</span>
    <span class="ansi-green-fg">if</span> x <span class="ansi-green-fg">not</span> <span class="ansi-green-fg">in</span> arr<span class="ansi-blue-fg">:</span>
        arr<span class="ansi-blue-fg">.</span>append<span class="ansi-blue-fg">(</span>x<span class="ansi-blue-fg">)</span>
<span class="ansi-green-fg">def</span> some_useless_slow_function<span class="ansi-blue-fg">(</span><span class="ansi-blue-fg">)</span><span class="ansi-blue-fg">:</span>
    arr <span class="ansi-blue-fg">=</span> list<span class="ansi-blue-fg">(</span><span class="ansi-blue-fg">)</span>
    <span class="ansi-green-fg">for</span> i <span class="ansi-green-fg">in</span> range<span class="ansi-blue-fg">(</span><span class="ansi-cyan-fg">10000</span><span class="ansi-blue-fg">)</span><span class="ansi-blue-fg">:</span>
        x <span class="ansi-blue-fg">=</span> numpy<span class="ansi-blue-fg">.</span>random<span class="ansi-blue-fg">.</span>randint<span class="ansi-blue-fg">(</span><span class="ansi-cyan-fg">0</span><span class="ansi-blue-fg">,</span> <span class="ansi-cyan-fg">10000</span><span class="ansi-blue-fg">)</span>
        append_if_not_exists<span class="ansi-blue-fg">(</span>arr<span class="ansi-blue-fg">,</span> x<span class="ansi-blue-fg">)</span>
</pre>

``` python
# %magic -brief
```

I can transfer variables with any content from one notebook to the next (useful if you run a number of notebooks in sequence, for instance, and the ouput of one serves as the input of another).

``` python
var_to_pass_on = dfu.head()
%store var_to_pass_on
```

    Stored 'var_to_pass_on' (DataFrame)

``` python
# I can pass on variables from one notebook (3.0-fgu) to another
%store -r var_to_pass_on
var_to_pass_on
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

|     | user_id | year_of_birth | user_registration_date | salary_range | postcode | gender | soa_lower | soa_middle | user_uid |
|-----|---------|---------------|------------------------|--------------|----------|--------|-----------|------------|----------|
| 0   | 3706    | 1967-01-01    | 2012-09-30             | NaN          | XXXX 0   | M      | NaN       | NaN        | 3706-0   |
| 1   | 1078    | 1964-01-01    | 2011-11-29             | 20K to 30K   | M25 9    | M      | E01005038 | E02001043  | 1078-0   |
| 2   | 232     | 1965-01-01    | 2010-09-09             | 30K to 40K   | CM4 0    | M      | E01021551 | E02004495  | 232-0    |
| 3   | 6133    | 1968-01-01    | 2012-10-21             | 10K to 20K   | SK12 1   | M      | E01018665 | E02003854  | 6133-0   |
| 4   | 7993    | 1961-01-01    | 2012-10-29             | 20K to 30K   | LS17 8   | M      | E01011556 | E02002344  | 7993-0   |

</div>

``` python
!conda list | grep pandas
```

    pandas                    1.0.1            py37h6c726b0_0  
    pandas-flavor             0.2.0                      py_0    conda-forge

## Code formatting

Install the below

    conda install -c conda-forge jupyterlab_code_formatter black isort

## Emojis

Copy from [here](https://getemoji.com) and paste into markdown cell.

## === Older notes to integrate ===


    ###########################################################
    ### Settings
    ###########################################################

    # Print all statements rather than just the last one
    from IPython.core.interactiveshell import InteractiveShell
    InteractiveShell.ast_node_interactivity = "all"

    # High-resolution plot output for retina displays
    %config InlineBackend.figure_format ='retina'

    # Print entire table

    pd.set_option('display.max_columns', None)
    pd.reset_option(“max_columns”)

    pd.set_option(“max_colwidth”, None)

    pd.set_option("max_rows", None)

    pd.set_option(‘precision’, 2)


    # Black auto formatting
    %load_ext lab_blacker

    # Figure settings
    sns.set_style('darkgrid')
    sns.mpl.rcParams['figure.figsize'] = (10.0, 6.0)


    ###########################################################
    ### Cool stuff
    ###########################################################

    # Execute shell commands
    !conda list | grep pandas

    # Use wildcards to find objects in namespace
    *df*?

    # Use cached input and output values
    In[101], Out[101]

    # Syntactic sugar for glob
    notebooks = !ls * fgu*
    notebooks

    # (Then) shell out to subcommand (e.g. execute file from inside notebook)
    !echo {notebooks[1]}

    # Time function calls as they happen with tqdm
    #Replace .map() by .progress_map(), same for .apply() and .applymap()

    from tqdm import tqdm_notebook
    tqdm_notebook().pandas()

    data['column_1'].progress_map(lambda x: x.count('e'))


    ###########################################################
    ### Magic functions
    ###########################################################

    # Info and brief info about magic function
    %magic
    %magic - brief

    # Debugging (instead of putting print statement throughout code)
    %debug
    %pdb

    # Install package using conda from current kernel
    %conda install < packagename >

    # Run different notebook from within notebook
    %run <path_to_notebook/name_of_notebook>

    # Write code to python file / read code from python file
    %%writefile pythoncode.py
    %pycat pythoncode.py

    # All objects in namespace displayed and as a list
    %who
    %who_ls

    # Run c or something else inside notebook
    %% cc



    # Time cell
    %% timeit   # Average of 100,000 runs
    %% time     # Time of single run
