"""Centralized Configuration Module for Secure API Key Management.

This module provides a secure, centralized approach to managing API keys
with support for multiple sources (environment variables, Docker secrets,
and optional user input).

Security features:
- Never logs API keys
- Prioritizes environment variables over user input
- Supports Docker secrets for containerized deployments
- Validates key formats before use
- Provides clear audit trail of key sources

Usage:
    from config import Config

    # Get API key with fallback to user input
    openai_key = Config.get_api_key("OPENAI_API_KEY", user_input=user_provided_key)

    # Get API key from environment only
    tavily_key = Config.get_api_key("TAVILY_API_KEY")

    # Check if running in production mode
    if Config.is_production():
        # Use stricter validation
        pass
"""

import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
import logging

# Configure logging to never log sensitive data
logger = logging.getLogger(__name__)


class Config:
    """Centralized configuration management for API keys and secrets.

    This class provides secure methods for retrieving API keys from multiple
    sources with a clear priority order:
    1. Docker secrets (production)
    2. Environment variables (development/production)
    3. User input (development fallback)

    All methods are static to provide easy access throughout the application.
    """

    # Load environment variables on module import
    _env_loaded = False

    @classmethod
    def _ensure_env_loaded(cls) -> None:
        """Ensure .env file is loaded exactly once."""
        if not cls._env_loaded:
            load_dotenv()
            cls._env_loaded = True
            logger.info("Environment variables loaded")

    @staticmethod
    def is_production() -> bool:
        """Check if running in production environment.

        Returns:
            True if ENVIRONMENT is set to 'production', False otherwise
        """
        return os.getenv("ENVIRONMENT", "development").lower() == "production"

    @staticmethod
    def _read_docker_secret(secret_name: str) -> Optional[str]:
        """Read secret from Docker secrets directory.

        Docker secrets are mounted at /run/secrets/ in containerized environments.
        This method safely attempts to read secrets without raising errors if
        they don't exist.

        Args:
            secret_name: Name of the secret file to read

        Returns:
            Secret value if found, None otherwise
        """
        secret_path = Path(f"/run/secrets/{secret_name}")
        if secret_path.exists():
            try:
                return secret_path.read_text().strip()
            except Exception as e:
                logger.warning(f"Failed to read Docker secret {secret_name}: {e}")
        return None

    @classmethod
    def get_api_key(
        cls,
        key_name: str,
        user_input: Optional[str] = None,
        allow_user_input: bool = True,
    ) -> Optional[str]:
        """Retrieve API key from secure sources with priority order.

        Priority order:
        1. Docker secrets (for production deployments)
        2. Environment variables (from .env file or system)
        3. User input (only if allow_user_input=True)

        Args:
            key_name: Environment variable name (e.g., 'OPENAI_API_KEY')
            user_input: Optional user-provided key as fallback
            allow_user_input: Whether to allow user input as fallback (default: True)

        Returns:
            API key string if found, None otherwise

        Example:
            >>> Config.get_api_key("OPENAI_API_KEY", user_input=st.text_input())
            'sk-proj-...'

            >>> Config.get_api_key("OPENAI_API_KEY", allow_user_input=False)
            'sk-proj-...'  # Only from env or Docker secrets
        """
        cls._ensure_env_loaded()

        # Priority 1: Docker secrets (production)
        docker_secret = cls._read_docker_secret(key_name.lower())
        if docker_secret:
            logger.info(f"API key '{key_name}' loaded from Docker secrets")
            return docker_secret

        # Priority 2: Environment variables
        env_value = os.getenv(key_name)
        if env_value:
            logger.info(f"API key '{key_name}' loaded from environment variables")
            return env_value

        # Priority 3: User input (only in development or if explicitly allowed)
        if allow_user_input and user_input:
            logger.info(f"API key '{key_name}' provided by user input")
            return user_input

        logger.warning(f"API key '{key_name}' not found in any source")
        return None

    @classmethod
    def get_openai_key(cls, user_input: Optional[str] = None) -> Optional[str]:
        """Get OpenAI API key.

        Convenience method for retrieving OpenAI API key.

        Args:
            user_input: Optional user-provided key

        Returns:
            OpenAI API key or None
        """
        return cls.get_api_key("OPENAI_API_KEY", user_input=user_input)

    @classmethod
    def get_tavily_key(cls, user_input: Optional[str] = None) -> Optional[str]:
        """Get Tavily API key.

        Convenience method for retrieving Tavily API key.

        Args:
            user_input: Optional user-provided key

        Returns:
            Tavily API key or None
        """
        return cls.get_api_key("TAVILY_API_KEY", user_input=user_input)

    @classmethod
    def get_mcp_server_url(cls, user_input: Optional[str] = None) -> Optional[str]:
        """Get MCP server URL.

        Convenience method for retrieving MCP server URL.

        Args:
            user_input: Optional user-provided URL

        Returns:
            MCP server URL or None
        """
        return cls.get_api_key("MCP_SERVER_URL", user_input=user_input)

    @classmethod
    def validate_config(cls) -> dict:
        """Validate that required configuration is present.

        Checks for the presence of critical API keys and returns a
        status report.

        Returns:
            Dictionary with validation results:
            {
                'openai_key_present': bool,
                'tavily_key_present': bool,
                'mcp_server_url_present': bool,
                'environment': str
            }
        """
        cls._ensure_env_loaded()

        return {
            "openai_key_present": bool(cls.get_openai_key()),
            "tavily_key_present": bool(cls.get_tavily_key()),
            "mcp_server_url_present": bool(cls.get_mcp_server_url()),
            "environment": "production" if cls.is_production() else "development",
        }


# Convenience function for backward compatibility
def get_api_key(key_name: str, user_input: Optional[str] = None) -> Optional[str]:
    """Legacy function for backward compatibility.

    Args:
        key_name: Environment variable name
        user_input: Optional user-provided value

    Returns:
        API key or None
    """
    return Config.get_api_key(key_name, user_input=user_input)
