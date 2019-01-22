# Gate service

## Testing

Run the following command to automagically setup virtual env and run all available tests:

```
  $ ./gmanager up test
```

*Note:* This should work under Linux and Windows.

The test results will be saved into `test-results/gate_service.xml`
All test should have names in format `test_*.py` and be placed somewhere inside `tests` folder.