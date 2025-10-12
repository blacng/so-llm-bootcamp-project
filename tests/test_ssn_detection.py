from langchain_helpers import PIIHelper

# Test SSN detection
test_text = "Johnson White's SSN is 172-32-1176."

print("Testing SSN Detection:")
print(f"Original text: {test_text}")
print()

# Detect PII
entities = PIIHelper.detect_pii(test_text)
print(f"Detected {len(entities)} entities:")
for e in entities:
    print(f"  - {e['type']}: '{e['text']}' (score: {e['score']:.2f})")
print()

# Anonymize
anonymized, entities = PIIHelper.anonymize_text(test_text, method="replace")
print(f"Anonymized: {anonymized}")
print()

# Test with document-like format
doc_text = """
Employee: Johnson White
SSN: 172-32-1176
Department: Engineering
"""

print("Testing document format:")
print(f"Original:\n{doc_text}")

anonymized_doc, doc_entities = PIIHelper.anonymize_text(doc_text, method="replace")
print(f"Anonymized:\n{anonymized_doc}")
print(f"\nDetected {len(doc_entities)} entities:")
for e in doc_entities:
    print(f"  - {e['type']}: '{e['text']}'")
