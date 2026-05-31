## Summary

What changed?

## Workflow / User Impact

Which maintainer workflow does this improve?

## Safety Notes

- [ ] Does not commit secrets or private runtime files
- [ ] Keeps risky behavior explicit and opt-in
- [ ] Does not broaden default filesystem access

## Validation

```text
python -m compileall .
python smoke_tests.py
```

## Screenshots or Transcript

Optional. Redact tokens, user IDs, private paths, and repository secrets.
