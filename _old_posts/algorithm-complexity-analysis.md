---
title: "Algorithm complexity analysis"
subtitle: "Notes and exercises"
tags: [cs]

date: 2021-11-21
featured: false
draft: false

reading_time: true
profile: false
commentable: true
summary: " "

---

- The goal of algorithm analysis is to study the efficiency of an algorithm in
  a language and machine-independent way.

- The two most important tools for this are (1) the RAM model of computation
  and (2) the asymptotic analysis of worst-case complexity.

- The Random Access Machine (RAM) model of computation is a simple model of a
  generic computer that is based on three main assumptions: (1) each simple
  operation takes exactly one time step, (2) loops and subroutines are
  considered composites of all simple operations they perform, and (3) memory
  access from cache and RAM takes one time unit. None of these hold in
  practice, but the model is extremely useful because it captures the essence
  of algorithm behaviour while being very simple to work with.

- Best, worst, and average-case complexity are functions defined by the
  minimum, maximum, and average number of steps taken for any instance of size
  *n* of the input string. (Think about a graph with *n* on the x-axis and *number
  of steps* on the y-axis, with number of steps for each instance of a problem
  of size *n* forming columns of dots with increasing variation as *n* -- and
  thus the number of possible instances -- increases. The three functions trace
  the lowest, highest, and middle dots at each input size *n*. See Fig 2.1 in
  ADM.)

- Using these functions to analyse algorithms is impractical, however, because
  they are not smooth and require lots of detail about the algorithm and its
  implementation.

- Big O notation ignores such details and focuses on the essentials to capture
  the rate at which runtime (or space requirements) grow as a function of the
  input size (the letter O is used because the growth rate of a function is
  also called its order). In essence, this means only focusing on the higest
  order term and ignoring constants (which depend on things like hardware and
  programming language used to run the algorithm).

- A function $f(n)$ is $O(g(n))$ if there exist constants $c$ and $n_0$ such
  that $f(n) \leq cg(n)$ for any $n > n_0$.  Intuitively, this means that
  $f(n)$ grows no faster than $cg(n)$ above a certain input size. For example:
  $T(n) = 2n^2 + 3n$ is $O(n^2)$, since $5n^2 \geq 2n^2 + 3n$ for all positive
  values of $n$.

- Amortised worse-case complexity takes into account that the running time of a
  given operation in an algorithm may take a very long or a very short time
  depending on the situation, and averages those different running times of the
  operation in a sequence over that sequence. Adding an element to an array
  that is dynamically resized takes $O(1)$ time until the array is full, when
  the array needs to create a new array of twice its original size, copy all
  elements over to the new array, and add the new element, which takes $O(n)$
  time. Average worst-case complexity averages these runtimes to find that
  pushing elements onto a dynamically resized array takes: $\frac{nO(1) +
  O(n)}{n + 1} = O(1)$, constant time.
  ([Source](https://en.wikipedia.org/wiki/Amortized_analysis#Dynamic_array))

Exercises:

1. Is $2^{n+1} = O(2^n)$?

2. Is $(x + y)^2 = O(x^2 + y^2)$?

3. What's the time complexity of $f(n) = min(n, 100)$?


Solutions:

1. The way to go is to start from the definition. The statement is true if
   there is a $c$ and $n_0$ for which $c2^n \geq 2^{n+1}$ for $n > n_0$. The key
   is to rewrite the right hand side to $c2^n \geq 2 \times 2^n$, which
   makes it obvious that the statement holds whenever $c \geq 2$.

2. Starting from the definition, the statement is true if there exist constants
   $c$ and $n_0$ for which $c(x^2 + y^2) \geq (x + y)^2$ for $n > n_0$. Expanding
   the right hand side, we get $c(x^2 + y^2) \geq x^2 + 2xy + y^2$.
   Ignoring the middle term, the statement holds for $c = 1$; considering
   only the middle term, we see that it is largest when $x = y$, in which
   case the statement holds for $c = 2$. Thus, $3(x^2 + y^2) \geq (x +
   y)^2$, so the statement is true.

3. I reflexively answered $n$. Thinking for a moment (an embarassingly long
   one, admittedly), I realised that $n$ here refers not to the length of an
   array but to a single number. So the operation is $O(1)$.



## Sources

- [Steven Skiena, The Algorithm Design Manual (ADM)](https://www.algorist.com)  

- [MIT, Big O notation](https://web.mit.edu/16.070/www/lecture/big_o.pdf)

- [Wikipedia, Big O notation](https://en.wikipedia.org/wiki/Big_O_notation)
