# Healthcare RCM Application - MVP Guide (Part 2: Modules & Features)

**Version:** 1.0  
**For:** Development Team & Technical Lead

---

## 3. Modules Included in MVP

### Module 1: Appointment Scheduling

**Purpose:**  
Schedule patient appointments and link them to encounters for billing.

**What User Does:**
1. Opens calendar view
2. Selects date and time slot
3. Selects patient and provider
4. Selects appointment type (New Patient, Follow-up, etc.)
5. Adds notes if needed
6. Clicks "Schedule"

**What Backend Does:**
1. Checks provider availability
2. Checks for scheduling conflicts
3. Creates appointment record
4. Sends confirmation (optional: via Twilio SMS)
5. Creates placeholder encounter

**APIs Needed:**
- **Internal:** Appointment CRUD endpoints
- **Twilio API** (optional for SMS reminders)

**Database Tables:**
- `appointments`
- `provider_schedules`
- `appointment_types`

**Features:**
- Calendar view (day/week/month)
- Color-coded by appointment type
- Drag-and-drop rescheduling
- Automated reminders (24 hours before)

---

### Module 2: User Login & Security

**Purpose:**  
Secure access control so only authorized staff can access patient data and billing information.

**What User Does:**
1. Opens application
2. Enters username and password
3. System shows dashboard based on their role

**What Backend Does:**
1. Validates credentials against database
2. Generates JWT token (expires in 8 hours)
3. Checks user role and permissions
4. Returns allowed menu items and features

**APIs Needed:**
- **Internal:** FastAPI authentication endpoints
- **External:** None (built in-house)

**Tech Details:**
```python
# Authentication flow
POST /api/v1/auth/login
{
  "username": "biller01",
  "password": "encrypted_password"
}

Response:
{
  "access_token": "jwt_token_here",
  "token_type": "bearer",
  "user_role": "medical_biller",
  "permissions": ["view_claims", "submit_claims", "post_payments"]
}
```

**Security Features:**
- Password encryption (bcrypt)
- JWT token-based authentication
- Role-based access control (RBAC)
- Session timeout after 8 hours
- Audit logging for all actions

---

### Module 3: Patient Registration

**Purpose:**  
Capture and store patient demographic and insurance information accurately.

**What User Does:**
1. Clicks "New Patient" button
2. Fills in patient form:
   - Name, DOB, Gender, SSN
   - Address, Phone, Email
   - Emergency contact
   - Insurance information (primary & secondary)
3. Clicks "Save"

**What Backend Does:**
1. Validates all required fields
2. Checks for duplicate patients (by name + DOB)
3. Generates unique patient ID
4. Stores data in PostgreSQL database
5. Returns success message

**APIs Needed:**
- **Internal:** Patient CRUD endpoints
- **External:** None for basic registration

**Database Tables:**
- `patients` (demographics)
- `patient_insurance` (insurance details)
- `patient_contacts` (emergency contacts)

**Validation Rules:**
- SSN format: XXX-XX-XXXX
- Phone: (XXX) XXX-XXXX
- Email: valid email format
- DOB: Cannot be future date
- Insurance policy number: Required if insurance selected

---

### Module 4: Insurance Verification

**Purpose:**  
Verify patient insurance eligibility and benefits before appointment to avoid claim denials.

**What User Does:**
1. Opens patient record
2. Clicks "Verify Insurance" button
3. System shows verification results in 10-30 seconds:
   - Coverage status (Active/Inactive)
   - Copay amount
   - Deductible (met/remaining)
   - Out-of-pocket max
   - Prior authorization requirements

**What Backend Does:**
1. Extracts patient insurance data
2. Creates EDI 270 transaction (eligibility inquiry)
3. Sends to **Waystar API** or **Availity API**
4. Receives EDI 271 response (eligibility response)
5. Parses response and stores in database
6. Caches result for 24 hours

**APIs Needed:**
- **Waystar API** (preferred for multi-payer support)
- **Availity API** (alternative, free for some payers)

**API Integration Example:**
```python
# Waystar eligibility check
POST https://api.waystar.com/eligibility/v1/inquiries
Headers:
  Authorization: Bearer {api_key}
  Content-Type: application/json

Body:
{
  "patient": {
    "firstName": "John",
    "lastName": "Doe",
    "dateOfBirth": "1980-05-15",
    "memberId": "ABC123456789"
  },
  "payer": {
    "payerId": "00431",  # Aetna
    "payerName": "Aetna"
  },
  "provider": {
    "npi": "1234567890",
    "taxId": "12-3456789"
  },
  "serviceDate": "2026-05-20"
}

Response:
{
  "eligibilityStatus": "Active",
  "copay": 25.00,
  "deductible": {
    "annual": 1500.00,
    "met": 800.00,
    "remaining": 700.00
  },
  "outOfPocketMax": {
    "annual": 5000.00,
    "met": 1200.00,
    "remaining": 3800.00
  },
  "priorAuthRequired": false
}
```

**Business Rules:**
- Verify before every appointment
- Cache results for 24 hours
- If inactive → patient becomes self-pay
- Alert user if prior auth required

---

### Module 5: Prior Authorization / Referral Management

**Purpose:**  
Obtain insurance company approval before expensive procedures, specialist consultations, surgeries, diagnostic tests, or inpatient admissions.

**What User Does:**
1. Opens "Prior Authorization" module
2. Clicks "Create Authorization Request"
3. Selects patient and scheduled service/procedure
4. Enters authorization details:
   - CPT/Procedure codes
   - Diagnosis codes (ICD-10)
   - Ordering physician
   - Requested service date
   - Facility information
5. Uploads supporting clinical documents:
   - Doctor notes
   - Lab reports
   - Imaging reports
   - Referral forms
6. Selects insurance payer
7. Submits authorization request
8. Monitors authorization status:
   - Pending
   - Approved
   - Denied
   - Additional information requested
9. Tracks authorization expiry dates
10. Communicates with payer if follow-up is required

**What Backend Does:**
1. Verifies whether authorization is required for selected procedure
2. Generates unique authorization request ID
3. Stores authorization request in database
4. Sends authorization request to payer system/API

**APIs Needed:**
- **Internal:**
  - Authorization CRUD APIs
  - Referral management APIs
  - Document upload APIs
  - Notification APIs
  - Status tracking APIs

- **External:**
  - Insurance payer authorization APIs
  - Clearinghouse APIs
  - EHR/EMR integration APIs
  - Fax/secure messaging APIs (for non-digital payers)

**Database Tables:**
- `prior_authorizations` (authorization requests)
- `authorization_status_history` (status tracking)
- `authorization_documents` (uploaded files)
- `referrals` (specialist referrals)
- `payer_communications` (payer interaction logs)
- `authorization_expiry_tracking` (expiry monitoring)

**Business Rules:**
- Authorization Requirement Rules
- Referral Management Rules
- Clinical Documentation Rules
- Authorization Submission Rules
- Authorization Expiry Rules
---

### Module 6: Patient Check-In

**Purpose:**  
Confirm patient arrival, verify demographic and insurance information, collect copays, obtain consent forms, and manage patient queue flow before the medical visit.

**What User Does:**
1. Opens "Patient Check-In" module
2. Searches patient by:
   - Appointment ID
   - Patient name
   - Phone number
   - Patient ID
3. Verifies patient details:
   - Address
   - Phone number
   - Insurance information
   - Emergency contact
4. Updates any changed information
5. Reviews appointment details
6. Collects required digital consent forms:
   - HIPAA consent
   - Treatment consent
   - Financial responsibility form
7. Collects copay/payment from patient
8. Generates payment receipt
9. Marks patient as "Checked-In"
10. Updates patient queue/waiting status
11. Notifies medical staff about patient arrival

**What Backend Does:**
1. Retrieves scheduled appointment details
2. Validates appointment date and time
3. Verifies patient insurance eligibility
4. Checks outstanding balances or copay requirements
5. Stores updated demographic information
6. Saves signed digital consent forms securely
7. Processes payment transaction
8. Generates receipt and payment confirmation
9. Updates appointment status to:
   - Checked-In
   - Waiting
   - Ready for Provider
10. Updates real-time patient queue
11. Sends notifications to:
   - Nurse station
   - Provider dashboard
   - Billing department
12. Logs complete audit trail of check-in activity

**APIs Needed:**
- **Internal:**
  - Appointment management APIs
  - Patient verification APIs
  - Check-in status APIs
  - Queue management APIs
  - Consent form APIs
  - Payment processing APIs
  - Notification APIs

- **External:**
  - Insurance eligibility verification APIs
  - Payment gateway APIs (Availity / Waystar) – coverage and copay verification
  - SMS/Email notification APIs (Twilio / SendGrid) – check-in alerts & notifications
  - Digital signature APIs

**Database Tables:**
- `patient_checkins` (check-in records)
- `appointment_queue` (patient waiting queue)
- `patient_consent_forms` (signed consent forms)
- `copay_transactions` (payment records)
- `checkin_audit_logs` (activity tracking)
- `appointment_status_history` (status changes)

**Validation Rules:**
- Required consent forms must be signed before completion
- Copay amount must match payer configuration
- Payment transaction must succeed before finalizing check-in
- Duplicate check-ins for same appointment are not allowed
---

### Module 7: Clinical Documentation / EMR

**Purpose:**  
Maintain a complete and structured Electronic Medical Record (EMR) containing all clinical information such as doctor notes, diagnoses, prescriptions, lab orders, and treatment plans for each patient encounter.

---

**What User Does:**
1. Opens "EMR / Clinical Documentation" module
2. Selects patient from search or active encounter list
3. Creates or updates clinical notes:
   - Chief complaint
   - History of present illness (HPI)
   - Physical examination findings
4. Adds diagnosis information:
   - Primary diagnosis
   - Secondary diagnoses
   - ICD-10 codes
5. Prescribes medications:
   - Drug name
   - Dosage
   - Frequency
   - Duration
6. Orders lab or radiology tests:
   - Lab tests (blood work, pathology)
   - Imaging (X-ray, CT, MRI)
7. Creates treatment plan:
   - Procedures
   - Follow-up schedule
   - Care instructions
8. Saves and signs the clinical documentation

---

**What Backend Does:**
1. Retrieves patient EMR history and active encounter data
2. Creates or updates encounter record in EMR system
3. Stores structured clinical data:
   - Notes
   - Diagnoses
   - Prescriptions
   - Orders
   - Treatment plans
4. Validates medical codes:
   - ICD-10 for diagnoses
   - RxNorm / drug database for prescriptions
5. Links clinical documentation to billing/RCM module
6. Triggers downstream workflows:
   - Charge capture generation
   - Lab/radiology order processing
7. Maintains version history of all clinical updates
8. Ensures compliance with HIPAA and audit logging
9. Locks signed notes from further edits (if finalized)

---

**APIs Needed:**
- **EHR/EMR API (Epic / Cerner / FHIR APIs)** – clinical data storage & retrieval  
- **FHIR API Layer** – standardized clinical data exchange  
- **Internal Encounter API** – visit/clinical note management  

---

**Clinical Validation Rules:**
- Encounter must be active before documentation
- Diagnosis must use valid ICD-10 codes
- Prescription must be validated against drug database
- Controlled substances require additional verification
- Lab/radiology orders must match clinical indication
- Documentation must be signed before finalization
- Signed notes cannot be edited (only amended via addendum)

---

**Data Stored:**
- `encounters` (visit-level clinical records)
- `clinical_notes` (doctor documentation)
- `diagnoses` (ICD-10 coded conditions)
- `prescriptions` (medication orders)
- `lab_orders` (lab test requests)
- `radiology_orders` (imaging requests)
- `treatment_plans` (care plans & follow-ups)

---

### Module 8: Medical Coding

**Purpose:**  
Assign correct ICD-10 diagnosis codes and CPT procedure codes to encounters for accurate billing.

**What User Does:**
1. Opens encounter after patient visit
2. Reviews doctor's notes
3. Searches and selects ICD-10 codes (diagnoses)
4. Searches and selects CPT codes (procedures)
5. Adds modifiers if needed
6. Links codes to encounter
7. Clicks "Save"

**What Backend Does:**
1. Validates code formats
2. Checks code validity (active codes only)
3. Validates code combinations (some codes can't be billed together)
4. Stores codes linked to encounter
5. Calculates expected reimbursement

**APIs Needed:**
- **Internal:** ICD-10 and CPT code database
- **OpenAI API** (optional for AI-assisted coding suggestions)
- **FHIR APIs** (optional to pull codes from EHR)

**AI-Assisted Coding (Optional MVP Feature):**
```python
# AI suggests codes based on doctor's notes
POST /api/v1/ai/suggest-codes
{
  "encounter_notes": "Patient presents with acute bronchitis, productive cough for 5 days. Prescribed antibiotics.",
  "patient_age": 45,
  "patient_gender": "M"
}

Response (using OpenAI API):
{
  "suggested_icd10": [
    {"code": "J20.9", "description": "Acute bronchitis, unspecified", "confidence": 0.95},
    {"code": "R05", "description": "Cough", "confidence": 0.88}
  ],
  "suggested_cpt": [
    {"code": "99213", "description": "Office visit, established patient, moderate complexity", "confidence": 0.92}
  ]
}
```

**Database Tables:**
- `icd10_codes` (100,000+ diagnosis codes)
- `cpt_codes` (10,000+ procedure codes)
- `encounter_diagnoses`
- `encounter_procedures`

---

### Module 9: Claim Creation

**Purpose:**  
Generate clean, accurate claims from encounter data ready for submission.

**What User Does:**
1. Opens "Claims" module
2. Selects encounters ready for billing
3. Clicks "Create Claim"
4. System auto-fills claim form (CMS-1500 or UB-04)
5. Reviews claim for errors
6. Edits if needed
7. Marks claim as "Ready to Submit"

**What Backend Does:**
1. Pulls data from multiple tables:
   - Patient demographics
   - Insurance information
   - Provider information
   - Encounter details (date, place of service)
   - Diagnosis codes (ICD-10)
   - Procedure codes (CPT)
   - Charges
2. Validates claim against payer rules
3. Runs claim scrubbing (error checking)
4. Generates claim in EDI 837 format
5. Stores claim in database with status "Ready"

**APIs Needed:**
- **Internal:** Claim generation logic
- **Waystar API** (for claim scrubbing/validation)

**Claim Validation Rules:**
- All required fields present
- Valid NPI numbers
- Valid diagnosis and procedure codes
- Diagnosis supports medical necessity for procedures
- Charges match fee schedule
- No duplicate claims

**Claim Formats:**
- **CMS-1500:** Professional claims (doctor's office)
- **UB-04:** Institutional claims (hospital)
- **EDI 837P:** Electronic professional claims
- **EDI 837I:** Electronic institutional claims

---

### Module 10: Claim Scrubbing

**Purpose:**  
Perform pre-submission validation of healthcare claims to detect errors, missing data, and coding issues in order to reduce rejections and denials from payers.

---

**What User Does:**
1. Opens "Claim Scrubbing" module
2. Selects claims in draft or ready status
3. Runs "Scrub Claims" process
4. Reviews scrubbing results:
   - Errors (must fix)
   - Warnings (recommended fixes)
   - Passed claims (ready for submission)
5. Opens each flagged claim
6. Fixes issues such as:
   - Missing diagnosis or procedure codes
   - Invalid CPT/ICD-10 codes
   - Incorrect modifiers
   - Missing provider or patient details
7. Re-runs scrubbing after corrections
8. Moves clean claims to "Ready for Submission"

---

**What Backend Does:**
1. Fetches claim data from billing database
2. Applies validation rules engine:
   - Required field checks
   - Code format validation (ICD-10, CPT, NPI)
   - Medical necessity validation
3. Cross-checks:
   - Diagnosis vs procedure compatibility
   - Payer-specific rules
   - Fee schedule consistency
4. Detects:
   - Duplicate claims
   - Missing modifiers
   - Invalid or inactive codes
5. Generates scrubbing report with:
   - Error list
   - Warning list
   - Suggested fixes
6. Updates claim status:
   - `Scrubbed`
   - `Failed Scrub`
   - `Ready for Submission`
7. Stores scrubbing history for audit and analytics

---

**APIs Needed:**
- **Internal Claim Scrubbing Engine API**
- **Waystar API (Claim Validation Rules Engine)**
- **Availity API (Payer Rule Validation)**
- **Coding Reference API (ICD-10 / CPT Lookup)**
- **Fee Schedule API (Payer Contract Validation)**

---

**Validation Rules:**
- All claims must have valid ICD-10 diagnosis codes
- CPT codes must match approved procedures
- NPI numbers must be active and valid
- Required modifiers must be present where applicable
- No duplicate claims for same encounter
- Diagnosis must support medical necessity for procedures
- Charges must align with payer fee schedules
- All required demographic and insurance data must be complete

---

**Data Stored:**
- `claims` (claim master records)
- `claim_scrub_results` (validation output)
- `claim_errors` (detected issues)
- `claim_warnings` (non-critical issues)
- `scrubbing_rules_log` (applied rules history)
- `claim_correction_history` (fix tracking)

---


### Module 11: Claim Submission

**Purpose:**  
Submit claims electronically to insurance payers and track submission status.

**What User Does:**
1. Opens "Claims" module
2. Filters claims by status "Ready to Submit"
3. Selects claims (single or batch)
4. Clicks "Submit Claims"
5. System shows submission confirmation

**What Backend Does:**
1. Converts claims to EDI 837 format
2. Sends to clearinghouse via **Waystar API** or **Availity API**
3. Receives submission acknowledgment (EDI 999)
4. Updates claim status to "Submitted"
5. Stores submission tracking number

**APIs Needed:**
- **Waystar API** (primary clearinghouse)
- **Availity API** (alternative clearinghouse)

**API Integration Example:**
```python
# Submit claim via Waystar
POST https://api.waystar.com/claims/v1/submit
Headers:
  Authorization: Bearer {api_key}
  Content-Type: application/json

Body:
{
  "claims": [
    {
      "claimId": "CLM-2026-001234",
      "ediContent": "ISA*00*...",  # Full EDI 837 content
      "payerId": "00431",
      "submissionDate": "2026-05-18"
    }
  ]
}

Response:
{
  "batchId": "BATCH-20260518-001",
  "submittedClaims": 1,
  "status": "Accepted",
  "trackingNumber": "TRK-987654321"
}
```

**Submission Workflow:**
1. Claim created → Status: "Ready"
2. Claim submitted → Status: "Submitted"
3. Acknowledgment received → Status: "Accepted" or "Rejected"
4. If rejected → Fix errors and resubmit
5. If accepted → Wait for adjudication

**Tracking:**
- Submission date/time
- Batch number
- Tracking number
- Acknowledgment status
- Error messages (if rejected)

---

### Module 12: Clearinghouse Validation

**Purpose:**  
Validate, scrub, and route claims through a clearinghouse to ensure they meet payer requirements before submission to insurance companies.

---

**What User Does:**
1. Opens "Clearinghouse Validation" module
2. Selects claims in "Ready to Submit" status
3. Initiates validation process
4. Reviews validation results:
   - Accepted
   - Rejected
   - Accepted with warnings
5. Opens rejected claims for correction
6. Fixes errors such as:
   - Missing fields
   - Invalid codes
   - Demographic mismatches
7. Resubmits corrected claims for validation
8. Tracks submission acknowledgment status

---

**What Backend Does:**
1. Sends claims to clearinghouse for validation
2. Performs pre-validation checks:
   - Required field validation
   - Code format validation (ICD-10, CPT, NPI)
3. Receives clearinghouse response:
   - Accepted for payer submission
   - Rejected with error codes
4. Stores validation results and error logs
5. Routes rejected claims to correction workflow
6. Updates claim status:
   - `Validated`
   - `Rejected`
   - `Pending Correction`
7. Generates submission acknowledgment tracking ID
8. Maintains full audit history of validation attempts
9. Triggers alerts for high rejection rates

---

**APIs Needed:**
- **Waystar API** (primary clearinghouse validation)
- **Availity API** (secondary clearinghouse integration)
- **Change Healthcare API** (claims validation & routing)
- **Internal Claim Validation API** (pre-scrubbing logic)
- **EDI 837/835 Processing API** (claim format validation & responses)

---

**Validation Rules:**
- Claim must have valid ICD-10 and CPT codes
- Patient and provider information must be complete
- NPI numbers must be valid and active
- Duplicate claims are not allowed
- Payer-specific formatting rules must be satisfied
- Charges must match fee schedule rules
- All required modifiers must be present where applicable

---

**Data Stored:**
- `clearinghouse_requests` (submitted claims)
- `clearinghouse_responses` (validation results)
- `claim_validation_errors` (error details)
- `claim_correction_queue` (rework items)
- `submission_acknowledgments` (tracking receipts)
- `edi_transactions` (837/835 message logs)

---

### Module 13: Claim Status Tracking

**Purpose:**  
Track and monitor the real-time status of insurance claims throughout the payer processing lifecycle using EDI 276/277 transactions, ensuring visibility into claim progress, delays, and outcomes.

---

**What User Does:**
1. Opens "Claim Status Tracking" module
2. Searches claims using:
   - Claim ID
   - Patient name
   - Date of service
   - Payer name
3. Views current claim status:
   - Received
   - In Review
   - Pending
   - Approved
   - Denied
   - Paid
4. Requests status refresh (manual inquiry)
5. Reviews claim history timeline
6. Identifies delayed or aging claims
7. Creates follow-up tasks for denied or pending claims
8. Receives automated alerts for status changes

---

**What Backend Does:**
1. Sends real-time or scheduled EDI 276 (claim status inquiry) requests to payer systems
2. Receives EDI 277 (claim status response) updates
3. Maps payer responses to internal claim status codes
4. Updates claim lifecycle status in database
5. Maintains full claim status history with timestamps
6. Triggers alerts for:
   - No response within SLA
   - Claim stuck in same status for long duration
7. Generates aging analysis reports
8. Supports batch and real-time status updates
9. Logs all payer communication for audit purposes

---

**APIs Needed:**
- **Waystar API** (primary clearinghouse for 276/277 transactions)
- **Availity API** (secondary payer status tracking)
- **Change Healthcare API** (claims status & EDI exchange)
- **EDI Gateway API (276/277 processing engine)**
- **Internal Claim Tracking API** (status mapping & history storage)

---

**Tracking Rules:**
- Every claim must have a unique tracking ID
- Status updates must be timestamped
- Payer responses must be mapped to standardized statuses
- Claims without updates beyond SLA threshold must trigger alerts
- Denied claims must be routed to denial management workflow
- Paid claims must be updated with payment details (if available via 835)

---

**Data Stored:**
- `claim_status_tracking` (current status)
- `claim_status_history` (full timeline)
- `edi_276_requests` (status inquiries sent)
- `edi_277_responses` (payer responses)
- `claim_aging_reports` (delayed claim analysis)
- `claim_followups` (task tracking for unresolved claims)

---

**Reports Generated:**
- Aging Report (0–30, 31–60, 61–90, 90+ days)
- Pending Claims Report
- Denied Claims Report
- SLA Breach Report
- Payer Performance Report

---

### Module 14: Insurance Adjudication Tracking

**Purpose:**  
Track and analyze the insurance payer adjudication process, including claim approvals, denials, partial payments, and medical necessity decisions to ensure transparency in claim processing and reimbursement outcomes.

---

**What User Does:**
1. Opens "Adjudication Tracking" module
2. Searches claims by:
   - Claim ID
   - Patient name
   - Payer name
   - Date of service
3. Views adjudication status:
   - Approved
   - Denied
   - Partially Paid
   - Under Review
   - Pending Medical Necessity Review
4. Opens detailed adjudication breakdown:
   - Allowed amount
   - Paid amount
   - Patient responsibility
   - Denial reasons
5. Reviews contract compliance information
6. Identifies underpaid or denied claims
7. Initiates appeal workflow (if required)
8. Monitors payer response timelines and delays

---

**What Backend Does:**
1. Receives adjudication data from payer systems via EDI 835 / payer APIs
2. Parses and stores adjudication results:
   - Allowed amounts
   - Adjustments
   - Denial codes
3. Maps adjudication outcomes to internal claim records
4. Tracks medical necessity review decisions
5. Validates claim payments against contract fee schedules
6. Detects underpayments and discrepancies
7. Updates claim financial status:
   - Fully Paid
   - Partially Paid
   - Denied
8. Maintains adjudication history and audit logs
9. Triggers alerts for:
   - Denials
   - Underpayments
   - High-value claim rejections
10. Generates payer performance and turnaround analytics

---

**APIs Needed:**
- **Waystar API** (primary adjudication & EDI 835 processing)
- **Availity API** (payer response & adjudication data)
- **Change Healthcare API** (claims payment & adjudication feed)
- **EDI 835 Processing API** (remittance & adjudication details)
- **Contract Management API** (fee schedule validation)

---

**Tracking Rules:**
- Every claim must have linked adjudication record
- All payer responses must be stored in normalized format
- Denial codes (CARC/RARC) must be recorded
- Payment must match allowed amount unless adjustment is applied
- Medical necessity denials must be flagged separately
- Contract variance must be calculated for every claim
- Partial payments must be broken into components:
  - Allowed amount
  - Paid amount
  - Patient responsibility

---

**Data Stored:**
- `adjudication_records` (payer decisions)
- `payment_details` (835 remittance data)
- `denial_codes` (CARC/RARC mapping)
- `contract_variance_logs` (expected vs actual payments)
- `medical_necessity_reviews` (clinical justification tracking)
- `payer_processing_metrics` (timelines and performance data)

---

**Reports Generated:**
- Adjudication Summary Report
- Denial Reason Analysis Report
- Underpayment Detection Report
- Payer Turnaround Time Report
- Contract Variance Report
- Medical Necessity Denial Report

---

### Module 15: ERA Processing

**Purpose:**  
Process Electronic Remittance Advice (ERA) files (EDI 835) received from insurance payers to reconcile payments, extract denials, and automate posting of financial transactions.

---

**What User Does:**
1. Opens "ERA Processing" module
2. Uploads or imports ERA files (EDI 835)
3. Selects payer or batch for processing
4. Initiates ERA processing workflow
5. Reviews processed results:
   - Payments posted
   - Denials extracted
   - Adjustments applied
6. Validates reconciliation reports
7. Manually corrects unmatched payments (if needed)
8. Confirms auto-posting to accounts receivable

---

**What Backend Does:**
1. Receives ERA (EDI 835) file from payer or clearinghouse
2. Parses 835 transaction segments:
   - Payment details
   - Claim adjustments
   - Denial codes (CARC/RARC)
3. Matches ERA data with existing claims
4. Performs payment reconciliation:
   - Claim level matching
   - Line item level matching
5. Posts payments automatically to patient accounts (if auto-post enabled)
6. Updates claim status:
   - Paid
   - Partially Paid
   - Denied
7. Extracts and categorizes denial reasons
8. Applies contractual adjustments based on payer rules
9. Flags unmatched or missing claims for review
10. Generates audit trail for all financial postings

---

**APIs Needed:**
- **Waystar API** (ERA/EDI 835 ingestion & processing)
- **Availity API** (ERA file exchange)
- **Change Healthcare API** (remittance data processing)
- **EDI 835 Parsing Engine API**
- **Accounting/AR System API** (payment posting & reconciliation)
- **Internal Claim Matching API** (claim-to-payment reconciliation logic)

---

**Processing Rules:**
- Each ERA must be linked to a valid payer and claim batch
- Payments must be matched using:
  - Claim number
  - Patient ID
  - Service date
- Denial codes (CARC/RARC) must be extracted and stored
- Contractual adjustments must be applied automatically
- Overpayments must be flagged for refund workflow
- Unmatched payments must go to exception queue
- Duplicate ERA files must be detected and ignored

---

**Data Stored:**
- `era_files` (raw EDI 835 files)
- `era_transactions` (parsed payment data)
- `payment_postings` (posted transactions)
- `denial_records` (CARC/RARC codes)
- `adjustment_records` (contractual write-offs)
- `unmatched_payments` (exception handling queue)
- `reconciliation_logs` (processing history)

---

**Reports Generated:**
- ERA Processing Summary Report
- Payment Reconciliation Report
- Denial Summary Report
- Unmatched Payments Report
- Adjustment Analysis Report
- AR Posting Audit Report

---

### Module 16: Payment Posting

**Purpose:**  
Record payments from insurance companies and patients, and reconcile with claims.

**What User Does:**
1. Opens "Payment Posting" module
2. Uploads ERA file (EDI 835) or enters manual payment
3. System auto-matches payments to claims
4. Reviews matches
5. Posts payments
6. Handles adjustments and denials

**What Backend Does:**
1. Parses ERA file (EDI 835)
2. Extracts payment information:
   - Claim number
   - Paid amount
   - Adjustment codes
   - Patient responsibility
3. Matches payments to claims automatically
4. Updates claim status:
   - Fully paid
   - Partially paid
   - Denied
5. Calculates patient balance
6. Updates accounts receivable

**APIs Needed:**
- **Waystar API** (to download ERA files)
- **Stripe API** (for patient credit card payments)

**ERA Processing Example:**
```python
# ERA (EDI 835) structure
Claim: CLM-2026-001234
Billed Amount: $150.00
Allowed Amount: $120.00
Paid Amount: $96.00
Patient Responsibility: $24.00 (copay)
Adjustment Codes:
  - CO-45: Charge exceeds fee schedule ($30.00)
  - PR-1: Deductible ($0.00)
  - PR-2: Coinsurance ($0.00)
  - PR-3: Copay ($24.00)
```

**Payment Types:**
- Insurance payments (from ERA)
- Patient payments (cash, check, credit card)
- Adjustments (contractual, write-offs)

**Database Updates:**
- `claim_payments` table
- `patient_ledger` table
- `accounts_receivable` table

---


### Module 17: Denial Dashboard

**Purpose:**  
Track denied claims and manage denial workflow to recover lost revenue.

**What User Does:**
1. Opens "Denials" dashboard
2. Sees list of denied claims with:
   - Claim number
   - Patient name
   - Denial reason
   - Denial date
   - Amount
   - Days since denial
3. Clicks on claim to see details
4. Takes action:
   - Correct and resubmit
   - Appeal denial
   - Write off (if not recoverable)

**What Backend Does:**
1. Receives denial information from ERA (EDI 835)
2. Parses denial reason codes
3. Categorizes denials:
   - Eligibility issues
   - Coding errors
   - Missing information
   - Timely filing
   - Medical necessity
4. Calculates denial rate and trends
5. Sends alerts for high-priority denials

**APIs Needed:**
- **Internal:** Denial tracking logic
- **Waystar API** (to receive ERA files)

**Denial Reason Codes (Common):**
- CO-16: Claim lacks information
- CO-18: Duplicate claim
- CO-22: Payment adjusted (coordination of benefits)
- CO-27: Expenses incurred after coverage terminated
- CO-50: Non-covered service
- CO-97: Payment adjusted (timely filing)

**Dashboard Metrics:**
- Total denied claims
- Total denied amount
- Denial rate (% of submitted claims)
- Top denial reasons
- Average days to resolve denial

---

### Module 18: Secondary Insurance Billing

**Purpose:**  
Handle Coordination of Benefits (COB) by billing secondary and tertiary insurance payers for remaining patient balances after primary insurance has processed the claim.

---

**What User Does:**
1. Opens "Secondary Insurance Billing" module
2. Selects claims with primary insurance payment posted
3. Reviews remaining patient balance after primary adjudication
4. Confirms eligibility for secondary billing
5. Generates secondary claim automatically or manually
6. Submits claim to secondary payer
7. Tracks submission and response status:
   - Submitted
   - Accepted
   - Rejected
   - Paid
8. Reviews secondary ERA results
9. Reconciles final patient responsibility
10. Closes claim after full settlement

---

**What Backend Does:**
1. Retrieves primary insurance adjudication data (ERA/835)
2. Calculates remaining balance after primary payment
3. Applies Coordination of Benefits (COB) rules
4. Determines secondary/tertiary payer hierarchy
5. Auto-generates secondary claim:
   - Adjusted charges
   - Primary payer payment details included
6. Submits secondary claim via clearinghouse
7. Tracks claim status using EDI 276/277 or payer APIs
8. Processes secondary ERA (EDI 835) responses
9. Updates claim financial lifecycle:
   - Primary Paid
   - Secondary Submitted
   - Fully Paid / Partially Paid
10. Handles rejection corrections and resubmissions
11. Maintains audit trail for multi-payer transactions

---

**APIs Needed:**
- **Waystar API** (COB processing & secondary claim submission)
- **Availity API** (secondary payer claim routing)
- **Change Healthcare API** (multi-payer claim handling)
- **EDI 837/835 Processing API** (claim submission & payment reconciliation)
- **Eligibility & COB Verification API** (payer hierarchy validation)
- **Internal Claim Management API** (secondary claim generation)

---

**COB Processing Rules:**
- Primary insurance must be fully processed before secondary billing
- COB rules must define payer priority order
- Secondary claims must include primary payer EOB/ERA details
- Patient responsibility is recalculated after each payer response
- Duplicate secondary submissions are not allowed
- Tertiary billing is triggered only after secondary adjudication
- All payer payments must reconcile to total allowed amount

---

**Data Stored:**
- `cob_records` (coordination of benefits data)
- `secondary_claims` (secondary/tertiary submissions)
- `primary_payment_details` (initial adjudication data)
- `secondary_era_responses` (payer remittance)
- `balance_transfers` (remaining AR movement)
- `multi_payer_history` (full billing lifecycle)

---

**Reports Generated:**
- COB Summary Report
- Secondary Billing Performance Report
- Multi-Payer Reconciliation Report
- Outstanding Secondary Balance Report
- Denial Analysis for Secondary Claims

---

### Module 19: Patient Billing

**Purpose:**  
Generate patient statements and manage collection of remaining balances after insurance payments, including payment plans and digital payment options.

---

**What User Does:**
1. Opens "Patient Billing" module
2. Searches patient account or encounter
3. Views outstanding patient balance
4. Generates patient statement:
   - Single statement
   - Batch statement run
5. Sends statement via:
   - Email
   - SMS
   - Physical mail (print option)
6. Configures payment options:
   - Full payment
   - Installment plan
7. Monitors payment status:
   - Paid
   - Partial
   - Overdue
8. Reviews payment history and receipts
9. Follows up on overdue accounts

---

**What Backend Does:**
1. Aggregates patient financial data:
   - Insurance payments
   - Adjustments
   - Remaining balances
2. Generates itemized patient statements
3. Applies billing rules:
   - Copay calculation
   - Deductible balance
   - Coinsurance
4. Creates payment links for online portal
5. Tracks payment plan schedules and due dates
6. Sends automated reminders:
   - SMS
   - Email
   - In-app notifications
7. Updates patient ledger in real time after payments
8. Flags overdue accounts for AR follow-up
9. Maintains billing history and audit logs

---

**APIs Needed:**
- **Internal Billing/AR API** (patient account & statement generation)
- **Payment Gateway API (Stripe / PayPal / Razorpay)** – online payments
- **SMS API (Twilio / MSG91)** – payment reminders
- **Email API (SendGrid / Amazon SES)** – statement delivery
- **Payment Plan Management API** – installment tracking
- **Document Generation API (PDF service)** – statement creation

---

**Billing Rules:**
- Patient balance is calculated after all insurance adjustments
- Statements must include:
  - Date of service
  - Procedure details
  - Insurance payments
  - Patient responsibility
- Payment plans require:
  - Minimum down payment
  - Fixed installment schedule
- Overdue accounts must trigger reminders automatically
- Partial payments must update remaining balance immediately
- Refunds must be processed through AR system

---

**Data Stored:**
- `patient_statements` (billing statements)
- `patient_balances` (outstanding amounts)
- `payment_plans` (installment agreements)
- `patient_payments` (transactions)
- `billing_notifications` (SMS/email logs)
- `patient_ledger` (financial history)

---

**Reports Generated:**
- Patient Billing Summary Report
- Outstanding Balance Report
- Payment Plan Performance Report
- Overdue Accounts Report
- Revenue Collection Report

---

### Module 20: Accounts Receivable (AR) Follow-Up

**Purpose:**  
Track and manage unpaid insurance and patient balances by prioritizing collections, managing follow-up workflows, and identifying bad debt for write-off decisions.

---

**What User Does:**
1. Opens "AR Follow-Up" module
2. Views AR aging dashboard:
   - 0–30 days
   - 31–60 days
   - 61–90 days
   - 90+ days
3. Filters accounts by:
   - Payer
   - Patient
   - Balance amount
   - Aging category
4. Assigns follow-up tasks to AR staff
5. Reviews collection work queues
6. Contacts payers/patients for payment status
7. Logs follow-up actions:
   - Calls
   - Emails
   - Appeals
8. Identifies accounts for write-off or escalation
9. Updates account status after resolution

---

**What Backend Does:**
1. Calculates AR aging based on invoice/claim due dates
2. Segregates accounts into aging buckets
3. Generates prioritized work queues using rules:
   - High-value claims first
   - Older accounts prioritized
   - High denial probability flagged
4. Assigns follow-up tasks automatically or manually
5. Tracks all follow-up activities:
   - Communication logs
   - Response status
6. Updates account status after payments or adjustments
7. Identifies potential bad debt accounts
8. Supports write-off processing workflows
9. Maintains audit trail of AR actions

---

**APIs Needed:**
- **Internal AR Management API** (account tracking & aging logic)
- **Billing/Claims API** (balance and claim data)
- **Payment Posting API** (real-time updates)
- **Notification API (Twilio / SendGrid)** – follow-up reminders
- **CRM/Task Management API** (work queue assignment)
- **Analytics/Reporting API** (aging and collection insights)

---

**AR Rules:**
- All unpaid balances must be categorized by aging bucket
- Older balances must be prioritized for follow-up
- High-value claims require immediate escalation
- Accounts with no response after defined period move to bad debt review
- Write-offs require supervisor approval
- Payment or adjustment updates must immediately reflect in AR ledger
- Duplicate follow-up tasks are not allowed

---

**Data Stored:**
- `ar_accounts` (open receivables)
- `ar_aging_summary` (bucketed balances)
- `followup_tasks` (assigned activities)
- `collection_logs` (communication history)
- `bad_debt_records` (unrecoverable accounts)
- `writeoff_transactions` (approved adjustments)

---

**Reports Generated:**
- AR Aging Report
- Collection Performance Report
- Follow-Up Productivity Report
- Bad Debt Analysis Report
- Write-Off Summary Report

---

### Module 21: Collections / Refund / Write-Off Management

**Purpose:**  
Manage overdue collections, process patient refunds, handle credit balances, and execute approved write-offs for uncollectible or adjusted accounts.

---

**What User Does:**
1. Opens "Collections / Refunds" module
2. Views accounts categorized as:
   - Overdue collections
   - Credit balances
   - Refund eligible accounts
   - Write-off candidates
3. Initiates collection workflow:
   - Assigns internal collector
   - Sends patient/payer reminders
4. Processes refunds:
   - Selects eligible credit balance
   - Initiates refund request
   - Chooses refund method (bank transfer, card reversal, check)
5. Reviews and approves write-off requests
6. Sends accounts to external collection agencies (if needed)
7. Tracks recovery status of collections
8. Monitors refund and write-off history

---

**What Backend Does:**
1. Identifies overdue accounts from AR system
2. Segregates financial statuses:
   - Active receivables
   - Credit balances
   - Refund eligible accounts
   - Bad debt candidates
3. Automates collection workflow assignment
4. Processes refund transactions securely:
   - Validates credit balance availability
   - Initiates payment reversal or payout
5. Applies write-off rules:
   - Small balance thresholds
   - Aging-based write-offs
   - Supervisor approval enforcement
6. Integrates with external collection agencies
7. Updates patient and insurance ledgers in real time
8. Maintains full audit logs of financial adjustments
9. Tracks recovery performance from collections

---

**APIs Needed:**
- **Internal AR Management API** (balance tracking & updates)
- **Payment Gateway API (Stripe / PayPal / Razorpay)** – refunds & reversals
- **Banking/EFT API** – direct deposit refunds
- **Collection Agency API (third-party integrations)** – external recovery workflows
- **Notification API (Twilio / SendGrid)** – reminders & alerts
- **Accounting/ERP API** – financial reconciliation

---

**Financial Rules:**
- Refunds can only be processed for validated credit balances
- Write-offs require defined approval hierarchy
- Small balance write-offs must follow configured threshold rules
- Collection accounts must follow escalation workflow:
  - Internal follow-up → Supervisor → External agency
- All financial adjustments must be auditable
- Duplicate refunds are strictly prevented
- External collection accounts must be marked as “Transferred”

---

**Data Stored:**
- `collection_accounts` (overdue receivables)
- `refund_requests` (refund transactions)
- `credit_balances` (patient/payer credits)
- `writeoff_records` (approved adjustments)
- `collection_agency_assignments` (external tracking)
- `financial_adjustments_log` (audit trail)

---

**Reports Generated:**
- Collection Performance Report
- Refund Summary Report
- Write-Off Analysis Report
- Credit Balance Report
- Recovery Rate Report

---

### Module 22: Basic Reports

**Purpose:**  
Provide essential financial and operational reports for practice management.

**What User Does:**
1. Opens "Reports" module
2. Selects report type
3. Selects date range
4. Clicks "Generate Report"
5. Views report on screen
6. Exports to PDF or Excel if needed

**What Backend Does:**
1. Queries database based on report parameters
2. Aggregates data
3. Calculates metrics
4. Formats report
5. Returns report data

**APIs Needed:**
- **Internal:** Reporting queries

**MVP Reports:**

1. **Daily Charges Report**
   - Total charges posted today
   - By provider
   - By service type

2. **Claims Status Report**
   - Claims submitted
   - Claims paid
   - Claims denied
   - Claims pending

3. **Payment Summary Report**
   - Total payments received
   - By payer
   - By payment type

4. **Aging Report (A/R)**
   - Outstanding balances by age:
     - 0-30 days
     - 31-60 days
     - 61-90 days
     - 90+ days

5. **Denial Report**
   - Denial rate
   - Top denial reasons
   - Denied amount

6. **Provider Productivity Report**
   - Encounters per provider
   - Charges per provider
   - Collections per provider

**Report Features:**
- Date range filters
- Export to PDF/Excel
- Email scheduling (optional)
- Dashboard widgets for key metrics

---

### Module 23: Compliance & Audit

**Purpose:**  
Ensure system-wide regulatory compliance (HIPAA and healthcare standards) by tracking all user activities, maintaining audit logs, monitoring access, and generating compliance reports across the RCM system.

---

**What User Does:**
1. Opens "Compliance & Audit" module
2. Views audit dashboards:
   - User activity logs
   - System access logs
   - Data modification history
3. Filters logs by:
   - User
   - Date range
   - Module (Billing, Claims, EMR, etc.)
4. Reviews security alerts:
   - Unauthorized access attempts
   - Suspicious activity
   - Failed login attempts
5. Generates compliance reports:
   - HIPAA audit reports
   - User activity summaries
6. Investigates flagged events
7. Exports audit logs for regulatory review

---

**What Backend Does:**
1. Captures every system action in real-time audit logs
2. Tracks:
   - User login/logout events
   - Data create/read/update/delete (CRUD)
   - Financial transactions
   - PHI (Protected Health Information) access
3. Monitors abnormal behavior patterns:
   - Repeated failed logins
   - Unauthorized data access attempts
   - Bulk data exports
4. Generates immutable audit trails (append-only logs)
5. Encrypts and secures all sensitive logs
6. Triggers security alerts for:
   - Role violations
   - Suspicious IP/device activity
7. Maintains compliance mapping:
   - HIPAA requirements
   - Internal security policies
8. Supports long-term log retention policies
9. Provides reporting for internal and external audits

---

**APIs Needed:**
- **Internal Audit Logging API** (system-wide event tracking)
- **Security Monitoring API** (SIEM tools like Splunk / Datadog)
- **Identity & Access Management API** (Okta / Keycloak)
- **Notification API** (Twilio / SendGrid / Email/SMS alerts)
- **Encryption/KMS API** (AWS KMS / Azure Key Vault)

---

**Compliance Rules:**
- All PHI access must be logged
- Logs must be immutable (no deletion allowed)
- Every user action must be traceable to a unique user ID
- Failed login attempts must trigger security alerts
- Sensitive data exports must be monitored and logged
- Role-based access control (RBAC) must be enforced
- Audit logs must be retained as per regulatory policy (e.g., 6–10 years)
- Any unauthorized access attempt must trigger immediate alerting

---

**Data Stored:**
- `audit_logs` (system activity records)
- `access_logs` (login/session tracking)
- `security_events` (alerts and incidents)
- `user_activity_history` (detailed user actions)
- `compliance_reports` (generated audit reports)
- `data_access_tracking` (PHI access records)

---

**Reports Generated:**
- HIPAA Compliance Report
- User Activity Report
- Security Incident Report
- Access Violation Report
- System Audit Summary Report

---

**Next:** Part 3 will cover the complete MVP workflow and recommended tech stack.

---

**Document Navigation:**
- **Part 1:** Introduction & Goals
- **Part 2:** Modules & Features (This document)
- **Part 3:** Workflow & Tech Stack
- **Part 4:** APIs & AI Integration
- **Part 5:** Development Plan & Timeline
