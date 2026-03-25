# Signup Evidence Template

**Purpose:** JSON schema for tracking each beta signup with evidence
**Location:** `/research/beta-user-evidence/signups/`
**Naming:** `SIGNUP-001.json`, `SIGNUP-002.json`, etc.

---

## Template

```json
{
  "signup_id": "SIGNUP-XXX",
  "timestamp": "2026-03-24T10:XX:XX+02:00",
  "user_data": {
    "email": "REDACTED",
    "segment_guess": "ai_engineer|cto|product_lead|founder|researcher|other",
    "company_type": "startup|enterprise|agency|consultant|academic|other",
    "system_size": "1_agent|2-5_agents|6-20_agents|21-50_agents|50+_agents"
  },
  "acquisition": {
    "source": "github_issue_90|twitter|hn|linkedin|direct|referral|other",
    "utm_params": {
      "utm_source": "string or null",
      "utm_medium": "string or null",
      "utm_campaign": "string or null"
    },
    "referrer_url": "string or null"
  },
  "engagement": {
    "onboarding_completed": false,
    "first_memory_created": false,
    "time_to_first_memory_minutes": null,
    "session_duration_minutes": null
  },
  "feedback": {
    "onboarding_survey_completed": false,
    "pain_point": null,
    "feature_request": null,
    "nps_score": null,
    "qualitative_feedback": null
  },
  "follow_up": {
    "priority": "high|medium|low",
    "interview_scheduled": false,
    "interview_date": null,
    "notes": "Free text observations"
  },
  "metadata": {
    "created_at": "2026-03-24T10:XX:XX+02:00",
    "updated_at": "2026-03-24T10:XX:XX+02:00",
    "researcher": "faintech-user-researcher"
  }
}
```

---

## Field Definitions

### signup_id
- Format: `SIGNUP-XXX` (sequential numbering)
- Example: `SIGNUP-001`, `SIGNUP-002`

### timestamp
- ISO 8601 format with timezone
- Time of signup completion

### user_data.segment_guess
- Initial segment classification based on available data
- Options: `ai_engineer`, `cto`, `product_lead`, `founder`, `researcher`, `other`
- Update after onboarding survey

### acquisition.source
- Primary traffic source attribution
- Options: `github_issue_90`, `twitter`, `hn` (Hacker News), `linkedin`, `direct`, `referral`, `other`
- Use UTM params when available

### engagement
- Track user behavior in first session
- `time_to_first_memory_minutes`: Duration from signup to first memory created
- `session_duration_minutes`: Total session length

### feedback
- Survey responses and qualitative feedback
- `nps_score`: Net Promoter Score (1-10)
- Update after surveys completed

### follow_up.priority
- `high`: Strategic segment, active engagement, high-value feedback
- `medium`: Active user, moderate feedback
- `low`: Passive user, minimal engagement

---

## Usage Instructions

### Creating a New Signup Record
1. Copy template to `/research/beta-user-evidence/signups/SIGNUP-XXX.json`
2. Fill in known fields at signup time
3. Leave unknown fields as `null`
4. Update fields as new data arrives (surveys, behavior tracking)

### Updating Existing Records
1. Read existing JSON file
2. Update relevant fields
3. Update `metadata.updated_at` timestamp
4. Save back to same file

### Aggregation Queries
```bash
# Count total signups
ls -1 /research/beta-user-evidence/signups/*.json | wc -l

# Count by source
cat /research/beta-user-evidence/signups/*.json | jq -r '.acquisition.source' | sort | uniq -c

# Count by segment
cat /research/beta-user-evidence/signups/*.json | jq -r '.user_data.segment_guess' | sort | uniq -c
```

---

## Example Record

```json
{
  "signup_id": "SIGNUP-001",
  "timestamp": "2026-03-24T10:15:32+02:00",
  "user_data": {
    "email": "REDACTED",
    "segment_guess": "ai_engineer",
    "company_type": "startup",
    "system_size": "6-20_agents"
  },
  "acquisition": {
    "source": "github_issue_90",
    "utm_params": {
      "utm_source": null,
      "utm_medium": null,
      "utm_campaign": null
    },
    "referrer_url": "https://github.com/eduardg7/faintech-lab/issues/90"
  },
  "engagement": {
    "onboarding_completed": true,
    "first_memory_created": true,
    "time_to_first_memory_minutes": 12,
    "session_duration_minutes": 28
  },
  "feedback": {
    "onboarding_survey_completed": true,
    "pain_point": "Agents forget context across sessions",
    "feature_request": "Team collaboration for shared memories",
    "nps_score": 9,
    "qualitative_feedback": "Finally a memory system that doesn't require vector DB setup"
  },
  "follow_up": {
    "priority": "high",
    "interview_scheduled": true,
    "interview_date": "2026-03-26T14:00:00+02:00",
    "notes": "Very engaged, asked about self-hosting. Potential champion user."
  },
  "metadata": {
    "created_at": "2026-03-24T10:15:32+02:00",
    "updated_at": "2026-03-24T10:43:18+02:00",
    "researcher": "faintech-user-researcher"
  }
}
```

---

**Status:** READY FOR USE
**Created:** 2026-03-23 21:30 EET
**Owner:** faintech-user-researcher
