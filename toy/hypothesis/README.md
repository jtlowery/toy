### Very brief overview
- Property-based testing
    - Describe a set of rules for generating random example data
    - Operate on examples
    - Test that expected properties hold true

- Basic usage
    - Use the hypothesis.given decorator to pass generated data inputs to tests
    - Use strategies in hypothesis.strategies to define a range of example values to generate
        - filter can be used to rule out values in that range
    - Use hypothesis.example decorator to ensure a certain value is passed
    - Use hypothesis.event to record an event (as str) in statistics
    
    
- Building more complex examples
    - Use hypothesis.strategies.builds to pass strategies as args to a callable
    - Use the hypothesis.composite decorator where more complex logic needs to be expressed in a function (i.e. some relationship between example values)
        - Use hypothesis.assume to indicate an example not meeting a condition is invalid

- Misc.
    - Numpy and Pandas support in hypothesis.extra
    - Set hypothesis.seed for reproducibility

### Running
- run normally with pytest 
    - `py.test ./tests/hypothesis/test_random_funcs.py`
- run with statistics on examples generated 
    - `py.test --hypothesis-show-statistics ./tests/hypothesis/test_random_funcs.py`

### References
- [Package docs](https://hypothesis.readthedocs.io/en/latest/index.html)
- [Examples / walkthrough / discussion](https://hypothesis.works/articles/)