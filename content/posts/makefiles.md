---
title: "Makefiles"
subtitle: "Cheatsheet"
tags: [tools, cheatsheet]

date: 2021-08-23
featured: false
draft: false

reading_time: true
profile: false
commentable: true
summary: " "

---

- A makefile is a data base that tells the `make` utilit how to recompile a
  system. In the default use case, `$: make <filename>` checks whether `filename` is out of date and, if so, recompiles it. In the way I use makefiles, `$: make <rule>`
  executes a predefined rule to accomplish a certain task like cleaning a
  particular dataset.
  
- Rules consist of a target (the name of a file to be modified), prerequisites
  (other files on which the target depends on), and commands to be run in order
  to update the traget based on changes in the prerequisites.

- A rule tells `make` when a target is out of date and how to update it. A
  target is out of date if it doesn't exist or is older then one of its
  prerequisite files.

- `$: make` executes the first specified rule, `$: make <rule>` executes a
  particular rule.

- A normal prerequisite makes both an *order statement* and a *dependency statement*:
  the order statement ensures that all commands needed to produce the
  prerequisete are fully executed before any commands to produce the target,
  while the dependency statement ensures that the target is updated every time a
  prerequisite changes. Occasionally, we want a prerequisite to invoke the order without the
  dependency statement (i.e. target is not udpated when the prerequisite
  changes, but when target is being updated, then the prerequisite commandas are
  run first). We can do this by writing the rule as `target:
  normal-prerequisites | order-only-prerequisites`.

- `make` does its work in two phases: during the *read-in* phase, it reads the
  makefile and internalises variables and rules to construct a dependency graph
  of all targets and their prerequisies; during the *target-update* phase, it
  determines what rules to update in what order and executes the commandas to do
  so.

- As a result, variable and function expansion can happen either *immediately*
  (during the read-in phase) or *deferred* (after the read-in phase), and gives
  rise to two flavours of variables: *recursively expanded variables*, defined by
  `varname = value` are expanded at the time the variable is substituted during
  the target-update phase. Before that point, `varname` contains the content of
  `value` verbatim (e.g. if `value` is `$(othervar)`, then that last string is
  the value of `varname`). In contrast, *simply expanded variables*, defined by
  `varname := value` is expanded immediately when the variable is defined during
  the read-in phase (and `varname` would be bound to the value of `othervar` in
  the above example).

- To define a variable containing all csv files in a directory, do `csvs :=
  $(wildcard *.csv)`. The `wildcard` function is needed here so that the
  wildcard gets expanded during function creation (as opposed to creating the
  variable with value `*.csv`). I could also create a list
  containing the same files but with a parquet extensions like so: `parqs :=
  $(patsubst %.csv,%.parquet,$(wildcard *.csv)). 

- Automatic variables: `$^` is a list of all prerequisites, `$@` is the target,
  `$<` the first prerequisite.

- If a target is an action to be performed rather than a file to be updated,
  then it's called a `phony target`. In this case, telling `make` that we're
  using a phone target explicitly by prepending the rule with a line like
  `.PHONY : nameofrule` is useful for two reasons: `make` doesn't think of a
  file called `nameofrule` as the target (which, if it did, would mean that our
  rule never gets run because it has no prerequisites so that `make` would think
  of `nameofrule` as always up to date) and it doesn't check for implicit
  commands to update the target, which improves performance.

- Commands begin with a tab and, unless specified otherwise, are executed by
  `bin/sh`. You can set a different shell by changing the value of the `SHELL`
  variable (I usually use `SHELL := /bin/bash`. Each line that begines with a tab and appears within a rule context
  (anything between the start of one rule and another) is interpreted as a
  command and sent to the shell.

- The only thing `make` does with commands is to check for `\` before newline,
  and for variables to expand (if you want `$` to appear in the command, use
  `$$`). To prevent `make` from echoing a command, prepend it with `@`.

- Prepend a command with `-` if you want `make` to continue regardless of
  errors. This can be useful for commands like `-rm tempfile.csv`, where you
  probaby want to continue even if the file didn't exist and could thus not be
  removed.


## Best practices

Define a phony target:

```
.PHONY: clean
clean:
    rm *.csv
```

Make `$: make` run all rules:

```
.PHONY: all
all : rule1 rule2

.PHONY: rule1
rule1:
    mkdir hello

.PHONY: rule2
rule2:
    rm -rf hello
```


