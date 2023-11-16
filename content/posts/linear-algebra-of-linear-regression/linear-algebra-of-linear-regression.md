---
title: "Linear algebra of linear regression"
subtitle: ""
tags: [stats]
date: 2023-10-23
featured: false
draft: true
profile: false
commentable: true
---

ho

We can think of a projection as an operation that maps a vector onto a subspace. The result of a projection is a vector that lies within the subspace and is the closest point in the subspace to the original vector.
m
\## Projection in 1-D

The easiest way to visualise a projection is when we project a vector $b$ in 2-dimensional space onto a line $a$ (because a line is a 1-dimensional object, it is a subspace of the vector).

We thus want to find the point on $a$ that is closest to $b$.

-   Use calculus approach below to find c, to show that result is orthogonal to line (as expected from intuition).

## Projection in 2-D

-   Formula
-   Geometric interpretation

Where does the projection matrix come from? provides a nice example that I'm going to borrow here (the site has a useful visualisation that I'm not going to redraw here). If we have a point $x$ in two dimensional space and a line $L$ in that same space, then the projection of $x$ onto $L$, $\bar{x}$, is the point on $L$ that is closest to $x$. If we think of $L$ as being formed by a vector $v$ and a set of scalar multiples $c$, we want to find the one scalar multiple $c$ for which the Euclidian distance between $x$ and $\bar{x}$, $\sqrt{\sum_i{(\bar{x_i} - x})^2}$ (the index $i$ ranges over all dimensions), is minimised -- we're looking for $\bar{x} = c^*v$, where $c^*$ is the optimal c. Formally, we want to find

$$
\begin{aligned}
\frac{d}{dc} \sum_{i} (cv_i - x)^2 & = \sum_{i}2v_i(cv_i - x) \\
& = 2(\sum_{i}cv_i^2  - \sum_{i}v_ix) \\
& = 2(cv'v - v'x) \Rightarrow 0
\end{aligned}
$$

$$
arg min_c \sqrt{\sum_i{(\bar{x_i} - x})^2}
$$

$$
arg min_c \sqrt{\sum_i{(\bar{x_i} - x})^2}
= arg min_c \sum_i{(\bar{x_i} - x})^2
= arg min_c \sum_i{(cv_{i} - x})^2,
$$

where the first equality holds because the square root is a monotonic transformation and the second because we have defined as $\bar{x} = c^*v$. To find $c^*$, we can differentiate and setting the result equal to zero

$$
\begin{aligned}
\frac{d}{dc} \sum_i{(cv_{i} - x})^2 &= \sum_i{2v_{i}(cv_{i} - x}) \\
& = 2\left(\sum_i{cv_{i}^2} - \sum_i{v_{i}x}\right) \\
&= 2(cv'v - v'x) & \text{using vector notation} \\
&= 0
\end{aligned}
$$

and solve for $c$:

$$
\begin{align*}
2(cv'v - v'x) &= 0 \\
cv'v - v'x &= 0 \\
cv'v &= v'x \\
c &= (v'v)^{-1}v'x
\end{align*}
$$

Remembering that $\bar{x} = vc$, we get:

$$
\bar{x} = vc = \underbrace{v(v'v)^{-1}v'}_\text{$P_v$}x,
$$

where $P_v = v(v'v)^{-1}v'$ is the projection matrix of $x$ onto $v$. Once we understand what the projection matrix is -- the function we apply to $x$ to find the nearest point on $v$ -- and know that we define "rearest" as minimising the Euclidean distance, this intimate link between minimising the Euclidean distance and the projection matrix is no surprise.

What does this mean in the context of linear regression? In the context of linear regression, with a covariance matrix $X$, the projection matrix is $P = X(X'X)^{-1}X'$. The coefficient estimates are given by:

$$
\hat{\beta} = (X'X)^{-1}X'y.
$$

and the predicted values are given by:

$$
\hat{y} = X\hat{\beta} = X(X'X)^{-1}X'y = Py.
$$

This tells us that the fitted values in a linear regression are a projection of the vector of observed outcomes, $y$, onto the subspace spanned by $X$.

Finally, the residuals of the linear model are:

$$
\hat{\epsilon} = y - \hat{y} = y - X\hat{\beta} = y - X(X'X)^{-1}X'y = My,
$$

where $M = I - X(X'X)^{-1}X'$. Hence, $M$ is called the residual-maker matrix because it is the matrix that, when pre-multiplied to the vector $y$, returns the vector of residuals.

## Useful resources

-   [Gilbert Strang's linear algebra lectures at MIT](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/video_galleries/video-lectures/)

-   [10 Fundamental Theorems for Econometrics](https://bookdown.org/ts_robinson1994/10EconometricTheorems/linear_projection.html#linear_projection)
