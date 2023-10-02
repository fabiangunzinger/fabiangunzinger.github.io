<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
<script type="application/javascript">define('jquery', [],function() {return window.jQuery;})</script>


``` python
import pandas as pd


df = pd.DataFrame(
    data={
        "id": [f"id{i}" for i in range(10000)],
        "country": ["country1"] * 6000 + ["country2"] * 3000 + ["country3"] * 1000,
        "assignment": [0, 1] * 5000
    }
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

|      | id     | country  | assignment |
|------|--------|----------|------------|
| 0    | id0    | country1 | 0          |
| 1    | id1    | country1 | 1          |
| 2    | id2    | country1 | 0          |
| 3    | id3    | country1 | 1          |
| 4    | id4    | country1 | 0          |
| \... | \...   | \...     | \...       |
| 9995 | id9995 | country3 | 1          |
| 9996 | id9996 | country3 | 0          |
| 9997 | id9997 | country3 | 1          |
| 9998 | id9998 | country3 | 0          |
| 9999 | id9999 | country3 | 1          |

<p>10000 rows × 3 columns</p>
</div>

``` python
dfs = df.sample(frac=0.1)
```

``` python
df.iloc[dfs.index]
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

|      | id     | country  | assignment |
|------|--------|----------|------------|
| 1401 | id1401 | country1 | 1          |
| 2103 | id2103 | country1 | 1          |
| 7093 | id7093 | country2 | 1          |
| 8646 | id8646 | country2 | 0          |
| 5538 | id5538 | country1 | 0          |
| \... | \...   | \...     | \...       |
| 9690 | id9690 | country3 | 0          |
| 9726 | id9726 | country3 | 0          |
| 2626 | id2626 | country1 | 0          |
| 2472 | id2472 | country1 | 0          |
| 799  | id799  | country1 | 1          |

<p>1000 rows × 3 columns</p>
</div>
