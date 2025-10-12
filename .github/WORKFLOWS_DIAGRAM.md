# GitHub Actions Workflows - Visual Overview

## 🔄 Complete CI/CD Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DEVELOPER WORKFLOW                           │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
              ┌─────▼─────┐              ┌────────▼────────┐
              │  git push │              │  Create PR      │
              │  to main  │              │  (feature branch)│
              └─────┬─────┘              └────────┬────────┘
                    │                             │
┌───────────────────▼──────────────────┐ ┌────────▼─────────────────────┐
│      CI/CD PIPELINE (ci.yml)         │ │   PR CHECKS (pr-checks.yml)  │
├──────────────────────────────────────┤ ├──────────────────────────────┤
│                                      │ │                              │
│  ┌────────────┐  ┌────────────┐    │ │  ┌────────────────────────┐  │
│  │   Lint     │→ │  Security  │    │ │  │   Validate PR Title    │  │
│  │  (ruff)    │  │  (bandit)  │    │ │  │   (semantic format)    │  │
│  └────────────┘  └────────────┘    │ │  └────────────────────────┘  │
│         │               │           │ │              │               │
│         ▼               ▼           │ │              ▼               │
│  ┌────────────┐  ┌────────────┐    │ │  ┌────────────────────────┐  │
│  │   Health   │  │Type Check  │    │ │  │   Auto-Label PR        │  │
│  │   Check    │  │  (mypy)    │    │ │  │   (based on files)     │  │
│  └────────────┘  └────────────┘    │ │  └────────────────────────┘  │
│         │               │           │ │              │               │
│         ▼               ▼           │ │              ▼               │
│  ┌────────────┐  ┌────────────┐    │ │  ┌────────────────────────┐  │
│  │  Docker    │  │Test        │    │ │  │   Add Size Label       │  │
│  │  Build     │  │Coverage    │    │ │  │   (lines changed)      │  │
│  └────────────┘  └────────────┘    │ │  └────────────────────────┘  │
│         │               │           │ │              │               │
│         └───────┬───────┘           │ │              ▼               │
│                 ▼                   │ │  ┌────────────────────────┐  │
│         ┌────────────┐              │ │  │   Post Welcome Comment │  │
│         │  Summary   │              │ │  │   (first-time contrib) │  │
│         │  Report    │              │ │  └────────────────────────┘  │
│         └────────────┘              │ │                              │
└──────────────────────────────────────┘ └──────────────────────────────┘
                    │                             │
                    │                             │
              ✅ All checks pass            ✅ PR approved
                    │                             │
                    └──────────────┬──────────────┘
                                   │
                            ┌──────▼──────┐
                            │    MERGE    │
                            │   to main   │
                            └──────┬──────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
    ┌────▼─────┐           ┌──────▼──────┐         ┌───────▼───────┐
    │Performance│          │   Create     │         │  Dependency   │
    │Monitoring │          │   Release    │         │   Updates     │
    │ (weekly)  │          │   Tag        │         │   (weekly)    │
    └───────────┘          └──────┬───────┘         └───────────────┘
                                  │
                          ┌───────▼────────┐
                          │ DOCKER PUBLISH │
                          │(docker-publish)│
                          ├────────────────┤
                          │ • Build image  │
                          │ • Push to GHCR │
                          │ • Scan (Trivy) │
                          │ • Generate SBOM│
                          └────────────────┘
```

---

## 📊 Workflow Execution Matrix

| Event | CI Pipeline | PR Checks | Docker Publish | Dependency Update | Performance |
|-------|------------|-----------|----------------|-------------------|-------------|
| Push to `main` | ✅ | ❌ | ❌ | ❌ | ✅ |
| Push to `develop` | ✅ | ❌ | ❌ | ❌ | ❌ |
| PR opened | ✅ | ✅ | ❌ | ❌ | ✅ |
| PR updated | ✅ | ✅ | ❌ | ❌ | ❌ |
| Release published | ❌ | ❌ | ✅ | ❌ | ❌ |
| Weekly (Monday) | ❌ | ❌ | ❌ | ✅ | ❌ |
| Manual trigger | ✅ | ❌ | ✅ | ✅ | ✅ |

---

## 🎯 Job Dependencies

### CI Pipeline Jobs

```
                    ┌──────────┐
                    │   Lint   │
                    └────┬─────┘
                         │
         ┌───────────────┼───────────────┬──────────────┐
         │               │               │              │
    ┌────▼────┐   ┌──────▼──────┐ ┌─────▼─────┐ ┌──────▼──────┐
    │Security │   │Health Check │ │Type Check │ │Test Coverage│
    └────┬────┘   └──────┬──────┘ └─────┬─────┘ └──────┬──────┘
         │               │               │              │
         └───────────────┼───────────────┼──────────────┘
                         │               │
                    ┌────▼───────────────▼───┐
                    │   Docker Build Test    │
                    └────────────┬───────────┘
                                 │
                         ┌───────▼────────┐
                         │    Summary     │
                         └────────────────┘

Legend:
  → : Sequential (must wait for previous)
  ║ : Parallel (can run simultaneously)
```

---

## 🔐 Security Scanning Flow

```
┌────────────────────────────────────────────────────────────┐
│                    SECURITY WORKFLOW                        │
└────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
         ┌────▼────┐    ┌─────▼─────┐   ┌────▼────┐
         │ Safety  │    │  Bandit   │   │Trufflehog│
         │ (deps)  │    │  (code)   │   │(secrets) │
         └────┬────┘    └─────┬─────┘   └────┬─────┘
              │               │               │
              └───────────────┼───────────────┘
                              │
                      ┌───────▼────────┐
                      │  Trivy (Docker)│
                      │   (on release)  │
                      └────────────────┘
                              │
                      ┌───────▼────────┐
                      │Upload to GitHub│
                      │   Security Tab │
                      └────────────────┘
```

**Checks for**:
- 🔍 Known vulnerabilities in dependencies (Safety)
- 🐛 Common security issues in Python code (Bandit)
- 🔑 Accidentally committed secrets (Trufflehog)
- 🐳 Container vulnerabilities (Trivy)

---

## 📦 Docker Publishing Flow

```
┌─────────────────────────────────────────────────────────────┐
│              DOCKER PUBLISH WORKFLOW                         │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Trigger Event    │
                    │ • Release         │
                    │ • Manual          │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Extract Metadata │
                    │  • Version tag    │
                    │  • Commit SHA     │
                    │  • Labels         │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │   Build Image     │
                    │   (with cache)    │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Push to ghcr.io  │
                    │  • latest         │
                    │  • v1.0.0         │
                    │  • sha-abc123     │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Generate SBOM    │
                    │  (vulnerability)   │
                    │  (tracking)       │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │   Scan Image      │
                    │   (Trivy)         │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │Upload to Security │
                    │       Tab         │
                    └───────────────────┘
```

**Resulting Tags**:
- `ghcr.io/username/repo:latest`
- `ghcr.io/username/repo:v1.0.0`
- `ghcr.io/username/repo:1.0`
- `ghcr.io/username/repo:sha-abc123`

---

## 🏷️ Auto-Labeling Logic

```
┌─────────────────────────────────────────────────────────────┐
│                    PR AUTO-LABELING                          │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   PR Opened       │
                    │   or Updated      │
                    └─────────┬─────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
         ┌────▼────────┐              ┌───────▼────────┐
         │ Analyze     │              │  Count Lines   │
         │ Changed     │              │  Changed       │
         │ Files       │              │                │
         └────┬────────┘              └───────┬────────┘
              │                               │
    ┌─────────┴─────────┐                    │
    │                   │                    │
┌───▼───┐          ┌────▼────┐        ┌──────▼──────┐
│*.md   │          │pages/*  │        │ < 10 lines  │
│docs/* │          │ui_*.py  │        │   → size/xs │
│       │          │         │        └─────────────┘
└───┬───┘          └────┬────┘        ┌──────────────┐
    │                   │             │ 10-100 lines │
    ▼                   ▼             │   → size/s   │
┌───────────┐     ┌─────────┐        └──────────────┘
│documentation│    │   ui    │        ┌──────────────┐
└───────────┘     └─────────┘        │100-500 lines │
                                     │   → size/m   │
┌──────────────────────────┐         └──────────────┘
│  Apply Labels to PR      │         ┌──────────────┐
│  • Category labels       │         │500-1000 lines│
│  • Size labels           │         │   → size/l   │
│  • Auto-assigned         │         └──────────────┘
└──────────────────────────┘         ┌──────────────┐
                                     │ > 1000 lines │
                                     │   → size/xl  │
                                     └──────────────┘
```

---

## ⏰ Scheduled Workflows

```
Monday        Wednesday      Friday         Sunday
9 AM UTC      (none)         (none)         (none)
   │
   ▼
┌──────────────────┐
│ Dependency       │
│ Updates          │
├──────────────────┤
│ 1. Check updates │
│ 2. Run health    │
│ 3. Create PR     │
└──────────────────┘
```

**Cron Schedule**:
- `0 9 * * 1` = Every Monday at 9:00 AM UTC

---

## 🎮 Manual Workflow Triggers

All workflows support manual triggering via `workflow_dispatch`:

```bash
# Using GitHub CLI
gh workflow run ci.yml
gh workflow run docker-publish.yml --field tag=v1.0.0
gh workflow run dependency-update.yml
gh workflow run performance.yml

# Or via GitHub UI
# Actions → Select workflow → Run workflow button
```

---

## 📈 Metrics Dashboard (Conceptual)

```
┌────────────────────────────────────────────────────────────┐
│                     CI/CD METRICS                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Success Rate: ████████████████████░░  95%                │
│  Avg Build Time: 8m 32s                                   │
│  Docker Size: 1.2 GB                                      │
│                                                            │
│  Last 7 Days:                                             │
│  ✅ Passed: 42    ❌ Failed: 2    ⏸️  Cancelled: 1        │
│                                                            │
│  Top Failures:                                            │
│  1. Docker timeout (1)                                    │
│  2. Linting errors (1)                                    │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

View actual metrics in: **Insights → Actions**

---

## 🔄 Full Lifecycle Example

### Feature Development

```
Day 1: Developer creates feature branch
       └─→ git checkout -b feat/new-chatbot

Day 2: Developer pushes code
       └─→ git push origin feat/new-chatbot

Day 3: Developer opens PR
       └─→ PR Checks workflow runs
           ├─→ Title validated ✅
           ├─→ Auto-labeled: ui, backend
           ├─→ Size: m (250 lines)
           └─→ Welcome comment posted

Day 4: CI Pipeline runs on PR
       └─→ All checks pass ✅

Day 5: Maintainer reviews and approves
       └─→ PR merged to main

Day 6: CI Pipeline runs on main
       └─→ All checks pass ✅
       └─→ Performance monitoring runs

Day 7: Create release v1.2.0
       └─→ Docker Publish workflow runs
           ├─→ Build image ✅
           ├─→ Push to ghcr.io ✅
           ├─→ Security scan ✅
           └─→ SBOM generated ✅
```

---

## 🎓 Quick Reference

| Task | Command |
|------|---------|
| View workflows | `gh workflow list` |
| Run workflow | `gh workflow run <workflow-name>` |
| View runs | `gh run list --workflow=<workflow-name>` |
| View logs | `gh run view <run-id> --log` |
| Create labels | `.github/setup-labels.sh` |
| Trigger manually | GitHub UI → Actions → Run workflow |

---

**Last Updated**: 2025-01-12
**Visual Guide Version**: 1.0
