---
marp: true
theme: default
paginate: true
backgroundColor: #fff
style: |
  section {
    font-family: 'Arial', sans-serif;
  }
  h1 {
    color: #0066cc;
  }
  h2 {
    color: #0066cc;
  }
  code {
    background-color: #f4f4f4;
    padding: 2px 6px;
    border-radius: 3px;
  }
  .columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# LangGraph Agent Architecture

## LLM Bootcamp Project
### Agentic RAG & ReAct Agents

---

# Overview

## Two Main LangGraph Implementations:

### 🔷 **Agentic RAG Workflow**
Intelligent document question-answering with adaptive retrieval

### 🔶 **ReAct Agent**
Web search-enabled conversational AI with tool-calling capability

---

# Agentic RAG Workflow Architecture

## Linear Flow Diagram:

```
┌─────────┐    ┌──────────────┐    ┌──────────┐    ┌──────────┐    ┌─────┐
│  START  │───▶│ classify_mode│───▶│ retrieve │───▶│ generate │───▶│ END │
└─────────┘    └──────────────┘    └──────────┘    └──────────┘    └─────┘
   Entry         Classify query      Fetch docs      Create          Exit
                 type (summary/      (3 or 8 docs)   response
                 fact mode)
```

**Key Feature**: Linear workflow with no conditional edges or loops

---

# RAG Workflow Nodes

## 🔹 **classify_mode**
Analyzes query to determine `"summary"` or `"fact"` mode
- **Summary hints**: "summarize", "overview", "key points"
- **Fact hints**: "when", "who", "where", "amount", "specific"

## 🔹 **retrieve**
Fetches documents from FAISS vector store
- **Summary mode**: 8 documents (broader context)
- **Fact mode**: 3 documents (focused retrieval)

## 🔹 **generate**
Creates grounded response using only retrieved context
- No external knowledge used
- Mode-specific prompts

---

# RAG State Management

## RAGState (TypedDict):

```python
class RAGState(TypedDict):
    question: str                       # User's query (input)
    mode: Literal["summary", "fact"]   # Response strategy
    documents: List[Document]           # Retrieved context
    generation: str                     # Final response (output)
```

**Type-safe state** ensures proper data flow between nodes

---

# RAG Key Features

✅ **Linear Workflow**
   No conditional edges or loops - predictable flow

✅ **Mode-Adaptive Retrieval**
   Different strategies for summaries vs. facts

✅ **Grounded Generation**
   Responses strictly based on retrieved documents

✅ **Type-Safe State**
   TypedDict ensures proper data flow between nodes

✅ **PII Anonymization**
   Optional privacy protection using Presidio

✅ **Vector Store Caching**
   Faster reloads with FAISS cache (7-day TTL)

---

# ReAct Agent Architecture

## Cyclic Flow Diagram:

```
                    ┌─────────┐
                    │  START  │
                    └────┬────┘
                         │
                         ▼
                  ┌─────────────┐
              ┌──▶│ Agent Node  │──── No ───▶ END
              │   │ (LLM)       │
              │   └──────┬──────┘
              │          │ Yes (tool call)
              │          ▼
              │   ┌─────────────┐
              └───│ Tools Node  │
                  │ (Tavily)    │
                  └─────────────┘
```

**Key Feature**: Cyclic workflow - can loop multiple times for complex queries

---

# ReAct Agent Features

✅ **Cyclic Workflow**
   Can loop multiple times for complex queries

✅ **Tool Integration**
   Tavily web search with 5 results per query

✅ **Conditional Edges**
   LLM decides when to use tools vs. respond

✅ **Streaming Support**
   Real-time response updates

✅ **Timeout Protection**
   90-second default timeout

✅ **Multi-Step Reasoning**
   Can chain multiple searches together

---

# RAG vs. ReAct Agent Comparison

| Feature | Agentic RAG | ReAct Agent |
|---------|-------------|-------------|
| **Purpose** | Document QA | Web search + Chat |
| **Data Source** | Uploaded PDFs | Real-time web (Tavily) |
| **Graph Type** | Linear (fixed) | Cyclic (loops) |
| **Nodes** | 3 agent nodes | 2 nodes (agent + tools) |
| **Conditional Logic** | None | Yes (tool decisions) |
| **Response Mode** | Adaptive (2 modes) | Single strategy |
| **Streaming** | Not implemented | Supported |
| **Context** | Strict (docs only) | Flexible (web + LLM) |

---

# When to Use Each Agent

<div class="columns">
<div>

## 🟦 Agentic RAG

**Use When:**
- You have proprietary documents (PDFs, reports)
- Need factually grounded responses
- Require citation to source material
- Want consistent, reproducible answers
- Privacy is critical (on-premises data)

</div>
<div>

## 🟧 ReAct Agent

**Use When:**
- Need current information (news, prices, events)
- Want broad web knowledge
- Require multi-step reasoning
- Need to combine multiple sources
- Real-time data is essential

</div>
</div>

---

# Implementation Example: RAG

```python
# RAG Workflow Setup
from langchain_helpers import RAGHelper

# Build RAG system with uploaded PDFs
rag_workflow, pii_entities = RAGHelper.setup_rag_system(
    uploaded_files,
    api_key=openai_key,
    anonymize_pii=True,    # Optional PII protection
    use_cache=True         # Enable caching
)

# Process query
result = rag_workflow.invoke({
    "question": "What are the key findings?"
})

answer = result["generation"]
```

**File**: `langchain_helpers.py:730-781`

---

# Implementation Example: ReAct

```python
# ReAct Agent Setup
from langchain_helpers import AgentChatbotHelper

# Create agent with Tavily search
agent = AgentChatbotHelper.setup_agent(
    openai_api_key=openai_key,
    tavily_api_key=tavily_key
)

# Process query (async)
response = await AgentChatbotHelper.process_agent_response(
    agent=agent,
    user_query="What are the latest AI developments in 2025?",
    timeout=90
)

print(response)
```

**File**: `langchain_helpers.py:129-228`

---

# Graph Construction: RAG

```python
from langgraph.graph import StateGraph, END

# Build the workflow graph
graph = StateGraph(RAGState)

# Add nodes
graph.add_node("classify_mode", classify_mode)
graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)

# Define edges (linear flow)
graph.set_entry_point("classify_mode")
graph.add_edge("classify_mode", "retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

# Compile the graph
rag_workflow = graph.compile()
```

---

# Graph Construction: ReAct

```python
from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI

# Configure search tool
tavily_search = TavilySearch(
    max_results=5,
    topic="general",
    tavily_api_key=tavily_api_key
)

# Create ReAct agent (pre-built graph)
llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)
agent = create_react_agent(llm, tools=[tavily_search])

# Agent automatically handles:
# - Tool calling decisions
# - Looping logic
# - Response streaming
```

---

# File References

### **Core Implementation**
- `langchain_helpers.py:591-728` - RAGHelper.build_simple_agentic_rag()
- `langchain_helpers.py:730-781` - RAGHelper.setup_rag_system()
- `langchain_helpers.py:129-228` - AgentChatbotHelper (ReAct)

### **Streamlit Pages**
- `pages/3_📄_RAG_Document_Chat.py` - RAG interface
- `pages/2_🔎_Search-Enabled_Chat.py` - ReAct interface

### **Configuration**
- `config.py` - Secure API key management
- `ui_components.py` - Reusable UI components
- `CLAUDE.md` - Full architecture documentation

---

# Advanced: Node Functions

```python
def classify_mode(state: RAGState) -> RAGState:
    """Classify query type to determine response strategy."""
    query_lower = state["question"].lower()

    if any(hint in query_lower for hint in SUMMARY_HINTS):
        mode = "summary"
    elif any(hint in query_lower for hint in FACT_HINTS):
        mode = "fact"
    else:
        mode = "fact"  # Default

    return {**state, "mode": mode}

def retrieve(state: RAGState) -> RAGState:
    """Retrieve relevant documents based on mode."""
    num_docs = 8 if state["mode"] == "summary" else 3
    docs = retriever.invoke(state["question"])
    return {**state, "documents": docs[:num_docs]}
```

---

# Advanced: Caching System

## Vector Store Caching Features:

- **Automatic cache key generation** based on files + settings
- **7-day TTL** for cache expiration
- **Metadata tracking**: file count, vector count, PII stats
- **Automatic cleanup** of old caches
- **Permission security**: Owner-only access (600)

```python
# Cache is transparent to users
rag_workflow, pii = RAGHelper.setup_rag_system(
    files,
    use_cache=True  # ✅ First run: builds cache
                    # ✅ Subsequent runs: loads from cache
)
```

**Location**: `tmp/vectorstores/{cache_key}/`

---

# Security: PII Anonymization

## Presidio Integration:

```python
# Detect PII in documents
entities = PIIHelper.detect_pii(text)
# Returns: [{'type': 'PERSON', 'score': 0.85, 'text': 'John'}]

# Anonymize text
anonymized, entities = PIIHelper.anonymize_text(
    text,
    method="replace",  # Options: replace, mask, hash, redact
    entities_to_anonymize=["PERSON", "EMAIL_ADDRESS"]
)

# Integrated into RAG
rag_workflow, pii = RAGHelper.setup_rag_system(
    files,
    anonymize_pii=True,
    pii_method="replace"
)
```

**File**: `langchain_helpers.py:824-1179`

---

# Visualizing the Graphs

## Using LangGraph's Built-in Visualization:

```python
from IPython.display import Image, display

# Compile the graph
rag_workflow = graph.compile()

# Generate visualization
display(Image(rag_workflow.get_graph().draw_mermaid_png()))
```

**Available in**: `langgraph_visualization.ipynb`

## Alternative: Mermaid Diagrams

Both agents can be visualized using Mermaid syntax in markdown, documentation, or GitHub README files.

---

# Performance Optimizations

### **RAG Workflow**
- ✅ FAISS vector store (fast similarity search)
- ✅ Caching system (instant reload for same files)
- ✅ Chunk size optimization (1500 chars, 200 overlap)
- ✅ Batch processing for multiple files

### **ReAct Agent**
- ✅ Streaming responses (real-time output)
- ✅ Timeout protection (prevents hanging)
- ✅ Async processing (non-blocking I/O)
- ✅ Connection pooling (Tavily API)

### **Both**
- ✅ OpenAI API key caching
- ✅ Singleton pattern for agents
- ✅ Error handling and retry logic

---

# Integration with Streamlit

```python
# In pages/3_📄_RAG_Document_Chat.py

import streamlit as st
from langchain_helpers import RAGHelper

# File uploader
uploaded_files = st.file_uploader(
    "Upload PDF documents",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    # Setup RAG
    with st.spinner("Processing documents..."):
        rag, pii = RAGHelper.setup_rag_system(
            uploaded_files,
            api_key=st.session_state.openai_key
        )

    # Query interface
    query = st.chat_input("Ask about your documents")
    if query:
        result = rag.invoke({"question": query})
        st.write(result["generation"])
```

---

# Key Takeaways

✅ **Both agents use typed state management** for reliability

✅ **RAG provides grounded, factual responses** from documents

✅ **ReAct enables real-time web search** and multi-step reasoning

✅ **Graphs are compiled and optimized** by LangGraph

✅ **Production-ready** with caching, PII protection, and error handling

✅ **Easily extensible** with custom nodes and tools

---

# Next Steps

1. **Try the Agents**
   ```bash
   streamlit run Home.py
   ```

2. **Upload Documents**
   Test RAG workflow with your PDFs

3. **Web Search**
   Try ReAct agent for current events

4. **Customize**
   Modify node logic in `langchain_helpers.py`

5. **Explore Notebook**
   See `langgraph_visualization.ipynb`

6. **Read Docs**
   Check `CLAUDE.md` for full architecture

---

# Resources

### **Documentation**
- `CLAUDE.md` - Project overview and architecture
- `README.md` - Setup and installation guide
- `langgraph_visualization.ipynb` - Interactive notebook

### **Code**
- `langchain_helpers.py` - Core implementation
- `agent_service.py` - MCP agent singleton
- `server.py` - FastMCP prompt optimization server

### **Community**
- LangGraph Docs: https://langchain-ai.github.io/langgraph/
- LangChain Docs: https://python.langchain.com/

---

<!-- _class: lead -->
<!-- _paginate: false -->

# Questions?

## Contact & Resources

**GitHub**: Review the codebase at `so-llm-bootcamp-project`
**Documentation**: See `CLAUDE.md` for detailed architecture
**Jupyter Notebook**: `langgraph_visualization.ipynb` for interactive examples

### Thank you!

---

# Appendix: State Types

```python
# RAG State (Strongly Typed)
class RAGState(TypedDict):
    question: str
    mode: Literal["summary", "fact"]
    documents: List[Document]
    generation: str

# ReAct State (Message-Based)
{
    "messages": [
        {"role": "user", "content": "query"},
        {"role": "assistant", "content": "...", "tool_calls": [...]},
        {"role": "tool", "content": "search results"},
        {"role": "assistant", "content": "final response"}
    ]
}
```

---

# Appendix: Error Handling

```python
# RAG Error Handling
try:
    result = rag_workflow.invoke({"question": query})
    if not result["generation"]:
        return "No relevant information found."
except Exception as e:
    logger.error(f"RAG error: {e}")
    return "Error processing request."

# ReAct Error Handling
try:
    response = await asyncio.wait_for(
        agent.invoke({"messages": query}),
        timeout=90
    )
except asyncio.TimeoutError:
    return "Query timed out. Try a simpler question."
except Exception as e:
    return f"Agent error: {str(e)}"
```
