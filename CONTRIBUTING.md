# Contributing to Faintech Lab

Thank you for your interest in contributing to Faintech Lab! This guide will help you get started.

## Overview

Faintech Lab is the R&D workspace for Faintech Solutions SRL. It hosts experimental projects, new product development, and infrastructure work for autonomous agents.

## Development Environment Setup

### Prerequisites

- **Git**: Version control
- **Node.js**: v22 or higher (check with `node --version`)
- **GitHub Account**: For PRs and collaboration

### Initial Setup

1. **Clone the repository**:
   ```bash
   git clone git@github.com:eduardg7/faintech-lab.git
   cd faintech-lab
   ```

2. **Verify your remote**:
   ```bash
   git remote -v
   # Should show: git@github.com:eduardg7/faintech-lab.git
   ```

3. **Switch to the correct branch**:
   ```bash
   git checkout master
   ```

### Working with the Repository

#### Branch Pattern
Use the following branch naming convention:
```
lab/<project>/<task-slug>
```

Examples:
- `lab/meta-ai/persistent-memory`
- `lab/new-product/mvp-design`
- `lab/meta-ai/agent-messaging`

#### Workflow Steps

1. **Create a new branch**:
   ```bash
   git checkout -b lab/<project>/<task-slug>
   ```

2. **Make your changes**:
   - Edit files
   - Test locally
   - Ensure CI would pass (JSON validity, basic checks)

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: description of change"
   ```
   Commit message prefixes:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation
   - `refactor:` Code refactoring
   - `test:` Test changes
   - `chore:` Maintenance

4. **Push to GitHub**:
   ```bash
   git push origin lab/<project>/<task-slug>
   ```

5. **Create a Pull Request**:
   - Go to https://github.com/eduardg7/faintech-lab
   - Click "Pull requests" → "New pull request"
   - Select your branch
   - Fill in PR template
   - Request review

#### CI/CD

The repository has basic CI checks that run on every push and PR:

- **JSON Validation**: All `.json` files must be valid
- **Markdown Validation**: Basic existence and non-empty checks
- **Repository Health**: Directory structure verification

CI will automatically run on your PR. Ensure it passes before requesting review.

## Agent Integration

Faintech Lab agents work autonomously with the following integration points:

### Task Database
- **Location**: `/Users/eduardgridan/faintech-os/data/ops/TASK_DB.json`
- **Usage**: Agents track task progress, status, and evidence

### Project State
- **Location**: `/Users/eduardgridan/faintech-os/data/ops/FAINTECH_OS_STATE.json`
- **Usage**: Project configuration, assignments, and team structure

### Specs Directory
- **Location**: `.specs/`
- **Usage**: Task specifications and requirements

### Autonomy
Agents can:
- Branch, commit, and push without manual intervention
- Create and update documentation
- Execute test scripts
- Track evidence for task completion

## Projects

### 1. meta-ai — Better Agents
**Goal**: Build reusable infrastructure for smarter, more autonomous agents.

Focus areas:
- Persistent agent memory across sessions
- Self-improvement loops
- Inter-agent communication protocols
- Agent observability

### 2. new-product — Customer Product
**Goal**: Build a new product for external customers.

Direction: TBD by CPO. Starting point: identify problems meta-ai infrastructure solves for non-technical teams.

## Documentation

- Every merged PR should update relevant `docs/` files
- Failed experiments get documented in `docs/experiments/`
- Use clear, concise explanations
- Include examples where helpful

## Code Style

- Use TypeScript for Node.js projects
- Follow existing code patterns
- Write meaningful commit messages
- Keep PRs focused and small (one task per PR)

## Questions?

- Check existing documentation in `docs/`
- Review `.specs/` for task requirements
- Reach out to the Faintech team via GitHub issues

---

**Happy contributing! 🚀**
