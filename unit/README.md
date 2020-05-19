# testing

`unit_helper.py`
- sets up the python system path so it will find this version of
`httperfpy.py` before any others installed on the system.
- imports httperfpy
- defines inputs and expected results for tests

`httperf_unit.py`
- tests executing `httperf` instances

`parser_unit.py`
- tests the parser instances

`input-data` - this directory holds httperf output generated with
the `httperf` `--print-reply header` option. there are three files.
- `short` - short file useful for interactive testing
- `long` - used by `parser_unit.py`. the first x-trace header's sample flag has been set to 0.
- `giant` - 3000 headers, useful for benchmarking the parser.
