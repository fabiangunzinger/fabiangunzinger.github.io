---
title: "Vim cheatsheet"
category:
    - craft
tag:
    - tools 
    - cheatsheet
date: 2021-09-11
draft: false
---

## Preliminaries

- I use [neovim](https://neovim.io). My configuration is
  [here](https://github.com/fabiangunzinger/dotfiles/blob/main/init.vim).
  There, I map `<esc>` to `jk`, a mapping I also use throughout this
  file.

- I've remaped Caps Look to `<ctrl>` on my mac.

## Quarto setup 

- `<shift-k>` to open help on object under cursor, `<shift-kk>` to ender help window, `q` to quit help.

- Terminal: open new terminal with `<leader>c`, then activate terminal by going into insert mode and going back to normal mode with usual keybinding.


## Reminders

- git-gutter: `]h` and `[h` to jump to next and previous hunk, `<leader>hs` and
  `<leader>hu` to stage and unstage hunk.
- Vim takes an additional command on startup (e.g. `nvim +CommandT`).

- Use one keystroke to move and one to execute (e.g. the dot-formula).

- Exit and re-enter insert mode strategically to chunk your undos (all changes
  in a single insert session count as one change).

- If you hit cursor keys more than 2 or 3 times, press backspace more than a
  couple times, perform the same change on several lines, there is a better
  way.

- I want to open a file and get an *E325: ATTENTION Found a swap file* warning.
  What happened? For me, it's most likely that I accidentally closed a terminal
  window while still editing the file. What to do? First, check that I'm not
  already editing the file elsewhere. Second, recover the file, save it under a
  new name (`:w filename2`), force quit the session, compare the original and
  the new file (`diff filename filename2`), use the file with the content I
  need and delete the other one and the swap file. (Based on
  [this](https://superuser.com/a/498658) great SE answer.)

- Don't solve a problem unless you come across it frequently (and if you do,
  check whether one of Tim Pope's plugins solves it).

Useful stuff I tend to forget:

| Command             | Effect |
| ------------------- | ------ |
| `<C-f>`/`<C-b>`     | Scroll down/up screen-wise ("forwards-backwards") |
| `c-x c-e`           | In command line: edit current line in vim, run after quit |
| `:x`                | Like `:wq` but only write if file was changed |
| `set: {option}?`    | Show present setting for {option} |
| `set: {option}&`    | Set option back to default value |
| `\|`                | Command separator (equivalent to `;` in shell) |
| `<c-k>-N`           | Enter en dash in insert mode using digraphs |
| `<c-o-o>`           | After opening vim, opens last file with cursor at last edit |
| `:scriptnames`      | List of scripts loaded on startup |
| `:map`, `:nmap`, ...| Show existing mappings |
| `<c-o>` / `<c-i>`   | To move back and forth in the jumplist |


## Help

| Command             | Effect |
| ------------------- | ------ |
| `gO`                | Show table of contents for current help file |
| `:helpc[lose]`      | Close help windows if any are open |
| `:vert h {keyword}` | Open help in a vertical split |


## Modes

### Normal mode

- Operators work as follows: operator + [count] + motion = action. E.g. `d2l`
  deletes two character to the right, `diw` the word under the cursor (without
  the surrounding whitespace), `dap` the current paragraph (including the
  surrounding whitespace). Similarly, `gUap` converts the current paragraph to
  uppercase.

Common operators:

| Trigger    | Effect |
| ---------- | ------ |
| `c`        | Change |
| `d`        | Delete into register |
| `d`        | Delete into register |
| `y`        | Yank into register |
| `p`        | Paste after cursor |
| `P`        | Paste before cursor |
| `~`        | Swap case of character under cursor and move right |
| `gu`       | Make lowercase |
| `gU`       | Make uppercase |
| `g~`       | Swap case |
| `>`        | Shift right |
| `<`        | Shift left |
| `=`        | Autoindent |
| `!`        | Filter {motion} lines through an external program |

Moving back and forth:

| Forwards      | Backwards   | Effect |
| - | - | - |
| `/`           | `?`         | Seach for pattern |
| `*`           | `#`         | Search for word under cursor |
| `n`           | `N`         | Jump to next search match |
| `$`           | `^`         | Jump to end of line |
| `f{char}`     | `F{char}`   | Position cursor on character |
| `t{char}`     | `T{char}`   | Position cursor before character |
| `;`           | `,`         | Repeat the last r, F, t, or T |
| `w`           | `b`         | Move to the start of the next word |
| `W`           | `B`         | Move to the start of the next WORD |
| `}`           | `{`         | Move down one (blank-line-separated) paragraph|
| `gg`          |             | Jump to the first line of the document |
| `G`           |             | Jump to the last line of the document |


Act, repeat, reverse:

| Intent                            | Act                 | Repeat      | Reverse |
| - | - | - | - |
| Make a change                     | `{edit}`            | `.`         | `u` |
| Scan line for next character      | `f{char}/t{char}`   | `;`         | `,` |
| Scan line for previous character  | `F{char}/T{char}`   | `;`         | `,` |
| Scan document for next match      | `/pattern<CR>`      | `n`         | `N` |
| Scan document for previous match  | `?pattern<CR>`      | `n`         | `N` |
| Perform substitution              | `:s/old/new`        | `&`         | `u` |
| Execute a sequence of changes     | `qx{change}q`       | `@x`        | `u` |

Compound commands:

| Compound command    | Equivalent in longhand |
| - | - |
| `C`                 | `c$` (delete from cursor until end of line and start insert) |
| `D`                 | `d$` (delete from cursor until end of line) |
| `Y`                 | `y$` (similar to above, but has to be mapped, see `h: Y`) |
| `s`                 | `cl` (delete single character and start insert) |
| `S`                 | `^c` (delete entire line and start inster, synonym for `cc`) |
| `x`                 | `dl` (delete one character to the right) |
| `X`                 | `dh` (delete one character to the left) |
| `I`                 | `^i` (jump to beginning of line and start insert) |
| `A`                 | `$a` (jumpt to end of line and start insert) |
| `o`                 | `A<cr>` |
| `O`                 | `ko` |

Miscellaneous:

| Command           | Effect |
| - | - |
| `<C-a>`/ `<C-x>`  | Add / subtract from the next number |
| `<C-o>`/ `<C-i>`  | Move backwards to last / forward to previous location |
| `u`/`<C-r>`       | Undo / redo change |
| `ga`              | Reveal numeric representation of character under cursor |
| `gx`              | Open url under cursor |
`<C-z>`/`fg`        | Put vim in background / return to vim


### Insert mode

Entering insert mode:

| Trigger | Effect |
| - | - |
| `i`       | Insert before cursor |
| `a`       | Insert after cursor |
| `I`       | Insert at beginning of current line |
| `A`       | Insert at end of current line |
| `o`       | Insert in a new line below the current one |
| `O`       | Insert in a new line above the current one |
| `gi`      | Insert at the end of last insert |

Useful commands:

| Keystroke            | action |
| - | - |
| `<c-h>`              | delete back one character (backspace) |
| `<c-w>`              | delete back one word |
| `<c-u>`              | delete back one line |
| `<c-o>`              | Enter insert normal mode to execute a single normal cmd |
| `<C-r>{register}`    | Paste content from address (use 0 for last yanked text) |
| `<C-r>=`             | Perform calculation in place |
| `r`, `R`             | Enter replace mode for single replacement or until exit |
| `<C-v>{123}`         | Insert character by decimal code  |
| `<C-v>u{1234}`       | Insert character by hexadecimal code  |
| `<C-v>{char1}{char2}`| Insert character by digraph |


### Visual mode

- Once in visual mode, you can use any normal mode movement command to specify
  the area to be selected. Reminder to myself: use search more often for this.

| Command    | Effect |
| - | - |
| `v`        | Enter character-wise visual mode / back to normal mode |
| `V`        | Enter line-wise visual mode / back to normal mode |
| `<C-v>`    | Enter block-wise visual mode / back to normal mode |
| `gv`       | Reselect last visual selection |
| `o`        | Toggle the free end of a selection |

Exercises:

1. Turn the list of objects into dictionary elements as shown.

foo
bar
baz
buzz

d[0] = "foo"
d[1] = "bar"
d[2] = "baz"
d[3] = "buzz"


Solutions:

1. `yip` to select paragraph, `:s/\(.*\)/d[0] = "\1"` to replace each line with dict entry, then move to 0 in last paragraph, then `<c-v>g<c-a>` to activate block visual mode, and increment the lines.


### Command-line mode

- Ex-commands allow you to make changes (in multiple places) anywhere in
  the file without moving the cursor -- "they strike far and wide".

- The general syntax is `:[range]{command}`, where `[range]` is
  either a single address or a range of addresses of the form `{start},{stop}`.
  There are three types of addresses: line numbers, visual selections, and
  patterns.

- To execute a command on all selected lines, use visual mode to make the
  selection and press `:`. This will start the command prompt with `'<, '>:`,
  to which you can then add the command.

- You can also specify offsets. For example, `:/<tag>/+1<\/tag>/-1{cmd}` would
  operate on the lines inside the html tag but not the lines containing the tag
  marks.

Command mode commands:

| Command                     | Effect |
| - | - |
| `:`, `/`, `?`               | Opens command line / search /reverse search mode |
| `<C-r><C-w>`                | Insert word under cursor in command prompt  |
| `<left>`/`<right>`          | Move one character left or right |
| `<S-left>`                  | Move one word left (similar for right) |
| `<C-b>`/`<C-e>`             | Move to the beginning/end of the command |
| `<C-w>`                     | Delete last word |
| `<C-u>`                     | Delete from cursor to beginning of line |

Types of addresses:

| Command                     | Effect |
| - | - |
| `:4{cmd}`                   | execute command on line 4 |
| `:4,8{cmd}`                 | execute command on lines 4 to 8 (inclusive) |
| `:/#/{cmd}`                 | execute command on next line with an `#` |
| `:/<tag>/<\/tag>/{cmd}`     | Execute command on next occurring html tag |
| `:'<,'>{cmd}`               | Execute command on selected lines |

Useful address/range characters:

| Symobol | Address |
| - | - |
| `1`       | First line of the file |
| `$`       | Last line of the file |
| `0`       | Virtual line above first line (e.g. to paste to top of file) |
| `.`       | Line of cursor |
| `'m`      | Line containing mark m |
| `'<`      | Start of visual selection |
| `'>`      | End of visual selection |
| `%`       | The entire file (short for `:1,$`) |

Common Ex-commands: 

| Command             | Effect |
| - | - |
| `p[rint]`           | Print |
| `d[elete]`          | Delete |
| `j[oin]`            | Join lines |
| `s[ubstitute]`      | Substitute (e.g. `s/old/new`) |
| `n[ormal]`          | Execute normal mode command |
| `m[ove]`            | Move to `{address}`, (e.g. `:1,5m$` moves lines to end of file) |
| `co[py]` (or `t)`   | Copy to `{address}`, (e.g. `:6t.` copies line 6 to current line) |

Exercises:

1. Wrap all elements in the first column of a table in quotes. 

2. Replace the word under the cursor throughout the file.

3. Open help for word under the cursor.

Solutions:

1. With cursor on word in first row: `:{start},{stop}normal ysaW'`.

2. `*`,`cw{change}jk`, `:%s//<C-r><C-w>/<options>`.

3. `:h <C-r><C-w><CR>`.


## Quickfix List

- The quickfix list is a special mode to speed up the edit-compile-edit cycle.
  But it can be used more generally to find a list of positions in files (e.g.
  list could hold search matches from running `:vimgrep`).

- The Location list is a local version of the quickfix list that is bound to the
  currently active window. There can be as many local lists as there are
  windows, while there is only a single globally available quickfix list.

| Command             | Effect |
| - | - |
| `:make [target]`    | Compile target (and jump to first error if there are some) |
| `:make! [target]`   | Compile target without jumping to first error |
| `:copen`            | Open quickfix window |
| `:cclose`           | Close quickfix window |
| `]q` / `[q`         | Jump to next/previous match (uses vim-unimpaired plugin) |


## Files

Setting the working directory:

| Command             | Effect |
| - | - |
| `:pwd`              | Show current directory window |
| `:cd`               | Set directory for all windows |
| `:cd -`             | Revert back to previous directory |
| `:lcd`              | Set directory for current window |
| `:tcd`              | Set directory for current tab |


### Buffers

- A buffer is an in-memory representation of a file.

- A hidden buffer is one that contains changes you haven't written to disk
  yet but switched away from. For a session with hidden buffers, quitting will
  raise error messages, and vim will automatically display the first hidden
  buffer. You now have the following options: `:w[rite]` to write the buffer's
  content to disk, `:e[dit]!` to reread the file from disk and thus revert all
  changes made, `:qa[ll]!` to discard all changes, and `:wa[ll]` to write all
  modified buffers to disk.

- `:bufdo` executes an Ex command in all open buffers, `:argo` in all grouped
  ones (e.g. `:argdo %s/hello/world/g` substitutes `world` for `hello` in all
  buffers in `:args`, `:argdo edit!` reverts all changes, and `:argdo update`
  writes changed buffers to disk.

- `:[range]bd` deletes buffers in range, with `[range]` working as for other
  Ex-commands (see above).

| Command             | Effect |
| - | - |
| `:x[it]` / `exi[t]` | Like `:wq` but only write if file was changed |
| `:xa`               | Write all changed buffers and exit (like `:wqa`) |

[vim-eunuch](https://github.com/tpope/vim-eunuch) commands:

| Command             | Effect |
| - | - |
| `Move[!] {file}`    | Like `:saveas`, but deletes old file |
| `Rename[!] {file}`  | Rename current buffer and file |
| `Chmod {mode}`	    | Change permissions of current file |
| `Mkdir {dir}`	    | Create dir with `mkdir()` |
| `Mkdir! {dir}`	    | Create dir with `mkdir()` with "p" argument (mkdir -p) |

Toggle buffer settings from vim-unimpaired:

| Command                 | Effect |
| - | - |
| `yoh`                   | Toggle search highlighting |
| `yob`                   | Toggle light background |
| `yoc`                   | Toggle cursor line highlighting |
| `yon`                   | Toggle line numbers |
| `yor`                   | Toggle relative line numbers |
| `yos`                   | Toggle the spell checker |


### Windows 

- A window is a viewport onto a buffer.

- We can open different windows that all provide a (different) view onto the
  same buffer, or load multiple buffers into one window.

| Command             | Effect |
| - | - |
| `<C-w>w`            | Go to next window |
| `<C-w>s`            | Split window horizontally |
| `<C-w>v`            | Split window vertically |
| `:sp[lit] {file}`   | Horizontally split window and load {file} into new buffer |
| `:vsp[lit] {file}`  | Vertically split window and load {file} into new buffer
| | |
| `:new`              | Split horizontally with new file |
| `:vne[w]`           | Split vertically with new file |
| `on[ly]`            | Close all but current window |
| `<C-w>=`            | Equalize width and height of all windows |
| `<C-w>r`            | Rorate windows |
| `<C-w>x`            | Exchange position of current window with its neighbour
| | |
| `q[uit]`            | Close current window |
| `:sb[uffer]`        | Open buffer number N in horizontal split
| `:vert sb N`        | Open buffer number N in vertical split (`<leader>vb`)


### Tabs

- A tab is a container of windows.

| Command             | Effect |
| - | - |
| `:tabe[dit]{file}`  | Open new tab with {file} if specified or empty otherwise |
| `:[count]tabnew`    | Open a new tab in an empty window. |
| `<C-w>T`            | Move current window into new tab |
| `:tabc[lose]`       | Close current tab with all its windows |
| `:tabo[nly]`        | Close all tabs but the current one |
| `{N}`gt             | Go to tab {N} if specified, or to next otherwise |
| `gT`                | Go to previous tab |

Handy [count] options for `tabnew`:

| Count  | Opens new tab ... |
| - | - |
| `[.]`  | ... after current one |
| `-`    | ... before current one |
| `0`    | ... before first one |
| `$`    | ... after last one |


### Opening files

- I use `command-t` to fuzzy-find files, which is what I use most of the time
  when working inside a project.

- To navigate file trees, I use `netrw` and `vinegar`.

- Deleting folders: `netrw` uses `delete()` with the `d` flat to delete
  directories. As explained in `:h delete()`, this only removes empty
  directories. I leave this default for now.

- To easily open a new file from the same directory as the current buffer in a
  new window/split/vertical split/tab I use the mappings `<leader>ew/es/ev/et`,
  following [this](http://vimcasts.org/episodes/the-edit-command/) Vimcast.

command-t commands:

| Command                     | Effect |
| - | - |
| `<c-o>`                     | Open or close command-t |
| `<c-i>`                     | Open command-t for open buffers |
| `<c-f>`                     | Flush path cash and rescan directory |
| `<c-v>`                     | Open file in vertical split |

`netrw` commands:

| Command             | Effect |
| - | - |
| `e[dit].`           | Open file explorer for current working directory |
| `E[xplore]`         | Open file explorer for the directory of active buffer |
| `%`                 | Open new file in current directory |
| `d`                 | Create new directory in current one |
| `R`                 | Rename file or directory under cursor |
| `D`                 | Delete file or directory under cursor |
| `gh`                | Toggle hiding dot-files |
| `:Ve`               | Open explorer in vertical split |
| `:Rex`              | Exit/return to explorer |
| `<c-l>`             | Refresh listing |


## Navigation

- Motions move within a file, jumps between files.

- Each motion can be prepended by a count (`5l` moves five characters to the
  right).


### Within files

General:

| Command             | Effect |
| - | - |
| `<C-g>`             | Shows current filepath and line number |
| `zz`                | Redraw current line in middle of window |
| `zt`                | Redraw current line at top of window |

Left-right and up-down:

- You can use search after an operator to great effect. For instance: typing
  `d/to <CR>` when the cursor is at the beginning of "after" in the previous
  sentence turns it into "You can use search to greate effect". This works
  because `d` is an exclusive operator (`h: exclusive`) and doesn't apply the
  operation on the endpoint of the selection.

- I use `vim-smoothie` for smoother screening behaviour of half-screen and
  screen-wise scrolling.

| Command             | Effect |
| - | - |
| `h`/`l`             | Move left/right (use `[count]` as needed) |
| `j`/`k`             | Down/up one line (think of `j` as a down arrow, use `[count]` as needed) |
| `gj`/`gk`           | Down/up by display rather than real lines |
| `0`/`^`/`$`         | To first non-blank/first/last character of line |
| `G`                 | Goto line `[count]`, default is last line |
| `gg`                | Goto line `[count]`, default is first line |
| `f{char}`/`F{char}` | To next occurrence of {char} to the right/left |
| `t{char}`/`T{char}` | Till (before) next occurrence of {char} to the right/left |
| `H`/`M`/`L`         | Jump to the top/middle/bottom of the screen |
| `<C-e>`/`<C-y>`     | Scroll down/up linewise |
| `<C-d>`/`<C-u>`     | Scroll down/up half-screen-wise ("down-up") |
| `<C-f>`/`<C-b>`     | Scroll down/up screen-wise ("forwards-backwards") |

Words:

| Command             | Effect |
| - | - |
| `w`/`e`             | Forward to start/end of current or next word |
| `b`/`ge`            | Backward to start/end of current or previous word |
| `W`, `E`, `B`       | Move WORD rather than word wise |

Text objects:

- Text objects come in two types: those within a pair of delimiters (e.g. text
  inside parentheses) and chucks of text (Vim calls them "block" and
  "non-block" objects).

- They can be moved over or selected.

- Text object selection start with `i` ("inner sentence") or `a` ("a
  sentence").  For example: `vi)` highlights text inside parentheses but not
  the parentheses themselves, while `va)` highlights the parentheses as well.

- Useful tip: when I'm not inside a block object, nvim selects applies the command to the next one.

| Command             | Effect |
| - | - |
| `)`/`(`             | Move [count] sentences forward/backward |
| `}`/`{`             | Move [count] paragraphs forward/backward |

| Command             | Select inside or around... |
| - | - |
| `w`/`W`             | word/WORD |
| `s`                 | sentence |
| `p`                 | paragraph |
| `]`                 | a `[]` block |
| `)` or `b`          | a `()` block |
| `}` or `B`          | a `{}` block |
| `<`                 | a `<>` block |
| `t`                 | a tag block |

Marks:

| Command             | Effect |
| - | - |
| `m{a-zA-Z}`         | Set lowercase (local) or uppercase (global) mark |
| `` `{mark} ``       | Jump to mark |
| double-backquote    | Go to position before last jump |
| `` `. ``            | Go to position of last change |
| `%`                 | Go to matching bracket |


### Between files

- A jump is a long-range motion (which, roughly, means moving faster than
  WORD-wise).

Traversing the jumps and changes lists

| Command             | Effect |
| - | - |
| `:jumps`            | Show the jump list |
| `<C-o>`/`<C-i>`     | Traverse jump history backwards/forwards |
| `:changes`          | Show the change list |
| `g;`/`g,`           | Traverse change list backwards/forwards |
| `gf`                | Jump to file under cursor |
| `<C-]>`             | Jump to definition of keyword under cursor |


### Back and forth

- Vim-unimpaired provides a set of normal mode commands to move between **next**
  (`]`) and **previous** (`[`), toggle **options**, and special **pasting**.
  Some commands I use often are listed below. The mnemonic is that `]` is next
  in general and "next line" here, and lowercase navigates one by one while
  lowercase jumpts to first or last (e.g.  `[b` moves to previous buffer, `[B`
  jumps to first one).

| Command                 | Effect |
| - | - |
| `]<space>`/`[<space>`   | Add [count] blank lines below/above the cursor |
| `]e`/`[e`               | Exchanges the current line with the one below/above |


## Registers

### Copy and paste

- A register is a container that holds text. By default, Vim deletes, yanks and
  puts to and from the `unnamed` register `"`. We can set the register with
  which a command interacts by prepending the command with `"{register}{cmd}`
  (e.g. to explicitly state that we want to delete the current line to the
  unnamed register, we'd use `""dd`; to put the just copied text, `""p`. But
  these are equivalent to `dd` and `p`, so we'd probably not do that.) However,
  the default register will always contains the content from the last command,
  even if an additional register was specified.

- Transposing characters and lines: to correct "Thi sis", starting from the last
  letter, use `F<space>xp`; to swap the current with the subsequent line, use
  `ddp`. As an alternative to `ddp`, which is useful to move lines up and down
  more flexibly, use `]e` from `vim-unimpaired` (see below).

- Expression register: when we fetch the content of the expression register, Vim
  drops into command-line mode with a `=` prompt. When we enter Vim script and
  press `<CR>`, Vim will coerce the result into a string if possible and use it.

| Command             | Effect |
| - | - |
| `"{reg}{cmd}`       | Make {cmd} interact with register {reg} |
| `""`                | The unnamed register (redundant, as it's the default) |
| `"0`                | The yank register |
| `"_`                | The black hole register (nothing returns from it) |
| `"{a-z}`            | Named registers (replace with {a-z}, append with {A-Z})
| | |
| `"+`                | The system clipboard |
| `"%`                | Name of current file (e.g. `"%p`) |
| `"#`                | Name of alternate file |
| `".`                | Last inserted text |
| `":`                | Last Ex command |
| `"/`                | Last search pattern |
| `:reg[ister] [reg]` | List content of registers *reg*, all by default |
| `<C-r>{reg}`        | Paste content of {reg} in insert mode

Useful patterns:

- Replace firstword with secondword. Solution 1: cursor at beginning of
  secondword; `ye`; `bb`; `ve`; `p`. Solution 2: cursor at beginning of
  secondword; `ye`; `bb`; `cw`; `<C-r>0`. Has advantage that `.` now replaces
  current word with `firstword`. 

- Swap firstword and secondword. Solution: cursor at beginning of firstword;
  `de`; `mm`; `ww`; `ve`; `p`; `` `m ``; `P`. Explanation: this exploits a quirk
  in the behaviour or `p` in visual mode. When we paste in visual mode, we put
  the content of the default register in place of the highlighted text, and the
  highlighted text into the default register.

- Complete the statement 27 * 45 = x. Solution: cursor at x and in insert
  mode; `<C-r>=27*45<CR>`.


### Macros

- Macros can be executed *in sequence* (e.g. `22@a`) or *in parallel*
  (`[range]:normal @a`). The former can be useful as it aborts on failure,
  which could be what we want (e.g. replace all search results and stop once
  none are left). But if it's not, then the latter approach is more useful
  (e.g. if you want to perform a change on all list items but not on other
  lines).

| Command             | Effect |
| - | - |
| `q{a-z}`            | Start recording macro to register |
| `q`                 | End recording |
| `[count]@{a-z}`     | Invoke macro in register [count] times |
| `@@`                | Replay last invoked macro |
| `q{A-Z}`            | Append to macro (e.g. if I forgot something) |

Exercises:

1. In the below block of code, prepend *var * and append *;* to each line.
```
foo = 1  
bar = 2  
baz = 3
```

2. Edit macro `q` by prepending it with a `^` using a) yanking and b) visual
   editing (based on
   [this](https://thoughtbot.com/blog/how-to-edit-an-existing-vim-macro) useful
   post).

3. Macro `q` hits its target with `n`; invoke it quickly for all 12 search
   results in the document.

4. In the list below, change `.` to `)` and words to title case.
```
a. ho  
b. hi  
c. he
```

5. Make the reverse changes in the list below
```
a) Ho  
b) Hi  
// a comment  
c) He
```

6. Turn the below lines into a numbered list.
```
- first
- second
- third
```

7. Turn the below list into a numbered list.
```
- This is the first bullet - stretching over multiple lines. Well, actually, it didn't, but now it does.
- The second bullet is long, too. Again, it wasn't really, but now it is, so we can actually simulate what would happen.
- The third one is short.
- The fourth and final one is long.
```

Solutions:

1. With the cursor anywhere on the first line, start recording and perform the
   change on the first line, then either repeat it (a) sequentially or (b) in
   parallel. `qq`, `Ivar<esc>A;<esc>j`, (a) `2@q`, (b) `Vj:normal@q`.

2. a) Paste the macro content into the buffer and edit it:  `"qpI^<esc>`, yank
   it back into the q register: `"qyy`, clean macro from the buffer `dd`. b)
   Redefine the macro content directly using `let` command by opening the
   register `:let @q='`, pasting the current contents `<c-r><c-r>q`, adding `^`
   at the beginning, and adding `'` and press enter to close the quote and
   finish editing the macro.

3. `22@q`. Explanation: Because `q` uses `n` to hit its targets, it will
   automatically abort once there are no more results. We can thus avoid
   counting matches and simply use a number that's comfortably above the number
   of matches. 22 is convenient because, on my keyboard, it's the same key as
   @.

4. Start with cursor anywhere on first line of list, record macro:
   `qq0f.r)w~jq`, replay macro: `22@q`.

5. Start with cursor anywhere on first line of list, record macro:
   `qq0f.r)w~q`, replay macro: `V}:normal @q`. Discussion: Executing the macro
   in series as in the previous exercise would abort at the line of the
   comment, so we need to execute it in parallel. As a result, there is no need
   to move to next line after performing the changes. 

6. Start anywhere on the first line, then instantiate the counter: `:let i=1`,
   record the changes: `qq0s<C-r>=i<CR>)<Esc>`, advance the counter: `let
   i+=1`, stop recording: `q` and replay: `jVj:normal @q`.

7. My best solution thus far: We need a few preparation steps before we can
   execute the macro; first, select and then deselect the area within which you
   want to replace list item markers (e.g. `vap`, `jk`). Second, search for all
   list item markers inside that area using `/\%V\_^-`, where the `\%V` atom
   restricts the search to the previous selection, the `\_^` atom matches
   start-of-line, and `-` matches the hyphens used as list item markers.
   Finally, initialise the counter using `:let i=1`. To record the marco, move
   the curser to before the first hypen in the list, then record the motions to
   the `q` register `qq`, move to the first hypehn and replace it while
   entering insert mode `ncw`, replace it with the counter and add a dot and
   exit insert mode `<c-r>=i<cr>.jk`, and increment the counter and stop the
   recording `:let i=i+1q`. Now, you can simply replay the recording in
   sequence `22@q` and, if needed, reformat the area `gvgq`. (I use 22 to
   replay the macro for convenience as on my keyboard, 2 is the same key as the
   `@` symbol, but any number at least as large as the number of remaining
   hyphens to be replaced would do).


## Patterns

### Matching patterns and literals

- In my `.vimrc`, I use `set: ignorecase` and `set: smartcase` to set the
  default search to be case insensitive except when I use an uppercase character
  in my pattern.

- You can use pattern swtiches anywhere in the search pattern. 

- Use `\v` for regex search, `\V` for verbatim search.

| Command             | Effect |
| - | - |
| `\c`                | Force case insensitive search |
| `\C`                | Force case sensitive search |
| `\v` (very magic)   | All characters assume special meaning (regex-like search) |
| `\V` (very nomagic) | No character but "\" has special meaning (verbatim search) |
| `()`                | Capture matched pattern inside and store in numbered silo |
| `%`                 | When before `()`, don't capture submatch |
| `<`/`>`             | Word boundaries when used with `\v` switch |
| `\zs`/`\ze`         | Start and end of match |

Useful patterns:

- Find `the` but not words it is a part of (e.g. `these`). Solution:
  `/\v<the><CR>`.

- In a CSS file, find all hex colour codes. Solution: `/\v#(\x{6}|\x{3})`.
  Explanation: use `\v` for regex search and `\x` to capture hexadecimal
  characters (equivalent to `[0-9a-fA-F]`).

- Find "a.k.a." in a file. Solution: `/\Va.k.a.`. Explanation: we need `\V`
  or else `.` matches any character and we'd also find words like "backwards".

- Check for words that occurr twice in a row. Solution: `/\v<(\w+)\_s+\1>`.
  Explanation: `(\w+)` captures any word, `\_s` matches a linebreak or a space
  (see `h: /\_`), `\1` is the reference to the previously captured word, and
  `<,>` ensure that only two occurrences of the same word get matched and not
  also patterns like "n" in "in nord".

- Reverse the order of all occurrences of `Fab Gunzinger` and `Fabian
  Gunzinger`. Solution: `/\v(Fa%(b|bian)) (Gunzinger)`; `:%s//\2, \1/g`.
  Explanation: the first bit captures the short and full version of my first
  name, and my last name, without capturing the `b` or `bian` fragments.  First
  and last name can now be references using `\1` and `\2`, respectively.  The
  substitution command finds the last search pattern (since we leave `pattern`
  blank) and replaces it with my first and last names reversed.

- Find all occurences of "Vim" that are part of "Practical Vim". Solution:
  `/Practical \zsVim<CR>`.

- Find all quoted text. Solution: `/\v"\zs[^"]+\ze"`. Explanation: `"[^"]+"`
  matches quotes followed by one or more occurances of anything but quotes
  followed by quotes (this is a useful regex idiom). `\zs` and `\ze` exclude the
  quotes from the match. Note: this only recognises quoted text on the same
  line. Note: doesn't work over multiple lines.

- Find `http://someurl.com/search?=\//`. Solution: Yank pattern into a register,
  `u` for url, say; `/\V<C-r>=escape(@u, getcmdtype().'\')<CR>`. Explanation:
  see tip 79 in PV.

Exercises:

- In *music amuse fuse refuse* replace *us* with *az* in *amuse* and *fuse*
  using the substitute command (the point is to practice substitution in a
  limited area within a line).

Solutions:

- Use to the *a* at the beginning of *amuse*, then use `vee` to select the two
  words needed, `jk` (my mapping for `<esc>`) to leave visual mode, and
  `:s/\%Vus/az/g` to make the substitution in the last selected area: the `\%V`
  atom is what restricts the substitution to the last selected area.


### Search

#### Within a file

| Command             | Effect |
| - | - |
| `/<CR>`             | Search previous pattern forward |
| `?<CR>`             | Search previous pattern backwards |
| `/<UP>`             | Access search history (similar for backward search) |
| `<C-r><C-w>`        | Autocomplete search field based on preview match |
| `/{pattern}/e<CR>`  | Use search offset to jump to end of match (`h: |
| search-offset` for more offset options) |
| `gn`                | Operate on a complete search match |

Exercises:

1. In the paragraph below, replace all occurrences of "lang" or "langs" with
  "language" or "languages".
```
learn a lang each year
which lang did you learn?
which lang will you learn?
how many langs do you know?
```

2. Now repeat the above, but start out by searching without using the search
   offset to jump to the end of the word and then make use of it midway through
   my search.

3. Search for the line below each occurrence of "lang". 

4. Replace all occurrences of "PyCode" and "PythonCode" with "PYCode" or
   "PYTHONCode". 

Solutions: 

1. `/lang/<CR>`; `ea`; `uage`; `n.`.  Explanation: the second `/` denotes teh
   end of the pattern, so from then on we're back in command line mode.

2. Use `//e<CR>` to repeat the previous search pattern but with search offset
   used.

3. `/lang/+1`. Explanation: `+#` in search offset positions the cursor # lines
   after the match. 

4. `/\vPy(thon)?\C<CR>`; `gUgn`; `.`. Explanation: `gn` applies the pending
   operator (`gU` in this case) to the current match or, if the cursor isn't on
   a match, on the next one. After executing `gUgn` for the first time, the
   cursor changes the first match and remains there. Once we press `.`, the
   word under the cursor no longer is a match, so Vim jumps to the next match
   and applies the pending `gU` operator. Drew Neil calls this the "Improved
   dot-formula", since we can use `.` to achieve `n.`.


#### Across files

- There are many options for this. I currently use `vim-ripgrep`. The basic
  syntax is `:Rg <string|pattern>`, with `<string|pattern>` defaulting to the
  word under the cursor.

- Vim will ist the results in the quickfix window and jump to the first entry
  in the window.

Exercises:

1. Find all files that contain the line *import s3fs* in (a) the current
   directory and (b) in the subdirectory `/data`.

Solutions:

1. (a) `:Rg 'import s3fs`, (b) `:Rg 'import s3fs' data/`.


### Substitution

- Full syntax is `:[range]s[ubstitute]/{pattern}/{string}/[flags]`

- For substitutions across files I use
  [`quickfix-reflector`](https://github.com/stefandtw/quickfix-reflector.vim),
  which allows for editing the quickfix window, and performs the changes made
  there in all files.

Flags:

| Command             | Effect |
| - | - |
| `g`                 | Substitute all matches on line (global) |
| `c`                 | Confirm substitution |
| `n`                 | Count number of matches instead of substitution |
| `&`                 | Reuse flags from previous substitution |

Replacement strings:

| Command             | Effect |
| - | - |
| `\1`                | Insert first submatch (similar for {1-9}) |
| `\0`/`&`            | Insert entire matched pattern |
| `~`                 | Use string from previous substitution |
| `\={vim scrip}`     | Evaluate vim-script expression |

Useful commands

| Command             | Effect |
| - | - |
| `:&`                | Rerun last substitution (flags aren't remembered) |
| `:&&`               | Rerun last substitution and reuse flags |
| `:g&`               | Rerun last search globally |

Exercise:

1.  Replace `import helpers.aws as ha` with `from helpers import aws` in all
    files in the current directory.

2. Decouple pattern matching and substitution (useful for complex patterns that
   require trial and error). 

3. Use last search pattern in substitute command. 

4. Substitute the highlighted text fragment. 

5. Rerun the last line-wise substitution globally.

6. In a file with columns "name", "age", "height", change order to "height",
  "name", "age". 

7. Replace "Hello" in (and only in) "Hello World" with "Hi" in all files in my
  project. 

Solutions:

1. Find all files and open the quickfix window `:Rg 'import helpers.aws as
   ha'`, perform the change in each file inside the quickfix window and save.

2. `/{pattern}` until you get it right (maybe use `q/`), then `:s//{string}`.
   Explanation: leaving {pattern} blank uses last search pattern.

3. `:s/<C-r>//{string}`

4. `` *:s//{string} ``.  Explanation: with [vim visual
   star](https://github.com/nelstrom/vim-visual-star-search) plugin installed,
   ``*`` searches for pattern highlighted in visual mode.

5. `g&`.

6. `/\v^([^,]), ([^,]), ([^,])$`; `:%s//\3, \1, \2`.

7. First, test pattern in current buffer: `/Hello\ze World<CR>`, then search
   all files in project and populate quickfix list with files that have a
   match: ``:vimgrep // **/*.txt``, finally: iterate through the files in the
   quickfix list to execute the substitute and update commands: `:cfdo
   %s//Hi/gc | update`


### Global commands`

- Full syntax: `:[range] global[!] /{pattern}/ {cmd}`. Range defaults to the
  entire file, leaving the pattern empty uses last search pattern, and command
  defaults to print.

- A generalised version of the command, useful to operate inside text or code
  blocks, is `:g/{start} .,{finish} [cmd]`, which applies the command to each
  range of lines that begins with {start} and ends with {finish}. See CSS
  sorting example below.

| Command                 | Effect |
| - | - |
| `g[lobal]`              | Global command |
| `v[global]`             | Invert global |
| `g[lobal]!`             | Invert global |

Exercises:

1. Delete all lines that contain "Hi". 

2. Keep only lines that contain "Hi". 

3. Print all lines that contain "Hi".

4. Yank all lines that contain "TODO" into register a. 

5. Glance at markdown file structure (create a table of contents).

6. Glance at top-level markdown titles.

7. Glance at markdown top and secondary level titles. 

8. Alphabetically sort properties inside each rule of a CSS file. 

Solutions:

1. `:g/Hi/d`.

2. `:v/Hi/d`.

3. `:g/Hi`.

4. `qaq` (to empty register); `:g/TODO/yank A`. Explanation: need capital `A`
   to append to rather than overwrite register.

5. `g/^#`.

6. `:g/^# `

7. `:g/\v^#(#)? `. Explanation: Need `\v` so that parentheses have magic
   characteristics (otherwise I'd have to escape them, which is cumbersome),
   need `?` ...

8. `:g/{/ .+1,/}/-1 sort`. Explanation: `/{/` is the pattern of the global
   command and searches for all lines that contain an `{`. `.+1,/}/-1` is the
   range of the Ex command, specified as from the current line until the next
   line that contains a closing curly bracket.  The offsets narrow the range to
   exclude the lines with curly brackets. The current line address here stands
   for each line in turn that matches the `/{/` pattern.


## Folds

| Command                     | Effect |
| - | - |
| `zR`                        | Open all folds |
| `zM`                        | Close all folds |
| `<leader><space>`           | Toggle fold under cursor (mapping of `za`) |


## Mappings

- General syntax: `{cmd} {attr} {lhs} {rhs}`.

- Mapping process: define the sequence of keys to be mapped, decide the editing
  mode in which the mapping will work, find a suitable and free key sequence.

- Understanding `noremap` mappings: by default, vim mappings are recursive
  (i.e.  if a is mapped to b and b to c, then a is really mapped to c because b
  will be expanded on the rhs. The second mapping could be part of a plugin so
  that I'm not even aware of it). This behaviour is set with the `remap`
  option.  To define non-recursive mappings, we can use the `noremap` mappings.

| Command                 | Effect |
| - | - |
| `:nmap {char}`		    | List all normal mode mappings starting with {char} |
| `:verbose nmap {char}`	| As above, but shows location where maps are defined |


## Editing

### Autocompletion

| Command                 | Effect |
| - | - |
| `<C-n>`/`<C-p>`         | Trigger autocompletion and navigate |
| `<C-e>`                 | Dismiss autocomplete window |
| `<C-n><C-p>`            | Filter suggestions as we type |
| `<C-x><C-k>`            | Dictionary lookup (requires spellchecker on - `yos`) |
| `<C-x><C-l>`            | Autocomplete entire line |
| `<C-x><C-f>`            | Autocomplete filename (relative to pwd) |

I've experimented with `youcompleteme`, which I deleted again because its too
clunky for my taste. In case I want to install again in the future, this might
be helpful:
[Often](https://github.com/ycm-core/YouCompleteMe/wiki/FAQ#ycm-does-not-work-with-my-anaconda-python-setup)
doesn't work with Anaconda Python, and I seem to be one of those cases.
Followed the suggestion in the link. I first tried compiling with
`/usr/bin/python3`, but this didn't work. I then tried
`/usr/local/bin/python3.9`, following
[this](https://stackoverflow.com/questions/62546912/youcompleteme-completed-failed),
which seems to have worked.


### Spell checking

| Command                 | Effect |
| - | - |
| `yos`                   | Toggle spell checker (uses `vim-unimpaired`) |
| `]s`/`[s`               | Jump to next/previous misspelled word |
| `z=`                    | Suggest corrections |
| `[n]z=`                 | Correct word with nth suggestion |
| `zg`                    | Add current word to spell file (mnem: "good") |
| `zw`                    | Remove current word from spell file (mnem: "wrong")
| | |
`zug`                   | Revert `zg` or `zw` command for current word


### Formatting

| Command                  | Effect |
| - | - |
| `gq{motion}`             | Formats text, defaults to wrapping long lines. |


### Case coercion

Uses [vim-abolish](https://github.com/tpope/vim-abolish), which deals with word
variants and provides powerful searching, grepping, substitution and case
coercion.

| Command             | Effect |
| - | - |
| `crs`               | Coerce to `snake_case` |
| `crc`               | Coerce to `camelCase` |
| `crm`               | Coerce to `MixedCase` |
| `cru`               | Coerce to `UPPER_CASE` |
| `cr-`               | Coerce to `dash-case` |
| `cr.`               | Coerce to `dot.case` |
| `cr<space>`         | Coerce to `space case` |
| `crt`               | Coerce to `Title Case` |

Exercises:

1. Replace all occurrences of *child[ren]* with *adult[s]*.

2. Replace all occurrences of *man* with *dog* and vice versa.

Solutions:

1. `:%S/child{,ren}/adult{,s}/g`

2. `:%S/{man,dog}/{dog,man}/g`. Discussion: Don't use whitespace after comma,
   as Vim would treat it as part of the search/replacement pattern.


### Comments

Uses [vim-commentary](https://github.com/tpope/vim-commentary)

Main commands:
- `gc{motion}`
- `gcc`
- `{Visual}gc`
- `:[range]Commentary`


## Language and program specific settings

### Git

- I use basic commands from vim-fugitive


### Python

- Execute makefiles using `:make` (Set up quicklist such that I can jump to
  errors directly, this currently doesn't work. Probably requires some
  additional setup to recognise Python errors.)

- I use Ctags to navigate my codebase. I've followed Tim Pope's
  [approach](https://tbaggery.com/2011/08/08/effortless-ctags-with-git.html) to
  set this up. For newly initialised or cloned directories, this setup
  automatically creates hooks and indexes the code with Ctags. For existing
  directories, you need to run `git init` to copy the hook templates into the
  local `.git/hooks`, and then `git ctags` to index the code.

Ctag commands:

| Command             | Effect |
| - | - |
| `<C-]>`             | Jump to definition of keyword under cursor |
| `g<C-]>`            | As above, but select definition if there are multiple |
| `:tag {keyword}`    | Jump to definition of keyword |
| `:tjump {keyword}`  | As above, but select definition if there are multiple |
    
- Look into using `matchit` or something similar for faster code navigation.


### Latex

- You can use `<C-N>` completion for words that already appear in one of the
  open buffers. This is especially useful for bibliography completion: just open
  the .bib file in another buffer and `<C-N>` will provide a list of
  available keys.

- I use [vimtex](https://github.com/lervag/vimtex), with `Skim` as my viewer. In
  vimtex, most shortcuts use `localleader`, which, by default, is set to `\`.

Vimtex commands:

| Command             | Effect |
| - | - |
| `\ll`               | Toggle continuous compilation using `latexmk` |
| `\lk`               | Kill compilation process |
| `\lc`               | Clear auxiliary files |
| `\lt`               | Show table of contents |
| `\ds{c/e/$/d}`      | Delete surrounding command/environment/math env/delimiter |
| `\cs{c/e/$/d}`      | Change surrounding command/environment/math env/delimiter |
| `:VimtexDocPackage` | Show docs for argument under cursor or supplied package
| | |
| `:VimtexCountWords` | Count words in document |
| `<C-x><C-o>/`       | Citation completion (inside `\cite{`) |
| `]]`                | To next section |
| `]m`                | To next environment |
| `]n`                | To next math zone |
`]r`                | To next frame

Vimtex text objects:

| Command             | Effect |
| - | - |
| `c`                 | Command |
| `d`                 | Delimiters (e.g. `[`, `{`) |
| `e`                 | Environment |
| `$`                 | Inline math environment |
| `P`                 | Sections |
| `m`                 | Items |

## Obscurities

- `<plug>` Allows authors of plugins to pre-map commands to so users can easily
  map them to their preferred keys. E.g. `<plug>(test)` might stand for a very
  long sequence of commands. To map that sequence to `<leader>t`, I can simply
  use `nmap <leader>t <plug>(test)`.
  [This](https://vi.stackexchange.com/a/31013) SE answer explains it very
  clearly.


## Troubleshooting

### Command-t ruby version differs from expected

- Error mesassage: "command-t cound not load the C extension ... VIM RUBY
  version (version number) Expected version (different version number)."

- Solution: recompile Command-T with the new system Ruby. Steps are detailed
  under "Compiling Command-T" in the Command-T helpfiles. They are as follows:

  `cd~/.config/nvin/plugged/command-t/ruby/command-t/ext/command-t`
  `ruby extconf.rb`
  `make`.


### CSS indent not working

- Vim recognised css files, but used my global indent of 4 spaces rather than a
  file-type specific indent of 2 spaces.

- `h: filetype` notes that filetype detection files are located in the runtime
  path. Going there, I found the `ftplugins` folder that contains the default
  file settings. Looking at `css.vim` makes clear that it doesn't set any
  tabstop settings, which explains why the defaults were used.

- Googling something along the lines of "custom filetype indent vim" let me to
  [this](https://stackoverflow.com/a/159066) SO answer, which helpfully links
  to `h: filetype-plugins`. Once there, it was easy to find the relevant
  section, `ftplugin-overrule` that documents how to add custom filetype
  settings. This is what I did, and it worked like a charm.


## Sources

This cheat sheet started out as a summary of Drew Neil's phenomenal [Practical
Vim](https://pragprog.com/titles/dnvim2/practical-vim-second-edition/), which I
can't recommend enough as a start to learning Vim seriously.

Other resources I found useful:

- [Vim Fandom mappings
  tutorial](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_2))
- Dough Black's [good vimrc](https://dougblack.io/words/a-good-vimrc.html#fold)
- Using help: https://vim.fandom.com/wiki/Learn_to_use_help
- [Idiomatic VIM](https://github.com/romainl/idiomatic-vimrc)
- Awesome vimrc: https://github.com/amix/vimrc
- Vim as Python IDE: https://realpython.com/vim-and-python-a-match-made-in-heaven/


