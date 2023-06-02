---
title: "Data analysis checklists"
subtitle: ""
tags: [datascience]

date: 2022-03-27
featured: false
draft: true

reading_time: false
profile: false
commentable: true
summary: " "

---

A list of checklists to ensure consistency and quality across key data science
tasks.

## General

- Use samples of different sized for code development if useful, but don't
  switch back and forth between samples for analysis (might get hung up on
  explaining small sample artifacts).



## Regression model specification

- Does it make sense to take logs of currency amounts or large integers
  (especially if there are few cases with zero, in which case using *log(x +
  1)* is usually fine to avoid missing values from zeroes)?

- Does it make sense to standardise some variables to interpret changes in std
  or even standardise all variables (to get Beta coefficients) to easily gage
  relative importance of variables?

- Have I included variables that I shouldn't have given the ceteris-paribus
  interpretation of the coefficients (e.g. include alcohol consumption when
  estimating effect of alcohol tax on traffic fatalities, which will mostly run
  through lower alcohol consumption).

- Are there variables that are correlated with *y* but not the included *x*s
  that I haven't included yet? (If so, I should, as it increases precision of
  the estimates without causing multicollinearity issues.)


