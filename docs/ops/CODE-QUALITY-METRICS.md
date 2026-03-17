# Code Quality Metrics

## Overview
Faintech Lab uses automated code quality metrics to ensure maintainability, reliability, and test coverage across all code contributions.

## Test Coverage Thresholds

We enforce test coverage thresholds using Vitest with v8 coverage provider. All code must meet the following minimum coverage standards before being considered production-ready:

### Coverage Requirements

| Metric | Threshold | Rationale |
|---------|-----------|-----------|
| **Statements** | 75% | Core code paths must be tested |
| **Functions** | 75% | All public functions should have tests |
| **Branches** | 70% | Conditional logic should be exercised |
| **Lines** | 75% | Practical line-level coverage |

### Implementation

Coverage is enforced via:

1. **Configuration**: `vitest.config.ts` defines thresholds
2. **CI Enforcement**: Coverage reports run on `npm run test:coverage`
3. **Failure**: Failing thresholds blocks merge/review

### Rationale

- **75% overall** balances quality with rapid experimentation velocity
- **70% branches** acknowledges complex conditionals are harder to test fully
- Enables rapid iteration without sacrificing reliability
- Aligns with industry standards for R&D environments

### Exceptions

Exception requests must include:
1. Justification for lower coverage
2. Plan to improve coverage
3. Approval from tech lead

## Measuring Coverage

Run coverage report:

```bash
npm run test:coverage
```

This generates:
- Console output with coverage summary
- `coverage/coverage-final.json` (machine-readable)
- `coverage/index.html` (visual report)

## Related

- Testing Strategy: TBD
- Quality Gates: TBD
- CI/CD Pipeline: TBD

---

**Last Updated**: 2026-03-16
**Owner**: ops (Faintech Lab)
