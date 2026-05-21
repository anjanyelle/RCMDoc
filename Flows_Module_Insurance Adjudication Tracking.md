# Module 13: Insurance Adjudication Tracking

**Version:** 1.0
**Module ID:** MOD-013
**Category:** Category 3: Claims Management

---

## 1. Module Overview

**Purpose:** Track how insurance companies review, process, approve, deny, or partially pay submitted claims.

**Why Hospitals Use It:** After claim submission, hospitals need to know claim status, payer decisions, payment amount, denial reason, adjustment amount, and next action.

**Main Users:** Billing Team, AR Team, Claim Follow-up Team, Denial Team, Finance Team, System Admin

---

## 2. Actors Involved

```
┌─────────────────────────────────────────────────┐
│ ACTORS IN INSURANCE ADJUDICATION TRACKING       │
├─────────────────────────────────────────────────┤
│                                                 │
│ 1. AR Team                                      │
│    - Tracks claim status                        │
│    - Follows up with payer                      │
│    - Reviews pending claims                     │
│                                                 │
│ 2. Billing Team                                 │
│    - Reviews submitted claims                   │
│    - Fixes claim issues if payer rejects        │
│                                                 │
│ 3. Denial Team                                  │
│    - Handles denied claims                      │
│    - Starts appeal process                      │
│                                                 │
│ 4. Insurance Payer                              │
│    - Reviews claim                              │
│    - Approves / denies / adjusts claim          │
│                                                 │
│ 5. System                                       │
│    - Claim Status Tracker                       │
│    - Adjudication Engine                        │
│    - ERA / EOB Parser                           │
│    - Payment Matching Engine                    │
│    - Audit Log Service                          │
│                                                 │
│ 6. External APIs                                │
│    - Waystar API                                │
│    - Availity API                               │
│    - Change Healthcare API                      │
│    - 277CA Claim Status API                     │
│    - ERA / 835 Integration                      │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 3. Step-by-Step Workflow

```
┌─────────────────────┐
│ Claim Submitted     │
│ to Insurance        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Payer Receives      │
│ Claim               │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Claim Status        │
│ Tracking Started    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ System Checks Claim │
│ Status via API      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Receive Payer       │
│ Response            │
│ - Accepted          │
│ - In Review         │
│ - Pending Info      │
│ - Paid              │
│ - Denied            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Parse Response      │
│ 277CA / ERA / EOB   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Update Claim Status │
│ in Dashboard        │
└──────────┬──────────┘
           ↓
    ╱ ╲
   ╱   ╲
  ╱Paid? ╲──No────────────┐
  ╲      ╱                │
   ╲    ╱                 │
    ╲  ╱                  │
     │Yes                 ▼
     │             ┌─────────────────┐
     │             │ Denied / Pending│
     │             │ Route to Team   │
     │             └────────┬────────┘
     │                      │
     ▼                      ▼
┌─────────────────────┐  ┌─────────────────────┐
│ Match Payment       │  │ Start Follow-up /   │
│ with Claim          │  │ Denial Workflow     │
└──────────┬──────────┘  └──────────┬──────────┘
           ↓                        ↓
┌─────────────────────┐  ┌─────────────────────┐
│ Post Insurance      │  │ Save Action Notes    │
│ Payment             │  │ & Follow-up Date     │
└──────────┬──────────┘  └──────────┬──────────┘
           ↓                        ↓
┌─────────────────────┐
│ Close or Move to    │
│ Patient Balance     │
└─────────────────────┘
```

---

## 4. Adjudication Tracking Engine Flow

```
┌─────────────────────┐
│ Submitted Claim     │
│ Input               │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Pull Claim Details  │
│ - Claim ID          │
│ - Payer ID          │
│ - Patient           │
│ - Amount            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Check Payer Status  │
│ API / Clearinghouse │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Receive Response    │
│ 277CA / 835 / EOB   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Parse Status        │
│ - Accepted          │
│ - Rejected          │
│ - Pending           │
│ - Paid              │
│ - Denied            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Extract Details     │
│ - Allowed Amount    │
│ - Paid Amount       │
│ - Adjustment        │
│ - Denial Code       │
│ - Patient Balance   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Update Claim        │
│ Adjudication Status │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Trigger Next Action │
│ - Payment Posting   │
│ - Denial Workflow   │
│ - AR Follow-up      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Return to Frontend  │
│ Tracking Dashboard  │
└─────────────────────┘
```

---

## 5. Use Case Diagram

```
┌──────────────┐                          ┌──────────────────┐
│ AR Team      │─────────────────────────>│ Track Claim      │
│              │                          │ Status           │
└──────┬───────┘                          └──────────────────┘
       │
       │                                  ┌──────────────────┐
       ├─────────────────────────────────>│ Follow-up with   │
       │                                  │ Payer            │
       │                                  └──────────────────┘
       │
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Update Follow-up │
                                          │ Notes            │
                                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ Billing Team │─────────────────────────>│ Review Claim     │
│              │                          │ Response         │
└──────┬───────┘                          └──────────────────┘
       │
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Correct Claim    │
                                          │ if Rejected      │
                                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ System       │─────────────────────────>│ Pull Payer       │
│              │                          │ Status           │
└──────┬───────┘                          └──────────────────┘
       │
       │                                  ┌──────────────────┐
       ├─────────────────────────────────>│ Parse ERA / EOB  │
       │                                  │ / 277CA          │
       │                                  └──────────────────┘
       │
       │                                  ┌──────────────────┐
       ├─────────────────────────────────>│ Update Claim     │
       │                                  │ Status           │
       │                                  └──────────────────┘
       │
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Trigger Payment  │
                                          │ or Denial Flow   │
                                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ Insurance    │─────────────────────────>│ Adjudicate Claim │
│ Payer        │                          │ Approve / Deny   │
└──────────────┘                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ Denial Team  │─────────────────────────>│ Review Denied    │
│              │                          │ Adjudication     │
└──────────────┘                          └──────────────────┘
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
│ Load Submitted      │
│ Claim               │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Check Claim Status  │
│ via API             │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Receive Payer       │
│ Response            │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Parse Response      │
│ ERA / EOB / 277CA   │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Update Dashboard    │
│ Status              │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Paid? ╲──No────────────┐
  ╲      ╱                │
   ╲    ╱                 │
    ╲  ╱                  │
     │Yes                 ▼
     │             ┌─────────────────┐
     │             │ Denied / Pending│
     │             │ / Rejected?     │
     │             └────┬────────────┘
     │                  │
     ▼                  ▼
┌─────────────────────┐  ┌─────────────────────┐
│ Match ERA Payment   │  │ Create Workqueue    │
│ to Claim            │  │ Task                │
└────┬────────────────┘  └────┬────────────────┘
     │                        │
     ▼                        ▼
┌─────────────────────┐  ┌─────────────────────┐
│ Post Payment        │  │ Assign to AR /      │
│                     │  │ Denial Team         │
└────┬────────────────┘  └────┬────────────────┘
     │                        │
     ▼                        ▼
┌─────────────────────┐  ┌─────────────────────┐
│ Calculate Patient   │  │ Follow-up / Denial  │
│ Responsibility      │  │ Process             │
└────┬────────────────┘  └────┬────────────────┘
     │                        │
     ▼                        ▼
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
AR Team  Frontend    Backend    Payer API    Database
   │          │          │           │           │
   │ Open     │          │           │           │
   │ Claim    │          │           │           │
   ├─────────>│          │           │           │
   │          │ GET /claim-status    │           │
   │          ├─────────>│           │           │
   │          │          │ Load Claim│           │
   │          │          ├─────────────────────>│
   │          │          │ Claim Data│           │
   │          │          │<─────────────────────┤
   │          │          │           │           │
   │ Refresh  │          │           │           │
   │ Status   │          │           │           │
   ├─────────>│          │           │           │
   │          │ POST /payer/status   │           │
   │          ├─────────>│           │           │
   │          │          │ Request Claim Status │
   │          │          ├──────────>│           │
   │          │          │           │ Payer     │
   │          │          │           │ Reviews   │
   │          │          │ Response  │           │
   │          │          │<──────────┤           │
   │          │          │ Parse ERA/EOB/277CA  │
   │          │          │           │           │
   │          │          │ Update Status        │
   │          │          ├─────────────────────>│
   │          │          │ Save Audit Log       │
   │          │          ├─────────────────────>│
   │          │ Status   │           │           │
   │          │ Updated  │           │           │
   │          │<─────────┤           │           │
   │ Review   │          │           │           │
   │ Status   │          │           │           │
   │<─────────┤          │           │           │
   │          │          │           │           │
```

---

## 8. API Flow

**Request:**

```http
POST /api/adjudication/status-check
{
  "claimId": "CLM-00001",
  "payerId": "PAY-001",
  "clearinghouseClaimId": "CH-987654",
  "patientId": "PAT-00001",
  "submittedDate": "2026-05-01"
}
```

**Response:**

```json
{
  "claimId": "CLM-00001",
  "payerStatus": "Paid",
  "adjudicationStatus": "Adjudicated",
  "allowedAmount": 2200.00,
  "paidAmount": 1800.00,
  "adjustmentAmount": 300.00,
  "patientResponsibility": 100.00,
  "denialCode": null,
  "remarkCodes": ["CO-45"],
  "paymentDate": "2026-05-18",
  "eraId": "ERA-00001",
  "nextAction": "Post payment",
  "processingTime": "2.4s"
}
```

---

## 9. Database Flow

```sql
-- Save adjudication status
INSERT INTO claim_adjudication_tracking (
    tracking_id,
    claim_id,
    payer_id,
    payer_status,
    adjudication_status,
    allowed_amount,
    paid_amount,
    adjustment_amount,
    patient_responsibility,
    next_action
) VALUES (
    'ADT-00001',
    'CLM-00001',
    'PAY-001',
    'Paid',
    'Adjudicated',
    2200.00,
    1800.00,
    300.00,
    100.00,
    'Post payment'
);

-- Save ERA/EOB response
INSERT INTO payer_responses (
    response_id,
    claim_id,
    response_type,
    payer_status,
    denial_code,
    remark_codes,
    raw_response
) VALUES (
    'RESP-00001',
    'CLM-00001',
    'ERA_835',
    'Paid',
    NULL,
    'CO-45',
    'Raw ERA/EOB response stored securely'
);

-- Save follow-up task if pending/denied
INSERT INTO ar_followup_tasks (
    task_id,
    claim_id,
    assigned_team,
    status,
    followup_date,
    notes
) VALUES (
    'AR-00001',
    'CLM-00001',
    'AR Team',
    'OPEN',
    '2026-05-25',
    'Follow up payer if no payment posted'
);

-- Save audit log
INSERT INTO adjudication_audit_logs (
    claim_id,
    action,
    performed_by,
    notes
) VALUES (
    'CLM-00001',
    'PAYER_STATUS_UPDATED',
    'SYSTEM',
    'Claim adjudication status updated from payer response'
);
```

---

## 10. Error Scenarios

```
Error 1: Payer API Down
   ↓
Show error
   ↓
Retry later / create AR follow-up task

Error 2: Claim Not Found at Payer
   ↓
Show payer response
   ↓
Verify clearinghouse claim ID
   ↓
Resubmit or contact payer

Error 3: ERA/EOB Parsing Failed
   ↓
Flag for manual review
   ↓
AR team uploads/validates response manually

Error 4: Payment Amount Mismatch
   ↓
System detects mismatch
   ↓
Route to payment posting team
   ↓
Review contractual adjustment

Error 5: Denied During Adjudication
   ↓
Capture denial code
   ↓
Send to Denial & Appeals Management

Error 6: Pending Too Long
   ↓
SLA alert triggered
   ↓
AR follow-up with payer
```

---

## 11. Dashboard Status Flow

```
┌─────────────────────┐
│ Claim Submitted     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Accepted by Payer   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ In Adjudication     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Pending Information │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Adjudicated         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Paid / Denied /     │
│ Partially Paid      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Payment Posted OR   │
│ Denial Workqueue    │
└─────────────────────┘
```

---

**Next Module:** [Module 15: Payment Posting](Flows_Module_Payment_Posting.md)