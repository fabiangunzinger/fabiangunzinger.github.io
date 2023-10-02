---
title: "Development setup and workflow"
subtitle: "Evolving notes"
tags: [tools]

date: 2022-02-28
featured: false
draft: true

reading_time: false
profile: false
commentable: true
summary: " "

---

Setting up a new macbook as a development machine can be painful. Here I want to collect what I do, why I do it, and how I use my setup.


## Homebrew

- I install all software with homebrew (using --cask for mac programs)

- Differences on M1 macs [here](https://earthly.dev/blog/homebrew-on-m1/#:~:text=On%20Intel%20Macs%2C%20Homebrew%2C%20and,%2Fusr%2Flocal%2Fbin%20.&text=Homebrew%20chose%20%2Fusr%2Flocal%2F,in%20your%20PATH%20by%20default.)


## SSH setup

- I want to be able to work on work and personal Github projects on my machines, and I use `.gitconfig` files to make this all work smoothly.

- My setup is as follows (largely following [this](https://blog.gitguardian.com/8-easy-steps-to-set-up-multiple-git-accounts/) tutorial):

1. Create ssh key without creating a passphrase: `cd ~/.ssh` and `ssh-keygen -t rsa -C "personal-email-address" -f "github_personal"`. The -t flag allows me to specify the type of key I want to generate, the -C flag to add a comment, the -f flag to add a file name.

2. Add SSH keys to SSH Agend: `ssh-add ~/.ssh/github_personal`.

3. Add SSH public key to Github account: go to account's SSH and GPG keys page in setting and add new account.

4. Create a config file `~/.ssh/config` to ensure the SSH agent uses the right key when connecting to a remote repository (I think this is not actually needed, and it's currently disabled in my settings).

```{markdown}
Host *
    AddKeysToAgent yes
```

5. Create a global `.gitconfig` file that tells git which config file to use depending on the directory I'm in (see [here](https://git-scm.com/docs/git-config#_conditional_includes) for details).

```{markdown}
[includeIf "gitdir:~/dev/personal/"]
    path = ~/dev/projects/dotfiles/git/.gitconfig.personal

[includeIf "gitdir:~/dev/work/"]
    path = ~/dev/projects/dotfiles/git/.gitconfig.work

[core]
    editor = nvim
```

6. Create the personal config file.

```{markdown}
[user]
    name = fabiangunzinger
    email = fa.gunzinger@gmail.com

[core]
    sshCommand = "ssh -i ~/.ssh/github_personal"
```

7. Done. I then repeat the same process for my work projects.

8. This way, when I'm in any directory in `~/dev/personal`, Github uses my personal email and user name as well as my personal ssh key for all connections. A very similar result coult be achieved by using `~/.ssh/config`, as described [here](https://www.freecodecamp.org/news/the-ultimate-guide-to-ssh-setting-up-ssh-keys/) and [here](https://gist.github.com/rahularity/86da20fe3858e6b311de068201d279e3), with the main difference that I'd have to manually specify username and email every time I clone a new repo, because there is no way to automatically set them via ssh. This would be slightly annoying, which is why I use gitconfig.

## Managing Python

I manage Python versions on my machine using
[pyenv](https://github.com/pyenv/pyenv), and virtual environments using
[`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv).


## Project management

The workflow for a new project is the following: 

I create a virtual environment with a specific Python version (e.g. 3.10.8) and activate it:

```commandline
pyenv virtualenv 3.10.8 project-name
pyenv activate project-name
```

### Poetry vs pip?

I install dependencies using `pip`. Hence, to install pandas into my currently active virtual environment, I'd use:

```commandline
pip install pandas
```

Or, sometimes I use Poetry. Still experimenting with it.

- In project folder, initiate poetry with `poetry init`. Fill in setup steps as
  required.

- Install required dependencies `poetry add pandas numpy seaborn` and
  development dependencies `poetry add --dev ipykernel`.

- Can reinstall dependencies using `poetry install`.

(See macsetup.md for installation and settings)

## Jupyter notebooks

Following approach of [Ethan Rosenthal](https://www.ethanrosenthal.com/2022/02/01/everything-gets-a-package/), I have a `base` environment that gets automatically activated when I start a shell session and that has Jupyter installed. I manage this environment with Poetry, and from a normal project folder (~/dev/projects/base). I start all my Jupyter sessions from this environment. The advantage of this is that I only have to customise Jupyter Lab once.

As a development dependency, I install ipykernel as a development dependency. With `poetry`, I'd do the following:

```commandline
poetry add --dev ipykernel
```

I make the IPython kernel of my project's virtual environment (with all the
necessary dependencies installed) available to Jupyter in the base
environment like so (from [IPython
docs](https://ipython.readthedocs.io/en/latest/install/kernel_install.html)):

```commandline
/path/to/project/env/bin/python -m ipykernel install --prefix=/path/to/base/env
--name 'project-name'
```





## Tools:

- [pyenv](https://github.com/pyenv/pyenv) is a Python version manager.

- [pipenv](https://pipenv.pypa.io/en/latest/) is a dependency manager for
  Python projects. Allows for using pip and virtualenv together.

- [virtualenv](https://github.com/pypa/virtualenv) is a tool to create isolated
  virtual Python environments.

- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) is a pyenv
  plugin that allows you to use pyenv to manage virtualenvs.

- [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
  provides a set of wrappers to work with virtualenvs.

- [poetry](https://python-poetry.org) is a packaging and dependency manager.




### Conda

- I create a separate environment for each major project.

- For smaller projects, I use generic Python version environment that I create
  for each major Python update and name accordingly (e.g. `python3.9`). When I
  start a small project, I use the latest generic environment and export the
  `environment.yml` to the project folder so I can reproduce the repo in the
  future (e.g. after I've added/updated packages).

- I'm currently using `conda`, but find it a bit clucky and slow, and have been
  thinking about moving to an alternative like pyenv (for managing Python
  version), pipenv, or poetry. But I don't understand how they relate to one
  another, so need to to this if I want to switch.



Advantages:

- Easily handles separate Python versions for each project.


Disadvantages:

- I find it clunky and often slow (removing a package can take an extremely
  long time).

- Some packages aren't available, so you need PyPI (via pip) nonetheless.


## Data Science workflow

I’m about to start with the write up of the entropy paper, but now face the
issue that exporting nice regression tables from Python is a pain. linearmodels
provides a comparison a function to create model summary tables but it can only
display numbers using scientific notation, which is a pain. Worse, I can’t seem
to use estimates from linearmodels with the Python stargazer package, as the
latter expects fitted models as input, while linearmodel’s `fit()` function
automatically produces a results object. Can this be changed? It really seems
like it cannot. Not being able to use at least the basic stargazer version
available in Python is a deal breaker. It is another reminder that Python is
not the best language to do empirical social science. For this you’d really
want to use R or Stata.

I’m gonna try the following workflow:
- Use Python for data preprocessing all the way up to creating analysis data
- Use Python or Rmd for exploratory analysis
- Use R for analysis and all paper figures and tables.

What do I need to do this?
- Need to be able to read from s3
- Data library in R: use data.table
- Graphics library: use ggplot
- Estimation library: use based on need.
- Regression table library: use stargazer.

- For each dataset I work with, I have a separate GitHub repo (named
  `data-NAME`) which contains
  code to minimally clean the data so as to create a version of the data that I
  can then use for all projects in which I use the data, the data documentation,
  and any thoughts and notes pertaining to the data (e.g. known limitations,
  additional information from the data provider, etc.).


## Blog

I use my blog mainly for note taking.

I currently use Hugo with the wowchemy theme.

Considerations to switching to blogdown:
- The [apero](https://hugo-apero.netlify.app/) theme looks beautiful and has gread [documentation](https://hugo-apero-docs.netlify.app/).
- Can I write Rmd posts in vim? Check out 


## Note taking

- I currently use Apple notes because it is leightweight and syncs seamlessly across all my devices.

- It has two major disadvantages: it requires context switching away from the terminal, which increasingly bothers me, and it doesn't allow for version control.

- Ideally, I want to look into the notes recommended by engineeringfordatascience.

- If these don't allow me to write in the terminal, then I want to look into a way to easily sync and edit the markdown files in this directory on my phone.





## Sources

- Great
  [post](https://www.ethanrosenthal.com/2022/02/01/everything-gets-a-package/)
  by Ethan Rosenthal on dependency management and packaging.
