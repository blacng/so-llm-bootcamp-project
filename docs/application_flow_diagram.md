# Application Flow Diagram

## Overview

The LLM Bootcamp Project is an enterprise-grade conversational AI platform built with **Streamlit**, **LangChain**, and **LangGraph**. It provides four distinct chatbot implementations with intelligent document processing, web search integration, and advanced agent capabilities.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface Layer                     │
│                        (Streamlit Frontend)                      │
├─────────────────────────────────────────────────────────────────┤
│  Home.py  │  Basic Chat  │  Agent Chat  │  RAG Chat  │  MCP    │
│  (Landing)│  (Page 1)    │  (Page 2)    │  (Page 3)  │ (Page 4)│
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    UI Components Layer                           │
│                     (ui_components.py)                           │
├─────────────────────────────────────────────────────────────────┤
│  • ChatbotUI (Chat interface, avatars, styling)                 │
│  • HomePageUI (Landing page, hero sections, feature cards)      │
│  • APIKeyUI (API key forms and validation)                      │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                          │
│                    (langchain_helpers.py)                        │
├─────────────────────────────────────────────────────────────────┤
│  BasicChatbotHelper  │  AgentChatbotHelper  │  RAGHelper        │
│  MCPHelper           │  PIIHelper           │  ValidationHelper │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Integration Layer                             │
├─────────────────────────────────────────────────────────────────┤
│  • LangChain (LLM orchestration)                                │
│  • LangGraph (Workflow management)                              │
│  • OpenAI API (GPT-4o, GPT-4o-mini)                            │
│  • Tavily API (Web search)                                      │
│  • FAISS (Vector storage)                                       │
│  • Presidio (PII detection/anonymization)                       │
│  • MCP Protocol (Agent tools)                                   │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data Persistence Layer                      │
├─────────────────────────────────────────────────────────────────┤
│  • tmp/ (File uploads, PDFs)                                    │
│  • tmp/vectorstores/ (FAISS indexes, cache metadata)            │
│  • Session State (Conversation history, agent instances)        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Entry Point & Navigation

```
Home.py (Landing Page)
│
├─── Page Configuration
│    ├── Title: "LLM Bootcamp Project"
│    ├── Icon: 🤖
│    └── Layout: Wide
│
├─── Hero Section (HomePageUI)
│    ├── Welcome message
│    ├── Feature highlights
│    └── Navigation links
│
└─── Page Registry
     ├── 1_Basic_Chatbot.py
     ├── 2_Chatbot_Agent.py
     ├── 3_Chat_with_your_Data.py
     └── 4_MCP_Agent.py
```

---

## Page-Specific Flows

### Page 1: Basic Chatbot Flow

```
User → 1_Basic_Chatbot.py
         │
         ├─── API Key Configuration
         │    └── ValidationHelper.validate_openai_key()
         │
         ├─── Response Style Selection
         │    ├── Professional
         │    ├── Casual
         │    ├── Creative
         │    ├── Technical
         │    └── Balanced
         │
         ├─── BasicChatbotHelper.build_chain()
         │    ├── Create ChatOpenAI instance
         │    ├── Apply system prompt based on style
         │    └── Build LangChain pipeline
         │
         ├─── User Input (st.chat_input)
         │
         ├─── BasicChatbotHelper.invoke_with_memory()
         │    ├── Convert chat history to LangChain format
         │    ├── Invoke chain with context
         │    └── Return AI response
         │
         └─── Display Response (ChatbotUI)
              └── Update session state
```

**Key Features:**
- 5 response styles with customizable system prompts
- Conversation memory via session state
- Configurable temperature, max tokens, top_p, penalties

---

### Page 2: Search-Enabled Chat (Agent) Flow

```
User → 2_Chatbot_Agent.py
         │
         ├─── API Key Configuration
         │    ├── OpenAI API Key
         │    └── Tavily API Key (tvly-*)
         │
         ├─── AgentChatbotHelper.setup_agent()
         │    ├── Create ChatOpenAI instance
         │    ├── Initialize TavilySearchResults tool
         │    ├── Create ReAct agent executor
         │    └── Enable streaming
         │
         ├─── User Query (st.chat_input)
         │
         ├─── AgentChatbotHelper.process_agent_response()
         │    ├── Invoke agent with streaming
         │    ├── Process agent steps:
         │    │   ├── Thought (reasoning)
         │    │   ├── Action (tool selection)
         │    │   ├── Observation (tool result)
         │    │   └── Final Answer
         │    └── Format and display response
         │
         └─── Display Response with Search Context
              ├── Show agent reasoning steps
              ├── Display search results
              └── Present final answer
```

**Key Features:**
- ReAct agent pattern (Reasoning + Acting)
- Tavily web search integration
- Streaming agent responses
- Transparent reasoning display

---

### Page 3: RAG (Chat with Your Data) Flow

```
User → 3_Chat_with_your_Data.py
         │
         ├─── API Key Configuration
         │
         ├─── PII & Performance Settings (Expandable)
         │    ├── PII Detection Toggle
         │    │   ├── Anonymization Method (replace/mask/hash/redact)
         │    │   └── Query PII Detection
         │    └── Smart Caching Toggle
         │
         ├─── Document Upload (PDF)
         │    └── st.file_uploader()
         │
         ├─── Document Processing Pipeline
         │    │
         │    ├─── RAGHelper.setup_rag_system()
         │    │    │
         │    │    ├─── Cache Check
         │    │    │    ├── Generate cache key (files + PII settings)
         │    │    │    ├── Check tmp/vectorstores/
         │    │    │    └── Load from cache if exists
         │    │    │
         │    │    ├─── RAGHelper.build_vectorstore()
         │    │    │    │
         │    │    │    ├─── Load PDFs (PyPDFLoader)
         │    │    │    │
         │    │    │    ├─── PII Detection (if enabled)
         │    │    │    │    ├── PIIHelper.detect_pii()
         │    │    │    │    │   └── Presidio AnalyzerEngine
         │    │    │    │    └── PIIHelper.anonymize_text()
         │    │    │    │        └── Presidio AnonymizerEngine
         │    │    │    │
         │    │    │    ├─── Text Splitting
         │    │    │    │    └── RecursiveCharacterTextSplitter
         │    │    │    │        ├── chunk_size: 1000
         │    │    │    │        └── chunk_overlap: 200
         │    │    │    │
         │    │    │    ├─── Create Embeddings
         │    │    │    │    └── OpenAIEmbeddings
         │    │    │    │
         │    │    │    ├─── Build FAISS Index
         │    │    │    │    └── FAISS.from_documents()
         │    │    │    │
         │    │    │    └─── Cache to Disk (if enabled)
         │    │    │         ├── Save FAISS index
         │    │    │         ├── Save PII entities JSON
         │    │    │         └── Save metadata
         │    │    │
         │    │    └─── RAGHelper.build_simple_agentic_rag()
         │    │         │
         │    │         └─── LangGraph Workflow
         │    │              │
         │    │              ├─── Node 1: classify_mode
         │    │              │    ├── Analyze query keywords
         │    │              │    ├── SUMMARY_HINTS: "summarize", "overview", "key points"
         │    │              │    ├── FACT_HINTS: "when", "who", "where", "amount"
         │    │              │    └── Set mode: "summary" or "fact"
         │    │              │
         │    │              ├─── Node 2: retrieve
         │    │              │    ├── Retrieve documents from FAISS
         │    │              │    ├── Summary mode: 8 documents
         │    │              │    └── Fact mode: 3 documents
         │    │              │
         │    │              └─── Node 3: generate
         │    │                   ├── Build context from documents
         │    │                   ├── Select prompt template (summary/fact)
         │    │                   ├── Invoke ChatOpenAI (gpt-4o-mini)
         │    │                   └── Return grounded response
         │    │
         │    └─── Display PII Report (if detected)
         │
         ├─── User Query (st.chat_input)
         │    │
         │    ├─── Query PII Detection (if enabled)
         │    │    └── Warn user if sensitive info detected
         │    │
         │    └─── RAG Workflow Invocation
         │         └── rag_app.invoke({"question": query})
         │
         ├─── Response PII Safety Layer
         │    ├── Detect PII leakage in response
         │    ├── Anonymize if found
         │    └── Show privacy alert
         │
         └─── Display Response (ChatbotUI)
```

**Key Features:**
- **Agentic RAG**: Automatic query classification (summary vs. fact)
- **PII Protection**: Multi-layer detection and anonymization
  - Document-level anonymization before embedding
  - Query-level PII detection
  - Response-level safety checks
- **Smart Caching**: Hash-based cache with 7-day expiration
- **Presidio Integration**: Enterprise-grade PII detection
  - Entities: PERSON, EMAIL, PHONE, SSN, CREDIT_CARD, etc.
  - Methods: replace, mask, hash, redact

---

### Page 4: MCP Agent Flow

```
User → 4_MCP_Agent.py
         │
         ├─── API Key Configuration
         │    ├── OpenAI API Key
         │    └── MCP Server URL
         │
         ├─── Agent Initialization
         │    └── MCPHelper.get_agent()
         │         ├── Connect to MCP server
         │         ├── Discover available tools
         │         └── Create agent instance (singleton)
         │
         ├─── User Query (st.chat_input)
         │
         ├─── MCPHelper.process_mcp_query()
         │    ├── Format messages for MCP protocol
         │    ├── Invoke agent with tools
         │    └── Handle tool calls and responses
         │
         └─── Display Response
              └── Show tool usage and results
```

**Key Features:**
- Model Context Protocol integration
- Dynamic tool discovery
- Singleton agent pattern (agent_service.py)
- Extensible tool ecosystem

---

## Helper Classes Architecture

### langchain_helpers.py

```
┌─────────────────────────────────────────────────────────────┐
│                   BasicChatbotHelper                         │
├─────────────────────────────────────────────────────────────┤
│  build_chain(config, api_key)                               │
│  ├── Create ChatOpenAI with parameters                      │
│  ├── Configure system prompt by style                       │
│  └── Build ChatPromptTemplate pipeline                      │
│                                                              │
│  invoke_with_memory(chain, user_input, chat_history)       │
│  ├── Convert history to LangChain format                    │
│  └── Invoke chain with context                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                 AgentChatbotHelper                           │
├─────────────────────────────────────────────────────────────┤
│  setup_agent(openai_key, tavily_key)                        │
│  ├── Initialize TavilySearchResults                         │
│  ├── Create ReAct agent with tools                          │
│  └── Enable streaming                                        │
│                                                              │
│  process_agent_response(agent_executor, messages)           │
│  └── Stream agent steps and format output                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      RAGHelper                               │
├─────────────────────────────────────────────────────────────┤
│  Cache Management:                                           │
│  ├── _generate_cache_key(files, anonymize_pii, pii_method) │
│  ├── _get_cache_path(cache_key)                            │
│  ├── _save_to_cache(vector_store, pii_entities, ...)       │
│  ├── _load_from_cache(cache_key, api_key)                  │
│  ├── cleanup_old_caches() [7-day expiration]               │
│  └── get_cache_statistics()                                 │
│                                                              │
│  Document Processing:                                        │
│  ├── save_file(file, folder)                               │
│  ├── build_vectorstore(files, api_key, anonymize_pii, ...) │
│  │   ├── Check cache first                                  │
│  │   ├── Load & split PDFs                                  │
│  │   ├── Detect & anonymize PII (optional)                 │
│  │   ├── Create embeddings (OpenAI)                         │
│  │   ├── Build FAISS index                                  │
│  │   └── Save to cache                                      │
│  │                                                           │
│  └── build_simple_agentic_rag(retriever, llm)              │
│      └── LangGraph StateGraph:                              │
│          ├── classify_mode → determine query type           │
│          ├── retrieve → fetch relevant docs                 │
│          └── generate → create grounded response            │
│                                                              │
│  Main Entry:                                                 │
│  └── setup_rag_system(files, api_key, anonymize_pii, ...)  │
│      ├── Cleanup old caches                                 │
│      ├── Build vectorstore (with cache)                     │
│      ├── Create retriever                                   │
│      └── Build RAG workflow                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      PIIHelper                               │
├─────────────────────────────────────────────────────────────┤
│  _check_presidio_available() → bool                         │
│  _get_analyzer() → AnalyzerEngine (singleton)               │
│  _get_anonymizer() → AnonymizerEngine (singleton)           │
│                                                              │
│  is_available() → bool                                       │
│                                                              │
│  detect_pii(text, language, entities, score_threshold)     │
│  └── Returns: List[Dict] with PII entities                  │
│                                                              │
│  anonymize_text(text, method, entities, score_threshold)   │
│  ├── Methods: replace, mask, hash, redact                   │
│  └── Returns: (anonymized_text, detected_entities)          │
│                                                              │
│  get_pii_statistics(pii_entities) → Dict                    │
│  └── Count by entity type                                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   ValidationHelper                           │
├─────────────────────────────────────────────────────────────┤
│  validate_openai_key(key) → bool                            │
│  ├── Check format: sk-proj-...                             │
│  └── Minimum length validation                              │
│                                                              │
│  validate_tavily_key(key) → bool                            │
│  ├── Check format: tvly-...                                │
│  └── Minimum length validation                              │
│                                                              │
│  validate_url(url) → bool                                   │
│  └── HTTP/HTTPS scheme validation                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      MCPHelper                               │
├─────────────────────────────────────────────────────────────┤
│  get_agent(openai_api_key, mcp_server_url)                 │
│  └── Delegates to agent_service.get_agent()                 │
│                                                              │
│  process_mcp_query(agent, messages) → str                   │
│  ├── Invoke agent with messages                             │
│  └── Handle errors gracefully                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### RAG Document Processing Pipeline

```
PDF Upload
    ↓
┌─────────────────────┐
│  Cache Key Check    │
│  MD5(files + PII)   │
└─────────────────────┘
    ↓
  [Cache Hit?]
    ↓ No
┌─────────────────────┐
│  PyPDFLoader        │
│  Load PDF Content   │
└─────────────────────┘
    ↓
┌─────────────────────┐
│  PII Detection      │ ← [If enabled]
│  (Presidio)         │
└─────────────────────┘
    ↓
┌─────────────────────┐
│  Text Splitting     │
│  RecursiveChars     │
│  1000/200           │
└─────────────────────┘
    ↓
┌─────────────────────┐
│  Anonymization      │ ← [If enabled]
│  (Presidio)         │
└─────────────────────┘
    ↓
┌─────────────────────┐
│  Embedding          │
│  OpenAIEmbeddings   │
└─────────────────────┘
    ↓
┌─────────────────────┐
│  FAISS Index        │
│  Vector Store       │
└─────────────────────┘
    ↓
┌─────────────────────┐
│  Cache Save         │
│  tmp/vectorstores/  │
│  ├─ index.faiss     │
│  ├─ index.pkl       │
│  ├─ metadata.json   │
│  └─ pii_entities.json│
└─────────────────────┘
    ↓
  Ready for Queries
```

### RAG Query Processing (LangGraph)

```
User Query: "Summarize the key findings"
    ↓
┌─────────────────────┐
│  classify_mode      │
│  Analyze keywords   │
│  → mode: "summary" │
└─────────────────────┘
    ↓
┌─────────────────────┐
│  retrieve           │
│  FAISS Search       │
│  → 8 documents      │
└─────────────────────┘
    ↓
┌─────────────────────┐
│  generate           │
│  ChatOpenAI         │
│  Summary Prompt     │
└─────────────────────┘
    ↓
┌─────────────────────┐
│  PII Safety Check   │ ← [If enabled]
│  Scan response      │
└─────────────────────┘
    ↓
Response to User
```

---

## Session State Management

### Streamlit Session State Keys

```python
# Basic Chatbot (Page 1)
st.session_state.basic_openai_key          # API key
st.session_state.basic_messages            # Chat history
st.session_state.basic_chain               # LangChain chain
st.session_state.basic_key_connected       # Connection flag

# Agent Chatbot (Page 2)
st.session_state.agent_openai_key          # OpenAI API key
st.session_state.agent_tavily_key          # Tavily API key
st.session_state.agent_messages            # Chat history
st.session_state.agent_executor            # ReAct agent
st.session_state.agent_keys_connected      # Connection flag

# RAG Chat (Page 3)
st.session_state.rag_openai_key            # API key
st.session_state.rag_uploaded_files        # PDF files
st.session_state.rag_app                   # RAG workflow
st.session_state.rag_messages              # Chat history
st.session_state.rag_anonymize_pii         # PII toggle
st.session_state.rag_pii_method            # Anonymization method
st.session_state.rag_pii_entities          # Detected PII
st.session_state.rag_detect_query_pii      # Query PII detection
st.session_state.rag_use_cache             # Cache toggle
st.session_state.rag_processing            # Processing flag
st.session_state.rag_last_query_pii        # Last query PII info

# MCP Agent (Page 4)
st.session_state.mcp_openai_key            # OpenAI API key
st.session_state.mcp_server_url            # MCP server URL
st.session_state.mcp_messages              # Chat history
st.session_state.mcp_agent                 # MCP agent instance
st.session_state.mcp_keys_connected        # Connection flag
```

---

## File System Structure

```
so-llm-bootcamp-project/
│
├── Home.py                      # Landing page & navigation
│
├── pages/                       # Streamlit pages
│   ├── 1_Basic_Chatbot.py      # Simple conversational AI
│   ├── 2_Chatbot_Agent.py      # Web search enabled agent
│   ├── 3_Chat_with_your_Data.py # RAG with PII protection
│   └── 4_MCP_Agent.py          # MCP integration
│
├── langchain_helpers.py         # Core AI/ML logic
│   ├── BasicChatbotHelper
│   ├── AgentChatbotHelper
│   ├── RAGHelper
│   ├── MCPHelper
│   ├── PIIHelper
│   └── ValidationHelper
│
├── ui_components.py             # Reusable UI components
│   ├── ChatbotUI
│   ├── HomePageUI
│   └── APIKeyUI
│
├── agent_service.py             # MCP agent singleton
│
├── server.py                    # FastMCP server (prompt optimization)
│
├── healthcheck.py               # Docker health checks
│
├── tmp/                         # Runtime data
│   ├── *.pdf                    # Uploaded documents
│   └── vectorstores/            # FAISS cache
│       ├── {cache_key}/
│       │   ├── index.faiss      # Vector index
│       │   ├── index.pkl        # FAISS metadata
│       │   ├── metadata.json    # Cache metadata
│       │   └── pii_entities.json # Detected PII
│
├── Dockerfile                   # Container definition
├── docker-compose.yml           # Service orchestration
├── Makefile                     # Infrastructure commands
├── pyproject.toml               # uv dependencies
└── .env                         # Environment variables
```

---

## Technology Stack

### Frontend
- **Streamlit** 1.28.0+ - Web UI framework
- **Custom CSS** - Enhanced dark theme styling

### Backend
- **LangChain** - LLM orchestration
  - langchain-core 0.3.75
  - langchain-openai 0.3.32
  - langchain-community 0.3.29
- **LangGraph** 0.6.6 - Workflow graphs
- **LangChain MCP Adapters** 0.1.9 - MCP integration

### AI/ML
- **OpenAI API** - GPT-4o, GPT-4o-mini
- **OpenAI Embeddings** - text-embedding-3-small
- **FAISS** 1.12.0 - Vector similarity search
- **Tavily** 0.7.1 - Web search

### Privacy & Security
- **Presidio Analyzer** 2.2.0+ - PII detection
- **Presidio Anonymizer** 2.2.0+ - PII anonymization
- **spaCy** 3.7.0+ - NLP (en_core_web_lg)

### Document Processing
- **PyPDF** 6.0.0 - PDF parsing
- **RecursiveCharacterTextSplitter** - Text chunking

### Infrastructure
- **Docker** - Containerization
- **uv** - Fast Python package manager
- **Make** - Build automation

---

## API Requirements

### Required for All Features
- **OpenAI API Key**: `sk-proj-...`
  - Models: gpt-4o-mini, gpt-4o
  - Embeddings: text-embedding-3-small

### Feature-Specific
- **Tavily API Key**: `tvly-...` (Search-Enabled Chat)
- **MCP Server URL**: `http://mcp-server:8000` (MCP Agent)

---

## Performance Optimizations

### 1. FAISS Caching
- **Location**: `tmp/vectorstores/{cache_key}/`
- **Key Generation**: MD5(file_info + PII_settings)
- **Expiration**: 7 days
- **Size Limit**: 500 MB
- **Benefits**: Instant reload on page refresh

### 2. Singleton Patterns
- **MCP Agent**: One instance per server URL
- **Presidio Engines**: Lazy-loaded singletons
  - AnalyzerEngine
  - AnonymizerEngine

### 3. Multi-Stage Docker Build
- **Builder Stage**: Install dependencies
- **Final Stage**: Copy only runtime artifacts
- **Result**: Optimized image size

### 4. Lazy Loading
- PII detection libraries loaded on-demand
- spaCy model loaded only when needed

---

## Security Features

### 1. PII Protection (3-Layer Defense)
```
Layer 1: Document Processing
├── Detect PII before embedding
├── Anonymize using Presidio
└── Never store sensitive data in vectors

Layer 2: Query Detection
├── Scan user queries for PII
├── Warn users before submission
└── Optional: block queries with PII

Layer 3: Response Safety
├── Scan AI responses for PII leakage
├── Anonymize any detected PII
└── Alert user with privacy warning
```

### 2. API Key Validation
- Format validation before storage
- Keys stored in session state (not persistent)
- Option to use environment variables

### 3. File Permissions
- Cache files: 0600 (owner-only)
- Prevents unauthorized access

### 4. Input Sanitization
- URL validation for MCP server
- File type restrictions (PDF only)

---

## Deployment Architecture

### Development Mode
```
Host Machine
    ├── uv run streamlit run Home.py
    ├── Port: 8501-8503
    └── Live code reload
```

### Docker Production Mode
```
Docker Container (llm-bootcamp-app)
    ├── Multi-stage build
    ├── uv for dependency management
    ├── Health checks every 30s
    ├── Persistent volumes:
    │   └── ./tmp → /app/tmp
    ├── Port: 8502:8501
    └── Auto-restart: unless-stopped

Optional: MCP Server Container
    ├── FastMCP server
    ├── Port: 8000:8000
    └── Profile: mcp
```

### Network
```
llm-bootcamp-network (Docker bridge)
    ├── streamlit-app (8502)
    └── mcp-server (8000)
```

---

## Error Handling

### 1. API Key Validation
```python
if not ValidationHelper.validate_openai_key(key):
    st.error("❌ Invalid key format")
    return False
```

### 2. Cache Failures
```python
try:
    vector_store = load_from_cache(cache_key)
except Exception as e:
    print(f"⚠️ Cache failed: {e}")
    # Fallback to fresh processing
```

### 3. PII Detection Unavailable
```python
if not PIIHelper.is_available():
    st.warning("⚠️ PII detection not available")
    # Continue without PII protection
```

### 4. Agent Errors
```python
try:
    response = await agent.invoke(messages)
except Exception as e:
    return f"❌ Agent Error: {str(e)}"
```

---

## Future Enhancements

### Planned Features
1. **Multi-format Support**: DOCX, TXT, CSV
2. **Advanced RAG**: Hybrid search, reranking
3. **User Authentication**: Multi-user support
4. **Conversation Export**: Download chat history
5. **Custom Embedding Models**: Support for other providers
6. **GPU Acceleration**: FAISS-GPU for large datasets
7. **Metrics Dashboard**: Usage analytics

---

## Troubleshooting Guide

### Common Issues

**1. Port Already in Use**
```bash
# Check port usage
lsof -i :8501

# Kill process
kill -9 <PID>

# Use different port in docker-compose.yml
ports:
  - "8503:8501"
```

**2. Cache Not Loading**
```bash
# Clear cache
make clean-cache

# Or manually
rm -rf tmp/vectorstores/*
```

**3. PII Detection Failed**
```bash
# Install dependencies
pip install presidio-analyzer presidio-anonymizer
python -m spacy download en_core_web_lg
```

**4. Docker Build Fails**
```bash
# Clean rebuild
make clean
make rebuild
```

---

## Monitoring & Health Checks

### Health Check Endpoint
- **URL**: `http://localhost:8502/_stcore/health`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Implementation**: `healthcheck.py`

### Log Monitoring
```bash
# All logs
make logs

# Application only
make logs-app

# MCP server only
make logs-mcp
```

### Resource Monitoring
```bash
# Container stats
make stats

# Output: CPU, Memory, Network I/O
```

---

## Development Workflow

### 1. Local Development
```bash
# Install dependencies
uv sync

# Run application
uv run streamlit run Home.py

# Run tests
uv run pytest

# Lint code
make lint

# Format code
make format
```

### 2. Docker Development
```bash
# Build and start
make up

# View logs
make logs

# Access shell
make shell

# Restart
make restart
```

### 3. Code Changes
```
Edit code → Docker auto-reloads (development mode)
           → Changes reflected immediately
```

---

## Conclusion

This application demonstrates enterprise-grade AI application development with:

✅ **Modular Architecture** - Helper class pattern for clean separation
✅ **Advanced RAG** - Intelligent query classification with LangGraph
✅ **Privacy-First** - Multi-layer PII protection with Presidio
✅ **Performance** - Smart caching and optimization
✅ **Production-Ready** - Docker, health checks, monitoring
✅ **Developer-Friendly** - Clear abstractions, comprehensive docs

The architecture balances **simplicity** (easy to understand), **scalability** (can handle growth), and **security** (privacy-protected by design).
