---
title: Testing and validating
date: '2021-08-12'
tags:
  - 'python, datascience'
execute:
  enabled: false
---


Notes on testing and data validation.

What I currently do:

-   I use `assert` to test small ad-hoc pieces of code, `pytest` to test crucial pieces of code, and a series of validating functions that check certain assumptions about the data

What I need:

-   A process to ensure that my data preprocessing pipeline produces the intended data.

-   I still don't fully understand how good data scientists test their code. Unit testing seems incomplete because while it ensures that a piece of code works as expected, the main challenge when working with large datasets is often that there are special cases in the data that I don't know in advance and can't think of. To catch these, I need to perform tests on the full data. In addition to that, manually creating a dataframe for testing is a huge pain when I need to test functions that create more complex data patterns (e.g. checking whether, in a financial transactions dataset, certain individuals in the data have a at least a certain number of monthly transactions for a certain type of bank account).

-   I currently mainly use validating functions that operate on the entire dataset at the end of the pipeline (e.g. transaction data production in entropy project), which already has proven invaluable in catching errors. Using a decorator to add each validator function to a list of validators, and then running the data through each validator in that list works well and is fairly convenient.

-   `pandera` seems potentially useful in that the defined schema can be used both to validate data and -- excitingly -- can also be used to generate sample datasets for `hypothesis` and `pytest`, which could go a long way towards solving the above problem. But specifying a data schema for a non-trivial dataset is not easy, and I can't see how to write one for a dataset like MDB, where I need constraints such as a certain number of financial accounts of a certain type per user. So, for now, I just use my own validation functions. The testing branch in the entropy project has a `schema.py` file that expriments with the library.

-   [This](https://www.peterbaumgartner.com/blog/testing-for-data-science/?utm_campaign=Data_Elixir&utm_source=Data_Elixir_368/) article has been very useful, suggesting the following approach to testing: `assert` statements for ad-hoc pieces of code in Jupyter Lab, `pytest` for pieces of code others user, `hypothesis` for code that operates on the data, and `pandera` or other validator libraries for overall data validation. I basically do the first and last of these, and am still looking for ways to do

## `pytest` notes

### Basic test for return value

``` python
def convert_to_int(s):
    return int(s.replace(",", ""))
```

Very basic test

``` python
def test_convert_to_int():
    assert convert_to_int("1,200") == 1200
```

More transparent test with message, which will show when AssertionError is raised

``` python
def test_convert_to_int():
    actual = convert_to_int("1,200")
    expected = 1200
    message = f"convert_to_int('1,200') returned {actual} instead of {expected}."
    assert actual == expected, message
```

Careful with floats: because of this:

``` python
0.1 + 0.1 + 0.1 == 0.3
```

    False

Use this:

``` python
0.1 + 0.1 + 0.1 == pytest.approx(0.3)
```

    True

### Testing for exceptions

Use context manager that silences expected error if raised within context and raises an assertion error if expected error isn't raised.

``` python
with pytest.raises(ValueError):
    raise ValueError
```

``` python
with pytest.raises(ValueError):
    pass
```

<pre><span class="ansi-red-fg">---------------------------------------------------------------------------</span>
<span class="ansi-red-fg">Failed</span>                                    Traceback (most recent call last)
<span class="ansi-green-fg">/var/folders/xg/n9p73cf50s52twlnz7z778vr0000gn/T/ipykernel_3961/1768107249.py</span> in <span class="ansi-cyan-fg">&lt;module&gt;</span>
<span class="ansi-green-fg ansi-bold">      1</span> <span class="ansi-green-fg">with</span> pytest<span class="ansi-blue-fg">.</span>raises<span class="ansi-blue-fg">(</span>ValueError<span class="ansi-blue-fg">)</span><span class="ansi-blue-fg">:</span>
<span class="ansi-green-fg">----&gt; 2</span><span class="ansi-red-fg">     </span><span class="ansi-green-fg">pass</span>

    <span class="ansi-red-fg">[... skipping hidden 1 frame]</span>

<span class="ansi-green-fg">~/miniconda3/envs/blog/lib/python3.9/site-packages/_pytest/outcomes.py</span> in <span class="ansi-cyan-fg">fail</span><span class="ansi-blue-fg">(msg, pytrace)</span>
<span class="ansi-green-fg ansi-bold">    151</span>     """
<span class="ansi-green-fg ansi-bold">    152</span>     __tracebackhide__ <span class="ansi-blue-fg">=</span> <span class="ansi-green-fg">True</span>
<span class="ansi-green-fg">--&gt; 153</span><span class="ansi-red-fg">     </span><span class="ansi-green-fg">raise</span> Failed<span class="ansi-blue-fg">(</span>msg<span class="ansi-blue-fg">=</span>msg<span class="ansi-blue-fg">,</span> pytrace<span class="ansi-blue-fg">=</span>pytrace<span class="ansi-blue-fg">)</span>
<span class="ansi-green-fg ansi-bold">    154</span> 
<span class="ansi-green-fg ansi-bold">    155</span> 

<span class="ansi-red-fg">Failed</span>: DID NOT RAISE &lt;class 'ValueError'&gt;</pre>

Basic example:

``` python
def incrementer(x):
    if isinstance(x, int):
        return x + 1
    elif isinstance(x, str):
        raise TypeError("Please enter a number")


def test_valueerror_on_string():
    example_argument = "hello"
    with pytest.raises(TypeError):
        incrementer(example_argument)


test_valueerror_on_string()
```

Test for correct error message

``` python
def test_valueerror_on_string():
    example_argument = "hello"
    with pytest.raises(TypeError) as exception_info:
        incrementer(example_argument)
    assert exception_info.match("Please enter a number")


test_valueerror_on_string()
```

### What's a "well-tested" function?

Argument types:
- Bad arguments
- Examples: incomplete args, wrong dimensions, wrong type, etc.
- Return value: exception
- Special arguments
- Examples: values triggering special logic, boundary value (value between bad and good arguments and before or after values that raise special logic)
- Return value: expected value
- Normal arguments
- Examples: All other values, test 2 or 3
- Return value: expected value

### Keeping tests organised

Principles to follow:

-   Mirror structure of `src` directory in `tests` directory
-   Name test modules as `test_<name of src module>`
-   Within test module, collect all tests for a single function in a class named `TestNameOfFunction` (from DataCamp: 'Test classes are containers inside test modules. They help separate tests for different functions within the test module, and serve as a structuring tool in the pytest framework.')

``` python
# test class layout


class TestNameOfFunction(object):
    def test_first_thing(self):
        pass

    def test_second_thing(self):
        pass
```

### Marking tests as expected to fail

Sometimes we might want to differentiate between failing code and tests that we know won't run yet or under certain conditions (e.g. we might follow TDD and haven't written a test yet, or we know a function only runs in Python 3). In this case, we can apply decorators to either functions or classes

Expect to fail always (e.g. because not implemented yet)

``` python
class TestNameOfFunction(object):
    @pytest.mark.xfail
    def test_first_thing(self):
        pass

    @pytest.mark.xfail(reason="Not implemented yet.")
    def test_first_thing(self):
        """With optional reason arg."""
        pass


# or


@pytest.mark.xfail(reason="Not implemented yet.")
class TestNameOfFunction(object):
    def test_first_thing(self):
        pass

    def test_first_thing(self):
        """With optional reason arg."""
        pass
```

Expect to fail under certain conditions (e.g. certain Python versions, operating systems, etc.).

``` python
import sys


class TestNameOfFunction(object):
    @pytest.mark.skipif(sys.version_info < (3, 0), reason="Requires Python 3")
    def test_first_thing(self):
        """Only runs in Python 3."""
        pass


# or


@pytest.mark.skipif(sys.version_info < (3, 0), reason="Requires Python 3")
class TestNameOfFunction(object):
    def test_first_thing(self):
        """Only runs in Python 3."""
        pass
```

### Running pytests

-   `pytest` runs all tests
-   `pytest -x` stops after first failure
-   `pytest <path to test module>` runs all tests in test module
-   `pytest <path to test module>::<test class name>` runs all tests in test module with specified node id
-   `pytest <path to test module>::<test class name>::<test name>` runs test with specified node id
-   `pytest -k <patter>` runds tests that fit pattern
    -   `pytest -k <TestNameOfFunction>` runs all tests in specified class
    -   `pytest -k <NameOf and not second thing>` runs all tests in specified class except for `test_second_thing`
-   `pytest -r` show reasons
-   `pytest -rs` show reasons for skipped tests
-   `pytest -rx` show reasons for xfailed tests
-   `pytest -rsx` show reasons for skipped and xfailed

### Fixtures

``` python
# create raw and clean data files in fixture
@pytest.fixture
def raw_and_clean_data():
    raw_path = "raw.csv"
    clean_path = "clean.csv"
    with open(raw_path, "w") as f:
        f.write("1000, 40\n" "2000, 50\n")
    yield raw_path, clean_path

    # teardown code so we start with clean env in next test
    os.remove(raw_path)
    os.remove(clean_path)


# use fixture in test
def test_on_raw_data(raw_and_clean_data):
    raw_path, clean_path = raw_and_clean_data
    preprocess(raw_path, clean_path)
```

Useful alternative using `tempdir()` and fixture chaining:

``` python
@pytest.fixture
def raw_and_clean_data(tempdir):
    raw_path = tempdir.join("raw.csv")
    clean_path = tempdir.join("clean.csv")
    with open(raw_path, "w") as f:
        f.write("1000, 40\n" "2000, 50\n")
    yield raw_path, clean_path

    # no teardown needed
```

<pre><span class="ansi-red-fg">---------------------------------------------------------------------------</span>
<span class="ansi-red-fg">NameError</span>                                 Traceback (most recent call last)
<span class="ansi-green-fg">/var/folders/xg/n9p73cf50s52twlnz7z778vr0000gn/T/ipykernel_2101/1056953037.py</span> in <span class="ansi-cyan-fg">&lt;module&gt;</span>
<span class="ansi-green-fg">----&gt; 1</span><span class="ansi-red-fg"> </span><span class="ansi-blue-fg">@</span>pytest<span class="ansi-blue-fg">.</span>fixture
<span class="ansi-green-fg ansi-bold">      2</span> <span class="ansi-green-fg">def</span> raw_and_clean_data<span class="ansi-blue-fg">(</span>tempdir<span class="ansi-blue-fg">)</span><span class="ansi-blue-fg">:</span>
<span class="ansi-green-fg ansi-bold">      3</span>     raw_path <span class="ansi-blue-fg">=</span> tempdir<span class="ansi-blue-fg">.</span>join<span class="ansi-blue-fg">(</span><span class="ansi-blue-fg">'raw.csv'</span><span class="ansi-blue-fg">)</span>
<span class="ansi-green-fg ansi-bold">      4</span>     clean_path <span class="ansi-blue-fg">=</span> tempdir<span class="ansi-blue-fg">.</span>join<span class="ansi-blue-fg">(</span><span class="ansi-blue-fg">'clean.csv'</span><span class="ansi-blue-fg">)</span>
<span class="ansi-green-fg ansi-bold">      5</span>     <span class="ansi-green-fg">with</span> open<span class="ansi-blue-fg">(</span>raw_path<span class="ansi-blue-fg">,</span> <span class="ansi-blue-fg">'w'</span><span class="ansi-blue-fg">)</span> <span class="ansi-green-fg">as</span> f<span class="ansi-blue-fg">:</span>

<span class="ansi-red-fg">NameError</span>: name 'pytest' is not defined</pre>

### Mocking

Testing functions independently of dependencies

### Testing models

To test models, use toy datasets for which I know the correct results and perform sanity-checks using assertions I can know.

Tests for training function

``` python
from models import train_model


def test_on_linear_data():
    """Can easily predict results precisely."""
    test_arg = np.array([[1, 3], [2, 5], [3, 7]])
    expected_slope = 2
    expected_intercept = 1

    slope, intercept = train_model(test_arg)
    assert slope == pytest.approx(expected_slope)
    assert intercept == pytest.approx(expected_intercept)


def test_on_positively_correlated_data():
    """Cannot easily predict result precisely,
    but can still assert that slope is positive
    as a sanity-check.
    """
    test_arg = np.array([[1, 4], [2, 3], [4, 8], [3, 7]])
    slope, intercept = train_model(test_arg)
    assert slope > 0
```

Tests for final model

``` python
def model_test(test_set, slope, intercept):
    """Assert that R^2 is between 0 and 1."""
    rsq = ...
    assert 0 <= rsq <= 1
```

### Testing plots

Overall approach:
1. Create baseline plot using plotting function and store as PNG image
2. Test plotting function and compare to baseline

Install `pytest-mpl`

``` python
def plot_best_fit_line(slope, intercept, x_array, y_array, title):
    """Plotting function to be tested."""
    pass


@pytest.mark.mpl_image_compare
def test_plot_for_linear_data():
    """Testing function.
    Under the hood, creates baseline and comparisons.
    """
    slope = 2
    intercept = 1
    x_array = np.array([1, 2, 3])
    y_array = np.array([3, 5, 7])
    title = "Test plot for linear data"
    return plot_best_fit_line(slope, intercept, x_array, y_array, title)
```

baseline image needs to be stored in `baseline` subfolder of the plot module testing directory.

To create baseline image, do following:

`>pytest -k 'test_plot_for_linear_data' --mpl-generate-path <path-to-baseline-folder>`

To compare future tests with baseline image run:

`> pytest -k 'test_plot_for_linear_data' --mpl`

## CI

-   [Travis CI](https://www.travis-ci.com)

-   [Python stuff](https://docs.travis-ci.com/user/languages/python/)

-   [Using Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/use-conda-with-travis-ci.html)

-   [Travis CI build info](https://app.travis-ci.com/github/fabiangunzinger/entropy/jobs/545437220)

## Resources

-   [Peter Baumgartner, Ways I use testing as a data scientist](https://www.peterbaumgartner.com/blog/testing-for-data-science/?utm_campaign=Data_Elixir&utm_source=Data_Elixir_368/)
-   [Code from DataCamp course](https://github.com/gutfeeling/univariate-linear-regression)
