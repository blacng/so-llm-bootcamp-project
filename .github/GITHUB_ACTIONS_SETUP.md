# GitHub Actions CI/CD Setup Guide

This document explains how to set up and use the GitHub Actions workflows for this project.

## 📋 Overview

We've implemented a comprehensive CI/CD pipeline with the following workflows:

| Workflow | Purpose | Trigger |
|----------|---------|---------|
| **CI Pipeline** | Code quality, testing, security | Push, PR |
| **Docker Publish** | Build and push Docker images | Release, Manual |
| **Dependency Updates** | Automated dependency updates | Weekly (Monday) |
| **PR Checks** | PR validation and auto-labeling | PR opened/updated |
| **Performance** | Code complexity and build metrics | Push to main, PR |

---

## 🚀 Quick Start

### 1. Enable GitHub Actions

GitHub Actions is enabled by default for public repositories. For private repos:

1. Go to **Settings** → **Actions** → **General**
2. Enable "Allow all actions and reusable workflows"
3. Click **Save**

### 2. Push Workflows to GitHub

```bash
# Commit the workflow files
git add .github/
git commit -m "ci: add GitHub Actions workflows"
git push origin main
```

The workflows will automatically start running!

---

## 📊 Workflow Details

### 1. CI Pipeline (`ci.yml`)

**Runs on**: Every push and pull request to `main` or `develop` branches

**Jobs**:
- ✅ **Lint**: Runs `ruff` linting and format checks
- 🔒 **Security**: Scans for vulnerabilities (safety, bandit, trufflehog)
- 🏥 **Health Check**: Runs comprehensive health check script
- 🐳 **Docker Build**: Builds and tests Docker image
- 📝 **Type Check**: Runs `mypy` type checking
- 📈 **Test Coverage**: Runs tests and generates coverage reports
- 📋 **Summary**: Aggregates all job results

**View Results**: Go to **Actions** tab → Select latest workflow run

**Example Output**:
```
✅ Lint: Passed
✅ Security: Passed (2 warnings)
✅ Health Check: Passed
✅ Docker Build: Passed
⚠️  Type Check: Passed with warnings
⚠️  Test Coverage: 0% (no tests yet)
```

---

### 2. Docker Publish (`docker-publish.yml`)

**Runs on**:
- Release published
- Manual trigger via workflow dispatch

**What it does**:
- Builds Docker image
- Pushes to GitHub Container Registry (ghcr.io)
- Generates SBOM (Software Bill of Materials)
- Scans image for vulnerabilities (Trivy)
- Uploads security scan results

**How to Trigger Manually**:

1. Go to **Actions** → **Docker Publish**
2. Click **Run workflow**
3. Enter desired tag (e.g., `v1.0.0`, `latest`)
4. Click **Run workflow**

**Access Published Images**:
```bash
# Pull the image
docker pull ghcr.io/YOUR_USERNAME/so-llm-bootcamp-project:latest

# Or use in docker-compose.yml
services:
  streamlit-app:
    image: ghcr.io/YOUR_USERNAME/so-llm-bootcamp-project:latest
```

**Note**: Make sure to enable GitHub Packages in your repository settings.

---

### 3. Dependency Updates (`dependency-update.yml`)

**Runs on**:
- Every Monday at 9 AM UTC
- Manual trigger

**What it does**:
- Updates all dependencies using `uv lock --upgrade`
- Runs health check to verify compatibility
- Creates a pull request with changes

**Review Process**:
1. Automated PR will be created with title: `chore: Automated dependency updates`
2. Review the PR for breaking changes
3. Check CI results
4. Test locally if needed
5. Merge when ready

**Manual Trigger**:
1. Go to **Actions** → **Dependency Updates**
2. Click **Run workflow**
3. Check for new PR

---

### 4. PR Checks (`pr-checks.yml`)

**Runs on**: Pull requests (opened, updated, edited)

**Features**:

#### Auto-Labeling
Automatically labels PRs based on changed files:
- 📚 `documentation` - Changes to `.md` or `docs/`
- 🎨 `ui` - Changes to `pages/` or `ui_components.py`
- ⚙️ `backend` - Changes to `langchain_helpers.py`, `agent_service.py`
- 🔧 `config` - Changes to config files
- 🐳 `devops` - Changes to Docker, Makefile, CI
- 🧪 `testing` - Changes to test files
- 🔒 `security` - Changes to security-related files
- 📦 `dependencies` - Changes to `pyproject.toml`, `uv.lock`

#### PR Size Labels
- `size/xs`: < 10 lines
- `size/s`: < 100 lines
- `size/m`: < 500 lines
- `size/l`: < 1000 lines
- `size/xl`: > 1000 lines

#### PR Title Validation
Enforces conventional commit format:
```
<type>: <description>

Types: feat, fix, docs, style, refactor, perf, test, chore, ci, build

Examples:
✅ feat: add timeout protection to RAG chatbot
✅ fix: resolve infinite spinning issue
✅ docs: update GitHub Actions setup guide
❌ Added new feature
❌ Fixed bug
```

#### Welcome Comment
First-time contributors get a welcome comment with:
- PR checklist
- Next steps
- Link to contribution guidelines

---

### 5. Performance Monitoring (`performance.yml`)

**Runs on**: Push to `main`, PRs to `main`

**Analyzes**:
- **Cyclomatic Complexity**: Identifies complex functions
- **Maintainability Index**: Scores code maintainability (0-100)
- **Docker Build Time**: Tracks build performance
- **Image Size**: Monitors Docker image bloat

**Reports Available**: Check **Actions** → **Performance Monitoring** → **Artifacts**

---

## 🔐 Secrets and Environment Variables

Some workflows require secrets to be configured:

### Required Secrets

1. **GITHUB_TOKEN** - Automatically provided by GitHub ✅
2. **OPENAI_API_KEY** - For integration tests (optional)
3. **TAVILY_API_KEY** - For integration tests (optional)

### How to Add Secrets

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add name and value
4. Click **Add secret**

**Note**: For CI, we use dummy keys. Real keys only needed for integration tests.

---

## 🏷️ GitHub Labels Setup

Create these labels for auto-labeling to work:

```bash
# Run this script to create all labels
gh label create "documentation" --color "0075ca" --description "Documentation changes"
gh label create "ui" --color "d4c5f9" --description "UI/Frontend changes"
gh label create "backend" --color "c2e0c6" --description "Backend/Logic changes"
gh label create "config" --color "fef2c0" --description "Configuration changes"
gh label create "devops" --color "0e8a16" --description "DevOps/Infrastructure"
gh label create "testing" --color "e99695" --description "Test changes"
gh label create "security" --color "d93f0b" --description "Security-related"
gh label create "dependencies" --color "0366d6" --description "Dependency updates"
gh label create "size/xs" --color "ededed" --description "< 10 lines"
gh label create "size/s" --color "d4c5f9" --description "< 100 lines"
gh label create "size/m" --color "fbca04" --description "< 500 lines"
gh label create "size/l" --color "ff9800" --description "< 1000 lines"
gh label create "size/xl" --color "d93f0b" --description "> 1000 lines"
gh label create "automated" --color "006b75" --description "Automated PR"
```

Or manually create them in **Issues** → **Labels** → **New label**

---

## 🎯 Best Practices

### For Developers

1. **Before Pushing**:
   ```bash
   # Run local checks
   make lint
   make health-check
   make test
   ```

2. **Create Feature Branch**:
   ```bash
   git checkout -b feat/my-new-feature
   # Make changes
   git push origin feat/my-new-feature
   ```

3. **Open PR**:
   - Use conventional commit format in title
   - Write detailed description
   - Wait for CI to pass
   - Address review feedback

4. **After PR Merged**:
   - Delete feature branch
   - Pull latest main
   - Celebrate! 🎉

### For Maintainers

1. **Review Checklist**:
   - ✅ CI passing
   - ✅ Code quality acceptable
   - ✅ Tests added/updated
   - ✅ Documentation updated
   - ✅ No security issues

2. **Release Process**:
   ```bash
   # Create release tag
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0

   # Create GitHub release
   gh release create v1.0.0 --title "v1.0.0" --notes "Release notes here"
   ```

3. **Monitor CI Health**:
   - Check **Actions** tab weekly
   - Review failed workflows
   - Update workflows as needed

---

## 🐛 Troubleshooting

### CI Fails on First Push

**Problem**: Workflows fail because dependencies or tools aren't available

**Solution**:
1. Check workflow logs in Actions tab
2. Update workflow if needed
3. Re-run failed jobs

### Docker Build Times Out

**Problem**: Docker build exceeds 60 minutes

**Solution**:
1. Optimize Dockerfile (multi-stage builds, layer caching)
2. Increase timeout in workflow:
   ```yaml
   - name: Build Docker image
     timeout-minutes: 120
   ```

### Auto-Labeling Not Working

**Problem**: PRs don't get labeled automatically

**Solution**:
1. Verify `.github/labeler.yml` exists
2. Check labels exist in repository
3. Ensure workflow has `pull-requests: write` permission

### Dependency Update PR Fails

**Problem**: Automated dependency update creates failing PR

**Solution**:
1. Review breaking changes in updated dependencies
2. Update code to fix compatibility
3. Merge manually after fixes

---

## 📈 Monitoring CI Performance

### View Workflow Status

```bash
# Using GitHub CLI
gh run list --workflow=ci.yml
gh run view <run-id>

# Check specific job
gh run view <run-id> --job=<job-id>
```

### Workflow Metrics to Track

- ⏱️ **Build Time**: Should be < 10 minutes
- ✅ **Success Rate**: Target > 95%
- 🔄 **Frequency**: How often workflows run
- 📦 **Artifact Size**: Uploaded reports size

### Generate Workflow Badge

Add to README.md:
```markdown
![CI](https://github.com/YOUR_USERNAME/so-llm-bootcamp-project/workflows/CI%2FCD%20Pipeline/badge.svg)
```

---

## 🎓 Learning Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Awesome GitHub Actions](https://github.com/sdras/awesome-actions)

---

## 🤝 Contributing to Workflows

Want to improve the CI/CD pipeline? Here's how:

1. Test changes locally using [act](https://github.com/nektos/act):
   ```bash
   brew install act
   act -l  # List workflows
   act push  # Simulate push event
   ```

2. Create PR with workflow changes
3. Use conventional commit: `ci: improve Docker build caching`
4. Document changes in this file

---

## 📞 Support

Issues with CI/CD?
- Check **Actions** tab logs
- Review this documentation
- Open issue with `ci` label
- Tag maintainers if urgent

---

**Last Updated**: 2025-01-12
**Maintained By**: Project Team
