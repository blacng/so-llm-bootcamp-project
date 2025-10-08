"""Test script for PIIHelper class.

This script demonstrates PII detection and anonymization capabilities
using the PIIHelper class from langchain_helpers.
"""

from langchain_helpers import PIIHelper


def test_pii_detection():
    """Test PII detection functionality."""
    print("=" * 60)
    print("Testing PII Detection")
    print("=" * 60)

    # Sample text with various PII types
    test_text = """
    Hi, my name is John Smith and I live in New York.
    You can reach me at john.smith@example.com or call (555) 123-4567.
    My SSN is 123-45-6789 and credit card is 4532-1234-5678-9010.
    I was born on 05/15/1985.
    """

    print(f"\nOriginal Text:\n{test_text}\n")

    # Check if Presidio is available
    if not PIIHelper.is_available():
        print("❌ Presidio is not installed!")
        print("Install with: pip install presidio-analyzer presidio-anonymizer")
        print("Then run: python -m spacy download en_core_web_lg")
        return

    # Detect PII entities
    print("Detecting PII entities...\n")
    entities = PIIHelper.detect_pii(test_text)

    if entities:
        print(f"Found {len(entities)} PII entities:\n")
        for i, entity in enumerate(entities, 1):
            print(f"{i}. {entity['type']}: '{entity['text']}' "
                  f"(confidence: {entity['score']:.2f})")

        # Show statistics
        print(f"\n{PIIHelper.format_pii_report(entities)}")
    else:
        print("No PII entities detected.")


def test_pii_anonymization():
    """Test PII anonymization with different methods."""
    print("\n" + "=" * 60)
    print("Testing PII Anonymization Methods")
    print("=" * 60)

    test_text = "Contact John Smith at john@example.com or call (555) 123-4567."

    print(f"\nOriginal Text:\n{test_text}\n")

    if not PIIHelper.is_available():
        print("❌ Presidio is not installed!")
        return

    # Test different anonymization methods
    methods = {
        "replace": "Replace with placeholders",
        "mask": "Mask with asterisks",
        "hash": "Hash values (SHA256)",
        "redact": "Redact completely"
    }

    for method, description in methods.items():
        print(f"\n{description} (method='{method}'):")
        print("-" * 60)
        anonymized, entities = PIIHelper.anonymize_text(test_text, method=method)
        print(f"Result: {anonymized}")
        print(f"Detected: {len(entities)} entities")


def test_selective_anonymization():
    """Test selective PII anonymization."""
    print("\n" + "=" * 60)
    print("Testing Selective PII Anonymization")
    print("=" * 60)

    test_text = "John Smith lives in NYC. Email: john@example.com, Phone: 555-1234"

    print(f"\nOriginal Text:\n{test_text}\n")

    if not PIIHelper.is_available():
        print("❌ Presidio is not installed!")
        return

    # Anonymize only email addresses
    print("\nAnonymizing ONLY email addresses:")
    print("-" * 60)
    anonymized, entities = PIIHelper.anonymize_text(
        test_text,
        method="replace",
        entities_to_anonymize=["EMAIL_ADDRESS"]
    )
    print(f"Result: {anonymized}")
    print(f"Detected: {[e['type'] for e in entities]}")

    # Anonymize only phone numbers
    print("\nAnonymizing ONLY phone numbers:")
    print("-" * 60)
    anonymized, entities = PIIHelper.anonymize_text(
        test_text,
        method="replace",
        entities_to_anonymize=["PHONE_NUMBER"]
    )
    print(f"Result: {anonymized}")
    print(f"Detected: {[e['type'] for e in entities]}")


def test_document_scenario():
    """Test realistic document anonymization scenario."""
    print("\n" + "=" * 60)
    print("Testing Realistic Document Scenario")
    print("=" * 60)

    # Sample medical document excerpt
    document_text = """
    Patient Name: Sarah Johnson
    Date of Birth: 03/22/1978
    SSN: 987-65-4321

    Contact Information:
    - Email: sarah.johnson@email.com
    - Phone: (555) 987-6543
    - Address: 123 Main Street, Los Angeles, CA 90001

    Medical Record: The patient visited on 01/15/2024 complaining of symptoms.
    Credit card on file: 5555-4444-3333-2222
    """

    print(f"\nOriginal Document:\n{document_text}\n")

    if not PIIHelper.is_available():
        print("❌ Presidio is not installed!")
        return

    # Anonymize the document
    print("Anonymizing document...")
    anonymized, entities = PIIHelper.anonymize_text(document_text, method="replace")

    print(f"\nAnonymized Document:\n{anonymized}\n")

    # Show detailed report
    print(PIIHelper.format_pii_report(entities, include_text=False))

    # Show statistics
    stats = PIIHelper.get_pii_statistics(entities)
    print(f"\nStatistics: {stats}")


def test_supported_entities():
    """Display supported PII entity types."""
    print("\n" + "=" * 60)
    print("Supported PII Entity Types")
    print("=" * 60)

    entities = PIIHelper.get_supported_entities()
    print(f"\nTotal supported entities: {len(entities)}\n")

    # Display in columns
    for i in range(0, len(entities), 3):
        row = entities[i:i+3]
        print("  ".join(f"{entity:25}" for entity in row))


def main():
    """Run all PII helper tests."""
    print("\n" + "=" * 60)
    print("PIIHelper Test Suite")
    print("=" * 60)

    # Run all tests
    test_pii_detection()
    test_pii_anonymization()
    test_selective_anonymization()
    test_document_scenario()
    test_supported_entities()

    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
