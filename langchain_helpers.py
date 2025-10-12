"""LangChain Helper Functions.

Centralized AI/ML functionality for the LLM Bootcamp Project.
Provides helper classes for different types of chatbot functionality:
- BasicChatbotHelper: Simple conversational AI
- AgentChatbotHelper: AI with web search capabilities
- RAGHelper: Retrieval-Augmented Generation for documents
- MCPHelper: Model Context Protocol integration
- PIIHelper: PII detection and anonymization utilities
- ValidationHelper: Input validation utilities
"""

import os
import hashlib
import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, TypedDict, Literal, Tuple, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph, END


class BasicChatbotHelper:
    """Helper class for basic conversational chatbot functionality.

    Provides utilities to create and manage simple AI chatbots with
    customizable response styles and conversation memory.
    """

    @staticmethod
    def build_chain(config: Dict[str, Any], api_key: str = None) -> Any:
        """Build a LangChain chain for basic chatbot functionality.

        Creates a conversational chain with customizable LLM parameters
        and response styles (Professional, Casual, Creative, Technical, Balanced).

        Args:
            config: Configuration dictionary with model settings
            api_key: Optional OpenAI API key override

        Returns:
            Configured LangChain chain ready for conversation
        """
        llm_kwargs = {
            "model": config["model"],
            "temperature": config["temperature"],
            "max_tokens": config["max_tokens"],
            "top_p": config.get("top_p", 1.0),
            "frequency_penalty": config.get("frequency_penalty", 0.0),
            "presence_penalty": config.get("presence_penalty", 0.0),
            "streaming": False,
        }

        if api_key:
            llm_kwargs["api_key"] = api_key

        llm = ChatOpenAI(**llm_kwargs)

        # Configure response style with predefined system prompts
        system_prompts = {
            "Professional": "You are a professional AI assistant. Provide formal, detailed, and well-structured responses suitable for business contexts.",
            "Casual": "You are a friendly and casual AI assistant. Use conversational language and be approachable in your responses.",
            "Creative": "You are a creative AI assistant. Provide imaginative, engaging responses with varied perspectives and creative insights.",
            "Technical": "You are a technical AI assistant. Provide precise, detailed explanations with technical accuracy and clarity.",
            "Balanced": config.get(
                "system_prompt",
                "You are a helpful AI assistant. Provide clear, concise, and friendly responses.",
            ),
        }

        system_message = system_prompts.get(
            config.get("response_style", "Balanced"), system_prompts["Balanced"]
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
            ]
        )

        return prompt | llm

    @staticmethod
    def invoke_with_memory(
        chain: Any, user_input: str, chat_history: List[Dict[str, str]]
    ) -> Any:
        """Invoke the chain with conversation memory support.

        Processes user input while maintaining context from previous messages
        in the conversation history.

        Args:
            chain: The LangChain chain to invoke
            user_input: Current user message
            chat_history: List of previous conversation messages

        Returns:
            Chain response with conversation context
        """
        # Convert chat history to LangChain message format
        formatted_history = []
        for msg in chat_history[:-1]:  # Exclude the current user message
            if msg["role"] == "user":
                formatted_history.append(("human", msg["content"]))
            elif msg["role"] == "assistant":
                formatted_history.append(("assistant", msg["content"]))

        return chain.invoke({"input": user_input, "chat_history": formatted_history})

    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Get default configuration for basic chatbot.

        Returns:
            Dictionary with default model settings optimized for conversation
        """
        return {"model": "gpt-4o-mini", "temperature": 0.7, "max_tokens": 2000}


class AgentChatbotHelper:
    """Helper class for agent chatbot with real-time web search functionality.

    Integrates with Tavily search API to provide AI agents with the ability
    to search and retrieve current information from the web.
    """

    @staticmethod
    def setup_agent(openai_api_key: str, tavily_api_key: str) -> Any:
        """Setup an AI agent with Tavily web search capabilities.

        Creates a ReAct agent that can search the web for real-time information
        to supplement its responses.

        Args:
            openai_api_key: OpenAI API key for LLM access
            tavily_api_key: Tavily API key for web search functionality

        Returns:
            Configured LangGraph ReAct agent with search tools
        """
        from langchain_tavily import TavilySearch
        from langgraph.prebuilt import create_react_agent

        # Configure Tavily search tool with optimal settings
        tavily_search = TavilySearch(
            max_results=5,
            topic="general",
            tavily_api_key=tavily_api_key,
        )

        tools = [tavily_search]

        llm = ChatOpenAI(model="gpt-4o-mini", streaming=True, api_key=openai_api_key)
        agent = create_react_agent(llm, tools)
        return agent

    @staticmethod
    async def process_agent_response(
        agent: Any, user_query: str, timeout: int = 90
    ) -> str:
        """Process agent response with streaming support and timeout.

        Handles the agent's reasoning and tool usage steps, collecting
        all output into a cohesive response.

        Args:
            agent: The configured LangGraph agent
            user_query: User's question or request
            timeout: Maximum time in seconds to wait for response (default: 90)

        Returns:
            Complete agent response as a string

        Raises:
            asyncio.TimeoutError: If the response takes longer than timeout seconds
        """
        import asyncio

        async def _process():
            accumulated_response = ""

            # Stream state updates (includes reasoning and tool execution steps)
            for update in agent.stream({"messages": user_query}):
                messages = update.get("messages", [])
                for message in messages:
                    content = getattr(message, "content", "")

                    # Handle structured content (list of content blocks)
                    if not content and isinstance(
                        getattr(message, "content", None), list
                    ):
                        content = "".join(
                            block.get("text", "")
                            for block in message.content
                            if isinstance(block, dict) and block.get("type") == "text"
                        )

                    if content:
                        accumulated_response += content

            # Fallback to direct invocation if streaming failed
            if not accumulated_response:
                response = agent.invoke({"messages": user_query})
                accumulated_response = (
                    response["messages"][-1].content
                    if isinstance(response, dict) and response.get("messages")
                    else str(response)
                )

            return accumulated_response

        # Apply timeout to the entire process
        try:
            return await asyncio.wait_for(_process(), timeout=timeout)
        except asyncio.TimeoutError:
            raise asyncio.TimeoutError(
                f"Agent response timed out after {timeout} seconds. The web search may be taking too long or the API may be unavailable."
            )


class RAGHelper:
    """Helper class for RAG (Retrieval-Augmented Generation) functionality.

    Provides document processing, vector storage, and intelligent retrieval
    capabilities for question-answering over user documents.
    """

    # Type definition for RAG workflow state management
    class RAGState(TypedDict):
        question: str
        mode: Literal["summary", "fact"]
        documents: List[Document]
        generation: str

    # Cache configuration
    CACHE_DIR = Path("tmp/vectorstores")
    MAX_CACHE_AGE_DAYS = 7
    MAX_CACHE_SIZE_MB = 500

    @staticmethod
    def _generate_cache_key(files, anonymize_pii: bool, pii_method: str) -> str:
        """Generate unique cache key based on files and PII settings.

        Args:
            files: List of uploaded files
            anonymize_pii: Whether PII anonymization is enabled
            pii_method: PII anonymization method used

        Returns:
            MD5 hash string as cache key
        """
        hasher = hashlib.md5()

        # Hash file information (name + size for quick check)
        # Note: Not hashing full content for performance
        file_info = []
        for file in sorted(files, key=lambda f: f.name):
            file_info.append((file.name, file.size))

        hasher.update(str(file_info).encode())

        # Hash PII settings
        settings_str = f"{anonymize_pii}_{pii_method}"
        hasher.update(settings_str.encode())

        return hasher.hexdigest()[:16]

    @staticmethod
    def _get_cache_path(cache_key: str) -> Path:
        """Get cache directory path for a given cache key.

        Args:
            cache_key: Unique cache identifier

        Returns:
            Path object for the cache directory
        """
        cache_path = RAGHelper.CACHE_DIR / cache_key
        cache_path.mkdir(parents=True, exist_ok=True)
        return cache_path

    @staticmethod
    def _save_to_cache(
        vector_store: FAISS,
        pii_entities: List[Dict],
        cache_key: str,
        files,
        settings: Dict,
    ):
        """Save vector store and metadata to cache.

        Args:
            vector_store: FAISS vector store to cache
            pii_entities: List of detected PII entities
            cache_key: Unique cache identifier
            files: List of uploaded files
            settings: PII settings used
        """
        cache_path = RAGHelper._get_cache_path(cache_key)

        try:
            # Save FAISS vector store
            vector_store.save_local(str(cache_path))

            # Save PII entities
            pii_file = cache_path / "pii_entities.json"
            with open(pii_file, "w") as f:
                json.dump(pii_entities, f, indent=2)

            # Save metadata
            metadata = {
                "cache_key": cache_key,
                "created_at": datetime.now().isoformat(),
                "files": [{"name": f.name, "size": f.size} for f in files],
                "file_count": len(files),
                "settings": settings,
                "pii_entity_count": len(pii_entities),
                "vector_count": vector_store.index.ntotal,
                "dimension": vector_store.index.d,
            }

            metadata_file = cache_path / "metadata.json"
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=2)

            # Set restrictive permissions (owner only)
            try:
                for item in cache_path.rglob("*"):
                    if item.is_file():
                        os.chmod(item, 0o600)
            except Exception:
                pass  # Permission setting may fail on Windows

            print(f"💾 Cached vector store: {cache_key}")

        except Exception as e:
            print(f"⚠️ Failed to save cache: {e}")

    @staticmethod
    def _load_from_cache(
        cache_key: str, api_key: str
    ) -> Optional[Tuple[FAISS, List[Dict]]]:
        """Load vector store and PII entities from cache.

        Args:
            cache_key: Unique cache identifier
            api_key: OpenAI API key for embeddings

        Returns:
            Tuple of (vector_store, pii_entities) if cache exists, None otherwise
        """
        cache_path = RAGHelper._get_cache_path(cache_key)
        index_file = cache_path / "index.faiss"

        if not index_file.exists():
            return None

        try:
            # Check cache age
            metadata_file = cache_path / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file) as f:
                    metadata = json.load(f)
                    created = datetime.fromisoformat(metadata["created_at"])
                    age = datetime.now() - created

                    if age > timedelta(days=RAGHelper.MAX_CACHE_AGE_DAYS):
                        print(f"⚠️ Cache expired (age: {age.days} days)")
                        return None

            # Load vector store
            embeddings_kwargs = {}
            if api_key:
                embeddings_kwargs["api_key"] = api_key

            embeddings = OpenAIEmbeddings(**embeddings_kwargs)
            vector_store = FAISS.load_local(
                str(cache_path), embeddings, allow_dangerous_deserialization=True
            )

            # Load PII entities
            pii_file = cache_path / "pii_entities.json"
            pii_entities = []
            if pii_file.exists():
                with open(pii_file) as f:
                    pii_entities = json.load(f)

            print(f"✅ Loaded from cache: {cache_key}")
            return vector_store, pii_entities

        except Exception as e:
            print(f"⚠️ Failed to load cache: {e}")
            return None

    @staticmethod
    def cleanup_old_caches():
        """Remove caches older than MAX_CACHE_AGE_DAYS."""
        if not RAGHelper.CACHE_DIR.exists():
            return

        cutoff = datetime.now() - timedelta(days=RAGHelper.MAX_CACHE_AGE_DAYS)
        removed_count = 0

        for cache_dir in RAGHelper.CACHE_DIR.iterdir():
            if not cache_dir.is_dir():
                continue

            metadata_file = cache_dir / "metadata.json"
            if metadata_file.exists():
                try:
                    with open(metadata_file) as f:
                        metadata = json.load(f)
                        created = datetime.fromisoformat(metadata["created_at"])

                        if created < cutoff:
                            shutil.rmtree(cache_dir)
                            removed_count += 1
                            print(f"🗑️ Removed old cache: {cache_dir.name}")
                except Exception as e:
                    print(f"⚠️ Error cleaning cache {cache_dir.name}: {e}")

        if removed_count > 0:
            print(f"Cleaned up {removed_count} old cache(s)")

    @staticmethod
    def get_cache_statistics() -> Dict[str, Any]:
        """Get statistics about cached vector stores.

        Returns:
            Dictionary with cache statistics
        """
        if not RAGHelper.CACHE_DIR.exists():
            return {
                "total_caches": 0,
                "total_size_mb": 0,
                "oldest_cache": None,
                "newest_cache": None,
            }

        caches = []
        total_size = 0

        for cache_dir in RAGHelper.CACHE_DIR.iterdir():
            if not cache_dir.is_dir():
                continue

            # Calculate size
            cache_size = sum(
                f.stat().st_size for f in cache_dir.rglob("*") if f.is_file()
            )
            total_size += cache_size

            # Read metadata
            metadata_file = cache_dir / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file) as f:
                    metadata = json.load(f)
                    metadata["size_mb"] = cache_size / (1024 * 1024)
                    caches.append(metadata)

        caches.sort(key=lambda x: x["created_at"])

        return {
            "total_caches": len(caches),
            "total_size_mb": total_size / (1024 * 1024),
            "oldest_cache": caches[0] if caches else None,
            "newest_cache": caches[-1] if caches else None,
            "caches": caches,
        }

    @staticmethod
    def save_file(file, folder: str = "tmp") -> str:
        """Save uploaded file to local storage.

        Args:
            file: Streamlit uploaded file object
            folder: Directory to save the file (created if doesn't exist)

        Returns:
            Full path to the saved file
        """
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getvalue())
        return file_path

    @staticmethod
    def build_vectorstore(
        files,
        api_key: str = None,
        anonymize_pii: bool = False,
        pii_method: str = "replace",
        pii_entities: Optional[List[str]] = None,
        use_cache: bool = True,
    ) -> Tuple[FAISS, List[Dict[str, Any]]]:
        """Build FAISS vector store from uploaded PDF files with optional PII anonymization and caching.

        Processes PDF files, optionally anonymizes PII, splits them into chunks,
        creates embeddings, and builds a searchable vector database. Supports caching
        for faster reloads.

        Args:
            files: List of uploaded PDF files
            api_key: Optional OpenAI API key for embeddings
            anonymize_pii: Whether to detect and anonymize PII (default: False)
            pii_method: Anonymization method - "replace", "mask", "hash", or "redact"
            pii_entities: List of specific PII types to anonymize (None = all types)
            use_cache: Whether to use caching (default: True)

        Returns:
            Tuple of (FAISS vector store, list of all detected PII entities)
        """
        # Generate cache key based on files and settings
        if use_cache:
            cache_key = RAGHelper._generate_cache_key(files, anonymize_pii, pii_method)

            # Try to load from cache
            cached_result = RAGHelper._load_from_cache(cache_key, api_key)
            if cached_result is not None:
                return cached_result

        # Cache miss or caching disabled - build new vector store
        documents: List[Document] = []
        all_pii_entities: List[Dict[str, Any]] = []

        # Process each uploaded PDF file
        for file in files:
            file_path = RAGHelper.save_file(file)
            loader = PyPDFLoader(file_path)
            loaded_docs = loader.load()

            # Optionally anonymize PII in document content
            if anonymize_pii and PIIHelper.is_available():
                for doc in loaded_docs:
                    # Anonymize the document content
                    anonymized_text, detected_entities = PIIHelper.anonymize_text(
                        doc.page_content,
                        method=pii_method,
                        entities_to_anonymize=pii_entities,
                    )

                    # Update document with anonymized content
                    doc.page_content = anonymized_text

                    # Track detected entities with source file metadata
                    for entity in detected_entities:
                        entity["source_file"] = file.name
                        entity["source_page"] = doc.metadata.get("page", "unknown")
                    all_pii_entities.extend(detected_entities)

            documents.extend(loaded_docs)

        # Split documents into manageable chunks for processing
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500, chunk_overlap=200
        )
        document_chunks = text_splitter.split_documents(documents)

        embeddings_kwargs = {}
        if api_key:
            embeddings_kwargs["api_key"] = api_key

        # Create embeddings and build vector store
        embeddings = OpenAIEmbeddings(**embeddings_kwargs)
        vector_store = FAISS.from_documents(document_chunks, embeddings)

        # Save to cache
        if use_cache:
            settings = {
                "anonymize_pii": anonymize_pii,
                "pii_method": pii_method,
                "pii_entities": pii_entities,
            }
            RAGHelper._save_to_cache(
                vector_store, all_pii_entities, cache_key, files, settings
            )

        return vector_store, all_pii_entities

    @staticmethod
    def build_simple_agentic_rag(retriever, llm: ChatOpenAI):
        """Build an intelligent agentic RAG workflow.

        Creates a graph-based workflow that automatically determines whether
        to provide summaries or specific facts based on the query type.

        Args:
            retriever: Vector store retriever for document search
            llm: Language model for generating responses

        Returns:
            Compiled LangGraph workflow for intelligent document QA
        """

        # Classification node: determine if query needs summary or specific facts
        SUMMARY_HINTS = (
            "summarize",
            "summary",
            "overview",
            "key points",
            "bullet",
            "synthesize",
        )
        FACT_HINTS = (
            "when",
            "date",
            "who",
            "where",
            "amount",
            "total",
            "price",
            "figure",
            "specific",
            "exact",
        )

        def classify_mode(state: RAGHelper.RAGState) -> RAGHelper.RAGState:
            """Classify query type to determine appropriate response mode."""
            query_lower = state["question"].lower()

            # Determine response mode based on query keywords
            if any(hint in query_lower for hint in SUMMARY_HINTS) and not any(
                hint in query_lower for hint in FACT_HINTS
            ):
                mode: Literal["summary", "fact"] = "summary"
            elif any(hint in query_lower for hint in FACT_HINTS):
                mode = "fact"
            else:
                # Default to summary for general questions, fact for specific queries
                mode = (
                    "summary"
                    if "summary" in query_lower or "summarize" in query_lower
                    else "fact"
                )

            return {**state, "mode": mode}

        # Retrieval node: fetch relevant documents based on query type
        def retrieve(state: RAGHelper.RAGState) -> RAGHelper.RAGState:
            """Retrieve relevant documents based on query and mode."""
            question = state["question"]

            # Adjust retrieval count based on response mode
            num_docs = 8 if state["mode"] == "summary" else 3
            retrieved_docs = retriever.invoke(question)

            return {**state, "documents": retrieved_docs[:num_docs]}

        # Generation node: create appropriate response based on mode and context
        gen_prompt_summary = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant. Create a concise, faithful summary ONLY using the provided context. "
                    "Prefer bullet points if helpful. Do not use outside knowledge.",
                ),
                (
                    "human",
                    "Question:\n{question}\n\n"
                    "Context (multiple document chunks):\n{context}\n\n"
                    "Write a grounded summary:",
                ),
            ]
        )

        gen_prompt_fact = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant. Answer precisely and ONLY using the provided context. "
                    "If the context is insufficient, say so.",
                ),
                ("human", "Question:\n{question}\n\nContext:\n{context}\n\nAnswer:"),
            ]
        )

        def generate(state: RAGHelper.RAGState) -> RAGHelper.RAGState:
            """Generate response based on retrieved documents and mode."""
            # Combine retrieved document content
            document_context = "\n\n---\n\n".join(
                doc.page_content for doc in state.get("documents", [])
            )

            # Handle case where no relevant documents found
            if not document_context.strip():
                return {
                    **state,
                    "generation": "I couldn't find enough information in the documents to answer that.",
                }

            # Generate response using appropriate prompt based on mode
            if state["mode"] == "summary":
                response = llm.invoke(
                    gen_prompt_summary.format_messages(
                        question=state["question"], context=document_context
                    )
                )
            else:
                response = llm.invoke(
                    gen_prompt_fact.format_messages(
                        question=state["question"], context=document_context
                    )
                )

            return {**state, "generation": response.content}

        # Construct the workflow graph with connected nodes
        graph = StateGraph(RAGHelper.RAGState)
        graph.add_node("classify_mode", classify_mode)
        graph.add_node("retrieve", retrieve)
        graph.add_node("generate", generate)

        graph.set_entry_point("classify_mode")
        graph.add_edge("classify_mode", "retrieve")
        graph.add_edge("retrieve", "generate")
        graph.add_edge("generate", END)

        return graph.compile()

    @staticmethod
    def setup_rag_system(
        uploaded_files,
        api_key: str = None,
        anonymize_pii: bool = False,
        pii_method: str = "replace",
        pii_entities: Optional[List[str]] = None,
        use_cache: bool = True,
    ) -> Tuple[Any, List[Dict[str, Any]]]:
        """Setup complete RAG system from uploaded files with optional PII anonymization and caching.

        Orchestrates the entire RAG pipeline: file processing, optional PII anonymization,
        vectorization, retriever setup, and workflow creation. Supports caching for faster reloads.

        Args:
            uploaded_files: List of PDF files to process
            api_key: Optional OpenAI API key
            anonymize_pii: Whether to detect and anonymize PII (default: False)
            pii_method: Anonymization method - "replace", "mask", "hash", or "redact"
            pii_entities: List of specific PII types to anonymize (None = all types)
            use_cache: Whether to use caching (default: True)

        Returns:
            Tuple of (RAG workflow ready for query processing, list of detected PII entities)
        """
        # Clean up old caches on setup
        RAGHelper.cleanup_old_caches()

        # Build vector store with optional PII anonymization and caching
        vector_store, pii_entities_detected = RAGHelper.build_vectorstore(
            uploaded_files,
            api_key,
            anonymize_pii=anonymize_pii,
            pii_method=pii_method,
            pii_entities=pii_entities,
            use_cache=use_cache,
        )
        retriever = vector_store.as_retriever()

        # Configure language model for generation
        llm_config = {
            "model": "gpt-4o-mini",
            "temperature": 0,  # Deterministic responses
            "streaming": False,
        }
        if api_key:
            llm_config["api_key"] = api_key

        llm = ChatOpenAI(**llm_config)
        rag_workflow = RAGHelper.build_simple_agentic_rag(retriever, llm)

        return rag_workflow, pii_entities_detected


class MCPHelper:
    """Helper class for Model Context Protocol (MCP) functionality.

    Provides utilities for working with MCP-powered agents that can access
    specialized tools and resources beyond standard LLM capabilities.
    """

    @staticmethod
    async def get_agent(openai_api_key: str, mcp_server_url: str):
        """Get or create an MCP agent instance.

        Args:
            openai_api_key: OpenAI API key for LLM access
            mcp_server_url: URL of the MCP server to connect to

        Returns:
            Initialized MCP agent ready for use
        """
        from agent_service import get_agent

        return await get_agent(openai_api_key, mcp_server_url)

    @staticmethod
    async def process_mcp_query(agent: Any, messages: List[Dict[str, str]]) -> str:
        """Process a query through the MCP agent.

        Args:
            agent: The MCP agent instance
            messages: List of conversation messages

        Returns:
            Agent response as a string, or error message if processing fails
        """
        try:
            response_text = await agent.invoke(messages)
            return response_text
        except Exception as e:
            return f"❌ MCP Agent Error: {str(e)}"


class PIIHelper:
    """Helper class for PII (Personally Identifiable Information) detection and anonymization.

    Provides utilities to detect, anonymize, and manage sensitive information in text
    using Microsoft Presidio for enterprise-grade privacy protection.
    """

    _analyzer = None
    _anonymizer = None
    _analyzer_available = None

    @staticmethod
    def _check_presidio_available() -> bool:
        """Check if Presidio libraries are available.

        Returns:
            True if Presidio is installed and available, False otherwise
        """
        if PIIHelper._analyzer_available is None:
            try:
                from presidio_analyzer import AnalyzerEngine  # noqa: F401
                from presidio_anonymizer import AnonymizerEngine  # noqa: F401

                PIIHelper._analyzer_available = True
            except ImportError:
                PIIHelper._analyzer_available = False

        return PIIHelper._analyzer_available

    @staticmethod
    def _get_analyzer():
        """Get or create singleton AnalyzerEngine instance.

        Returns:
            Presidio AnalyzerEngine instance

        Raises:
            ImportError: If Presidio is not installed
        """
        if not PIIHelper._check_presidio_available():
            raise ImportError(
                "Presidio is not installed. Install with: "
                "pip install presidio-analyzer presidio-anonymizer && "
                "python -m spacy download en_core_web_lg"
            )

        if PIIHelper._analyzer is None:
            from presidio_analyzer import AnalyzerEngine

            PIIHelper._analyzer = AnalyzerEngine()

        return PIIHelper._analyzer

    @staticmethod
    def _get_anonymizer():
        """Get or create singleton AnonymizerEngine instance.

        Returns:
            Presidio AnonymizerEngine instance

        Raises:
            ImportError: If Presidio is not installed
        """
        if not PIIHelper._check_presidio_available():
            raise ImportError(
                "Presidio is not installed. Install with: "
                "pip install presidio-analyzer presidio-anonymizer"
            )

        if PIIHelper._anonymizer is None:
            from presidio_anonymizer import AnonymizerEngine

            PIIHelper._anonymizer = AnonymizerEngine()

        return PIIHelper._anonymizer

    @staticmethod
    def detect_pii(
        text: str,
        entities_to_detect: Optional[List[str]] = None,
        language: str = "en",
        score_threshold: float = 0.5,
    ) -> List[Dict[str, Any]]:
        """Detect PII entities in text.

        Args:
            text: Input text to analyze
            entities_to_detect: List of entity types to detect (None = all types)
                Common types: PERSON, EMAIL_ADDRESS, PHONE_NUMBER, CREDIT_CARD,
                US_SSN, LOCATION, DATE_TIME, MEDICAL_LICENSE, etc.
            language: Language code (default: "en")
            score_threshold: Minimum confidence score (0.0-1.0)

        Returns:
            List of detected entity dictionaries with type, score, position, and text

        Example:
            >>> entities = PIIHelper.detect_pii("John's email is john@example.com")
            >>> print(entities)
            [{'type': 'PERSON', 'score': 0.85, 'start': 0, 'end': 4, 'text': 'John'},
             {'type': 'EMAIL_ADDRESS', 'score': 1.0, 'start': 18, 'end': 35, 'text': 'john@example.com'}]
        """
        try:
            analyzer = PIIHelper._get_analyzer()

            # Analyze text for PII
            results = analyzer.analyze(
                text=text,
                language=language,
                entities=entities_to_detect,
                score_threshold=score_threshold,
            )

            # Convert results to structured format
            detected_entities = [
                {
                    "type": result.entity_type,
                    "score": result.score,
                    "start": result.start,
                    "end": result.end,
                    "text": text[result.start : result.end],
                }
                for result in results
            ]

            return detected_entities

        except Exception as e:
            print(f"Error detecting PII: {e}")
            return []

    @staticmethod
    def anonymize_text(
        text: str,
        method: str = "replace",
        entities_to_anonymize: Optional[List[str]] = None,
        score_threshold: float = 0.5,
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """Detect and anonymize PII in text.

        Args:
            text: Input text to anonymize
            method: Anonymization method - "replace", "mask", "hash", or "redact"
                - replace: Replace with entity type placeholders (e.g., <PERSON>)
                - mask: Replace with asterisks (e.g., ****)
                - hash: Replace with SHA256 hash
                - redact: Remove completely
            entities_to_anonymize: List of entity types to anonymize (None = all)
            score_threshold: Minimum confidence score for detection (0.0-1.0)

        Returns:
            Tuple of (anonymized_text, detected_entities_list)

        Example:
            >>> text = "Call John at 555-1234 or email john@example.com"
            >>> anonymized, entities = PIIHelper.anonymize_text(text, method="replace")
            >>> print(anonymized)
            "Call <PERSON> at <PHONE_NUMBER> or email <EMAIL_ADDRESS>"
        """
        try:
            from presidio_anonymizer.entities import OperatorConfig

            analyzer = PIIHelper._get_analyzer()
            anonymizer = PIIHelper._get_anonymizer()

            # Detect PII entities
            results = analyzer.analyze(
                text=text,
                language="en",
                entities=entities_to_anonymize,
                score_threshold=score_threshold,
            )

            if not results:
                return text, []

            # Configure anonymization operators based on method
            if method == "replace":
                operators = {
                    "DEFAULT": OperatorConfig(
                        "replace", {"new_value": "<{entity_type}>"}
                    ),
                    "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "<PHONE>"}),
                    "EMAIL_ADDRESS": OperatorConfig(
                        "replace", {"new_value": "<EMAIL>"}
                    ),
                    "PERSON": OperatorConfig("replace", {"new_value": "<PERSON>"}),
                    "CREDIT_CARD": OperatorConfig(
                        "replace", {"new_value": "<CREDIT_CARD>"}
                    ),
                    "US_SSN": OperatorConfig("replace", {"new_value": "<SSN>"}),
                    "LOCATION": OperatorConfig("replace", {"new_value": "<LOCATION>"}),
                    "DATE_TIME": OperatorConfig("replace", {"new_value": "<DATE>"}),
                    "US_DRIVER_LICENSE": OperatorConfig(
                        "replace", {"new_value": "<DRIVER_LICENSE>"}
                    ),
                    "US_PASSPORT": OperatorConfig(
                        "replace", {"new_value": "<PASSPORT>"}
                    ),
                    "MEDICAL_LICENSE": OperatorConfig(
                        "replace", {"new_value": "<MEDICAL_LICENSE>"}
                    ),
                    "URL": OperatorConfig("replace", {"new_value": "<URL>"}),
                    "IP_ADDRESS": OperatorConfig(
                        "replace", {"new_value": "<IP_ADDRESS>"}
                    ),
                }
            elif method == "mask":
                operators = {
                    "DEFAULT": OperatorConfig(
                        "mask",
                        {"chars_to_mask": 100, "masking_char": "*", "from_end": False},
                    )
                }
            elif method == "hash":
                operators = {"DEFAULT": OperatorConfig("hash", {"hash_type": "sha256"})}
            elif method == "redact":
                operators = {"DEFAULT": OperatorConfig("redact", {})}
            else:
                raise ValueError(
                    f"Invalid anonymization method: {method}. Use 'replace', 'mask', 'hash', or 'redact'."
                )

            # Anonymize text
            anonymized_result = anonymizer.anonymize(
                text=text, analyzer_results=results, operators=operators
            )

            # Extract detected entity information
            detected_entities = [
                {
                    "type": result.entity_type,
                    "score": result.score,
                    "start": result.start,
                    "end": result.end,
                    "text": text[result.start : result.end],
                }
                for result in results
            ]

            return anonymized_result.text, detected_entities

        except Exception as e:
            print(f"Error anonymizing text: {e}")
            return text, []

    @staticmethod
    def get_pii_statistics(entities: List[Dict[str, Any]]) -> Dict[str, int]:
        """Generate statistics from detected PII entities.

        Args:
            entities: List of detected entity dictionaries

        Returns:
            Dictionary mapping entity types to their occurrence counts

        Example:
            >>> entities = [{'type': 'PERSON', ...}, {'type': 'EMAIL_ADDRESS', ...}, {'type': 'PERSON', ...}]
            >>> stats = PIIHelper.get_pii_statistics(entities)
            >>> print(stats)
            {'PERSON': 2, 'EMAIL_ADDRESS': 1}
        """
        stats = {}
        for entity in entities:
            entity_type = entity.get("type", "UNKNOWN")
            stats[entity_type] = stats.get(entity_type, 0) + 1
        return stats

    @staticmethod
    def format_pii_report(
        entities: List[Dict[str, Any]], include_text: bool = False
    ) -> str:
        """Format detected PII entities into a human-readable report.

        Args:
            entities: List of detected entity dictionaries
            include_text: Whether to include the actual PII text (default: False for security)

        Returns:
            Formatted report string

        Example:
            >>> entities = PIIHelper.detect_pii("Contact John at john@example.com")
            >>> print(PIIHelper.format_pii_report(entities))
            PII Detection Report
            ====================
            Total entities found: 2

            Entity Types:
            - PERSON: 1
            - EMAIL_ADDRESS: 1
        """
        if not entities:
            return "No PII detected."

        stats = PIIHelper.get_pii_statistics(entities)

        report = [
            "PII Detection Report",
            "=" * 20,
            f"Total entities found: {len(entities)}",
            "",
        ]
        report.append("Entity Types:")
        for entity_type, count in sorted(stats.items()):
            report.append(f"- {entity_type}: {count}")

        if include_text:
            report.append("\nDetected Entities:")
            for i, entity in enumerate(entities, 1):
                report.append(
                    f"{i}. {entity['type']} (score: {entity['score']:.2f}): "
                    f"'{entity['text']}' at position {entity['start']}-{entity['end']}"
                )

        return "\n".join(report)

    @staticmethod
    def is_available() -> bool:
        """Check if PII detection functionality is available.

        Returns:
            True if Presidio is installed and ready to use, False otherwise
        """
        return PIIHelper._check_presidio_available()

    @staticmethod
    def get_supported_entities() -> List[str]:
        """Get list of supported PII entity types.

        Returns:
            List of supported entity type names

        Note:
            Requires Presidio to be installed. Returns empty list if not available.
        """
        try:
            analyzer = PIIHelper._get_analyzer()
            return analyzer.get_supported_entities()
        except Exception:
            # Return common entity types if Presidio is not available
            return [
                "PERSON",
                "EMAIL_ADDRESS",
                "PHONE_NUMBER",
                "CREDIT_CARD",
                "US_SSN",
                "US_DRIVER_LICENSE",
                "US_PASSPORT",
                "LOCATION",
                "DATE_TIME",
                "MEDICAL_LICENSE",
                "URL",
                "IP_ADDRESS",
            ]


class ValidationHelper:
    """Helper class for input validation.

    Provides validation utilities for API keys and configuration values
    used throughout the application.
    """

    @staticmethod
    def validate_openai_key(api_key: str) -> bool:
        """Validate OpenAI API key format.

        Args:
            api_key: API key string to validate

        Returns:
            True if key format is valid, False otherwise
        """
        return api_key and api_key.startswith("sk-")

    @staticmethod
    def validate_tavily_key(api_key: str) -> bool:
        """Validate Tavily API key format.

        Args:
            api_key: Tavily API key string to validate

        Returns:
            True if key format is valid, False otherwise
        """
        return api_key and api_key.startswith("tvly-")

    @staticmethod
    def validate_mcp_url(url: str) -> bool:
        """Validate MCP server URL format.

        Args:
            url: MCP server URL to validate

        Returns:
            True if URL format is valid, False otherwise
        """
        return url and (url.startswith("http://") or url.startswith("https://"))
