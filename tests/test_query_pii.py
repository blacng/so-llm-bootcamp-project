"""Test query PII detection."""

from langchain_helpers import PIIHelper

# Test queries with PII
test_queries = [
    "What is Johnson White's SSN?",
    "Tell me about patient 123-45-6789",
    "What are the key findings?",  # No PII
    "Email the results to john@example.com",
    "Call me at (555) 123-4567",
]

print("Testing Query PII Detection:")
print("=" * 60)

for query in test_queries:
    entities = PIIHelper.detect_pii(query, score_threshold=0.6)

    if entities:
        pii_types = list(set([e["type"] for e in entities]))
        print("\n⚠️  PII DETECTED")
        print(f"Query: {query}")
        print(f"Found: {', '.join(pii_types)} ({len(entities)} entities)")
    else:
        print("\n✅ Clean")
        print(f"Query: {query}")

print("\n" + "=" * 60)
