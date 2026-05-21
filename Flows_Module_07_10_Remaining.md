# Modules 8-10: Charge Entry / Charge Capture, Claim Creation, Scrubbing, & Submission

**Version:** 1.0  
**Category:** Category 2 & Category 3: Clinical, Billing & Claims Management

---

# Module 8: Charge Entry / Charge Capture

## 1. Overview
**Purpose:** Capture all billable services, procedures, medications, and supplies and convert them into charges for insurance claim creation and patient billing.

## 2. Actors
- Billing Team, Medical Coder, Provider/Doctor, System, Charge Master Database (CDM), Insurance Contract Engine, Revenue Integrity Team, Compliance Team

## 3. Workflow

```
┌──────────────────────────┐
│ Codes Finalized          │
│ (from Module 6 Coding)   │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Load Encounter Details   │
│ - Patient                │
│ - Visit                  │
│ - Provider               │
│ - Insurance              │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Validate Documentation   │
│ Completeness             │
└────────────┬─────────────┘
             ↓
      ┌──────┴──────┐
      │ Missing Docs?│
      └──────┬──────┘
             │
      ┌──────┴──────┐
      │ Yes         │
      ▼             │ No
┌──────────────┐    │
│ Hold Charge  │    │
│ Notify Staff │    │
└──────────────┘    │
                    ↓
┌──────────────────────────┐
│ Load Procedure Codes     │
│ CPT / HCPCS / Revenue    │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ For Each CPT Code        │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Lookup Charge Master     │
│ (CDM)                    │
│ - CPT                    │
│ - Standard Rate          │
│ - Department             │
│ - Revenue Code           │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Validate Code Status     │
│ - Active?                │
│ - Expired?               │
│ - Billable?              │
└────────────┬─────────────┘
             ↓
      ┌──────┴──────┐
      │ Invalid?    │
      └──────┬──────┘
             │
      ┌──────┴──────┐
      │ Yes         │
      ▼             │ No
┌──────────────┐    │
│ Send to      │    │
│ Coding Queue │    │
└──────────────┘    │
                    ↓
┌──────────────────────────┐
│ Check Insurance Contract │
│ Rate                     │
└────────────┬─────────────┘
             ↓
     ┌───────┴────────┐
     │ Contract Exists?│
     └───────┬────────┘
             │
     ┌───────┴────────┐
     │ Yes            │ No
     ▼                ▼
┌──────────────┐  ┌────────────────┐
│ Contract Rate│  │ Standard Rate  │
│ Example:$120 │  │ Example:$150   │
└──────┬───────┘  └────────┬───────┘
       └──────────┬────────┘
                  ↓
┌──────────────────────────┐
│ Apply Modifiers          │
│ - 25                     │
│ - 59                     │
│ - TC                     │
│ - Professional Split     │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Calculate Units / Qty    │
│ Example: Qty = 2         │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Create Charge Line       │
│ - CPT                    │
│ - Modifier               │
│ - Qty                    │
│ - Unit Amount            │
│ - Total Amount           │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Check Duplicate Charges  │
└────────────┬─────────────┘
             ↓
      ┌──────┴──────┐
      │ Duplicate?  │
      └──────┬──────┘
             │
      ┌──────┴──────┐
      │ Yes         │
      ▼             │ No
┌──────────────┐    │
│ Send for     │    │
│ Manual Review│    │
└──────────────┘    │
                    ↓
┌──────────────────────────┐
│ Validate NCCI / Payer    │
│ Edit Rules               │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Apply Adjustments        │
│ - Discounts              │
│ - Write-offs             │
│ - Contractual Adj.       │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Calculate Encounter Total│
│ - Gross Charges          │
│ - Adjustments            │
│ - Net Charges            │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Charge Audit Validation  │
│ - Missing Charges        │
│ - Compliance Checks      │
│ - Medical Necessity      │
└────────────┬─────────────┘
             ↓
      ┌──────┴──────┐
      │ Errors Found?│
      └──────┬──────┘
             │
      ┌──────┴──────┐
      │ Yes         │
      ▼             │ No
┌──────────────┐    │
│ Return to    │    │
│ Billing/Coder│    │
└──────────────┘    │
                    ↓
┌──────────────────────────┐
│ Review & Approval        │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Save Charges to Database │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Generate Audit Logs      │
│ - User                   │
│ - Timestamp              │
│ - Changes                │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Status Updated           │
│ "Ready for Claim"        │
└──────────────────────────┘
```

---

# Module 8a: Claim Creation

## 1. Overview
**Purpose:** Create CMS-1500, UB-04, and EDI 837 claims using captured charges, patient details, provider data, and insurance information for claim submission.

## 2. Actors
- Billing Team, System, EDI Engine, Database, Insurance/Payer System, Provider

## 3. Workflow

```
┌──────────────────────────┐
│ Charges Captured         │
│ (from Module 7)          │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Billing Opens Claim      │
│ Creation Screen          │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Select Encounters Ready  │
│ for Billing              │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Verify Billing Status    │
│ & Authorization          │
└────────────┬─────────────┘
             ↓
      ┌──────┴──────┐
      │ Eligible?   │
      └──────┬──────┘
             │
      ┌──────┴──────┐
      │ No          │
      ▼             │ Yes
┌───────────────┐   │
│ Send to Hold  │   │
│ Queue         │   │
└───────────────┘   │
                    ↓
┌──────────────────────────┐
│ Click "Create Claim"     │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ System Gathers:          │
│ - Patient Info           │
│ - Insurance Info         │
│ - Provider Info          │
│ - Diagnosis Codes        │
│ - Procedure Codes        │
│ - Charges                │
│ - Authorization Info     │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Validate Required Fields │
│ - NPI                    │
│ - Tax ID                 │
│ - Place of Service       │
│ - Dates of Service       │
│ - Subscriber ID          │
│ - Payer ID               │
└────────────┬─────────────┘
             ↓
      ╱ ╲
     ╱   ╲
    ╱Valid?╲────No────────────┐
    ╲     ╱                   │
     ╲   ╱                    │
      ╲ ╱                     │
       │Yes                   ▼
       │              ┌──────────────────┐
       │              │ Show Missing     │
       │              │ / Invalid Fields │
       │              └────────┬─────────┘
       │                       │
       └───────────────────────┘
               ↓
┌──────────────────────────┐
│ Determine Claim Type     │
│ - CMS-1500               │
│ - UB-04                  │
│ - Professional           │
│ - Institutional          │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Assign Claim Frequency   │
│ - Original               │
│ - Corrected              │
│ - Void                   │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Calculate Claim Totals   │
│ - Gross Charges          │
│ - Adjustments            │
│ - Patient Responsibility │
│ - Insurance Responsibility│
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Link Diagnosis to CPT    │
│ Pointer Validation       │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Build EDI 837 Claim File │
│ - 837P                   │
│ - 837I                   │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Generate Claim ID        │
│ Example: CLM-00001       │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Save Claim to Database   │
│ Status: Created          │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Generate Audit Logs      │
│ - User                   │
│ - Timestamp              │
│ - Claim Changes          │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Display Claim Summary    │
│ - Claim ID               │
│ - Patient Name           │
│ - Payer                  │
│ - Total Amount           │
│ - Status                 │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Status: Ready for        │
│ Claim Scrubbing          │
└──────────────────────────┘
```

---

# Module 9a: Claim Scrubbing (AI-Powered)

## 1. Overview
**Purpose:** Validate claims using rules engine and AI to detect billing errors, coding issues, missing information, and denial risks before claim submission.

## 2. Actors
- System, AI Engine, Clearinghouse Rules Engine, Billing Team, Medical Coder, Database, Insurance/Payer Rules

## 3. Workflow

```
┌──────────────────────────┐
│ Claim Created            │
│ (from Module 8)          │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Click "Scrub Claim"      │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Load Claim Data          │
│ - Patient                │
│ - Insurance              │
│ - Provider               │
│ - CPT/ICD Codes          │
│ - Charges                │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Run Validation Rules     │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Rule 1: NPI Validation   │
│ - Valid format?          │
│ - Active provider?       │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Rule 2: Date Validation  │
│ - DOS < Today?           │
│ - Admit/Discharge valid? │
│ - Future date check      │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Rule 3: Code Validation  │
│ - Valid ICD-10?          │
│ - Valid CPT/HCPCS?       │
│ - Expired codes?         │
│ - Code pairing OK?       │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Rule 4: Insurance Check  │
│ - Active coverage?       │
│ - Prior auth required?   │
│ - Referral required?     │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Rule 5: Modifier Check   │
│ - Missing modifiers?     │
│ - Invalid modifiers?     │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Rule 6: NCCI / Bundling  │
│ Validation               │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Rule 7: Duplicate Claim  │
│ Detection                │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Rule 8: Medical Necessity│
│ Validation               │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Rule 9: AI Claim Review  │
│ (OpenAI / AI Engine)     │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ AI Analyzes Claim:       │
│ - Common denial risks    │
│ - Missing documentation  │
│ - Coding optimization    │
│ - Revenue leakage        │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ AI Detects Issues:       │
│ ⚠ Missing Modifier 25    │
│ ⚠ Invalid DX-CPT Pairing │
│ ⚠ Authorization Missing  │
│ ⚠ High denial probability│
└────────────┬─────────────┘
             ↓
      ┌──────┴──────┐
      │ Errors Found?│
      └──────┬──────┘
             │
      ┌──────┴──────┐
      │ No          │ Yes
      ▼             ▼
┌───────────────┐  ┌──────────────────┐
│ Scrub Passed  │  │ Display Errors   │
│ Successfully  │  │                  │
└──────┬────────┘  │ 🔴 Critical      │
       │           │ ⚠ Warning        │
       │           │ ℹ Info           │
       │           └────────┬─────────┘
       │                    ↓
       │           ┌──────────────────┐
       │           │ Assign to Billing│
       │           │ / Coding Queue   │
       │           └────────┬─────────┘
       │                    ↓
       │           ┌──────────────────┐
       │           │ Fix Errors       │
       │           └────────┬─────────┘
       │                    ↓
       │           ┌──────────────────┐
       │           │ Re-Scrub Claim   │
       │           └────────┬─────────┘
       └────────────────────┘
                    ↓
┌──────────────────────────┐
│ Generate Scrub Report    │
│ - Errors                 │
│ - Warnings               │
│ - AI Recommendations     │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Save Scrub Audit Logs    │
│ - User                   │
│ - Timestamp              │
│ - Corrections            │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Status Updated           │
│ "Scrubbed - OK"          │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Ready for Submission     │
└──────────────────────────┘
```

---

# Module 10: Claim Submission

## 1. Overview
**Purpose:** Submit validated claims to insurance payers through clearinghouses such as Waystar and Availity, track acknowledgments, and monitor claim acceptance or rejection status.

## 2. Actors
- Billing Team, System, Clearinghouse API, Waystar API, Availity API, Payer, Database
## 3. Workflow

```
┌──────────────────────────┐
│ Claim Scrubbed OK        │
│ (from Module 9a)         │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Billing Selects Claims   │
│ Ready for Submission     │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Verify Submission Rules  │
│ - Payer Mapping          │
│ - Enrollment Status      │
│ - Claim Completeness     │
└────────────┬─────────────┘
             ↓
      ┌──────┴──────┐
      │ Eligible?   │
      └──────┬──────┘
             │
      ┌──────┴──────┐
      │ No          │ Yes
      ▼             ▼
┌───────────────┐   ┌──────────────────┐
│ Move to Hold  │   │ Click "Submit    │
│ Queue         │   │ Batch"           │
└───────────────┘   └────────┬─────────┘
                              ↓
┌──────────────────────────┐
│ Group Claims by          │
│ Clearinghouse / Payer    │
│ - Waystar                │
│ - Availity               │
│ - Office Ally            │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Create Claim Batches     │
│ by Payer Type            │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ For Each Batch           │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Convert Claims to        │
│ EDI 837 Format           │
│ - 837P                   │
│ - 837I                   │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Encrypt & Secure Payload │
│ (HIPAA Compliance)       │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ POST to Clearinghouse    │
│ API                      │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Clearinghouse Validates  │
│ File Structure & Format  │
└────────────┬─────────────┘
             ↓
      ┌──────┴──────┐
      │ Accepted?   │
      └──────┬──────┘
             │
      ┌──────┴──────┐
      │ No          │ Yes
      ▼             ▼
┌───────────────┐  ┌──────────────────┐
│ Show Format   │  │ Receive Batch ID │
│ Errors        │  │ & Tracking No.   │
└──────┬────────┘  └────────┬─────────┘
       │                    ↓
       │          ┌──────────────────┐
       │          │ Save Batch ID    │
       │          │ to Database      │
       │          └────────┬─────────┘
       │                    ↓
       │          ┌──────────────────┐
       │          │ Update Claim     │
       │          │ Status: Submitted│
       │          └────────┬─────────┘
       │                    ↓
       │          ┌──────────────────┐
       │          │ Clearinghouse    │
       │          │ Forwards to Payer│
       │          └────────┬─────────┘
       │                    ↓
       │          ┌──────────────────┐
       │          │ Wait for ACK     │
       │          │ (997 / 999 / 277)│
       │          └────────┬─────────┘
       │                    ↓
       └──────────────┐ ┌──┴─────────────┐
                      │ │ ACK Received?  │
                      │ └──────┬─────────┘
                      │        │
               ┌──────┴──────┐ ┌──────┴──────┐
               │ Rejected    │ │ Accepted    │
               └──────┬──────┘ └──────┬──────┘
                      │                ↓
                      │      ┌──────────────────┐
                      │      │ Update Status:   │
                      │      │ Accepted by Payer│
                      │      └────────┬─────────┘
                      │                ↓
                      │      ┌──────────────────┐
                      │      │ Wait for         │
                      │      │ Adjudication     │
                      │      │ (7-14 Days)      │
                      │      └────────┬─────────┘
                      │                ↓
                      │      ┌──────────────────┐
                      │      │ Receive ERA/835  │
                      │      │ Payment/Denial   │
                      │      └────────┬─────────┘
                      │                ↓
                      │      ┌──────────────────┐
                      │      │ Send to Payment  │
                      │      │ Posting Module   │
                      │      └──────────────────┘
                      ↓
┌──────────────────────────┐
│ Display Rejection Reason │
│ - Invalid Subscriber ID  │
│ - Payer Rejection        │
│ - Coverage Terminated    │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Move to Rework / Denial  │
│ Management Queue         │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Fix & Resubmit Claim     │
└──────────────────────────┘
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

**Next Module:** [Module 13: Insurance Adjudication Tracking](Flows_Module_Insurance%20Adjudication%20Tracking.md)