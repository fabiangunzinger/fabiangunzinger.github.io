---
title: "Git"
subtitle: "Notes and best-practices"
tags: [tools]

date: 2022-02-02
featured: false
draft: false

reading_time: false
profile: false
commentable: true
summary: " "

---

My evolving notes and on how to effectively use Git and GitHub.


## Git

- Evolution of version control systems (and their shortcomings): from having
  **differently named files and folders** (error prone and inefficient) to
  **local version control systems (LVCs)** where files are checked out from a
  locally hosted database that contains the entire history (single point of
  failure and impractical for collaboration) to **centralized version control
  systems (CVCSs)** where files are checked out from a server-hosted database
  (single point of failure) to **distributed version control systems (DVCs)**
  where files and a database containing the entire history are checked out from
  a served-hosted database, so that each local node contains all information
  stored on the server (content on server can easily be restored in case of
  failure).

- Git stores data as snapshots: at each new commit, modified files are replaced
  with a snapshot of their new state, while unmodified files are replaced with
  a link to the previous snapshot.

- In a basic workflow I edit a file in the *working tree* (the locally checked
  out version of the project), add them to the *staging area* (also called
  *index*), *commit* them to the local database, and finally push them to the
  remote database on GitHub.

- Neither *main* (or, formerly, *master*), nor *origin* have any special
  significance in Git. The reason they are widely used is that *main* is the
  default name for the starting branch when running `git init` and *origin* is
  the default name for the remote repository when running `git clone`.

- Git stores a single file as a
  [blob](https://en.wikipedia.org/wiki/Binary_large_object), which is a
  [backronym](https://en.wikipedia.org/wiki/Backronym) for *binary large
  object* and is a collection of binary data. It can store any type of data
  including multimedia files and images. Blobs in the git object database are
  stored named with a SHA-1 hash key of their content and containing the [exact
  same](https://stackoverflow.com/a/48959460/13666841) content as the file
  would on my filesystem.


## Interacting with remotes

- A *remote repository* is a version of the project that's hosted on a server,
  in my case always on GitHub. The default name Git assigns to the remote when
  I clone it is *origin*. (Technically, the remote could also be hosted on my
  machine but in a separate location from my working copy.)

- `git fetch <remote>` downloads all new objects from the remote repository
  (e.g.  including references to new branches) but does not automatically merge
  these objects into my local work. `git pull` fetches and automatically merges
  the remote version of the local branch I'm currently on and merges it if the
  current branch is set up to track the remote. By default, `git clone` sets up
  my local `main` branch to track the remote version, named `origin/main`.

- To share work with the remote, I can use `git push <remote> <branch>` (e.g.
  to share work from my local `main` branch with `origin/main`, I can do `git
  push origin main`).


## Undoing things

- Cardinal rule: don't push stuff before you're fully happy with it. Changing
  your local history is easy, changing the history on the server isn't.

- Changing message of last commit: (with an empty index) run `git commit
  --amend`.

- Changing the content of the last commit: stage changes you want to add, then
  run `git commit --amend`. If you don't want to change the commit message,
  append `--no-edit`.

- Unstaging a staged file: `git restore --staged <pathspec>`. 

- Undoing changes in the working directory and reverting a file to its state
  after the last commit: `git restore <pathspec>`.

- Changing multiple commits (edit, reorder, squash, delete, split,
  etc.): `git rebase -i HEAD~#`, where `#` is the parent of the last commit you
  want to edit (e.g. if you want to edit the last 3 commits, `HEAD~3` will
  select commits `HEAD`, `HEAD~1`, and `HEAD~2`). More in
  [docs](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History)

- I've accidentally overwritten a file with content I meant to place in a
  new file, and now want to 1) save the new content under a different name and
  2) restore the file I've overwritten. Solution: Just save the new content
  under a new name (temporarily deleting the file I've accidentally
  overwritten, and then use `git restore <name_of_overwritten_file>` to restore
  the old version of the overwritten file.

- I've deleted one or more commits (e.g. by using a hard reset) that I need to
  recover. First thing to try: run `git reflog` to get a log of commits HEAD
  pointed to. Once I've identified the commit I need (ab1af) I can create a new branch
  that points to it using `git branch recover-branch ab1af`. If there is no
  reflog, I can run `git fsck --full` to check the database for integrity and
  get a list of objects that aren't reacheable. The commit I'm looking for will
  be labelled with `dangling commit`, and I can create a branch pointing to it.

- Removing a file from every commit (e.g. accidentally committed large data
  file): `git filter-branch --index-filter 'rm --ignore-unmatch --cached
  data.csv' HEAD`. This can take a long time. One way to speed things up is to
  find the commit that added the file to the history and only filter downstream
  from there. `git log --oneline --branches -- data.csv` will list all commits
  that contain the file from latest to earliest. If the file was added in
  commit `a34s5`, then I only want to rewrite commits `a34s5^..HEAD`, which I
  can substitute for `HEAD` in the `filter-branch` command. (In case I don't
  know the name of the large file I want to remove, see
  [here](https://git-scm.com/book/en/v2/Git-Internals-Maintenance-and-Data-Recovery)
  for how to find it. Finally, as advised in relevant section
  [here](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History), it's best
  to first do this on a separate branch to test the behaviour before running it
  on `main`.


## Frequently used stuff and best practices 

- I've started to work on an issue I decide I don't want to work on yet but I
  want to save that work. Just
  [stash](https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning) the
  work.

- I'm working on a topic branch and discover another issue I need to fix first.
  What to do?

- Create local version of remote branch that automatically tracks remote branch
  (if branch has unique remote counterpart): `git switch <branch>`.

- Reset vs restore vs revert vs rebase (docs
  [here](https://git-scm.com/docs/git#_reset_restore_and_revert)): `reset` is
  about updating your branch by adding or removing commits from the branch,
  `restore` is about unstading files from the index or undoing changes in the
  working directory, `reset` is about making new commits to undo changes made
  by other commits,
  [`rebase`](https://git-scm.com/book/en/v2/Git-Branching-Rebasing#_rebase_peril),
  like `merge`, is a way to integrate work from two different branches. But
  unlike `merge`, which takes the endpoints of two branches and merges them
  together, `rebase` applies changes from the branch you merge onto the branch
  you merge to in the order they happened and thus creates a linear history.

- Adding a local repository to GitHub:
    
    1. Initialise the local repo as a Git repository: `git init`.

    2. Add and commit all content of the local repo: `git add --all; git commit
       -m 'Intial commit'`.

    3. Create a GitHub repo and follow prompts: `gh repo create`.

    4. Done.


## Understanding reset

- Think of **HEAD** as the last commit on the current branch (it's a pointer to
  the current branch which is a pointer to the last commit on that branch), the
  **index** as the proposed next commit, and the **working directory** as a
  sandbox. Think of all of them as collections of files, or file trees.

- When I switch to a branch, Git makes HEAD point to the new branch ref,
  populates the index with the snapshot of the last commit on that branch, and
  copies the contents of the index into the working directory.

- Changing a file updates it in the working directory, staging it updates the
  version in the index with that of the working directory, and committing it
  updates the version HEAD points to with that of the index.

- `git reset --soft HEAD~` moves the branch that HEAD points to to the parent
  of the last commit. The version of the file that HEAD points to now differs
  from the versions in the index and the working directory, which still contain
  the version of the last commit on the branch. Effectively, we've undone the
  last commit. You could now make changes to the index and then commit them,
  accomplishing the same as `git commit --amend`. So, `--soft` undoes `git
  commit`.

- `git reset [--mixed] HEAD~` moves the branch HEAD points to (just as `--soft`
  above) but then also updates index with the content of the snapshot HEAD now
  points to. So, `--mixed` undoes `git commit` and `git add`.

- `git reset --hard HEAD~`, does what the above does, but then continues and
  also updates the working directory with the content of the index. This
  forcibly overwrites files, which, if they haven't been committed (in which
  case they can be recovered using the reflog), is unrecoverable. So, `--hard`
  undoes `git commit`, `git add`, and all changes made in the working
  directory since the last commit.

- We can undo multiple commits: to undo all commits since commit *9e5bf*,
  simply run `git reset <option> 9e5bf`.

- `reset` is also handy to squash commits together. To squash the last three
  unpushed commits, use `git reset --soft HEAD~3`. This moves the branch ref to
  the great-grandparent of the latest commit. Because the index remains
  unchanged, all changes committed after `HEAD~3` now appear as staged and can
  be committed in a single new commit.


## Writing good commits

- Writing good commits (more
  [here](https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project)):

  1) No whitespace errors (`git diff --check`, probs integrated in `fugitive`
  somehow).

  2) Each commit is a logically separate changeset.

  3) Useful commit message using capitalisation and written in imperative style
  ("Fix bug" instead of "Fixed bug" or "Fixes bug", to be compatible with Git's
  auto generated messages) comprising a short summary (no longer than 50
  characters so it fits on one line in log) followed by a blank line followed
  by a motivation for the changes and a description of the contrast between old
  and new behaviour.


## Selecting commits

- [Docs](https://git-scm.com/book/en/v2/Git-Tools-Revision-Selection)

- Short SHA-1 hashes: `git show d921` shows the commit with abbreviated SHA-1 hash `d921`.

- Branch references: `git show iss3` shows the commit on the tip of the branch
  `iss3`.

- Ancestry references: There are two different ways of ancestry selection which
  I think of as "horizontal" and "vertical" selection. `^` selects different
  parents for merge commits: `git show d921^` shows the first parent of the
  merge commit. By default, this parent is from the branch from which the merge
  was performed (frequently `main`). `git show d921^2` shows the second parent,
  which is from the branch that was merged. I think of this as horizontal
  ancestor selection.  Conversely, `~` performs vertical ancestor selection in
  that it iteratively selects the first parent a specified number of times.
  `git show d921~` shows the parent of `d921`, `git show d921~2` the parent of
  the parent, `git show d921~3` the parent of the parent of the parent, and so
  on (the previous could also be written as `git show d921~~~`). The two
  syntaxes can be combined: `git show d921~2^2` shows the second parent of the
  grandparent of `d921`, assuming the grandparent is a merge commit.

- Double dot: `git log main..iss3` lists all commits that are reachable from
  the `iss3` but not the `main` branch. Git substitues `HEAD` if one side of
  `..` is empty, so to list local commits that aren't yet on the remote, you
  could do `git log origin/main..`. Similarly, to select the last three
  commits, use `HEAD~3..HEAD`, which selects all commits reachable from `HEAD`
  but not `HEAD~3`, which are commits `HEAD~2`, `HEAD~`, and `HEAD`.

- Triple dot: to list commits that occur either on `master` or `iss3` but not
  both, I can do `git log master...iss3`, and to get arrows to indicate whether
  a commit is reachable from the right or left branch, `git log --left-right
  master...iss3`.


## Misc.

- To search for commit message in log history: `git log --grep='regex'`


## `.gitignore`

- The section on ignoring files in
  [this](http://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository)
  ProGit book chapter is excellently clear and provides very useful examples.

