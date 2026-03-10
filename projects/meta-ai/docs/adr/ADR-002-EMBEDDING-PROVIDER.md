# ADR-002: Embedding Provider Selection

**Status:** Accepted  
**Date:** 2026-03-10  
**Decision:** faintech-cto  
**Context:** AMC MVP Technical Planning  
**Related:** AMC-MVP-001

---

## Context

We need to select a text embedding provider for semantic search in Agent Memory Cloud MVP.

### Requirements

- High-quality semantic search (better than keyword matching)
- API availability and reliability
- Reasonable cost for MVP scale (<10K embeddings)
- Simple integration (Python SDK or REST API)

---

## Options Considered

**Option A: OpenAI text-embedding-3-small**
- Pros: Best quality, reliable API, simple integration
- Cons: Requires API key, not self-hosted
- Cost: $0.02/1M tokens (~$0.20 for 10K memories)

**Option B: Cohere embed-multilingual-v3.0**
- Pros: Multilingual support, good quality
- Cons: Similar cost to OpenAI, less ecosystem
- Cost: $0.10/1M tokens (~$1.00 for 10K memories)

**Option C: SentenceTransformers (self-hosted)**
- Pros: Free, self-hosted, no API keys
- Cons: Requires GPU for speed, model hosting complexity
- Cost: Server cost (~$20/mo for GPU instance)

**Option D: Open Source + OpenAI Hybrid**
- Pros: Free for >90% of queries, fallback for quality
- Cons: Complex integration, two systems to maintain
- Cost: $5/mo self-hosted + $0.02/1M tokens for 10%

---

## Decision

**Selected: Option A - OpenAI text-embedding-3-small**

### Rationale

1. **Quality** - OpenAI embeddings have best semantic search quality in benchmarks
2. **Simplicity** - Single API integration, no self-hosting complexity
3. **Cost** - $0.20 for 10K embeddings fits $25/mo infrastructure target
4. **Reliability** - 99.9% uptime, no self-hosting maintenance
5. **Speed** - <50ms embedding generation, fits API latency targets

### Implementation

```python
# embeddings.py
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_embedding(text: str) -> list[float]:
    """Generate embedding using OpenAI text-embedding-3-small."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding
```

### Async Job Queue (Background Processing)

```python
# embedding_jobs.py
from celery import Celery
from .embeddings import generate_embedding
from .models import MemoryEntry, EmbeddingJob

celery = Celery('tasks', broker=os.getenv("REDIS_URL"))

@celery.task
def process_embedding_job(memory_id: str):
    """Background task to generate and store embedding."""
    job = EmbeddingJob.get(memory_id)
    job.status = "processing"
    job.save()
    
    try:
        memory = MemoryEntry.get(memory_id)
        embedding = generate_embedding(memory.content)
        memory.embedding = embedding
        memory.save()
        
        job.status = "completed"
        job.completed_at = datetime.utcnow()
    except Exception as e:
        job.status = "failed"
        job.last_error = str(e)
        job.attempts += 1
    
    job.save()
```

### Cost Tracking

```python
# analytics.py
def track_embedding_cost(memory_count: int):
    """Track embedding costs for billing/analytics."""
    # Approximate: 1000 words ~ 1333 tokens
    avg_words_per_memory = 100
    tokens_per_memory = avg_words_per_memory * 1.33
    total_tokens = memory_count * tokens_per_memory
    cost_usd = (total_tokens / 1_000_000) * 0.02
    
    return {
        "memory_count": memory_count,
        "total_tokens": total_tokens,
        "cost_usd": round(cost_usd, 4)
    }
```

### Cost Examples

| Memories | Avg Words | Tokens | Cost (USD) |
|----------|-------------|---------|--------------|
| 1,000 | 100 | 1,333 | $0.027 |
| 5,000 | 100 | 6,667 | $0.133 |
| 10,000 | 100 | 13,333 | $0.267 |
| 50,000 | 100 | 66,667 | $1.333 |
| 100,000 | 100 | 133,333 | $2.667 |

---

## Consequences

### Positive
- Best-in-class semantic search quality
- Simple, reliable integration
- Low cost for MVP scale (<$1/mo for 10K embeddings)
- Fast embedding generation (<50ms)

### Negative
- Requires OpenAI API key (customer trust concern)
- Monthly cost grows with usage
- Not self-hosted (vendor lock-in)

### Mitigation
- Document API key security clearly in docs
- Show embedding costs in customer dashboard
- ADR-003: Switch to self-hosted at 50K+ memories

---

## Alternatives Considered

### Cohere (Rejected)
- Similar cost, worse quality
- Less ecosystem/tooling

### SentenceTransformers (Rejected)
- GPU hosting too complex for MVP
- Dev experience suffers

### Hybrid Approach (Rejected)
- Too complex for MVP timeline
- Two systems to maintain

---

## Status

**Accepted** - Decision to use OpenAI text-embedding-3-small is final for MVP.

**Future Review** (Week 6, April 20): Switch to self-hosted (SentenceTransformers) when customer count >10 to reduce costs.

---

**Review Date:** Week 6 (April 20, 2026)  
**Owner:** faintech-cto
