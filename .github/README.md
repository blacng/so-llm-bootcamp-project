# GitHub Configuration

This directory contains GitHub-specific configuration files for automated workflows, PR management, and CI/CD pipelines.

## 📁 Directory Structure

```
.github/
├── workflows/           # GitHub Actions workflow definitions
│   ├── ci.yml          # Main CI/CD pipeline
│   ├── docker-publish.yml  # Docker image publishing
│   ├── dependency-update.yml  # Automated dependency updates
│   ├── pr-checks.yml   # PR validation and auto-labeling
│   └── performance.yml # Performance monitoring
├── labeler.yml         # Auto-labeling configuration
├── GITHUB_ACTIONS_SETUP.md  # Detailed setup guide
└── README.md           # This file
```

## 🚀 Quick Links

- **[Setup Guide](GITHUB_ACTIONS_SETUP.md)** - Comprehensive guide to GitHub Actions setup
- **[Actions Tab](../../actions)** - View workflow runs and results
- **[Security Tab](../../security)** - View security alerts and scans

## 🔧 Workflows Overview

| Workflow | Status | Trigger |
|----------|--------|---------|
| CI/CD Pipeline | ![CI](https://github.com/YOUR_USERNAME/so-llm-bootcamp-project/workflows/CI%2FCD%20Pipeline/badge.svg) | Push, PR |
| Docker Publish | ![Docker](https://github.com/YOUR_USERNAME/so-llm-bootcamp-project/workflows/Docker%20Publish/badge.svg) | Release |
| Dependency Updates | ![Deps](https://github.com/YOUR_USERNAME/so-llm-bootcamp-project/workflows/Dependency%20Updates/badge.svg) | Weekly |
| PR Checks | ![PR](https://github.com/YOUR_USERNAME/so-llm-bootcamp-project/workflows/Pull%20Request%20Checks/badge.svg) | PR |
| Performance | ![Perf](https://github.com/YOUR_USERNAME/so-llm-bootcamp-project/workflows/Performance%20Monitoring/badge.svg) | Push to main |

## 📖 Getting Started

1. **Enable GitHub Actions** (automatic for public repos)
2. **Push workflows to GitHub**:
   ```bash
   git add .github/
   git commit -m "ci: add GitHub Actions workflows"
   git push origin main
   ```
3. **View workflow runs** in the Actions tab
4. **Read the [full setup guide](GITHUB_ACTIONS_SETUP.md)** for details

## 🏷️ Auto-Labeling

PRs are automatically labeled based on changed files:

- 📚 `documentation` - Docs changes
- 🎨 `ui` - Frontend changes
- ⚙️ `backend` - Backend logic
- 🔧 `config` - Configuration
- 🐳 `devops` - Infrastructure
- 🧪 `testing` - Tests
- 🔒 `security` - Security
- 📦 `dependencies` - Deps

Size labels are also applied automatically.

## 🤝 Contributing

Want to improve the CI/CD pipeline? See [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md#-contributing-to-workflows)

## 📞 Support

Issues? Check the [setup guide](GITHUB_ACTIONS_SETUP.md#-troubleshooting) or open an issue with the `ci` label.
