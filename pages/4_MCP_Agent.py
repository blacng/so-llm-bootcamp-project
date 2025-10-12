"""MCP Agent Chatbot Page.

Demonstrates Model Context Protocol (MCP) integration for enhanced AI capabilities.
Connects to MCP servers to provide specialized tools and resources beyond standard
LLM functionality, enabling extensible and context-aware AI interactions.
"""

import streamlit as st
import asyncio

from ui_components import ChatbotUI
from langchain_helpers import MCPHelper, ValidationHelper
from config import Config

def setup_page() -> None:
    """Set up the MCP agent page with enhanced styling.
    
    Configures page layout and applies custom CSS optimized
    for MCP agent interactions and tool demonstrations.
    """
    st.set_page_config(
        page_title="MCP Agent",
        page_icon="🔧",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Enhanced visual styling
    st.markdown("""
    <style>
        /* Enhanced chat styling */
        .stChatMessage {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 15px;
            background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
            border: 1px solid rgba(0, 212, 170, 0.1);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }
        
        /* Enhanced buttons */
        .stButton > button {
            background: linear-gradient(135deg, #00d4aa, #00a883);
            border: none;
            border-radius: 10px;
            color: white;
            font-weight: 600;
            padding: 0.75rem 2rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 212, 170, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 212, 170, 0.4);
            background: linear-gradient(135deg, #00e6c0, #00cc99);
        }
        
        /* Enhanced text inputs */
        .stTextInput > div > div > input {
            background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
            border: 2px solid rgba(0, 212, 170, 0.2);
            border-radius: 10px;
            color: #ffffff;
            font-size: 16px;
            padding: 12px;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #00d4aa;
            box-shadow: 0 0 20px rgba(0, 212, 170, 0.3);
        }
        
        /* Enhanced titles */
        h1 {
            background: linear-gradient(135deg, #00d4aa, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            text-shadow: 0 0 30px rgba(0, 212, 170, 0.5);
        }
        
        /* Enhanced info boxes */
        .stInfo {
            background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
            border-left: 4px solid #00d4aa;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 212, 170, 0.2);
        }
        
        /* Enhanced warning boxes */
        .stWarning {
            background: linear-gradient(135deg, #2e2e1e, #3a3a2a);
            border-left: 4px solid #ffaa00;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(255, 170, 0, 0.2);
        }
        
        /* Enhanced error boxes */
        .stError {
            background: linear-gradient(135deg, #2e1e1e, #3a2a2a);
            border-left: 4px solid #ff6b6b;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(255, 107, 107, 0.2);
        }
    </style>
    """, unsafe_allow_html=True)


def configure_mcp_settings() -> bool:
    """Configure OpenAI API key and MCP server URL.

    Handles collection and validation of both the LLM API key
    and MCP server endpoint for agent functionality.
    Prioritizes environment variables over user input for security.

    Returns:
        True if both settings are configured and valid, False otherwise
    """
    # Check session state
    api_key = st.session_state.get("mcp_openai_key", "")
    mcp_url = st.session_state.get("mcp_server_url", "")

    if not api_key or not mcp_url:
        # Try to get from environment variables first (secure)
        env_api_key = Config.get_openai_key()
        env_mcp_url = Config.get_mcp_server_url()

        # If both found in environment, use them
        if env_api_key and env_mcp_url:
            st.session_state["mcp_openai_key"] = env_api_key
            st.session_state["mcp_server_url"] = env_mcp_url
            st.info("🔐 Using API key and MCP URL from secure configuration")
            return True

        # Handle post-connection state to prevent form re-display
        if st.session_state.get("mcp_keys_connected", False):
            st.session_state["mcp_keys_connected"] = False
            return True

        # Partial or no config in environment - show form
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔧 Enter Configuration")

            if not env_api_key and not env_mcp_url:
                st.warning("⚠️ No configuration found in environment. Please enter manually (not recommended for production).")
            elif not env_api_key:
                st.warning("⚠️ OpenAI API key not found in environment.")
                mcp_url = env_mcp_url
                st.session_state["mcp_server_url"] = mcp_url
            elif not env_mcp_url:
                st.warning("⚠️ MCP Server URL not found in environment.")
                api_key = env_api_key
                st.session_state["mcp_openai_key"] = api_key

            # API key input (if not in env)
            if not api_key and not env_api_key:
                api_key_input = st.text_input(
                    "OpenAI API Key",
                    type="password",
                    placeholder="sk-proj-...",
                    key="mcp_api_key_input"
                )
            else:
                api_key_input = api_key or env_api_key
                st.success("✅ OpenAI API key configured")

            # MCP URL input (if not in env)
            if not mcp_url and not env_mcp_url:
                mcp_url_input = st.text_input(
                    "MCP Server URL",
                    placeholder="http://localhost:8000",
                    key="mcp_url_input"
                )
            else:
                mcp_url_input = mcp_url or env_mcp_url
                st.success("✅ MCP Server URL configured")

            # Only show connect button if we need user input
            if (not api_key and not env_api_key) or (not mcp_url and not env_mcp_url):
                if st.button("Connect", type="primary", use_container_width=True):
                    valid_openai = ValidationHelper.validate_openai_key(api_key_input)
                    valid_mcp_url = ValidationHelper.validate_mcp_url(mcp_url_input)

                    if valid_openai and valid_mcp_url:
                        st.session_state["mcp_openai_key"] = api_key_input
                        st.session_state["mcp_server_url"] = mcp_url_input
                        st.session_state["mcp_keys_connected"] = True
                        st.rerun()
                    else:
                        if not valid_openai:
                            st.error("❌ Please enter a valid OpenAI API key")
                        if not valid_mcp_url:
                            st.error("❌ Please enter a valid MCP URL")
        return False

    return True

def display_messages() -> None:
    """Display MCP agent chat messages with capability awareness.
    
    Shows conversation history or informative welcome message
    highlighting the agent's MCP-powered capabilities and tools.
    """
    if not st.session_state.mcp_messages:
        st.info("""🔧 **MCP Agent Ready!** 

Ask me anything! I'm powered by Model Context Protocol.

**I can help with:**
• General questions and conversations
• Using any tools from connected MCP servers
• Accessing enhanced capabilities beyond standard LLM features""")
    else:
        for message in st.session_state.mcp_messages:
            if message["role"] == "user":
                with st.chat_message("user", avatar=ChatbotUI.get_user_avatar()):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant", avatar=ChatbotUI.get_bot_avatar()):
                    st.write(message["content"])

def main() -> None:
    """Main application function for the MCP agent page.
    
    Orchestrates the complete MCP workflow including server connection,
    tool integration, and enhanced AI interactions.
    """
    setup_page()

    # Page title - centered with enhanced styling
    st.markdown("""
    <div style='text-align: center; margin: 0.5rem 0 1rem 0;'>
        <h1 style='font-size: 2.625rem; margin-bottom: 1rem; text-shadow: 0 0 30px rgba(0, 212, 170, 0.5);'>
            🔧 MCP Agent
        </h1>
        <p style='font-size: 0.9rem; color: #a0a0a0; margin-top: -0.5rem;'>
            AI agent powered by Model Context Protocol
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Validate MCP configuration before proceeding
    if not configure_mcp_settings():
        return

    # Initialize MCP agent-specific conversation history
    if "mcp_messages" not in st.session_state:
        st.session_state.mcp_messages = []

    # Render conversation with MCP context awareness
    display_messages()

    # Process query through MCP agent with tool access
    if (st.session_state.mcp_messages and
        st.session_state.mcp_messages[-1]["role"] == "user" and
        not st.session_state.get("mcp_processing", False)):

        st.session_state.mcp_processing = True
        try:
            # Show processing indicator
            with st.chat_message("assistant", avatar=ChatbotUI.get_bot_avatar()):
                with st.spinner("Processing with MCP agent..."):
                    # Extract user query for MCP processing
                    user_query = st.session_state.mcp_messages[-1]["content"]

                    # Retrieve configuration from session state
                    openai_api_key = st.session_state.get("mcp_openai_key", "")
                    mcp_server_url = st.session_state.get("mcp_server_url", "")

                    if openai_api_key and mcp_server_url:
                        try:
                            # Setup async event loop for MCP operations
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)

                            try:
                                # Initialize MCP agent with server connection
                                agent = loop.run_until_complete(
                                    MCPHelper.get_agent(openai_api_key, mcp_server_url)
                                )

                                # Format conversation history for agent processing
                                formatted_messages = [
                                    {"role": msg["role"], "content": msg["content"]}
                                    for msg in st.session_state.mcp_messages
                                ]

                                # Process query through MCP agent
                                response_text = loop.run_until_complete(
                                    MCPHelper.process_mcp_query(agent, formatted_messages)
                                )

                            finally:
                                loop.close()

                        except Exception as e:
                            response_text = f"❌ MCP Agent Error: {str(e)}"
                    else:
                        response_text = "❌ Configuration missing. Please check API key and MCP URL."

                    # Add assistant response
                    st.session_state.mcp_messages.append({"role": "assistant", "content": response_text})

            st.session_state.mcp_processing = False
            st.rerun()

        except Exception as e:
            st.session_state.mcp_processing = False
            st.error(f"Error: {str(e)}")
            st.rerun()

    # MCP agent query input interface
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to MCP conversation history
        st.session_state.mcp_messages.append({"role": "user", "content": prompt})
        st.rerun()

if __name__ == "__main__":
    main()
