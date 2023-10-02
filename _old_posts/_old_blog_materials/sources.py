import functools
import operator
import os
import random
import re
import sys
import sqlite3

import linearmodels 
import numpy as np
import pandas as pd
import scipy as sp
import statsmodels.api as sm
import statsmodels.formula.api as smf

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt
from vega_datasets import data

# pandas settings
pd.set_option('display.max_rows', 120)
pd.set_option('display.max_columns', 120)
pd.set_option('max_colwidth', None)
pd.set_option('precision', 4)

# seaborn settings
sns.set_context("notebook")
# sns.set(rc={'figure.figsize': (16, 9.)})
sns.set_style("whitegrid")

# global vars
TEMPDIR = '/Users/fgu/tmp/'
SAMPLEDATA = '/Users/fgu/tmp/mdb/data_777.parquet'


- [Fluent Python](https://www.oreilly.com/library/view/fluent-python/9781491946237/)
- [Python Cookbook](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/)
- [Learning Python](https://www.oreilly.com/library/view/learning-python-5th/9781449355722/)
- [The Hitchhiker's Guide to Python](https://docs.python-guide.org/writing/structure/)
- [Effective Python](https://effectivepython.com)
- [Python for Data Analysis](https://www.oreilly.com/library/view/python-for-data/9781491957653/)
- [Python Data Science Handbook](https://www.oreilly.com/library/view/python-data-science/9781491912126/)
- [Pandas cookbook](https://pandas.pydata.org/pandas-docs/stable/user_guide/cookbook.html)
- [Numpy docs](https://numpy.org/doc/stable/)

- [An introduction to statistical learning](https://www.statlearning.com)
- [Applied predictive modeling](http://appliedpredictivemodeling.com)
- [Hands on machine learning with scikit-learn, keras, and tenserflow](https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/)
- [The hundred-page machine learning book](http://themlbook.com)