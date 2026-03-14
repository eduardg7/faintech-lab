# SDK Publishing Guide

This document describes how to publish the Agent Memory Cloud SDKs to PyPI and npm.

## Prerequisites

### Python SDK (PyPI)

1. Create a PyPI account at https://pypi.org/account/register/
2. Generate an API token: https://pypi.org/manage/account/token/
3. Add the token as a GitHub secret: `PYPI_API_TOKEN`

### TypeScript SDK (npm)

1. Create an npm account at https://www.npmjs.com/signup
2. Generate an automation token: https://www.npmjs.com/settings/tokens
3. Add the token as a GitHub secret: `NPM_TOKEN`

## Automated Publishing

SDKs are automatically published when you create a GitHub release.

### Steps:

1. **Update version numbers**:
   ```bash
   # Python SDK
   cd sdks/python
   # Edit version in pyproject.toml

   # TypeScript SDK
   cd sdks/typescript
   # Edit version in package.json
   ```

2. **Commit and tag**:
   ```bash
   git add sdks/python/pyproject.toml sdks/typescript/package.json
   git commit -m "chore(sdk): bump version to X.Y.Z"
   git tag sdk-vX.Y.Z
   git push origin master --tags
   ```

3. **Create GitHub release**:
   - Go to https://github.com/eduardg7/faintech-lab/releases/new
   - Select the tag: `sdk-vX.Y.Z`
   - Title: `SDK vX.Y.Z`
   - Description: List changes
   - Click "Publish release"

4. **Monitor the workflow**:
   - Go to Actions tab in GitHub
   - Watch the "Publish SDKs" workflow
   - Verify both Python and TypeScript SDKs are published

## Manual Publishing

### Python SDK

```bash
cd sdks/python

# Build the distribution
python -m build

# Upload to PyPI
twine upload dist/*
```

### TypeScript SDK

```bash
cd sdks/typescript

# Install dependencies
npm ci

# Build the SDK
npm run build

# Publish to npm
npm publish --access public
```

## Testing the Published SDKs

### Python SDK

```bash
# Install from PyPI
pip install agentmemory

# Test import
python -c "from agentmemory import MemoryClient; print('✅ SDK installed successfully')"
```

### TypeScript SDK

```bash
# Install from npm
npm install @agentmemory/sdk

# Test import
node -e "const { MemoryClient } = require('@agentmemory/sdk'); console.log('✅ SDK installed successfully')"
```

## Troubleshooting

### PyPI Upload Fails

- **Error**: "File already exists"
  - **Solution**: You cannot re-upload the same version. Bump the version number.

- **Error**: "Invalid or missing authentication"
  - **Solution**: Check your `PYPI_API_TOKEN` secret in GitHub.

### npm Upload Fails

- **Error**: "You need a paid account to publish this package"
  - **Solution**: The package is scoped (`@agentmemory/sdk`). Make sure to use `--access public`.

- **Error**: "You do not have permission to publish"
  - **Solution**: Check your `NPM_TOKEN` secret in GitHub and ensure it has automation permissions.

### Build Fails

- **Python**: Check that all dependencies in `pyproject.toml` are installable
- **TypeScript**: Run `npm run build` locally to verify the build

## Version Management

### Semantic Versioning

Follow [SemVer](https://semver.org/):

- **MAJOR (X.0.0)**: Breaking changes
- **MINOR (0.Y.0)**: New features, backward compatible
- **PATCH (0.0.Z)**: Bug fixes, backward compatible

### Changelog

Keep a `CHANGELOG.md` in each SDK directory to track changes:

```markdown
## [0.1.0] - 2026-03-11

### Added
- Initial release
- Python SDK with full API coverage
- TypeScript SDK with full type safety
- Memory CRUD operations
- Keyword and semantic search
- Agent and project management
```

## Security Best Practices

1. **Never commit tokens** to the repository
2. **Use GitHub secrets** for all credentials
3. **Rotate tokens** periodically
4. **Monitor PyPI/npm** for unauthorized uploads
5. **Enable 2FA** on PyPI and npm accounts

## Support

For issues with publishing:
- 📧 Email: support@faintech.dev
- 📖 Docs: https://docs.faintech.dev/publishing
- 🐛 Issues: https://github.com/eduardg7/faintech-lab/issues
