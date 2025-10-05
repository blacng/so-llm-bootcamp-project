# PII Safety Guide - Important Information

## ⚠️ Critical: When PII Protection Works

### The Problem You Encountered

**Issue**: You uploaded a document, queried for "Johnson White's SSN", and got the answer `172-32-1176` instead of `<SSN>`.

**Root Cause**: The document was uploaded **BEFORE** enabling PII anonymization.

### Why This Happens

PII protection works at the **document processing stage**:

```
┌─────────────────────────────────────────────────────────────┐
│  WITHOUT PII Protection (What Happened to You)              │
├─────────────────────────────────────────────────────────────┤
│  1. Upload PDF with "SSN: 172-32-1176"                      │
│  2. Process → Store "SSN: 172-32-1176" in vectors ❌        │
│  3. Query → Retrieve "SSN: 172-32-1176" ❌                  │
│  4. Answer: "The SSN is 172-32-1176" ❌                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  WITH PII Protection (Correct Way)                          │
├─────────────────────────────────────────────────────────────┤
│  1. Enable PII Protection FIRST ✅                          │
│  2. Upload PDF with "SSN: 172-32-1176"                      │
│  3. Detect PII → Anonymize to "SSN: <SSN>"                  │
│  4. Process → Store "SSN: <SSN>" in vectors ✅              │
│  5. Query → Retrieve "SSN: <SSN>" ✅                        │
│  6. Answer: "The SSN is <SSN>" ✅                           │
└─────────────────────────────────────────────────────────────┘
```

## ✅ Correct Usage Workflow

### Step 1: Enable PII Protection FIRST

**Before uploading any documents:**

1. Open "Chat with your Data" page
2. Click **"🔒 Privacy & PII Settings"** expander
3. ✅ Check **"Enable PII Detection & Anonymization"**
4. Select method: **"Replace with placeholders"** (recommended)
5. ✅ Check **"Detect PII in user queries"**

### Step 2: Upload Documents

Upload your PDFs. You should see:

```
📚 Processing documents and detecting PII...
```

Then:

```
🔍 PII Detection Report (15 entities found)

Summary by Type:
- PERSON: 5
- US_SSN: 3
- EMAIL_ADDRESS: 4
- PHONE_NUMBER: 3

Method: replace
✅ All PII has been anonymized before processing.
```

### Step 3: Query Safely

Now when you ask:
- **Query**: "What is Johnson White's SSN?"
- **Answer**: "The SSN of Johnson White is <SSN>." ✅

## 🛡️ New Safety Layer (Added)

I've added an **extra safety layer** that detects PII leakage in responses:

### How It Works

If you query a document that was uploaded **without** PII protection, and PII appears in the response, you'll now see:

```
⚠️ Privacy Alert: Response contained 1 potentially sensitive
item(s) (US_SSN) which have been anonymized.

Note: This suggests the document may have been uploaded without
PII protection enabled. For better privacy, please re-upload
with PII anonymization enabled.

Anonymized Response:
The SSN of Johnson White is <SSN>.
```

This provides a **second line of defense** but is **NOT a replacement** for proper document anonymization.

## 🔄 If You Already Uploaded Documents

If you uploaded documents **before** enabling PII protection:

### Option 1: Re-upload (Recommended)

1. **Clear the session**:
   - Streamlit menu (☰) → "Clear cache"
   - Or refresh the page (Ctrl+R / Cmd+R)

2. **Enable PII protection** (see Step 1 above)

3. **Re-upload all documents**

4. **Verify** the PII detection report shows expected entities

### Option 2: Continue with Safety Layer

If you can't re-upload:

1. **Keep PII anonymization enabled**
2. The response-level safety layer will catch and anonymize leaked PII
3. **Be aware**: The vector database still contains raw PII
4. **Limitation**: If the LLM generates creative responses combining multiple PII pieces, some may slip through

**Recommendation**: Always use Option 1 (re-upload) for maximum protection.

## 🔍 How to Verify Protection is Working

### Test 1: Check PII Report After Upload

After uploading, you should see:

```
🔍 PII Detection Report (X entities found)
```

If you see `ℹ️ No PII detected`, either:
- ✅ Your document genuinely has no PII
- ❌ PII protection wasn't enabled before upload

### Test 2: Query for Specific PII

Ask: "What is [person's name]'s [PII type]?"

**Expected answers**:
- ✅ "The SSN is <SSN>"
- ✅ "The email is <EMAIL>"
- ✅ "The phone number is <PHONE>"

**Wrong answers** (need to re-upload):
- ❌ "The SSN is 172-32-1176"
- ❌ "The email is john@example.com"
- ❌ "The phone number is 555-1234"

### Test 3: Check Session State

In the Privacy Settings expander, verify:
- ✅ Green checkmark: "PII detection is available"
- ✅ Checkbox enabled: "Enable PII Detection & Anonymization"

## 📊 What Gets Protected

When PII protection is **properly enabled before upload**:

| PII Type | Original | Anonymized |
|----------|----------|------------|
| Names | Johnson White | `<PERSON>` |
| SSN | 172-32-1176 | `<SSN>` |
| Email | john@example.com | `<EMAIL>` |
| Phone | (555) 123-4567 | `<PHONE>` |
| Credit Card | 4532-1234-5678-9010 | `<CREDIT_CARD>` |
| Address | 123 Main St, LA | 123 Main St, `<LOCATION>` |
| Dates | 05/15/1985 | `<DATE>` |

## ⚠️ Important Limitations

### 1. Must Enable BEFORE Upload

- ❌ Enabling after upload does NOT protect already-processed documents
- ✅ Must re-upload for protection to apply

### 2. Detection Accuracy

- Typical accuracy: 85-95%
- Some context-dependent PII may be missed
- Complex/obfuscated PII may not be detected

### 3. Safety Layer Limitations

The response-level safety layer:
- ✅ Catches direct PII in responses
- ✅ Anonymizes leaked sensitive data
- ❌ Cannot protect PII already in vector embeddings
- ❌ May miss PII in complex/paraphrased responses

### 4. Not a Substitute for Proper Anonymization

**Safety layer is a backup, not primary protection.**

**Best practice**: Always enable PII protection **before** upload.

## 🎯 Use Case Examples

### Example 1: Medical Records (Correct)

```
1. Enable PII protection ✅
2. Upload patient_records.pdf
3. See: "Detected 25 entities: PERSON (8), US_SSN (4), EMAIL (5)..." ✅
4. Query: "What medications is patient #123 taking?"
5. Answer: "<PERSON> is taking Aspirin and Lisinopril" ✅
```

### Example 2: Medical Records (Wrong)

```
1. Upload patient_records.pdf ❌ (PII protection not enabled)
2. Enable PII protection (too late!)
3. Query: "What is John Smith's diagnosis?"
4. Answer: "John Smith has Type 2 Diabetes" ❌ (name leaked)

   With safety layer:
   "⚠️ Privacy Alert: Response contained PERSON (John Smith)...
   Anonymized: <PERSON> has Type 2 Diabetes" ⚠️ (better, but not ideal)
```

### Example 3: Legal Documents (Correct)

```
1. Enable PII protection ✅
2. Upload contract.pdf
3. See: "Detected 12 entities: PERSON (4), EMAIL (3), LOCATION (5)" ✅
4. Query: "What are the contract terms?"
5. Answer: "The contract between <PERSON> and <PERSON>..." ✅
```

## 🔧 Troubleshooting

### Issue: "No PII detected" but document has PII

**Possible causes**:
1. PII protection not enabled before upload
2. PII in uncommon format (non-US SSN, foreign phone numbers)
3. Detection threshold too high

**Solution**:
```python
# Lower detection threshold in code
entities = PIIHelper.detect_pii(text, score_threshold=0.3)
```

### Issue: Response still shows PII even with protection enabled

**Diagnosis**:
- Check if you see the privacy alert message
- If YES: Document was uploaded without protection (re-upload needed)
- If NO: PII may not have been detected (adjust threshold or patterns)

**Solution**:
1. Re-upload document with PII protection enabled
2. Verify PII detection report
3. If specific PII type still missed, report for enhancement

### Issue: Too many false positives

**Cause**: Common words detected as PII

**Solution**: Use selective anonymization
```python
# Only anonymize high-confidence PII
pii_entities = ["US_SSN", "CREDIT_CARD", "EMAIL_ADDRESS", "PHONE_NUMBER"]
```

## ✅ Best Practices Checklist

- [ ] **Enable PII protection BEFORE uploading documents**
- [ ] **Verify PII detection report after upload**
- [ ] **Test with sample queries to confirm anonymization**
- [ ] **Re-upload if documents were processed without protection**
- [ ] **Keep "Detect PII in user queries" enabled**
- [ ] **Use "Replace" method for best RAG performance**
- [ ] **Review privacy alerts if they appear**
- [ ] **Clear cache when switching between protected/unprotected mode**

## 📞 Quick Reference

| Scenario | What You See | Action Required |
|----------|--------------|-----------------|
| Uploaded before enabling | No PII report OR PII in answers | ❌ Re-upload with protection enabled |
| Uploaded after enabling | PII detection report | ✅ Good to go |
| Privacy alert in response | Warning + anonymized answer | ⚠️ Re-upload recommended |
| Query PII warning | "Query contains PERSON" | ℹ️ Rephrase query |

## 🆘 Need Help?

If you're still seeing PII in responses after following this guide:

1. Verify PII protection was enabled **before** upload
2. Check the PII detection report appeared after upload
3. Run test: `uv run python test_ssn_detection.py`
4. Review session state in Privacy Settings
5. Clear cache and re-upload documents

---

## Summary

**Critical Rule**: **Enable PII protection BEFORE uploading documents**

The PII protection system works by:
1. ✅ Detecting PII during document processing
2. ✅ Anonymizing before creating embeddings
3. ✅ Storing only anonymized content in vectors
4. ✅ Returning anonymized responses from RAG

The new safety layer provides backup protection but is **not a substitute** for proper document anonymization.

**Always enable protection first, then upload!** 🛡️
