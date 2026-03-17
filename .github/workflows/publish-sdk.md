# SDK Publishing Workflow

This workflow publishes Python and TypeScript SDKs when a GitHub release is created.

## Setup Required

### 1. Configure GitHub Secrets

Navigate to: `https://github.com/eduardg7/faintech-lab/settings/secrets/actions`

Add the following secrets:

#### PyPI Token
- Name: `PYPI_API_TOKEN`
- Value: Your PyPI API token
- How to get it: https://pypi.org/manage/account/token/

#### npm Token
- Name: `NPM_TOKEN`
- Value: Your npm automation token
- How to get it: https://www.npmjs.com/settings/tokens

### 2. Create GitHub Release

```bash
# Tag the version
git tag sdk-v1.0.0

# Push tags
git push origin lab/amc-mvp-113 --tags

# Create release via GitHub UI
# https://github.com/eduardg7/faintech-lab/releases/new
```

## Workflow Details

### Python SDK
- Builds using `python -m build`
- Publishes to PyPI using `twine`
- Triggered on release publish

### TypeScript SDK
- Builds using `npm run build`
- Publishes to npm using `npm publish --access public`
- Triggered on release publish

## Verification

After publishing, verify:

```bash
# Python SDK
pip install agentmemory
python -c "from agentmemory import MemoryClient; print('✅ Python SDK installed')"

# TypeScript SDK
npm install @agentmemory/sdk
node -e "const { MemoryClient } = require('@agentmemory/sdk'); console.log('✅ TypeScript SDK installed')"
```

## Troubleshooting

### PyPI Upload Fails
- Check `PYPI_API_TOKEN` secret exists and is valid
- Verify version number is not already published
- Ensure tag matches version in pyproject.toml

### npm Upload Fails
- Check `NPM_TOKEN` secret exists and has automation permissions
- Verify version number is not already published
- Ensure package name matches scope (`@agentmemory/sdk`)
