# Module 6: Medical Coding (AI-Assisted) - Flow Documentation

**Version:** 1.0  
**Module ID:** MOD-006  
**Category:** Clinical & Documentation

---

## 1. Module Overview

**Purpose:** Convert clinical documentation into ICD-10, CPT, and HCPCS codes for billing using AI assistance.

**Why Hospitals Use It:** Accurate coding ensures proper reimbursement, reduces claim denials, speeds up billing.

**Main Users:** Medical Coders, Billing Team, AI System

---

## 2. Actors Involved

```
┌─────────────────────────────────────────────────┐
│ ACTORS IN MEDICAL CODING MODULE                 │
├─────────────────────────────────────────────────┤
│                                                  │
│ 1. Medical Coder                                │
│    - Reviews clinical notes                     │
│    - Validates AI-suggested codes                │
│    - Adds/removes codes                          │
│                                                  │
│ 2. Doctor                                        │
│    - Provides clinical documentation             │
│    - Adds diagnosis and procedures               │
│                                                  │
│ 3. AI System (OpenAI GPT-4)                     │
│    - Analyzes clinical notes                     │
│    - Suggests ICD-10 codes                       │
│    - Suggests CPT codes                          │
│                                                  │
│ 4. System                                        │
│    - Coding Engine                               │
│    - Code Validation Service                     │
│    - Database                                    │
│                                                  │
│ 5. External APIs                                 │
│    - OpenAI API (AI coding suggestions)          │
│    - CMS Code Lookup API                         │
│    - ICD-10 Database                             │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 3. Step-by-Step Workflow

```
┌─────────────────────┐
│ Doctor Completes    │
│ Clinical            │
│ Documentation       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Encounter Marked    │
│ "Ready for Coding"  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Coder Opens Coding  │
│ Workqueue           │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Display Pending     │
│ Encounters:         │
│ - Patient: John     │
│ - Date: May 20      │
│ - Provider: Dr. Lee │
│ - Type: Office Visit│
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Coder Selects       │
│ Encounter           │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Load Clinical Notes:│
│                     │
│ "Patient presents   │
│  with chest pain,   │
│  shortness of breath│
│  Diagnosis: Acute   │
│  myocardial         │
│  infarction         │
│  Procedure: EKG,    │
│  Blood work"        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Click "AI Suggest   │
│ Codes"              │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Show Loading:       │
│ "AI analyzing       │
│  notes..."          │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Backend Sends Notes │
│ to OpenAI API       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ OpenAI Prompt:      │
│ "Extract ICD-10 and │
│  CPT codes from     │
│  these clinical     │
│  notes..."          │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ OpenAI Returns:     │
│                     │
│ ICD-10 Codes:       │
│ - I21.9 (Acute MI)  │
│ - R07.9 (Chest pain)│
│ - R06.02 (Dyspnea)  │
│                     │
│ CPT Codes:          │
│ - 93000 (EKG)       │
│ - 85025 (CBC)       │
│ - 99213 (Office     │
│   Visit Level 3)    │
│                     │
│ Confidence: 95%     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Display AI          │
│ Suggestions:        │
│                     │
│ ✅ I21.9 (95%)      │
│ ✅ R07.9 (90%)      │
│ ✅ R06.02 (88%)     │
│ ✅ 93000 (98%)      │
│ ✅ 85025 (92%)      │
│ ⚠️  99213 (75%)     │
│    (Review needed)  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Coder Reviews Each  │
│ Code                │
└──────────┬──────────┘
           ↓
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌─────────┐  ┌─────────────────┐
│ Accept  │  │ Reject/Modify   │
│ Code    │  └────────┬────────┘
└────┬────┘           │
     │                ▼
     │       ┌─────────────────┐
     │       │ Search for      │
     │       │ Correct Code    │
     │       └────────┬────────┘
     │                │
     │                ▼
     │       ┌─────────────────┐
     │       │ Code Lookup:    │
     │       │ Type: "myocard" │
     │       └────────┬────────┘
     │                │
     │                ▼
     │       ┌─────────────────┐
     │       │ Show Results:   │
     │       │ - I21.0         │
     │       │ - I21.1         │
     │       │ - I21.9         │
     │       └────────┬────────┘
     │                │
     │                ▼
     │       ┌─────────────────┐
     │       │ Select Correct  │
     │       │ Code            │
     │       └────────┬────────┘
     │                │
     └────────┬───────┘
              ↓
     ┌─────────────────┐
     │ Add Additional  │
     │ Codes if Needed │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Validate Codes: │
     │ - Valid ICD-10? │
     │ - Valid CPT?    │
     │ - Billable?     │
     │ - Age/Gender    │
     │   appropriate?  │
     └────┬────────────┘
          ↓
    ╱ ╲
   ╱   ╲
  ╱Valid?╲───No──────┐
  ╲     ╱            │
   ╲   ╱             │
    ╲ ╱              │
     │Yes            │
     │               ▼
     │         ┌─────────────────┐
     │         │ Show Validation │
     │         │ Errors:         │
     │         │ "I21.9 requires │
     │         │  4th digit"     │
     │         └────┬────────────┘
     │              │
     │              └─────────────┐
     │                            │
     ▼                            │
┌─────────────────────┐          │
│ Link Codes to       │          │
│ Charges:            │          │
│ - 93000 → $150      │          │
│ - 85025 → $75       │          │
│ - 99213 → $200      │          │
└──────────┬──────────┘          │
           │                     │
           ▼                     │
┌─────────────────────┐          │
│ Add Modifiers       │          │
│ (if needed)         │          │
│ - 25 (Significant   │          │
│   E/M)              │          │
└──────────┬──────────┘          │
           │                     │
           ▼                     │
┌─────────────────────┐          │
│ Review Final Codes: │          │
│                     │          │
│ Diagnosis:          │          │
│ - I21.9 (Primary)   │          │
│ - R07.9             │          │
│ - R06.02            │          │
│                     │          │
│ Procedures:         │          │
│ - 99213             │          │
│ - 93000             │          │
│ - 85025             │          │
│                     │          │
│ Total Charges: $425 │          │
└──────────┬──────────┘          │
           │                     │
           ▼                     │
┌─────────────────────┐          │
│ Click "Submit"      │          │
└──────────┬──────────┘          │
           │                     │
           ▼◄────────────────────┘
┌─────────────────────┐
│ Save Codes to       │
│ Database            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Log AI Usage:       │
│ - Codes suggested: 6│
│ - Codes accepted: 5 │
│ - Codes modified: 1 │
│ - Accuracy: 83%     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Update Encounter    │
│ Status: "Coded"     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Move to Charge      │
│ Capture Queue       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Show Success:       │
│ "Coding complete    │
│  for John Smith"    │
└─────────────────────┘
```

---

## 4. AI Coding Engine Flow

```
┌─────────────────────┐
│ Clinical Notes      │
│ Input               │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Preprocess Text:    │
│ - Remove PHI        │
│ - Extract key terms │
│ - Format for AI     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Build OpenAI Prompt:│
│                     │
│ "You are a medical  │
│  coding expert.     │
│  Extract ICD-10 and │
│  CPT codes from:    │
│  [clinical notes]   │
│  Return JSON with   │
│  codes and          │
│  confidence scores" │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Call OpenAI API     │
│ (GPT-4)             │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Parse AI Response:  │
│ {                   │
│   "icd10": [        │
│     {               │
│       "code":"I21.9"│
│       "conf": 0.95  │
│     }               │
│   ],                │
│   "cpt": [...]      │
│ }                   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Validate Each Code: │
│ - Exists in DB?     │
│ - Current year?     │
│ - Billable?         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Enrich with Details:│
│ - Code description  │
│ - Charge amount     │
│ - Required modifiers│
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Return to Frontend  │
└─────────────────────┘
```

---

## 5. Use Case Diagram

```
┌──────────────┐                          ┌──────────────────┐
│ Medical Coder│─────────────────────────>│ Review Clinical  │
│              │                          │ Notes            │
└──────┬───────┘                          └──────────────────┘
       │
       │                                  ┌──────────────────┐
       ├─────────────────────────────────>│ Request AI       │
       │                                  │ Suggestions      │
       │                                  └──────────────────┘
       │
       │                                  ┌──────────────────┐
       ├─────────────────────────────────>│ Validate Codes   │
       │                                  └──────────────────┘
       │
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Submit Final     │
                                          │ Codes            │
                                          └──────────────────┘

┌──────────────┐                          ┌──────────────────┐
│ AI System    │─────────────────────────>│ Analyze Notes    │
│ (OpenAI)     │                          └──────────────────┘
└──────┬───────┘
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Suggest Codes    │
                                          └──────────────────┘

┌──────────────┐                          ┌──────────────────┐
│ System       │─────────────────────────>│ Validate Code    │
│              │                          │ Format           │
└──────┬───────┘                          └──────────────────┘
       │
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Calculate Charges│
                                          └──────────────────┘
```

---

## 6. Activity Flow Diagram

```
┌─────────┐
│  START  │
└────┬────┘
     │
     ▼
┌─────────────────────┐
│ Load Encounter      │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Read Clinical Notes │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Click "AI Suggest"  │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Call OpenAI API     │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Wait for Response   │
│ (3-5 seconds)       │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Success?╲───No──────┐
  ╲       ╱            │
   ╲     ╱             │
    ╲   ╱              │
     │Yes              │
     │                 ▼
     │         ┌─────────────────┐
     │         │ Show Error:     │
     │         │ "AI unavailable"│
     │         │ Manual coding   │
     │         └─────────────────┘
     │
     ▼
┌─────────────────────┐
│ Display Suggested   │
│ Codes               │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Review Each Code    │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Accept?╲───No──────┐
  ╲      ╱            │
   ╲    ╱             │
    ╲  ╱              │
     │Yes             │
     │                ▼
     │         ┌─────────────────┐
     │         │ Search Correct  │
     │         │ Code            │
     │         └────┬────────────┘
     │              │
     │              │
     └──────┬───────┘
            ↓
     ┌─────────────────┐
     │ Add to Final    │
     │ Code List       │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ More Codes?     │
     └────┬────────────┘
          │
          ▼
    ╱ ╲
   ╱   ╲
  ╱Done? ╲───No──────┐
  ╲     ╱            │
   ╲   ╱             │
    ╲ ╱              │
     │Yes            │
     │               │
     │               └──────────┐
     │                          │
     ▼                          │
┌─────────────────────┐         │
│ Validate All Codes  │         │
└────┬────────────────┘         │
     │                          │
     ▼                          │
    ╱ ╲                         │
   ╱   ╲                        │
  ╱Valid?╲───No──────┐          │
  ╲     ╱            │          │
   ╲   ╱             │          │
    ╲ ╱              │          │
     │Yes            │          │
     │               ▼          │
     │         ┌─────────────────┐
     │         │ Fix Errors      │
     │         └────┬────────────┘
     │              │            │
     │              └────────────┘
     │                          │
     ▼◄─────────────────────────┘
┌─────────────────────┐
│ Link to Charges     │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Submit Codes        │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Save to Database    │
└────┬────────────────┘
     │
     ▼
┌─────────┐
│   END   │
└─────────┘
```

---

## 7. Sequence Diagram

```
Coder    Frontend    Backend    OpenAI    Database
  │          │          │          │          │
  │ Click AI │          │          │          │
  │ Suggest  │          │          │          │
  ├─────────>│          │          │          │
  │          │          │          │          │
  │          │ POST /ai-code       │          │
  │          ├─────────>│          │          │
  │          │          │          │          │
  │          │          │ Load     │          │
  │          │          │ Notes    │          │
  │          │          ├──────────────────>│
  │          │          │          │          │
  │          │          │ Build    │          │
  │          │          │ Prompt   │          │
  │          │          │          │          │
  │          │          │ POST     │          │
  │          │          ├─────────>│          │
  │          │          │          │          │
  │          │          │          │ AI       │
  │          │          │          │ Process  │
  │          │          │          │          │
  │          │          │ Response │          │
  │          │          │<─────────┤          │
  │          │          │          │          │
  │          │          │ Validate │          │
  │          │          │ Codes    │          │
  │          │          ├──────────────────>│
  │          │          │          │          │
  │          │ Suggested│          │          │
  │          │ Codes    │          │          │
  │          │<─────────┤          │          │
  │          │          │          │          │
  │ Review   │          │          │          │
  │<─────────┤          │          │          │
  │          │          │          │          │
  │ Submit   │          │          │          │
  ├─────────>│          │          │          │
  │          │          │          │          │
  │          │ POST /save-codes    │          │
  │          ├─────────>│          │          │
  │          │          │          │          │
  │          │          │ INSERT   │          │
  │          │          ├──────────────────>│
  │          │          │          │          │
  │          │ Success  │          │          │
  │          │<─────────┤          │          │
  │          │          │          │          │
  │ Done     │          │          │          │
  │<─────────┤          │          │          │
  │          │          │          │          │
```

---

## 8. API Flow

**Request:**
```http
POST /api/coding/ai-suggest
{
  "encounterId": "ENC-00001",
  "clinicalNotes": "Patient presents with chest pain..."
}
```

**Response:**
```json
{
  "icd10Codes": [
    {
      "code": "I21.9",
      "description": "Acute myocardial infarction",
      "confidence": 0.95,
      "primary": true
    },
    {
      "code": "R07.9",
      "description": "Chest pain, unspecified",
      "confidence": 0.90,
      "primary": false
    }
  ],
  "cptCodes": [
    {
      "code": "93000",
      "description": "Electrocardiogram, routine ECG",
      "confidence": 0.98,
      "chargeAmount": 150.00
    }
  ],
  "aiModel": "gpt-4",
  "processingTime": "3.2s"
}
```

---

## 9. Database Flow

```sql
-- Save codes
INSERT INTO encounter_codes (
    encounter_id,
    code_type,
    code,
    description,
    is_primary,
    ai_suggested,
    ai_confidence,
    coder_id
) VALUES
    ('ENC-00001', 'ICD10', 'I21.9', 'Acute MI', true, true, 0.95, 'USR-001'),
    ('ENC-00001', 'CPT', '93000', 'EKG', false, true, 0.98, 'USR-001');

-- Link to charges
INSERT INTO charges (
    charge_id,
    encounter_id,
    cpt_code,
    amount,
    quantity
) VALUES
    ('CHG-00001', 'ENC-00001', '93000', 150.00, 1);

-- Log AI usage
INSERT INTO ai_coding_logs (
    encounter_id,
    codes_suggested,
    codes_accepted,
    accuracy_rate,
    processing_time
) VALUES
    ('ENC-00001', 6, 5, 0.83, 3.2);
```

---

## 10. Error Scenarios

```
Error 1: AI API Down
   ↓
Show error
   ↓
Fall back to manual coding

Error 2: Low Confidence (<70%)
   ↓
Flag for manual review
   ↓
Coder validates carefully

Error 3: Invalid Code Suggested
   ↓
Validation catches it
   ↓
Show error to coder
   ↓
Coder selects correct code
```

---

## 11. Dashboard & Status Flow

```
┌─────────────────────┐
│ Encounter Complete  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Pending Coding      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ AI Coding in        │
│ Progress            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Coder Review        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Coding Complete     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Ready for Charge    │
│ Capture             │
└─────────────────────┘
```

---

**Next Module:** [Module 7: Charge Capture](Flows_Module_07_Charge_Capture.md)
