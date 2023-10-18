---
title: "Creating a Python package"
date: "2023-10-11"
categories: [craft]
tag: [tools, Python]
draft: false
math:
  enable: true
---

Creating a Python package and uploading it to PyPI or Test PyPI isn't that complicated, but there are a few details I want to remember next time. Some of the steps below reflect my personal preferences and are not necessary.


## Creating a basic package

To create a package, do the following:

- Create a directory called `packagename` that has a structure akin to the below:

```
packagename/
├── LICENSE
├── pyproject.toml
├── README.md
│── packagename/
│   ├── __init__.py
│   └── example.py
└── tests/
```

- Add project descriptions to `README.md`

- Add the appropriate [text](https://choosealicense.com) to `LICENSE`
  
- Add the following contents to `pyproject.toml`:

```{toml}
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "packagename"
version = "0.0.1"
authors = [
  { name="Example Author", email="author@example.com" },
]
description = "Package description"
readme = "README.md"
requires-python = ">=3.7"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

[project.urls]
"Homepage" = "https://github.com/pypa/sampleproject"
"Bug Tracker" = "https://github.com/pypa/sampleproject/issues"

```

- Create a virtual environment: `python3.10 -m venv .venv`

- Activate the virtual environment: `source ./.venv/bin/activate`

- Initialise Git and create a GitHub repo [as usual](https://fabiangunzinger.github.io/git/) (only the files in `projectname\dist` get uploaded, so there is nothing special about the rest of the directory)

- Write some code to put in the package ...

- Install distribution and upload dependencies:

```
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine
```

- Build the package: `python3 -m build`
  
- Upload the build files to...
  - Test PyPI: `python3 -m twine upload --repository testpypi dist/*`
  - PyPI: `python3 -m twine upload dist/*`

- Done! You can now install your package using

  - `python -m pip install packagename` (from PyPI)
  - `python -m pip install --index-url https://test.pypi.org/simple/ --no-deps packagename` (from Test PyPI)


## Organising your package

I often want to organise the modules in my package into subpackages and submodules for additional structure. Something like the below:

```
packagename/
├── LICENSE
├── pyproject.toml
├── README.md
│── packagename/
|   |-- subpackage1
|   |   |-- __init.py__
|   |   |-- a.py
|   |   |-- b.py
|   |-- subpackage2
|   |   |-- __init.py__
|   |   |-- c.py
│   ├── __init__.py
└── tests/
```

and, if the content of `a.py` is:

```{python}
def a():
    return "Module a content"
```

I want to be able to import my package as `import packagename as p`, and then access function `a` in module `a` as `p.subpackage1.a`.

To be able to do that, the `__init.py__` in `packagename` needs to contain:

```{python}
from .subpackage1 import a
```

so that module `a` gets loaded into the namespace when I import the package, and `__init.py__` in `subpackage1` needs to contain

```{python}
from .a import a
```

so that function `a` gets loaded into the namespace when I import module `a`.


## Creating tokens for pypi and test pypi

When uploading packages to either Test PyPI or PyPI, the default behaviour of Twine is to ask for the username and passwort on the respective platform. A more secure and much easier way to verify your identity is to create a tocken in your user account, and save the details in your `~/.pypirc` file. Twine then automatically sources those details during the upload process.

Your `~/.pypirc` would look something like this:

```
[pypi]
  username = __token__
  password = pypi-someverylongkey

[testpypi]
  username = __token__
  password = pypi-someotherverylongkey
```


## Versioning

Making new versions of a package is so easy nobody even seems to bother to mention how it's done. So here are the steps:

- Make the desired changes in the code

- Change the `version` field in `pyproject.toml`

- Rebuild the package (see above for command)

- Upload build files (see above for command)


## Useful tools

There are a lot of packaging tools that automate some of the above. I've tried Poetry in the past, and [Hatch](https://hatch.pypa.io/latest/) this time. But I find that all these tools do many things I neither need nor understand. So, for the time being, I'll keep things simple and just follow the process above.


## Useful resources

- [Python docs](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

- [How to build your very first Python package](https://www.freecodecamp.org/news/build-your-first-python-package/)
