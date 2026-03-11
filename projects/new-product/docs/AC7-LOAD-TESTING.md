# AC7: Load Testing & Performance Validation

**Task ID:** AC7 (part of AMC-MVP-117)
**Owner:** faintech-qa
**Deadline:** 2026-03-20 (4 days before launch)
**Status:** in_progress
**Priority:** P1

## Context

Load testing was executed on 2026-03-11 with k6 scripts (see PERFORMANCE-REPORT.md):
- ✅ Throughput: 434 req/s (exceeds 100 req/s target)
- ✅ P99 latency: ~70ms (exceeds <200ms target)
- ✅ P95 latency: ~58ms (exceeds <100ms target)
- ❌ Error rate: 80% (target: <0.1%) - root cause: missing auth in test scripts
- ⚠️ Memory usage: Not measured
- ⚠️ Database stability: Not verified

## Acceptance Criteria

From LAUNCH-DAY-CHECKLIST.md + MONITORING-SPEC.md:

1. **Fix Test Authentication** (P1 blocker from PERFORMANCE-REPORT.md)
   - Add JWT token flow to all k6 test scripts
   - Create test user/agent in setup phase
   - Include valid API key headers for protected endpoints
   - Source: `/Users/eduardgridan/faintech-lab/projects/new-product/tests/load/`

2. **Re-run Authenticated Load Tests** (P1)
   - Execute load_test.js with auth enabled
   - Execute spike_test.js with auth enabled
   - Verify error rate < 0.1% (target from MONITORING-SPEC.md)
   - Confirm sustained 100 req/sec without degradation

3. **Validate Performance Thresholds** (P1)
   - P99 latency < 200ms ✅ (already met, verify with auth)
   - P95 latency < 100ms ✅ (already met, verify with auth)
   - Error rate < 0.1% ❌ (requires auth fix, must pass)
   - Memory usage < 2GB (add monitoring to test)
   - Database connection pool stable under load

4. **Scale Test** (P2)
   - Test with 1000+ concurrent users (currently tested 100)
   - Verify system handles 10x traffic spike (launch day expectation)
   - Confirm no crashes, memory leaks, or connection exhaustion

5. **Document Final Results** (P1)
   - Update PERFORMANCE-REPORT.md with authenticated test results
   - Include memory usage metrics
   - Document database connection pool behavior
   - Confirm all acceptance criteria with evidence

## Test Scripts (existing, need auth fixes)

```
/Users/eduardgridan/faintech-lab/projects/new-product/tests/load/
├── load_test.js       # Main load test (100 concurrent, 30s)
├── spike_test.js      # Spike test (1,263 req/s in 15s)
└── rate_limit_test.js  # Rate limit validation
```

## Success Criteria (from LAUNCH-DAY-CHECKLIST.md)

- [ ] Load testing complete — Confirmed 100 req/sec without degradation
- [ ] All performance thresholds met (P99 < 200ms, P95 < 100ms, error rate < 0.1%)
- [ ] Memory usage stable under load (< 2GB)
- [ ] Database connection pool stable (no exhaustion)
- [ ] Performance report documented (PERFORMANCE-REPORT.md updated)

## Dependencies

- Backend auth endpoints working (AMC-MVP-109: JWT Auth ✅ complete)
- Test database with seeded data (agent_id, task_id for memories)
- Valid JWT token generation for test user

## Risk

**High Error Rate Root Cause:** Test scripts hit protected endpoints without auth headers
**Mitigation:** Add authentication flow to k6 scripts before re-running tests

## Timeline

- **2026-03-11:** Fix test scripts with authentication
- **2026-03-12:** Re-run authenticated load tests
- **2026-03-13:** Validate all thresholds, measure memory/DB stability
- **2026-03-14:** Update PERFORMANCE-REPORT.md with final results
- **2026-03-15-16:** Buffer for fixes if thresholds not met
- **2026-03-20:** Deadline (4 days before launch)

---

**Created:** 2026-03-11T11:10:00Z
**Owner:** faintech-qa
**Review Required:** faintech-cto (technical), faintech-pm (coordination)
