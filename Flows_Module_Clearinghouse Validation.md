# Module: Clearinghouse Validation

**Version:** 1.0
**Module ID:** MOD-011
**Category:** Claims Validation & Submission

---

## 1. Module Overview

**Purpose:** Validate insurance claims before sending them to the payer through a clearinghouse like Waystar, Availity, or Change Healthcare.

**Why Hospitals Use It:** Clearinghouse validation catches claim errors early, before payer submission. It helps hospitals:

- Reduce claim rejections
- Fix missing/invalid data
- Validate payer rules
- Improve first-pass acceptance
- Speed up reimbursement
- Prevent revenue delay

**Main Users:** Billing Team, Claims Team, Claim Scrubber, AR Team, Denial Team, System Admin

---

## 2. Actors Involved

```
┌─────────────────────────────────────────────────┐
│ ACTORS IN CLEARINGHOUSE VALIDATION MODULE       │
├─────────────────────────────────────────────────┤
│                                                 │
│ 1. Billing Team                                 │
│    - Reviews claim before submission            │
│    - Fixes claim validation errors              │
│                                                 │
│ 2. Claims Team                                  │
│    - Prepares final claim                       │
│    - Sends claim to clearinghouse               │
│                                                 │
│ 3. Claim Scrubber                               │
│    - Checks missing fields                      │
│    - Validates payer-specific rules             │
│                                                 │
│ 4. Clearinghouse                                │
│    - Validates claim format                     │
│    - Returns acceptance/rejection response      │
│                                                 │
│ 5. Insurance Payer                              │
│    - Receives accepted clean claim              │
│                                                 │
│ 6. System                                       │
│    - Clearinghouse Connector                    │
│    - Validation Engine                          │
│    - Error Parser                               │
│    - Audit Log Service                          │
│                                                 │
│ 7. External APIs                                │
│    - Waystar API                                │
│    - Availity API                               │
│    - Change Healthcare API                      │
│    - X12 837 Validation                         │
│    - 999 / 277CA Response API                   │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 3. Step-by-Step Workflow

```
┌─────────────────────┐
│ Claim Created       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Claim Scrubbing     │
│ Completed           │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Convert Claim to    │
│ X12 837 Format      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Send Claim to       │
│ Clearinghouse       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Clearinghouse       │
│ Validates Claim     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Receive Response    │
│ 999 / 277CA         │
└──────────┬──────────┘
           ↓
    ╱ ╲
   ╱   ╲
  ╱Accepted?╲──No────────────┐
  ╲         ╱                │
   ╲       ╱                 │
    ╲     ╱                  │
     │Yes                    ▼
     │              ┌─────────────────┐
     │              │ Parse Errors    │
     │              │ Show to Billing │
     │              │ Team            │
     │              └────────┬────────┘
     │                       ↓
     │              ┌─────────────────┐
     │              │ Fix Claim       │
     │              │ Errors          │
     │              └────────┬────────┘
     │                       ↓
     │              ┌─────────────────┐
     │              │ Resubmit to     │
     │              │ Clearinghouse   │
     │              └─────────────────┘
     │
     ▼
┌─────────────────────┐
│ Forward Claim to    │
│ Insurance Payer     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Update Claim Status │
│ Accepted by CH      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Save Audit Log      │
└─────────────────────┘
```

---

## 4. Clearinghouse Validation Engine Flow

```
┌─────────────────────┐
│ Final Claim Input   │
│ CMS-1500 / UB-04    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Validate Claim Data │
│ - Patient Info      │
│ - Provider NPI      │
│ - Payer ID          │
│ - ICD / CPT Codes   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Format Claim        │
│ X12 837P / 837I     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Send to             │
│ Clearinghouse API   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Receive Validation  │
│ Response            │
│ 999 / 277CA         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Parse Response      │
│ - Accepted          │
│ - Rejected          │
│ - Warning           │
│ - Error Segment     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Map Errors to Claim │
│ Fields              │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Return to Frontend  │
│ Validation Results  │
└─────────────────────┘
```

---

## 5. Use Case Diagram

```
┌──────────────┐                          ┌──────────────────┐
│ Billing Team │─────────────────────────>│ Review Claim     │
│              │                          │ Validation       │
└──────┬───────┘                          └──────────────────┘
       │
       ├─────────────────────────────────>│ Fix Validation   │
       │                                  │ Errors           │
       │                                  └──────────────────┘
       │
       └─────────────────────────────────>│ Resubmit Claim   │
                                          │ to Clearinghouse │
                                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ Claims Team  │─────────────────────────>│ Send Claim to    │
│              │                          │ Clearinghouse    │
└──────┬───────┘                          └──────────────────┘
       │
       └─────────────────────────────────>│ Track Response   │
                                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ System       │─────────────────────────>│ Convert to X12   │
│              │                          │ 837 Format       │
└──────┬───────┘                          └──────────────────┘
       │
       ├─────────────────────────────────>│ Parse 999 /      │
       │                                  │ 277CA Response   │
       │                                  └──────────────────┘
       │
       └─────────────────────────────────>│ Update Claim     │
                                          │ Status           │
                                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ Clearinghouse│─────────────────────────>│ Validate Claim   │
│              │                          │ Format / Rules   │
└──────┬───────┘                          └──────────────────┘
       │
       └─────────────────────────────────>│ Forward Claim to │
                                          │ Payer            │
                                          └──────────────────┘
```

---

## 6. Activity Flow Diagram

```
┌─────────┐
│ START   │
└────┬────┘
     │
     ▼
┌─────────────────────┐
│ Load Final Claim    │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Pre-Validation      │
│ Missing Fields      │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Convert to X12 837  │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Send to             │
│ Clearinghouse       │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Receive Response    │
│ 999 / 277CA         │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Accepted?╲──No────────────┐
  ╲         ╱                │
   ╲       ╱                 │
    ╲     ╱                  │
     │Yes                    ▼
     │              ┌─────────────────┐
     │              │ Show Errors     │
     │              │ to Billing Team │
     │              └────┬────────────┘
     │                   ↓
     │              ┌─────────────────┐
     │              │ Correct Claim   │
     │              └────┬────────────┘
     │                   ↓
     │              ┌─────────────────┐
     │              │ Resubmit Claim  │
     │              └─────────────────┘
     │
     ▼
┌─────────────────────┐
│ Forward to Payer    │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Update Status       │
│ Accepted by CH      │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Save Audit Log      │
└────┬────────────────┘
     │
     ▼
┌─────────┐
│ END     │
└─────────┘
```

---

## 7. Sequence Diagram

```
Claims Team  Frontend    Backend    Clearinghouse    Database
    │            │           │             │             │
    │ Submit     │           │             │             │
    │ Claim      │           │             │             │
    ├───────────>│           │             │             │
    │            │ POST /validate-claim    │             │
    │            ├──────────>│             │             │
    │            │           │ Load Claim  │             │
    │            │           ├──────────────────────────>│
    │            │           │ Claim Data  │             │
    │            │           │<──────────────────────────┤
    │            │           │ Convert X12 │             │
    │            │           │ 837         │             │
    │            │           │ Send Claim  │             │
    │            │           ├────────────>│             │
    │            │           │             │ Validate    │
    │            │           │             │ Claim       │
    │            │           │ Response    │             │
    │            │           │<────────────┤             │
    │            │           │ Parse Resp  │             │
    │            │           │ Save Status │             │
    │            │           ├──────────────────────────>│
    │            │ Result    │             │             │
    │            │<──────────┤             │             │
    │ Review     │           │             │             │
    │ Result     │           │             │             │
    │<───────────┤           │             │             │
```

---

## 8. API Flow

**Request:**

```http
POST /api/clearinghouse/validate-claim
{
  "claimId": "CLM-00001",
  "claimType": "837P",
  "payerId": "PAY-001",
  "patientId": "PAT-00001",
  "providerNpi": "1234567890",
  "totalCharge": 425.00
}
```

**Response:**

```json
{
  "claimId": "CLM-00001",
  "clearinghouseStatus": "ACCEPTED",
  "transactionType": "837P",
  "acknowledgement": "999",
  "trackingId": "CH-987654",
  "errors": [],
  "warnings": [],
  "nextAction": "Forwarded to payer",
  "processingTime": "2.1s"
}
```

---

## 9. Database Flow

```sql
-- Save clearinghouse validation result
INSERT INTO clearinghouse_validations (
    validation_id,
    claim_id,
    payer_id,
    transaction_type,
    clearinghouse_status,
    tracking_id,
    response_type,
    created_at
)
VALUES (
    'CHV-00001',
    'CLM-00001',
    'PAY-001',
    '837P',
    'ACCEPTED',
    'CH-987654',
    '999',
    NOW()
);

-- Save validation errors if rejected
INSERT INTO clearinghouse_validation_errors (
    error_id,
    validation_id,
    claim_id,
    error_code,
    error_message,
    field_name,
    severity
)
VALUES (
    'ERR-00001',
    'CHV-00001',
    'CLM-00001',
    'A7:562',
    'Invalid subscriber ID',
    'subscriber_id',
    'HIGH'
);

-- Update claim status
UPDATE claims
SET status = 'ACCEPTED_BY_CLEARINGHOUSE'
WHERE claim_id = 'CLM-00001';

-- Save audit log
INSERT INTO clearinghouse_audit_logs (
    claim_id,
    action,
    performed_by,
    notes
)
VALUES (
    'CLM-00001',
    'CLEARINGHOUSE_VALIDATION_COMPLETED',
    'SYSTEM',
    'Claim validated and accepted by clearinghouse'
);
```

---

## 10. Error Scenarios

```
Error 1: Clearinghouse API Down
   ↓
Show error
   ↓
Retry submission later

Error 2: Invalid Subscriber ID
   ↓
Validation rejects claim
   ↓
Billing team corrects insurance ID
   ↓
Resubmit claim

Error 3: Invalid Provider NPI
   ↓
Show provider error
   ↓
Fix provider credential/NPI
   ↓
Resubmit

Error 4: Missing Required Claim Field
   ↓
Show missing field
   ↓
Billing team updates claim
   ↓
Resubmit

Error 5: Duplicate Claim
   ↓
Clearinghouse rejects duplicate
   ↓
Review claim history
   ↓
Void/Correct claim if needed
```

---

## 11. Dashboard Status Flow

```
┌─────────────────────┐
│ Claim Ready         │
│ for Submission      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Sent to             │
│ Clearinghouse       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Validation in       │
│ Progress            │
└──────────┬──────────┘
           ↓
    ╱ ╲
   ╱   ╲
  ╱Accepted?╲──No──────────┐
  ╲         ╱              │
   ╲       ╱               │
    ╲     ╱                │
     │Yes                  ▼
     │              ┌─────────────────┐
     │              │ Rejected by     │
     │              │ Clearinghouse   │
     │              └────────┬────────┘
     │                       ↓
     │              ┌─────────────────┐
     │              │ Correction      │
     │              │ Required        │
     │              └────────┬────────┘
     │                       ↓
     │              ┌─────────────────┐
     │              │ Resubmitted     │
     │              └─────────────────┘
     │
     ▼
┌─────────────────────┐
│ Accepted by         │
│ Clearinghouse       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Forwarded to Payer  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Awaiting Payer      │
│ Response            │
└─────────────────────┘
```

---

**Next Module:** [Module 12: Claim Submission](Flows_Module_12_Claim_Submission.md)
