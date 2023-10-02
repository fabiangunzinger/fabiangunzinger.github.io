---
title: "HDF5"
date: "2021-01-13"
tags:
    - tools
execute:
    enabled: false
---

My hdf5 cheatsheet.

``` python
import h5py
import numpy as np
```

## Create a file

``` python
f = h5py.File('demo.hdf5', 'w')
```

``` python
data = np.arange(10)
data
```

    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

``` python
f['array'] = data
```

``` python
dset = f['array']
```

``` python
dset
```

    <HDF5 dataset "array": shape (10,), type "<i8">

``` python
dset[:]
```

    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

``` python
dset[[1, 2, 5]]
```

    array([1, 2, 5])

Add additional data

``` python
f['dataset'] = data
```

``` python
f['full/dataset'] = data
```

``` python
list(f.keys())
```

    ['array', 'dataset', 'full']

``` python
grp = f['full']
```

``` python
'dataset' in grp
```

    True

``` python
list(grp.keys())
```

    ['dataset']

Create dataset

``` python
dset = f.create_dataset('/full/bigger', (10000, 1000, 1000, 1000), compression='gzip')
```

## Set attributes

``` python
dset.attrs
```

    <Attributes of HDF5 object at 140618810188336>

Atributes again have dictionary structure, so can add attribute like so:

``` python
dset.attrs['sampling frequency'] = 'Every other week between 1 Jan 2001 and 7 Feb 2010'
dset.attrs['PI'] = 'Fabian'
```

``` python
list(dset.attrs.items())
for i in dset.attrs.items():
    print(i)
```

    ('PI', 'Fabian')
    ('sampling frequency', 'Every other week between 1 Jan 2001 and 7 Feb 2010')

## Open file

``` python
f.close()
```

``` python
f = h5py.File('demo.hdf5', 'r')
```

``` python
list(f.keys())
```

    ['array', 'dataset', 'full']

``` python
dset = f['array']
```

hdf5 files are organised in a hierarchy - that's what the "h" stands for.

``` python
dset.name
```

    '/array'

``` python
root = f['/']
```

``` python
list(root.keys())
```

    ['array', 'dataset', 'full']

``` python
list(f['full'].keys())
```

    ['bigger', 'dataset']

## Sources

-   [Managing Large Datasets with Python and HDF5 - O'Reilly Webcast](https://www.youtube.com/watch?v=wZEFoVUu8h0)
