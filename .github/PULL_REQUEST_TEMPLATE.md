# Pull Request

## Summary

<!-- What does this PR change, and why? Link any related issue. -->

## Definition of Done (SaMD)

This kit holds contributions to the same Definition of Done it asks downstream
devices to meet. Check each box honestly; a contribution is not "done" until all
apply (or are explicitly justified as N/A).

- [ ] **Tests pass with numbers reported.** I ran the relevant test suites and pasted the actual counts below (e.g. `X passed, Y skipped`). "It renders / it builds" is not a test.
- [ ] **No tracebacks or technical errors leak to the end user.** Failure paths degrade safely and predictably, with clear, empathetic messages — never raw stack traces, SQL, or internal metadata.
- [ ] **Documentation traceability (DHF) is updated in this same PR.** Changes to clinical logic, schemas, business rules, or security flows are reflected in the relevant Design History File documents — not deferred to a later sprint.
- [ ] **Impact analysis done.** I searched for every consumer of any symbol, parameter, schema, return value, or constant I changed, and updated them all (not only the file where the change started).
- [ ] **Identity comes only from the verified token.** No user/subject identity is read from request body or query parameters.
- [ ] **Boy Scout rule applied.** I left the touched files at least as clean as I found them (dead imports, stray `any`, oversized functions).
- [ ] I have read and followed [CONTRIBUTING.md](../CONTRIBUTING.md).

## Test Evidence

<!-- Paste the actual command(s) and the resulting numbers. -->

```
# e.g. pytest -q  ->  123 passed
# e.g. vitest run ->  456 passed
```

## Impact Analysis

<!-- Which symbols/files/consumers were affected, and how you confirmed they were all updated. -->

## Traceability / DHF Notes

<!-- Which DHF documents, requirements, or risk-matrix entries this PR touches, if any. -->
