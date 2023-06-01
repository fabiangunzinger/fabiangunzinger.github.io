---
title: "Command-line utilities"
date: "2023-05-21"
category: craft
tag: tools
format: hugo-md
jupyter: python3
draft: false
math:
  enable: true
---

# Getting help

## `man`

-   Displays and formats the on-line manual pages.

-   Invoke by typing `man` followed by the name of the command you want to know more about.

## `info`

-   Displays and formats the entire documentation of a command.

# Searching

-   First, conceptually understand the difference between grep, find, and fzf, and then understand the role of ripgrep (fast grep), and fd (fast find)

## `grep`

-   Searches for a pattern in a file or files.

-   To find all markdown files in the current directory and subdirectories that contain the word "python":

``` bash
grep -r --inlcude="*.md" "python" .
```

## `find`

## `rg`

# File manipulation

## `sed`

## `awk`

## `xargs`

## `sort`

## `uniq`

## `cat`

## \`cut

## `paste`

## `tr`

## `head`

## `tail`

## `wc`

## `diff`
