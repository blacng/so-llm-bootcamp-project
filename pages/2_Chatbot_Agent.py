"""Agent Chatbot Page.

AI agent with real-time web search capabilities using Tavily API.
Features intelligent web search integration and streaming responses
for current information and real-time data queries.
"""

import streamlit as st
import asyncio
from typing import Any

from ui_components import ChatbotUI
from langchain_helpers import AgentChatbotHelper, ValidationHelper
from config import Config


def configure_api_keys() -> bool:
    """Configure OpenAI and Tavily API keys for the agent.

    Handles collection and validation of both required API keys
    for the web search-enabled agent functionality.
    Prioritizes environment variables over user input for security.

    Returns:
        True if both API keys are configured and valid, False otherwise
    """
    # Check session state
    openai_key = st.session_state.get("agent_openai_key", "")
    tavily_key = st.session_state.get("agent_tavily_key", "")

    if not openai_key or not tavily_key:
        # Try to get from environment variables first (secure)
        env_openai_key = Config.get_openai_key()
        env_tavily_key = Config.get_tavily_key()

        # If both keys found in environment, use them
        if env_openai_key and env_tavily_key:
            st.session_state["agent_openai_key"] = env_openai_key
            st.session_state["agent_tavily_key"] = env_tavily_key
            st.info("🔐 Using API keys from secure configuration")
            return True

        # Handle post-connection state to prevent form re-display
        if st.session_state.get("agent_keys_connected", False):
            st.session_state["agent_keys_connected"] = False
            return True

        # Partial or no keys in environment - show form
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔑 Enter API Keys")

            if not env_openai_key and not env_tavily_key:
                st.warning("⚠️ No API keys found in environment. Please enter manually (not recommended for production).")
            elif not env_openai_key:
                st.warning("⚠️ OpenAI API key not found in environment.")
                tavily_key = env_tavily_key
                st.session_state["agent_tavily_key"] = tavily_key
            elif not env_tavily_key:
                st.warning("⚠️ Tavily API key not found in environment.")
                openai_key = env_openai_key
                st.session_state["agent_openai_key"] = openai_key

            # OpenAI key input (if not in env)
            if not openai_key and not env_openai_key:
                openai_input = st.text_input(
                    "OpenAI API Key",
                    type="password",
                    placeholder="sk-proj-...",
                    key="agent_openai_input"
                )
            else:
                openai_input = openai_key or env_openai_key
                st.success("✅ OpenAI API key configured")

            # Tavily key input (if not in env)
            if not tavily_key and not env_tavily_key:
                tavily_input = st.text_input(
                    "Tavily API Key",
                    type="password",
                    placeholder="tvly-...",
                    key="agent_tavily_input"
                )
            else:
                tavily_input = tavily_key or env_tavily_key
                st.success("✅ Tavily API key configured")

            # Only show connect button if we need user input
            if (not openai_key and not env_openai_key) or (not tavily_key and not env_tavily_key):
                if st.button("Connect", type="primary", use_container_width=True):
                    valid_openai = ValidationHelper.validate_openai_key(openai_input)
                    valid_tavily = ValidationHelper.validate_tavily_key(tavily_input)

                    if valid_openai and valid_tavily:
                        st.session_state["agent_openai_key"] = openai_input
                        st.session_state["agent_tavily_key"] = tavily_input
                        st.session_state["agent_keys_connected"] = True
                        st.rerun()
                    else:
                        if not valid_openai:
                            st.error("❌ Invalid OpenAI key format")
                        if not valid_tavily:
                            st.error("❌ Invalid Tavily key format")
        return False

    return True

class ChatbotTools:
    """Core functionality class for the agent chatbot.
    
    Manages agent setup, message display, and response processing
    with web search capabilities through Tavily integration.
    """
    def setup_agent(self) -> Any:
        """Setup the web search-enabled agent.
        
        Returns:
            Configured LangGraph agent with Tavily search tools
        """
        openai_key = st.session_state.get("agent_openai_key", "")
        tavily_key = st.session_state.get("agent_tavily_key", "")
        return AgentChatbotHelper.setup_agent(openai_key, tavily_key)

    def display_messages(self) -> None:
        """Display chat messages with web search context awareness.
        
        Shows conversation history or informative welcome message
        highlighting the agent's web search capabilities.
        """
        if not st.session_state.agent_messages:
            st.info("🌐 Ask me anything and I'll search the web for real-time information!")
        else:
            for message in st.session_state.agent_messages:
                if message["role"] == "user":
                    with st.chat_message("user", avatar=ChatbotUI.get_user_avatar()):
                        st.write(message["content"])
                else:
                    with st.chat_message("assistant", avatar=ChatbotUI.get_bot_avatar()):
                        st.write(message["content"])

    def main(self) -> None:
        """Main agent chatbot logic.
        
        Manages the complete agent workflow including message processing,
        web search integration, and streaming response handling.
        """
        # Initialize agent-specific conversation history
        if "agent_messages" not in st.session_state:
            st.session_state.agent_messages = []

        # Configure agent with web search capabilities
        agent = self.setup_agent()

        # Render current conversation with search context
        self.display_messages()

        # Process user query through web search agent
        if (st.session_state.agent_messages and
            st.session_state.agent_messages[-1]["role"] == "user" and
            not st.session_state.get("agent_processing", False)):

            st.session_state.agent_processing = True
            try:
                # Show processing indicator
                with st.chat_message("assistant", avatar=ChatbotUI.get_bot_avatar()):
                    with st.spinner("Searching the web..."):
                        # Extract user query for web search processing
                        user_query = st.session_state.agent_messages[-1]["content"]

                        # Process query through agent with search capabilities
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        try:
                            response = loop.run_until_complete(
                                AgentChatbotHelper.process_agent_response(agent, user_query)
                            )
                        finally:
                            loop.close()

                        # Add assistant response
                        st.session_state.agent_messages.append({"role": "assistant", "content": response})

                st.session_state.agent_processing = False
                st.rerun()

            except Exception as e:
                st.session_state.agent_processing = False
                st.error(f"Error: {str(e)}")
                st.rerun()

        # Chat input for web search queries
        if prompt := st.chat_input("Ask me anything about current events..."):
            # Add user message to conversation history
            st.session_state.agent_messages.append({"role": "user", "content": prompt})
            st.rerun()


def main() -> None:
    """Main application function for the agent chatbot page.
    
    Orchestrates the complete agent workflow including UI setup,
    API key validation, and agent-based conversation processing.
    """
    # Configure page with centralized UI components
    ChatbotUI.setup_page("Agent Chatbot", "🌐")
    ChatbotUI.render_page_header(
        "🌐",
        "Chatbot Agent",
        "AI agent with real-time web search capabilities"
    )

    # Validate required API keys before proceeding
    if not configure_api_keys():
        return

    # Initialize and run the agent chatbot interface
    obj = ChatbotTools()
    obj.main()

if __name__ == "__main__":
    main()
