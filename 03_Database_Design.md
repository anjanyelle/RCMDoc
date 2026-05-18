# Healthcare RCM Application - Database Design Document

**Version:** 1.0  
**Date:** May 18, 2026  
**For:** Development Team

---

## 1. Database Overview

**Database Type:** Relational Database (PostgreSQL recommended)  
**Why Relational:** Healthcare data is highly structured with complex relationships

**Total Tables:** 35 core tables  
**Estimated Records (Medium Hospital):**
- Patients: 100,000+
- Encounters: 500,000+ per year
- Claims: 500,000+ per year
- Payments: 1,000,000+ per year

---

## 2. Core Database Tables

### Table 1: users
**Purpose:** Store all system users (staff, providers, admins)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| user_id | UUID | PRIMARY KEY | Unique user identifier |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Login username |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| email | VARCHAR(100) | UNIQUE, NOT NULL | Email address |
| first_name | VARCHAR(50) | NOT NULL | First name |
| last_name | VARCHAR(50) | NOT NULL | Last name |
| role_id | UUID | FOREIGN KEY → roles | User role |
| is_active | BOOLEAN | DEFAULT TRUE | Account status |
| last_login | TIMESTAMP | | Last login time |
| mfa_enabled | BOOLEAN | DEFAULT FALSE | Multi-factor auth enabled |
| mfa_secret | VARCHAR(100) | | MFA secret key |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation date |
| updated_at | TIMESTAMP | | Last update date |

**Indexes:** username, email, role_id

---

### Table 2: roles
**Purpose:** Define user roles and permissions

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| role_id | UUID | PRIMARY KEY | Unique role identifier |
| role_name | VARCHAR(50) | UNIQUE, NOT NULL | Role name (e.g., "Front Desk") |
| description | TEXT | | Role description |
| permissions | JSONB | | Permissions object |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Sample Roles:**
- System Administrator
- Front Desk Staff
- Clinical Staff
- Medical Coder
- Billing Specialist
- AR Manager
- Collections Staff
- Finance Manager
- Compliance Officer
- Provider (Doctor)

**Permissions Structure (JSONB):**
```json
{
  "patients": {"create": true, "read": true, "update": true, "delete": false},
  "encounters": {"create": true, "read": true, "update": true, "delete": false},
  "claims": {"create": true, "read": true, "update": true, "delete": false},
  "payments": {"create": true, "read": true, "update": false, "delete": false},
  "reports": {"create": false, "read": true, "update": false, "delete": false}
}
```

---

### Table 3: providers
**Purpose:** Store doctor/provider information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| provider_id | UUID | PRIMARY KEY | Unique provider identifier |
| npi_type1 | VARCHAR(10) | UNIQUE, NOT NULL | Individual NPI number |
| first_name | VARCHAR(50) | NOT NULL | First name |
| last_name | VARCHAR(50) | NOT NULL | Last name |
| middle_name | VARCHAR(50) | | Middle name |
| suffix | VARCHAR(10) | | Suffix (MD, DO, etc.) |
| dob | DATE | | Date of birth |
| ssn_encrypted | VARCHAR(255) | | Encrypted SSN |
| license_number | VARCHAR(50) | | Medical license number |
| license_state | VARCHAR(2) | | License state |
| dea_number | VARCHAR(20) | | DEA number |
| taxonomy_code | VARCHAR(20) | | Provider taxonomy code |
| specialty_primary | VARCHAR(100) | | Primary specialty |
| specialty_secondary | VARCHAR(100) | | Secondary specialty |
| email | VARCHAR(100) | | Email |
| phone | VARCHAR(20) | | Phone |
| signature_image | TEXT | | Digital signature (base64) |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | | |

**Indexes:** npi_type1, last_name

---

### Table 4: provider_credentials
**Purpose:** Track provider credentialing with each payer

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| credential_id | UUID | PRIMARY KEY | |
| provider_id | UUID | FOREIGN KEY → providers | Provider |
| payer_id | UUID | FOREIGN KEY → payers | Insurance payer |
| status | VARCHAR(20) | NOT NULL | Pending, Approved, Denied, Expired |
| application_date | DATE | | Application submitted date |
| effective_date | DATE | | Credential effective date |
| expiration_date | DATE | | Credential expiration date |
| credential_number | VARCHAR(50) | | Payer-assigned credential number |
| notes | TEXT | | Notes |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | | |

**Indexes:** provider_id, payer_id, expiration_date

---

### Table 5: payers
**Purpose:** Store insurance companies/payers

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| payer_id | UUID | PRIMARY KEY | |
| payer_name | VARCHAR(100) | NOT NULL | Payer name (e.g., "Blue Cross Blue Shield") |
| payer_code | VARCHAR(20) | UNIQUE | Internal payer code |
| payer_id_external | VARCHAR(50) | | External payer ID (for clearinghouse) |
| payer_type | VARCHAR(20) | | Commercial, Medicare, Medicaid, Other |
| address_line1 | VARCHAR(100) | | Address |
| address_line2 | VARCHAR(100) | | |
| city | VARCHAR(50) | | |
| state | VARCHAR(2) | | |
| zip_code | VARCHAR(10) | | |
| phone | VARCHAR(20) | | |
| claims_address | VARCHAR(200) | | Claims mailing address |
| electronic_payer_id | VARCHAR(20) | | Electronic payer ID for EDI |
| timely_filing_days | INTEGER | | Timely filing limit (days) |
| is_active | BOOLEAN | DEFAULT TRUE | |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:** payer_name, payer_code

---

### Table 6: payer_contracts
**Purpose:** Store contracted rates with each payer

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| contract_id | UUID | PRIMARY KEY | |
| payer_id | UUID | FOREIGN KEY → payers | |
| contract_name | VARCHAR(100) | | Contract name |
| effective_date | DATE | NOT NULL | Contract start date |
| end_date | DATE | | Contract end date |
| payment_methodology | VARCHAR(50) | | Fee Schedule, % of Charges, DRG, Capitation |
| percentage_of_charges | DECIMAL(5,2) | | If % of charges (e.g., 80.00) |
| contract_terms | TEXT | | Contract terms |
| is_active | BOOLEAN | DEFAULT TRUE | |
| created_at | TIMESTAMP | DEFAULT NOW() | |

---

### Table 7: payer_contract_rates
**Purpose:** Store allowed amounts by CPT code for each contract

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| rate_id | UUID | PRIMARY KEY | |
| contract_id | UUID | FOREIGN KEY → payer_contracts | |
| cpt_code | VARCHAR(10) | NOT NULL | CPT/HCPCS code |
| modifier | VARCHAR(10) | | Modifier (if applicable) |
| allowed_amount | DECIMAL(10,2) | NOT NULL | Contracted allowed amount |
| effective_date | DATE | | Rate effective date |
| end_date | DATE | | Rate end date |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:** contract_id, cpt_code

---

### Table 8: chargemaster (CDM)
**Purpose:** Hospital fee schedule - all services with standard prices

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| cdm_id | UUID | PRIMARY KEY | |
| charge_code | VARCHAR(20) | UNIQUE, NOT NULL | Internal charge code |
| cpt_code | VARCHAR(10) | | CPT/HCPCS code |
| description | VARCHAR(255) | NOT NULL | Service description |
| department | VARCHAR(50) | | Department |
| revenue_code | VARCHAR(4) | | Revenue code (for UB-04) |
| standard_charge | DECIMAL(10,2) | NOT NULL | Standard charge amount |
| effective_date | DATE | NOT NULL | Effective date |
| end_date | DATE | | End date |
| is_active | BOOLEAN | DEFAULT TRUE | |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:** charge_code, cpt_code, department

---

### Table 9: patients
**Purpose:** Store patient demographics

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| patient_id | UUID | PRIMARY KEY | |
| mrn | VARCHAR(20) | UNIQUE, NOT NULL | Medical Record Number |
| first_name | VARCHAR(50) | NOT NULL | |
| last_name | VARCHAR(50) | NOT NULL | |
| middle_name | VARCHAR(50) | | |
| suffix | VARCHAR(10) | | |
| dob | DATE | NOT NULL | Date of birth |
| gender | VARCHAR(10) | NOT NULL | Male, Female, Other |
| ssn_encrypted | VARCHAR(255) | | Encrypted SSN |
| address_line1 | VARCHAR(100) | | |
| address_line2 | VARCHAR(100) | | |
| city | VARCHAR(50) | | |
| state | VARCHAR(2) | | |
| zip_code | VARCHAR(10) | | |
| phone_home | VARCHAR(20) | | |
| phone_mobile | VARCHAR(20) | | |
| phone_work | VARCHAR(20) | | |
| email | VARCHAR(100) | | |
| preferred_language | VARCHAR(20) | | |
| race | VARCHAR(50) | | |
| ethnicity | VARCHAR(50) | | |
| emergency_contact_name | VARCHAR(100) | | |
| emergency_contact_phone | VARCHAR(20) | | |
| emergency_contact_relationship | VARCHAR(50) | | |
| is_active | BOOLEAN | DEFAULT TRUE | |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | | |

**Indexes:** mrn, last_name, dob, ssn_encrypted

---

### Table 10: patient_insurance
**Purpose:** Store patient insurance information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| insurance_id | UUID | PRIMARY KEY | |
| patient_id | UUID | FOREIGN KEY → patients | |
| payer_id | UUID | FOREIGN KEY → payers | |
| priority | INTEGER | NOT NULL | 1=Primary, 2=Secondary, 3=Tertiary |
| policy_number | VARCHAR(50) | NOT NULL | Policy/Member ID |
| group_number | VARCHAR(50) | | Group number |
| subscriber_name | VARCHAR(100) | | Subscriber name |
| subscriber_dob | DATE | | Subscriber DOB |
| subscriber_relationship | VARCHAR(20) | | Self, Spouse, Child, Other |
| effective_date | DATE | | Coverage effective date |
| termination_date | DATE | | Coverage termination date |
| copay | DECIMAL(10,2) | | Copay amount |
| deductible_annual | DECIMAL(10,2) | | Annual deductible |
| deductible_met | DECIMAL(10,2) | | Deductible met YTD |
| oop_max_annual | DECIMAL(10,2) | | Out-of-pocket maximum |
| oop_met | DECIMAL(10,2) | | OOP met YTD |
| card_front_image | TEXT | | Insurance card front (base64) |
| card_back_image | TEXT | | Insurance card back (base64) |
| is_active | BOOLEAN | DEFAULT TRUE | |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | | |

**Indexes:** patient_id, payer_id, priority

---

### Table 11: eligibility_checks
**Purpose:** Store insurance eligibility verification history

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| check_id | UUID | PRIMARY KEY | |
| patient_id | UUID | FOREIGN KEY → patients | |
| insurance_id | UUID | FOREIGN KEY → patient_insurance | |
| check_date | TIMESTAMP | NOT NULL | Verification date/time |
| service_date | DATE | | Date of service being verified |
| coverage_status | VARCHAR(20) | | Active, Inactive, Terminated |
| copay | DECIMAL(10,2) | | Copay amount |
| deductible_remaining | DECIMAL(10,2) | | Deductible remaining |
| oop_remaining | DECIMAL(10,2) | | OOP remaining |
| coinsurance_pct | DECIMAL(5,2) | | Coinsurance % |
| requires_authorization | BOOLEAN | | Prior auth required |
| requires_referral | BOOLEAN | | Referral required |
| network_status | VARCHAR(20) | | In-Network, Out-of-Network |
| response_raw | JSONB | | Full EDI 271 response |
| checked_by | UUID | FOREIGN KEY → users | User who ran check |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:** patient_id, check_date

---

### Table 12: authorizations
**Purpose:** Track prior authorizations

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| authorization_id | UUID | PRIMARY KEY | |
| patient_id | UUID | FOREIGN KEY → patients | |
| insurance_id | UUID | FOREIGN KEY → patient_insurance | |
| provider_id | UUID | FOREIGN KEY → providers | Requesting provider |
| authorization_number | VARCHAR(50) | | Payer-assigned auth number |
| status | VARCHAR(20) | NOT NULL | Submitted, Pending, Approved, Denied, Expired |
| request_date | DATE | | Request submitted date |
| approved_date | DATE | | Approval date |
| valid_from | DATE | | Authorization valid from |
| valid_to | DATE | | Authorization valid to |
| diagnosis_codes | TEXT[] | | Array of ICD-10 codes |
| procedure_codes | TEXT[] | | Array of CPT codes |
| units_approved | INTEGER | | Number of units/visits approved |
| units_used | INTEGER | DEFAULT 0 | Number of units used |
| clinical_notes | TEXT | | Clinical justification |
| denial_reason | TEXT | | Denial reason if denied |
| created_by | UUID | FOREIGN KEY → users | |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | | |

**Indexes:** patient_id, authorization_number, valid_to

---

### Table 13: appointments
**Purpose:** Store patient appointments

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| appointment_id | UUID | PRIMARY KEY | |
| patient_id | UUID | FOREIGN KEY → patients | |
| provider_id | UUID | FOREIGN KEY → providers | |
| appointment_date | DATE | NOT NULL | Appointment date |
| appointment_time | TIME | NOT NULL | Appointment time |
| duration_minutes | INTEGER | NOT NULL | Duration (e.g., 30, 60) |
| appointment_type | VARCHAR(50) | | New Patient, Follow-up, Procedure |
| reason | TEXT | | Reason for visit |
| location | VARCHAR(100) | | Clinic/room location |
| status | VARCHAR(20) | NOT NULL | Scheduled, Confirmed, Checked In, Completed, Cancelled, No Show |
| reminder_sent | BOOLEAN | DEFAULT FALSE | Reminder sent flag |
| notes | TEXT | | Appointment notes |
| created_by | UUID | FOREIGN KEY → users | |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | | |

**Indexes:** patient_id, provider_id, appointment_date, status

---

### Table 14: encounters
**Purpose:** Store patient visit/encounter records

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| encounter_id | UUID | PRIMARY KEY | |
| patient_id | UUID | FOREIGN KEY → patients | |
| provider_id | UUID | FOREIGN KEY → providers | Rendering provider |
| appointment_id | UUID | FOREIGN KEY → appointments | Linked appointment |
| encounter_type | VARCHAR(50) | NOT NULL | Office, Emergency, Inpatient, Outpatient, Telehealth |
| encounter_date | DATE | NOT NULL | Date of service |
| check_in_time | TIMESTAMP | | Check-in time |
| check_out_time | TIMESTAMP | | Check-out time |
| department | VARCHAR(50) | | Department |
| facility_location | VARCHAR(100) | | Facility location |
| place_of_service | VARCHAR(2) | | POS code (11=Office, 21=Inpatient, 22=Outpatient, etc.) |
| chief_complaint | TEXT | | Chief complaint |
| referring_provider_id | UUID | FOREIGN KEY → providers | Referring provider |
| status | VARCHAR(20) | NOT NULL | Scheduled, Checked In, In Progress, Completed, Cancelled |
| admission_date | DATE | | Admission date (inpatient) |
| discharge_date | DATE | | Discharge date (inpatient) |
| discharge_disposition | VARCHAR(50) | | Discharge disposition |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | | |

**Indexes:** patient_id, provider_id, encounter_date, status

---

### Table 15: encounter_diagnoses
**Purpose:** Store diagnoses for each encounter

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| diagnosis_id | UUID | PRIMARY KEY | |
| encounter_id | UUID | FOREIGN KEY → encounters | |
| icd10_code | VARCHAR(10) | NOT NULL | ICD-10 diagnosis code |
| description | VARCHAR(255) | | Diagnosis description |
| is_principal | BOOLEAN | DEFAULT FALSE | Principal diagnosis flag |
| sequence | INTEGER | | Diagnosis sequence (1, 2, 3...) |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:** encounter_id, icd10_code

---

### Table 16: encounter_procedures
**Purpose:** Store procedures for each encounter

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| procedure_id | UUID | PRIMARY KEY | |
| encounter_id | UUID | FOREIGN KEY → encounters | |
| cpt_code | VARCHAR(10) | NOT NULL | CPT/HCPCS code |
| description | VARCHAR(255) | | Procedure description |
| modifier1 | VARCHAR(2) | | Modifier 1 |
| modifier2 | VARCHAR(2) | | Modifier 2 |
| modifier3 | VARCHAR(2) | | Modifier 3 |
| modifier4 | VARCHAR(2) | | Modifier 4 |
| units | INTEGER | DEFAULT 1 | Number of units |
| diagnosis_pointers | TEXT[] | | Array of linked diagnosis sequence numbers |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:** encounter_id, cpt_code

---

### Table 17: charges
**Purpose:** Store all billable charges

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| charge_id | UUID | PRIMARY KEY | |
| encounter_id | UUID | FOREIGN KEY → encounters | |
| patient_id | UUID | FOREIGN KEY → patients | |
| provider_id | UUID | FOREIGN KEY → providers | |
| service_date | DATE | NOT NULL | Date of service |
| cdm_id | UUID | FOREIGN KEY → chargemaster | CDM reference |
| cpt_code | VARCHAR(10) | NOT NULL | CPT/HCPCS code |
| description | VARCHAR(255) | | Charge description |
| modifier1 | VARCHAR(2) | | |
| modifier2 | VARCHAR(2) | | |
| modifier3 | VARCHAR(2) | | |
| modifier4 | VARCHAR(2) | | |
| units | INTEGER | DEFAULT 1 | Quantity |
| charge_amount | DECIMAL(10,2) | NOT NULL | Standard charge |
| revenue_code | VARCHAR(4) | | Revenue code (UB-04) |
| department | VARCHAR(50) | | Department |
| status | VARCHAR(20) | NOT NULL | Pending, Hold, Released, Billed |
| hold_reason | TEXT | | Reason for hold |
| entered_by | UUID | FOREIGN KEY → users | User who entered charge |
| entered_date | TIMESTAMP | DEFAULT NOW() | Charge entry date |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:** encounter_id, patient_id, service_date, status

---

### Table 18: claims
**Purpose:** Store insurance claims

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| claim_id | UUID | PRIMARY KEY | |
| encounter_id | UUID | FOREIGN KEY → encounters | |
| patient_id | UUID | FOREIGN KEY → patients | |
| insurance_id | UUID | FOREIGN KEY → patient_insurance | |
| payer_id | UUID | FOREIGN KEY → payers | |
| provider_id | UUID | FOREIGN KEY → providers | Rendering provider |
| claim_number | VARCHAR(50) | UNIQUE | Internal claim number |
| claim_type | VARCHAR(10) | NOT NULL | CMS-1500, UB-04 |
| claim_frequency | VARCHAR(1) | DEFAULT '1' | 1=Original, 7=Corrected, 8=Void |
| original_claim_number | VARCHAR(50) | | Original claim # (for corrected claims) |
| billing_provider_npi | VARCHAR(10) | NOT NULL | Billing provider NPI |
| rendering_provider_npi | VARCHAR(10) | NOT NULL | Rendering provider NPI |
| referring_provider_npi | VARCHAR(10) | | Referring provider NPI |
| service_date_from | DATE | NOT NULL | Service date from |
| service_date_to | DATE | NOT NULL | Service date to |
| total_charge_amount | DECIMAL(10,2) | NOT NULL | Total billed amount |
| authorization_number | VARCHAR(50) | | Prior auth number |
| status | VARCHAR(20) | NOT NULL | Draft, Scrubbing, Ready, Submitted, Accepted, Pending, Paid, Denied, Rejected |
| is_clean_claim | BOOLEAN | DEFAULT FALSE | Passed scrubbing |
| submission_date | DATE | | Date submitted |
| submission_method | VARCHAR(20) | | Electronic, Paper |
| clearinghouse_id | VARCHAR(50) | | Clearinghouse tracking ID |
| payer_claim_number | VARCHAR(50) | | Payer-assigned claim number (ICN) |
| timely_filing_deadline | DATE | | Timely filing deadline |
| created_by | UUID | FOREIGN KEY → users | |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | | |

**Indexes:** claim_number, patient_id, payer_id, status, submission_date

---

### Table 19: claim_lines
**Purpose:** Store individual line items on claims

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| line_id | UUID | PRIMARY KEY | |
| claim_id | UUID | FOREIGN KEY → claims | |
| charge_id | UUID | FOREIGN KEY → charges | |
| line_number | INTEGER | NOT NULL | Line number (1, 2, 3...) |
| service_date | DATE | NOT NULL | Date of service |
| place_of_service | VARCHAR(2) | | POS code |
| cpt_code | VARCHAR(10) | NOT NULL | CPT/HCPCS code |
| modifier1 | VARCHAR(2) | | |
| modifier2 | VARCHAR(2) | | |
| modifier3 | VARCHAR(2) | | |
| modifier4 | VARCHAR(2) | | |
| diagnosis_pointers | TEXT[] | | Linked diagnosis codes |
| units | INTEGER | DEFAULT 1 | Units |
| charge_amount | DECIMAL(10,2) | NOT NULL | Billed amount |
| revenue_code | VARCHAR(4) | | Revenue code (UB-04) |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:** claim_id, charge_id

---

### Table 20: claim_scrubbing_errors
**Purpose:** Store claim scrubbing validation errors

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| error_id | UUID | PRIMARY KEY | |
| claim_id | UUID | FOREIGN KEY → claims | |
| error_level | VARCHAR(10) | NOT NULL | Fatal, Warning, Info |
| error_code | VARCHAR(20) | | Error code |
| error_message | TEXT | NOT NULL | Error description |
| field_name | VARCHAR(50) | | Field with error |
| resolved | BOOLEAN | DEFAULT FALSE | Error resolved flag |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:** claim_id, error_level, resolved

---

### Table 21: payments
**Purpose:** Store all payments (insurance and patient)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| payment_id | UUID | PRIMARY KEY | |
| claim_id | UUID | FOREIGN KEY → claims | Claim paid |
| patient_id | UUID | FOREIGN KEY → patients | |
| payer_id | UUID | FOREIGN KEY → payers | Payer (NULL if patient payment) |
| payment_type | VARCHAR(20) | NOT NULL | Insurance, Patient |
| payment_method | VARCHAR(20) | | EFT, Check, Credit Card, Cash, ACH |
| payment_date | DATE | NOT NULL | Payment date |
| check_number | VARCHAR(50) | | Check/EFT number |
| payment_amount | DECIMAL(10,2) | NOT NULL | Total payment amount |
| era_file_id | UUID | FOREIGN KEY → era_files | ERA file reference |
| posted_by | UUID | FOREIGN KEY → users | User who posted payment |
| posted_date | TIMESTAMP | DEFAULT NOW() | Payment posting date |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:** claim_id, patient_id, payer_id, payment_date

---

### Table 22: payment_line_items
**Purpose:** Store line-level payment details

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| line_item_id | UUID | PRIMARY KEY | |
| payment_id | UUID | FOREIGN KEY → payments | |
| claim_line_id | UUID | FOREIGN KEY → claim_lines | |
| billed_amount | DECIMAL(10,2) | NOT NULL | Amount billed |
| allowed_amount | DECIMAL(10,2) | NOT NULL | Allowed amount |
| paid_amount | DECIMAL(10,2) | NOT NULL | Amount paid |
| deductible | DECIMAL(10,2) | DEFAULT 0 | Deductible applied |
| copay | DECIMAL(10,2) | DEFAULT 0 | Copay applied |
| coinsurance | DECIMAL(10,2) | DEFAULT 0 | Coinsurance applied |
| contractual_adjustment | DECIMAL(10,2) | DEFAULT 0 | Contractual write-off |
| adjustment_code | VARCHAR(10) | | CARC code |
| adjustment_reason | TEXT | | Adjustment reason |
| remark_code | VARCHAR(10) | | RARC code |
| patient_responsibility | DECIMAL(10,2) | DEFAULT 0 | Patient balance |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:** payment_id, claim_line_id

---

### Table 23: era_files
**Purpose:** Store ERA (EDI 835) files

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| era_file_id | UUID | PRIMARY KEY | |
| payer_id | UUID | FOREIGN KEY → payers | |
| file_name | VARCHAR(255) | | ERA file name |
| file_content | TEXT | | Raw EDI 835 content |
| check_number | VARCHAR(50) | | Check/EFT number |
| check_date | DATE | | Check date |
| total_amount | DECIMAL(10,2) | | Total payment amount |
| claim_count | INTEGER | | Number of claims in ERA |
| auto_posted_count | INTEGER | DEFAULT 0 | Claims auto-posted |
| manual_posted_count | INTEGER | DEFAULT 0 | Claims manually posted |
| status | VARCHAR(20) | NOT NULL | Received, Processing, Completed |
| imported_by | UUID | FOREIGN KEY → users | |
| imported_date | TIMESTAMP | DEFAULT NOW() | |

**Indexes:** payer_id, check_number, check_date

---

### Table 24: denials
**Purpose:** Track denied claims

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| denial_id | UUID | PRIMARY KEY | |
| claim_id | UUID | FOREIGN KEY → claims | |
| denial_date | DATE | NOT NULL | Denial date |
| denial_code | VARCHAR(10) | | CARC code |
| denial_reason | TEXT | NOT NULL | Denial reason |
| denial_category | VARCHAR(50) | | Clinical, Technical, Authorization, Eligibility, Timely Filing |
| denial_amount | DECIMAL(10,2) | NOT NULL | Denied amount |
| is_appealable | BOOLEAN | DEFAULT TRUE | Can be appealed |
| appeal_deadline | DATE | | Appeal deadline |
| status | VARCHAR(20) | NOT NULL | New, Under Review, Appealed, Overturned, Upheld |
| assigned_to | UUID | FOREIGN KEY → users | User assigned to work denial |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | | |

**Indexes:** claim_id, denial_date, status, appeal_deadline

---

### Table 25: appeals
**Purpose:** Track claim appeals

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| appeal_id | UUID | PRIMARY KEY | |
| denial_id | UUID | FOREIGN KEY → denials | |
| claim_id | UUID | FOREIGN KEY → claims | |
| appeal_level | INTEGER | NOT NULL | 1, 2, 3 |
| appeal_date | DATE | NOT NULL | Appeal submission date |
| appeal_method | VARCHAR(20) | | Fax, Mail, Portal |
| appeal_letter | TEXT | | Appeal letter content |
| supporting_documents | TEXT[] | | Array of document URLs |
| status | VARCHAR(20) | NOT NULL | Submitted, Under Review, Approved, Denied, Partially Approved |
| outcome_date | DATE | | Outcome date |
| additional_payment | DECIMAL(10,2) | DEFAULT 0 | Additional payment received |
| outcome_notes | TEXT | | Outcome notes |
| submitted_by | UUID | FOREIGN KEY → users | |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | | |

**Indexes:** denial_id, claim_id, appeal_date, status

---

### Table 26: patient_statements
**Purpose:** Track patient billing statements

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| statement_id | UUID | PRIMARY KEY | |
| patient_id | UUID | FOREIGN KEY → patients | |
| statement_date | DATE | NOT NULL | Statement date |
| statement_number | VARCHAR(50) | UNIQUE | Statement number |
| previous_balance | DECIMAL(10,2) | DEFAULT 0 | Previous balance |
| new_charges | DECIMAL(10,2) | DEFAULT 0 | New charges |
| payments_received | DECIMAL(10,2) | DEFAULT 0 | Payments received |
| adjustments | DECIMAL(10,2) | DEFAULT 0 | Adjustments |
| current_balance | DECIMAL(10,2) | NOT NULL | Current balance due |
| due_date | DATE | | Payment due date |
| delivery_method | VARCHAR(20) | | Mail, Email, Portal |
| sent_date | DATE | | Date sent |
| pdf_url | TEXT | | Statement PDF URL |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:** patient_id, statement_date

---

### Table 27: patient_payments
**Purpose:** Track patient payments

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| patient_payment_id | UUID | PRIMARY KEY | |
| patient_id | UUID | FOREIGN KEY → patients | |
| payment_date | DATE | NOT NULL | Payment date |
| payment_amount | DECIMAL(10,2) | NOT NULL | Payment amount |
| payment_method | VARCHAR(20) | NOT NULL | Credit Card, Debit Card, ACH, Check, Cash |
| transaction_id | VARCHAR(100) | | Payment processor transaction ID |
| check_number | VARCHAR(50) | | Check number |
| payment_plan_id | UUID | FOREIGN KEY → payment_plans | If part of payment plan |
| notes | TEXT | | Payment notes |
| received_by | UUID | FOREIGN KEY → users | |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:** patient_id, payment_date

---

### Table 28: payment_plans
**Purpose:** Track patient payment plans

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| plan_id | UUID | PRIMARY KEY | |
| patient_id | UUID | FOREIGN KEY → patients | |
| total_amount | DECIMAL(10,2) | NOT NULL | Total amount owed |
| monthly_payment | DECIMAL(10,2) | NOT NULL | Monthly payment amount |
| start_date | DATE | NOT NULL | Plan start date |
| end_date | DATE | NOT NULL | Plan end date |
| interest_rate | DECIMAL(5,2) | DEFAULT 0 | Interest rate % |
| status | VARCHAR(20) | NOT NULL | Active, Completed, Defaulted, Cancelled |
| auto_pay_enabled | BOOLEAN | DEFAULT FALSE | Auto-pay enabled |
| created_by | UUID | FOREIGN KEY → users | |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | | |

**Indexes:** patient_id, status

---

### Table 29: collections
**Purpose:** Track accounts in collections

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| collection_id | UUID | PRIMARY KEY | |
| patient_id | UUID | FOREIGN KEY → patients | |
| original_balance | DECIMAL(10,2) | NOT NULL | Original balance |
| current_balance | DECIMAL(10,2) | NOT NULL | Current balance |
| collection_status | VARCHAR(20) | NOT NULL | Internal, External, Bad Debt |
| sent_to_collections_date | DATE | | Date sent to external collections |
| collection_agency | VARCHAR(100) | | Collection agency name |
| agency_fee_pct | DECIMAL(5,2) | | Agency commission % |
| notes | TEXT | | Collection notes |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | | |

**Indexes:** patient_id, collection_status

---

### Table 30: refunds
**Purpose:** Track refunds issued

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| refund_id | UUID | PRIMARY KEY | |
| patient_id | UUID | FOREIGN KEY → patients | |
| payer_id | UUID | FOREIGN KEY → payers | If refund to payer |
| refund_amount | DECIMAL(10,2) | NOT NULL | Refund amount |
| refund_reason | TEXT | NOT NULL | Reason for refund |
| refund_method | VARCHAR(20) | | Check, ACH, Credit Card Reversal |
| check_number | VARCHAR(50) | | Check number |
| refund_date | DATE | NOT NULL | Refund date |
| original_payment_id | UUID | FOREIGN KEY → payments | Original payment |
| issued_by | UUID | FOREIGN KEY → users | |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:** patient_id, payer_id, refund_date

---

### Table 31: audit_logs
**Purpose:** Comprehensive audit trail (HIPAA compliance)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| log_id | UUID | PRIMARY KEY | |
| user_id | UUID | FOREIGN KEY → users | User who performed action |
| action_type | VARCHAR(50) | NOT NULL | Login, Logout, Create, Read, Update, Delete |
| table_name | VARCHAR(50) | | Table affected |
| record_id | UUID | | Record ID affected |
| patient_id | UUID | FOREIGN KEY → patients | Patient record accessed (if applicable) |
| before_value | JSONB | | Data before change |
| after_value | JSONB | | Data after change |
| ip_address | VARCHAR(50) | | User IP address |
| timestamp | TIMESTAMP | DEFAULT NOW() | Action timestamp |

**Indexes:** user_id, patient_id, action_type, timestamp  
**Retention:** 7 years minimum

---

### Table 32: reports
**Purpose:** Store saved reports and schedules

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| report_id | UUID | PRIMARY KEY | |
| report_name | VARCHAR(100) | NOT NULL | Report name |
| report_type | VARCHAR(50) | NOT NULL | Standard, Custom |
| report_category | VARCHAR(50) | | Financial, Operational, Compliance |
| parameters | JSONB | | Report parameters |
| schedule | VARCHAR(50) | | Daily, Weekly, Monthly, None |
| recipients | TEXT[] | | Email recipients |
| created_by | UUID | FOREIGN KEY → users | |
| created_at | TIMESTAMP | DEFAULT NOW() | |

---

### Table 33: code_sets
**Purpose:** Store medical code sets (ICD-10, CPT, HCPCS)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| code_id | UUID | PRIMARY KEY | |
| code_type | VARCHAR(10) | NOT NULL | ICD10, CPT, HCPCS, DRG, MODIFIER |
| code | VARCHAR(10) | NOT NULL | Code value |
| description | TEXT | NOT NULL | Code description |
| effective_date | DATE | NOT NULL | Effective date |
| termination_date | DATE | | Termination date |
| is_active | BOOLEAN | DEFAULT TRUE | |

**Indexes:** code_type, code, effective_date  
**Update Frequency:** Annual (ICD-10, CPT updates every January 1)

---

### Table 34: ncci_edits
**Purpose:** Store NCCI (National Correct Coding Initiative) edits

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| edit_id | UUID | PRIMARY KEY | |
| column1_code | VARCHAR(10) | NOT NULL | Column 1 CPT code |
| column2_code | VARCHAR(10) | NOT NULL | Column 2 CPT code |
| modifier_indicator | VARCHAR(1) | | 0=Not allowed, 1=Allowed with modifier |
| effective_date | DATE | NOT NULL | |
| deletion_date | DATE | | |

**Indexes:** column1_code, column2_code  
**Update Frequency:** Quarterly from CMS

---

### Table 35: lcd_ncd_rules
**Purpose:** Store LCD/NCD (Local/National Coverage Determination) rules

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| rule_id | UUID | PRIMARY KEY | |
| rule_type | VARCHAR(10) | NOT NULL | LCD, NCD |
| cpt_code | VARCHAR(10) | NOT NULL | CPT code |
| covered_icd10_codes | TEXT[] | | Array of covered ICD-10 codes |
| mac_region | VARCHAR(10) | | MAC region (for LCD) |
| effective_date | DATE | NOT NULL | |
| termination_date | DATE | | |

**Indexes:** cpt_code, rule_type

---

## 3. Database Relationships

### Key Relationships:
1. **patients** → **patient_insurance** (1:Many) - One patient, multiple insurances
2. **patients** → **encounters** (1:Many) - One patient, many visits
3. **encounters** → **charges** (1:Many) - One encounter, many charges
4. **encounters** → **claims** (1:1 or 1:Many) - One encounter can generate multiple claims (primary, secondary)
5. **claims** → **claim_lines** (1:Many) - One claim, multiple line items
6. **claims** → **payments** (1:Many) - One claim can have multiple payments
7. **claims** → **denials** (1:1) - One claim, one denial record
8. **denials** → **appeals** (1:Many) - One denial, multiple appeal levels
9. **providers** → **provider_credentials** (1:Many) - One provider, credentialed with many payers
10. **payers** → **payer_contracts** (1:Many) - One payer, multiple contracts
11. **payer_contracts** → **payer_contract_rates** (1:Many) - One contract, many CPT rates

---

## 4. Indexes & Performance

### Critical Indexes:
- All foreign keys
- Date fields used in queries (service_date, payment_date, etc.)
- Status fields (claim.status, encounter.status)
- Search fields (patient.last_name, patient.mrn)

### Partitioning Strategy:
- **claims** table: Partition by submission_date (monthly partitions)
- **payments** table: Partition by payment_date (monthly partitions)
- **audit_logs** table: Partition by timestamp (monthly partitions)

---

## 5. Data Retention Policy

| Table | Retention Period |
|-------|------------------|
| audit_logs | 7 years (HIPAA) |
| patients | Indefinite |
| encounters | Indefinite |
| claims | 10 years |
| payments | 10 years |
| denials | 10 years |
| appeals | 10 years |
| reports | 3 years |

---

## 6. Security & Encryption

### Encrypted Fields:
- patients.ssn_encrypted
- providers.ssn_encrypted
- Any PHI (Protected Health Information)

### Encryption Method:
- AES-256 encryption at rest
- TLS 1.2+ for data in transit
- Application-level encryption for SSN fields

---

## 7. Backup Strategy

- **Full Backup:** Daily at 2 AM
- **Incremental Backup:** Every 4 hours
- **Transaction Log Backup:** Every 15 minutes
- **Backup Retention:** 30 days
- **Disaster Recovery:** Geo-redundant backups in separate region

---

**Next Step:** Create API Integration Requirements Document
