# Modules 7-10: Charge Capture, Claim Creation, Scrubbing, Submission

**Version:** 1.0  
**Category:** Billing & Claims

---

# Module 7: Charge Capture

## 1. Overview
**Purpose:** Capture all billable services and link to charges for claim creation.

## 2. Actors
- Billing Team, Medical Coder, System, Charge Master Database

## 3. Workflow

```
┌─────────────────────┐
│ Codes Finalized     │
│ (from Module 6)     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Load Encounter Codes│
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ For Each CPT Code:  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Lookup in Charge    │
│ Master:             │
│ - CPT: 93000        │
│ - Amount: $150      │
│ - Department: Cardio│
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Check Insurance     │
│ Contract Rate       │
└──────────┬──────────┘
           ↓
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌─────────┐  ┌─────────────────┐
│Contract │  │ Standard Rate   │
│Rate     │  └─────────────────┘
│$120     │
└────┬────┘
     │
     └────────┬───────────┘
              ↓
     ┌─────────────────┐
     │ Create Charge:  │
     │ - CPT: 93000    │
     │ - Amount: $120  │
     │ - Qty: 1        │
     │ - Total: $120   │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Add Modifiers   │
     │ (if applicable) │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Calculate Total:│
     │ - Charges: $425 │
     │ - Adjustments: 0│
     │ - Net: $425     │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Review & Approve│
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Save to Database│
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Status: Ready   │
     │ for Claim       │
     └─────────────────┘
```

---

# Module 8: Claim Creation

## 1. Overview
**Purpose:** Create CMS-1500 or UB-04 claims from charges.

## 2. Actors
- Billing Team, System, EDI Engine, Database

## 3. Workflow

```
┌─────────────────────┐
│ Charges Captured    │
│ (from Module 7)     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Billing Opens Claim │
│ Creation Screen     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Select Encounters   │
│ Ready for Billing   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Click "Create Claim"│
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ System Gathers:     │
│ - Patient Info      │
│ - Insurance Info    │
│ - Provider Info     │
│ - Diagnosis Codes   │
│ - Procedure Codes   │
│ - Charges           │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Validate Required   │
│ Fields:             │
│ - NPI               │
│ - Tax ID            │
│ - Place of Service  │
│ - Dates             │
└──────────┬──────────┘
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
     │         │ Show Missing    │
     │         │ Fields          │
     │         └────┬────────────┘
     │              │
     │              └─────────────┐
     │                            │
     ▼                            │
┌─────────────────────┐          │
│ Build EDI 837       │          │
│ (Professional)      │          │
└──────────┬──────────┘          │
           │                     │
           ▼                     │
┌─────────────────────┐          │
│ Generate Claim ID   │          │
│ (CLM-00001)         │          │
└──────────┬──────────┘          │
           │                     │
           ▼                     │
┌─────────────────────┐          │
│ Save Claim to DB    │          │
│ Status: Created     │          │
└──────────┬──────────┘          │
           │                     │
           ▼◄────────────────────┘
┌─────────────────────┐
│ Display Claim       │
│ Summary:            │
│ - Claim ID          │
│ - Patient           │
│ - Total: $425       │
│ - Status: Created   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Ready for Scrubbing │
└─────────────────────┘
```

---

# Module 9: Claim Scrubbing (AI-Powered)

## 1. Overview
**Purpose:** Validate claims for errors before submission using AI.

## 2. Actors
- System, AI Engine (OpenAI), Clearinghouse Rules, Database

## 3. Workflow

```
┌─────────────────────┐
│ Claim Created       │
│ (from Module 8)     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Click "Scrub Claim" │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Run Validation      │
│ Rules:              │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Rule 1: Check NPI   │
│ - Valid format?     │
│ - Active?           │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Rule 2: Check Dates │
│ - DOS < Today?      │
│ - DOS > Admit?      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Rule 3: Check Codes │
│ - Valid ICD-10?     │
│ - Valid CPT?        │
│ - Code pairing OK?  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Rule 4: Check       │
│ Insurance:          │
│ - Active coverage?  │
│ - Auth required?    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Rule 5: AI Check    │
│ (OpenAI)            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ AI Analyzes Claim:  │
│ "Check for common   │
│  denial reasons"    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ AI Finds Issues:    │
│ ⚠️  Missing modifier│
│     25 for E/M      │
│ ⚠️  Diagnosis doesn't│
│     support procedure│
└──────────┬──────────┘
           ↓
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌─────────┐  ┌─────────────────┐
│ No      │  │ Errors Found    │
│ Errors  │  └────────┬────────┘
└────┬────┘           │
     │                ▼
     │       ┌─────────────────┐
     │       │ Display Errors: │
     │       │                 │
     │       │ 🔴 Critical:    │
     │       │ - Missing NPI   │
     │       │                 │
     │       │ ⚠️  Warning:    │
     │       │ - Missing mod 25│
     │       │                 │
     │       │ ℹ️  Info:       │
     │       │ - Optimize code │
     │       └────────┬────────┘
     │                │
     │                ▼
     │       ┌─────────────────┐
     │       │ Fix Errors      │
     │       └────┬────────────┘
     │            │
     │            ▼
     │       ┌─────────────────┐
     │       │ Re-scrub        │
     │       └────┬────────────┘
     │            │
     └────────┬───┘
              ↓
     ┌─────────────────┐
     │ Mark as         │
     │ "Scrubbed - OK" │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Ready for       │
     │ Submission      │
     └─────────────────┘
```

---

# Module 10: Claim Submission

## 1. Overview
**Purpose:** Submit claims to insurance payers via clearinghouse (Waystar/Availity).

## 2. Actors
- Billing Team, System, Waystar API, Availity API, Payer

## 3. Workflow

```
┌─────────────────────┐
│ Claim Scrubbed OK   │
│ (from Module 9)     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Billing Selects     │
│ Claims to Submit    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Click "Submit Batch"│
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ System Groups by    │
│ Clearinghouse:      │
│ - Waystar: 10 claims│
│ - Availity: 5 claims│
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ For Each Batch:     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Convert to EDI 837  │
│ Format              │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ POST to Waystar API │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Waystar Validates   │
│ Format              │
└──────────┬──────────┘
           ↓
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌─────────┐  ┌─────────────────┐
│Accepted │  │ Rejected        │
└────┬────┘  └────────┬────────┘
     │                │
     │                ▼
     │       ┌─────────────────┐
     │       │ Show Errors:    │
     │       │ "Invalid format"│
     │       └────┬────────────┘
     │            │
     │            ▼
     │       ┌─────────────────┐
     │       │ Fix & Resubmit  │
     │       └─────────────────┘
     │
     ▼
┌─────────────────────┐
│ Waystar Returns     │
│ Batch ID            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Save Batch ID       │
│ to Database         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Waystar Forwards    │
│ to Payer            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Update Claim Status:│
│ "Submitted"         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Wait for            │
│ Acknowledgment      │
│ (997/999)           │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Payer Sends ACK     │
│ (within 24 hrs)     │
└──────────┬──────────┘
           ↓
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌─────────┐  ┌─────────────────┐
│Accepted │  │ Rejected        │
└────┬────┘  └────────┬────────┘
     │                │
     │                ▼
     │       ┌─────────────────┐
     │       │ Show Rejection  │
     │       │ Reason:         │
     │       │ - Invalid ID    │
     │       │ - Not covered   │
     │       └────┬────────────┘
     │            │
     │            ▼
     │       ┌─────────────────┐
     │       │ Move to Denial  │
     │       │ Management      │
     │       └─────────────────┘
     │
     ▼
┌─────────────────────┐
│ Update Status:      │
│ "Accepted by Payer" │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Wait for Adjudication│
│ (7-14 days)         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Receive ERA/835     │
│ (Payment/Denial)    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Process in Module 18│
│ (Payment Posting)   │
└─────────────────────┘
```

## 4. Batch Submission Flow

```
┌─────────────────────┐
│ Select 50 Claims    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Group by Payer:     │
│ - Aetna: 20         │
│ - BCBS: 15          │
│ - Medicare: 15      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Create 3 Batches    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Submit Each Batch   │
│ Sequentially        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Track Status:       │
│ ✅ Batch 1: Sent    │
│ ⏳ Batch 2: Pending │
│ ⏳ Batch 3: Pending │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ All Batches Sent    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Generate Report:    │
│ - Submitted: 50     │
│ - Accepted: 48      │
│ - Rejected: 2       │
└─────────────────────┘
```

---

## Summary

**Modules 7-10 Complete Flow:**

```
Charge Capture → Claim Creation → Claim Scrubbing → Claim Submission
     ↓                ↓                 ↓                  ↓
  Link codes      Build EDI 837    AI validation      Send to payer
  to charges      CMS-1500         Fix errors         via Waystar
  Calculate $     Validate         Re-scrub           Get ACK
  Review          Generate ID      Approve            Track status
```

**Next Module:** [Module 11: Prior Authorization](Flows_Module_11_Prior_Authorization.md)
