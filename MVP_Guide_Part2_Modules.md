# Healthcare RCM Application - MVP Guide (Part 2: Modules & Features)

**Version:** 1.0  
**For:** Development Team & Technical Lead

---

## 3. Modules Included in MVP

### Module 1: User Login & Security

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

### Module 2: Patient Registration

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

### Module 3: Insurance Verification

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

### Module 4: Appointment Scheduling

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

### Module 5: Medical Coding

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

### Module 6: Claim Creation

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

### Module 7: Claim Submission

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

### Module 8: Denial Dashboard

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

### Module 9: Payment Posting

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

### Module 10: Basic Reports

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

**Next:** Part 3 will cover the complete MVP workflow and recommended tech stack.

---

**Document Navigation:**
- **Part 1:** Introduction & Goals
- **Part 2:** Modules & Features (This document)
- **Part 3:** Workflow & Tech Stack
- **Part 4:** APIs & AI Integration
- **Part 5:** Development Plan & Timeline
