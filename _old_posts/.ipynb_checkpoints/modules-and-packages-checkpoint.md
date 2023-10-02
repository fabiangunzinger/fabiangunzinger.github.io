---
title: "Python modules and packages"
subtitle: "Notes"
tags: [python]

date: 2021-05-21
featured: false
draft: false

reading_time: true
profile: false
commentable: true
summary: " "

---

## Modules

- A *module* is a file that contains definitions intended for reuse in a script
  or an interactive session.

- Calling `import module` for the first time does three things: 1) create a new
  namespace that acts as the global namespace for all objects defined in module,
  2) execute the entire module, 3) create a name -- identical to the module name
  -- within the caller namespace that references to the module. This can be used
  to access module objects in the caller namespace as `module.object`.

- Calling `from module import symbol` imports `symbol` into the current
  namespace. However, the global namespace for `symbol` (if it's a function)
  always remains the namespace in which it was defined, not the caller's
  namespace.

- Regardless of what variant of the import statement is being used to import
  contents from a module, all of the module's statements will be initialised the
  first time (and only the first time) the module name is encountered in an
  import statement (more details
  [here](https://docs.python.org/3/tutorial/modules.html#more-on-modules)).

- One reason `from module import *` is generally discouraged is that it directly
  imports all the module's objects into the caller's namespace, which is often
  said to cluter it up. Especially when importing large modules this makes
  sense, as it's much cleaner to keep objects defined in imported modules in
  eponymous namespaces and accessing them via `module.object`, which immediately
  makes clear where object comes from and can help greatly with debugging.

- One implication of all the above is that as a developer, you don't have to
  worry about clashing variable names between modules, as they are each stored
  in their own namespace, and accessed via `moduleA.foo` and `moduleB.foo` in
  the caller namespace.

- When we import a module `foo`, the interpreter first searches for a built-in
  module and, if none is found, searches a list of directories given the
  variable `sys.path`. `sys.path` contains the directory of the input script,
  the variable `PYTHONPATH`, and installation-dependent defaults. I can
  manipulate `sys.path` using standard list operations; to add a directory, use
  `sys.path.append('dirname')`.

- A common usecase of the above for me is to make a package available to Jupyter
  Notebooks. By default, a notebook's `sys.path` contains the folder the noteook
  is located in and a bunch of conda managed directories linked to my running
  Conda environment. To make available a package that lives in the project root
  directory, just do
  `sys.path.append('/Users/fgu/dev/projectname/packagename')`. I can then
  reference modules from the package using `from packagename import module`.

- Use `dir(modulename)` to list all names defined in `modulname`, or `dir()` to
  list all names that are currently defined.


## Running a module as a script

- For relative imports to work as described, for instance, here and in Chapter 8
  in Python Essential References and in recipees 10.1 and 10.3 in the Python
  Cookbook, the file into which you import has itself to be a module rather than
  a top-level script. If it's the latter, it's name will be main and it won't be
  considered part of a package, regardless of where on the file system it is
  saved. Generally, for a file to be considered part of a package, it needs to
  nave a dot (.) in its name, as in package.submodule.modulename.

- To import modules into a main script, one (somewhat unideal) solution is to
  add the absolute path to the package to `sys.path`.


## Packages

- Packages are collections of modules. They help structure Python's module
  namespace by using dotted module names. E.g. `a.b` refers to submodule `b` in
  package `a`. Thus, just as the use of modules alleviates worries about
  clashing global variable names between modules, using a package alleviates
  worries about clashing module between multi-module packages.

### Example: creating utility package

Utils repo:

- If you want to publish to PyPI, choose name that doesn't exist yet.

- Create virtual environment `pyenv virtualenv 3.9 futils` and activate
  venv `pyenv activate futils`.

- Create project folder with Poetry for nice default setup `poetry new
  projectname` but rename `projectname` subdirectory to `src` because of
  [this](https://hynek.me/articles/testing-packaging/) blog post.

- Install required dependencies `poetry add pandas numpy seaborn` and
  development dependencies `poetry add --dev ipykernel`.

- Can reinstall dependencies using `poetry install`.

- Publish project to private server: `poetry publish -r reponame`. -- currently
  not working, getting 403 forbidden error


Project repo:

- Install 


## todo

- Automatic git credentials reading when publishing package

- Remove pyenv prompt warning message


## Sources

- [Python docs -
  Modules](https://docs.python.org/3/tutorial/modules.html#executing-modules-as-scripts)

- [SO answer on relative imports for
  scripts](https://stackoverflow.com/questions/14132789/relative-imports-in-python-2-7/14132912#14132912)

