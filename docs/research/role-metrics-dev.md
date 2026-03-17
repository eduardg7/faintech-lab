# Dev Role-Specific Metrics Framework

**Role:** Dev (Developer)
**Last Updated:** 2026-03-16
**Status:** Thresholds Documented in TASK_DB

---

## Overview

Dev metrics focus on measurable engineering productivity: tasks completed, code delivered via PRs, and code quality standards. These metrics reflect the core engineering work mode of "code → commits → PRs → tasks → completion".

## Metric Thresholds (TASK_DB Reference)

### 1. Tasks Completed
- **Metric ID:** `dev_tasks_completed_weekly`
- **Type:** Counter
- **Unit:** Tasks completed per week
- **Success Threshold:** ≥5 tasks/week
- **Warning Threshold:** 2-4 tasks/week
- **Critical Threshold:** <2 tasks/week
- **Data Source:** TASK_DB API: GET /api/company/tasks?owner=dev&status=done
- **Calculation:** COUNT(tasks WHERE owner='dev' AND status='done' AND completed_at >= today - 7d)
- **Notes:** Includes all task types (features, bugfixes, refactoring, docs)

### 2. PRs Merged
- **Metric ID:** `dev_prs_merged_daily`
- **Type:** Counter
- **Unit:** Pull requests merged per day
- **Success Threshold:** ≥2 PRs/day (healthy)
- **Warning Threshold:** 1 PR/day (minimum)
- **Critical Threshold:** 0 PRs/day (stalled)
- **Data Source:** GitHub API: GET /repos/{owner}/{repo}/pulls?state=closed
- **Calculation:** COUNT(pulls WHERE merged_at=today AND author_association=OWNER AND merged=true)
- **Notes:** Focus on code delivery velocity, not just PR creation

### 3. PR Merge Rate
- **Metric ID:** `dev_pr_merge_rate`
- **Type:** Percentage
- **Unit:** % of opened PRs merged
- **Success Threshold:** ≥80% merge rate
- **Warning Threshold:** 60-79% merge rate
- **Critical Threshold:** <60% merge rate
- **Data Source:** GitHub API: GET /repos/{owner}/{repo}/pulls?state=all
- **Calculation:** (merged_prs / opened_prs) * 100 WHERE created_at >= today - 7d
- **Notes:** Low merge rate indicates quality issues, review bottlenecks, or poor scoping

### 4. Code Quality (Test Coverage)
- **Metric ID:** `dev_test_coverage_percent`
- **Type:** Percentage
- **Unit:** % of code covered by tests
- **Success Threshold:** ≥80% coverage
- **Warning Threshold:** 60-79% coverage
- **Critical Threshold:** <60% coverage
- **Data Source:** Coverage reports (pytest coverage, Jest coverage, etc.)
- **Calculation:** (lines_covered / total_lines) * 100
- **Notes:** Applies to new code + regression on existing codebase

### 5. Build Success Rate
- **Metric ID:** `dev_build_success_rate`
- **Type:** Percentage
- **Unit:** % of CI/CD builds passing
- **Success Threshold:** ≥95% success rate
- **Warning Threshold:** 85-94% success rate
- **Critical Threshold:** <85% success rate
- **Data Source:** CI/CD pipeline logs (GitHub Actions, CircleCI, etc.)
- **Calculation:** (successful_builds / total_builds) * 100 WHERE triggered_at >= today - 7d
- **Notes:** Failed builds indicate technical debt or breaking changes

---

## TASK_DB Schema for Dev Metrics

```json
{
  "role": "dev",
  "metrics": {
    "dev_tasks_completed_weekly": {
      "type": "counter",
      "unit": "tasks/week",
      "thresholds": {
        "success": ">=5",
        "warning": "2-4",
        "critical": "<2"
      },
      "data_source": "TASK_DB",
      "api_endpoint": "/api/company/tasks?owner=dev&status=done"
    },
    "dev_prs_merged_daily": {
      "type": "counter",
      "unit": "PRs/day",
      "thresholds": {
        "success": ">=2",
        "warning": "1",
        "critical": "0"
      },
      "data_source": "GitHub API",
      "api_endpoint": "/repos/{owner}/{repo}/pulls?state=closed"
    },
    "dev_pr_merge_rate": {
      "type": "percentage",
      "unit": "%",
      "thresholds": {
        "success": ">=80",
        "warning": "60-79",
        "critical": "<60"
      },
      "data_source": "GitHub API",
      "api_endpoint": "/repos/{owner}/{repo}/pulls?state=all"
    },
    "dev_test_coverage_percent": {
      "type": "percentage",
      "unit": "%",
      "thresholds": {
        "success": ">=80",
        "warning": "60-79",
        "critical": "<60"
      },
      "data_source": "Coverage Reports",
      "api_endpoint": "/api/coverage/report"
    },
    "dev_build_success_rate": {
      "type": "percentage",
      "unit": "%",
      "thresholds": {
        "success": ">=95",
        "warning": "85-94",
        "critical": "<85"
      },
      "data_source": "CI/CD Logs",
      "api_endpoint": "/api/ci/builds"
    }
  }
}
```

---

## Implementation Plan

### Phase 1: Data Collection (Immediate)
1. **Tasks Completed:** Already available via TASK_DB API
   - Query: GET /api/company/tasks?owner=dev&status=done
   - Filter by date range (last 7 days)
   - Count results

2. **PRs Merged:** Integrate GitHub API
   - Authenticate with GitHub token
   - Query closed pull requests
   - Filter by merged=true and date

3. **PR Merge Rate:** Derived from PR data
   - Calculate ratio of merged/opened PRs
   - 7-day rolling window

### Phase 2: Code Quality Metrics (Sprint 2+)
4. **Test Coverage:** Set up coverage reporting
   - Configure pytest-coverage / Jest coverage
   - Expose coverage API endpoint
   - Track coverage trends over time

5. **Build Success Rate:** Monitor CI/CD pipeline
   - Hook into GitHub Actions / CircleCI webhooks
   - Log build results to metrics store
   - Calculate success rates

---

## Metric Collection Schedule

- **Real-time:** Build success rate (per build)
- **Daily:** PRs merged, PR merge rate (end of day)
- **Weekly:** Tasks completed (Sunday EoD)
- **Per-commit:** Test coverage (on every push)

---

## Integration with Autonomy-Engine

The autonomy-engine should:

1. **Generate dev-appropriate tasks:**
   - Feature implementation
   - Bug fixes
   - Refactoring
   - Code reviews
   - Test improvements
   - Documentation updates

2. **Monitor metric health:**
   - Alert on critical thresholds (<2 tasks/week, <60% merge rate)
   - Warn on warning thresholds (2-4 tasks/week, 60-79% merge rate)
   - Celebrate success thresholds (≥5 tasks/week, ≥80% merge rate)

3. **Adjust task allocation:**
   - Reduce workload if build success rate drops (quality issues)
   - Increase bugfix tasks if merge rate drops (scoping issues)
   - Balance feature vs maintenance based on velocity

---

## Known Limitations

1. **Tasks completed metric:** May be skewed by task size. Small tasks inflate count; large tasks deflate count. Consider task weighting in future iterations.

2. **PRs merged metric:** Doesn't account for PR complexity. 1-line PRs count the same as 500-line refactorations. Future enhancement: PR size weighting.

3. **Test coverage metric:** 100% coverage doesn't guarantee bug-free code. Quality of tests matters more than quantity. Future enhancement: Test effectiveness metrics.

4. **Build success rate:** False positives (builds passing but tests ineffective) and false negatives (builds failing due to flaky tests) can distort data. Requires manual review.

---

## Related Documents

- **LAB-SCOPE.md:** Decision 2: Role-Specific Metrics Framework
- **LAB-RES-005:** Role-Specific Metrics Framework Implementation (parent task)
- **INSIGHT-role-productivity-measurement.md:** Rationale for role-specific metrics
- **LAB-FINDINGS.md:** Sprint 1 research findings on metrics

---

## Change Log

- **2026-03-16:** Initial thresholds documented in TASK_DB (AC4/5 complete)
- **Future:** Add metric collection endpoints (AC5/5 pending)
- **Future:** Implement code quality metrics (test coverage, build success rate)
