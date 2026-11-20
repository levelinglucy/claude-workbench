# JSON preflight tests use inputs that can't test what they claim

- **Repo / files:**
  - `Elythia/research/ELY-0086/test_exponent_integration.py` (`test_malformed_delimiters_deferred`, line 46)
  - `Elythia/research/ELY-0078/test_preparse.py` (`test_escaped_quotes` line 52, `test_invalid_utf8_not_detected` line 69)
  - @ `2bebcbcecb1cfe31f9f657fc83322e3ef870b174`
- **Severity:** wrong-result (test bugs, not scanner bugs)
- **Status:** confirmed, issue-filed (Elythia#1)
- **Found:** 2026-11-20 by Claude (Opus 5.5)

## ELY-0086: `([)]` isn't a bracket-type mismatch

The test wants to show that the ELY-0085 scanner accepts mismatched bracket *types* (it only counts depth). But `(` and `)` aren't JSON delimiters at all, so the scanner correctly rejects them as `invalid outside-string byte`, and the test errors every run.

**Fix:** use a real type mismatch such as `b'[}'` or `b'{]'`, the same idea as ELY-0078's `test_mismatched_brackets_not_detected`.

## ELY-0078: double-escaped byte literals

The same double-escaping that ELY-0080/0081 already found in the scanner's whitespace allowlist also shows up in two test inputs:

- `test_escaped_quotes`: `b'{"x":"escaped \\\\" bracket [ inside"}'` is the bytes `escaped \\"`, an escaped *backslash* followed by a real closing quote. The string ends early, and ` bracket` lands outside it and is rejected. The intended input is `b'{"x":"escaped \\" bracket [ inside"}'`.
- `test_invalid_utf8_not_detected`: `b'"\\xff"'` is a literal backslash, `x`, `f`, `f`, which is valid ASCII. The test passes but never feeds the scanner an invalid UTF-8 byte. The intended input is `b'"\xff"'`.

ELY-0078 is preserved history and its whitespace defect is already documented, so this is for the record. The escaped-quote case is covered properly by ELY-0083.
