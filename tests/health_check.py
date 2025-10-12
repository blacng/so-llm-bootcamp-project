"""Health check script for the LLM Bootcamp project.

Run this before deploying or after making significant changes to verify:
- No syntax errors
- Imports work correctly
- Environment variables load properly
- Config module functions correctly
- No breaking changes in logic

Usage:
    python tests/health_check.py

    # Or with make
    make health-check

Exit codes:
    0 - All checks passed
    1 - One or more checks failed
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f"{title}")
    print("=" * 60)


def test_imports() -> bool:
    """Test that all critical modules can be imported.

    Returns:
        True if all imports successful, False otherwise
    """
    print("\n🔍 Testing imports...")
    try:
        from config import Config  # noqa: F401

        print("  ✓ config.py imports successfully")

        from langchain_helpers import (  # noqa: F401
            BasicChatbotHelper,
            AgentChatbotHelper,
            RAGHelper,
            MCPHelper,
            ValidationHelper,
            PIIHelper,
        )

        print("  ✓ langchain_helpers.py imports successfully")

        from ui_components import ChatbotUI, APIKeyUI, HomePageUI  # noqa: F401

        print("  ✓ ui_components.py imports successfully")

        return True
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Unexpected error: {e}")
        return False


def test_environment_config() -> bool:
    """Test environment variable loading and Config class.

    Returns:
        True if config works correctly, False otherwise
    """
    print("\n🔍 Testing environment configuration...")
    try:
        from config import Config

        # Test Config methods exist and are callable
        Config.get_openai_key()
        Config.get_tavily_key()
        Config.get_mcp_server_url()
        Config.is_production()
        print("  ✓ Config class methods work")

        # Test validation
        validation = Config.validate_config()
        print(f"  ✓ Configuration validation: {validation['environment']} mode")

        # Report key presence
        if validation["openai_key_present"]:
            print("  ✓ OpenAI API key detected")
        else:
            print("  ⚠ OpenAI API key not found (will require manual input)")

        if validation["tavily_key_present"]:
            print("  ✓ Tavily API key detected")
        else:
            print(
                "  ⚠ Tavily API key not found (search features will require manual input)"
            )

        if validation["mcp_server_url_present"]:
            print("  ✓ MCP Server URL detected")
        else:
            print(
                "  ⚠ MCP Server URL not found (MCP features will require manual input)"
            )

        return True
    except Exception as e:
        print(f"  ✗ Config error: {e}")
        return False


def test_syntax() -> bool:
    """Test Python syntax for all critical files.

    Returns:
        True if no syntax errors, False otherwise
    """
    print("\n🔍 Testing syntax...")
    import ast

    files = [
        "config.py",
        "langchain_helpers.py",
        "ui_components.py",
        "agent_service.py",
        "server.py",
        "Home.py",
        "pages/1_Basic_Chatbot.py",
        "pages/2_Chatbot_Agent.py",
        "pages/3_Chat_with_your_Data.py",
        "pages/4_MCP_Agent.py",
    ]

    all_good = True
    for filepath in files:
        file_path = project_root / filepath
        if not file_path.exists():
            print(f"  ⚠ {filepath}: File not found (skipping)")
            continue

        try:
            with open(file_path, "r") as f:
                code = f.read()
            ast.parse(code)
            print(f"  ✓ {filepath}: No syntax errors")
        except SyntaxError as e:
            print(f"  ✗ {filepath}: Syntax error at line {e.lineno}")
            all_good = False
        except Exception as e:
            print(f"  ✗ {filepath}: Error - {e}")
            all_good = False

    return all_good


def test_security_config() -> bool:
    """Test that security configurations are in place.

    Returns:
        True if security config correct, False otherwise
    """
    print("\n🔍 Testing security configuration...")
    try:
        # Check .gitignore
        gitignore_path = project_root / ".gitignore"
        with open(gitignore_path, "r") as f:
            gitignore = f.read()

        if ".env" in gitignore:
            print("  ✓ .env is in .gitignore")
        else:
            print("  ✗ .env NOT in .gitignore (security risk!)")
            return False

        if "secrets/" in gitignore:
            print("  ✓ secrets/ is in .gitignore")
        else:
            print("  ✗ secrets/ NOT in .gitignore (security risk!)")
            return False

        # Check .env.example exists
        env_example = project_root / ".env.example"
        if env_example.exists():
            print("  ✓ .env.example template exists")
        else:
            print("  ⚠ .env.example not found")

        # Check docker-compose.yml has secrets config
        compose_path = project_root / "docker-compose.yml"
        if compose_path.exists():
            with open(compose_path, "r") as f:
                compose = f.read()
            if "secrets:" in compose and "openai_api_key" in compose:
                print("  ✓ docker-compose.yml has secrets configuration")
            else:
                print("  ⚠ docker-compose.yml may need secrets configuration")

        return True
    except FileNotFoundError as e:
        print(f"  ✗ File not found: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Security config error: {e}")
        return False


def test_api_key_priority() -> bool:
    """Test that API key priority system works correctly.

    Returns:
        True if priority system works, False otherwise
    """
    print("\n🔍 Testing API key priority system...")
    try:
        import os
        from config import Config

        # Test that environment variables take priority
        test_key = "TEST_HEALTH_CHECK_KEY"
        os.environ[test_key] = "from_environment"

        result = Config.get_api_key(test_key, user_input="from_user")

        if result == "from_environment":
            print("  ✓ Environment variables have correct priority over user input")
            del os.environ[test_key]
            return True
        else:
            print("  ✗ Priority system not working correctly")
            return False

    except Exception as e:
        print(f"  ✗ Priority test error: {e}")
        return False


def test_docker_config() -> bool:
    """Test Docker configuration.

    Returns:
        True if Docker config looks good, False otherwise
    """
    print("\n🔍 Testing Docker configuration...")
    try:
        compose_path = project_root / "docker-compose.yml"

        if not compose_path.exists():
            print("  ⚠ docker-compose.yml not found")
            return True  # Not critical

        with open(compose_path, "r") as f:
            compose = f.read()

        checks = {
            "OPENAI_API_KEY": "OpenAI API key environment variable",
            "TAVILY_API_KEY": "Tavily API key environment variable",
            "MCP_SERVER_URL": "MCP server URL environment variable",
            "ENVIRONMENT": "Environment mode variable",
        }

        for key, description in checks.items():
            if key in compose:
                print(f"  ✓ {description} configured")
            else:
                print(f"  ⚠ {description} not found in docker-compose.yml")

        return True

    except Exception as e:
        print(f"  ✗ Docker config error: {e}")
        return False


def generate_report(results: dict) -> None:
    """Generate and display the health check report.

    Args:
        results: Dictionary of test names and their results
    """
    print_section("HEALTH CHECK SUMMARY")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    print(f"\nTests Passed: {passed}/{total}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name}: {status}")

    print("\n" + "=" * 60)

    if all(results.values()):
        print("✅ All health checks passed! Project is ready.")
        print("\nYou can now run:")
        print("  • streamlit run Home.py")
        print("  • docker-compose up --build")
        print("  • make run (if using Makefile)")
    else:
        print("❌ Some health checks failed. Please review errors above.")
        print("\nRecommended actions:")
        for test_name, passed in results.items():
            if not passed:
                print(f"  • Fix issues in: {test_name}")


def main() -> int:
    """Run all health checks.

    Returns:
        0 if all checks passed, 1 if any failed
    """
    print_section("LLM BOOTCAMP PROJECT - HEALTH CHECK")
    print(f"Project root: {project_root}")
    print(f"Python version: {sys.version.split()[0]}")

    # Run all tests
    results = {
        "Imports": test_imports(),
        "Environment Config": test_environment_config(),
        "Syntax Validation": test_syntax(),
        "Security Config": test_security_config(),
        "API Key Priority": test_api_key_priority(),
        "Docker Config": test_docker_config(),
    }

    # Generate report
    generate_report(results)

    # Return exit code
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
