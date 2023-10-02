---
title: "tmux"
subtitle: ""
tags: [tools]

date: 2022-02-28
featured: false
draft: true

reading_time: false
profile: false
commentable: true
summary: " "

---

## Getting help

- `man tmux`

- `tmux list-commands` lists all commands. To find all commands related to
  panes, I can thus use `tmux list-commands | grep pane`.

## Workflow

- One client (i.e. use tmux in a single iTerm tab only), one session per
  project, as many windows as needed per session, as many tabs as needed per
  window, one vim instance per session (to avoid cross-editing files)

- Custom configs in `.tmux.conf`


## Key bindings I use often

General

| Key               | Legend |
| -                 | - |
| `prefix ?`        | List default key bindings |

### Panes 
| Key               | Legend |
| -                 | - |
| `C-d`             | Exit current pane |
| `prefix o`        | Select the next pane |
| `prefix C-o`      | Rotate through the panes |
| `prefix z`        | Toggle to zoom current pane into full-screen |



Windows

- `<prefix ->`: split window vertically
- `<prefix \>`: split window horizontally
-
- `<prefix window-#>`: jump to window #
- `<prefix n>`: jump to next window
- `<prefix p>`: jump to previous window
- `<prefix l>`: jump to last window

Sessions

- `tat`: To open session, navigate to project directory and type `tat` (for tmux
  attach), which automatically creates a new session with the name of the
  project directory. The script lives in `~/bin`, and is from
  [here](https://github.com/thoughtbot/dotfiles/blob/main/bin/tat).

- `<C-j>`: open choose-tree to jump between sessions.
- `<prefix L>`: jump to last session

Scrollback

- Requires settings in .tmux.conf

- `<prefix [>`: enter copy-mode. From here can use vim-bindings to navigate long command output.

