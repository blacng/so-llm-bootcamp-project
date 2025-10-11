# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

An enterprise-grade conversational AI platform built with Streamlit, LangChain, and LangGraph. Features four distinct AI chatbot implementations: Basic Chat, Search-Enabled Chat (with Tavily), RAG Document Chat, and MCP Agent integration.

## Development Commands

### Running the Application
```bash
streamlit run Home.py
```

### Testing
The project uses `uv` for dependency management:
```bash
# Install dependencies
uv sync

# Run with uv
uv run streamlit run Home.py
```

## Architecture

### Core Structure
- **Home.py** - Main entry point and landing page with navigation
- **langchain_helpers.py** - Centralized AI/ML functionality organized into helper classes
- **agent_service.py** - MCP agent implementation with singleton pattern
- **server.py** - FastMCP server for prompt optimization using LangMem
- **ui_components.py** - Reusable UI components and styling (ChatbotUI, HomePageUI, APIKeyUI)
- **config.py** - Centralized configuration management for secure API key handling
- **pages/** - Four Streamlit pages for different chatbot implementations

### Helper Classes Architecture (langchain_helpers.py)

The codebase uses a **helper class pattern** to organize functionality by chatbot type:

1. **BasicChatbotHelper** - Simple conversational AI
   - `build_chain()`: Creates LangChain chain with customizable response styles
   - `invoke_with_memory()`: Handles conversation history
   - Supports 5 response styles: Professional, Casual, Creative, Technical, Balanced

2. **AgentChatbotHelper** - Web search integration
   - `setup_agent()`: Creates ReAct agent with Tavily search tools
   - `process_agent_response()`: Handles streaming agent responses

3. **RAGHelper** - Document processing and question-answering
   - `build_vectorstore()`: Creates FAISS vector store from PDFs
   - `build_simple_agentic_rag()`: Constructs intelligent RAG workflow with LangGraph
   - Uses **agentic RAG workflow**: Automatically classifies queries as "summary" or "fact" mode, retrieves appropriate number of documents (8 for summary, 3 for facts), and generates grounded responses

4. **MCPHelper** - Model Context Protocol integration
   - `get_agent()`: Creates MCP-powered agent with tool access
   - `process_mcp_query()`: Processes queries through MCP agent

5. **ValidationHelper** - Input validation for API keys and URLs

### MCP Server (server.py)

FastMCP server providing prompt optimization tools:
- `optimize_prompt()`: Single-feedback optimization using LangMem
- `batch_optimize_prompt()`: Multi-feedback batch optimization
- `get_optimization_history()`: Retrieve past optimizations
- `get_latest_optimized_prompt()`: Get most recent optimized prompt
- Persistent storage in `tmp/optimization_history.json`

### UI Components Pattern

All UI styling and components are centralized in **ui_components.py**:
- **ChatbotUI**: Chat interface components, enhanced dark theme, avatars
- **HomePageUI**: Landing page hero sections and feature cards
- **APIKeyUI**: API key configuration forms with validation

Pages should use these components instead of duplicating styling code.

## API Requirements & Security

### Required API Keys
- **OpenAI API Key**: Required for all chatbot implementations (models: gpt-4o-mini, gpt-4o)
- **Tavily API Key**: Required for Search-Enabled Chat (format: `tvly-*`)
- **MCP Server URL**: Required for MCP Agent (HTTP/HTTPS endpoints)

### Secure API Key Management

The application implements a **layered security approach** for API key management through the centralized `config.py` module:

#### Priority Order (Most Secure to Least Secure)
1. **Docker Secrets** (Production) - `/run/secrets/`
2. **Environment Variables** (Development/Production) - `.env` file or system env
3. **User Input** (Development Fallback) - Streamlit UI forms

#### Configuration Module (config.py)

The `Config` class provides secure API key retrieval:

```python
from config import Config

# Get API keys with automatic fallback
openai_key = Config.get_openai_key()
tavily_key = Config.get_tavily_key()
mcp_url = Config.get_mcp_server_url()

# Check environment mode
if Config.is_production():
    # Stricter validation in production
    pass
```

#### Environment Variables Setup

1. **Copy the example file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your API keys**:
   ```bash
   OPENAI_API_KEY=sk-proj-your-key-here
   TAVILY_API_KEY=tvly-your-key-here
   MCP_SERVER_URL=http://localhost:8000
   ENVIRONMENT=development
   ```

3. **Verify `.env` is in `.gitignore`** (already configured)

#### Docker Secrets (Production)

For production deployments using Docker:

1. **Create secrets directory**:
   ```bash
   mkdir -p secrets
   echo "your-openai-key" > secrets/openai_api_key.txt
   echo "your-tavily-key" > secrets/tavily_api_key.txt
   echo "http://mcp-server:8000" > secrets/mcp_server_url.txt
   chmod 600 secrets/*
   ```

2. **Uncomment secrets in `docker-compose.yml`**:
   ```yaml
   services:
     streamlit-app:
       secrets:
         - openai_api_key
         - tavily_api_key
         - mcp_server_url

   secrets:
     openai_api_key:
       file: ./secrets/openai_api_key.txt
     tavily_api_key:
       file: ./secrets/tavily_api_key.txt
     mcp_server_url:
       file: ./secrets/mcp_server_url.txt
   ```

3. **Add `secrets/` to `.gitignore`** (recommended)

#### Security Best Practices

- ✅ **Never commit** `.env` or `secrets/` to version control
- ✅ **Rotate keys regularly** (every 90 days minimum)
- ✅ **Use environment variables** in production, not UI input
- ✅ **Enable production mode** by setting `ENVIRONMENT=production` in `.env`
- ✅ **Use read-only or scoped keys** when possible
- ✅ **Monitor API usage** for unusual activity
- ✅ **Never log API keys** - the config module prevents logging

#### Page-Level Implementation

All Streamlit pages automatically check for environment variables first:

```python
from config import Config

# In page configuration functions:
env_key = Config.get_openai_key()

if env_key:
    # Use secure key from environment
    st.session_state["openai_key"] = env_key
    st.info("🔐 Using API key from secure configuration")
else:
    # Fallback to user input (development mode)
    st.warning("⚠️ No API key found in environment")
    # Show input form...
```

This ensures production deployments never expose API key input forms.

## Key Patterns

1. **Helper Class Pattern**: All AI/ML logic is organized into static helper classes in `langchain_helpers.py`
2. **Singleton Pattern**: MCP agents use singleton pattern via `get_agent()` in `agent_service.py`
3. **LangGraph Workflows**: RAG uses StateGraph for intelligent query classification and routing
4. **Centralized UI**: All styling and reusable components live in `ui_components.py`
5. **Centralized Config**: API keys managed securely through `config.py` with layered security
6. **Session State**: Streamlit session state manages chat history and initialized agents
7. **Streaming Support**: Agent responses support streaming for better UX

## File Storage

- **tmp/** - Temporary storage for uploaded PDFs and optimization history
- Documents are processed in-memory after loading from tmp/

## Response Modes (RAG)

The RAG system intelligently determines response strategy:
- **Summary Mode**: Triggered by "summarize", "overview", "key points" - retrieves 8 documents
- **Fact Mode**: Triggered by "when", "who", "where", "amount", "specific" - retrieves 3 documents
- Both modes generate grounded responses using only retrieved context
- Use uv for package management
- Use docker and docker-compose to containerize this application
- Use make for infrastructure management
- Use ruff for linting and code formatting