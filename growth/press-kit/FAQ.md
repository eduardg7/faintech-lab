# FAQ - Faintech Lab Agent Memory Service Beta

**Document Purpose**: Anticipate and answer common questions from technical founders, press, and beta applicants

**Target Audience**: Technical founders, developers, AI engineers, tech journalists

**Date**: 2026-03-19

---

## Product Questions

### Q1: What exactly is Agent Memory Service (AMC)?

**A:** AMC is a persistent memory API for AI agent fleets. It allows teams running 1-50+ AI agents to store, retrieve, and search memories across sessions. Key capabilities include:

- **Persistent storage**: Agent memories survive session restarts
- **Semantic search**: Query memories by meaning, not just keywords
- **Multi-agent context**: Coordinate memories across distributed agent workflows
- **Structured documentation**: Every endpoint documented with examples and failure modes

Unlike ad-hoc memory solutions built on Redis or databases, AMC is designed specifically for AI agent workflows with semantic understanding and multi-agent orchestration patterns.

---

### Q2: How is this different from existing orchestration platforms (LangChain, AutoGen, CrewAI)?

**A:** AMC is **memory infrastructure**, not orchestration. It works with any orchestration layer:

- **LangChain**: Use AMC as a persistent memory store for LangChain agents
- **AutoGen**: Store and retrieve conversation history across AutoGen sessions
- **CrewAI**: Coordinate memories between different crew members

We're not competing with orchestration—we're building the memory layer that orchestration platforms assume exists but don't provide.

---

### Q3: What's the technical architecture?

**A:** AMC provides RESTful API endpoints with the following structure:

- **`/v1/memories`**: CRUD operations for memory entries
- **`/v1/agents`**: Agent registration and context management
- **`/v1/projects`**: Multi-project isolation and organization
- **`/v1/search/keyword`**: Traditional keyword search
- **`/v1/search/semantic`**: Vector-based semantic search

Backend is built on FastAPI with PostgreSQL for structured data and vector extensions for semantic search. Open-source SDK available for Python, with other languages planned based on community demand.

---

### Q4: Is there an open-source SDK?

**A:** Yes. The Python SDK is available at github.com/eduardg7/faintech-lab with:

- Full API coverage
- Example agents and workflows
- Contribution guidelines for community extensions
- Transparent development process (all PRs and issues public)

We're committed to open-source as the primary distribution model. No vendor lock-in, no proprietary protocols.

---

## Beta Program Questions

### Q5: Who is the ideal beta user?

**A:** Technical founders or engineers who:

- Run AI agent fleets (1-50+ agents) in production or advanced prototyping
- Struggle with memory persistence, context management, or multi-agent coordination
- Can provide structured feedback on API design and documentation
- Are interested in contributing to open-source AI infrastructure

We're not looking for enterprise pilot programs or proof-of-concept demos. We want teams shipping real code who can validate or challenge our hypotheses.

---

### Q6: How do I apply for the beta?

**A:** Apply at github.com/eduardg7/faintech-lab by:

1. Reviewing our Channel Hypotheses document to understand our methodology
2. Opening a GitHub issue describing your agent fleet use case
3. Providing your technical background and current pain points

We're selecting 20-50 beta users based on:

- Technical fit (running agent fleets, not just exploring AI)
- Feedback quality (willingness to provide structured input)
- Community alignment (interest in open-source contribution)

---

### Q7: What do beta participants get?

**A:** Beta participants receive:

- **Early API access**: Full access to AMC endpoints before public launch
- **Direct engineering channel**: Slack or Discord access to the Faintech Lab team
- **Roadmap influence**: Input on feature prioritization and API design decisions
- **Recognition**: Attribution in public documentation and case studies (optional)
- **Pricing advantage**: Beta pricing lock-in for early adopters (details TBD)

In exchange, we ask for:

- Structured feedback on API usability and documentation
- Bug reports and edge case discoveries
- Optional contributions to open-source SDK and examples

---

### Q8: How long is the beta period?

**A:** We're targeting a 4-8 week beta period starting March 24, 2026. Public launch is planned for late Q2 2026, but timeline depends on:

- Beta user feedback quality and volume
- Critical bugs or API design changes required
- Infrastructure scaling needs

We'll communicate timeline updates transparently through GitHub and the beta user channel.

---

## Technical Questions

### Q9: What programming languages are supported?

**A:** Python SDK is available at beta launch. Additional language support (JavaScript, Go, Rust) depends on:

- Community demand (GitHub issues requesting specific languages)
- Contribution interest from the community
- Our internal capacity for SDK maintenance

If you need a specific language SDK, open a GitHub issue describing your use case. Community contributions are welcome and encouraged.

---

### Q10: How do you handle vector embeddings for semantic search?

**A:** AMC handles embedding generation internally—you don't need to manage embedding models or vector databases. When you store a memory:

1. AMC generates embeddings using a default model (currently OpenAI text-embedding-3-small)
2. Embeddings are stored in PostgreSQL with pgvector extension
3. Semantic search queries are handled via the `/v1/search/semantic` endpoint

Future versions will support:

- Custom embedding models (BYOM - bring your own model)
- Multiple embedding strategies per project
- Hybrid search (keyword + semantic combined)

---

### Q11: What's the pricing model?

**A:** Beta pricing details will be announced closer to launch. Our principles:

- **Developer-friendly**: No per-seat licenses, no enterprise-only features
- **Usage-based**: Pay for API calls and storage, not agent count
- **Transparent**: Pricing published publicly with clear tiers
- **Beta advantage**: Early adopters get pricing lock-in or discounts

Specific numbers TBD based on infrastructure costs and beta feedback.

---

### Q12: What are the API rate limits and performance characteristics?

**A:** Beta phase limits (subject to change):

- **Rate limits**: 100 requests/minute per API key (adjustable for high-volume users)
- **Latency**: p50 < 100ms, p95 < 500ms for standard CRUD operations
- **Storage**: 1GB included per beta account, expandable on request
- **Semantic search**: Optimized for <1s response time on datasets up to 100K memories

Post-beta limits will scale based on infrastructure testing and user feedback.

---

## Privacy & Compliance Questions

### Q13: Is AMC GDPR-compliant?

**A:** Yes. Privacy-first architecture is a core design principle:

- **Data subject rights built-in**: APIs for access, deletion, and portability requests
- **Data minimization**: Only store what's necessary for memory functionality
- **Encryption at rest and in transit**: All data encrypted by default
- **EU hosting**: Primary infrastructure in EU data centers

Full privacy policy available at [link to be provided]. We've documented our GDPR compliance process publicly in the repo.

---

### Q14: Who owns the data stored in AMC?

**A:** You own your data. AMC is infrastructure, not a data platform:

- **Your memories, your control**: Full CRUD access and deletion capabilities
- **No data monetization**: We don't train models on your memories or sell access
- **Export anytime**: API endpoints for full data export in standard formats
- **Deletion guarantees**: Permanent deletion on request, verified through documentation

---

### Q15: Can I self-host AMC?

**A:** Not at beta launch, but it's on the roadmap. Self-hosting requires:

- Docker-compose setup for local development (available now for contributors)
- Production-ready self-hosting guide (planned post-public launch)
- Enterprise support options for self-hosted deployments (future consideration)

If self-hosting is a hard requirement for your team, open a GitHub issue describing your constraints.

---

## Future & Roadmap Questions

### Q16: What's on the roadmap after beta?

**A:** Near-term priorities (based on beta feedback):

1. **Multi-language SDKs**: JavaScript, Go, Rust based on community demand
2. **Custom embedding models**: BYOM support for teams with specific requirements
3. **Hybrid search**: Combined keyword + semantic search capabilities
4. **Agent orchestration patterns**: Documentation and examples for common multi-agent workflows

Long-term vision:

- **Agent observability**: Debugging and monitoring tools for multi-agent systems
- **Collaboration features**: Multi-team memory sharing and access control
- **Edge deployment**: Lightweight memory service for resource-constrained environments

Roadmap is public and influenced by beta user feedback. No surprises.

---

### Q17: How do you decide what to build next?

**A:** We follow a hypothesis-first methodology:

1. **Identify hypothesis**: "Feature X will reduce friction by Y% for Z user segment"
2. **Document publicly**: Hypothesis, success metrics, and timeline in GitHub
3. **Build MVP**: Minimum implementation to test hypothesis
4. **Measure outcomes**: Track awareness, engagement, conversion, quality
5. **Pivot or double-down**: If 0-2/4 metrics pass, pivot within 1-2 weeks

All experiments documented in CHANNEL-HYPOTHESES.md. You can see exactly how we make decisions.

---

### Q18: Will there be an enterprise tier?

**A:** Maybe, but not during beta. Our focus is technical founders and mid-market teams, not enterprise sales cycles. If enterprise demand emerges, we'll:

- Document the hypothesis publicly
- Define success metrics (e.g., "5 enterprise teams request pilot")
- Build minimal enterprise features (SSO, audit logs, custom SLAs)
- Measure and decide based on data

No enterprise roadmap until we see validated demand.

---

### Q19: How can I contribute to the project?

**A:** Contributions welcome in several forms:

- **Code**: SDK improvements, new language bindings, bug fixes via GitHub PRs
- **Documentation**: Examples, tutorials, API docs improvements
- **Feedback**: Structured input on API design, pain points, edge cases
- **Experiments**: Run your own channel experiments and share learnings

See CONTRIBUTING.md in the repo for guidelines. All contributions credited publicly.

---

### Q20: What if AMC doesn't solve my problem?

**A:** Tell us. We want to know:

- **What's missing**: Features you expected but didn't find
- **What's broken**: Bugs, edge cases, documentation gaps
- **What's better elsewhere**: Competitors doing something we should learn from

We'd rather lose you to a better solution than keep you with a product that doesn't fit. Honest feedback improves the project for everyone.

Open a GitHub issue or reach out through the beta channel. We read everything.

---

## Quick Reference

| Question Type | Count |
|--------------|-------|
| Product | 4 (Q1-Q4) |
| Beta Program | 4 (Q5-Q8) |
| Technical | 4 (Q9-Q12) |
| Privacy & Compliance | 3 (Q13-Q15) |
| Future & Roadmap | 5 (Q16-Q20) |
| **Total** | **20** |

---

**Document Version**: 1.0
**Date**: 2026-03-19
**Status**: Draft - Ready for Review
**Task**: CONTENT-20260318133800-PRESS-KIT (AC3/5)
**Next Owner**: faintech-content-creator (review and finalize)
