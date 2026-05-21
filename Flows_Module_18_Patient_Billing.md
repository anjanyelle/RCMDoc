# Module 18: Patient Billing - Flow Documentation
Updated for Business, Production, and Industry-Level RCM Workflow

**Version:** 1.0 - Updated  
**Module ID:** MOD-018  
**Category:** Patient Financial Services / Patient Responsibility  
**Next Module:** Module 19: Collections / Payment Plans  

---

## 1. Module Overview

### Purpose
Generate, review, send, and track patient statements after all applicable insurance payments, secondary billing, adjustments, and patient responsibility calculations are completed.

### Why Hospitals Use It
Collect accurate patient balances, reduce billing disputes, support online payments, provide transparent statements, and avoid billing patients before insurance processing is complete.

### Main Users
- **Patient Billing Team**
- **Collections Team**
- **Payment Posting Team**
- **AR Manager**
- **Finance Manager**
- **Front Desk Staff**
- **Patient**
- **Compliance / Audit Team**
- **System**

### Business Goal
Improve patient collections, reduce incorrect patient statements, reduce call-center disputes, support payment plans and financial assistance, ensure patient balances are released only after insurance/secondary billing is complete, track statement cycles, comply with estimate/surprise billing rules, and reconcile gateway payments with the patient ledger.

---

## 2. Actors Involved

```
+-----------------------------------------------------------------------+
| ACTORS IN PATIENT BILLING MODULE                                      |
+-----------------------------------------------------------------------+
| 1. Patient Billing Team                                               |
|    - Reviews final patient responsibility                              |
|    - Generates and sends patient statements                            |
|    - Handles statement corrections and billing holds                   |
|                                                                       |
| 2. Patient                                                            |
|    - Receives statement by portal, email, SMS link, or mail            |
|    - Reviews balance, insurance payments, and due amount               |
|    - Pays online, requests payment plan, or asks billing question      |
|                                                                       |
| 3. Payment Posting Team                                               |
|    - Confirms insurance and patient payments are posted correctly      |
|    - Updates patient ledger after payments, refunds, or adjustments    |
|    - Reconciles payment gateway transactions with patient ledger       |
|                                                                       |
| 4. AR Manager / Collections Team                                      |
|    - Reviews unpaid patient balances and aging                         |
|    - Moves accounts to payment plan, collections, or write-off review  |
|                                                                       |
| 5. Finance Manager                                                    |
|    - Monitors patient collection rate, bad debt, and write-offs        |
|    - Reviews high-value adjustments, refunds, and credit balances      |
|                                                                       |
| 6. Front Desk Staff                                                   |
|    - Collects point-of-service payments and answers basic balance info |
|    - Updates contact details when patient confirms changes             |
|                                                                       |
| 7. Compliance / Audit Team                                            |
|    - Reviews billing accuracy, patient complaints, and statement audit |
|    - Checks PHI-safe statement delivery and access logs                |
|    - Reviews estimate / No Surprises Act related billing holds         |
|                                                                       |
| 8. System                                                             |
|    - Patient balance rules engine                                      |
|    - Statement generation, notification, payment link, audit, database |
|    - Dunning cycle, consent, payment plan, and reconciliation controls |
|                                                                       |
| 9. External Systems                                                   |
|    - Payment Gateway, Email/SMS, Patient Portal, Print/Mail Vendor     |
+-----------------------------------------------------------------------+
```

---

## 3. Step-by-Step Workflow

```
+-----------------------------+
| Insurance / Secondary       |
| Billing Completed           |
+-------------+---------------+
              |
              v
+-----------------------------+
| Final Patient Responsibility|
| Calculated                  |
+-------------+---------------+
              |
              v
+-----------------------------+
| Validate Patient Balance:   |
| - Insurance payments posted |
| - Adjustments applied       |
| - Secondary complete/closed |
| - No open claim hold        |
| - Ledger matches encounter  |
+-------------+---------------+
              |
              v
+-----------------------------+
| Check Estimate / Surprise   |
| Billing Rules if Applicable |
+-------------+---------------+
              |
        +-----+------+
        |            |
        v            v
+--------------+  +-----------------------------+
| Issue Found  |  | Balance Valid               |
+------+-------+  +-------------+---------------+
       |                        |
       v                        v
+----------------+   +-----------------------------+
| Place Statement|   | Check Patient Consent and    |
| on Hold        |   | Preferences: Portal/Email/   |
| Create Task    |   | SMS/Mail                     |
+------+---------+   +-------------+---------------+
       |                         |
       |                         v
       |             +-----------------------------+
       |             | Generate Itemized Statement  |
       |             | with Cycle: Initial/Reminder|
       |             | Final Notice                 |
       |             +-------------+---------------+
       |                         |
       |                         v
       |             +-----------------------------+
       |             | Apply Financial Assistance   |
       |             | / Payment Plan Eligibility   |
       |             +-------------+---------------+
       |                         |
       |                         v
       |             +-----------------------------+
       |             | Send Statement and Payment   |
       |             | Link to Patient              |
       |             +-------------+---------------+
       |                         |
       |                         v
       |             +-----------------------------+
       |             | Track Delivery / View / Pay  |
       |             | Initial -> Reminder 1 ->     |
       |             | Reminder 2 -> Final Notice   |
       |             +-------------+---------------+
       |                         |
       |                 +-------+-------+
       |                 |               |
       |                 v               v
       |        +----------------+ +-------------------------+
       |        | Payment Made   | | No Payment / Dispute    |
       |        +-------+--------+ +-----------+-------------+
       |                |                      |
       |                v                      v
       |        +----------------+ +-------------------------+
       |        | Verify Gateway | | Reminder / Call /       |
       |        | Webhook, Post  | | Payment Plan / Review   |
       |        | Payment, Update| +-----------+-------------+
       |        | Ledger         |             |
       |        +-------+--------+             v
       |                |            +-------------------------+
       |                |            | If credit/overpayment,  |
       |                |            | create refund review    |
       +----------------+------------+-------------------------+
                        |
                        v
             +-----------------------------+
             | Close Balance or Move to    |
             | Collections if Needed       |
             +-----------------------------+
```

---

## 4. Patient Billing Transaction / Integration Flow

```
RCM Backend            Patient Portal       Payment Gateway       Email/SMS/Mail        Patient Ledger
     |                       |                     |                    |                     |
     | Build patient bill    |                     |                    |                     |
     | - Patient ID          |                     |                    |                     |
     | - Encounter/claim IDs |                     |                    |                     |
     | - Final balance       |                     |                    |                     |
     | - Insurance payments  |                     |                    |                     |
     | - Adjustments         |                     |                    |                     |
     | - Statement cycle     |                     |                    |                     |
     | - Due date            |                     |                    |                     |
     | - Trace/statement ID  |                     |                    |                     |
     +---------------------->|                     |                    |                     |
     | Publish statement     |                     |                    |                     |
     +----------------------------------------------->|                  |
     | Confirm communication consent and send notification               |
     +------------------------------------------------------------------->|
     |                       | Patient opens/pays    |                    |
     |                       +---------------------->|                    |
     |                       |                     | Payment success/fail |
     |<---------------------------------------------+                    |
     | Verify gateway webhook signature                                  |
     | Post patient payment, receipt, and update ledger                  |
     +------------------------------------------------------------------------------------->|
     | Daily gateway-to-ledger reconciliation                            |
     | Audit statement release, delivery, payment, hold, correction, and balance changes      |
```

- **Important:** Patient statement should be released only after primary, secondary, adjustment, and patient responsibility checks are complete.
- **Important:** Payment gateway webhook must be verified before marking payment as successful.
- **Important:** Confirm patient communication consent and delivery preference before sending email/SMS statement links.
- **Important:** Reconcile payment gateway transactions with patient ledger daily.
- **Important:** Store statement ID, payment transaction ID, trace ID, delivery status, statement cycle, consent status, and ledger update for audit and support.

---

## 5. Use Case Diagram

```
+-------------------+                     +-------------------------+
| Payment Posting   |-------------------->| Confirm Final Balance   |
| Team              |                     +-------------------------+
+-------------------+                                  |
                                                     v
+-------------------+                     +-------------------------+
| System            |-------------------->| Validate Billing Hold   |
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| Compliance/System |-------------------->| Check Estimate /        |
|                   |                     | Surprise Billing Rules  |
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| Patient Billing   |-------------------->| Generate Statement      |
| Team              |                     +-------------------------+
+-------------------+                                  |
                                                     v
+-------------------+                     +-------------------------+
| System            |-------------------->| Send Email/SMS/Mail     |
|                   |                     | Based on Consent        |
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| Patient           |-------------------->| View Bill / Pay Online  |
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| Patient           |-------------------->| Request Payment Plan    |
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| Patient Billing   |-------------------->| Correct / Hold Statement|
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| Finance / AR      |-------------------->| Refund / Credit Balance |
|                   |                     | Review                  |
+-------------------+                     +-------------------------+
                                                     |
+-------------------+                     +-------------------------+
| AR / Collections  |-------------------->| Follow-up Unpaid Balance|
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
| Final Patient Balance |
| Available             |
+---+-------------------+
    |
    v
+-----------------------+
| Validate Balance,     |
| Insurance Completion, |
| Estimate/NSA Rules    |
+---+-------------------+
    |
    v
   / \
  /Hold\
 /Issue?\
 \     /
  \   /
   \/
 No|Yes
   |                         
   |                         v
   |              +-----------------------+
   |              | Place Statement Hold  |
   |              | and Create Task       |
   |              +---+-------------------+
   |                  |
   |                  v
   |              +-----------------------+
   |              | Correct Balance /     |
   |              | Missing Data / Rule   |
   |              +---+-------------------+
   |                  |
   +<-----------------+
   |
   v
+-----------------------+
| Confirm Communication |
| Consent / Preference  |
+---+-------------------+
    |
    v
+-----------------------+
| Generate Statement    |
| Cycle: Initial        |
+---+-------------------+
    |
    v
+-----------------------+
| Send via Portal /     |
| Email / SMS / Mail    |
+---+-------------------+
    |
    v
+-----------------------+
| Track Delivery, View, |
| Cycle and Due Date    |
+---+-------------------+
    |
    v
   / \
  /Paid\
 /?    \
 \    /
  \  /
   \/
 Yes|No
    |                       v
    |            +-----------------------+
    |            | Send Reminder / Offer |
    |            | Payment Plan / Review |
    |            +---+-------------------+
    |                |
    v                v
+-----------------------+
| Verify Webhook, Post  |
| Payment, Reconcile    |
| Gateway and Ledger    |
+---+-------------------+
    |
    v
+-----------------------+
| Close Balance or Move |
| to Collections        |
+---+-------------------+
    |
    v
+-------+
| END   |
+-------+
```

---

## 7. Sequence Diagram

```
Billing Team  Frontend   Backend   Rules/Ledger   Payment Gateway   Notify API   Database   Audit
    |            |          |           |                |              |          |        |
    | Generate   |          |           |                |              |          |        |
    | Statement  |          |           |                |              |          |        |
    +----------->|          |           |                |              |          |        |
    |            | POST /patient-bills |                |              |          |        |
    |            +--------->|           |                |              |          |        |
    |            |          | Validate final balance, holds, consent, estimate rules        |
    |            |          +---------->|                |              |          |        |
    |            |          | Rules OK  |                |              |          |        |
    |            |          |<----------+                |              |          |        |
    |            |          | Save statement and cycle                  |          |        |
    |            |          +-------------------------------------------------->|        |
    |            |          | Send notification if consent exists       |          |        |
    |            |          +-------------------------------------->|          |        |
    |            |          | Audit statement release                 |          |        |
    |            |          +---------------------------------------------------------->|
    | Response   |          |           |                |              |          |        |
    |<-----------+          |           |                |              |          |        |
    |            |          | Patient pays via portal                 |          |        |
    |            |          |<-------------------------- Payment webhook success/fail      |
    |            |          | Verify webhook signature                |          |        |
    |            |          | Post payment / update ledger            |          |        |
    |            |          +-------------------------------------------------->|        |
    |            |          | Reconcile gateway transaction           |          |        |
    |            |          +-------------------------------------------------->|        |
    |            |          | Audit payment, reconciliation, balance update                 |
    |            |          +---------------------------------------------------------->|
```

---

## 8. API Flow

### Request

`POST /api/patient-bills`

```json
{
  "patientId": "PAT-00001",
  "encounterId": "ENC-00001",
  "claimId": "CLM-00001",
  "primaryClaimId": "CLM-PRIMARY-00001",
  "secondaryClaimId": "CLM-SEC-00001",
  "finalPatientResponsibility": 35.00,
  "insurancePaidAmount": 145.00,
  "adjustmentAmount": 20.00,
  "dueDate": "2026-06-20",
  "deliveryPreference": "portal_email_sms",
  "communicationConsent": true,
  "statementType": "initial",
  "statementCycle": "initial",
  "paymentPlanEligible": true,
  "financialAssistanceEligible": false,
  "estimateComplianceChecked": true,
  "traceId": "TRC-BILL-00001",
  "createdBy": "USR-001"
}
```

### Response - Statement Created

```json
{
  "patientBillId": "PBILL-00001",
  "statementId": "STMT-00001",
  "status": "ready_to_send",
  "amountDue": 35.00,
  "statementHold": false,
  "statementCycle": "initial",
  "nextReminderAt": "2026-06-27T09:00:00Z",
  "paymentLinkCreated": true,
  "message": "Patient statement created and ready for delivery",
  "traceId": "TRC-BILL-00001"
}
```

### Response - Payment Posted

```json
{
  "patientBillId": "PBILL-00001",
  "status": "paid",
  "paymentTransactionId": "PAY-98765",
  "amountPaid": 35.00,
  "remainingBalance": 0.00,
  "receiptGenerated": true,
  "reconciliationStatus": "pending_daily_reconciliation",
  "message": "Patient payment posted and balance closed"
}
```

### Response - Statement Hold

```json
{
  "patientBillId": "PBILL-00001",
  "status": "hold",
  "holdReason": "Secondary claim still pending",
  "message": "Statement cannot be released until insurance processing is complete"
}
```

---

## 9. Database Flow

```sql
-- Create patient bill / statement
INSERT INTO patient_bills (
    patient_bill_id,
    patient_id,
    encounter_id,
    claim_id,
    primary_claim_id,
    secondary_claim_id,
    final_patient_responsibility,
    insurance_paid_amount,
    adjustment_amount,
    amount_due,
    due_date,
    status,
    statement_type,
    statement_cycle,
    delivery_preference,
    communication_consent,
    payment_plan_eligible,
    financial_assistance_eligible,
    estimate_compliance_checked,
    last_statement_sent_at,
    next_reminder_at,
    trace_id,
    created_by,
    created_at,
    updated_at
) VALUES (...);

-- Save statement delivery record
INSERT INTO patient_statement_deliveries (
    delivery_id,
    patient_bill_id,
    channel,
    delivery_status,
    sent_at,
    viewed_at,
    failure_reason
) VALUES (...);

-- Save payment link / gateway transaction
INSERT INTO patient_payment_transactions (
    transaction_id,
    patient_bill_id,
    gateway_name,
    gateway_transaction_id,
    amount,
    status,
    webhook_verified,
    reconciled,
    reconciled_at,
    paid_at,
    raw_gateway_response
) VALUES (...);

-- Post patient payment to ledger
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

-- Update bill after payment
UPDATE patient_bills
SET status = 'paid',
    amount_paid = 35.00,
    remaining_balance = 0.00,
    paid_at = NOW(),
    updated_at = NOW()
WHERE patient_bill_id = 'PBILL-00001';

-- Place or remove statement hold
UPDATE patient_bills
SET status = 'hold',
    hold_reason = 'Secondary claim still pending',
    updated_at = NOW()
WHERE patient_bill_id = 'PBILL-00001';

-- Daily gateway reconciliation
UPDATE patient_payment_transactions
SET reconciled = true,
    reconciled_at = NOW()
WHERE transaction_id = 'PAY-98765';
```

---

## 10. Error Scenarios

- **Error 1: Insurance Processing Not Complete**
  - Route: Place statement on hold
  - Action: Notify billing team to wait for primary/secondary completion
- **Error 2: Patient Balance Mismatch**
  - Route: Hold statement release
  - Action: Reconcile ledger, ERA/EOB, adjustments, and payments
- **Error 3: Statement Sent with Wrong Balance**
  - Route: Place corrected statement workflow
  - Action: Notify patient billing team and audit correction
- **Error 4: Payment Gateway Failure**
  - Route: Show payment failed message
  - Action: Allow retry or alternative payment method
- **Error 5: Payment Webhook Not Verified**
  - Route: Do not mark payment successful
  - Action: Move transaction to manual review
- **Error 6: Duplicate Patient Payment**
  - Route: Create refund/adjustment review task
  - Action: Finance/AR approval before refund
- **Error 7: Statement Delivery Failed**
  - Route: Retry delivery or switch channel
  - Action: Notify billing team if repeated failure
- **Error 8: Patient Disputes Balance**
  - Route: Place account on dispute hold
  - Action: Review EOB, statement, ledger, and documentation
- **Error 9: Payment Plan Requested**
  - Route: Validate payment plan amount, due date, installment frequency, approval requirement, and missed-payment rule
  - Action: Hold collections while plan is active
- **Error 10: Financial Assistance Requested**
  - Route: Route to charity/financial assistance review
  - Action: Hold statement/collections until decision
- **Error 11: Patient Statement Released Before Secondary Complete**
  - Route: Hold/correct statement
  - Action: Notify patient billing team and update ledger after secondary result
- **Error 12: Patient Credit Balance / Refund Needed**
  - Route: Create refund or adjustment review task
  - Action: Finance/AR approval before refund
- **Error 13: Communication Consent Missing**
  - Route: Do not send SMS/email statement link
  - Action: Use approved delivery method or update consent/preference
- **Error 14: Estimate / Surprise Billing Review Required**
  - Route: Place statement on compliance hold
  - Action: Release only after review is completed

---

## 11. Dashboard & Status Flow

```
+----------------------+
| Final Patient Resp.  |
| Available            |
+----------+-----------+
           |
           v
+----------------------+
| Billing Validation   |
+----------+-----------+
     |                 |
     v                 v
+-------------+   +----------------------+
| Hold /      |   | Statement Created    |
| Correction  |   +----------+-----------+
+------+------+              |
       |                     v
       |          +----------------------+
       |          | Sent / Delivered     |
       |          +----------+-----------+
       |                     |
       |        +------------+-------------+----------------+
       |        |            |             |                |
       v        v            v             v                v
+----------+ +----------+ +------------+ +----------------+ +--------------+
| Hold     | | Viewed   | | Payment    | | Payment Plan   | | Dispute      |
| Reason   | +----+-----+ | Pending    | | Requested      | | Review       |
+----------+      |       +-----+------+ +--------+-------+ +------+-------+
                  |             |                 |                |
                  v             v                 v                v
             +----------+ +-------------+ +----------------+ +-------------+
             | Paid     | | Reminder    | | Plan Active    | | Corrected   |
             +----+-----+ | Required    | +----------------+ | Statement   |
                  |       +-------------+                    +-------------+
                  v
             +----------------------+
             | Gateway Reconcile    |
             | Pending / Complete   |
             +----------+-----------+
                        |
                        v
             +----------------------+
             | Balance Closed       |
             +----------------------+
```

**Other possible statuses:** Delivery Failed, Gateway Failed, Duplicate Payment Review, Financial Assistance Review, Collections Ready, Statement Corrected, Initial Statement, Reminder 1, Reminder 2, Final Notice, Credit Balance / Refund Review, Communication Consent Missing, Estimate / Surprise Billing Hold.

---

## 12. Follow-up & Notification Flow

```
+----------------------------+
| Statement Created          |
+-------------+--------------+
              |
              v
+----------------------------+
| Confirm Consent and Send   |
| Portal/Email/SMS/Mail      |
+-------------+--------------+
              |
              v
+----------------------------+
| If Delivered, Track View   |
+-------------+--------------+
              |
              v
+----------------------------+
| If Not Paid by Due Date,   |
| Move to Next Statement     |
| Cycle / Send Reminder      |
+-------------+--------------+
              |
              v
+----------------------------+
| If Patient Requests Plan,  |
| Validate Terms and Route   |
| to Payment Plan Review     |
+-------------+--------------+
              |
              v
+----------------------------+
| If Dispute / Wrong Balance,|
| Hold and Review            |
+-------------+--------------+
              |
              v
+----------------------------+
| If Paid, Verify Webhook,   |
| Send Receipt and Reconcile |
+-------------+--------------+
              |
              v
+----------------------------+
| If Aging Exceeds Policy,   |
| Move to Collections Review |
+----------------------------+
```

- If secondary payment or primary EOB correction changes the balance, hold or correct statement before patient collection.
- If payment gateway fails, notify patient and keep balance open until verified payment success.
- If statement delivery fails, retry or switch to another approved delivery method.
- If patient disputes the balance, pause collections until review is completed.
- If financial assistance is requested, pause patient billing/collections until decision is made.
- If patient payment creates a credit balance, create refund/adjustment review before issuing refund.
- If communication consent is missing, use only approved delivery method and update patient preferences.
- Reconcile payment gateway transactions with patient ledger daily and create exception tasks for mismatches.
