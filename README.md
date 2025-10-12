# AI Chatbot Platform

An enterprise-grade conversational AI platform featuring intelligent agents, document processing, web search integration, and adaptive prompt optimization through Model Context Protocol.

## 🚀 Quick Start

```bash
cd project_code/
pip install -r requirements.txt
streamlit run Home.py
```

## 📁 System Architecture

```
├── pages/                 # Chatbot interfaces
│   ├── 1_Basic_Chatbot.py
│   ├── 2_Chatbot_Agent.py
│   ├── 3_Chat_with_your_Data.py
│   └── 4_MCP_Agent.py
├── Home.py                # Application entry point
├── langchain_helpers.py   # AI integration layer
├── ui_components.py       # Reusable UI components
├── config.py              # Secure configuration
├── agent_service.py       # MCP agent orchestration
├── server.py              # MCP optimization server
├── docker-compose.yml     # Container orchestration
├── Makefile               # Infrastructure management
├── .github/workflows/     # CI/CD pipelines
└── docs/                  # Documentation
```

## Platform Capabilities

### Four AI Chatbot Implementations

1. **Basic Chatbot**
   - Conversational AI with memory and context awareness
   - 5 customizable response styles (Professional, Casual, Creative, Technical, Balanced)
   - Secure API key management with environment variable support

2. **Chatbot Agent**
   - Real-time web search integration using Tavily API
   - Intelligent information retrieval and research capabilities
   - Streaming responses with timeout protection

3. **Chat with your Data**
   - PDF document processing with RAG (Retrieval-Augmented Generation)
   - Agentic workflow with automatic query classification
   - PII detection and anonymization support
   - Smart caching for instant document reload

4. **MCP Agent**
   - Model Context Protocol integration for extensible AI capabilities
   - Tool access and enhanced context management
   - Feedback-driven prompt optimization using LangMem

## 🔄 CI/CD Pipeline

This project uses GitHub Actions for automated testing, security scanning, and deployment.

### Workflows

| Workflow | Status | Description |
|----------|--------|-------------|
| CI/CD Pipeline | ![CI](https://github.com/blacng/so-llm-bootcamp-project/workflows/CI%2FCD%20Pipeline/badge.svg) | Code quality, testing, security |
| Docker Publish | ![Docker](https://github.com/blacng/so-llm-bootcamp-project/workflows/Docker%20Publish/badge.svg) | Build and publish Docker images |
| PR Checks | ![PR](https://github.com/blacng/so-llm-bootcamp-project/workflows/Pull%20Request%20Checks/badge.svg) | PR validation and auto-labeling |

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

## Deployment

1. **System Setup**
   ```bash
   git clone <repository>
   cd llmbootcamp-project/project_code/
   pip install -r requirements.txt
   ```

2. **Configuration**
   - OpenAI API key for language models
   - Tavily API key for web search
   - MCP server endpoint configuration

3. **Launch**
   ```bash
   streamlit run Home.py
   ```

4. **Access**
   - Navigate through 4 different AI interfaces
   - Configure agents for specific use cases
   - Upload documents for analysis