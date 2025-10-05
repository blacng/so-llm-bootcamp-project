# PII Detection and Anonymization Guide

This guide explains how to use the `PIIHelper` class for detecting and anonymizing Personally Identifiable Information (PII) in the Chat with Your Data chatbot.

## Overview

The `PIIHelper` class provides enterprise-grade PII detection and anonymization using Microsoft Presidio. It can detect and anonymize:

- **Personal Information**: Names, dates of birth, ages
- **Contact Information**: Email addresses, phone numbers, addresses
- **Financial Data**: Credit card numbers, bank accounts
- **Government IDs**: SSN, driver's licenses, passports
- **Medical Information**: Medical license numbers
- **Technical Data**: IP addresses, URLs
- **Location Data**: Addresses, cities, countries

## Installation

### 1. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install presidio-analyzer presidio-anonymizer spacy
```

### 2. Download spaCy Language Model

```bash
python -m spacy download en_core_web_lg
```

## Basic Usage

### 1. Detecting PII

```python
from langchain_helpers import PIIHelper

# Sample text with PII
text = "John Smith's email is john@example.com and phone is (555) 123-4567"

# Detect PII entities
entities = PIIHelper.detect_pii(text)

# Display results
for entity in entities:
    print(f"{entity['type']}: {entity['text']} (confidence: {entity['score']:.2f})")
```

**Output:**
```
PERSON: John Smith (confidence: 0.85)
EMAIL_ADDRESS: john@example.com (confidence: 1.00)
PHONE_NUMBER: (555) 123-4567 (confidence: 0.75)
```

### 2. Anonymizing Text

```python
# Anonymize with placeholders (default)
anonymized, entities = PIIHelper.anonymize_text(text, method="replace")
print(anonymized)
# Output: "<PERSON>'s email is <EMAIL> and phone is <PHONE>"

# Anonymize with masking
anonymized, entities = PIIHelper.anonymize_text(text, method="mask")
print(anonymized)
# Output: "**********'s email is ********************* and phone is **************"

# Anonymize with hashing
anonymized, entities = PIIHelper.anonymize_text(text, method="hash")
print(anonymized)
# Output: "a1b2c3d4...'s email is e5f6g7h8... and phone is i9j0k1l2..."

# Anonymize with redaction
anonymized, entities = PIIHelper.anonymize_text(text, method="redact")
print(anonymized)
# Output: "'s email is  and phone is "
```

### 3. Selective Anonymization

```python
# Anonymize only specific PII types
text = "John at john@example.com, phone: 555-1234"

# Only anonymize email addresses
anonymized, entities = PIIHelper.anonymize_text(
    text,
    method="replace",
    entities_to_anonymize=["EMAIL_ADDRESS"]
)
print(anonymized)
# Output: "John at <EMAIL>, phone: 555-1234"

# Only anonymize phone numbers
anonymized, entities = PIIHelper.anonymize_text(
    text,
    method="replace",
    entities_to_anonymize=["PHONE_NUMBER"]
)
print(anonymized)
# Output: "John at john@example.com, phone: <PHONE>"
```

### 4. Generating Reports

```python
# Generate PII detection report
entities = PIIHelper.detect_pii(text)
report = PIIHelper.format_pii_report(entities)
print(report)
```

**Output:**
```
PII Detection Report
====================
Total entities found: 3

Entity Types:
- EMAIL_ADDRESS: 1
- PERSON: 1
- PHONE_NUMBER: 1
```

### 5. Get Statistics

```python
# Get PII statistics
entities = PIIHelper.detect_pii(text)
stats = PIIHelper.get_pii_statistics(entities)
print(stats)
# Output: {'PERSON': 1, 'EMAIL_ADDRESS': 1, 'PHONE_NUMBER': 1}
```

## Advanced Features

### Custom Detection Threshold

```python
# Adjust confidence threshold (default: 0.5)
entities = PIIHelper.detect_pii(
    text,
    score_threshold=0.7  # Only detect entities with 70%+ confidence
)
```

### Check Availability

```python
# Check if Presidio is installed
if PIIHelper.is_available():
    print("PII detection is ready!")
else:
    print("Please install Presidio")
```

### Get Supported Entity Types

```python
# Get list of all supported PII types
supported = PIIHelper.get_supported_entities()
print(f"Supports {len(supported)} entity types")
print(supported)
```

## Integration Examples

### Example 1: Anonymize Document Before Processing

```python
from langchain_helpers import PIIHelper, RAGHelper

# Read document content
document_text = load_document("sensitive_data.pdf")

# Anonymize PII before processing
anonymized_text, entities = PIIHelper.anonymize_text(
    document_text,
    method="replace"
)

# Show what was detected
print(f"Detected {len(entities)} PII entities")
print(PIIHelper.format_pii_report(entities))

# Process anonymized text with RAG
# ... continue with vector store creation
```

### Example 2: Detect PII in User Queries

```python
# User query
user_query = "What's John Smith's phone number?"

# Detect PII in query
entities = PIIHelper.detect_pii(user_query)

if entities:
    print(f"⚠️ Warning: Query contains PII")
    for entity in entities:
        print(f"  - {entity['type']}: {entity['text']}")

    # Anonymize query
    anonymized_query, _ = PIIHelper.anonymize_text(user_query)
    print(f"Anonymized query: {anonymized_query}")
```

### Example 3: Batch Document Processing

```python
# Process multiple documents
documents = ["doc1.txt", "doc2.txt", "doc3.txt"]
all_entities = []

for doc_path in documents:
    with open(doc_path, 'r') as f:
        content = f.read()

    # Detect PII
    entities = PIIHelper.detect_pii(content)
    all_entities.extend(entities)

    print(f"{doc_path}: Found {len(entities)} PII entities")

# Overall statistics
total_stats = PIIHelper.get_pii_statistics(all_entities)
print(f"\nTotal PII across all documents: {total_stats}")
```

## Supported PII Entity Types

| Category | Entity Types |
|----------|-------------|
| **Personal** | PERSON, DATE_TIME, AGE |
| **Contact** | EMAIL_ADDRESS, PHONE_NUMBER, URL |
| **Location** | LOCATION, US_ZIP_CODE |
| **Financial** | CREDIT_CARD, US_BANK_NUMBER, IBAN_CODE, CRYPTO |
| **Government IDs** | US_SSN, US_DRIVER_LICENSE, US_PASSPORT |
| **Medical** | MEDICAL_LICENSE |
| **Technical** | IP_ADDRESS, MAC_ADDRESS |

## Anonymization Methods

| Method | Description | Use Case |
|--------|-------------|----------|
| `replace` | Replace with type placeholders (`<PERSON>`) | Maintaining document structure |
| `mask` | Replace with asterisks (`****`) | Visual redaction |
| `hash` | Replace with SHA256 hash | Consistent anonymization |
| `redact` | Remove completely | Maximum privacy |

## Performance Considerations

- **First Detection**: May take 2-3 seconds to load spaCy model
- **Subsequent Detections**: ~100ms for typical documents
- **Large Documents**: Process in chunks for better performance

## Error Handling

```python
# Graceful degradation if Presidio not installed
if not PIIHelper.is_available():
    print("PII detection unavailable - proceeding without anonymization")
    # Continue with original text
else:
    # Use PII detection
    anonymized, entities = PIIHelper.anonymize_text(text)
```

## Testing

Run the test suite to verify installation:

```bash
python test_pii_helper.py
```

This will run comprehensive tests including:
- PII detection
- Multiple anonymization methods
- Selective anonymization
- Realistic document scenarios
- Supported entity types

## Troubleshooting

### Issue: ImportError for Presidio

**Solution:**
```bash
pip install presidio-analyzer presidio-anonymizer
```

### Issue: spaCy model not found

**Solution:**
```bash
python -m spacy download en_core_web_lg
```

### Issue: Slow first detection

**Expected behavior:** The first detection loads the spaCy model, which takes 2-3 seconds. Subsequent detections are fast.

### Issue: Low detection accuracy

**Solution:** Adjust the `score_threshold` parameter:
```python
entities = PIIHelper.detect_pii(text, score_threshold=0.3)  # Lower threshold
```

## Best Practices

1. **Always anonymize before vectorization** - Prevents PII from being embedded in vector stores
2. **Use replace method for RAG** - Maintains semantic structure while protecting privacy
3. **Show detection reports to users** - Transparency about what PII was found
4. **Selective anonymization** - Only anonymize what's necessary for your use case
5. **Test with sample data** - Verify detection accuracy with domain-specific PII

## Next Steps

- [Integrate with RAG System](./docs/rag-integration.md)
- [Add UI Controls](./docs/ui-integration.md)
- [Configure Custom Entities](./docs/custom-entities.md)

## Resources

- [Microsoft Presidio Documentation](https://microsoft.github.io/presidio/)
- [spaCy Documentation](https://spacy.io/)
- [GDPR Compliance Guide](https://gdpr.eu/)
- [HIPAA Privacy Rules](https://www.hhs.gov/hipaa/for-professionals/privacy/index.html)
