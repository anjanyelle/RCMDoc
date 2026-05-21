# Module 4: Prior Authorization / Referral Management - Flow Documentation
**Updated for Business, Production, and Industry-Level RCM Workflow**

**Version:** 1.0 - Updated  
**Module ID:** MOD-004  
**Category:** Category 1: Patient Access Management

---

## 1. Module Overview
* **Purpose:** Check whether insurance approval is required before service, submit authorization requests, track payer decision, and save authorization number for claim submission.
* **Why Hospitals Use It:** Prevent authorization-related denials, confirm medical necessity, avoid delayed procedures, and make sure claims include valid authorization details.
* **Main Users:** Prior Authorization Specialist, Front Desk Staff, Billing Team, Provider, Clinical Staff.
* **Business Goal:** Reduce prior-authorization denials, avoid cancelled or delayed services, improve clean claim rate, reduce avoidable write-offs, prevent cancelled procedures, and improve reimbursement accuracy by ensuring authorization is completed before service is provided.

---

## 2. Actors Involved
```
+---------------------------------------------------------+
| ACTORS IN PRIOR AUTHORIZATION MODULE                    |
+---------------------------------------------------------+
|                                                         |
| 1. Prior Authorization Specialist                       |
|    - Checks if authorization is required                 |
|    - Submits authorization request                       |
|    - Uploads clinical documents                          |
|    - Tracks approval, denial, or pending status          |
|                                                         |
| 2. Provider / Doctor                                    |
|    - Orders service or procedure                         |
|    - Provides clinical notes and medical necessity       |
|    - Responds to payer questions if more info needed     |
|                                                         |
| 3. Clinical Staff                                       |
|    - Supports document collection                        |
|    - Shares orders, diagnosis, lab, imaging, notes       |
|                                                         |
| 4. Front Desk / Scheduling Team                         |
|    - Checks auth status before appointment/procedure     |
|    - Holds or reschedules service if auth is pending     |
|                                                         |
| 5. Billing Team                                         |
|    - Uses authorization number on the claim              |
|    - Reviews authorization before claim submission       |
|                                                         |
| 6. System                                               |
|    - Authorization rules engine                          |
|    - Document upload service                             |
|    - Status tracking and database                        |
|                                                         |
| 7. External APIs                                        |
|    - Payer Portal / Payer API                            |
|    - Availity / Waystar authorization services           |
|    - EDI 278 request/response where supported            |
|                                                         |
| 8. Payer Reviewer / Insurance Reviewer                  |
|    - Reviews medical necessity                           |
|    - Approves, denies, or requests more information      |
|    - Provides authorization number or denial reason      |
|                                                         |
+---------------------------------------------------------+
```

---

## 3. Step-by-Step Workflow
```
+--------------------------+
| Service / Procedure      |
| Ordered by Provider      |
| (from Encounter/Orders)  |
+------------+-------------+
             |
             v
+--------------------------+
| System Checks Patient    |
| Insurance and Service    |
| Type                     |
+------------+-------------+
             |
             v
+--------------------------+
| Check Authorization Rule |
| by Payer + CPT/Service   |
+------------+-------------+
             |
        +----+----+
        |         |
        v         v
+--------------+  +--------------------------+
| Auth Not     |  | Auth Required            |
| Required     |  +------------+-------------+
+------+-------+               |
       |                       v
       |          +--------------------------+
       |          | Check Existing Valid     |
       |          | Authorization            |
       |          | Same patient, payer,     |
       |          | provider, CPT, date,     |
       |          | and units                |
       |          +------------+-------------+
       |                       |
       |              +--------+--------+
       |              |                 |
       |              v                 v
       |     +----------------+  +--------------------------+
       |     | Existing Auth  |  | Create Authorization     |
       |     | Found - Link   |  | Case                     |
       |     | to Order       |  +------------+-------------+
       |     +-------+--------+               |
       |             |                        v
       |             |           +--------------------------+
       |             |           | Set Priority:            |
       |             |           | Standard / Urgent / Stat |
       |             |           +------------+-------------+
       |             |                        |
       |             |                        v
       |             |           +--------------------------+
       |             |           | Collect Required Data:   |
       |             |           | - Patient details        |
       |             |           | - Insurance details      |
       |             |           | - Provider NPI           |
       |             |           | - Diagnosis code         |
       |             |           | - CPT/service code       |
       |             |           | - Units requested        |
       |             |           | - Medical necessity docs |
       |             |           +------------+-------------+
       |             |                        |
       |             |                        v
       |             |           +--------------------------+
       |             |           | Submit Request to Payer  |
       |             |           | Portal/API/EDI 278       |
       |             |           +------------+-------------+
       |             |                        |
       |             |                        v
       |             |           +--------------------------+
       |             |           | Payer Reviews Request    |
       |             |           +------------+-------------+
       |             |                        |
       |             |                +-------+-------+
       |             |                |               |
       |             |                v               v
       |             |        +---------------+   +-------------------+
       |             |        | Approved      |   | Pending / Denied  |
       |             |        +-------+-------+   +---------+---------+
       |             |                |                     |
       |             |                v                     v
       |             |        +---------------+   +-------------------+
       |             |        | Validate Auth |   | More Info / Appeal|
       |             |        | No, Dates,    |   | Peer Review or    |
       |             |        | CPT, Units    |   | Reschedule        |
       |             |        +-------+-------+   +---------+---------+
       |             |                |                     |
       +-------------+----------------+---------------------+
                                      v
                         +--------------------------+
                         | Update Appointment /     |
                         | Order / Claim Status     |
                         +------------+-------------+
                                      |
                                      v
                         +--------------------------+
                         | Proceed to Service or    |
                         | Claim Submission         |
                         +--------------------------+
```

---

## 4. Authorization Transaction Flow
```
RCM System / Backend       Clearinghouse/API        Insurance Payer
        |                         |                         |
        | Build authorization     |                         |
        | request:                |                         |
        | - Trace/Correlation ID  |                         |
        | - Patient info          |                         |
        | - Member ID             |                         |
        | - Provider NPI          |                         |
        | - Diagnosis code        |                         |
        | - CPT/service code      |                         |
        | - Units requested       |                         |
        | - Place of service      |                         |
        | - Clinical documents    |                         |
        +------------------------>|                         |
        |                         | Forward request          |
        |                         +------------------------>|
        |                         |                         |
        |                         |                         | Review medical necessity
        |                         |                         | and payer rules
        |                         | Response:                |
        |                         | Approved / Denied /      |
        |                         | Pending / More Info      |
        |                         |<------------------------+
        | Authorization response  |                         |
        |<------------------------+                         |
        |                         |                         |
        | Save trace ID, status,  |                         |
        | payer ref, auth number, |                         |
        | decision reason, dates, |                         |
        | units, and appeal data  |                         |
```
* **Important:** Use EDI 278 for prior authorization request/response when payer or clearinghouse supports it. If EDI is not supported, use payer portal/API and store payer reference number.

---

## 5. Use Case Diagram
```
+-------------------+                     +-------------------------+
| Provider / Doctor |-------------------->| Order Service/Procedure |
+-------------------+                     +-------------------------+
                                                   |
+-------------------+                     +-------------------------+
| Prior Auth        |-------------------->| Check Auth Requirement  |
| Specialist        |                     +-------------------------+
+---------+---------+                                  |
          |                                +------------+------------+
          |                                |                         |
          v                                v                         v
+-------------------+              +-----------------+       +-------------------+
| Submit Auth       |              | Upload Clinical |       | Track Auth Status |
| Request           |              | Documents       |       +-------------------+
+-------------------+              +-----------------+               |
                                                                  v
+-------------------+                     +-------------------------+
| Payer / API       |-------------------->| Approve / Deny / Pend   |
+-------------------+                     +-------------------------+

+-------------------+                     +-------------------------+
| Billing Team      |-------------------->| Use Auth Number on Claim|
+-------------------+                     +-------------------------+

+-------------------+                     +-------------------------+
| Front Desk /      |-------------------->| Check Auth Before Visit |
| Scheduling Team   |                     +-------------------------+
+-------------------+

+-------------------+                     +-------------------------+
| Provider / Prior  |-------------------->| Appeal / Peer Review    |
| Auth Specialist   |                     | for Denied Auth         |
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
| Service Order Created |
+---+-------------------+
    |
    v
+-----------------------+
| Check Insurance and   |
| Payer Rule            |
+---+-------------------+
    |
    v
   /   /Auth /Req?  \     /
  \   /
   \ /
  No|Yes
    |                         
    |                         v
    |              +-----------------------+
    |              | Check Existing Valid  |
    |              | Authorization         |
    |              +---+-------------------+
    |                  |
    |                  v
    |              +-----------------------+
    |              | Create Auth Case      |
    |              | if not already found  |
    |              +---+-------------------+
    |                  |
    |                  v
    |              +-----------------------+
    |              | Attach Documents      |
    |              +---+-------------------+
    |                  |
    |                  v
    |              +-----------------------+
    |              | Submit to Payer       |
    |              +---+-------------------+
    |                  |
    |                  v
    |                 /     |                /Resp    |               /?        |               \     /
    |                \   /
    |                 \ /
    |       +----------+----------+
    |       |          |          |
    |       v          v          v
    | +----------+ +----------+ +----------------+
    | |Approved  | |Denied    | |More Info/Pend  |
    | +----+-----+ +----+-----+ +-------+--------+
    |      |            |               |
    |      v            v               v
    | +----------+ +----------+ +----------------+
    | |Validate  | |Review /  | |Request Missing |
    | |Auth No,  | |Appeal /  | |Documents       |
    | |Date, CPT,| |Peer Rev. | +-------+--------+
    | |Units     | +----+-----+         |
    | +----+-----+      |               |
    +------+------------+---------------+
           |
           v
+-----------------------+
| Update Status and     |
| Notify Teams          |
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
User     Frontend     Backend     Payer/API     Database     Provider     Audit Log     Notification
 |          |           |           |             |            |             |             |
 | Open     |           |           |             |            |             |             |
 | Auth     |           |           |             |            |             |             |
 +--------->|           |           |             |            |             |             |
 |          | GET order/patient     |             |            |             |             |
 |          +---------->|           |             |            |             |             |
 |          |           | Load data |             |            |             |             |
 |          |           +------------------------>|            |             |             |
 |          |           | Data      |             |            |             |             |
 |          |<----------+           |             |            |             |             |
 | Submit   |           |           |             |            |             |             |
 | Request  |           |           |             |            |             |             |
 +--------->| POST /authorizations  |             |            |             |             |
 |          +---------->|           |             |            |             |             |
 |          |           | Validate docs/rules     |            |             |             |
 |          |           +---------->|             |            |             |             |
 |          |           |           | Response    |            |             |             |
 |          |           |<----------+             |            |             |             |
 |          |           | Save case/status        |            |             |             |
 |          |           +------------------------>|            |             |             |
 |          |           | Record auth action      |            |             |             |
 |          |           +------------------------------------->|             |
 |          |           | Notify teams based on status         |             |
 |          |           +--------------------------------------------------->|
 |          | Response  |           |             |            |             |             |
 |          |<----------+           |             |            |             |             |
 | Display  |           |           |             |            |             |             |
 | Status   |           |           |             |            |             |             |
 |<---------+           |           |             |            |             |             |
 |          |           | If more info needed     |            |             |             |
 |          |           +------------------------------------>|             |             |
 |          |           | Notify provider         |            |             |             |
```

---

## 8. API Flow

### Request
```json
POST /api/authorizations
{
  "patientId": "PAT-00001",
  "insuranceId": "INS-00001",
  "payerId": "AETNA001",
  "providerNpi": "1234567890",
  "orderId": "ORD-00001",
  "serviceDate": "2026-05-20",
  "serviceType": "MRI",
  "cptCode": "70551",
  "diagnosisCodes": ["M54.5"],
  "priority": "standard",
  "urgency": "standard",
  "unitsRequested": 1,
  "placeOfService": "outpatient",
  "facilityId": "FAC-001",
  "traceId": "TRC-00001",
  "documents": ["clinical-note.pdf", "mri-order.pdf"]
}
```

### Response - Approved
```json
{
  "authorizationId": "AUTHCASE-00001",
  "status": "approved",
  "authorizationNumber": "AUTH123456",
  "payerReferenceNumber": "PAYER-REF-98765",
  "validFrom": "2026-05-20",
  "validTo": "2026-06-20",
  "approvedUnits": 1,
  "message": "Authorization approved"
}
```

### Response - Pending / More Information Required
```json
{
  "authorizationId": "AUTHCASE-00001",
  "status": "more_info_required",
  "payerReferenceNumber": "PAYER-REF-98765",
  "requiredItems": ["recent clinical note", "previous treatment history"],
  "message": "Payer requested additional documentation"
}
```

### Response - Denied
```json
{
  "authorizationId": "AUTHCASE-00001",
  "status": "denied",
  "payerReferenceNumber": "PAYER-REF-98765",
  "denialReason": "Medical necessity not met",
  "appealAllowed": true,
  "appealDeadline": "2026-06-05",
  "message": "Authorization denied. Appeal can be submitted before deadline."
}
```

---

## 9. Database Flow
```sql
-- Create authorization case
INSERT INTO prior_authorizations (
    authorization_id,
    patient_id,
    insurance_id,
    payer_id,
    provider_npi,
    order_id,
    service_type,
    cpt_code,
    diagnosis_codes,
    status,
    priority,
    urgency,
    units_requested,
    place_of_service,
    facility_id,
    trace_id,
    requested_by,
    requested_at,
    payer_reference_number,
    created_at,
    updated_at
) VALUES (...);

-- Save uploaded clinical documents
INSERT INTO authorization_documents (
    document_id,
    authorization_id,
    document_type,
    file_url,
    document_status,
    uploaded_by,
    uploaded_at,
    reviewed_by,
    reviewed_at
) VALUES (...);

-- Update authorization decision
UPDATE prior_authorizations
SET status = 'approved',
    authorization_number = 'AUTH123456',
    valid_from = '2026-05-20',
    valid_to = '2026-06-20',
    approved_units = 1,
    validity_checked_at = NOW(),
    decision_at = NOW(),
    updated_at = NOW()
WHERE authorization_id = 'AUTHCASE-00001';

-- Update authorization denial / appeal details
UPDATE prior_authorizations
SET status = 'denied',
    denial_reason = 'Medical necessity not met',
    appeal_allowed = true,
    appeal_deadline = '2026-06-05',
    decision_at = NOW(),
    updated_at = NOW()
WHERE authorization_id = 'AUTHCASE-00001';

-- Follow-up tracking
UPDATE prior_authorizations
SET last_follow_up_at = NOW(),
    next_follow_up_at = NOW() + INTERVAL '2 days',
    updated_at = NOW()
WHERE authorization_id = 'AUTHCASE-00001';

-- Link authorization to order/claim when needed
UPDATE orders
SET authorization_id = 'AUTHCASE-00001',
    authorization_status = 'approved'
WHERE order_id = 'ORD-00001';
```

---

## 10. Error Scenarios
```
Error 1: Authorization Not Required
   ↓
Mark as not required
   ↓
Proceed to appointment/service/claim

Error 2: Missing Clinical Documents
   ↓
Show missing document list
   ↓
Request documents from provider/clinical staff

Error 3: Payer Portal/API Down
   ↓
Retry based on policy
   ↓
Move to manual follow-up queue

Error 4: Authorization Denied
   ↓
Show denial reason
   ↓
Notify provider and auth specialist
   ↓
Appeal / peer review / reschedule service

Error 5: More Information Required
   ↓
Collect missing documents
   ↓
Resubmit to payer

Error 6: Authorization Expired
   ↓
Block claim submission warning
   ↓
Request new authorization or confirm payer rule

Error 7: Service Changed After Approval
   ↓
Check if new service/CPT needs new authorization
   ↓
Update or resubmit authorization

Error 8: Duplicate Authorization Case Found
   ↓
Show existing authorization case
   ↓
Link existing valid authorization or create new only if needed

Error 9: Authorization Approved for Wrong CPT/Service
   ↓
Block ready-for-service status
   ↓
Update or resubmit authorization request

Error 10: Approved Units Exhausted
   ↓
Warn billing/scheduling/provider
   ↓
Request additional units or new authorization

Error 11: Valid Date Does Not Cover Service Date
   ↓
Block claim/service warning
   ↓
Request corrected authorization or reschedule service

Error 12: Payer Reference Number Missing
   ↓
Hold case for manual review
   ↓
Contact payer or clearinghouse

Error 13: Document Upload Failed
   ↓
Show upload failure
   ↓
Retry upload and notify auth specialist
```

---

## 11. Dashboard & Status Flow
```
+----------------------+
| Auth Not Started     |
+----------+-----------+
           |
           v
+----------------------+
| Auth Required        |
+----------+-----------+
           |
           v
+----------------------+
| Check Existing Auth  |
+----------+-----------+
     |                 |
     v                 v
+-------------+   +----------------------+
| Duplicate / |   | Documents Pending    |
| Existing    |   +----------+-----------+
| Auth Found  |              |
+------+------+              v
       |          +----------------------+
       |          | Submitted to Payer   |
       |          +----------+-----------+
       |                     |
       |        +------------+-------------+----------------+
       |        |            |             |                |
       v        v            v             v                v
+----------+ +----------+ +------------+ +----------------+ +--------------+
| Not      | | Approved | | Denied     | | More Info Req. | | Urgent Review|
| Required | +----+-----+ +-----+------+ +--------+-------+ +------+-------+
+----------+      |             |                 |                |
                  v             v                 v                v
             +----------+ +-------------+ +----------------+ +-------------+
             | Validate | | Appeal      | | Resubmit       | | Follow-up   |
             | Dates,   | | Submitted / | | Documents      | | Task        |
             | CPT,     | | Peer Review | +----------------+ +-------------+
             | Units    | | Pending     |
             +----+-----+ +-------------+
                  |
                  v
             +----------+
             | Ready    |
             | for      |
             | Service  |
             +----+-----+
                  |
                  v
             +----------------------+
             | Auth Used on Claim   |
             +----------------------+

Other possible statuses: Expired, Cancelled, Units Exhausted.
```

---

## 12. Follow-up & Notification Flow
```
+--------------------------+
| Auth Case Created        |
+------------+-------------+
             |
             v
+--------------------------+
| Notify Auth Specialist   |
+------------+-------------+
             |
             v
+--------------------------+
| If Documents Missing     |
| Notify Provider/Clinical |
+------------+-------------+
             |
             v
+--------------------------+
| If Pending > SLA         |
| Create Follow-up Task    |
| and Escalate to          |
| Supervisor if needed     |
+------------+-------------+
             |
             v
+--------------------------+
| If Appeal Deadline Near  |
| Create Urgent Task       |
+------------+-------------+
             |
             v
+--------------------------+
| If Approved              |
| Notify Front Desk,       |
| Billing, Provider        |
+------------+-------------+
             |
             v
+--------------------------+
| If Approved but Service  |
| Date Outside Validity    |
| Notify Scheduling and    |
| Billing                  |
+------------+-------------+
             |
             v
+--------------------------+
| If Denied                |
| Notify Provider and      |
| Scheduling Team          |
+--------------------------+
```

---

**Next Module:** [Module 5: Patient Check-In](Flows_Module_05_Patient_Checkin.md)