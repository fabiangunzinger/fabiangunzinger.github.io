---
title: Python functions
date: '2020-10-05'
tags:
  - python
execute:
  enabled: false
---


## Functions as first-class objects

In Python, functions are first-class objects.

First-Class functions:
"A programming language is said to have first class functions if it treats functions as first-class citizens."

First-Class Citizen (Programming):
"A first-class citizen (sometimes calles first-class object) is an entity which supports all the operations generally available to other entities, such as being being passes as an argument, returned from a function, and assigned to a variable."

Assign function to variables

``` python
def square(x):
    return x * x


f = square(5)  # Assign function *output* to variable
f = square  # Assign function to variable (no (), as this triggers execution)

print(square)
print(f)  # f points to same object as square
print(f.__name__)

f(5)
```

    <function square at 0x106f968b0>
    <function square at 0x106f968b0>
    square

    25

Use function as argument in function

``` python
print(map(lambda x: x ** 2, [1, 2, 3]))
filter(lambda x: x % 2 == 0, [1, 2, 3])
```

    <map object at 0x106fd07c0>

    <filter at 0x106f9ca90>

``` python
def do_twice(fn, *args):
    fn(*args)
    fn(*args)


do_twice(print, "Hello world!")
```

    Hello world!
    Hello world!

Return function from function

``` python
def create_adder(n):
    def adder(m):
        return n + m

    return adder


add_5 = create_adder(5)
print(add_5.__name__)
add_5(10)
```

    adder

    15

## Attributes of user-defined functions

``` python
def greeter(text="Hello"):
    """Print greeting text."""
    print(text)


def printer(func):
    print("Docstring:", func.__doc__)
    print("Name:", func.__name__)
    print("Attributes:", func.__dict__)
    print("Code:", func.__code__)
    print("Defaults:", func.__defaults__)
    print("Globals:", func.__globals__.keys())
    print("Closures:", func.__closure__)


printer(greeter)
```

    Docstring: Print greeting text.
        
    Name: greeter
    Attributes: {}
    Code: <code object greeter at 0x7fbc814a3ea0, file "<ipython-input-28-dd4fd47dbd24>", line 1>
    Defaults: ('Hello',)
    Globals: dict_keys(['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__builtin__', '__builtins__', '_ih', '_oh', '_dh', 'In', 'Out', 'get_ipython', 'exit', 'quit', '_', '__', '___', '_i', '_ii', '_iii', '_i1', 'greeter', 'printer', '_i2', '_i3', '_i4', '_i5', '_5', '_i6', '_6', '_i7', '_7', '_i8', 'c', '_i9', '_i10', '_i11', '_i12', '_i13', '_i14', '_i15', '_i16', '_16', '_i17', '_i18', '_18', '_i19', '_19', '_i20', '_20', '_i21', '_21', '_i22', '_i23', '_23', '_i24', '_i25', '_i26', '_26', '_i27', '_i28'])
    Closures: None

-   The global attribute points to the global namespace in which the function was defined.

Some of these attributes return objects that have attributes themselves:

``` python
print(greeter.__doc__.upper())
print(greeter.__doc__.splitlines())
```

    PRINT GREETING TEXT.
        
    ['Print greeting text.', '    ']

``` python
print(greeter.__code__.co_argcount)
print(greeter.__code__.co_code)
```

    1
    b't\x00|\x00\x83\x01\x01\x00d\x01S\x00'

## Function scoping rules

-   Each time a function executes, a new local namespace is created that contans the function arguments and all variables that are assigned inside the function body.
-   Variables that are assigned inside the function body are local variables; those assigned outside the function body are global variables.
-   To resolve names, the interpreter first checks the local namespace, then the global namespace, and then the build-in namespace.
-   To change the value of a global variable inside the (local) function context, use the `global` declaration.
-   For nested functions, the interpreter resolves names by checking the namespaces of all enclosing functions from the innermost to the outermost, and then then global and built-in namespaces. To reassign the value of a local variable defined in an enclosing function use the `nonlocal` declaration.

### Use of `global`

Because `a` is assigned inside the function body, it is a local variable in the local namespace of the `f` function and a completely separate object from the variable `a` defined in the global namespace.

``` python
a = 5


def f():
    a = 10


f()
a
```

    5

`global` declares the `a` variable created inside the function body to be a global variable, making it reassing the previously declared global variable of the same name.

``` python
a = 5


def f():
    global a
    a = 10


f()
a
```

    10

### Use of `nonlocal`:

Because `n` reassigned inside `decrement`, it is a local variable of that function's namespace. But because `n -= 1` is the same as `n = n - 1` and Python first runs the right hand side of assignment statements, when running `n - 1` throws an error because there it is asked to reference the variable `n` that hasn't been assigned yet.

``` python
def countdown(n):
    def display():
        print(n)

    def decrement():
        n -= 1

    while n:
        display()
        decrement()


countdown(3)
```

    3

<pre><span class="ansi-red-fg">---------------------------------------------------------------------------</span>
<span class="ansi-red-fg">UnboundLocalError</span>                         Traceback (most recent call last)
<span class="ansi-green-fg">&lt;ipython-input-21-473dc28d8ecc&gt;</span> in <span class="ansi-cyan-fg">&lt;module&gt;</span>
<span class="ansi-green-fg ansi-bold">     12</span> 
<span class="ansi-green-fg ansi-bold">     13</span> 
<span class="ansi-green-fg">---&gt; 14</span><span class="ansi-red-fg"> </span>countdown<span class="ansi-blue-fg">(</span><span class="ansi-cyan-fg">3</span><span class="ansi-blue-fg">)</span>

<span class="ansi-green-fg">&lt;ipython-input-21-473dc28d8ecc&gt;</span> in <span class="ansi-cyan-fg">countdown</span><span class="ansi-blue-fg">(n)</span>
<span class="ansi-green-fg ansi-bold">      9</span>     <span class="ansi-green-fg">while</span> n<span class="ansi-blue-fg">:</span>
<span class="ansi-green-fg ansi-bold">     10</span>         display<span class="ansi-blue-fg">(</span><span class="ansi-blue-fg">)</span>
<span class="ansi-green-fg">---&gt; 11</span><span class="ansi-red-fg">         </span>decrement<span class="ansi-blue-fg">(</span><span class="ansi-blue-fg">)</span>
<span class="ansi-green-fg ansi-bold">     12</span> 
<span class="ansi-green-fg ansi-bold">     13</span> 

<span class="ansi-green-fg">&lt;ipython-input-21-473dc28d8ecc&gt;</span> in <span class="ansi-cyan-fg">decrement</span><span class="ansi-blue-fg">()</span>
<span class="ansi-green-fg ansi-bold">      5</span> 
<span class="ansi-green-fg ansi-bold">      6</span>     <span class="ansi-green-fg">def</span> decrement<span class="ansi-blue-fg">(</span><span class="ansi-blue-fg">)</span><span class="ansi-blue-fg">:</span>
<span class="ansi-green-fg">----&gt; 7</span><span class="ansi-red-fg">         </span>n <span class="ansi-blue-fg">-=</span> <span class="ansi-cyan-fg">1</span>
<span class="ansi-green-fg ansi-bold">      8</span> 
<span class="ansi-green-fg ansi-bold">      9</span>     <span class="ansi-green-fg">while</span> n<span class="ansi-blue-fg">:</span>

<span class="ansi-red-fg">UnboundLocalError</span>: local variable 'n' referenced before assignment</pre>

`nonlocal` declares `n` to be a variable in the scope of an enclosing function of `decrement`.

``` python
def countdown(n):
    def display():
        print(n)

    def decrement():
        nonlocal n
        n -= 1

    while n:
        display()
        decrement()


countdown(3)
```

    3
    2
    1

## Closures

> A closure is the object that results from packaging up the statements that make up a function with the environment in which it executes. David Beazley, Python Essential Reference

> A closure is a function that has access to variables that are neither global nor local (i.e. not defined in the function's body). Luciano Ramalho, Fluent Python

> A closure is an inner function that remembers and has access to variables in the local scope in which it was created, even after the outer function has finished executing. - 'A closure closes over the free variables from the environment in which they were creates'. - A free variable is a variable defined inside the scope of the outer function that is not an argument in the inner function. Below, the 'free variable' is message. Stanford CS course

How I think of them (not sure that's correct):

-   The closure attribute of a user-defined function is non-empty if the function is defined inside the scope of an outer function and references a local variable defined in the scope of the outer function. From the point of view of the inner function, said variable is a nonlocal variable.

-   A user-defined function is a closure if its closure attribute is non-empty.

In the first case below, the inner function doesn't reference a nonlocal variable and thus isn't a closure. In the second case, it does reference a nonlocal variable, which gets stored in its `closure` attribute, which makes `inner` a closure.

``` python
def outer():
    x = 5

    def inner():
        print("Hello")

    return inner


def outer2():
    x = 5

    def inner():
        print(x)

    return inner


g = outer()
print(g.__closure__)

g = outer2()
print(g.__closure__[0].cell_contents)
```

    None
    5

## Mutable function parameters

*Notes based on chapter 8 in [Fluent Python](https://www.oreilly.com/library/view/fluent-python/9781491946237/).*

Functions that take mutable objects as arguments require caution, because function arguments are aliases for the passed arguments (i.e. they refer to the original object). This can cause unintended behaviour in two types of situations:

-   When setting a mutable object as default
-   When aliasing a mutable object passed to the constructor

### Setting a mutable object as default

``` python
class HauntedBus:
    def __init__(self, passengers=[]):
        self.passengers = passengers

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)


bus1 = HauntedBus(["pete", "lara", "nick"])
bus1.drop("nick")
print(bus1.passengers)

bus2 = HauntedBus()
bus2.pick("heather")
print(bus2.passengers)

bus3 = HauntedBus()
bus3.pick("katy")
print(bus3.passengers)
```

    ['pete', 'lara']
    ['heather']
    ['heather', 'katy']

Between bus 1 and 2, all works as intended, since we passed our own list when creating bus 1. Then things get a bit weird, though: how did Heather get into bus 3? When we define the `HauntedBus` class, we create a single empty list that is kept in the background and will be used whenever we instantiate a new bus without a custom passenger list. Importantly, all such buses will operate on the same list. We can see this by checking the object ids of the three buses' passenger lists:

``` python
assert bus1.passengers is not bus2.passengers
assert bus2.passengers is bus3.passengers
```

This shows that while the passenger list of bus 1 and 2 are not the same object, the lists of bus 2 and 3 are. Once we know that, the above behaviour makes sense: all passenger list operations on buses without a custom list operate on the same list. Anohter way of seeing this by inspecting the default dict of `HauntedBus` after our operations abve.

``` python
HauntedBus.__init__.__defaults__
```

    (['heather', 'katy'],)

The above shows that after the `bus3.pick('katy')` call above, the default list is now changed, and will be inherited by future instances of `HauntedBus`.

``` python
bus4 = HauntedBus()
bus4.passengers
```

    ['heather', 'katy']

This behaviour is an example of why it matters whether we think of variables as boxes or labels. If we think that variables are boxes, then the above bevaviour doesn't make sense, since each passenger list would be its own box with its own content. But when we think of variables as labels -- the correct way to think about them in Python -- then the behaviour makes complete sense: each time we instantiate a bus without a custom passenger list, we create a new label -- of the form `name-of-bus.passengers` -- for the empty list we created when we loaded or created `HauntedBus`.

What to do to avoid the unwanted behaviour? The solution is to create a new empty list each time no list is provided.

``` python
class Bus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)


bus1 = Bus()
bus1.pick("tim")
bus2 = Bus()
bus2.passengers
```

    []

### Aliasing a mutable object argument inside the function

The `init` method of the above class copies the passed passenger list by calling `list(passengers)`. This is critical. If, instead of copying we alias the passed list, we change lists defined outside the function that are passed as arguments, which is probably not what we want.

``` python
class Bus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = passengers

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)


team = ["hugh", "lisa", "gerd", "adam", "emily"]

bus = Bus(team)
bus.drop("hugh")
team
```

    ['lisa', 'gerd', 'adam', 'emily']

Again, the reason for this is that `self.passengers` is an alias for `passengers`, which is itself an alias for `team`, so that all operations we perfom on `self.passengers` are actually performed on `team`. The identity check below shows what the passengers attribute of `bus` is indeed the same object as the team list.

``` python
bus.passengers is team
```

    True

**To summarise:** unless there is a good reason for an exception, for functions that take mutable objects as arguments do the following:

1.  Create a new object each time a class is instantiated by using None as the default parameter, rather than creating the object at the time of the function definition.

2.  Make a copy of the mutable object for processing inside the function to leave the original object unchanged.

## Functional programming

A programming paradigm built on the idea of composing programs of functions,
rather than sequential steps of execution.

Advantages of functional programming:
- Simplifies debugging
- Shorter and cleaner code
- Modular and reusable code

Memory and speed considerations:
- Map/filter more memory efficient because they compute elements only when called, while list comprehension buffers them all.
- Call to map/filter if you pass lambda comes with extra function overhead which list comprehension doesn't have, which makes the latter usually faster.

See [here](https://docs.python.org/3/howto/functional.html) for more.

### Exercises

*Mapping* is the process of applying a function elementwise to an array and storing the result. Apply the `len` function to each item in `a` and return a list of lengths.

``` python
a = ["a", "ab", "abc", "abcd"]
```

Procedural approach.

``` python
def lengths(items):
    result = []
    for item in items:
        result.append(len(item))
    return result


lengths(a)
```

    [1, 2, 3, 4]

List comprehension.

``` python
def lengths(items):
    return [len(item) for item in items]


lengths(a)
```

    [1, 2, 3, 4]

Functional approach.

``` python
def lengths(items):
    return list(map(len, items))


lengths(a)
```

    [1, 2, 3, 4]

*Filtering* is the process of extracting items from an iterable which satisfy a certain condition. Filter all elements of even length from `a`.

Procedural approach.

``` python
def even_lengths(items):
    result = []
    for item in items:
        if len(item) % 2 == 0:
            result.append(item)
    return result


even_lengths(a)
```

    ['ab', 'abcd']

List comprehension.

``` python
def even_lengths(items):
    return [item for item in items if len(item) % 2 == 0]


even_lengths(a)
```

    ['ab', 'abcd']

Functional approach.

``` python
def even_lengths(items):
    return list(filter(lambda x: len(x) % 2 == 0, items))


even_lengths(a)
```

    ['ab', 'abcd']

## Sources

-   [Fluent Python](https://www.oreilly.com/library/view/fluent-python/9781491946237/)
-   [Python Cookbook](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/)
-   [Python Essential Reference](https://www.oreilly.com/library/view/python-essential-reference/9780768687040/)
-   [Learning Python](https://www.oreilly.com/library/view/learning-python-5th/9781449355722/)
-   [Stanford CS41](https://stanfordpython.com/#/)
