# Unix basics



This is my cheetsheet for all things Unix. I use it to keep track of useful things I learn and want to remember.

## Basics

-   A process is a running instance of a program.

-   Everything is a fiele (the keyboard is read-only, the screen write only)

-   `man <command>` opens the manual for `<command>`.

-   `man -k <search term>` lists all commands with `<search term>` in the manual
    pages.

## Stuff I use often and tend to forget

-   Creating a soft link: `ln -s <file> <link>`. If you use `.` for `<link>`, a
    link with the same name as `<file>` will be created in the current location.

-   Renaming multiple files: `rename 's/<pattern to replace>/<new pattern>'   [files]`. For example, to replace `foo` with `bar` in all Python files, use
    `rename 's/foo/bar/' *.py`. Notice that the string command passed is a vim
    substitution pattern.

-   Copying and pasting from and to the clipboard: `pbcopy` and `pbpaste` allow
    you to copy from and paste to the terminal. I often use `pwd | pbcopy` to get
    a directory path for use elsewhere, and `pbpaste > .gitignore` to create a
    gitignore file from a template (e.g. from gitignore.io).

-   Using the test utility: Use `[[ condition ]]` instead of `[ condition ]`.
    They are both test utilities, but the former is an extension of the latter
    that's supported in all shells I'd ever use (see
    [here](https://unix.stackexchange.com/a/306115)).

-   Moving current process to background: use `ctrl-z` to move current job to
    background, `jobs` to list running background jobs, and `fg <job id>` to move
    job to foreground.

## Bash scripting

-   `'` and `"`: single quotes are used to interpret all content literally, while
    double quotes allow for variable substitution. For example, `echo '$PATH'`
    will print `$PATH`, while `echo "$PATH"` will print the value of `$PATH`.

-   `$( command )`: saves command output into a variable. For example, `myvar=$(ls)` will save the output of `ls` into `myvar`.

-   `export var`: makes `var` available to child process. For example, `export PATH=$PATH:/usr/local/bin` will add `/usr/local/bin` to the `PATH` variable.

-   `let var=expr`: assigns result of expression to a variable. For example, `let var=5+5` will assign 10 to `var`.

-   `expr`: prints result of expression. For example, `expr 5 + 5` will print 10.

-   `$(( expression ))`: returns the result of expression. For example, `echo $(( 5 + 5 ))` will print 10.

-   Create a basic function in bash:

``` bash
function_name () {
  <commands>
}
```

## Permissions

-   Three actions: `r` (read), `w` (write), `x` (execute).

-   Three types of users: owner or user (u), group (g), and others (o). (a)
    applies to all types.

-   Permission info is 10 characters long: first character is file type (`-` for
    file, `d` for directory), the remaining ones are rwx permissions for owner,
    group, and others, with letter indicating permission on, hyphen indicating
    permission off.

-   Changing persmission: `chmod <user type><add or remove><permission type>`.
    User type defaults to a. Example: `chmod g+w` adds write permission for
    group, `chmod u-x` removes execute permission for owner, `chmod a+rwx` grants
    all permission to everyone. `chmod` stands for change file mode bits.

-   Shortcuts: Remember the following:

| Octal | Binary |
|-------|--------|
| 0     | 000    |
| 1     | 001    |
| 2     | 010    |
| 3     | 011    |
| 4     | 100    |
| 5     | 101    |
| 6     | 110    |
| 7     | 111    |

-   This is useful because we can use the binary numbers to refer to rwx and the
    Octal ones as shortcuts (e.g. 5 is r-x). Further using the order of users as
    ugo, and using one Octal shortcut for each user, we can quickly set
    permissions for all users (e.g. 753 is rwxr-x-wx).

-   Directory permissions: r means you can read content (e.g. do ls), w means you
    can write (e.g. create files or subdirectories), and x means you can enter
    (e.g. cd).

## Shebang

-   The shebang character sequence (`#!`) is used in the first line of a script to specify the interpreter that executes the commands in the script.

-   There are two options, well explained [here](https://www.baeldung.com/linux/bash-shebang-lines) (and also, a bit more elaborately, [here](https://en.wikipedia.org/wiki/Shebang_(Unix)): one is the specify the absoute path to the interpreter (`#!/bin/zsh`), the other is to use the `env` utility to search for the specified interpreter in all directories in the `$PATH` variable and use the first occurrence that is found (`#!/usr/bin/env zsh`).

-   The second option trades security for portability and is what most people seem to recommend. So this is what I use most of the time.

## Command-line utilities

### Getting help

#### `man`

-   Displays and formats the on-line manual pages.

-   Invoke by typing `man` followed by the name of the command you want to know more about.

#### `info`

-   Displays and formats the entire documentation of a command.

### Searching

#### `fzf`

-   A command-line fuzzy finder that filters the results from a given input based on additional user input.

-   For example, `ls | fzf` will display all files in the current directory and subdirectories, and then filter the results based on the user input.

-   By default, it searches for files from the current directories.

-   Advanced example uses [here](https://github.com/junegunn/fzf/wiki/examples).

-   I have created shortcuts that allow me to search and preview (with `bat`) all files in the current directory and subdirectories with `fp` ("file preview"), and do the same but then open the selected file with nvim with `fv` ("file vim").

#### `grep` and `rg`

-   Searches for a pattern in a file or files.

-   To find all markdown files in the current directory and subdirectories that contain the word "python":

``` bash
grep -r --inlcude="*.md" "python" .
```

-   `rg` is a faster alternative to `grep`.

#### `find` and `fd`

-   `find` is a command-line utility that searches for files in a directory hierarchy.

-   `fd` is a simple, fast and user-friendly alternative to `find`.

### File manipulation

#### `awk`

-   A programming language designed for text processing and typically used as a data extraction and reporting tool (it takes its name from the initials of its [three creators](https://en.wikipedia.org/wiki/AWK)).

-   It is a standard feature of most Unix-like operating systems, and particularly useful for processing text files.

-   It operates on a line-by-line basis and splits each line into fields.

-   For example, to print the first and second fields of each line of a file:

``` bash
awk '{print $1, $2}' file.txt
```

#### `sort`

-   Sorts lines of text files.

-   For example, to sort the lines of a file in reverse order:

``` bash
sort -r file.txt
```

#### `uniq`

-   Filters adjacent matching lines from input.

-   For example, to print only unique lines of a (sorted) file:

``` bash
uniq file.txt
```

#### `cat`

-   Concatenates files and prints on the standard output.

-   For example, to print the contents of a file:

``` bash
cat file.txt
```

#### `sed`

-   A stream editor for filtering and transforming text.

-   It reads text, line by line, from standard input and modifies it according to an expression, before outputting it again.

-   For example, to replace all occurrences of "foo" with "bar" in a file:

``` bash
sed -i 's/foo/bar/g' file.txt
```

-   To remove the first line of the input file:

``` bash
sed -i '1d' file.txt
```

### Process management

#### `ps`

-   `ps` stands for "process status" and, by default, shows all processes with controlling terminals.

### Miscellaneous

#### `eval`

-   Evaluates the arguments as a shell command.

-   For example, to run the command `ls -l`:

``` bash
eval ls -l
```

-   This is useful when you want to run a command that is stored in a variable:

``` bash
cmd="ls -l"
eval $cmd
```

#### `diff`

-   Compares files line by line.

#### `xargs`

-   A command-line utility that reads data from standard input and executes a command separately for each element in the input (by default, elements are separated by blanks).

-   For example, to create directories 'one', 'two', and 'three':

``` bash
echo "one two three" | xargs mkdir
```

-   Or, to delete all files in the current directory and subdirectories that contain the word "python":

``` bash
grep -r --inlcude="*.md" "python" . | xargs rm
```

## Custom scripts

-   To practice the use of the command-line utilities, I have created a few custom scripts that I use on a regular basis.

-   They are stored in my dotfiles [repo](https://github.com/fabiangunzinger/.dotfiles/tree/main/scripts/bin).

### Kill processes by name

-   Inspired by this [post](https://sidneyliebrand.io/blog/how-fzf-and-ripgrep-improved-my-workflow), I create a script to easily kill processes by name.

``` bash
#!/bin/zsh
# A simple script to kill a process by name. Use [tab] to select 
# multiple processes and press [enter] to kill them or [esc] to cancel.

local pid=$(ps -e | sed 1d | fzf -m --header='[kill:process]' | awk '{print $1}')

if [[ -n "$pid" ]]
then
  echo $pid | xargs kill
else
  echo "No process selected"
fi
```

-   The script saves all selected processes in the variable `pid` and then kills them.

-   `$( expression )` saves the output of the entire expression in the variable `pid`.

-   `ps -e` lists all processes (by default, only processes with controlling terminals are shown, so the `-e` flag is passed to show all processes).

-   `sed 1d` removes the first line of the output (which contains the column names).

-   `fzf -m --header='[kill:process]'` displays all processes in a fuzzy finder and allows the user to select multiple processes.

-   `awk '{print $1}'` prints the first column of the output (which contains the process ids).

-   The test condition evaluation utility `[[` is used to check if the variable `pid` is not empty. This is achieved using the `-n` flag, which returns true if length of the following string is non-zero (see `man test`).

-   `echo $pid | xargs kill` passes the selected process ids to the `kill` command one by one.

## Resources

-   [Ryan's bash-scripting tutorial](https://ryanstutorials.net/bash-scripting-tutorial/)

-   [Ryan's linux tutorial](https://ryanstutorials.net/bash-scripting-tutorial/)

