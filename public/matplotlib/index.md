# Matplotlib


<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
<script type="application/javascript">define('jquery', [],function() {return window.jQuery;})</script>


``` python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

%config InlineBackend.figure_format ='retina'
%load_ext nb_black
```

<script type="application/javascript">

            setTimeout(function() {
                var nbb_cell_id = 1;
                var nbb_unformatted_code = "import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\n%config InlineBackend.figure_format ='retina'\n%load_ext nb_black";
                var nbb_formatted_code = "import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\n%config InlineBackend.figure_format ='retina'\n%load_ext nb_black";
                var nbb_cells = Jupyter.notebook.get_cells();
                for (var i = 0; i < nbb_cells.length; ++i) {
                    if (nbb_cells[i].input_prompt_number == nbb_cell_id) {
                        if (nbb_cells[i].get_text() == nbb_unformatted_code) {
                             nbb_cells[i].set_text(nbb_formatted_code);
                        }
                        break;
                    }
                }
            }, 500);
            
</script>

## Basics

### pyplot vs object-oriented interface

Matplotlib has two interfaces: the object-oriented interface renders Axes instances on Figure instances, while the less flexible state-based MATLAB style-interface keeps track of the current figure and axes and other objects and directs plotting functions accordingly (more [here](https://matplotlib.org/stable/tutorials/introductory/lifecycle.html#a-note-on-the-object-oriented-api-vs-pyplot)).

Object-oriented plot

``` python
df = sns.load_dataset("diamonds")

fig, ax = plt.subplots()
ax.scatter(x="carat", y="price", data=df)
ax.set(xlabel="Carat", ylabel="Price")
```

    [Text(0.5, 0, 'Carat'), Text(0, 0.5, 'Price')]

![](matplotlib_files/figure-markdown_strict/cell-3-output-2.png)

<script type="application/javascript">

            setTimeout(function() {
                var nbb_cell_id = 2;
                var nbb_unformatted_code = "df = sns.load_dataset(\"diamonds\")\n\nfig, ax = plt.subplots()\nax.scatter(x=\"carat\", y=\"price\", data=df)\nax.set(xlabel=\"Carat\", ylabel=\"Price\")";
                var nbb_formatted_code = "df = sns.load_dataset(\"diamonds\")\n\nfig, ax = plt.subplots()\nax.scatter(x=\"carat\", y=\"price\", data=df)\nax.set(xlabel=\"Carat\", ylabel=\"Price\")";
                var nbb_cells = Jupyter.notebook.get_cells();
                for (var i = 0; i < nbb_cells.length; ++i) {
                    if (nbb_cells[i].input_prompt_number == nbb_cell_id) {
                        if (nbb_cells[i].get_text() == nbb_unformatted_code) {
                             nbb_cells[i].set_text(nbb_formatted_code);
                        }
                        break;
                    }
                }
            }, 500);
            
</script>

pyplot version

``` python
plt.scatter(x="carat", y="price", data=df)
plt.xlabel("Carat")
plt.ylabel("Price")
```

    Text(0, 0.5, 'Price')

![](matplotlib_files/figure-markdown_strict/cell-4-output-2.png)

<script type="application/javascript">

            setTimeout(function() {
                var nbb_cell_id = 3;
                var nbb_unformatted_code = "plt.scatter(x=\"carat\", y=\"price\", data=df)\nplt.xlabel(\"Carat\")\nplt.ylabel(\"Price\")";
                var nbb_formatted_code = "plt.scatter(x=\"carat\", y=\"price\", data=df)\nplt.xlabel(\"Carat\")\nplt.ylabel(\"Price\")";
                var nbb_cells = Jupyter.notebook.get_cells();
                for (var i = 0; i < nbb_cells.length; ++i) {
                    if (nbb_cells[i].input_prompt_number == nbb_cell_id) {
                        if (nbb_cells[i].get_text() == nbb_unformatted_code) {
                             nbb_cells[i].set_text(nbb_formatted_code);
                        }
                        break;
                    }
                }
            }, 500);
            
</script>

## Plot lifecycle

Based on [this](https://pbpython.com/effective-matplotlib.html) great blog post by Chris Moffitt and the matplotlib [tutorial](https://matplotlib.org/stable/tutorials/introductory/lifecycle.html) that's based on the same post.

Reading in raw data of customer sales transactions and keeping sales volume and number of purchases for top 10 customers by sales.

``` python
fp = (
    "https://github.com/chris1610/pbpython/blob/master/data/"
    "sample-salesv3.xlsx?raw=true"
)
df_raw = pd.read_excel(fp)
print(df_raw.shape)
df_raw.head(2)
```

    (1500, 7)

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

|     | account number | name            | sku      | quantity | unit price | ext price | date                |
|-----|----------------|-----------------|----------|----------|------------|-----------|---------------------|
| 0   | 740150         | Barton LLC      | B1-20000 | 39       | 86.69      | 3380.91   | 2014-01-01 07:21:51 |
| 1   | 714466         | Trantow-Barrows | S2-77896 | -1       | 63.16      | -63.16    | 2014-01-01 10:00:47 |

</div>
<script type="application/javascript">

            setTimeout(function() {
                var nbb_cell_id = 4;
                var nbb_unformatted_code = "fp = (\n    \"https://github.com/chris1610/pbpython/blob/master/data/\"\n    \"sample-salesv3.xlsx?raw=true\"\n)\ndf_raw = pd.read_excel(fp)\nprint(df_raw.shape)\ndf_raw.head(2)";
                var nbb_formatted_code = "fp = (\n    \"https://github.com/chris1610/pbpython/blob/master/data/\"\n    \"sample-salesv3.xlsx?raw=true\"\n)\ndf_raw = pd.read_excel(fp)\nprint(df_raw.shape)\ndf_raw.head(2)";
                var nbb_cells = Jupyter.notebook.get_cells();
                for (var i = 0; i < nbb_cells.length; ++i) {
                    if (nbb_cells[i].input_prompt_number == nbb_cell_id) {
                        if (nbb_cells[i].get_text() == nbb_unformatted_code) {
                             nbb_cells[i].set_text(nbb_formatted_code);
                        }
                        break;
                    }
                }
            }, 500);
            
</script>

``` python
df = (
    df_raw.groupby("name")
    .agg(sales=("ext price", "sum"), purchases=("quantity", "count"))
    .sort_values("sales")[-10:]
    .reset_index()
)
df
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

|     | name                         | sales     | purchases |
|-----|------------------------------|-----------|-----------|
| 0   | Keeling LLC                  | 100934.30 | 74        |
| 1   | Frami, Hills and Schmidt     | 103569.59 | 72        |
| 2   | Koepp Ltd                    | 103660.54 | 82        |
| 3   | Will LLC                     | 104437.60 | 74        |
| 4   | Barton LLC                   | 109438.50 | 82        |
| 5   | Fritsch, Russel and Anderson | 112214.71 | 81        |
| 6   | Jerde-Hilpert                | 112591.43 | 89        |
| 7   | Trantow-Barrows              | 123381.38 | 94        |
| 8   | White-Trantow                | 135841.99 | 86        |
| 9   | Kulas Inc                    | 137351.96 | 94        |

</div>
<script type="application/javascript">

            setTimeout(function() {
                var nbb_cell_id = 5;
                var nbb_unformatted_code = "df = (\n    df_raw.groupby(\"name\")\n    .agg(sales=(\"ext price\", \"sum\"), purchases=(\"quantity\", \"count\"))\n    .sort_values(\"sales\")[-10:]\n    .reset_index()\n)\ndf";
                var nbb_formatted_code = "df = (\n    df_raw.groupby(\"name\")\n    .agg(sales=(\"ext price\", \"sum\"), purchases=(\"quantity\", \"count\"))\n    .sort_values(\"sales\")[-10:]\n    .reset_index()\n)\ndf";
                var nbb_cells = Jupyter.notebook.get_cells();
                for (var i = 0; i < nbb_cells.length; ++i) {
                    if (nbb_cells[i].input_prompt_number == nbb_cell_id) {
                        if (nbb_cells[i].get_text() == nbb_unformatted_code) {
                             nbb_cells[i].set_text(nbb_formatted_code);
                        }
                        break;
                    }
                }
            }, 500);
            
</script>

Choosing a style

``` python
plt.style.available
```

    ['Solarize_Light2',
     '_classic_test_patch',
     '_mpl-gallery',
     '_mpl-gallery-nogrid',
     'bmh',
     'classic',
     'dark_background',
     'fast',
     'fivethirtyeight',
     'ggplot',
     'grayscale',
     'seaborn',
     'seaborn-bright',
     'seaborn-colorblind',
     'seaborn-dark',
     'seaborn-dark-palette',
     'seaborn-darkgrid',
     'seaborn-deep',
     'seaborn-muted',
     'seaborn-notebook',
     'seaborn-paper',
     'seaborn-pastel',
     'seaborn-poster',
     'seaborn-talk',
     'seaborn-ticks',
     'seaborn-white',
     'seaborn-whitegrid',
     'tableau-colorblind10']

<script type="application/javascript">

            setTimeout(function() {
                var nbb_cell_id = 6;
                var nbb_unformatted_code = "plt.style.available";
                var nbb_formatted_code = "plt.style.available";
                var nbb_cells = Jupyter.notebook.get_cells();
                for (var i = 0; i < nbb_cells.length; ++i) {
                    if (nbb_cells[i].input_prompt_number == nbb_cell_id) {
                        if (nbb_cells[i].get_text() == nbb_unformatted_code) {
                             nbb_cells[i].set_text(nbb_formatted_code);
                        }
                        break;
                    }
                }
            }, 500);
            
</script>

``` python
plt.style.use("seaborn-whitegrid")
```

<script type="application/javascript">

            setTimeout(function() {
                var nbb_cell_id = 7;
                var nbb_unformatted_code = "plt.style.use(\"seaborn-whitegrid\")";
                var nbb_formatted_code = "plt.style.use(\"seaborn-whitegrid\")";
                var nbb_cells = Jupyter.notebook.get_cells();
                for (var i = 0; i < nbb_cells.length; ++i) {
                    if (nbb_cells[i].input_prompt_number == nbb_cell_id) {
                        if (nbb_cells[i].get_text() == nbb_unformatted_code) {
                             nbb_cells[i].set_text(nbb_formatted_code);
                        }
                        break;
                    }
                }
            }, 500);
            
</script>

Prototyping plot with Pandas

``` python
df.plot(kind="barh", x="name", y="sales", legend=None);
```

![](matplotlib_files/figure-markdown_strict/cell-9-output-1.png)

<script type="application/javascript">

            setTimeout(function() {
                var nbb_cell_id = 8;
                var nbb_unformatted_code = "df.plot(kind=\"barh\", x=\"name\", y=\"sales\", legend=None);";
                var nbb_formatted_code = "df.plot(kind=\"barh\", x=\"name\", y=\"sales\", legend=None)";
                var nbb_cells = Jupyter.notebook.get_cells();
                for (var i = 0; i < nbb_cells.length; ++i) {
                    if (nbb_cells[i].input_prompt_number == nbb_cell_id) {
                        if (nbb_cells[i].get_text() == nbb_unformatted_code) {
                             nbb_cells[i].set_text(nbb_formatted_code);
                        }
                        break;
                    }
                }
            }, 500);
            
</script>

Customising plot combining fast Pandas plotting with Matplotlib object-oriented API

``` python
def xlim(x):
    """Set xlim with custom padding."""
    return x.max() * np.array([-0.05, 1.3])


fig, ax = plt.subplots()
df.plot(kind="barh", x="name", y="sales", legend=None, ax=ax)
ax.set(
    xlim=xlim(df.sales),
    xlabel="Sales",
    ylabel="Customer",
    title="Top customers 2014",
);
```

![](matplotlib_files/figure-markdown_strict/cell-10-output-1.png)

<script type="application/javascript">

            setTimeout(function() {
                var nbb_cell_id = 9;
                var nbb_unformatted_code = "def xlim(x):\n    \"\"\"Set xlim with custom padding.\"\"\"\n    return x.max() * np.array([-0.05, 1.3])\n\n\nfig, ax = plt.subplots()\ndf.plot(kind=\"barh\", x=\"name\", y=\"sales\", legend=None, ax=ax)\nax.set(\n    xlim=xlim(df.sales),\n    xlabel=\"Sales\",\n    ylabel=\"Customer\",\n    title=\"Top customers 2014\",\n);";
                var nbb_formatted_code = "def xlim(x):\n    \"\"\"Set xlim with custom padding.\"\"\"\n    return x.max() * np.array([-0.05, 1.3])\n\n\nfig, ax = plt.subplots()\ndf.plot(kind=\"barh\", x=\"name\", y=\"sales\", legend=None, ax=ax)\nax.set(\n    xlim=xlim(df.sales),\n    xlabel=\"Sales\",\n    ylabel=\"Customer\",\n    title=\"Top customers 2014\",\n)";
                var nbb_cells = Jupyter.notebook.get_cells();
                for (var i = 0; i < nbb_cells.length; ++i) {
                    if (nbb_cells[i].input_prompt_number == nbb_cell_id) {
                        if (nbb_cells[i].get_text() == nbb_unformatted_code) {
                             nbb_cells[i].set_text(nbb_formatted_code);
                        }
                        break;
                    }
                }
            }, 500);
            
</script>

Formatting currency values using custom formatter

``` python
def currency(x, pos):
    """Reformat currency amount at position x."""
    return f"{x * 1e-3:1.1f}K"


ax.xaxis.set_major_formatter(currency)

fig
```

![](matplotlib_files/figure-markdown_strict/cell-11-output-1.png)

<script type="application/javascript">

            setTimeout(function() {
                var nbb_cell_id = 10;
                var nbb_unformatted_code = "def currency(x, pos):\n    \"\"\"Reformat currency amount at position x.\"\"\"\n    return f\"{x * 1e-3:1.1f}K\"\n\n\nax.xaxis.set_major_formatter(currency)\n\nfig";
                var nbb_formatted_code = "def currency(x, pos):\n    \"\"\"Reformat currency amount at position x.\"\"\"\n    return f\"{x * 1e-3:1.1f}K\"\n\n\nax.xaxis.set_major_formatter(currency)\n\nfig";
                var nbb_cells = Jupyter.notebook.get_cells();
                for (var i = 0; i < nbb_cells.length; ++i) {
                    if (nbb_cells[i].input_prompt_number == nbb_cell_id) {
                        if (nbb_cells[i].get_text() == nbb_unformatted_code) {
                             nbb_cells[i].set_text(nbb_formatted_code);
                        }
                        break;
                    }
                }
            }, 500);
            
</script>

Adding a line for average sales

``` python
sales_mean = df.sales.mean()
ax.axvline(sales_mean, linestyle=":", color="green")
lab = f"Mean: {currency(sales_mean, 0)}"
ax.text(
    x=1.05 * sales_mean,
    y=0,
    s=lab,
    color="green",
)

fig
```

![](matplotlib_files/figure-markdown_strict/cell-12-output-1.png)

<script type="application/javascript">

            setTimeout(function() {
                var nbb_cell_id = 11;
                var nbb_unformatted_code = "sales_mean = df.sales.mean()\nax.axvline(sales_mean, linestyle=\":\", color=\"green\")\nlab = f\"Mean: {currency(sales_mean, 0)}\"\nax.text(\n    x=1.05 * sales_mean,\n    y=0,\n    s=lab,\n    color=\"green\",\n)\n\nfig";
                var nbb_formatted_code = "sales_mean = df.sales.mean()\nax.axvline(sales_mean, linestyle=\":\", color=\"green\")\nlab = f\"Mean: {currency(sales_mean, 0)}\"\nax.text(\n    x=1.05 * sales_mean,\n    y=0,\n    s=lab,\n    color=\"green\",\n)\n\nfig";
                var nbb_cells = Jupyter.notebook.get_cells();
                for (var i = 0; i < nbb_cells.length; ++i) {
                    if (nbb_cells[i].input_prompt_number == nbb_cell_id) {
                        if (nbb_cells[i].get_text() == nbb_unformatted_code) {
                             nbb_cells[i].set_text(nbb_formatted_code);
                        }
                        break;
                    }
                }
            }, 500);
            
</script>

Identify new customers

``` python
for customer in [2, 4, 5]:
    ax.text(x=1.05 * sales_mean, y=customer, s="New customer")
fig
```

![](matplotlib_files/figure-markdown_strict/cell-13-output-1.png)

<script type="application/javascript">

            setTimeout(function() {
                var nbb_cell_id = 12;
                var nbb_unformatted_code = "for customer in [2, 4, 5]:\n    ax.text(x=1.05 * sales_mean, y=customer, s=\"New customer\")\nfig";
                var nbb_formatted_code = "for customer in [2, 4, 5]:\n    ax.text(x=1.05 * sales_mean, y=customer, s=\"New customer\")\nfig";
                var nbb_cells = Jupyter.notebook.get_cells();
                for (var i = 0; i < nbb_cells.length; ++i) {
                    if (nbb_cells[i].input_prompt_number == nbb_cell_id) {
                        if (nbb_cells[i].get_text() == nbb_unformatted_code) {
                             nbb_cells[i].set_text(nbb_formatted_code);
                        }
                        break;
                    }
                }
            }, 500);
            
</script>

Show sales and number of purchases, [xkcd](https://xkcd.com)-themed (just because...)

``` python
with plt.xkcd():
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(8, 4), sharey=True)

    df.plot(kind="barh", x="name", y="sales", legend=None, ax=ax0)
    sales_mean = df.sales.mean()
    ax0.axvline(sales_mean, color="green", linestyle=":")
    lab = f"Mean: {currency(sales_mean, 0)}"
    ax0.text(1.05 * sales_mean, 0, lab, color="green")
    for customer in [2, 4, 5]:
        ax0.text(sales_mean, customer, "New customer")
    ax0.xaxis.set_major_formatter(currency)
    ax0.set(xlim=xlim(df.sales), ylabel="Customer",title="Sales")

    df.plot(kind="barh", x="name", y="purchases", legend=None, ax=ax1)
    purch_mean = df.purchases.mean()
    ax1.axvline(purch_mean, color="green", linestyle=":")
    ax1.text(purch_mean, 0, f"Mean: {purch_mean}", color="green")
    ax1.set(title="Purchases", xlim=xlim(df.purchases))

    fig.suptitle(
        "Sales and purchases for top 10 customers in 2022",
        fontsize=18,
        fontweight="bold",
        y=1.05,
    )
```

![](matplotlib_files/figure-markdown_strict/cell-14-output-1.png)

<script type="application/javascript">

            setTimeout(function() {
                var nbb_cell_id = 20;
                var nbb_unformatted_code = "with plt.xkcd():\n    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(8, 4), sharey=True)\n\n    df.plot(kind=\"barh\", x=\"name\", y=\"sales\", legend=None, ax=ax0)\n    sales_mean = df.sales.mean()\n    ax0.axvline(sales_mean, color=\"green\", linestyle=\":\")\n    lab = f\"Mean: {currency(sales_mean, 0)}\"\n    ax0.text(1.05 * sales_mean, 0, lab, color=\"green\")\n    for customer in [2, 4, 5]:\n        ax0.text(sales_mean, customer, \"New customer\")\n    ax0.xaxis.set_major_formatter(currency)\n    ax0.set(xlim=xlim(df.sales), ylabel=\"Customer\",title=\"Sales\")\n\n    df.plot(kind=\"barh\", x=\"name\", y=\"purchases\", legend=None, ax=ax1)\n    purch_mean = df.purchases.mean()\n    ax1.axvline(purch_mean, color=\"green\", linestyle=\":\")\n    ax1.text(purch_mean, 0, f\"Mean: {purch_mean}\", color=\"green\")\n    ax1.set(title=\"Purchases\", xlim=xlim(df.purchases))\n\n    fig.suptitle(\n        \"Sales and purchases for top 10 customers in 2022\",\n        fontsize=18,\n        fontweight=\"bold\",\n        y=1.05,\n    )";
                var nbb_formatted_code = "with plt.xkcd():\n    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(8, 4), sharey=True)\n\n    df.plot(kind=\"barh\", x=\"name\", y=\"sales\", legend=None, ax=ax0)\n    sales_mean = df.sales.mean()\n    ax0.axvline(sales_mean, color=\"green\", linestyle=\":\")\n    lab = f\"Mean: {currency(sales_mean, 0)}\"\n    ax0.text(1.05 * sales_mean, 0, lab, color=\"green\")\n    for customer in [2, 4, 5]:\n        ax0.text(sales_mean, customer, \"New customer\")\n    ax0.xaxis.set_major_formatter(currency)\n    ax0.set(xlim=xlim(df.sales), ylabel=\"Customer\", title=\"Sales\")\n\n    df.plot(kind=\"barh\", x=\"name\", y=\"purchases\", legend=None, ax=ax1)\n    purch_mean = df.purchases.mean()\n    ax1.axvline(purch_mean, color=\"green\", linestyle=\":\")\n    ax1.text(purch_mean, 0, f\"Mean: {purch_mean}\", color=\"green\")\n    ax1.set(title=\"Purchases\", xlim=xlim(df.purchases))\n\n    fig.suptitle(\n        \"Sales and purchases for top 10 customers in 2022\",\n        fontsize=18,\n        fontweight=\"bold\",\n        y=1.05,\n    )";
                var nbb_cells = Jupyter.notebook.get_cells();
                for (var i = 0; i < nbb_cells.length; ++i) {
                    if (nbb_cells[i].input_prompt_number == nbb_cell_id) {
                        if (nbb_cells[i].get_text() == nbb_unformatted_code) {
                             nbb_cells[i].set_text(nbb_formatted_code);
                        }
                        break;
                    }
                }
            }, 500);
            
</script>

Save figure

``` python
fig.canvas.get_supported_filetypes()
```

    {'eps': 'Encapsulated Postscript',
     'jpg': 'Joint Photographic Experts Group',
     'jpeg': 'Joint Photographic Experts Group',
     'pdf': 'Portable Document Format',
     'pgf': 'PGF code for LaTeX',
     'png': 'Portable Network Graphics',
     'ps': 'Postscript',
     'raw': 'Raw RGBA bitmap',
     'rgba': 'Raw RGBA bitmap',
     'svg': 'Scalable Vector Graphics',
     'svgz': 'Scalable Vector Graphics',
     'tif': 'Tagged Image File Format',
     'tiff': 'Tagged Image File Format'}

<script type="application/javascript">

            setTimeout(function() {
                var nbb_cell_id = 14;
                var nbb_unformatted_code = "fig.canvas.get_supported_filetypes()";
                var nbb_formatted_code = "fig.canvas.get_supported_filetypes()";
                var nbb_cells = Jupyter.notebook.get_cells();
                for (var i = 0; i < nbb_cells.length; ++i) {
                    if (nbb_cells[i].input_prompt_number == nbb_cell_id) {
                        if (nbb_cells[i].get_text() == nbb_unformatted_code) {
                             nbb_cells[i].set_text(nbb_formatted_code);
                        }
                        break;
                    }
                }
            }, 500);
            
</script>

``` python
fp = 'figure-path.png'
fig.savefig(fp, transparent=False, dpi=80, bbox_inches="tight")
```

<script type="application/javascript">

            setTimeout(function() {
                var nbb_cell_id = 15;
                var nbb_unformatted_code = "fp = 'figure-path.png'\nfig.savefig(fp, transparent=False, dpi=80, bbox_inches=\"tight\")";
                var nbb_formatted_code = "fp = \"figure-path.png\"\nfig.savefig(fp, transparent=False, dpi=80, bbox_inches=\"tight\")";
                var nbb_cells = Jupyter.notebook.get_cells();
                for (var i = 0; i < nbb_cells.length; ++i) {
                    if (nbb_cells[i].input_prompt_number == nbb_cell_id) {
                        if (nbb_cells[i].get_text() == nbb_unformatted_code) {
                             nbb_cells[i].set_text(nbb_formatted_code);
                        }
                        break;
                    }
                }
            }, 500);
            
</script>

