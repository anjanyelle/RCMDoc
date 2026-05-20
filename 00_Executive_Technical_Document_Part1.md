# Healthcare RCM Application - Executive Technical Document

**Project Name:** Healthcare Revenue Cycle Management (RCM) Platform  
**Version:** 1.0  
**Prepared For:** Technical Lead & Development Team  
**Document Type:** Complete Project Blueprint  

---

## Table of Contents
- [Project Overview](#1-project-overview)
- [Complete Application Flow](#2-complete-application-flow)
- [System Architecture](#3-system-architecture)
- [Recommended Technology Stack](#4-recommended-technology-stack)
- [Third-Party APIs & Integrations](#5-third-party-apis--integrations)
- [AI Features & Implementation](#6-ai-features--implementation)
- [Development Plan](#7-development-plan)
- [Recommended Team Structure](#8-recommended-team-structure)
- [Challenges & Risks](#9-challenges--risks)
- [Final Project Execution Strategy](#10-final-project-execution-strategy)

---

## 1. Project Overview

### 1.1 What is This Project?
We are building a comprehensive Healthcare Revenue Cycle Management (RCM) platform that automates the complete financial workflow of hospitals and clinics—from patient registration to final payment collection.

**In Simple Terms:**  
When a patient visits a hospital, the hospital must:
- Register the patient
- Verify their insurance coverage
- Provide medical treatment
- Document the treatment
- Convert treatment into billing codes
- Create and submit insurance claims
- Track claim status and handle denials
- Collect payments from insurance and patients
- Generate financial reports

Our application automates all these steps, reducing manual work, preventing billing errors, and accelerating payment collection.

### 1.2 Why Hospitals Need This
**Current Problems Hospitals Face:**

| Problem | Impact | Our Solution |
| :--- | :--- | :--- |
| Manual claim creation | Slow, error-prone (10-15% denial rate) | Automated claim generation with validation |
| Insurance verification delays | Patients arrive with inactive insurance | Real-time eligibility checks via API |
| Coding errors | Claims denied, revenue lost | AI-assisted medical coding |
| Slow payment collection | 50-60 days to collect payment | Automated workflows reduce to <40 days |
| Revenue leakage | 5-10% of revenue lost to errors | Charge capture automation prevents loss |
| Compliance risks | HIPAA violations, audit failures | Built-in audit logging and compliance |
| Missed authorization | 100% claim denial | Automated auth check & tracking |
| Missed charge capture | Lost revenue | Orders-to-charges reconciliation |
| Wrong patient balance | Patient complaints, lost trust | Accurate ERA posting & calculation |
| Duplicate patient | Split records, billing errors | Duplicate detection on registration |
| Payer downtime | Submission delays | Queue system & offline retry |

**Financial Impact:**
- Hospital with $50M annual revenue loses $2.5M-$5M to inefficiencies
- Our system can recover $1.5M-$3M annually
- ROI: System pays for itself in 6-12 months

### 1.3 Main Business Goals
- Reduce Claim Denial Rate: From 10-15% to <5%
- Accelerate Payment Collection: From 50-60 days to <40 days in AR
- Increase Clean Claim Rate: From 75-80% to >95%
- Eliminate Revenue Leakage: From 5-10% to <2%
- Ensure HIPAA Compliance: 100% audit-ready with complete logging
- Improve Patient Experience: Transparent billing, easy payment options

### 1.4 End Users

| User Role | Count (Medium Hospital) | Primary Responsibilities |
| :--- | :--- | :--- |
| Front Desk Staff | 10-20 | Patient registration, scheduling, insurance verification |
| Clinical Staff | 50-100 | Order entry, clinical documentation |
| Medical Coders | 5-15 | Assign ICD-10/CPT codes to encounters |
| Billing Specialists | 10-20 | Create, scrub, and submit claims |
| AR Managers | 5-10 | Payment posting, denial management, follow-up |
| Collections Staff | 3-8 | Patient billing, payment plans, collections |
| Providers (Doctors) | 20-100 | Clinical documentation, encounter review |
| Finance Managers | 2-5 | Reporting, analytics, strategic decisions |
| Compliance Officers | 1-3 | Audits, HIPAA compliance monitoring |
| System Administrators | 1-2 | User management, system configuration |

**Total Users per Hospital:** 100-300 concurrent users

---

## 2. Complete Application Flow

### 2.1 End-to-End Workflow Overview

Appointment Scheduling / Walk-In → Pre-Registration → Patient Registration → Insurance Eligibility Verification → Prior Authorization / Referral Management → Patient Check-In → Doctor Consultation / Encounter → Clinical Documentation / EMR → Orders & Ancillary Services → Treatment / Procedure → Medical Coding → Charge Capture → Claim Creation → Claim Scrubbing → Claim Submission (EDI 837) → Clearinghouse Validation (999/277CA) → Insurance Adjudication → Claim Status Tracking (EDI 276/277) → ERA / EOB Processing (EDI 835) → Payment Posting → Denial Management / Appeals → Secondary Insurance Billing (COB) → Patient Billing → Collections / AR Follow-Up → Refunds / Write-Offs → Reporting & Analytics → Compliance & Audit → Backup & Recovery

**Key Process Highlights:**
- **Prior Authorization:** Must be obtained before service when required to prevent automatic denials.
- **Claim Scrubbing:** Validates claims against payer rules, coding edits, and missing information before submission.
- **Clearinghouse Validation:** Claims are validated through 999 and 277CA acknowledgment workflows immediately after submission.
- **Insurance Adjudication:** Insurance payers review claims for coverage, coding accuracy, medical necessity, and contract compliance.
- **ERA / Payment Posting:** Automated ERA/EOB matching and payment posting occur after insurance adjudication completes.
- **Denial Management:** Denied claims are corrected, appealed, and resubmitted through denial workflows.
- **Secondary Insurance Billing:** Remaining balances are automatically forwarded to secondary payers when applicable.
- **Patient Billing:** Patient statements are generated only after insurance processing and payment posting complete.
- **AR Follow-Up:** Outstanding balances and unpaid claims are tracked through Accounts Receivable workflows.
- **Reporting & Analytics:** Financial, operational, denial, and KPI reports provide enterprise revenue visibility.
- **Compliance & Audit:** HIPAA audit logging, security monitoring, and compliance reporting ensure regulatory compliance.

### 2.2 Detailed Module Flow

#### CATEGORY 1 — PRE-RCM / FOUNDATIONAL FLOW

##### Module 1: Provider Credentialing (Pre-requisite)
**What Happens:**  
Before any billing can occur, every doctor must be registered and approved by insurance companies.

**Process:**
- Hospital submits doctor's credentials (NPI, license, certifications) to CAQH
- Insurance companies verify credentials
- Doctor gets approved and assigned a provider ID
- System tracks credential expiration dates

**Data Flow:**
- **Input:** Doctor NPI, license, specialty, education
- **Output:** Credentialing status, expiration dates
- **Integration:** CAQH ProView API, NPI Registry API

**Why Critical:**  
If doctor is not credentialed, ALL claims from that doctor are automatically rejected.

---

##### Module 2: Provider Management
**What Happens:**  
Hospital adds and manages provider information such as specialties, departments, licenses, and contact details inside the system.

**Process:**
- Hospital creates provider profile
- Provider specialty and department are assigned
- License and NPI details are added
- Provider documents are uploaded
- Provider record becomes available for credentialing and billing workflows

**Data Flow:**
- **Input:** Provider name, specialty, department, NPI, license details
- **Output:** Provider profile and provider master record
- **Integration:** Workday API, SAP ERP API, Active Directory API

**Why Critical:**  
Accurate provider information is required for credentialing, scheduling, claim submission, and insurance billing.

---

##### Module 3: Provider Enrollment
**What Happens:**  
Hospital enrolls providers with insurance companies so they can submit insurance claims and receive payments.

**Process:**
- Hospital submits provider enrollment request to insurance payer
- Insurance company reviews provider details
- Enrollment approval or rejection is received
- Effective dates and payer mappings are updated
- Provider becomes eligible for insurance billing

**Data Flow:**
- **Input:** Provider details, payer information, enrollment documents
- **Output:** Enrollment status, payer approval, effective dates
- **Integration:** Availity API, Waystar API, PECOS API

**Why Critical:**  
If a provider is not enrolled with insurance companies, claims cannot be submitted or reimbursed.

---

##### Module 4: Contract Management
**What Happens:**  
Hospital manages insurance payer contracts, reimbursement rates, and fee schedules for medical services.

**Process:**
- Hospital creates payer contract records
- Reimbursement rules and fee schedules are configured
- Contract effective and renewal dates are tracked
- Underpayment and contract compliance are monitored
- Contract updates are applied to billing workflows

**Data Flow:**
- **Input:** Payer contracts, reimbursement rates, fee schedules
- **Output:** Active contract rules, payment configurations, reimbursement tracking
- **Integration:** DocuSign API, SAP ERP API, Contract Management Systems

**Why Critical:**  
Incorrect contract setup can lead to underpayments, claim disputes, and revenue loss.

---

##### Provider Becomes Billable
**What Happens:**  
After credentialing, provider enrollment, and contract approvals are completed, the provider becomes eligible for insurance billing.

**Process:**
- Provider credentials are approved
- Insurance enrollment becomes active
- Payer contracts are activated
- Provider status changes to "Billable"
- Provider can now submit insurance claims

**Result:**  
Provider Status = Billable

**Why Critical:**  
Only billable providers can generate valid insurance claims and receive reimbursements from insurance companies.

#### CATEGORY 2 — PATIENT ACCESS MANAGEMENT

##### Module 5: Appointment Scheduling
**What Happens:**  
Patients schedule appointments with providers.

**Process:**
- Staff or patient selects provider and date/time
- System checks provider availability
- Appointment created and linked to patient
- Automated reminders sent via SMS/email (7 days, 1 day, 2 hours before)
- Patient can confirm, reschedule, or cancel

**Data Flow:**
- **Input:** Patient, provider, date/time, appointment type
- **Output:** Confirmed appointment, reminder notifications
- **Integration:** Twilio (SMS), SendGrid (Email), Zoom (telehealth)
- **Database Tables:** `appointments`

**Business Rules:**
- No double-booking same provider/time
- Track no-shows (block after 3 no-shows)
- Waitlist management for full slots

---

##### Module 6: Patient Registration
**What Happens:**  
Front desk staff registers new patients or updates existing patient information.

**Process:**
- Staff searches for existing patient (prevent duplicates)
- If new, system generates unique Medical Record Number (MRN)
- Collect demographics: Name, DOB, address, phone, email
- Collect insurance information: Primary, secondary, tertiary
- Scan insurance cards (front and back)
- Capture digital consent forms

**Data Flow:**
- **Input:** Patient demographics, insurance card images
- **Output:** Patient record with MRN, insurance details
- **Database Tables:** `patients`, `patient_insurance`

**Business Rules:**
- Duplicate detection: Check name + DOB before creating new record
- SSN must be encrypted (AES-256) before storage
- Insurance card images stored in S3 with encryption

**Common Mistakes:**
- Wrong insurance ID → Claim denial
- Misspelled name → Payment posting errors
- Missing secondary insurance → Lost revenue

---

##### Module 7: Insurance Verification
**What Happens:**  
System checks in real-time whether patient's insurance is active and what they owe.

**Process:**
- Staff clicks "Verify Insurance" button
- System sends EDI 270 transaction to payer via Waystar/Availity
- Payer responds with EDI 271 containing:
  - Coverage status (Active/Inactive)
  - Copay amount
  - Deductible (annual amount, amount met, remaining)
  - Out-of-pocket maximum
  - Network status (in-network/out-of-network)
  - Prior authorization requirements

**Data Flow:**
- **Input:** Patient demographics, insurance policy number, service date
- **Output:** Eligibility response with financial responsibility
- **Integration:** Waystar API, Availity API, or direct payer APIs
- **Cache:** Results cached in Redis for 15 minutes

**Business Rules:**
- Verify before every appointment
- If inactive, patient becomes self-pay
- Collect copay at check-in

**Revenue Impact:**  
Prevents treating patients with inactive insurance (saves $50K-$200K/year in bad debt)

---

##### Module 8: Prior Authorization
**What Happens:**  
For expensive procedures, hospital must get insurance approval before treatment.

**Process:**
- Doctor orders procedure (e.g., MRI, surgery)
- System checks if authorization required (based on CPT code + payer rules)
- If required, staff submits authorization request with:
  - Diagnosis codes (ICD-10)
  - Procedure codes (CPT)
  - Clinical justification
  - Medical necessity documentation
- Insurance reviews and approves/denies
- If approved, authorization number is issued
- System tracks authorization validity dates and units used

**Data Flow:**
- **Input:** Diagnosis, procedure, clinical notes
- **Output:** Authorization number, approved units, expiration date
- **Integration:** Availity, Change Healthcare, Cohere Health
- **Database Tables:** `authorizations`

**Business Rules:**
- Service performed without required authorization = 100% claim denial
- Track units used (e.g., 8 of 10 physical therapy visits used)
- Alert 7 days before expiration

---

##### Module 9: Patient Check-In
**What Happens:**  
Front desk staff checks in the patient when they arrive for the appointment and creates an encounter record for the visit.

**Process:**
- Patient arrives at hospital or clinic
- Staff verifies patient demographics and insurance information
- Copay or outstanding balance collected
- Patient signs consent forms
- System creates encounter/visit record
- Patient assigned to provider or exam room
- Doctor notified that patient is ready

**Data Flow:**
- **Input:** Appointment details, patient information, insurance details
- **Output:** Encounter record, updated visit status, payment details
- **Database Tables:** `encounters`, `patient_checkin`, `payments`

**Business Rules:**
- Insurance must be verified before check-in
- Copay collected before provider visit
- One encounter created per visit
- Check-in time tracked for audit and reporting

**Common Mistakes:**
- Incorrect insurance verification → Claim denial
- Missing copay collection → Revenue loss
- Wrong provider assignment → Billing errors
- Duplicate encounter creation → Duplicate claims

#### CATEGORY 3 — CLINICAL & MID-CYCLE MANAGEMENT

##### Module 10: Clinical Documentation / EMR
**What Happens:**  
Doctor examines patient and documents visit in EMR.

**Process:**
- Doctor reviews patient history
- Examines patient and documents findings
- Records diagnoses (what's wrong with patient)
- Records procedures performed (what doctor did)
- Orders tests (labs, imaging, medications)
- Creates treatment plan
- Signs encounter (locks documentation)

**Data Flow:**
- **Input:** Clinical observations, test results
- **Output:** SOAP notes, diagnoses, procedures, orders
- **Integration:** Epic, Cerner, or other EMR via HL7/FHIR
- **Database Tables:** `encounter_diagnoses`, `encounter_procedures`, `orders`

**SOAP Note Structure:**
- **Subjective:** Patient's complaints
- **Objective:** Doctor's observations, vital signs
- **Assessment:** Diagnoses
- **Plan:** Treatment plan

**Why Critical:**  
Insurance only pays for documented services. Poor documentation = claim denial.

---

##### Module 11: Order Management
**What Happens:**  
Doctor's orders (labs, imaging, meds) are tracked and executed.

**Process:**
- Doctor places order in EMR
- Order sent to appropriate department (lab, radiology, pharmacy)
- Department performs service
- Results returned to EMR
- Charge automatically captured when order completed

**Data Flow:**
- **Input:** Order details (CPT code, quantity, instructions)
- **Output:** Order status, results, automatic charges
- **Integration:** Lab systems (HL7 ORM/ORU), PACS (radiology), pharmacy systems
- **Integration Engine:** Mirth Connect (free, open-source HL7 engine)

**Automatic Charge Capture:**
- Lab order completed → Lab CPT code charged
- X-ray completed → Radiology CPT code charged
- Medication dispensed → HCPCS J-code charged

**Revenue Impact:**  
Prevents missed charges (5-10% of revenue typically lost to missed charges)

---

##### Module 12: Medical Coding
**What Happens:**  
Medical coders review clinical documentation and assign standardized codes.

**Process:**
- Coder opens encounter from coding worklist
- Reviews doctor's SOAP notes
- Assigns diagnosis codes (ICD-10):
  - E11.9 = Type 2 Diabetes
  - I10 = Essential Hypertension
- Assigns procedure codes (CPT):
  - 99214 = Office visit, level 4
  - 80053 = Comprehensive metabolic panel (lab)
- Links diagnoses to procedures (medical necessity)
- Assigns modifiers if needed (e.g., modifier 25 for separate E&M)
- For inpatient: Assigns DRG code
- Marks encounter as "Coded - Ready to Bill"

**Data Flow:**
- **Input:** Clinical documentation
- **Output:** ICD-10 codes, CPT codes, DRG codes
- **Integration:** 3M CodeFinder, Optum CAC (optional AI assistance)
- **Database Tables:** `encounter_diagnoses`, `encounter_procedures`

**Code Types:**
- **ICD-10:** Diagnosis codes (70,000+ codes)
- **CPT:** Procedure codes (10,000+ codes)
- **HCPCS:** Additional services (drugs, supplies, DME)
- **DRG:** Inpatient payment groups (Medicare)
- **Modifiers:** 2-digit codes that modify CPT meaning

**Business Rules:**
- Principal diagnosis must be listed first (inpatient)
- Diagnosis must support medical necessity for procedure
- Maximum 12 diagnosis codes per claim (CMS-1500)
- Maximum 18 diagnosis codes per claim (UB-04)

**Common Mistakes:**
- Vague diagnosis (e.g., "diabetes" instead of "E11.9")
- Missing laterality (left vs right)
- Incorrect E&M level selection
- Unbundling (billing components instead of comprehensive code)

---

##### Module 13: Charge Entry / Charge Capture
**What Happens:**  
Every medical service, procedure, medication, or supply used during the patient visit is converted into a billable charge for insurance and patient billing.

**Process:**
- Services performed during patient encounter
- System captures charges automatically from completed orders
- Doctor-documented procedures added manually
- Medications and supplies linked to charges
- Each charge mapped with CPT/HCPCS codes
- Charge amounts pulled from chargemaster
- Charges prepared for claim generation

**Data Flow:**
- **Input:** Completed orders, procedures, medications, supplies
- **Output:** Charge line items ready for billing and claim creation
- **Database Tables:** `charges`, `chargemaster`

**Business Rules:**
- Charges must be entered within service timeline
- Charges validated against documentation
- Missing charges flagged for review
- Duplicate charges prevented

**Common Mistakes:**
- Missing procedure charges → Revenue loss
- Incorrect CPT code mapping → Claim denial
- Duplicate charge entry → Overbilling issues
- Incomplete documentation → Billing hold

---

##### Module 14: Coding Compliance
**What Happens:**  
System validates codes against compliance rules before billing.

**Process:**
- System checks NCCI edits (National Correct Coding Initiative)
  - Prevents billing incompatible code combinations
  - Example: Cannot bill CPT 99213 and 99214 together
- Checks LCD/NCD rules (Coverage Determinations)
  - Verifies diagnosis supports procedure per Medicare rules
  - Example: Diagnosis E11.9 supports HbA1c test
- Checks MUE limits (Medically Unlikely Edits)
  - Prevents billing excessive units
  - Example: Maximum 2 units of CPT 99213 per day
- Flags potential upcoding/downcoding
- Alerts coder to fix errors before claim creation

**Data Flow:**
- **Input:** Coded encounter
- **Output:** Validation results, error alerts
- **Data Sources:** CMS NCCI edits (updated quarterly), LCD/NCD databases

**Why Critical:**  
Prevents fraud, reduces denials, avoids audits and penalties.

#### CATEGORY 4 — CLAIMS MANAGEMENT

##### Module 15: Claim Scrubbing
**What Happens:**  
System validates claim against 200+ rules before submission.

**Process:**
- System runs automated validation checks:
  - **Demographic Checks:** Patient name, DOB, address complete?
  - **Insurance Checks:** Valid policy number? Coverage active on service date?
  - **Provider Checks:** Valid NPI? Provider credentialed with payer?
  - **Coding Checks:** Valid ICD-10/CPT codes? NCCI edits passed?
  - **Authorization Checks:** Authorization number present if required?
  - **Financial Checks:** Charge amount >$0? Units >0?
  - **Date Checks:** Service date not in future? Within timely filing limit?
  - **Duplicate Checks:** Not duplicate of previously submitted claim?
- Errors categorized:
  - **Fatal (Red):** Claim cannot be submitted, must fix
  - **Warning (Yellow):** Claim can submit but may deny
  - **Info (Blue):** Informational only
- Clean claims marked with green checkmark
- Error claims returned to biller for correction

**Data Flow:**
- **Input:** Draft claim
- **Output:** Scrubbing results, clean claim indicator
- **Database Tables:** `claim_scrubbing_errors`

**Goal:** 95%+ clean claim rate

---

##### Module 16: Claim Submission
**What Happens:**  
Clean claims submitted electronically to insurance companies.

**Process:**
- Biller selects clean claims for submission
- System converts claims to EDI 837 format:
  - **EDI 837P:** Professional claims
  - **EDI 837I:** Institutional claims
- Claims batched (e.g., 100 claims per batch)
- Batch transmitted to clearinghouse via SFTP or API
- Clearinghouse validates and forwards to payers
- System receives acknowledgments:
  - **EDI 999:** File received confirmation
  - **EDI 277:** Claim accepted/rejected by payer
- Claim status updated to "Submitted" or "Rejected"

**Data Flow:**
- **Input:** Clean claims
- **Output:** EDI 837 file, submission confirmation
- **Integration:** Waystar, Availity, Change Healthcare (clearinghouse)

**Submission Frequency:** Every 2 hours (configurable)

**Timely Filing:**  
Most payers require claims within 90-365 days of service. System alerts before deadline.

---

##### Module 17: Clearinghouse Validation
**What Happens:**  
After claim submission, the clearinghouse validates insurance claims for formatting errors, missing information, and payer requirements before sending claims to insurance companies.

**Process:**
- Claim received from billing system
- Clearinghouse validates EDI 837 claim format
- Syntax and payer rule checks performed
- Missing or invalid data identified
- Accepted claims forwarded to insurance payer
- Rejected claims returned for correction
- Acknowledgment responses generated (999/277CA)

**Data Flow:**
- **Input:** EDI 837 insurance claims
- **Output:** Accepted claims, rejected claims, validation responses
- **Database Tables:** `clearinghouse_responses`, `claim_validation_logs`

**Business Rules:**
- Claims must pass validation before payer submission
- Invalid claims moved to rejection queue
- Required payer fields cannot be empty
- Duplicate claim submissions prevented

**Common Mistakes:**
- Invalid insurance ID → Claim rejection
- Missing provider NPI → Submission failure
- Incorrect EDI format → Clearinghouse rejection
- Missing authorization number → Claim denial

**Integrations:** Waystar API, Availity API, Change Healthcare API, EDI 999 / 277CA Transactions

---

##### Module 18: Claim Status Tracking
**What Happens:**  
System monitors claim status after submission.

**Process:**
- Claims tracked in real-time via:
  - EDI 276/277 status inquiries
  - Payer portal checks
  - Clearinghouse status updates
- Status categories:
  - **Submitted:** Sent to payer
  - **Accepted:** Payer received claim
  - **Pending:** Under payer review
  - **Paid:** Payment received
  - **Denied:** Claim rejected
  - **Rejected:** Claim bounced back (technical error)
- Aging buckets:
  - 0-30 days
  - 31-60 days
  - 61-90 days
  - 90+ days (high priority follow-up)
- Automated follow-up for claims pending >30 days

**Data Flow:**
- **Input:** Submitted claims
- **Output:** Claim status updates, aging reports
- **Integration:** Waystar, Availity APIs

**Worklists:**
- Claims pending >60 days
- Claims approaching timely filing deadline
- Claims with payer requests for additional information

---

##### Module 19: Insurance Adjudication Tracking
**What Happens:**  
This module tracks how insurance companies review, approve, deny, or partially pay submitted claims based on coverage rules, medical necessity, and payer contracts.

**Process:**
- Insurance payer receives submitted claim
- Payer reviews patient coverage and eligibility
- Diagnosis and procedure codes validated
- Medical necessity checks performed
- Payer contract rules applied
- Claim approved, denied, or partially paid
- Adjudication decision returned to billing system
- Claim status updated for payment or denial workflows

**Data Flow:**
- **Input:** Submitted insurance claims, payer rules, patient coverage details
- **Output:** Claim approval status, denial details, payment decisions
- **Database Tables:** `adjudication_status`, `payer_responses`, `claim_status_history`

**Business Rules:**
- Claims must meet payer medical necessity requirements
- Invalid or non-covered services may be denied
- Contract reimbursement rules applied during adjudication
- Authorization-required services validated before payment

**Common Mistakes:**
- Missing authorization → Claim denial
- Non-covered procedure → Partial payment
- Incorrect coding → Adjudication rejection
- Invalid insurance coverage → Claim denial

**Integration:** Waystar API, Availity API, Change Healthcare API, EDI 276/277 Transactions

**Why Critical:**  
Insurance adjudication directly impacts claim payments, denial rates, reimbursement accuracy, and hospital revenue collection.

#### CATEGORY 5 — PAYMENT & REVENUE MANAGEMENT

##### Module 20: ERA Processing
**What Happens:**  
This module processes Electronic Remittance Advice (EDI 835) files received from insurance companies after claim adjudication.

**Process:**
- Insurance company sends ERA (EDI 835) file
- System imports and reads ERA payment data
- Claim payment details extracted
- Adjustment and denial codes identified
- Paid, allowed, deductible, and copay amounts processed
- Payment information prepared for posting
- Claim payment status updated

**Data Flow:**
- **Input:** EDI 835 ERA files, insurance payment data
- **Output:** Processed payment details, adjustment records, payment posting data
- **Database Tables:** `era_files`, `era_payments`, `payment_adjustments`

**Business Rules:**
- ERA files must match submitted claims
- Duplicate ERA processing prevented
- Invalid payment records moved for manual review
- Adjustment codes validated before posting

**Common Mistakes:**
- Unmatched claim numbers → Posting failure
- Incorrect adjustment codes → Balance mismatch
- Duplicate ERA file upload → Duplicate payments
- Missing payer information → Processing errors

**Integration:** EDI 835 Transactions, Waystar API, Availity API, Change Healthcare API

**Why Critical:**  
ERA processing automates insurance payment handling, improves payment accuracy, and reduces manual payment posting effort.

---

##### Module 21: Payment Posting
**What Happens:**  
When insurance pays, payment details are posted to patient accounts.

**Process:**
- Insurance sends payment via:
  - **EFT:** Electronic funds transfer to hospital bank account
  - **ERA:** Electronic Remittance Advice (EDI 835) with payment details
- System imports ERA file
- ERA parser extracts payment data:
  - Check number and date
  - Total payment amount
  - Claim-level details:
    - Claim number
    - Billed amount
    - Allowed amount
    - Paid amount
    - Deductible applied
    - Copay applied
    - Coinsurance applied
    - Adjustment codes (CARC/RARC)
- Auto-posting engine matches ERA to claims:
  - If unique match found → Auto-post
  - If multiple matches or no match → Manual review queue
- Payment posted to patient account
- Claim status updated to "Paid" or "Partially Paid"
- Patient balance calculated

**Data Flow:**
- **Input:** EDI 835 (ERA) file
- **Output:** Posted payments, updated account balances
- **Database Tables:** `payments`, `payment_line_items`, `era_files`

**Adjustment Reason Codes (CARC):**
- **CO-45:** Contractual adjustment (write-off)
- **PR-1:** Deductible amount
- **PR-2:** Coinsurance amount
- **PR-3:** Copay amount
- **CO-16:** Claim lacks information
- **CO-97:** Service not covered

**Auto-Posting Rate:** Target 80-90% of payments auto-posted

---

##### Module 22: Denial Management
**What Happens:**  
Denied claims are reviewed, corrected, and appealed.

**Process:**
- Denied claim identified from ERA
- Denial reason captured (CARC code)
- Denial categorized:
  - **Clinical:** Medical necessity not supported
  - **Technical:** Missing/incorrect information
  - **Authorization:** No prior authorization
  - **Eligibility:** Coverage inactive
  - **Timely Filing:** Claim submitted too late
- Denial assigned to specialist based on category
- Specialist reviews and determines action:
  - **Correct and resubmit:** Fix error, submit corrected claim
  - **Appeal:** Submit appeal letter with supporting documentation
  - **Write-off:** Accept denial if not appealable
- Appeals tracked through multiple levels:
  - Level 1: Reconsideration
  - Level 2: Internal review
  - Level 3: External independent review
- Appeal outcomes recorded

**Data Flow:**
- **Input:** Denied claims with reason codes
- **Output:** Corrected claims, appeal letters, outcomes
- **Database Tables:** `denials`, `appeals`

**Common Denial Reasons:**
- Missing authorization (30%)
- Incorrect coding (25%)
- Eligibility issues (20%)
- Timely filing (10%)
- Duplicate claim (5%)
- Other (10%)

**Appeal Success Rate:** Target 60-70% overturn rate

**Revenue Impact:**  
Recovering $500K-$2M annually in denied claims

---

##### Module 23: Secondary Insurance Billing/Tertiary Billing
**What Happens:**  
After primary insurance pays, remaining balance billed to secondary insurance.

**Process:**
- Primary insurance payment posted
- System checks if patient has secondary insurance
- If yes, automatically generates secondary claim with:
  - All original claim data
  - Primary payer name and payment amount
  - Remaining patient responsibility
- Submit to secondary payer
- Secondary payment posted
- If tertiary insurance exists, repeat process
- Final patient balance calculated after all insurance pays

**Data Flow:**
- **Input:** Primary payment details, secondary insurance info
- **Output:** Secondary claim, final patient balance

**Coordination of Benefits (COB):**
- Birthday rule: For dependent children, parent with earlier birthday is primary
- Medicare Secondary Payer (MSP): When patient has Medicare + other coverage
- Crossover claims: Medicare auto-forwards to Medicaid/Medigap

---

##### Module 24: Patient Billing
**What Happens:**  
Patient receives bill for their portion after insurance pays.

**Process:**
- All insurance payments completed
- System generates patient statement showing:
  - Service date and description
  - Total charges
  - Insurance payments (by payer)
  - Adjustments
  - Patient responsibility (deductible + copay + coinsurance)
  - Previous balance
  - Current balance due
  - Payment due date
- Statement delivered via:
  - Paper mail
  - Email (PDF)
  - Patient portal
- Patient payment options:
  - Online payment (credit card, ACH)
  - Payment plan (installments)
  - Phone payment
  - Mail check
  - In-person payment

**Data Flow:**
- **Input:** Final account balance after insurance
- **Output:** Patient statement, payment confirmation
- **Integration:** Stripe (payment processing), Cedar (patient billing platform)
- **Database Tables:** `patient_statements`, `patient_payments`

**Point-of-Service Collections:**  
Collect copay/deductible at check-in (before visit) = 3x higher collection rate

---

##### Module 25: Accounts Receivable (AR) Follow-Up
**What Happens:**  
This module tracks unpaid insurance and patient balances and manages follow-up activities to improve payment collection and reduce outstanding receivables.

**Process:**
- System identifies unpaid or partially paid claims
- Claims grouped by aging categories (30, 60, 90+ days)
- AR staff reviews pending balances
- Follow-up actions performed with insurance companies or patients
- Denied or delayed claims escalated for resolution
- Payment promises and follow-up notes recorded
- Account status updated after follow-up activity

**Data Flow:**
- **Input:** Unpaid claims, patient balances, insurance payment status
- **Output:** AR follow-up records, collection status, updated account balances
- **Database Tables:** `accounts_receivable`, `ar_followup`, `followup_notes`

**Business Rules:**
- High-value accounts prioritized first
- Claims approaching timely filing limits flagged
- Follow-up activities logged for audit tracking
- Outstanding balances monitored continuously

**Common Mistakes:**
- Missed follow-up deadlines → Revenue loss
- Incorrect payer communication → Payment delays
- Unresolved denied claims → Increased AR aging
- Missing follow-up documentation → Audit issues

**Integration:** Waystar API, Availity API, EDI 276/277 Transactions, Collection Systems

**Why Critical:**  
AR Follow-Up helps hospitals recover outstanding payments faster, reduce aging balances, and improve overall cash flow and revenue collection.

---

##### Module 26: Collections
**What Happens:**  
Unpaid patient balances moved through collection process.

**Process:**
- **Statement 1 (Day 0):** Friendly reminder
- **Statement 2 (Day 30):** Payment due notice
- **Statement 3 (Day 60):** Urgent notice
- **Statement 4 (Day 90):** Final notice before collections
- **Internal Collections (Day 90-120):**
  - Collection calls by hospital staff
  - Payment plan negotiations
- **External Collections (Day 120+):**
  - Account transferred to collection agency
  - Agency keeps 25-40% of collected amount
- **Bad Debt Write-Off (Day 180+):**
  - Uncollectable accounts written off
  - Reported to credit bureaus

**Data Flow:**
- **Input:** Unpaid patient balances
- **Output:** Collection notices, payment arrangements, write-offs
- **Database Tables:** `collections`, `payment_plans`

**Compliance:**
- Screen for charity care eligibility before collections
- Follow No Surprises Act regulations
- Comply with Fair Debt Collection Practices Act

#### CATEGORY 6 — REPORTING, COMPLIANCE & GOVERNANCE

##### Module 27: Reporting & Analytics
**What Happens:**  
Management monitors RCM performance through dashboards and reports.

**Key Performance Indicators (KPIs):**

| KPI | Target | Current Industry Avg |
| :--- | :--- | :--- |
| Clean Claim Rate | >95% | 75-80% |
| Denial Rate | <5% | 10-15% |
| Days in AR | <40 days | 50-60 days |
| Net Collection Rate | >95% | 85-90% |
| AR >90 Days | <15% | 25-30% |
| Cost to Collect | <$0.05 per $1 | $0.08-$0.12 |
| Revenue Leakage | <2% | 5-10% |

**Standard Reports:**
- Daily revenue report
- Weekly clean claim rate
- Monthly revenue by department/provider/payer
- AR aging report
- Denial reason analysis
- Coding productivity
- Payer performance scorecard

**Data Flow:**
- **Input:** All transactional data from modules
- **Output:** Dashboards, scheduled reports, ad-hoc queries
- **Integration:** Tableau, Power BI, Looker (optional)
- **Database:** Data warehouse for historical analysis

---

##### Module 28: Compliance & Audit
**What Happens:**  
System maintains complete audit trail for HIPAA compliance and fraud prevention.

**Audit Logging:**
- Every user login/logout
- Every patient record access
- Every data modification (before/after values)
- Every claim submission
- Every payment posting
- Every write-off

**Compliance Monitoring:**
- Upcoding detection (billing higher level than documented)
- Unbundling detection (billing components vs comprehensive code)
- Duplicate claim detection
- Overpayment identification (must refund within 60 days)
- HIPAA access violations (accessing family/friend records)

**Data Flow:**
- **Input:** All system activities
- **Output:** Audit logs, compliance alerts, audit reports
- **Database Tables:** `audit_logs`
- **Retention:** 7 years (HIPAA requirement)

**External Audits:**
- RAC (Recovery Audit Contractors): Medicare overpayment audits
- MAC (Medicare Administrative Contractors): Claims processing audits
- OIG (Office of Inspector General): Fraud investigations
- State Medicaid audits

---

### 2.3 Patient Data Flow Summary

Patient walk-in/Appointment Scheduling → Patient Registration → Insurance Verification → Prior Authorization → Patient Check-In / Encounter Creation → Clinical Documentation / EMR → Order Management → Medical Coding → Charge Entry / Charge Capture → Coding Compliance → Claim Scrubbing → Claim Submission → Clearinghouse Validation → Claim Status Tracking → Insurance Adjudication Tracking → ERA Processing → Payment Posting → Denial Management → Secondary / Tertiary Insurance Billing → Patient Billing → Accounts Receivable (AR) Follow-Up → Collections → Reporting & Analytics → Compliance & Audit

**Key Integration Points:**
- **Patient Access ↔ Insurance Payers:** EDI 270/271 transactions, Availity API, Waystar API for insurance eligibility and authorization verification
- **EMR ↔ RCM:** HL7 / FHIR integrations for clinical documentation, encounters, orders, and diagnoses
- **RCM ↔ Coding Systems:** ICD-10, CPT, HCPCS coding systems, 3M CodeFinder, Optum CAC integrations
- **RCM ↔ Clearinghouse:** EDI 837, 999, 277CA transactions for claim submission and clearinghouse validation
- **RCM ↔ Insurance Payers:** EDI 276/277 transactions and payer APIs for claim status tracking and adjudication
- **RCM ↔ Payment Systems:** EDI 835 ERA processing, EFT banking integrations, Stripe API for patient payments
- **RCM ↔ Notification Services:** Twilio API, SendGrid API for appointment reminders, billing alerts, and notifications
- **RCM ↔ Document Management:** AWS S3 storage, OCR integrations, AWS Textract for insurance card and document scanning
- **RCM ↔ Reporting & Analytics:** Power BI, Tableau, Looker integrations for dashboards and financial reporting
- **RCM ↔ Security & Compliance:** HIPAA audit logging, SIEM monitoring, access control, and compliance tracking systems

---

*[Continue to Part 2 for System Architecture, Technology Stack, and Implementation Plan]*
