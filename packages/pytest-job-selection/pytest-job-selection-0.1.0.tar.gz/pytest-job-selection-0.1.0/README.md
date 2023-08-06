pytest-job-selection
====================

[![PyPI version](https://img.shields.io/pypi/v/pytest-job-selection.svg)](https://pypi.org/project/pytest-job-selection)

[![Python versions](https://img.shields.io/pypi/pyversions/pytest-job-selection.svg)](https://pypi.org/project/pytest-job-selection)

`pytest-job-selection` is a
[pytest](https://github.com/pytest-dev/pytest) plugin for load
balancing test suites. In short, it provides a new pytest argument
`--job` such that running `pytest --job X/Y` (where `1 <= X <= Y`)
groups the selected tests in `Y` jobs, and then executes the tests of
job `X`. Jobs are balanced by using a JUnit XML file as a previous
recording of test run times.

This enables convenient parallel execution of large pytest suites in CIs
such as [GitLab CI](https://docs.gitlab.com/ee/ci/) using [parallel
jobs](https://docs.gitlab.com/ee/ci/jobs/job_control.html#parallelize-large-jobs).
See below for details on [GitLab CI integration](#gitlab-ci-integration)

This plugin is inspired by a similar functionality in
[Tezt](https://gitlab.com/nomadic-labs/tezt), an OCaml test framework.

Features
--------

-   Adds a `--job` pytest argument that executes a subset of selected
    test.
-   Adds a `--prev-junit-xml <junit.xml>` pytest argument. When
    supplied, the plugin heuristically attempts to balance test jobs
    using a greedy knapsack algorithm into jobs of even runtime, using
    the timing information in `junit.xml`.
-   Adds a `--jobs-dry-run` pytest argument that outputs debug
    information on test balancing.

Requirements
------------

-   [pytest](https://github.com/pytest-dev/pytest)
-   [typing_extensions](https://pypi.org/project/typing-extensions/)

In addition, [cram](https://bitheap.org/cram/) is used to test the
plugin.

Installation
------------

You can install `pytest-job-selection` via
[pip](https://pypi.org/project/pip/) from
[PyPI](https://pypi.org/project):

    $ pip install pytest-job-selection

Usage
-----

The following command should suffice for most use cases:

    pytest --prev-junit-xml junit.xml --job X/Y [tests...]

This will group selected tests into `Y` jobs. It uses a
[Balancing heuristic](#balancing-heuristic) to group selected
tests, based on the previously recorded timing information in the
JUnit XML file `junit.xml`. It then executes all tests in job `X`. Jobs
are 1-indexed, so that job `1` is the first job and job `Y` is the last
one. In other words, executing:

    pytest --prev-junit-xml junit.xml --job 1/Y [tests...]
    pytest --prev-junit-xml junit.xml --job 2/Y [tests...]
    ...
    pytest --prev-junit-xml junit.xml --job Y/Y [tests...]

Will execute the same tests as:

    pytest [tests...]

### JUnit XML files

See the [pytest
documentation](https://docs.pytest.org/en/6.2.x/usage.html#creating-junitxml-format-files)
for more information on JUnit XML files.
In short, an JUnit XML can be obtained file by executing a test suite with the
`--junitxml=junit.xml` argument:

    pytest --junitxml=junit.xml [tests...]

If a `junit.xml` is not provided using `--prev-junit-xml`, then the
batching heuristic will assume that all test classes have the same
running time, and will attempt to create batches with a balanced number
of test classes.

### Dry run

You can to simulate balancing run with the `--jobs-dry-run --job X/Y`
flag. This will collect and group tests, and then output:

 - The list of jobs with:
     - `weight`: the sum of the runtime of all the test classes in
         that job as per the previously recorded timing information
     - `#classes`: the number of test classes in this job
 - The full list of test classes with sorted by job appartenance and
   the weight of that test class (the weight of the class is sum of
   the running time of all test classes in that class as per the
   previously recorded timing information)

 - Job statistics, including:
     - the total number of jobs;
     - the minimum, maximum and average job weight;
     - the minimum, maximum and average number of classes per job.

 - The test classes of the currently selected jobs and their weight.

 - A list of *orphaned* test classes. These are test classes that
   appear in the JUnit XML file supplied with `--prev-junit-xml` but
   which does not correspond to any selected test. The presence of
   orphans indicates that the JUnit XML file may be out of date, but
   it will not impact balancing.

A Worked Example
----------------

We will use a simple dummy test
[example/example_test.py](example/example_test.py):

```python
from time import sleep

class TestExampleA:
    def test_a(self):
        sleep(1)

class TestExampleB:
    def test_b(self):
        sleep(2)

class TestExampleC:
    def test_c(self):
        sleep(1)

class TestExampleD:
    def test_d(self):
        sleep(2)
```

This module contains four test classes that do nothing but sleep for a
given period of time. We can try run these tests in two jobs without
giving the job selection plugin any previous timings on which to base
balancing:

    $ pytest --job 1/2 example/example_test.py -v
    example/example_test.py::TestExampleA::test_a PASSED [ 50%]
    example/example_test.py::TestExampleC::test_c PASSED [100%]
    $ pytest --job 2/2 example/example_test.py -v
    example/example_test.py::TestExampleB::test_b PASSED [ 50%]
    example/example_test.py::TestExampleD::test_d PASSED [100%]

This groups `TestExampleA` with `TestExampleC` and `TestExampleB` with
`TestExampleD`. Each job contains an even number of job, but the jobs
are unbalanced, as the first job will run in \~2 seconds while the
second will run in \~4 seconds.

Note that you can preview the balancing using the pytest argument
`--collect-only` (here in addition to the `--quiet` flag for terse
output):

    $ pytest --job 1/2 example/example_test.py --collect-only --quiet
    (job selection: 1/2 with 4 timings from junit.xml)
    example/example_test.py::TestExampleA::test_a
    example/example_test.py::TestExampleB::test_b

    4 tests collected in 0.01s
    $ pytest --job 2/2 example/example_test.py --collect-only --quiet
    (job selection: 2/2 with 4 timings from junit.xml)
    example/example_test.py::TestExampleC::test_c
    example/example_test.py::TestExampleD::test_d

    4 tests collected in 0.01s

To even out the jobs based on the expected runtime of individual test
classes, we record a `junit.xml` file:

    $ pytest --junitxml=junit.xml example/example_test.py

We can inspect `junit.xml` and verify that it contains the expected
timings:

```xml
<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="pytest" errors="0" failures="0" skipped="0" tests="4" time="6.040">
    <testcase classname="example.example_test.TestExampleA" name="test_a" time="1.002"/>
    <testcase classname="example.example_test.TestExampleB" name="test_b" time="2.002"/>
    <testcase classname="example.example_test.TestExampleC" name="test_c" time="1.003"/>
    <testcase classname="example.example_test.TestExampleD" name="test_d" time="2.004"/>
  </testsuite>
</testsuites>
```

And then feed the recording into the plugin:

    $ pytest --prev-junit-xml junit.xml --job 1/2 example/example_test.py -v
    example/example_test.py::TestExampleA::test_a PASSED [ 50%]
    example/example_test.py::TestExampleD::test_d PASSED [100%]
    $ pytest --prev-junit-xml junit.xml --job 2/2 example/example_test.py -v
    example/example_test.py::TestExampleB::test_b PASSED [ 50%]
    example/example_test.py::TestExampleC::test_c PASSED [100%]

This time, `TestExampleA` is grouped with `TestExampleD` and
`TestExampleB` is grouped with `TestExampleC`, giving both jobs an
expected runtime of \~3 seconds each.

Finally, we can do a dry run to obtain an overview of the obtained
balancing:

    $ pytest --prev-junit-xml junit.xml --job 2/2 --jobs-dry-run example/example_test.py
    collecting ... (job selection: 2/2 with 4 timings from junit.xml)
    dry run
    Jobs: weight and contents
    job       weight   #classes
    1        0:00:03          2
    2        0:00:03          2

    Jobs: weight and full contents
    job                                  class    weight
    1        example.example_test.TestExampleD   0:00:02
    1        example.example_test.TestExampleA   0:00:01
    2        example.example_test.TestExampleB   0:00:02
    2        example.example_test.TestExampleC   0:00:01

    Jobs: statistics
    jobs_total        weight: avg       min       max   #classes: avg   min   max
    jobs_total=2          0:00:03   0:00:03   0:00:03             2.0     2     2
    Can add 0:00:00.001000 without increasing wall-time.

    Slowest classes (top 10):
    weight                                   class
    0:00:02      example.example_test.TestExampleD
    0:00:02      example.example_test.TestExampleB
    0:00:01      example.example_test.TestExampleC
    0:00:01      example.example_test.TestExampleA

    Would run test classes in job 2/2:
    class                                   weight
    example.example_test.TestExampleB      0:00:02
    example.example_test.TestExampleC      0:00:01

Balancing Heuristic
-------------------

The balancing heuristic is based on a greedy solution to the knapsack
problem. Each test class that is missing a previously recorded run time
provided through `--prev-junit-xml` will be assigned a default runtime
of 1 minute. If no previously recorded run times are provided, then this
applies to all test classes, and consequently the heuristic will balance
jobs based only on the number of assigned test classes (i.e., attempting
to create jobs whose number of test classes are close to each other).

GitLab CI integration
---------------------

This plugin can conveniently be used in [GitLab
CI](https://docs.gitlab.com/ee/ci/) to exploit [parallel
jobs](https://docs.gitlab.com/ee/ci/jobs/job_control.html#parallelize-large-jobs).

For instance, to parallelize a job like:

```yaml
pytest:
  script:
    - pytest tests/
```

Install the plugin in the CI, make sure that a `junit.xml` is available
in the repository at e.g. `tests/junit.xml` and change the job to:

```yaml
pytest:
  parallel: 10
  script:
    - pytest --prev-junit-xml tests/junit.xml --job ${CI_NODE_INDEX}/${CI_NODE_TOTAL}
      "--junitxml=reports/report_${CI_NODE_INDEX}_${CI_NODE_TOTAL}.xml"
      tests/
  artifacts:
    paths:
      - reports
    when: always
```

This will split the pytest job into 10 parallel jobs. The `--junitxml`
argument has also been added to the pytest command so that new JUnit
XML recordings are produced in the CI and then stored as artifacts
using the `artifacts` stanza.

This last points helps when rebalancing the tests, which you can now do
more easily by downloading the recordings from the CI. In the next
section, we describe the included script `scripts/jobs_fetch_reports.py`
that can be used to partially automate this process.

#### Retrieving JUnit XML files from GitLab CI

Updating the `junit.xml` file used for balancing quickly becomes a
hassle when the number of jobs grow. This plugin contains a script
`glci_jobs_fetch_reports` that can be used to this effect. For usage
information, call `glci_jobs_fetch_reports --help`.

Limitations
-----------

#### Test classes

This plugin balances tests at the granularity of modules or test
classes. All test cases of the same class will always execute in the
same job. Similarly, all test cases in a module that do not correspond
to class methods will execute in the same job.

#### Missing timings

If timings are missing for test case, then the balancer will silently
assume its running time is 1 minute.

#### Empty jobs

If there are more jobs than test classes or modules to balance, then at
least one job will be empty. In this case, `pytest` will
exit with a non-zero error code.

Contributing
------------

Contributions are very welcome. Tests can be run with
[tox](https://tox.readthedocs.io/en/latest/), please ensure the coverage
at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the
[MIT](http://opensource.org/licenses/MIT) license,
"pytest-job-selection" is free and open source software

Issues
------

If you encounter any problems, please [file an
issue](https://gitlab.com/arvidnl/pytest-job-selection/-/issues) along with
a detailed description.
