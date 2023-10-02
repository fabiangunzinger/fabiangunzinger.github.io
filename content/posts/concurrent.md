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

## Theory

Elements:
- RAM
- memory controller (interface between cup and ram)
- CPU
- Kernel
    - Lowest level of software. It manages cpu resources, file system, memory resources, drivers, networking, etc.

- Program
    - Code and data structures that can be executed (like newspaper)


- Cores (units of cpu?)
    - Multi core: instead of dividing up cpu time among different processes, can actually run stuff in parallel, but within each core, the process is exactly the same as with only one core.

- Process
    - A logical container that tells kernel what program to run. Process has id, priority, status, memory space, etc.. Kernel uses that info to allocate cpu time to each program. Because happens at milisecond level, creates illusion of concurrency (comic analogy).
    - A program that competes for CPU resources (e.g. a web browser, or a bit of cleaning code)
    - The program in execution. Given that program is composed of multiple threads, program is program + state of all threads executing the program 
    
- Threads
    - Threads run within a single process, to allow it to do multiple things at once (like a newspaper)
    - They are lines of control cursing through the code and data structures of the program (called a thread of execution through the program). Akin to one reader scanning through a section of the newspaper.
    - Multiple threads: different lines of control cursing through the program (multiple readers reading different sections of the newspaper).
    - Potential conflict: threads operate on (read/update) same data structures. Solution: locks
    - A ... running within a program (e.g. reading data, processing, writing to disk) 


Type of tasks: 
- CPU-bound tasks: using CPU to crunch numbers 

- I/O-bound tasks: waiting for some I/O operations to complete (downloading files from internet, reading and writing to file-system)

Theading:
- Gives speed ups for I/O-bound tasks


Multiprocessing:
- Run CPU-bound tasks in prallel 


## Misc.

Check number of CPUs:

```python
os.cpu_count()
```

## Sources

- [Udacity on process vs threads](https://www.youtube.com/watch?v=O3EyzlZxx3g)
- [Gary explains - processes and threads](https://www.youtube.com/watch?v=h_HwkHobfs0)
- [Gary explains - what is a kernel](https://www.youtube.com/watch?v=mycVSMyShk8)
- [Corey Schafer on threading](https://www.youtube.com/watch?v=IEEhzQoKtQU)
- [Fluent Python](https://www.oreilly.com/library/view/fluent-python/9781491946237/)
- [Python Cookbook](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/)
- [Learning Python](https://www.oreilly.com/library/view/learning-python-5th/9781449355722/)
- [Python for Data Analysis](https://www.oreilly.com/library/view/python-for-data/9781491957653/)
- [Python Data Science Handbook](https://www.oreilly.com/library/view/python-data-science/9781491912126/)