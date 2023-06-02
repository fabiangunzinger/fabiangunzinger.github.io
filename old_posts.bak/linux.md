---
title: "Linux"
subtitle: "Cheetsheet"
tags: [tools, cheatsheet]

date: 2020-11-21
featured: false
draft: false

reading_time: true
profile: false
commentable: true
summary: " "

---

## Getting help and finding stuff

- `man <command>` opens the manual for `<command>`.
- `man -k <search term>` lists all commands with `<search term>` in the manual
    pages.
- Search inside manual works as in vim.


## Basics

- A process is a running instance of a program.
- Everything is a fiele (the keyboard is read-only, the screen write only) 


## Misc. useful stuff I use often

- `ln -s [OPTIONS] FILE LINK`. Create a soft link for FILE at LINK. If you use
  `.` for LINK, a link with the same name as FILE will be created in the current
  location.

- In mac terminal, `pbcopy` and `pbpaste` allow you to copy from and paste to
  the terminal. I often use `pwd | pbcopy` to get a directory path for use
  elsewhere, and `pbpaste > .gitignore` to create a gitignore file from a
  template (e.g. from gitignore.io).

- Renaming multiple files: `rename 's/<pattern to replace>/<new pattern>' [files]`. For example, to replace `foo` with `bar` in all Python files, use `rename 's/foo/bar/' *.py`. Notice that the string command passed is a vim substitution pattern.

- Use `[[ condition ]]` instead of `[ condition ]`. The former is an extension of the latter that's supported in all shells I'd ever use (see [here](https://unix.stackexchange.com/a/306115)).


## File handling

- `file` lists file type of all files in a directory.
- `wc` returns the number of words, lines, and bytes of the input file. Options
    -w, -l, -c return any one of those counts, -m returns the number of
    characters. (Remember difference between `wc -w <filename>` and `wc -w < <filename>`: former prints file name, latter redirects file content to
    command anonymously, so prints result only.)
- `cut` print certain columns of input file.
- `sed` (stream edit) offers vim-like search and replace on data.
- `uniq` removes duplicates from data.
- `egrep` for regex-based filtering.


## Processes

- `top` to list most memory-intensive processes.
- `ps` lists processes running in current terminal, use -aux option to print all
    running processes (use | grep to filter output).
- `kill [signal] <process id>` to kill a process, use -9 signal to force if
    required.
- `ctrl-z` to move current job to background, `jobs` to list running background
    jobs, `fg <job id>` to move job to foreground.


## Bash scripting

Variables
- `'` interpret all content literally, `"` allow for variable substitution.
- `$( command )` saves command output into a variable.
- `export var` makes `var` available to child process.
- `/dev/stdin` reads input from pipe.

Arithmetic
- `let` assigns result of expression to a variable.
- `expr` prints result of expression.
- `$(( expression ))` returns the result of expression.
- `${#var}` returns the length of `var` in characters.

Functions
- `function_name () {
     <commands>
   }` 
   is the basic format (there is also `function function_name {`, but I prefer this.




## Permissions

- Three actions: `r` (read), `w` (write), `x` (execute).
- Three types of users: owner or user (u), group (g), and others (o). (a)
  applies to all types.
- Permission info is 10 characters long: first character is file type (`-` for
  file, `d` for directory), the remaining ones are rwx permissions for owner,
  group, and others, with letter indicating permission on, hyphen indicating
  permission off. 
- Changing persmission: `chmod <user type><add or remove><permission type>`.
  User type defaults to a.  Example: `chmod g+w` adds write permission for
  group, `chmod u-x` removes execute permission for owner, `chmod a+rwx` grants
  all permission to everyone.  `chmod` stands for change file mode bits.
- Shortcuts: Remember the following:

 Octal    | Binary 
 -------- | -------- 
        0 |      000 
        1 |      001 
        2 |      010 
        3 |      011 
        4 |      100 
        5 |      101 
        6 |      110 
        7 |      111 

- This is useful because we can use the binary numbers to refer to rwx and the
  Octal ones as shortcuts (e.g. 5 is r-x). Further using the order of users as
  ugo, and using one Octal shortcut for each user, we can quickly set
  permissions for all users (e.g. 753 is rwxr-x-wx).

- Directory permissions: r means you can read content (e.g. do ls), w means you
  can write (e.g. create files or subdirectories), and x means you can enter
  (e.g. cd).

## Shebang

- The shebang character sequence (`#!`) is used in the first line of a script to specify the interpreter that executes the commands in the script.

- There are two options, well explained [here](https://www.baeldung.com/linux/bash-shebang-lines) (and also, a bit more elaborately, [here](https://en.wikipedia.org/wiki/Shebang_(Unix)): one is the specify the absoute path to the interpreter (`#!/bin/zsh`), the other is to use the `env` utility to search for the specified interpreter in all directories in the `$PATH` variable and use the first occurrence that is found (`#!/usr/bin/env zsh`).

- The second option trades security for portability and is what most people seem to recommend. So this is what I use. 

## Sources

- [Ryan's bash-scripting tutorial](https://ryanstutorials.net/bash-scripting-tutorial/)
- [Ryan's linux tutorial](https://ryanstutorials.net/bash-scripting-tutorial/)

