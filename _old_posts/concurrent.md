---
title: "Concurrent code"
subtitle: "Notes"
tags: [python]

date: 2022-05-19
featured: false
draft: true

reading_time: true
profile: false
commentable: true
summary: " "
---

## Resources

- Super promising looking tutorial: https://superfastpython.com/processpoolexecutor-in-python/
- Also useful: https://realpython.com/python-concurrency/

## Glossary

- Asynchronous: not occurring or existing at the same time.

- Thread: a component of a process, that shares resources (memory, dynamically
  allocated variables) with other threads of the same process.

- Concurrency: a form of computation in which several computations are executed
  concurrently -- during overlapping time periods -- instead of sequentially.

- Subroutine (type of function): a function calling model in which each time a program calls a
  function, control moves to the function, runs the code in the function body
  top to bottom, and then returns control back to the calling program, which
  continues at the point immediately after the function was called. Subsequent
  calls to the same function are independent of previous calls, and again run
  the function body from top to bottom.

- Coroutine (type of function): a function calling model in which the function yiels rather than
  returns control to the calling function, with the result that subsequent
  calls to the coroutine run code starting immediately after the point where
  control was last yielded.

## ThreadPoolExecutor

- `map()` applies function to iterable asynchronously (instead of sequentially,
  as in the case of the built-in `map()` function).







