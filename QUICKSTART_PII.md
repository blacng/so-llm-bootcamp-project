# PII Detection - Quick Start Guide

Get PII detection running in 5 minutes! ⚡

## Step 1: Install Dependencies (2 min)

```bash
# Install PII detection libraries
uv sync

# Download spaCy language model
python -m spacy download en_core_web_lg
```

## Step 2: Verify Installation (1 min)

```bash
# Test PIIHelper class
python test_pii_helper.py

# Test RAG integration
python test_pii_integration.py
```

Expected output:
```
✅ All tests passed! PII integration is ready to use.
```

## Step 3: Start the App (1 min)

```bash
streamlit run Home.py
```

Navigate to: **📚 Chat with your Data**

## Step 4: Enable PII Protection (1 min)

1. Click **🔒 Privacy & PII Settings**
2. Check ✅ **"Enable PII Detection & Anonymization"**
3. Select method: **"Replace with placeholders"** (recommended)
4. Check ✅ **"Detect PII in user queries"**

## Step 5: Test It! (30 sec)

Upload a PDF with PII (or create a test file with):
- Names: "John Smith"
- Emails: "john@example.com"
- Phone: "(555) 123-4567"
- SSN: "123-45-6789"

You'll see:
```
🔍 PII Detection Report (4 entities found)

Summary by Type:
- PERSON: 1
- EMAIL_ADDRESS: 1
- PHONE_NUMBER: 1
- US_SSN: 1

✅ All PII has been anonymized before processing.
```

## Done! 🎉

Your chatbot now has enterprise-grade PII protection.

---

## Common Commands

```bash
# Run all tests
python test_pii_helper.py && python test_pii_integration.py

# Start app
streamlit run Home.py

# Update dependencies
uv sync
python -m spacy download en_core_web_lg --upgrade
```

## Quick Examples

### Example 1: Detect PII in Text

```python
from langchain_helpers import PIIHelper

text = "Contact John at john@example.com or call 555-1234"
entities = PIIHelper.detect_pii(text)

print(f"Found {len(entities)} PII entities")
# Output: Found 3 PII entities
```

### Example 2: Anonymize Text

```python
from langchain_helpers import PIIHelper

text = "John's SSN is 123-45-6789"
anonymized, entities = PIIHelper.anonymize_text(text, method="replace")

print(anonymized)
# Output: <PERSON>'s SSN is <SSN>
```

### Example 3: Use with RAG

```python
from langchain_helpers import RAGHelper

# Enable PII protection
rag_app, pii_entities = RAGHelper.setup_rag_system(
    files,
    api_key,
    anonymize_pii=True,
    pii_method="replace"
)

print(f"Protected {len(pii_entities)} PII entities")
```

---

## Troubleshooting

**Issue**: "PII detection not available"

**Fix**:
```bash
pip install presidio-analyzer presidio-anonymizer
python -m spacy download en_core_web_lg
```

**Issue**: Tests fail

**Fix**: Check Python version (requires >=3.11)
```bash
python --version
```

**Issue**: Slow first detection

**Expected**: First detection loads spaCy model (~3s). Subsequent detections are fast (~100ms).

---

## Need Help?

- 📖 **Full Documentation**: `PII_INTEGRATION_GUIDE.md`
- 🔧 **API Reference**: `PII_DETECTION_GUIDE.md`
- 📝 **Implementation Details**: `PII_IMPLEMENTATION_SUMMARY.md`
- 🧪 **Test Examples**: `test_pii_helper.py`

---

## What's Protected?

✅ Names, emails, phone numbers
✅ SSN, credit cards, driver's licenses
✅ Addresses, dates, IP addresses
✅ Medical licenses, passports
✅ And 12+ more entity types

Your documents are privacy-protected! 🛡️
