# Module 18: Payment Posting - Flow Documentation

**Version:** 1.0  
**Module ID:** MOD-018  
**Category:** Financial Management / Revenue Cycle Management  

---

## 1. Module Overview

**Purpose:** Process insurance and patient payments, reconcile ERA/EFT transactions, update AR balances, apply financial adjustments, and realize hospital revenue.

**Why Hospitals Use It:** Ensure accurate payment posting, reduce manual reconciliation work, detect denials/underpayments, improve cash flow, and maintain financial accuracy.

**Business Goal:** Accelerate revenue realization, reduce AR days, automate payment reconciliation, prevent revenue leakage, and ensure payer contract compliance.

**Main Users:** Payment Posting Team, Billing Team, AR Team, Financial Supervisors, Revenue Integrity Team, Finance Department

---

## 2. Actors Involved

```
┌───────────────────────────────────────────────────────┐
│ ACTORS IN PAYMENT POSTING MODULE                     │
├───────────────────────────────────────────────────────┤
│                                                       │
│ 1. Payment Posting Team                              │
│    - Posts insurance payments                        │
│    - Reviews ERA exceptions                          │
│    - Handles reconciliation issues                   │
│                                                       │
│ 2. Billing Team                                      │
│    - Reviews denials                                 │
│    - Handles patient balances                        │
│    - Processes adjustments                           │
│                                                       │
│ 3. AR Follow-up Team                                 │
│    - Reviews underpayments                           │
│    - Escalates unresolved balances                   │
│    - Handles payer follow-ups                        │
│                                                       │
│ 4. Financial Supervisor                              │
│    - Approves refunds                                │
│    - Approves write-offs                             │
│    - Reviews financial exceptions                    │
│                                                       │
│ 5. System                                            │
│    - ERA Processing Engine                           │
│    - Auto Posting Engine                             │
│    - Reconciliation Engine                           │
│    - Adjustment Engine                               │
│    - Audit Logging System                            │
│                                                       │
│ 6. External APIs / Systems                           │
│    - Clearinghouse APIs                              │
│    - Banking APIs                                    │
│    - Stripe / Payment Gateway                        │
│    - EFT / ACH Systems                               │
│    - Lockbox Systems                                 │
│                                                       │
│ 7. Insurance Payers                                  │
│    - Send ERA/835 Files                              │
│    - Send EFT Payments                               │
│    - Return Denials/Adjustments                      │
│                                                       │
└───────────────────────────────────────────────────────┘
```

---

## 3. Step-by-Step Workflow

```
┌─────────────────────┐
│ Insurance Processes │
│ Claim               │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ ERA / EDI 835 File  │
│ Received            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Upload ERA File     │
│ via API / SFTP      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Validate ERA File   │
│ Format & Integrity  │
└──────────┬──────────┘
           ↓
      ╱ ╲
     ╱   ╲
    ╱Valid?╲────No──────┐
    ╲      ╱            │
     ╲    ╱             │
      │Yes              ▼
      ▼          ┌──────────────────┐
┌──────────────┐ │ Move to ERA      │
│ Parse ERA    │ │ Exception Queue  │
│ Segments     │ └────────┬─────────┘
└──────┬───────┘          │
       ↓                  ▼
┌─────────────────────┐  ┌─────────────────┐
│ Extract:            │  │ Manual Review   │
│ - Payments          │  │ & Correction    │
│ - CARC/RARC         │  └─────────────────┘
│ - Denials           │
│ - Adjustments       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Match Claim &       │
│ Service Lines       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Reconcile EFT       │
│ Against ERA Amount  │
└──────────┬──────────┘
           ↓
      ╱ ╲
     ╱   ╲
    ╱Match?╲────No─────┐
    ╲      ╱           │
     ╲    ╱            ▼
      │Yes      ┌─────────────────┐
      ▼         │ Variance /      │
┌─────────────┐ │ Exception Queue │
│ Auto Posting│ └────────┬────────┘
│ Engine Runs │          │
└─────┬───────┘          ▼
      ↓          ┌─────────────────┐
┌─────────────────────┐
│ Apply Payments      │
│ to Claim            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Apply Adjustments   │
│ (CARC/RARC)         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Calculate Patient   │
│ Responsibility      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Detect:             │
│ - Underpayment      │
│ - Overpayment       │
│ - Zero Payment      │
└──────────┬──────────┘
           ↓
      ╱ ╲
     ╱   ╲
    ╱Issue?╲────Yes────┐
    ╲      ╱           │
     ╲    ╱            ▼
      │No       ┌─────────────────┐
      ▼         │ Exception /     │
┌─────────────┐ │ Denial Workflow │
│ Update AR   │ └────────┬────────┘
│ Balances    │          │
└─────┬───────┘          ▼
      ↓           ┌─────────────────┐
┌─────────────────────┐
│ Trigger Secondary   │
│ Insurance Claim     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Update Financial    │
│ Reporting           │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Revenue Realized    │
└─────────────────────┘
```

---

## 4. ERA Reconciliation Logic

```
┌─────────────────────┐
│ Receive ERA File    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Validate ANSI X12   │
│ 835 Structure       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Parse Claim Data    │
│ & Service Lines     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Extract CARC/RARC   │
│ Adjustment Codes    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Match Claim in AR   │
│ System              │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Compare ERA vs EFT  │
│ Deposit             │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Validate Balancing  │
│ & Variances         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Auto Post Payment   │
│ & Adjustments       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Generate Audit Log  │
└─────────────────────┘
```

---

## 5. Use Case Diagram

```
┌──────────────┐                         ┌──────────────────┐
│ Payment      │────────────────────────>│ Upload ERA File  │
│ Posting Team │                         └──────────────────┘
└──────┬───────┘
       │                                 ┌──────────────────┐
       ├────────────────────────────────>│ Review Exceptions│
       │                                 └──────────────────┘
       │
       │                                 ┌──────────────────┐
       └────────────────────────────────>│ Manual Posting   │
                                         └──────────────────┘

┌──────────────┐                         ┌──────────────────┐
│ Billing Team │────────────────────────>│ Review Denials   │
└──────┬───────┘                         └──────────────────┘
       │
       └────────────────────────────────>│ Process Refunds  │
                                         └──────────────────┘

┌──────────────┐                         ┌──────────────────┐
│ System       │────────────────────────>│ Auto Posting     │
└──────┬───────┘                         └──────────────────┘
       │
       ├────────────────────────────────>│ Reconciliation   │
       │                                 └──────────────────┘
       │
       └────────────────────────────────>│ Generate Reports │
                                         └──────────────────┘
```

---

## 6. Activity Flow Diagram

```
┌─────────┐
│ START   │
└────┬────┘
     ↓
┌─────────────────────┐
│ Receive ERA File    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Validate File       │
└──────────┬──────────┘
           ↓
      ╱ ╲
     ╱   ╲
    ╱Valid?╲──No─────┐
    ╲      ╱         │
     ╲    ╱          ▼
      │Yes    ┌───────────────┐
      ▼       │ Exception     │
┌───────────┐ │ Queue         │
│ Parse ERA │ └──────┬────────┘
└────┬──────┘        │
     ↓               ▼
┌─────────────────────┐
│ Match Claims        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Reconcile EFT       │
└──────────┬──────────┘
           ↓
      ╱ ╲
     ╱   ╲
    ╱Match?╲──No─────┐
    ╲      ╱         │
     ╲    ╱          ▼
      │Yes    ┌───────────────┐
      ▼       │ Variance      │
┌───────────┐ │ Review        │
│ Auto Post │ └──────┬────────┘
└────┬──────┘        │
     ↓               ▼
┌─────────────────────┐
│ Apply Adjustments   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Update AR           │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Generate Reports    │
└──────────┬──────────┘
           ↓
┌─────────┐
│ END     │
└─────────┘
```

---

## 7. Sequence Diagram

```
Poster     Frontend     Backend     Database     Bank API
  │             │            │            │            │
  │ Upload ERA  │            │            │            │
  ├────────────>│            │            │            │
  │             │ POST /era  │            │            │
  │             ├───────────>│            │            │
  │             │            │ Validate   │            │
  │             │            ├───────────>│            │
  │             │            │            │            │
  │             │            │ Parse ERA  │            │
  │             │            ├───────────>│            │
  │             │            │            │            │
  │             │            │ Match EFT  │            │
  │             │            ├────────────────────────>│
  │             │            │ EFT Match              │
  │             │            │<────────────────────────┤
  │             │            │            │            │
  │             │            │ Auto Post │            │
  │             │            ├───────────>│            │
  │             │            │            │            │
  │             │ Response   │            │            │
  │             │<───────────┤            │            │
  │ Success     │            │            │            │
  │<────────────┤            │            │            │
```

---

## 8. API Flow

**Request**
```
POST /api/payment-posting/era-upload
{
  "payerId": "PAY-001",
  "eraFileName": "835_ERA_MAY2026.txt",
  "depositAmount": 15000,
  "depositDate": "2026-05-20",
  "uploadedBy": "USR-001",
  "tenantId": "TEN-001"
}
```

**Response**
```
{
  "batchId": "BAT-90001",
  "eraStatus": "processed",
  "matchedClaims": 145,
  "unmatchedClaims": 3,
  "totalPostedAmount": 14850,
  "varianceAmount": 150,
  "exceptionQueueCreated": true
}
```

---

## 9. Database Flow

### Multi-Tenant Financial Isolation

Every financial table contains:

- tenant_id
- organization_id
- facility_id
- branch_id

**Purpose:**
- Separate hospital financial data
- Prevent cross-tenant payment visibility
- Support enterprise SaaS architecture
- Enable branch-level reconciliation
- Enable multi-hospital deployment

**SQL Examples:**

```sql
-- Insert ERA Batch
INSERT INTO era_batches (
    batch_id,
    payer_id,
    era_file_name,
    deposit_amount,
    deposit_date,
    batch_status,
    uploaded_by,
    created_at
) VALUES (
    'BAT-90001',
    'PAY-001',
    '835_ERA_MAY2026.txt',
    15000,
    '2026-05-20',
    'processed',
    'USR-001',
    NOW()
);

-- Insert Payment Posting
INSERT INTO payment_postings (
    posting_id,
    claim_id,
    patient_id,
    paid_amount,
    adjustment_amount,
    denial_code,
    posting_status,
    created_at
) VALUES (
    'POST-001',
    'CLM-10001',
    'PAT-0001',
    500,
    50,
    NULL,
    'posted',
    NOW()
);

-- Update AR Balance
UPDATE claims
SET balance_amount = balance_amount - 500
WHERE claim_id = 'CLM-10001';
```

---

## 10. Error Scenarios

**Error 1: Invalid ERA File**
```
↓
Move file to exception queue
↓
Notify payment posting team
```

**Error 2: EFT Mismatch**
```
↓
Variance detected
↓
Send for reconciliation review
```

**Error 3: Duplicate ERA Upload**
```
↓
Block upload
↓
Log duplicate attempt
```

**Error 4: Claim Not Found**
```
↓
Move to unmatched queue
↓
Manual claim review
```

**Error 5: Auto Posting Failed**
```
↓
Retry posting engine
↓
Escalate unresolved records
```

**Error 6: Underpayment Detected**
```
↓
Create underpayment work item
↓
AR follow-up initiated
```

**Error 7: Overpayment Detected**
```
↓
Create refund workflow
↓
Supervisor approval required
```

**Error 8: Denial Code Detected**
```
↓
Create denial workflow
↓
Send to denial management team
```

**Error 9: Negative Patient Balance**
```
↓
Trigger refund review
↓
Prevent incorrect billing
```

**Error 10: Batch Balancing Failure**
```
↓
Lock financial batch
↓
Require supervisor review
```

---

## 11. Dashboard & Status Flow

```
                ┌───────────────────────┐
                │ ERA File Received     │
                └──────────┬────────────┘
                           ↓
                ┌───────────────────────┐
                │ Parsing In Progress   │
                └──────────┬────────────┘
                           ↓
                ┌───────────────────────┐
                │ Reconciliation Running│
                └──────────┬────────────┘
                           ↓
                ┌───────────────────────┐
                │ Auto Posting Running  │
                └──────────┬────────────┘
                           ↓
        ┌──────────────────┼─────────────────────┐
        ▼                  ▼                     ▼
┌─────────────┐    ┌─────────────┐      ┌─────────────┐
│ Posted      │    │ Exceptions  │      │ Denials     │
│ Successfully│    │ Queue       │      │ Detected    │
└─────┬───────┘    └─────┬───────┘      └─────┬───────┘
      │                  │                    │
      ▼                  ▼                    ▼
┌─────────────┐   ┌─────────────┐     ┌─────────────┐
│ AR Updated  │   │ Manual      │     │ Appeal      │
│ Successfully│   │ Review      │     │ Workflow    │
└─────┬───────┘   └─────────────┘     └─────┬───────┘
      ↓
┌─────────────┐
│ Revenue     │
│ Realized    │
└─────────────┘
```

### Financial KPI Dashboard

- Daily Collections
- ERA Processing Volume
- Payment Posting Accuracy %
- Underpayment Amount
- Refund Totals
- Denial Amount
- Revenue Realized
- AR Reduction Metrics
- Payment Variance Trends
- Payer Reimbursement Analytics

---

## 12. Automation & Background Jobs

```
┌─────────────────────┐
│ Scheduled ERA Poll  │
│ Every 15 Minutes    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Download ERA Files  │
│ from Clearinghouse  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Auto Parse & Match  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Run Auto Posting    │
│ Rules Engine        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Generate Exceptions │
│ if Failures Found   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Send Dashboard      │
│ Metrics Update      │
└─────────────────────┘
```

---

## 13. Audit & Compliance

```
┌─────────────────────┐
│ User Performs       │
│ Financial Action    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Capture:            │
│ - User ID           │
│ - Timestamp         │
│ - Old Value         │
│ - New Value         │
│ - IP Address        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Store Immutable     │
│ Audit Record        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ HIPAA / SOX         │
│ Compliance Logging  │
└─────────────────────┘
```

### Financial Backup & Recovery

- ERA file backups
- Payment posting snapshots
- Daily financial backups
- Geo-redundant storage
- Point-in-time recovery
- Audit log retention
- Disaster recovery replication

---

## 14. Role-Based Access Control

### Payment Posting Permissions

| Role | Access |
|------|---------|
| Payment Poster | Post payments only |
| Financial Supervisor | Approve refunds/write-offs |
| AR Team | Review underpayments |
| Admin | Full access |
| Auditor | Read-only audit access |

### Sensitive Financial Restrictions

- Refund approval requires supervisor role
- Write-off override requires admin approval
- ERA deletion prohibited after posting
- Manual posting tracked in audit logs

---

## 15. Enterprise Integrations

```
┌────────────────────────────┐
│ Clearinghouse Integration  │
├────────────────────────────┤
│ Waystar                    │
│ Availity                   │
│ Change Healthcare          │
└────────────────────────────┘

┌────────────────────────────┐
│ Banking / EFT Integration  │
├────────────────────────────┤
│ ACH Systems                │
│ EFT APIs                   │
│ Treasury Systems           │
└────────────────────────────┘

┌────────────────────────────┐
│ Payment Gateway            │
├────────────────────────────┤
│ Stripe                     │
│ Authorize.Net              │
│ Square                     │
└────────────────────────────┘

┌────────────────────────────┐
│ EHR / Billing Integration  │
├────────────────────────────┤
│ Epic Resolute              │
│ Cerner                     │
│ Athenahealth               │
└────────────────────────────┘
```

---

## 16. Enterprise Enhancements

✔ AI-Based Variance Detection  
✔ Intelligent Claim Matching  
✔ Automated Secondary Billing  
✔ Real-Time EFT Reconciliation  
✔ Revenue Leakage Detection  
✔ Automated Refund Triggering  
✔ Payment Accuracy Validation  
✔ Multi-Tenant Financial Isolation  
✔ Enterprise Audit Logging  
✔ Contract Compliance Monitoring  
✔ Cross-Hospital Reconciliation  
✔ Financial KPI Dashboards  

---

## 17. Revenue Leakage Control Flow 

```
┌─────────────────────┐
│ Detect Underpayment │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Compare Contract    │
│ vs Actual Payment   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Generate Recovery   │
│ Work Queue          │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ AR Team Follow-up   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Recover Revenue     │
└─────────────────────┘
```

---

## 18. Summary

The Payment Posting Module is one of the most critical financial control systems in healthcare Revenue Cycle Management.

It ensures:

- accurate payment posting,
- proper financial reconciliation,
- AR reduction,
- denial identification,
- underpayment detection,
- revenue realization,
- and financial compliance.

Without this module:

- revenue leakage increases,
- financial reporting becomes inaccurate,
- AR grows uncontrollably,
- and payer reimbursement issues remain unresolved.

This module directly impacts:

- hospital cash flow,
- reimbursement accuracy,
- financial reporting,
- operational efficiency,
- and enterprise revenue integrity.

