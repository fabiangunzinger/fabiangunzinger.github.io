---
title: "AWS"
date: "2020-03-14"
tags:
    - tools
---

Frequently used interaction patterns with AWS.

## CLI

-   To create a new bucket, use `aws s3 mb bucketname`.

-   To add a subfolder to a bucket, use `aws s3api put-object --bucket bucketname   --key foldername`

## Setup

-   There are multiple ways to access your AWS account. I store config and credential files in `~/.aws` as discussed [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html). AWS access methods find these files automatically so I don't have to worry about that.

-   What I do have to worry about is choosing the appropriate profile depending on what AWS account I want to interact with (e.g. my personal one or one for work). This is different for each library, so I cover this below.

## `s3fs`

Built by people at Dask, [`s3fs`](https://github.com/dask/s3fs) is built on top of `botocore` and provides a convenient way to interact with S3. It can read and -- I think -- write data, but there are easier ways to do that, and I use the library mainly to navigate buckets and list content.

### Navigate buckets

``` python
import s3fs

# establish connection
fs = s3fs.S3FileSystem()

# count items in s3 root bucket
fs.ls('/fgu-samples')
```

To choose a profile other than `default`, use:

``` python
# connect using a different profile
fs = s3fs.S3FileSystem(profile='tracker-fgu')
len(fs.ls('/'))
```

# Read and write directly from `Pandas`

-   Pandas can read and write files to and from S3 directly if you provide the file name as `s3://<bucket>/<filename>`.

-   By default, `Pandas` uses the default profile to access S3. Recent versions of `Pandas` have a `storage_options` parameter that can be used to provide, among other things, a profile name.

## Basics

``` python
import pandas as pd

# read using default profile 

fp = 's3://fgu-samples/transactions.parquet'
df = pd.read_parquet(fp)
df.shape
```

``` python
# read using custom profile

fp = 's3://temp-mdb/data_XX7.parquet'
df = pd.read_parquet(fp, storage_options = dict(profile='tracker-fgu'))
df.shape
```

This works well for simple jobs, but in a large project, passing the profile information to each read and write call is cumbersome and ugly.

## Simple improvement using `functools.partial`

`functools.partial`provides a simple solution, as it allows me to create a custom function with a frozen storage options argument.

``` python
import functools

options = dict(storage_options=dict(profile='tracker-fgu'))
read_parquet_s3 = functools.partial(pd.read_parquet, **options)
df = read_parquet_s3(fp)
df.shape
```

## More flexible solution with custom function

Often, I run projects on my Mac for testing and a virtual machine to run the full code. In this case, I need a way to automatically provide the correct profile name.

``` python
s3 = s3fs.S3FileSystem(profile='tracker-fgu')
s3.ls('/raw-mdb/')
```

``` python
import functools
import platform

def get_aws_profile():
    """
    Return access point specific AWS profile to use for S3 access.
    """
    if platform.node() == 'FabsMacBook.local':
        profile = 'tracker-fgu'
    else:
        profile = 'default'

    return profile


class s3:
    """
    Create read and write functions with frozen AWS profile.
    """
    def __init__(self):
        self.profile = get_aws_profile()
        self.options = dict(storage_options=dict(profile=self.profile))
        
    def read_csv(self):
        return functools.partial(pd.read_csv, **self.options)
    
    

def make_s3_funcs():
    """
    Return readers and writers with frozen AWS profile name.
    """
    # identify required profile (depends on project)
    if platform.node() == 'FabsMacBook.local':
        profile = 'tracker-fgu'
    else:
        profile = 'default'
        
    # create partial readers and writers
    options = dict(storage_options=dict(profile=profile))
    read_csv_s3 = functools.partial(pd.read_csv, **options)
    write_csv_s3 = functools.partial(pd.write_csv, **options)
    read_parquet_s3 = functools.partial(pd.read_parquet, **options)
    write_parquet_s3 = functools.partial(pd.write_parquet, **options)
    
fp = 's3://raw-mdb/data_777.csv'
    
s3.read_csv(fp)
```

The above is not ideal, as it requires cumbersome unpacking of return. Maybe using decorator is better.

## `awswrangler`

A new [library](https://github.com/awslabs/aws-data-wrangler) from AWS labs for Pandas interaction with a number of AWS services. Looks very promising, but haven't had any use for it thus far.
