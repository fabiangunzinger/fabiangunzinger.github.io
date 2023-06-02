---
title: "Data science workflow"
subtitle: "Evolving notes"
tags: [python]

date: 2022-02-28
featured: false
draft: true

reading_time: false
profile: false
commentable: true
summary: " "

---


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



## Version control


- For each dataset I work with, I have a separate GitHub repo (named
  `data-NAME`) which contains
  code to minimally clean the data so as to create a version of the data that I
  can then use for all projects in which I use the data, the data documentation,
  and any thoughts and notes pertaining to the data (e.g. known limitations,
  additional information from the data provider, etc.).


## Dependency management

Tools:

- [pyenv](https://github.com/pyenv/pyenv) is a Python version manager.

- [virtualenv](https://github.com/pypa/virtualenv) is a tool to create isolated
  virtual Python environments.

- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) is a pyenv
  plugin that allows you to use pyenv to manage virtualenvs.

- [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
  provides a set of wrappers to work with virtualenvs.

- [poetry](https://python-poetry.org) is a packaging and dependency manager.


Workflow (evolving):

- Create virtual environment `pyenv virtualenv 3.9 projectname` and activate
  venv `pyenv activate projectname`.

- Create project folder with Poetry for nice default setup `poetry new
  projectname` but rename `projectname` subdirectory to `src` because of
  [this](https://hynek.me/articles/testing-packaging/) blog post.

- Install required dependencies `poetry add pandas numpy seaborn` and
  development dependencies `poetry add --dev ipykernel`.

- Can reinstall dependencies using `poetry install`.



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




## Sources

- Great
  [post](https://www.ethanrosenthal.com/2022/02/01/everything-gets-a-package/)
  by Ethan Rosenthal on dependency management and packaging.
