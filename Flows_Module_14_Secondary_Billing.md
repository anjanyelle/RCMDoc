# Module 20: Secondary Billing - Flow Documentation
**Updated for Business, Production, and Industry-Level RCM Workflow**

**Version:** 1.0 - Updated  
**Module ID:** MOD-020  
**Category:** Billing / Claims / Revenue Cycle Management  
**Next Module:** Module 21: Patient Responsibility / Patient Billing  

---

## 1. Module Overview
* **Purpose:** Create and submit secondary insurance claims after the primary payer adjudicates the claim, using primary EOB/ERA details, remaining balance, COB rules, and correct patient responsibility calculation.
* **Why Hospitals Use It:** Recover additional reimbursement from secondary insurance, reduce patient balance errors, prevent duplicate billing, and avoid revenue leakage after primary payment.
* **Main Users:** Billing Specialist, AR Manager, Payment Posting Team, Insurance Verification Team, Collections Team, Finance Manager, Compliance / Audit Team, System.
* **Business Goal:** Increase total reimbursement, reduce incorrect patient billing, reduce secondary claim denials, reduce secondary timely filing losses, and prevent patient statements before all available insurance benefits are processed.

---

## 2. Actors Involved
```
+-----------------------------------------------------------------------+
| ACTORS IN SECONDARY BILLING MODULE                                    |
+-----------------------------------------------------------------------+
| 1. Billing Specialist                                                 |
|    - Reviews primary payment/EOB                                      |
|    - Creates secondary claim                                           |
|    - Submits secondary claim to clearinghouse/payer                    |
|                                                                       |
| 2. AR Manager / AR Team                                               |
|    - Monitors secondary claim status                                   |
|    - Follows up unpaid or denied secondary claims                      |
|    - Reviews underpayment, overpayment, and aging issues               |
|                                                                       |
| 3. Payment Posting Team                                               |
|    - Posts primary ERA/EOB details                                     |
|    - Confirms remaining balance and patient responsibility             |
|    - Posts secondary payment after response                            |
|    - Recalculates balance if primary EOB is reversed/corrected         |
|                                                                       |
| 4. Insurance Verification Team                                        |
|    - Confirms secondary payer coverage and COB order                   |
|    - Updates secondary policy details if incorrect                     |
|                                                                       |
| 5. Collections / Patient Billing Team                                 |
|    - Waits until secondary billing is completed before billing patient |
|    - Sends patient statement only for true final responsibility        |
|    - Holds/corrects statement if secondary balance changes             |
|                                                                       |
| 6. Finance Manager                                                    |
|    - Reviews secondary collection performance                          |
|    - Monitors underpayment, overpayment, write-off, and balance accuracy|
|                                                                       |
| 7. Compliance / Audit Team                                            |
|    - Reviews secondary billing accuracy                                |
|    - Checks COB-related billing issues                                 |
|    - Audits patient balance calculation and claim changes              |
|                                                                       |
| 8. System                                                             |
|    - COB rules engine                                                  |
|    - Claim generation and status tracking                              |
|    - ERA/EOB parsing, audit, and database layer                        |
|                                                                       |
| 9. External Systems                                                   |
|    - Clearinghouse, primary payer, secondary payer                     |
|    - EDI 837, 835, 276/277, 999/277CA where supported                  |
+-----------------------------------------------------------------------+
```

---

## 3. Step-by-Step Workflow
```
+----------------------------+
| Primary Claim Submitted    |
| and Processed              |
+-------------+--------------+
              |
              v
+----------------------------+
| Primary ERA/EOB Received   |
| and Payment Posted         |
+-------------+--------------+
              |
              v
+----------------------------+
| System Calculates          |
| Remaining Balance          |
+-------------+--------------+
              |
              v
+----------------------------+
| Check Patient Has          |
| Secondary Insurance        |
+-------------+--------------+
              |
        +-----+------+
        |            |
        v            v
+--------------+  +----------------------------+
| No Secondary |  | Secondary Insurance Found  |
| Insurance    |  +-------------+--------------+
+------+-------+                |
       |                        v
       |          +----------------------------+
       |          | Verify COB Order and       |
       |          | Secondary Coverage         |
       |          +-------------+--------------+
       |                        |
       |                        v
       |          +----------------------------+
       |          | Validate Primary EOB/ERA   |
       |          | - Paid amount              |
       |          | - Adjustments              |
       |          | - Deductible/copay/coins   |
       |          | - Patient responsibility   |
       |          | - Claim/line status        |
       |          +-------------+--------------+
       |                        |
       |                        v
       |          +----------------------------+
       |          | Check Timely Filing        |
       |          | Deadline and Claim IDs     |
       |          +-------------+--------------+
       |                        |
       |                        v
       |          +----------------------------+
       |          | Create Secondary Claim     |
       |          | with Primary EOB Details   |
       |          +-------------+--------------+
       |                        |
       |                        v
       |          +----------------------------+
       |          | Scrub Secondary Claim      |
       |          | for payer rules/errors     |
       |          +-------------+--------------+
       |                        |
       |                        v
       |          +----------------------------+
       |          | Submit Secondary Claim     |
       |          | via Clearinghouse/API      |
       |          +-------------+--------------+
       |                        |
       |                        v
       |          +----------------------------+
       |          | Track Ack / Rejection /    |
       |          | Claim Status               |
       |          +-------------+--------------+
       |                        |
       |                        v
       |          +----------------------------+
       |          | Secondary ERA/EOB Received |
       |          | and Payment Posted         |
       |          +-------------+--------------+
       |                        |
       |                        v
       |          +----------------------------+
       |          | Check if Primary EOB/ERA   |
       |          | Was Adjusted/Reversed      |
       |          +-------------+--------------+
       |                        |
       +------------------------+
              |
              v
+----------------------------+
| Validate Secondary Payment,|
| Adjustment, and Balance    |
+-------------+--------------+
              |
              v
+----------------------------+
| Calculate Final Patient    |
| Responsibility             |
+-------------+--------------+
              |
              v
+----------------------------+
| Send to Patient Billing    |
| or Hold Statement if Needed|
+----------------------------+
```

---

## 4. Secondary Claim Transaction / Integration Flow
```
RCM Backend             Clearinghouse/API       Secondary Payer       Payment Posting
     |                         |                       |                      |
     | Build secondary claim   |                       |                      |
     | - Original claim data   |                       |                      |
     | - Primary claim control |                       |                      |
     | - Primary payer paid    |                       |                      |
     | - Adjustments/CARC/RARC |                       |                      |
     | - Remaining balance     |                       |                      |
     | - COB details           |                       |                      |
     | - Timely filing deadline|                       |                      |
     | - Trace/claim ID        |                       |                      |
     +------------------------>|                       |                      |
     |                         | Forward 837 claim     |                      |
     |                         +---------------------->|                      |
     |                         |                       |                      |
     | Acknowledgment / 277CA  |                       |                      |
     |<------------------------+<----------------------+                      |
     |                         |                       |                      |
     | Save submission batch ID and payer claim control number if available  |
     |                         |                       |                      |
     | Claim status 276/277    |                       |                      |
     |<------------------------------------------------+                      |
     |                         |                       |                      |
     | Secondary ERA/EOB 835   |                       |                      |
     |<------------------------------------------------+                      |
     |                         |                       |                      |
     | Parse ERA/EOB and post payment                                          |
     +--------------------------------------------------------------------->|
     |                                                                      |
     | Update claim, balance, patient responsibility, and audit trail        |
     |                                                                      |
```
* **Important:** Use EDI 837 for secondary claim submission when supported by clearinghouse/payer.
* **Important:** Use EDI 835/ERA or manual EOB posting for secondary payment response.
* **Important:** Use 999/277CA acknowledgments to confirm secondary claim acceptance or rejection.
* **Important:** Store trace ID, original claim ID, secondary claim ID, primary EOB/ERA, raw response, parsed response, submission batch ID, and payer claim control number for audit and support.

---

## 5. Use Case Diagram
```
+-------------------+                     +-------------------------+
| Payment Posting   |-------------------->| Post Primary ERA/EOB     |
| Team              |                     +-------------------------+
+-------------------+                                  |
                                                     v
+-------------------+                     +-------------------------+
| System            |-------------------->| Check Secondary Coverage |
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| Billing Specialist|-------------------->| Create Secondary Claim   |
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| System            |-------------------->| Scrub Secondary Claim    |
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| Clearinghouse /   |-------------------->| Submit to Secondary Payer|
| Payer             |                     +-------------------------+
+-------------------+                                  |
                                                     v
+-------------------+                     +-------------------------+
| AR Team           |-------------------->| Track Status / Follow-up |
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| Payment Posting   |-------------------->| Post Secondary Payment   |
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| AR Team           |-------------------->| Review Under/Overpayment |
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| Payment Posting   |-------------------->| Recalculate Balance if   |
| Team              |                     | Primary EOB Reversed     |
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| Patient Billing   |-------------------->| Bill Final Patient Bal.  |
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
| Primary EOB/ERA Posted|
+---+-------------------+
    |
    v
+-----------------------+
| Check Remaining Bal.  |
+---+-------------------+
    |
    v
   /   /Sec /Ins?  \     /
  \   /
   \/
 No|Yes
   |                         
   |                         v
   |              +-----------------------+
   |              | Verify Secondary COB  |
   |              | and Eligibility       |
   |              +---+-------------------+
   |                  |
   |                  v
   |                 /    |                /Valid   |               /?        |               \      /
   |                \    /
   |                 \/
   |        +--------+--------+
   |        |                 |
   |        v                 v
   | +--------------+  +-----------------------+
   | | Update /     |  | Check Timely Filing   |
   | | Manual Review|  +---+-------------------+
   | +------+-------+      |
   |        |              v
   |        |       +-----------------------+
   |        |       | Create Secondary      |
   |        |       | Claim                 |
   |        |       +---+-------------------+
   |        |              |
   |        |              v
   |        |       +-----------------------+
   |        |       | Scrub Claim           |
   |        |       +---+-------------------+
   |        |              |
   |        |              v
   |        |       +-----------------------+
   |        |       | Submit Claim          |
   |        |       +---+-------------------+
   |        |              |
   |        |              v
   |        |       +-----------------------+
   |        |       | Track Ack/Status      |
   |        |       +---+-------------------+
   |        |              |
   |        |              v
   |        |       +-----------------------+
   |        |       | Post Secondary ERA/EOB|
   |        |       +---+-------------------+
   |        |              |
   |        |              v
   |        |       +-----------------------+
   |        |       | Validate Payment and  |
   |        |       | Remaining Balance     |
   |        |       +---+-------------------+
   +--------+--------------+
            |
            v
+-----------------------+
| Calculate Final       |
| Patient Responsibility|
+---+-------------------+
    |
    v
+-----------------------+
| Move to Patient       |
| Billing if balance > 0|
| or Hold if issue found|
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
Billing   Frontend   Backend   Rules/COB   Clearinghouse   Sec Payer   Database   Patient Billing   Audit
   |          |          |          |             |             |          |             |          |
   | Create   |          |          |             |             |          |             |          |
   | Sec Claim|          |          |             |             |          |             |          |
   +--------->|          |          |             |             |          |             |          |
   |          | POST /secondary-claims           |             |          |             |          |
   |          +--------->|          |             |             |          |             |          |
   |          |          | Validate COB/EOB       |             |          |             |          |
   |          |          +--------->|             |             |          |             |          |
   |          |          | Rules OK |             |             |          |             |          |
   |          |          |<---------+             |             |          |             |          |
   |          |          | Save secondary claim   |             |          |             |          |
   |          |          +------------------------------------>|          |             |          |
   |          |          | Submit 837             |             |          |             |          |
   |          |          +---------------------->|             |          |             |          |
   |          |          | Ack/277CA              |             |          |             |          |
   |          |          |<----------------------+             |          |             |          |
   |          | Response |          |             |             |          |             |          |
   |          |<---------+          |             |             |          |             |          |
   | Display  |          |          |             |             |          |             |          |
   | Status   |          |          |             |             |          |             |          |
   |<---------+          |          |             |             |          |             |          |
   |          |          | Secondary ERA/EOB 835  |             |          |             |          |
   |          |          |<-----------------------------------------------+             |          |
   |          |          | Post secondary payment |             |          |             |          |
   |          |          +------------------------------------>|          |             |          |
   |          |          | Audit payment posting  |             |          |             |          |
   |          |          +-------------------------------------------------------------------->|
   |          |          | Update final balance   |             |          |             |          |
   |          |          +------------------------------------>|          |             |          |
   |          |          | Audit balance recalculation and billing release                  |
   |          |          +-------------------------------------------------------------------->|
   |          |          | If patient balance > 0, send/hold patient billing                 |
   |          |          +------------------------------------------------------------>|          |
```

---

## 8. API Flow

### Request
```json
POST /api/secondary-claims
{
  "patientId": "PAT-00001",
  "encounterId": "ENC-00001",
  "primaryClaimId": "CLM-PRIMARY-00001",
  "primaryClaimControlNumber": "PCN-12345",
  "secondaryInsuranceId": "INS-SECONDARY-00001",
  "secondaryPayerId": "AETNA002",
  "secondaryPolicyOrder": 2,
  "primaryPayerId": "BCBS001",
  "primaryPaidAmount": 120.00,
  "primaryAdjustmentAmount": 30.00,
  "patientResponsibility": 30.00,
  "remainingBalance": 30.00,
  "primaryEobId": "EOB-00001",
  "timelyFilingDeadline": "2026-08-20",
  "serviceLines": [
    {
      "cptCode": "99213",
      "billedAmount": 150.00,
      "primaryPaid": 120.00,
      "adjustment": 30.00,
      "remainingBalance": 30.00,
      "carcCodes": ["PR-2"],
      "rarcCodes": []
    }
  ],
  "traceId": "TRC-SEC-00001",
  "createdBy": "USR-001"
}
```

### Response - Secondary Claim Created
```json
{
  "secondaryClaimId": "CLM-SEC-00001",
  "status": "ready_for_submission",
  "scrubStatus": "passed",
  "message": "Secondary claim created and ready for submission",
  "traceId": "TRC-SEC-00001"
}
```

### Response - Submitted
```json
{
  "secondaryClaimId": "CLM-SEC-00001",
  "status": "submitted",
  "submissionBatchId": "BATCH-SEC-00001",
  "clearinghouseTraceId": "CH-SEC-98765",
  "payerClaimControlNumber": "PCCN-98765",
  "acknowledgmentStatus": "pending",
  "message": "Secondary claim submitted to clearinghouse"
}
```

### Response - Secondary Payment Posted
```json
{
  "secondaryClaimId": "CLM-SEC-00001",
  "status": "paid",
  "secondaryPaidAmount": 25.00,
  "finalPatientResponsibility": 5.00,
  "patientBillingRequired": true,
  "patientStatementStatus": "ready",
  "message": "Secondary payment posted and final patient balance calculated"
}
```

---

## 9. Database Flow
```sql
-- Create secondary claim
INSERT INTO secondary_claims (
    secondary_claim_id,
    patient_id,
    encounter_id,
    primary_claim_id,
    primary_claim_control_number,
    secondary_insurance_id,
    secondary_policy_order,
    secondary_payer_id,
    primary_eob_id,
    primary_paid_amount,
    primary_adjustment_amount,
    patient_responsibility,
    remaining_balance,
    timely_filing_deadline,
    status,
    scrub_status,
    trace_id,
    created_by,
    created_at,
    updated_at
) VALUES (...);

-- Save secondary claim line details
INSERT INTO secondary_claim_lines (
    line_id,
    secondary_claim_id,
    cpt_code,
    billed_amount,
    primary_paid,
    primary_adjustment,
    remaining_balance,
    carc_codes,
    rarc_codes,
    status
) VALUES (...);

-- Save clearinghouse submission message
INSERT INTO secondary_claim_messages (
    message_id,
    secondary_claim_id,
    message_type,
    trace_id,
    submission_batch_id,
    clearinghouse_trace_id,
    payer_claim_control_number,
    raw_payload,
    raw_response,
    acknowledgment_status,
    status,
    sent_at
) VALUES (...);

-- Post secondary payment
UPDATE secondary_claims
SET status = 'paid',
    secondary_paid_amount = 25.00,
    final_patient_responsibility = 5.00,
    paid_at = NOW(),
    balance_recalculated_at = NOW(),
    updated_at = NOW()
WHERE secondary_claim_id = 'CLM-SEC-00001';

-- Handle primary EOB reversal / correction
UPDATE secondary_claims
SET status = 'balance_recalculation_required',
    balance_recalculated_at = NOW(),
    updated_at = NOW()
WHERE primary_claim_id = 'CLM-PRIMARY-00001';

-- Update patient ledger after secondary payment
INSERT INTO patient_ledger (
    ledger_id,
    patient_id,
    encounter_id,
    source_type,
    source_id,
    amount,
    balance_type,
    created_at
) VALUES (...);

-- Move final balance to patient billing if needed
UPDATE encounters
SET final_patient_balance = 5.00,
    patient_billing_status = 'ready',
    patient_statement_released_at = NOW()
WHERE encounter_id = 'ENC-00001';

-- Hold patient statement when secondary balance changes
UPDATE encounters
SET patient_billing_status = 'hold',
    updated_at = NOW()
WHERE encounter_id = 'ENC-00001';
```

---

## 10. Error Scenarios
```
Error 1: No Secondary Insurance Found
   |
   v
Move remaining balance to patient responsibility review
   |
   v
Send to patient billing if balance is valid

Error 2: Secondary Insurance Inactive
   |
   v
Notify insurance verification team
   |
   v
Update policy or move to patient responsibility after review

Error 3: COB Order Incorrect
   |
   v
Hold secondary claim
   |
   v
Correct primary/secondary payer order before submission

Error 4: Primary EOB/ERA Missing
   |
   v
Block secondary claim creation
   |
   v
Request primary EOB/ERA or post primary payment first

Error 5: Secondary Claim Scrub Failed
   |
   v
Show errors
   |
   v
Correct claim details and rescrub

Error 6: Clearinghouse Rejection
   |
   v
Show rejection reason
   |
   v
Billing corrects and resubmits

Error 7: Secondary Payer Denial
   |
   v
Route to AR/Denial worklist
   |
   v
Appeal, correct, or move balance based on denial reason

Error 8: Duplicate Secondary Claim Found
   |
   v
Show existing secondary claim
   |
   v
Prevent duplicate unless supervisor override is allowed

Error 9: Secondary Payment Less Than Expected
   |
   v
Create underpayment review task
   |
   v
AR team reviews contract/COB/payment reason

Error 10: Patient Balance Calculated Before Secondary Billing Complete
   |
   v
Block patient statement
   |
   v
Wait for secondary claim resolution or supervisor approval

Error 11: Secondary ERA/EOB Unmatched
   |
   v
Move to unmatched payment queue
   |
   v
Manual matching by payment posting team

Error 12: Timely Filing Risk
   |
   v
Escalate secondary claim
   |
   v
Submit urgently or document reason for delay

Error 13: Primary EOB Reversed or Corrected
   |
   v
Hold secondary claim or recalculate secondary balance
   |
   v
Update patient ledger and patient billing status

Error 14: Secondary Overpayment
   |
   v
Create refund/adjustment review task
   |
   v
Finance or AR team reviews before action
```

---

## 11. Dashboard & Status Flow
```
+----------------------+
| Primary Paid / EOB   |
| Posted               |
+----------+-----------+
           |
           v
+----------------------+
| Secondary Check      |
+----------+-----------+
     |                 |
     v                 v
+-------------+   +----------------------+
| No Secondary|   | Secondary Eligible   |
+------+------+   +----------+-----------+
       |                     |
       v                     v
+-------------+   +----------------------+
| Patient     |   | Secondary Claim      |
| Balance Rev.|   | Created              |
+-------------+   +----------+-----------+
                             |
                             v
+----------------------+
| Scrubbed / Ready     |
+----------+-----------+
           |
           v
+----------------------+
| Submitted            |
+----------+-----------+
           |
    +------+-------+----------------+
    |              |                |
    v              v                v
+----------+ +-------------+ +----------------+
| Accepted | | Rejected    | | Denied         |
+----+-----+ +------+------+ +-------+--------+
     |              |                |
     v              v                v
+----------+ +-------------+ +----------------+
| Paid     | | Correction  | | AR Follow-up   |
| paid     | | Needed      | | / Appeal       |
+----+-----+ +-------------+ +----------------+
     |
     v
+----------------------+
| Validate Secondary   |
| Payment and Balance  |
+----------+-----------+
           |
           v
+----------------------+
| Final Patient Resp.  |
+----------+-----------+
           |
           v
+----------------------+
| Ready / Hold Patient |
| Statement            |
+----------------------+

Other possible statuses: COB Hold, EOB Missing, Timely Filing Risk, Duplicate Claim, Underpayment Review, Unmatched ERA, Primary EOB Reversed, Balance Recalculation Required, Secondary Overpayment Review, Patient Statement Hold.
```

---

## 12. Follow-up & Notification Flow
```
+----------------------------+
| Primary EOB/ERA Posted     |
+-------------+--------------+
              |
              v
+----------------------------+
| If Secondary Exists,       |
| Notify Billing Team        |
+-------------+--------------+
              |
              v
+----------------------------+
| If COB/Eligibility Issue,  |
| Notify Verification Team   |
+-------------+--------------+
              |
              v
+----------------------------+
| If Secondary Claim Ready,  |
| Submit or Queue for Batch  |
+-------------+--------------+
              |
              v
+----------------------------+
| If Rejected, Notify        |
| Billing Specialist         |
+-------------+--------------+
              |
              v
+----------------------------+
| If Denied or Unpaid > SLA, |
| Notify AR Team             |
+-------------+--------------+
              |
              v
+----------------------------+
| If Secondary Paid,         |
| Notify Payment Posting     |
| and Patient Billing        |
+-------------+--------------+
              |
              v
+----------------------------+
| If Final Patient Balance   |
| Exists, Release Statement  |
| or Hold if Issue Found     |
+----------------------------+
```
* **Important:** If secondary claim is close to timely filing limit, escalate to billing supervisor.
* **Important:** If primary EOB is corrected or reversed, recheck secondary claim and patient balance.
* **Important:** If secondary payer denies due to COB issue, return to insurance verification for correction.
* **Important:** If final patient balance changes after secondary payment, update patient ledger before statement generation.
* **Important:** If patient statement is already generated and secondary payment changes balance, notify patient billing team to correct or hold statement.
* **Important:** If secondary overpayment is found, notify AR/Finance for adjustment or refund review.
