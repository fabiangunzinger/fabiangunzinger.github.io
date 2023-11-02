---
title: "The linear algebra of linear regression"
subtitle: ""
tags: [stats]
date: 2023-10-23
featured: false
draft: true
profile: false
commentable: true
---

Linear regression is by far the most often used method to estimate relationships between outcomes and explanatory variables in applied econometrics and -- probably -- all of applied social science. In this article I want to to two things: define the related terminology that is often used but not defined (OLS, linear equation, etc.) and -- mainly -- explain a less frequently taught and understand way to think about linear regression, that in terms of its linear algebra.

There are, of course, a lot of very good resources on linear regression and OLS, and I list my favourite ones at the bottom. But none of them quite tie everything together in the way I was looking for.

There are two ways to understand linear regression: one is to think of the variables involved as dimensions and of each row as a data point -- this is the way the problem is usually motivated in introductory econometrics classes. The other is the linear algebra approach -- to think of each row of data as a dimension, and to think of the variable as vectors in the space formed by those dimensions.

The first approach straightforwardly links to the intuition of minimising squares, which is useful. It's the one I have learned and relied on most of my life. The second one, though, provides an alternative and very powerful way to understand what linear regression does. And, importantly, understanding the linear algebra notation simplifies much of the notation and manipulations, and opens the way to much of the literature of econometric theory, such as an understanding of the Frisch-Waugh-Lowell theorem, which was the impetus for me to dig into the linear algebra of OLS.

In this post I want to cover the following:

-   Understand all the terminology related to linear regression so we fully know what we're talking about

-   Understand the matrix representation of linear regression

-   Understand how we can think of the least squares solution as a projection

-   Understand why this is a very useful way of seeing things

## The setup

We usually start with data of the form (y variable and x variables)

We think that it might be reasonable to think of the outcome being linearly related to the regressors, so that, for each unit in our dataset, we can write the following linear equation:
s
$$
y_{i} = \beta_{1}x_{i1} + \beta_{2}x_{i2} + ... + \beta_{k}x_{ik} + \epsilon_{i} 
$$

Notice what makes this a "linear" equation:
- The highest power to which any regressor is raised is 1
- The coefficients are constants, not variables
- Regressors are related to one another using addition and subtraction only
- The resulting line (in 2-D space), plane (in 3-D space) and hyperplane (in N-D space) are linear (the term linear equation originates from the simple case where there are two regressors, one of which is a constant, in which case we get a straight line in a Cartesian plane.)

What are the assumptions we're making here?

-   The relationship between y and the regressors x is linear

-   The error term is random

<!-- todo: look at Angrist and Pischke for discussion on use of OLS if relationship is not linear -- BLUE -->


- We thus have a system of $n$ linear equations

- Can rewrite in vector notation

- Can rewrite in matrix notation


## Classic motivation

## Linear algebra motivation


$$
Y_1 = \beta_0 + \beta_1 X_{1_1} + \beta_2 X_{2_1} + \ldots + \beta_k X_{k_1} + \varepsilon_1 \\
Y_2 = \beta_0 + \beta_1 X_{1_2} + \beta_2 X_{2_2} + \ldots + \beta_k X_{k_2} + \varepsilon_2 \\
Y_n = \beta_0 + \beta_1 X_{1_n} + \beta_2 X_{2_n} + \ldots + \beta_k X_{k_n} + \varepsilon_n \\
$$





## Resources

- Hayashi, Wooldridge, Verbeek, online resources
