# Add this section to your main README.md

---

## 🔄 CI/CD Pipeline

This project uses GitHub Actions for automated testing, security scanning, and deployment.

### Workflows

| Workflow | Status | Description |
|----------|--------|-------------|
| CI/CD Pipeline | ![CI](https://github.com/YOUR_USERNAME/so-llm-bootcamp-project/workflows/CI%2FCD%20Pipeline/badge.svg) | Code quality, testing, security |
| Docker Publish | ![Docker](https://github.com/YOUR_USERNAME/so-llm-bootcamp-project/workflows/Docker%20Publish/badge.svg) | Build and publish Docker images |
| PR Checks | ![PR](https://github.com/YOUR_USERNAME/so-llm-bootcamp-project/workflows/Pull%20Request%20Checks/badge.svg) | PR validation and auto-labeling |

### Features

- ✅ **Automated Quality Checks**: Linting, type checking, code complexity analysis
- 🔒 **Security Scanning**: Dependency vulnerabilities, code security, secret detection
- 🐳 **Docker Publishing**: Automatic image building and publishing to GitHub Container Registry
- 🏷️ **PR Auto-Labeling**: Automatic categorization and size labeling of pull requests
- 📦 **Dependency Updates**: Weekly automated dependency update PRs
- 📊 **Performance Monitoring**: Track code quality and build performance over time

### Quick Start

```bash
# Push to trigger CI
git push origin main

# Create PR (auto-labeled and validated)
gh pr create --title "feat: new feature" --body "Description"

# Create release (auto-publishes Docker image)
gh release create v1.0.0 --title "v1.0.0" --notes "Release notes"
```

### Documentation

- 📖 [Quick Start Guide](docs/GITHUB_ACTIONS_SUMMARY.md)
- 📘 [Comprehensive Setup Guide](.github/GITHUB_ACTIONS_SETUP.md)
- 📊 [Workflow Diagrams](.github/WORKFLOWS_DIAGRAM.md)

---
