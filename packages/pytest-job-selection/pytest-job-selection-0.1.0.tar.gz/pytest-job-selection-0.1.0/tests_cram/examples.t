Make the plugin available in the python path:

  $ export ROOT=$TESTDIR/../
  $ export PYTHONPATH=$ROOT
  $ . $TESTDIR/cram.inc.sh
  $ cd $ROOT

Make example tests run quickly:

  $ export QUICK=1

Try job selection without timings:

  $ _pytest --collect-only --quiet --job 1/2 example/example_test.py
  (job selection: 1/2 with 0 timings from None)
  example/example_test.py::TestExampleA::test_a
  example/example_test.py::TestExampleC::test_c
  
  $ _pytest --collect-only --quiet --job 2/2 example/example_test.py
  (job selection: 2/2 with 0 timings from None)
  example/example_test.py::TestExampleB::test_b
  example/example_test.py::TestExampleD::test_d
  
  $ _pytest -v --no-header --job 1/2 example/example_test.py
  ============================= test session starts ==============================
  collecting ... (job selection: 1/2 with 0 timings from None)
  collected 4 items
  
  example/example_test.py::TestExampleA::test_a PASSED                     [ 50%]
  example/example_test.py::TestExampleC::test_c PASSED                     [100%]
  
  $ _pytest -v --no-header --job 2/2 example/example_test.py
  ============================= test session starts ==============================
  collecting ... (job selection: 2/2 with 0 timings from None)
  collected 4 items
  
  example/example_test.py::TestExampleB::test_b PASSED                     [ 50%]
  example/example_test.py::TestExampleD::test_d PASSED                     [100%]
  

Try job selection with timings:

  $ _pytest -v --no-header --prev-junit-xml example/junit.xml --job 1/2 example/example_test.py
  ============================= test session starts ==============================
  collecting ... (job selection: 1/2 with 4 timings from example/junit.xml)
  collected 4 items
  
  example/example_test.py::TestExampleA::test_a PASSED                     [ 50%]
  example/example_test.py::TestExampleB::test_b PASSED                     [100%]
  
  $ _pytest -v --no-header --prev-junit-xml example/junit.xml --job 2/2 example/example_test.py
  ============================= test session starts ==============================
  collecting ... (job selection: 2/2 with 4 timings from example/junit.xml)
  collected 4 items
  
  example/example_test.py::TestExampleC::test_c PASSED                     [ 50%]
  example/example_test.py::TestExampleD::test_d PASSED                     [100%]
  

Inspect the dry run:

  $ _pytest -v --no-header --prev-junit-xml example/junit.xml --job 1/2 --jobs-dry-run example/example_test.py
  ============================= test session starts ==============================
  collecting ... (job selection: 1/2 with 4 timings from example/junit.xml)
  dry run
  Jobs: weight and contents
  job       weight   #classes
  1        0:00:03          2
  2        0:00:03          2
  
  Jobs: weight and full contents
  job                                  class    weight
  1        example.example_test.TestExampleB   0:00:02
  1        example.example_test.TestExampleA   0:00:01
  2        example.example_test.TestExampleD   0:00:02
  2        example.example_test.TestExampleC   0:00:01
  
  Jobs: statistics
  jobs_total        weight: avg       min       max   #classes: avg   min   max
  jobs_total=2          0:00:03   0:00:03   0:00:03             2.0     2     2
  Can add 0:00:00 without increasing wall-time.
  
  Slowest classes (top 10):
  weight                                   class
  0:00:02      example.example_test.TestExampleB
  0:00:02      example.example_test.TestExampleD
  0:00:01      example.example_test.TestExampleA
  0:00:01      example.example_test.TestExampleC
  
  Would run test classes in job 1/2:
  class                                   weight
  example.example_test.TestExampleB      0:00:02
  example.example_test.TestExampleA      0:00:01
  
  collected 4 items
  
