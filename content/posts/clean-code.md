---
title: "Clean code"
subtitle: "An evolving set of principles I try to adhere to"
tags: [cs]

date: 2021-07-22
featured: false
draft: false

reading_time: true
profile: false
commentable: true
summary: " "

---


> When people look under the hood, we want them to be impressed by the neatness,
> consistency, and attention to detail [...] If instead they see a scrambled
> mass of code that looks like it was written by a bevy of drunken sailors, then
> they are likely to conclude that the same inattention to detail pervades every
> other aspect of the project. Robert Martin, *Clean Code*


## Definitions

- A design pattern is a general repeatable solution to a frequently occuring
  problem.

- An idiom is the translation of a design pattern into code using the language
  clearly and correctly.


## Principles

- Don't repeat yourself. Collect often used pieces of code in a function of
  class for reuse. Don't copy and paste more than once.

- Single Responsibility Principle (SRP): a class or module should only have a
  single reason to change -- it should be responsible to a single actor that can
  demand change. Example: an employee class that produces outputs for the
  finance and HR departments violates the principle, as both the CFO and the CHO
  might demand changes that then unintenionally affects the output seen by the
  other. Solution: Separate code that different actors depend on. Corollary:
  don't reuse a function for two different outputs just because it does they
  require the same task, only reuse the function for two outputs that require
  the same task *and* have a common owner. Example, don't if both HR and finance
  need to calculate regular hours, don't use the same function, as the CFO might
  want to change the definition of regular hours but HR doesn't.

- Open-Closed Principle (OCP): classes should be open for extension and closed
  for modification. (We should easily be able to add new functionality without
  having to change existing functionality.)

- Use names to make the context explicit (e.g. "for user in users" is explicit,
  "for i in list" isn't).

- Get to proof of concept asap.

- "You ain't gonna need it" (YAGNI). Don't add functionality before it's really
  necessary.


## Names

- Choose names that make clear what a thing is, what it does, and how it is used.

- Use plain and unabbreviated words.

- Omit needless words like "get" or "calculate", but remember that "terseness
  and obscurity are the limits where brevity should
  [stop](https://docs.python-guide.org/writing/structure/)". 

- Use verbs or verb phrases for functions, nouns for classes.

- Choose names of variables in proportion to their scope.

- Whenever appropriate, use names from the solution domain (e.g. computer or
  data science) or the problem domain (e.g. personal finance) otherwise.


## Functions

- Functions should do one thing and one thing only and should do it well. (It's
  not always obvious what "one thing" is, use your judgement.)

- Make functions as short as possible to make it obvious how they work and what
  they are for.

- Most often, blocks inside flow control statements should be one line long -
  calls to transparently named functions.

- A good function interface allows the user to do what they need without having
  to worry about unnecessary details. Hence: ask for the minimally required
  number of intuitive arguments and return the expected output.

- Write pure functions. A function is pure when it is idempotent (returns the
  same output for a given input) and has no side-effects.


## Comments and docstrings

- Don't comment bad code -- rewrite it.

- Add docstrings to functions unless -- following
  [Google](https://google.github.io/styleguide/pyguide.html#383-functions-and-methods)
  -- they are helpers, short and obvious.


## Modules

- Use the `module.function` idiom (i.e. use `import module` rather than `from
  module import function`) in all but the simplest projects.


## Systems

- Kent Beck's four rules for a simply designed system (in order or importance):

    - It runs all tests

    - Contains no duplication

    - Expresses the intent of the programmer (choose expressive names, keep
      functions and classes small, use standard nomenclature, good unit tests)

    - Minimises the number of classes and methods


## Resources

- [Clean Code](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)

- [The Hitchhiker's Guide to Python, code
  style](https://docs.python-guide.org/writing/style/#code-style)

- [IPython cookbook, writing high-quality Python
  code](https://github.com/ipython-books/cookbook-2nd/blob/master/chapter02_best_practices/07_high_quality.md)

- [Google style guide](https://google.github.io/styleguide/pyguide.html)

- [Jeff Knupp
  post](https://jeffknupp.com/blog/2018/10/11/write-better-python-functions/)

- [Think Python](https://greenteapress.com/wp/think-python-2e/)
