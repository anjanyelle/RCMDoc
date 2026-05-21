# Module 14: ERA Processing - Flow Documentation

Updated for Business, Production, and Industry-Level RCM Workflow

**Version:** 1.0 - Updated  
**Module ID:** MOD-014  
**Category:** Payment Posting / Remittance / Revenue Cycle Management  
**Next Module:** [Module 15: Payment Posting / Reconciliation](Flows_Module_Payment_Posting.md)

---

## 1. Module Overview

### Purpose
Process Electronic Remittance Advice (EDI 835) files received from insurance payers, extract payment, adjustment, denial, patient responsibility, provider-level adjustment, and reconciliation details, and prepare accurate payment posting.

### Why Hospitals Use It
Automates payer payment processing, reduces manual posting errors, identifies denials and adjustments, supports faster reconciliation, prevents duplicate ERA posting, and keeps claim and patient balances accurate before patient billing.

### Main Users
Payment Posting Team, Billing Team, AR Team, Denial Management Team, Finance Manager, Compliance / Audit Team, System, Clearinghouse / Payer.

### Business Goal
Improve payment posting speed and accuracy, reduce unapplied cash, detect denials early, reconcile payer payments with EFT/bank deposits, validate allowed/contractual amounts, handle PLB/provider-level adjustments, and ensure correct claim, ledger, secondary billing, and patient responsibility balances.

---

## 2. Actors Involved

```
+-----------------------------------------------------------------------+
| ACTORS IN ERA PROCESSING MODULE                                       |
+-----------------------------------------------------------------------+
| 1. Payment Posting Team                                               |
|    - Reviews imported ERA files and auto-posting results              |
|    - Handles unmatched payments, exceptions, reversals, and takebacks |
|                                                                       |
| 2. Billing Team                                                       |
|    - Reviews claim-level payment updates                              |
|    - Confirms claim balance before next billing action                 |
|                                                                       |
| 3. AR / Denial Management Team                                        |
|    - Reviews denied, partially paid, or unpaid claim lines             |
|    - Starts denial follow-up, appeal, or correction workflow           |
|                                                                       |
| 4. Finance Manager                                                    |
|    - Reconciles ERA payments with bank deposits / EFT                 |
|    - Reviews PLB adjustments, underpayment, overpayment, and cash      |
|                                                                       |
| 5. Compliance / Audit Team                                            |
|    - Audits payment posting, adjustments, manual overrides, balances   |
|                                                                       |
| 6. System                                                             |
|    - ERA parser, matching rules, auto-posting, reconciliation, audit   |
|                                                                       |
| 7. External Systems                                                   |
|    - Payer, clearinghouse, bank/EFT system, PM/claims system           |
|    - EDI 835, EFT, claim status, and payment gateway where applicable  |
+-----------------------------------------------------------------------+
```

---

## 3. Step-by-Step Workflow

```
+-----------------------------+
| ERA / EDI 835 Received     |
| from Payer/Clearinghouse   |
+-------------+---------------+
              |
              v
+-----------------------------+
| Validate ERA File           |
| - File format               |
| - Payer ID                  |
| - Trace/check/EFT number    |
| - Payment date/method       |
| - File hash duplicate check |
+-------------+---------------+
              |
        +-----+------+
        |            |
        v            v
+--------------+  +-----------------------------+
| Invalid /    |  | Valid ERA File              |
| Duplicate    |  +-------------+---------------+
+------+-------+                |
       |                        v
       |          +-----------------------------+
       |          | Parse ERA 835 Segments:     |
       |          | - Claim/line payments       |
       |          | - CARC/RARC codes           |
       |          | - Patient responsibility     |
       |          | - PLB/provider adjustments   |
       |          +-------------+---------------+
       |                        |
       |                        v
       |          +-----------------------------+
       |          | Match ERA to Claims, Lines, |
       |          | Encounters, and Patients    |
       |          +-------------+---------------+
       |                        |
       |              +---------+---------+
       |              |                   |
       |              v                   v
       |   +------------------+   +-----------------------------+
       |   | Match Failed /   |   | Match Successful            |
       |   | Manual Review    |   +-------------+---------------+
       |   +--------+---------+                 |
       |            |                           v
       |            |             +-----------------------------+
       |            |             | Apply Posting Rules:        |
       |            |             | - Paid amount               |
       |            |             | - Contractual adjustment     |
       |            |             | - Denial/rejection reason    |
       |            |             | - Allowed amount validation  |
       |            |             | - Patient responsibility     |
       |            |             +-------------+---------------+
       |            |                           |
       |            |                           v
       |            |             +-----------------------------+
       |            |             | Partial Auto-Post: only     |
       |            |             | fully matched/rule-passed   |
       |            |             | items; hold exceptions      |
       |            |             +-------------+---------------+
       |            |                           |
       +------------+---------------------------+
                                    |
                                    v
             +--------------------------------------------+
             | Reconcile ERA Payment with EFT/Bank Deposit|
             +----------------------+---------------------+
                                    |
                                    v
             +--------------------------------------------+
             | Update Claim, Ledger, Denial Worklist,     |
             | Secondary Billing Need, Patient Resp.,     |
             | PLB Adjustments, and Audit Trail           |
             +----------------------+---------------------+
                                    |
                                    v
             +--------------------------------------------+
             | Send Completed Balances to Patient Billing |
             | or Denial / AR / Secondary Billing Follow-up|
             +--------------------------------------------+
```

---

## 4. ERA Transaction / Integration Flow

```
Payer / Clearinghouse      RCM Backend            Rules Engine       Claims/Ledger       Finance
        |                         |                     |                 |               |
        | Send ERA 835 file       |                     |                 |               |
        +------------------------>|                     |                 |               |
        |                         | Validate file       |                 |               |
        |                         | - duplicate/file hash check           |               |
        |                         | - payer/check/EFT ID                  |               |
        |                         +-------------------->|                 |               |
        |                         | Parse ERA/PLB data  |                 |               |
        |                         +-------------------->|                 |               |
        |                         | Match claim/line    |                 |               |
        |                         +------------------------------------->|
        |                         | Validate allowed/contractual amounts |
        |                         +-------------------->|                 |
        |                         | Auto-post passed items; hold exceptions             |
        |                         +------------------------------------->|
        |                         | Reconcile EFT/bank deposit and PLB adjustments      |
        |                         +---------------------------------------------------->|
        |                         | Update claim status, ledger, denials, patient resp. |
        |                         +------------------------------------->|
        |                         | Audit all posting, adjustment, and override actions |
```

- **Important:** Store raw ERA file, parsed ERA JSON, payer trace/check/EFT number, file hash, claim match result, posting result, exception reason, PLB adjustment details, and reconciliation status.
- **Important:** Do not update patient balance until ERA posting and reconciliation rules are completed.
- **Important:** CARC/RARC codes should drive denial, adjustment, and patient responsibility workflows.
- **Important:** If ERA creates secondary billing requirement or changes patient responsibility, hold patient billing until secondary billing and balance validation are complete.

---

## 5. Use Case Diagram

```
+-------------------+                     +-------------------------+
| Clearinghouse /   |-------------------->| Send ERA 835 File       |
| Payer             |                     +-------------------------+
+-------------------+                                  |
                                                     v
+-------------------+                     +-------------------------+
| System            |-------------------->| Validate / Parse ERA    |
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| System            |-------------------->| Match Claims and Lines  |
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| System            |-------------------->| Validate Allowed Amount |
|                   |                     | / Contractual Adj.      |
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| Payment Posting   |-------------------->| Review Auto-Posting     |
| Team              |                     | Exceptions              |
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| Finance Manager   |-------------------->| Reconcile EFT / Deposit |
|                   |                     | and PLB Adjustments     |
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| Denial / AR Team  |-------------------->| Review Denials /        |
|                   |                     | Underpayments           |
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| Patient Billing / |-------------------->| Receive Final Patient   |
| Secondary Billing |                     | Responsibility / Hold   |
+-------------------+                     +-------------------------+
```

---

## 6. Activity Flow Diagram

```
+-------+
| START |
+---+---+
    |
    v
+-----------------------+
| Receive ERA 835 File  |
+---+-------------------+
    |
    v
+-----------------------+
| Validate File, Hash,  |
| Payer, EFT, Duplicate |
+---+-------------------+
    |
    v
   / \
  /   \
 < Valid >--No---------------------------+
  \  ?  /                                |
   \ /                                   |
    |Yes                                 |
    v                                    v
+-----------------------+        +---------------+
| Parse ERA Segments    |        | Exception /   |
| and PLB Adjustments   |        | Manual Review |
+---+-------------------+        +-------+-------+
    |                                    |
    v                                    |
+-----------------------+                |
| Match Claim / Patient |                |
| / Service Line        |                |
+---+-------------------+                |
    |                                    |
    v                                    |
   / \                                   |
  /   \                                  |
 < Match >--No---------------------------+
  \  ?  /                                |
   \ /                                   |
    |Yes                                 |
    v                                    |
+-----------------------+                |
| Validate Contract /   |                |
| Allowed Amount        |                |
+---+-------------------+                |
    |                                    |
    v                                    |
+-----------------------+                |
| Auto-Post Passed Items|                |
| Hold Failed Lines     |                |
+---+-------------------+                |
    |                                    |
    v                                    |
+-----------------------+                |
| Extract Denials, PLB, |                |
| Patient Responsibility|                |
+---+-------------------+                |
    |                                    |
    +-------------------+----------------+
                        |
                        v
              +-----------------------+
              | Reconcile EFT / Bank  |
              | Deposit               |
              +---+-------------------+
                  |
                  v
              +-----------------------+
              | Update Claims, Ledger,|
              | Worklists, Holds, Audit|
              +---+-------------------+
                  |
                  v
               +-------+
               |  END  |
               +-------+
```

---

## 7. Sequence Diagram

```
Payer/CH   Backend   Parser   Rules/Match   Database   Finance   Denial/AR   Audit
   |          |        |         |           |          |          |        |
   | ERA 835  |        |         |           |          |          |        |
   +--------->|        |         |           |          |          |        |
   |          | Validate file/hash          |          |          |        |
   |          +------->|         |           |          |          |        |
   |          | Parse segments and PLB      |          |          |        |
   |          +------->|         |           |          |          |        |
   |          |        | Parsed ERA          |          |          |        |
   |          |<-------+         |           |          |          |        |
   |          | Match claims/service lines  |          |          |        |
   |          +----------------->|           |          |          |        |
   |          | Validate allowed/contract amounts       |          |        |
   |          +----------------->|           |          |          |        |
   |          | Save raw/parsed ERA, posting, exceptions, PLB       |        |
   |          +----------------------------->|          |          |        |
   |          | Reconcile EFT/deposit                  |          |        |
   |          +---------------------------------------->|          |        |
   |          | Send denials/underpayments to AR worklist             |        |
   |          +-------------------------------------------------->|        |
   |          | Audit ERA import, posting, exceptions, adjustments     |        |
   |          +---------------------------------------------------------->|
```

---

## 8. API Flow

### Request
`POST /api/era/import`
```json
{
  "payerId": "BCBS001",
  "clearinghouseId": "WAYSTAR",
  "eraFileName": "ERA_835_20260520.edi",
  "fileSource": "clearinghouse_sftp",
  "fileHash": "sha256-xxxx",
  "checkOrEftNumber": "EFT-98765",
  "paymentMethod": "EFT",
  "payerPaymentDate": "2026-05-20",
  "receivedAt": "2026-05-20T09:30:00Z",
  "traceId": "TRC-ERA-00001",
  "uploadedBy": "SYSTEM"
}
```

### Response - ERA Imported
```json
{
  "eraId": "ERA-00001",
  "status": "imported",
  "duplicateFile": false,
  "claimCount": 25,
  "totalPaymentAmount": 12500.00,
  "providerAdjustmentAmount": -100.00,
  "message": "ERA file imported and ready for parsing",
  "traceId": "TRC-ERA-00001"
}
```

### Response - Auto Posting Completed
```json
{
  "eraId": "ERA-00001",
  "status": "posted_with_exceptions",
  "autoPostedClaims": 21,
  "exceptionClaims": 4,
  "denialsExtracted": 3,
  "unmatchedPayments": 1,
  "contractVarianceItems": 2,
  "secondaryBillingRequired": true,
  "reconciliationStatus": "pending_eft_match",
  "message": "ERA processed. Exceptions require manual review."
}
```

### Response - Reconciliation Completed
```json
{
  "eraId": "ERA-00001",
  "status": "reconciled",
  "eftTraceNumber": "EFT-98765",
  "bankDepositAmount": 12500.00,
  "eraPaymentAmount": 12500.00,
  "differenceAmount": 0.00,
  "message": "ERA payment reconciled with bank deposit"
}
```

---

## 9. Database Flow

```sql
-- Save ERA file metadata
INSERT INTO era_files (
    era_id, payer_id, clearinghouse_id, file_name, file_source,
    raw_file_url, file_hash, total_payment_amount, check_or_eft_number,
    payment_method, payer_payment_date, duplicate_file, status, trace_id,
    received_at, created_at, updated_at
) VALUES (...);

-- Save claim-level ERA details
INSERT INTO era_claim_payments (
    era_claim_payment_id, era_id, claim_id, payer_claim_control_number,
    billed_amount, allowed_amount, paid_amount, adjustment_amount,
    contractual_adjustment_amount, patient_responsibility,
    claim_status, match_status, exception_reason, created_at
) VALUES (...);

-- Save service-line payment details
INSERT INTO era_service_line_payments (
    line_payment_id, era_claim_payment_id, claim_line_id, cpt_code,
    billed_amount, allowed_amount, paid_amount, adjustment_amount,
    carc_codes, rarc_codes, denial_flag, patient_responsibility,
    contract_variance_flag, created_at
) VALUES (...);

-- Save provider-level adjustments from PLB segments
INSERT INTO era_provider_adjustments (
    adjustment_id, era_id, adjustment_code, adjustment_amount,
    reason, created_at
) VALUES (...);

-- Post payment and adjustments to claim ledger
INSERT INTO claim_ledger (
    ledger_id, claim_id, source_type, source_id, transaction_type,
    amount, balance_after, created_at
) VALUES (...);

-- Create denial / exception worklist item
INSERT INTO denial_worklist (
    denial_id, claim_id, era_id, denial_reason_code, rarc_codes,
    priority, status, created_at
) VALUES (...);

-- Save EFT / bank reconciliation
INSERT INTO era_reconciliation (
    reconciliation_id, era_id, eft_trace_number, era_payment_amount,
    bank_deposit_amount, difference_amount, status, reconciled_by, reconciled_at
) VALUES (...);

-- Update claim after posting
UPDATE claims
SET status = 'paid_or_partially_paid',
    paid_amount = paid_amount + 120.00,
    patient_responsibility = 30.00,
    updated_at = NOW()
WHERE claim_id = 'CLM-00001';
```

---

## 10. Error Scenarios

* **Error 1: Invalid ERA File Format**
  * *Route:* Reject file import
  * *Action:* Notify payment posting team and request corrected file
* **Error 2: Duplicate ERA File**
  * *Route:* Block duplicate posting
  * *Action:* Use payer/check/EFT/date/payment amount/file hash to identify duplicate
* **Error 3: Claim Not Found**
  * *Route:* Move to unmatched payment queue
  * *Action:* Manual matching by payment posting team
* **Error 4: Service Line Not Matched**
  * *Route:* Hold line-level posting
  * *Action:* Review CPT, claim line, and payer control number
* **Error 5: Payment Amount Mismatch**
  * *Route:* Create reconciliation exception
  * *Action:* Finance reviews ERA vs EFT/bank deposit
* **Error 6: Denial Codes Found**
  * *Route:* Create denial worklist item
  * *Action:* AR/Denial team reviews CARC/RARC and next action
* **Error 7: Adjustment Exceeds Allowed Amount**
  * *Route:* Hold auto-posting
  * *Action:* Supervisor or finance approval required
* **Error 8: Patient Responsibility Changed**
  * *Route:* Update patient responsibility only after posting validation
  * *Action:* Hold patient billing until balance validation is complete
* **Error 9: ERA Contains Reversal / Takeback**
  * *Route:* Reverse previous payment posting
  * *Action:* Update claim ledger and patient balance
* **Error 10: Auto-Posting Rule Failed**
  * *Route:* Hold claim for manual review
  * *Action:* Payment posting team corrects or posts manually
* **Error 11: Missing EFT / Bank Deposit Match**
  * *Route:* Keep reconciliation pending
  * *Action:* Finance follows up with bank or payer
* **Error 12: Raw ERA Parsing Failed**
  * *Route:* Move file to parser exception queue
  * *Action:* Technical/support team reviews raw EDI segment
* **Error 13: PLB / Provider-Level Adjustment Found**
  * *Route:* Send to finance review if not auto-classified
  * *Action:* Post or reconcile adjustment according to policy
* **Error 14: Contract / Allowed Amount Variance**
  * *Route:* Create underpayment/overpayment review
  * *Action:* Compare payer allowed amount against contract/fee schedule
* **Error 15: Secondary Billing Required**
  * *Route:* Hold patient billing
  * *Action:* Route remaining balance to secondary billing before statement release

---

## 11. Dashboard & Status Flow

```
+----------------------+
| ERA Received         |
+----------+-----------+
           |
           v
+----------------------+
| File Validation      |
+----------+-----------+
     |                 |
     v                 v
+-------------+   +----------------------+
| Invalid /   |   | Parsed Successfully  |
| Duplicate   |   +----------+-----------+
+------+------+              |
       |                     v
       |          +----------------------+
       |          | Claim Matching       |
       |          +----------+-----------+
       |                     |
       |        +------------+-------------+----------------+
       |        |            |             |                |
       v        v            v             v                v
+----------+ +----------+ +------------+ +----------------+ +--------------+
| Exception| | Matched  | | Denial     | | Unmatched      | | Reversal /   |
| Review   | +----+-----+ | Extracted  | | Payment        | | Takeback     |
+----------+      |       +-----+------+ +--------+-------+ +------+-------+
                  |             |                 |                |
                  v             v                 v                v
             +----------+ +-------------+ +----------------+ +-------------+
             | Auto     | | Denial      | | Manual Match   | | Reverse     |
             | Posted   | | Worklist    | | Required       | | Posting     |
             +----+-----+ +-------------+ +----------------+ +-------------+
                  |
                  v
             +----------------------+
             | Contract / PLB Review|
             +----------+-----------+
                        |
                        v
             +----------------------+
             | EFT Reconciliation  |
             +----------+-----------+
                        |
                        v
             +----------------------+
             | Reconciled / Closed |
             +----------------------+
```

* **Other possible statuses:** Parser Failed, Pending Auto-Post, Posted with Exceptions, Pending EFT Match, Underpayment Review, Overpayment Review, Unapplied Cash, PLB Adjustment Review, Contract Variance Review, Secondary Billing Required, Patient Billing Hold.

---

## 12. Follow-up & Notification Flow

```
+----------------------------+
| ERA File Received          |
+-------------+--------------+
              |
              v
+----------------------------+
| If Import Failed, Notify   |
| Payment Posting Team       |
+-------------+--------------+
              |
              v
+----------------------------+
| If Claims Unmatched,       |
| Create Manual Match Task   |
+-------------+--------------+
              |
              v
+----------------------------+
| If Denials Found, Notify   |
| Denial / AR Team           |
+-------------+--------------+
              |
              v
+----------------------------+
| If Payment/PLB Mismatch,   |
| Notify Finance Team        |
+-------------+--------------+
              |
              v
+----------------------------+
| If Auto-Post Completed,    |
| Update Claim and Ledger    |
+-------------+--------------+
              |
              v
+----------------------------+
| If Secondary or Patient    |
| Billing Hold Needed, Route |
| to Correct Worklist        |
+----------------------------+
```

- If ERA is not reconciled with EFT/bank deposit within SLA, escalate to Finance Manager.
- If denial codes are present, create denial worklist item with CARC/RARC reason and priority.
- If auto-posting creates exception, keep claim out of patient billing until manual review is complete.
- If payer sends reversal/takeback, reverse previous posting and recalculate claim and patient balances.
- If unmatched payment remains unresolved, create unapplied cash follow-up task.
- If ERA creates secondary billing requirement or changes patient responsibility, hold patient billing until secondary billing and balance validation are complete.
- If PLB/provider-level adjustment is found, notify Finance for reconciliation and posting policy review.
- If contract variance is found, create underpayment/overpayment review task.

---

## Summary
- **Module:** ERA Processing
- **Complexity:** High
- **Dependencies:** Claim Submission, Claim Status, Payment Posting, Denial Management, Secondary Billing, Patient Billing, Clearinghouse/Payer 835 feeds, EFT/bank reconciliation
- **Critical:** Yes - required for accurate payment posting, denial extraction, reconciliation, PLB adjustment handling, and final patient responsibility calculation.
