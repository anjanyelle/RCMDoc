# Healthcare RCM Application - Database Design Document

**Version:** 1.0  
**Date:** May 18, 2026  
**For:** Development Team  

---

## 1. Database Overview

**Database Type:** Relational Database (PostgreSQL recommended)  
**Why Relational:** Healthcare data is highly structured with complex relationships  

**Total Tables:**  
- 35 Core RCM Tables  
- 15 Enterprise Operational & Integration Tables  
- 50 Enterprise Healthcare RCM Tables  

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
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| employee_id | VARCHAR(50) | UNIQUE | Internal employee identifier |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Login username |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| email | VARCHAR(100) | UNIQUE, NOT NULL | Email address |
| email_verified | BOOLEAN | DEFAULT FALSE | Email verification status |
| phone_verified | BOOLEAN | DEFAULT FALSE | Phone verification status |
| first_name | VARCHAR(50) | NOT NULL | First name |
| middle_name | VARCHAR(50) | | Middle name |
| last_name | VARCHAR(50) | NOT NULL | Last name |
| phone_number | VARCHAR(20) | | Contact number |
| profile_image_url | TEXT | | User profile image |
| department | VARCHAR(100) | | Billing, Coding, AR, IT |
| designation | VARCHAR(100) | | Job designation |
| role_id | UUID | FOREIGN KEY → roles | User role |
| provider_id | UUID | FOREIGN KEY → providers | Linked provider account |
| supervisor_user_id | UUID | FOREIGN KEY → users | Reporting manager |
| is_active | BOOLEAN | DEFAULT TRUE | Account status |
| account_locked | BOOLEAN | DEFAULT FALSE | Account locked status |
| account_locked_until | TIMESTAMP | | Lock expiration timestamp |
| failed_login_attempts | INTEGER | DEFAULT 0 | Failed login attempts |
| last_failed_login | TIMESTAMP | | Last failed login timestamp |
| last_login | TIMESTAMP | | Last login time |
| login_status | VARCHAR(20) | | Online, Offline |
| last_activity_at | TIMESTAMP | | Last user activity |
| session_timeout_minutes | INTEGER | DEFAULT 30 | Session timeout duration |
| mfa_enabled | BOOLEAN | DEFAULT FALSE | Multi-factor auth enabled |
| mfa_secret | VARCHAR(100) | | MFA secret key |
| password_last_changed_at | TIMESTAMP | | Password last changed date |
| password_reset_token | VARCHAR(255) | | Password reset token |
| password_reset_expiry | TIMESTAMP | | Password reset token expiration |
| is_password_change_required | BOOLEAN | DEFAULT FALSE | Force password change |
| timezone | VARCHAR(50) | | User timezone |
| preferred_language | VARCHAR(20) | | Preferred language |
| signature_url | TEXT | | Digital signature path |
| hire_date | DATE | | Employee joining date |
| termination_date | DATE | | Employee termination date |
| created_by | UUID | FOREIGN KEY → users | User who created record |
| updated_by | UUID | FOREIGN KEY → users | User who updated record |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation date |
| updated_at | TIMESTAMP | | Last update date |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | User who soft deleted record |

**Indexes:** username, email, role_id, tenant_id, employee_id, provider_id, supervisor_user_id, is_active, account_locked, email_verified, deleted_at

---

### Table 2: roles
**Purpose:** Define user roles and permissions

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| role_id | UUID | PRIMARY KEY | Unique role identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| role_name | VARCHAR(50) | UNIQUE, NOT NULL | Role name |
| description | TEXT | | Role description |
| permissions | JSONB | | Permissions object |
| is_active | BOOLEAN | DEFAULT TRUE | Role active status |
| created_by | UUID | FOREIGN KEY → users | User who created role |
| updated_by | UUID | FOREIGN KEY → users | User who updated role |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | User who deleted role |

Sample Roles:

System Administrator
Front Desk Staff
Clinical Staff
Medical Coder
Billing Specialist
AR Manager
Collections Staff
Finance Manager
Compliance Officer
Provider (Doctor)


**Indexes:** role_name, tenant_id, is_active

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
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| npi_type1 | VARCHAR(10) | UNIQUE, NOT NULL | Individual NPI number |
| npi_type2 | VARCHAR(10) | | Organization NPI |
| first_name | VARCHAR(50) | NOT NULL | First name |
| last_name | VARCHAR(50) | NOT NULL | Last name |
| middle_name | VARCHAR(50) | | Middle name |
| suffix | VARCHAR(10) | | MD, DO, etc. |
| dob | DATE | | Date of birth |
| ssn_encrypted | VARCHAR(255) | | Encrypted SSN |
| license_number | VARCHAR(50) | | Medical license number |
| license_state | VARCHAR(2) | | License state |
| dea_number | VARCHAR(20) | | DEA number |
| caqh_id | VARCHAR(50) | | CAQH credentialing ID |
| taxonomy_code | VARCHAR(20) | | Provider taxonomy code |
| taxonomy_description | VARCHAR(255) | | Taxonomy description |
| specialty_primary | VARCHAR(100) | | Primary specialty |
| specialty_secondary | VARCHAR(100) | | Secondary specialty |
| credentialing_status | VARCHAR(30) | | Credentialing workflow status |
| employment_status | VARCHAR(30) | | Active/Inactive |
| email | VARCHAR(100) | | Email |
| phone | VARCHAR(20) | | Phone |
| fax_number | VARCHAR(20) | | Fax number |
| address_line1 | VARCHAR(100) | | Address |
| address_line2 | VARCHAR(100) | | Address line 2 |
| city | VARCHAR(50) | | City |
| state | VARCHAR(2) | | State |
| zip_code | VARCHAR(10) | | ZIP code |
| signature_image | TEXT | | Digital signature |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |
| created_by | UUID | FOREIGN KEY → users | Created by |
| updated_by | UUID | FOREIGN KEY → users | Updated by |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | User who deleted provider |

**Indexes:** npi_type1, last_name, tenant_id, credentialing_status

---

### Table 4: provider_credentials
**Purpose:** Track provider credentialing with each payer

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| credential_id | UUID | PRIMARY KEY | Credential identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| provider_id | UUID | FOREIGN KEY → providers | Provider |
| payer_id | UUID | FOREIGN KEY → payers | Insurance payer |
| credentialing_type | VARCHAR(50) | | Medicare/Commercial |
| status | VARCHAR(20) | NOT NULL | Pending, Approved, Denied |
| application_date | DATE | | Application submitted date |
| effective_date | DATE | | Credential effective date |
| expiration_date | DATE | | Credential expiration date |
| recredential_due_date | DATE | | Recredentialing due date |
| credential_number | VARCHAR(50) | | Payer credential number |
| rejection_reason | TEXT | | Denial reason |
| document_id | UUID | FOREIGN KEY → documents | Credential documents |
| notes | TEXT | | Notes |
| approved_by | UUID | FOREIGN KEY → users | Approved by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |

**Indexes:** provider_id, payer_id, expiration_date

---

### Table 5: payers
**Purpose:** Store insurance companies/payers

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| payer_id | UUID | PRIMARY KEY | Payer identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| payer_name | VARCHAR(100) | NOT NULL | Insurance payer name |
| payer_code | VARCHAR(20) | UNIQUE | Internal payer code |
| payer_id_external | VARCHAR(50) | | External payer ID |
| payer_type | VARCHAR(20) | | Commercial, Medicare |
| payer_category | VARCHAR(50) | | Government/Commercial |
| address_line1 | VARCHAR(100) | | Address |
| address_line2 | VARCHAR(100) | | Address line 2 |
| city | VARCHAR(50) | | City |
| state | VARCHAR(2) | | State |
| zip_code | VARCHAR(10) | | ZIP code |
| phone | VARCHAR(20) | | Phone |
| support_email | VARCHAR(100) | | Support email |
| website_url | TEXT | | Website URL |
| portal_url | TEXT | | Claims portal URL |
| edi_support_contact | VARCHAR(100) | | EDI support contact |
| claims_address | VARCHAR(200) | | Claims mailing address |
| electronic_payer_id | VARCHAR(20) | | Electronic payer ID |
| timely_filing_days | INTEGER | | Timely filing limit |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |

**Indexes:** payer_name, payer_code, electronic_payer_id

---

### Table 6: payer_contracts
**Purpose:** Store contracted reimbursement agreements with insurance payers

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| contract_id | UUID | PRIMARY KEY | Contract identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| payer_id | UUID | FOREIGN KEY → payers | Insurance payer |
| contract_name | VARCHAR(100) | NOT NULL | Contract name |
| contract_number | VARCHAR(50) | | Contract identifier |
| contract_status | VARCHAR(30) | | Active, Expired, Pending |
| effective_date | DATE | NOT NULL | Contract start date |
| end_date | DATE | | Contract end date |
| renewal_date | DATE | | Contract renewal date |
| signed_date | DATE | | Contract signed date |
| signed_document_id | UUID | FOREIGN KEY → documents | Contract PDF document |
| payment_methodology | VARCHAR(50) | | Fee Schedule, DRG, APC |
| percentage_of_charges | DECIMAL(5,2) | | Percent reimbursement |
| reimbursement_cycle_days | INTEGER | | Expected reimbursement days |
| contract_terms | TEXT | | Contract terms |
| escalation_clause | TEXT | | Escalation details |
| carve_out_services | TEXT | | Special carve-out services |
| stop_loss_threshold | DECIMAL(10,2) | | Stop loss amount |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | Deleted by user |

**Indexes:** payer_id, contract_status, effective_date, tenant_id

---

### Table 7: payer_contract_rates
**Purpose:** Store CPT/HCPCS reimbursement rates for payer contracts

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| rate_id | UUID | PRIMARY KEY | Rate identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| contract_id | UUID | FOREIGN KEY → payer_contracts | Linked payer contract |
| fee_schedule_name | VARCHAR(100) | | Fee schedule name |
| cpt_code | VARCHAR(10) | NOT NULL | CPT/HCPCS code |
| modifier | VARCHAR(10) | | Modifier |
| place_of_service | VARCHAR(2) | | POS-specific reimbursement |
| revenue_code | VARCHAR(4) | | Revenue code |
| billing_classification | VARCHAR(50) | | Professional/Facility |
| allowed_amount | DECIMAL(10,2) | NOT NULL | Contracted allowed amount |
| expected_patient_responsibility | DECIMAL(10,2) | | Estimated patient balance |
| reimbursement_percentage | DECIMAL(5,2) | | Reimbursement percentage |
| effective_date | DATE | | Rate effective date |
| end_date | DATE | | Rate end date |
| requires_authorization | BOOLEAN | DEFAULT FALSE | Prior auth required |
| requires_modifier | BOOLEAN | DEFAULT FALSE | Modifier required |
| notes | TEXT | | Internal notes |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |

**Indexes:** contract_id, cpt_code, place_of_service, effective_date, tenant_id

---

### Table 8: chargemaster (CDM)
**Purpose:** Hospital fee schedule and charge master services

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| cdm_id | UUID | PRIMARY KEY | Chargemaster identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| charge_code | VARCHAR(20) | UNIQUE, NOT NULL | Internal charge code |
| cpt_code | VARCHAR(10) | | CPT/HCPCS code |
| hcpcs_code | VARCHAR(10) | | HCPCS code |
| description | VARCHAR(255) | NOT NULL | Service description |
| department | VARCHAR(50) | | Department |
| billing_category | VARCHAR(50) | | Radiology, Lab, Surgery |
| revenue_code | VARCHAR(4) | | UB-04 revenue code |
| place_of_service | VARCHAR(2) | | POS code |
| standard_charge | DECIMAL(10,2) | NOT NULL | Standard charge amount |
| minimum_charge | DECIMAL(10,2) | | Minimum allowed charge |
| maximum_charge | DECIMAL(10,2) | | Maximum charge |
| cost_to_hospital | DECIMAL(10,2) | | Internal hospital cost |
| requires_authorization | BOOLEAN | DEFAULT FALSE | Prior auth required |
| requires_modifier | BOOLEAN | DEFAULT FALSE | Modifier required |
| billable_flag | BOOLEAN | DEFAULT TRUE | Billable service flag |
| active_for_claims | BOOLEAN | DEFAULT TRUE | Available for billing |
| effective_date | DATE | NOT NULL | Effective date |
| end_date | DATE | | End date |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | Deleted by user |

**Indexes:** charge_code, cpt_code, department, billing_category, tenant_id

---

### Table 9: patients
**Purpose:** Store patient demographics

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| patient_id | UUID | PRIMARY KEY | Patient identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| mrn | VARCHAR(20) | UNIQUE, NOT NULL | Medical record number |
| first_name | VARCHAR(50) | NOT NULL | First name |
| last_name | VARCHAR(50) | NOT NULL | Last name |
| middle_name | VARCHAR(50) | | Middle name |
| suffix | VARCHAR(10) | | Suffix |
| dob | DATE | NOT NULL | Date of birth |
| gender | VARCHAR(10) | NOT NULL | Gender |
| marital_status | VARCHAR(20) | | Marital status |
| employment_status | VARCHAR(30) | | Employment status |
| employer_name | VARCHAR(100) | | Employer name |
| ssn_encrypted | VARCHAR(255) | | Encrypted SSN |
| address_line1 | VARCHAR(100) | | Address |
| address_line2 | VARCHAR(100) | | Address line 2 |
| city | VARCHAR(50) | | City |
| state | VARCHAR(2) | | State |
| zip_code | VARCHAR(10) | | ZIP code |
| phone_home | VARCHAR(20) | | Home phone |
| phone_mobile | VARCHAR(20) | | Mobile phone |
| phone_work | VARCHAR(20) | | Work phone |
| email | VARCHAR(100) | | Email |
| preferred_language | VARCHAR(20) | | Preferred language |
| preferred_contact_method | VARCHAR(20) | | Email/SMS/Phone |
| race | VARCHAR(50) | | Race |
| ethnicity | VARCHAR(50) | | Ethnicity |
| emergency_contact_name | VARCHAR(100) | | Emergency contact |
| emergency_contact_phone | VARCHAR(20) | | Emergency phone |
| emergency_contact_relationship | VARCHAR(50) | | Relationship |
| portal_access_enabled | BOOLEAN | DEFAULT FALSE | Patient portal access |
| consent_signed | BOOLEAN | DEFAULT FALSE | HIPAA consent signed |
| consent_signed_date | DATE | | Consent date |
| deceased_flag | BOOLEAN | DEFAULT FALSE | Deceased patient flag |
| deceased_date | DATE | | Date of death |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | Deleted by user |

**Indexes:** mrn, last_name, dob, tenant_id, email

---

### Table 10: patient_insurance
**Purpose:** Store patient insurance coverage details

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| insurance_id | UUID | PRIMARY KEY | Insurance identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| patient_id | UUID | FOREIGN KEY → patients | Patient |
| payer_id | UUID | FOREIGN KEY → payers | Insurance payer |
| priority | INTEGER | NOT NULL | Primary/Secondary/Tertiary |
| policy_number | VARCHAR(50) | NOT NULL | Policy/member ID |
| group_number | VARCHAR(50) | | Group number |
| subscriber_name | VARCHAR(100) | | Subscriber name |
| subscriber_dob | DATE | | Subscriber DOB |
| subscriber_ssn_encrypted | VARCHAR(255) | | Subscriber SSN |
| subscriber_relationship | VARCHAR(20) | | Self/Spouse/Child |
| employer_name | VARCHAR(100) | | Employer name |
| effective_date | DATE | | Coverage effective date |
| termination_date | DATE | | Coverage termination date |
| insurance_status | VARCHAR(20) | | Active/Inactive |
| verification_status | VARCHAR(30) | | Verified/Unverified |
| verification_date | TIMESTAMP | | Last verification |
| authorization_required | BOOLEAN | DEFAULT FALSE | Prior auth required |
| referral_required | BOOLEAN | DEFAULT FALSE | Referral required |
| copay | DECIMAL(10,2) | | Copay amount |
| deductible_annual | DECIMAL(10,2) | | Annual deductible |
| deductible_met | DECIMAL(10,2) | | Deductible met |
| oop_max_annual | DECIMAL(10,2) | | OOP maximum |
| oop_met | DECIMAL(10,2) | | OOP met |
| coinsurance_percentage | DECIMAL(5,2) | | Coinsurance percentage |
| card_front_image | TEXT | | Insurance card front |
| card_back_image | TEXT | | Insurance card back |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | Deleted by user |

**Indexes:** patient_id, payer_id, priority, verification_status, tenant_id

---

### Table 11: eligibility_checks
**Purpose:** Store insurance eligibility verification history

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| check_id | UUID | PRIMARY KEY | Eligibility check identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| patient_id | UUID | FOREIGN KEY → patients | Patient |
| insurance_id | UUID | FOREIGN KEY → patient_insurance | Insurance |
| appointment_id | UUID | FOREIGN KEY → appointments | Related appointment |
| transaction_id | VARCHAR(100) | | EDI/API transaction ID |
| verification_source | VARCHAR(50) | | Clearinghouse/API |
| response_code | VARCHAR(50) | | Eligibility response code |
| check_date | TIMESTAMP | NOT NULL | Verification timestamp |
| service_date | DATE | | Service date |
| coverage_status | VARCHAR(20) | | Active/Inactive |
| network_status | VARCHAR(20) | | In/Out-of-network |
| copay | DECIMAL(10,2) | | Copay |
| deductible_remaining | DECIMAL(10,2) | | Remaining deductible |
| oop_remaining | DECIMAL(10,2) | | Remaining OOP |
| coinsurance_pct | DECIMAL(5,2) | | Coinsurance percentage |
| requires_authorization | BOOLEAN | | Prior auth required |
| requires_referral | BOOLEAN | | Referral required |
| response_time_ms | INTEGER | | API response latency |
| retry_attempts | INTEGER | DEFAULT 0 | Retry count |
| response_raw | JSONB | | Full EDI 271 response |
| checked_by | UUID | FOREIGN KEY → users | User who checked eligibility |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes:** patient_id, insurance_id, check_date, transaction_id, tenant_id

---

### Table 12: authorizations
**Purpose:** Track prior authorizations

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| authorization_id | UUID | PRIMARY KEY | Authorization identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| patient_id | UUID | FOREIGN KEY → patients | Patient |
| insurance_id | UUID | FOREIGN KEY → patient_insurance | Insurance |
| provider_id | UUID | FOREIGN KEY → providers | Requesting provider |
| encounter_id | UUID | FOREIGN KEY → encounters | Related encounter |
| authorization_type | VARCHAR(50) | | Inpatient/Outpatient |
| urgency_level | VARCHAR(20) | | Urgent/Routine |
| authorization_number | VARCHAR(50) | | Auth number |
| payer_case_reference | VARCHAR(100) | | Payer reference |
| status | VARCHAR(20) | NOT NULL | Pending/Approved/Denied |
| status_reason | TEXT | | Status reason |
| request_date | DATE | | Request date |
| approved_date | DATE | | Approval date |
| valid_from | DATE | | Valid from |
| valid_to | DATE | | Valid to |
| diagnosis_codes | TEXT[] | | ICD-10 codes |
| procedure_codes | TEXT[] | | CPT codes |
| units_approved | INTEGER | | Approved units |
| units_used | INTEGER | DEFAULT 0 | Used units |
| clinical_notes | TEXT | | Clinical justification |
| denial_reason | TEXT | | Denial reason |
| assigned_to | UUID | FOREIGN KEY → users | Assigned user |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |

**Indexes:** patient_id, authorization_number, valid_to, status, tenant_id

---

### Table 13: appointments
**Purpose:** Store patient appointments

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| appointment_id | UUID | PRIMARY KEY | Appointment identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| patient_id | UUID | FOREIGN KEY → patients | Patient |
| provider_id | UUID | FOREIGN KEY → providers | Provider |
| appointment_date | DATE | NOT NULL | Appointment date |
| appointment_time | TIME | NOT NULL | Appointment time |
| duration_minutes | INTEGER | NOT NULL | Duration |
| appointment_type | VARCHAR(50) | | Appointment type |
| appointment_source | VARCHAR(30) | | Portal/Phone/API |
| reason | TEXT | | Visit reason |
| location | VARCHAR(100) | | Clinic/Room |
| telehealth_link | TEXT | | Virtual visit link |
| status | VARCHAR(20) | NOT NULL | Appointment status |
| status_reason | TEXT | | Status reason |
| confirmation_date | TIMESTAMP | | Confirmation time |
| reminder_sent | BOOLEAN | DEFAULT FALSE | Reminder sent |
| checked_in_by | UUID | FOREIGN KEY → users | Front desk user |
| cancellation_reason | TEXT | | Cancellation reason |
| no_show_reason | TEXT | | No-show reason |
| notes | TEXT | | Notes |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | Deleted by user |

**Indexes:** patient_id, provider_id, appointment_date, status, tenant_id

---

### Table 14: encounters
**Purpose:** Store patient encounter records

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| encounter_id | UUID | PRIMARY KEY | Encounter identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| patient_id | UUID | FOREIGN KEY → patients | Patient |
| provider_id | UUID | FOREIGN KEY → providers | Rendering provider |
| appointment_id | UUID | FOREIGN KEY → appointments | Linked appointment |
| encounter_type | VARCHAR(50) | NOT NULL | Office/Inpatient/ER |
| encounter_date | DATE | NOT NULL | Encounter date |
| check_in_time | TIMESTAMP | | Check-in time |
| check_out_time | TIMESTAMP | | Check-out time |
| total_visit_minutes | INTEGER | | Visit duration |
| department | VARCHAR(50) | | Department |
| facility_location | VARCHAR(100) | | Facility |
| place_of_service | VARCHAR(2) | | POS code |
| chief_complaint | TEXT | | Chief complaint |
| attending_provider_id | UUID | FOREIGN KEY → providers | Attending provider |
| admitting_provider_id | UUID | FOREIGN KEY → providers | Admitting provider |
| discharge_provider_id | UUID | FOREIGN KEY → providers | Discharge provider |
| referring_provider_id | UUID | FOREIGN KEY → providers | Referring provider |
| status | VARCHAR(20) | NOT NULL | Encounter status |
| medical_record_signed | BOOLEAN | DEFAULT FALSE | Signed documentation |
| signed_by | UUID | FOREIGN KEY → users | Signed by provider |
| admission_date | DATE | | Admission date |
| discharge_date | DATE | | Discharge date |
| discharge_disposition | VARCHAR(50) | | Disposition |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | Deleted by user |

**Indexes:** patient_id, provider_id, encounter_date, status, tenant_id

---

### Table 15: encounter_diagnoses
**Purpose:** Store encounter diagnoses

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| diagnosis_id | UUID | PRIMARY KEY | Diagnosis identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| encounter_id | UUID | FOREIGN KEY → encounters | Encounter |
| icd10_code | VARCHAR(10) | NOT NULL | ICD-10 code |
| diagnosis_version | VARCHAR(10) | | ICD version |
| description | VARCHAR(255) | | Diagnosis description |
| diagnosis_type | VARCHAR(30) | | Primary/Secondary |
| present_on_admission | BOOLEAN | | POA indicator |
| is_principal | BOOLEAN | DEFAULT FALSE | Principal diagnosis |
| sequence | INTEGER | | Sequence |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes:** encounter_id, icd10_code, tenant_id

---

### Table 16: encounter_procedures
**Purpose:** Store encounter procedures

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| procedure_id | UUID | PRIMARY KEY | Procedure identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| encounter_id | UUID | FOREIGN KEY → encounters | Encounter |
| cpt_code | VARCHAR(10) | NOT NULL | CPT/HCPCS code |
| procedure_status | VARCHAR(30) | | Pending/Completed |
| description | VARCHAR(255) | | Procedure description |
| modifier1 | VARCHAR(2) | | Modifier 1 |
| modifier2 | VARCHAR(2) | | Modifier 2 |
| modifier3 | VARCHAR(2) | | Modifier 3 |
| modifier4 | VARCHAR(2) | | Modifier 4 |
| performing_provider_id | UUID | FOREIGN KEY → providers | Performing provider |
| units | INTEGER | DEFAULT 1 | Units |
| diagnosis_pointers | TEXT[] | | Linked diagnoses |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes:** encounter_id, cpt_code, tenant_id

---

### Table 17: charges
**Purpose:** Store billable charges

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| charge_id | UUID | PRIMARY KEY | Charge identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| encounter_id | UUID | FOREIGN KEY → encounters | Encounter |
| patient_id | UUID | FOREIGN KEY → patients | Patient |
| provider_id | UUID | FOREIGN KEY → providers | Provider |
| service_date | DATE | NOT NULL | Service date |
| cdm_id | UUID | FOREIGN KEY → chargemaster | CDM reference |
| cpt_code | VARCHAR(10) | NOT NULL | CPT/HCPCS code |
| charge_source | VARCHAR(30) | | Manual/System |
| description | VARCHAR(255) | | Charge description |
| modifier1 | VARCHAR(2) | | Modifier 1 |
| modifier2 | VARCHAR(2) | | Modifier 2 |
| modifier3 | VARCHAR(2) | | Modifier 3 |
| modifier4 | VARCHAR(2) | | Modifier 4 |
| units | INTEGER | DEFAULT 1 | Quantity |
| charge_amount | DECIMAL(10,2) | NOT NULL | Charge amount |
| expected_allowed_amount | DECIMAL(10,2) | | Expected reimbursement |
| revenue_code | VARCHAR(4) | | Revenue code |
| department | VARCHAR(50) | | Department |
| status | VARCHAR(20) | NOT NULL | Charge status |
| hold_reason | TEXT | | Hold reason |
| billing_ready | BOOLEAN | DEFAULT FALSE | Billing readiness |
| entered_by | UUID | FOREIGN KEY → users | Entered by user |
| entered_date | TIMESTAMP | DEFAULT NOW() | Entry date |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | Deleted by user |

**Indexes:** encounter_id, patient_id, service_date, status, tenant_id

---

### Table 18: claims
**Purpose:** Store insurance claims

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| claim_id | UUID | PRIMARY KEY | Claim identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| encounter_id | UUID | FOREIGN KEY → encounters | Encounter |
| patient_id | UUID | FOREIGN KEY → patients | Patient |
| insurance_id | UUID | FOREIGN KEY → patient_insurance | Insurance |
| payer_id | UUID | FOREIGN KEY → payers | Payer |
| provider_id | UUID | FOREIGN KEY → providers | Rendering provider |
| claim_number | VARCHAR(50) | UNIQUE | Internal claim number |
| claim_type | VARCHAR(10) | NOT NULL | CMS-1500, UB-04 |
| claim_frequency | VARCHAR(1) | DEFAULT '1' | Original/Corrected/Void |
| original_claim_number | VARCHAR(50) | | Original claim number |
| billing_provider_npi | VARCHAR(10) | NOT NULL | Billing provider NPI |
| rendering_provider_npi | VARCHAR(10) | NOT NULL | Rendering provider NPI |
| referring_provider_npi | VARCHAR(10) | | Referring provider NPI |
| service_date_from | DATE | NOT NULL | Service date from |
| service_date_to | DATE | NOT NULL | Service date to |
| total_charge_amount | DECIMAL(10,2) | NOT NULL | Total billed amount |
| authorization_number | VARCHAR(50) | | Prior authorization |
| status | VARCHAR(20) | NOT NULL | Claim status |
| status_reason | TEXT | | Status reason |
| status_updated_at | TIMESTAMP | | Status update timestamp |
| is_clean_claim | BOOLEAN | DEFAULT FALSE | Passed scrubbing |
| submission_date | DATE | | Submission date |
| submission_method | VARCHAR(20) | | Electronic/Paper |
| clearinghouse_id | VARCHAR(50) | | Clearinghouse tracking ID |
| payer_claim_number | VARCHAR(50) | | Payer ICN |
| timely_filing_deadline | DATE | | Filing deadline |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | Deleted by user |

**Indexes:** claim_number, patient_id, payer_id, status, submission_date, tenant_id

---

### Table 19: claim_lines
**Purpose:** Store individual claim service line items

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| line_id | UUID | PRIMARY KEY | Claim line identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| claim_id | UUID | FOREIGN KEY → claims | Related claim |
| charge_id | UUID | FOREIGN KEY → charges | Related charge |
| line_number | INTEGER | NOT NULL | Claim line sequence number |
| service_date | DATE | NOT NULL | Date of service |
| place_of_service | VARCHAR(2) | | POS code |
| cpt_code | VARCHAR(10) | NOT NULL | CPT/HCPCS code |
| hcpcs_code | VARCHAR(10) | | HCPCS code |
| line_status | VARCHAR(30) | | Pending/Billed/Paid/Denied |
| line_status_reason | TEXT | | Status reason |
| modifier1 | VARCHAR(2) | | Modifier 1 |
| modifier2 | VARCHAR(2) | | Modifier 2 |
| modifier3 | VARCHAR(2) | | Modifier 3 |
| modifier4 | VARCHAR(2) | | Modifier 4 |
| diagnosis_pointers | TEXT[] | | Linked diagnosis pointers |
| rendering_provider_id | UUID | FOREIGN KEY → providers | Rendering provider |
| units | INTEGER | DEFAULT 1 | Units |
| billed_amount | DECIMAL(10,2) | NOT NULL | Billed amount |
| expected_allowed_amount | DECIMAL(10,2) | | Expected allowed amount |
| expected_patient_responsibility | DECIMAL(10,2) | | Expected patient responsibility |
| revenue_code | VARCHAR(4) | | Revenue code |
| authorization_number | VARCHAR(50) | | Prior authorization number |
| ndc_code | VARCHAR(20) | | National drug code |
| drug_quantity | DECIMAL(10,2) | | Drug quantity |
| drug_unit_measure | VARCHAR(20) | | Drug unit measure |
| is_emergency_service | BOOLEAN | DEFAULT FALSE | Emergency service indicator |
| claim_line_notes | TEXT | | Internal claim line notes |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | Deleted by user |

**Indexes:** claim_id, charge_id, cpt_code, service_date, line_status, tenant_id

---

### Table 20: claim_scrubbing_errors
**Purpose:** Store claim scrubbing and validation errors

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| error_id | UUID | PRIMARY KEY | Scrubbing error identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| claim_id | UUID | FOREIGN KEY → claims | Related claim |
| claim_line_id | UUID | FOREIGN KEY → claim_lines | Related claim line |
| scrub_rule_id | VARCHAR(50) | | Internal scrub rule identifier |
| error_level | VARCHAR(10) | NOT NULL | Fatal, Warning, Info |
| error_category | VARCHAR(50) | | Coding, Eligibility, Authorization |
| error_code | VARCHAR(20) | | Error code |
| external_error_code | VARCHAR(50) | | Clearinghouse/payer code |
| error_message | TEXT | NOT NULL | Error description |
| field_name | VARCHAR(50) | | Field with validation issue |
| field_value | TEXT | | Invalid field value |
| suggested_fix | TEXT | | Suggested correction |
| auto_corrected | BOOLEAN | DEFAULT FALSE | Auto-corrected indicator |
| corrected_value | TEXT | | Auto-corrected value |
| resolution_notes | TEXT | | Resolution notes |
| resolved | BOOLEAN | DEFAULT FALSE | Resolved flag |
| resolved_by | UUID | FOREIGN KEY → users | User who resolved issue |
| resolved_at | TIMESTAMP | | Resolution timestamp |
| assigned_to | UUID | FOREIGN KEY → users | Assigned user |
| retry_count | INTEGER | DEFAULT 0 | Resubmission attempts |
| source_system | VARCHAR(50) | | Internal/Clearinghouse |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |

**Indexes:** claim_id, claim_line_id, error_level, error_category, resolved, assigned_to, tenant_id

---

### Table 21: payments
**Purpose:** Store all payments (insurance and patient)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| payment_id | UUID | PRIMARY KEY | Payment identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| claim_id | UUID | FOREIGN KEY → claims | Claim paid |
| patient_id | UUID | FOREIGN KEY → patients | Patient |
| payer_id | UUID | FOREIGN KEY → payers | Payer |
| payment_type | VARCHAR(20) | NOT NULL | Insurance/Patient |
| payment_method | VARCHAR(20) | | EFT, ACH, Check |
| payment_reference_number | VARCHAR(100) | | EFT/check reference |
| payment_date | DATE | NOT NULL | Payment date |
| check_number | VARCHAR(50) | | Check number |
| payment_amount | DECIMAL(10,2) | NOT NULL | Total payment amount |
| deposit_batch_id | UUID | FOREIGN KEY → bank_deposits | Bank deposit batch |
| reconciliation_status | VARCHAR(30) | | Pending/Matched |
| era_file_id | UUID | FOREIGN KEY → era_files | ERA reference |
| posted_by | UUID | FOREIGN KEY → users | Posted by user |
| posted_date | TIMESTAMP | DEFAULT NOW() | Posting timestamp |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | Deleted by user |

**Indexes:** claim_id, patient_id, payer_id, payment_date, reconciliation_status

---

### Table 22: payment_line_items (Final Enterprise Version)
**Purpose:** Store line-level payment posting and reimbursement details

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| line_item_id | UUID | PRIMARY KEY | Payment line item identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| payment_id | UUID | FOREIGN KEY → payments | Related payment |
| claim_line_id | UUID | FOREIGN KEY → claim_lines | Related claim line |
| payer_id | UUID | FOREIGN KEY → payers | Insurance payer |
| patient_id | UUID | FOREIGN KEY → patients | Patient |
| payment_posting_batch_id | UUID | FOREIGN KEY → reconciliation_batches | Posting batch reference |
| billed_amount | DECIMAL(10,2) | NOT NULL | Billed amount |
| allowed_amount | DECIMAL(10,2) | NOT NULL | Allowed reimbursement amount |
| expected_allowed_amount | DECIMAL(10,2) | | Expected reimbursement |
| paid_amount | DECIMAL(10,2) | NOT NULL | Paid amount |
| expected_paid_amount | DECIMAL(10,2) | | Expected paid amount |
| payment_variance_amount | DECIMAL(10,2) | | Variance amount |
| variance_reason | TEXT | | Variance explanation |
| deductible | DECIMAL(10,2) | DEFAULT 0 | Deductible applied |
| copay | DECIMAL(10,2) | DEFAULT 0 | Copay applied |
| coinsurance | DECIMAL(10,2) | DEFAULT 0 | Coinsurance amount |
| patient_responsibility | DECIMAL(10,2) | DEFAULT 0 | Patient balance responsibility |
| contractual_adjustment | DECIMAL(10,2) | DEFAULT 0 | Contractual write-off |
| non_contractual_adjustment | DECIMAL(10,2) | DEFAULT 0 | Non-contractual adjustment |
| sequestration_adjustment | DECIMAL(10,2) | DEFAULT 0 | Medicare sequestration adjustment |
| adjustment_code | VARCHAR(10) | | CARC code |
| adjustment_group_code | VARCHAR(5) | | PR, CO, OA, PI |
| adjustment_reason | TEXT | | Adjustment explanation |
| remark_code | VARCHAR(10) | | RARC code |
| denial_code | VARCHAR(10) | | Denial CARC code |
| denial_reason | TEXT | | Denial explanation |
| underpayment_flag | BOOLEAN | DEFAULT FALSE | Underpayment detected |
| overpayment_flag | BOOLEAN | DEFAULT FALSE | Overpayment detected |
| reimbursement_status | VARCHAR(30) | | Paid/Partial/Denied |
| posting_status | VARCHAR(30) | | Posted/Pending/Reversed |
| posting_notes | TEXT | | Payment posting notes |
| service_date | DATE | | Related service date |
| payment_effective_date | DATE | | Effective payment date |
| reversal_flag | BOOLEAN | DEFAULT FALSE | Reversal indicator |
| reversal_reason | TEXT | | Reversal explanation |
| posted_by | UUID | FOREIGN KEY → users | User who posted payment |
| reviewed_by | UUID | FOREIGN KEY → users | User who reviewed posting |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | Deleted by user |

**Indexes:** payment_id, claim_line_id, payer_id, patient_id, reimbursement_status, posting_status, denial_code, adjustment_code, tenant_id

---

### Table 23: era_files
**Purpose:** Store ERA (EDI 835) files

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| era_file_id | UUID | PRIMARY KEY | ERA identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| payer_id | UUID | FOREIGN KEY → payers | Payer |
| file_name | VARCHAR(255) | | ERA file name |
| storage_path | TEXT | | S3/blob storage path |
| file_size_kb | INTEGER | | File size |
| check_number | VARCHAR(50) | | Check number |
| check_date | DATE | | Check date |
| total_amount | DECIMAL(10,2) | | Total ERA amount |
| claim_count | INTEGER | | Claim count |
| auto_posted_count | INTEGER | DEFAULT 0 | Auto posted claims |
| manual_posted_count | INTEGER | DEFAULT 0 | Manual posted claims |
| processing_start_time | TIMESTAMP | | Processing start |
| processing_end_time | TIMESTAMP | | Processing end |
| processing_errors | TEXT | | Processing errors |
| status | VARCHAR(20) | NOT NULL | Processing status |
| imported_by | UUID | FOREIGN KEY → users | Imported by user |
| imported_date | TIMESTAMP | DEFAULT NOW() | Import timestamp |

**Indexes:** payer_id, check_number, check_date, status

---

### Table 24: Denials
**Purpose:** Track denied claims and denial management workflow

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| denial_id | UUID | PRIMARY KEY | Denial identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| claim_id | UUID | FOREIGN KEY → claims | Related claim |
| claim_line_id | UUID | FOREIGN KEY → claim_lines | Related claim line |
| patient_id | UUID | FOREIGN KEY → patients | Patient |
| payer_id | UUID | FOREIGN KEY → payers | Insurance payer |
| denial_date | DATE | NOT NULL | Denial date |
| denial_code | VARCHAR(10) | | CARC denial code |
| denial_group_code | VARCHAR(5) | | PR, CO, OA, PI |
| denial_reason | TEXT | NOT NULL | Denial explanation |
| denial_category | VARCHAR(50) | | Clinical, Authorization |
| denial_subcategory | VARCHAR(100) | | Detailed denial type |
| denial_source | VARCHAR(30) | | Clearinghouse/Payer |
| denial_amount | DECIMAL(10,2) | NOT NULL | Denied amount |
| expected_reimbursement | DECIMAL(10,2) | | Expected reimbursement |
| root_cause | TEXT | | Root cause analysis |
| prevention_strategy | TEXT | | Future prevention notes |
| is_appealable | BOOLEAN | DEFAULT TRUE | Appeal eligible |
| appeal_deadline | DATE | | Appeal due date |
| filing_deadline | DATE | | Timely filing limit |
| denial_priority | VARCHAR(20) | | High/Medium/Low |
| status | VARCHAR(20) | NOT NULL | New/Appealed/Resolved |
| status_reason | TEXT | | Status explanation |
| assigned_to | UUID | FOREIGN KEY → users | Assigned AR user |
| assigned_date | TIMESTAMP | | Assignment timestamp |
| worked_date | TIMESTAMP | | Last worked timestamp |
| next_followup_date | DATE | | Follow-up date |
| resolution_notes | TEXT | | Resolution notes |
| resolved_by | UUID | FOREIGN KEY → users | Resolved by user |
| resolved_at | TIMESTAMP | | Resolution timestamp |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | Deleted by user |

**Indexes:** claim_id, denial_code, denial_category, status, assigned_to, appeal_deadline, tenant_id

---

### Table 25: appeals
**Purpose:** Track denial appeals and appeal workflow management

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| appeal_id | UUID | PRIMARY KEY | Appeal identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| denial_id | UUID | FOREIGN KEY → denials | Related denial |
| claim_id | UUID | FOREIGN KEY → claims | Related claim |
| patient_id | UUID | FOREIGN KEY → patients | Patient |
| payer_id | UUID | FOREIGN KEY → payers | Insurance payer |
| appeal_level | INTEGER | NOT NULL | 1st, 2nd, 3rd level |
| appeal_type | VARCHAR(50) | | Clinical/Technical/Billing |
| appeal_method | VARCHAR(20) | | Portal/Fax/Mail |
| appeal_date | DATE | NOT NULL | Appeal submission date |
| appeal_deadline | DATE | | Appeal due date |
| appeal_letter | TEXT | | Appeal content |
| supporting_documents | TEXT[] | | Supporting documents |
| medical_records_attached | BOOLEAN | DEFAULT FALSE | Medical records attached |
| corrected_claim_submitted | BOOLEAN | DEFAULT FALSE | Corrected claim sent |
| status | VARCHAR(20) | NOT NULL | Submitted/Approved/Denied |
| status_reason | TEXT | | Status explanation |
| payer_reference_number | VARCHAR(100) | | Payer reference |
| outcome_date | DATE | | Outcome date |
| additional_payment | DECIMAL(10,2) | DEFAULT 0 | Additional reimbursement |
| expected_recovery_amount | DECIMAL(10,2) | | Expected recovery |
| appeal_outcome_category | VARCHAR(50) | | Fully approved/Partial |
| outcome_notes | TEXT | | Outcome explanation |
| assigned_to | UUID | FOREIGN KEY → users | Assigned user |
| submitted_by | UUID | FOREIGN KEY → users | Submitted by user |
| reviewed_by | UUID | FOREIGN KEY → users | Reviewed by user |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | Deleted by user |

**Indexes:** denial_id, claim_id, appeal_date, status, assigned_to, tenant_id

---

### Table 26: patient_statements
**Purpose:** Track patient billing statements and statement delivery

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| statement_id | UUID | PRIMARY KEY | Statement identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| patient_id | UUID | FOREIGN KEY → patients | Patient |
| guarantor_id | UUID | FOREIGN KEY → guarantors | Responsible party |
| statement_number | VARCHAR(50) | UNIQUE | Statement number |
| statement_cycle | VARCHAR(20) | | Monthly/Biweekly |
| statement_date | DATE | NOT NULL | Statement date |
| previous_balance | DECIMAL(10,2) | DEFAULT 0 | Previous balance |
| new_charges | DECIMAL(10,2) | DEFAULT 0 | New charges |
| payments_received | DECIMAL(10,2) | DEFAULT 0 | Payments received |
| adjustments | DECIMAL(10,2) | DEFAULT 0 | Adjustments |
| interest_charges | DECIMAL(10,2) | DEFAULT 0 | Interest/late fees |
| current_balance | DECIMAL(10,2) | NOT NULL | Current balance |
| minimum_due_amount | DECIMAL(10,2) | | Minimum payment due |
| due_date | DATE | | Payment due date |
| delivery_method | VARCHAR(20) | | Mail/Email/Portal |
| delivery_status | VARCHAR(20) | | Pending/Sent/Failed |
| sent_date | DATE | | Statement sent date |
| viewed_in_portal | BOOLEAN | DEFAULT FALSE | Portal viewed flag |
| viewed_date | TIMESTAMP | | Viewed timestamp |
| pdf_url | TEXT | | PDF storage URL |
| statement_notes | TEXT | | Internal notes |
| generated_by | UUID | FOREIGN KEY → users | Generated by user |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |

**Indexes:** patient_id, statement_date, statement_number, delivery_status, tenant_id

---

### Table 27: patient_payments
**Purpose:** Track patient payments and payment processing

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| patient_payment_id | UUID | PRIMARY KEY | Patient payment identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| patient_id | UUID | FOREIGN KEY → patients | Patient |
| guarantor_id | UUID | FOREIGN KEY → guarantors | Responsible guarantor |
| statement_id | UUID | FOREIGN KEY → patient_statements | Related statement |
| payment_plan_id | UUID | FOREIGN KEY → payment_plans | Payment plan reference |
| payment_date | DATE | NOT NULL | Payment date |
| payment_amount | DECIMAL(10,2) | NOT NULL | Payment amount |
| payment_method | VARCHAR(20) | NOT NULL | Card/ACH/Cash |
| payment_source | VARCHAR(30) | | Portal/Front Desk |
| transaction_id | VARCHAR(100) | | Payment transaction ID |
| authorization_code | VARCHAR(100) | | Gateway authorization |
| check_number | VARCHAR(50) | | Check number |
| card_last_four_digits | VARCHAR(4) | | Last four digits |
| payment_gateway | VARCHAR(50) | | Stripe/Authorize.Net |
| payment_status | VARCHAR(30) | | Pending/Completed/Failed |
| reconciliation_status | VARCHAR(30) | | Matched/Pending |
| refund_flag | BOOLEAN | DEFAULT FALSE | Refunded indicator |
| refund_amount | DECIMAL(10,2) | DEFAULT 0 | Refunded amount |
| refund_reason | TEXT | | Refund explanation |
| posting_notes | TEXT | | Posting notes |
| received_by | UUID | FOREIGN KEY → users | Received by user |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | Deleted by user |

**Indexes:** patient_id, payment_date, payment_status, transaction_id, tenant_id

---

### Table 28: payment_plans
**Purpose:** Track patient payment plans and installment schedules

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| plan_id | UUID | PRIMARY KEY | Payment plan identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| patient_id | UUID | FOREIGN KEY → patients | Patient |
| guarantor_id | UUID | FOREIGN KEY → guarantors | Responsible guarantor |
| total_amount | DECIMAL(10,2) | NOT NULL | Total balance |
| down_payment_amount | DECIMAL(10,2) | DEFAULT 0 | Initial payment |
| remaining_balance | DECIMAL(10,2) | | Remaining balance |
| monthly_payment | DECIMAL(10,2) | NOT NULL | Monthly installment |
| installment_frequency | VARCHAR(20) | | Monthly/Biweekly |
| number_of_installments | INTEGER | | Total installments |
| completed_installments | INTEGER | DEFAULT 0 | Completed installments |
| missed_payments_count | INTEGER | DEFAULT 0 | Missed payment count |
| start_date | DATE | NOT NULL | Start date |
| end_date | DATE | NOT NULL | End date |
| next_payment_date | DATE | | Upcoming payment |
| interest_rate | DECIMAL(5,2) | DEFAULT 0 | Interest rate |
| auto_pay_enabled | BOOLEAN | DEFAULT FALSE | Auto payment enabled |
| auto_pay_method | VARCHAR(20) | | ACH/Card |
| status | VARCHAR(20) | NOT NULL | Active/Completed |
| status_reason | TEXT | | Status explanation |
| agreement_document_url | TEXT | | Signed agreement |
| defaulted_date | DATE | | Default date |
| notes | TEXT | | Internal notes |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |

**Indexes:** patient_id, status, next_payment_date, tenant_id

---

### Table 29: collections
**Purpose:** Track patient balances sent to collections

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| collection_id | UUID | PRIMARY KEY | Collection identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| patient_id | UUID | FOREIGN KEY → patients | Patient |
| guarantor_id | UUID | FOREIGN KEY → guarantors | Responsible guarantor |
| statement_id | UUID | FOREIGN KEY → patient_statements | Related statement |
| original_balance | DECIMAL(10,2) | NOT NULL | Original balance |
| current_balance | DECIMAL(10,2) | NOT NULL | Current balance |
| collection_status | VARCHAR(20) | NOT NULL | Internal/External/Bad Debt |
| collection_stage | VARCHAR(30) | | Pre-collection/Agency |
| sent_to_collections_date | DATE | | Sent date |
| collection_agency | VARCHAR(100) | | Agency name |
| agency_account_number | VARCHAR(100) | | Agency reference |
| agency_fee_pct | DECIMAL(5,2) | | Agency commission |
| last_collection_activity_date | DATE | | Last activity |
| next_followup_date | DATE | | Follow-up date |
| payment_arrangement_flag | BOOLEAN | DEFAULT FALSE | Payment arrangement |
| settlement_offer_amount | DECIMAL(10,2) | | Settlement offer |
| settlement_expiration_date | DATE | | Settlement expiration |
| bankruptcy_flag | BOOLEAN | DEFAULT FALSE | Bankruptcy indicator |
| legal_action_flag | BOOLEAN | DEFAULT FALSE | Legal action initiated |
| write_off_flag | BOOLEAN | DEFAULT FALSE | Written off indicator |
| notes | TEXT | | Collection notes |
| assigned_to | UUID | FOREIGN KEY → users | Assigned collector |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |

**Indexes:** patient_id, collection_status, collection_agency, next_followup_date, tenant_id

---

### Table 30: refunds (Final Enterprise Version)
**Purpose:** Track insurance and patient refunds

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| refund_id | UUID | PRIMARY KEY | Refund identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| patient_id | UUID | FOREIGN KEY → patients | Patient |
| payer_id | UUID | FOREIGN KEY → payers | Insurance payer |
| original_payment_id | UUID | FOREIGN KEY → payments | Original payment |
| patient_payment_id | UUID | FOREIGN KEY → patient_payments | Patient payment |
| refund_type | VARCHAR(30) | | Patient/Payer |
| refund_reason | TEXT | NOT NULL | Refund reason |
| refund_category | VARCHAR(50) | | Overpayment/Duplicate |
| refund_amount | DECIMAL(10,2) | NOT NULL | Refund amount |
| refund_method | VARCHAR(20) | | Check/ACH/Reversal |
| refund_status | VARCHAR(30) | | Pending/Processed |
| refund_reference_number | VARCHAR(100) | | Refund transaction reference |
| check_number | VARCHAR(50) | | Refund check number |
| bank_transaction_id | VARCHAR(100) | | ACH reference |
| approval_required | BOOLEAN | DEFAULT FALSE | Requires approval |
| approved_by | UUID | FOREIGN KEY → users | Approved by user |
| approved_at | TIMESTAMP | | Approval timestamp |
| refund_date | DATE | NOT NULL | Refund issued date |
| posting_notes | TEXT | | Refund notes |
| reconciliation_status | VARCHAR(30) | | Matched/Pending |
| issued_by | UUID | FOREIGN KEY → users | Issued by user |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | Deleted by user |

**Indexes:** patient_id, payer_id, refund_date, refund_status, reconciliation_status, tenant_id

---

### Table 31: audit_logs
**Purpose:** Comprehensive audit trail (HIPAA compliance)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| log_id | UUID | PRIMARY KEY | Audit log identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| user_id | UUID | FOREIGN KEY → users | User performing action |
| action_type | VARCHAR(50) | NOT NULL | Create/Update/Delete/Login |
| module_name | VARCHAR(100) | | Application module |
| table_name | VARCHAR(50) | | Affected table |
| record_id | UUID | | Affected record |
| patient_id | UUID | FOREIGN KEY → patients | Patient involved |
| before_value | JSONB | | Before data |
| after_value | JSONB | | After data |
| ip_address | VARCHAR(50) | | IP address |
| device_info | TEXT | | Device/browser info |
| session_id | VARCHAR(255) | | Session identifier |
| action_status | VARCHAR(20) | | Success/Failed |
| timestamp | TIMESTAMP | DEFAULT NOW() | Audit timestamp |

**Indexes:** user_id, patient_id, action_type, timestamp, tenant_id

---

### Table 32: code_sets
**Purpose:** Store standardized medical coding systems (ICD, CPT, HCPCS, Revenue Codes)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| code_set_id | UUID | PRIMARY KEY | Code set identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| code_type | VARCHAR(20) | NOT NULL | ICD10, CPT, HCPCS, REVCODE |
| code | VARCHAR(20) | NOT NULL | Medical code |
| short_description | VARCHAR(255) | | Short description |
| long_description | TEXT | | Full description |
| code_category | VARCHAR(100) | | Category classification |
| specialty | VARCHAR(100) | | Medical specialty |
| gender_specific | VARCHAR(20) | | Male/Female/Both |
| minimum_age | INTEGER | | Minimum patient age |
| maximum_age | INTEGER | | Maximum patient age |
| requires_authorization | BOOLEAN | DEFAULT FALSE | Prior auth required |
| requires_medical_necessity | BOOLEAN | DEFAULT FALSE | Medical necessity required |
| billable_flag | BOOLEAN | DEFAULT TRUE | Billable code indicator |
| global_period_days | INTEGER | | Surgical global period |
| relative_value_unit | DECIMAL(10,2) | | RVU value |
| modifier_allowed | BOOLEAN | DEFAULT TRUE | Modifier allowed |
| effective_date | DATE | NOT NULL | Effective date |
| termination_date | DATE | | Termination date |
| annual_update_version | VARCHAR(20) | | CMS annual version |
| status | VARCHAR(20) | | Active/Inactive |
| source_authority | VARCHAR(50) | | CMS/AMA |
| notes | TEXT | | Internal notes |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | Deleted by user |

**Indexes:** code_type, code, specialty, status, effective_date, tenant_id

---

### Table 33: ncci_edits
**Purpose:** Store National Correct Coding Initiative (NCCI) edit rules

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ncci_edit_id | UUID | PRIMARY KEY | NCCI edit identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| primary_cpt_code | VARCHAR(10) | NOT NULL | Primary CPT code |
| secondary_cpt_code | VARCHAR(10) | NOT NULL | Secondary CPT code |
| edit_type | VARCHAR(30) | | Mutually Exclusive/Column1/Column2 |
| modifier_indicator | VARCHAR(5) | | Modifier indicator |
| modifier_override_allowed | BOOLEAN | DEFAULT FALSE | Override allowed |
| edit_description | TEXT | | Edit explanation |
| denial_message | TEXT | | Claim denial explanation |
| cms_reference | VARCHAR(100) | | CMS reference |
| effective_date | DATE | NOT NULL | Effective date |
| termination_date | DATE | | End date |
| severity_level | VARCHAR(20) | | Fatal/Warning |
| auto_scrub_enabled | BOOLEAN | DEFAULT TRUE | Auto scrub rule |
| override_reason_required | BOOLEAN | DEFAULT FALSE | Override reason required |
| override_approval_required | BOOLEAN | DEFAULT FALSE | Approval required |
| frequency_limit | INTEGER | | Frequency limit |
| specialty_restriction | VARCHAR(100) | | Specialty restriction |
| status | VARCHAR(20) | | Active/Inactive |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |

**Indexes:** primary_cpt_code, secondary_cpt_code, effective_date, severity_level, tenant_id

---

### Table 34: lcd_ncd_rules
**Purpose:** Store Local Coverage Determination (LCD) and National Coverage Determination (NCD) rules

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| rule_id | UUID | PRIMARY KEY | LCD/NCD rule identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| rule_type | VARCHAR(10) | NOT NULL | LCD/NCD |
| rule_number | VARCHAR(50) | | CMS rule number |
| payer_id | UUID | FOREIGN KEY → payers | Related payer |
| cpt_code | VARCHAR(10) | | CPT/HCPCS code |
| icd10_code | VARCHAR(10) | | ICD-10 diagnosis code |
| medical_necessity_criteria | TEXT | | Medical necessity requirements |
| frequency_limit | INTEGER | | Frequency limitation |
| age_restriction_min | INTEGER | | Minimum age |
| age_restriction_max | INTEGER | | Maximum age |
| gender_restriction | VARCHAR(20) | | Male/Female/Both |
| place_of_service | VARCHAR(2) | | POS restriction |
| authorization_required | BOOLEAN | DEFAULT FALSE | Prior auth required |
| documentation_required | BOOLEAN | DEFAULT FALSE | Additional documentation |
| denial_message | TEXT | | Denial explanation |
| cms_reference_url | TEXT | | CMS reference URL |
| effective_date | DATE | NOT NULL | Effective date |
| termination_date | DATE | | Termination date |
| status | VARCHAR(20) | | Active/Inactive |
| auto_validation_enabled | BOOLEAN | DEFAULT TRUE | Automatic validation |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |

**Indexes:** cpt_code, icd10_code, payer_id, rule_type, effective_date, tenant_id

---

### Table 35: reports
**Purpose:** Store generated reports, report configurations, and analytics exports

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| report_id | UUID | PRIMARY KEY | Report identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| report_name | VARCHAR(100) | NOT NULL | Report name |
| report_category | VARCHAR(50) | | Financial/Operational |
| report_type | VARCHAR(50) | | Dashboard/PDF/Excel |
| report_description | TEXT | | Report description |
| generated_by | UUID | FOREIGN KEY → users | Generated by user |
| report_parameters | JSONB | | Report filters/parameters |
| date_range_from | DATE | | Report start date |
| date_range_to | DATE | | Report end date |
| generation_start_time | TIMESTAMP | | Generation start |
| generation_end_time | TIMESTAMP | | Generation completion |
| execution_time_ms | INTEGER | | Execution duration |
| row_count | INTEGER | | Number of rows |
| file_format | VARCHAR(20) | | PDF/XLSX/CSV |
| file_size_kb | INTEGER | | Report file size |
| storage_path | TEXT | | File storage location |
| report_status | VARCHAR(20) | | Processing/Completed/Failed |
| scheduled_report | BOOLEAN | DEFAULT FALSE | Scheduled report flag |
| schedule_frequency | VARCHAR(20) | | Daily/Weekly/Monthly |
| next_run_date | TIMESTAMP | | Next execution |
| email_distribution_list | TEXT[] | | Distribution emails |
| access_level | VARCHAR(30) | | Public/Restricted |
| contains_phi | BOOLEAN | DEFAULT TRUE | PHI data indicator |
| encryption_enabled | BOOLEAN | DEFAULT TRUE | File encryption |
| download_count | INTEGER | DEFAULT 0 | Download count |
| last_downloaded_at | TIMESTAMP | | Last download |
| retention_expiration_date | DATE | | Report retention |
| created_by | UUID | FOREIGN KEY → users | Created by user |
| updated_by | UUID | FOREIGN KEY → users | Updated by user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update timestamp |
| deleted_at | TIMESTAMP | | Soft delete timestamp |
| deleted_by | UUID | FOREIGN KEY → users | Deleted by user |

**Indexes:** report_name, report_category, generated_by, report_status, scheduled_report, tenant_id

---

### Table 36: tenant_organizations
**Purpose:** Store multi-tenant organizations (hospitals, clinics, billing companies)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| tenant_id | UUID | PRIMARY KEY | Unique tenant identifier |
| organization_code | VARCHAR(50) | UNIQUE | Internal organization code |
| organization_name | VARCHAR(150) | NOT NULL | Organization name |
| organization_type | VARCHAR(50) | | Hospital/Clinic/Billing Company |
| tax_id | VARCHAR(20) | | EIN/Tax ID |
| npi_number | VARCHAR(20) | | Organization NPI |
| address_line1 | VARCHAR(100) | | Address |
| address_line2 | VARCHAR(100) | | Address line 2 |
| city | VARCHAR(50) | | City |
| state | VARCHAR(2) | | State |
| zip_code | VARCHAR(10) | | ZIP code |
| country | VARCHAR(50) | | Country |
| timezone | VARCHAR(50) | | Organization timezone |
| default_timezone | VARCHAR(50) | | Default timezone |
| phone | VARCHAR(20) | | Contact number |
| email | VARCHAR(100) | | Email |
| website_url | TEXT | | Organization website |
| logo_url | TEXT | | Branding logo |
| subscription_plan | VARCHAR(50) | | Basic/Enterprise |
| subscription_start_date | DATE | | Subscription start |
| subscription_end_date | DATE | | Subscription end |
| max_users_allowed | INTEGER | | License limit |
| hipaa_baa_signed | BOOLEAN | DEFAULT FALSE | HIPAA BAA signed |
| hipaa_baa_signed_date | DATE | | BAA signed date |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |
| created_by | UUID | FOREIGN KEY → users | Created by |
| updated_by | UUID | FOREIGN KEY → users | Updated by |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update |
| deleted_at | TIMESTAMP | | Soft delete |
| deleted_by | UUID | FOREIGN KEY → users | Deleted by |

**Indexes:** organization_name, organization_code, tax_id, is_active

---

### Table 37: clearinghouse_submissions
**Purpose:** Track claim submissions to clearinghouses

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| submission_id | UUID | PRIMARY KEY | Submission identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| claim_id | UUID | FOREIGN KEY → claims | Related claim |
| clearinghouse_name | VARCHAR(100) | NOT NULL | Clearinghouse name |
| batch_id | VARCHAR(100) | | Clearinghouse batch ID |
| submission_method | VARCHAR(20) | | API/SFTP |
| transmission_control_number | VARCHAR(100) | | EDI control number |
| transmission_date | TIMESTAMP | | Submission date |
| submission_status | VARCHAR(30) | | Submitted/Accepted/Rejected |
| acknowledgement_999_status | VARCHAR(30) | | 999 status |
| acknowledgement_277_status | VARCHAR(30) | | 277 status |
| claim_status_277ca | VARCHAR(30) | | 277CA claim status |
| resubmission_flag | BOOLEAN | DEFAULT FALSE | Resubmitted claim |
| resubmission_reason | TEXT | | Resubmission reason |
| rejection_reason | TEXT | | Rejection details |
| raw_response | JSONB | | Clearinghouse response |
| retry_count | INTEGER | DEFAULT 0 | Retry attempts |
| submitted_by | UUID | FOREIGN KEY → users | Submitted by |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update |

**Indexes:** claim_id, batch_id, submission_status, clearinghouse_name, tenant_id

---

### Table 38: edi_transactions
**Purpose:** Store inbound and outbound EDI transactions

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| transaction_id | UUID | PRIMARY KEY | Transaction identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| transaction_type | VARCHAR(10) | NOT NULL | 837/835/270/271 |
| direction | VARCHAR(10) | NOT NULL | Inbound/Outbound |
| clearinghouse_name | VARCHAR(100) | | Clearinghouse |
| related_claim_id | UUID | FOREIGN KEY → claims | Related claim |
| payer_id | UUID | FOREIGN KEY → payers | Payer |
| interchange_control_number | VARCHAR(100) | | ISA control number |
| functional_group_number | VARCHAR(100) | | GS control number |
| transaction_set_control_number | VARCHAR(100) | | ST control number |
| file_name | VARCHAR(255) | | EDI file name |
| storage_path | TEXT | | EDI file location |
| raw_edi_content_path | TEXT | | Raw EDI content |
| transaction_status | VARCHAR(30) | | Processing status |
| processed_date | TIMESTAMP | | Processed timestamp |
| retry_attempts | INTEGER | DEFAULT 0 | Retry count |
| error_message | TEXT | | Error details |
| processed_by | UUID | FOREIGN KEY → users | Processed by |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes:** transaction_type, transaction_status, payer_id, related_claim_id, tenant_id

---

### Table 39: claim_status_history
**Purpose:** Maintain claim lifecycle audit history

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| history_id | UUID | PRIMARY KEY | History identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| claim_id | UUID | FOREIGN KEY → claims | Related claim |
| workflow_stage | VARCHAR(50) | | Claim workflow stage |
| old_status | VARCHAR(30) | | Previous status |
| new_status | VARCHAR(30) | NOT NULL | Updated status |
| change_reason | TEXT | | Reason for status change |
| source_system | VARCHAR(50) | | Internal/Payer |
| automated_change | BOOLEAN | DEFAULT FALSE | Auto workflow update |
| external_reference_number | VARCHAR(100) | | External tracking |
| changed_by | UUID | FOREIGN KEY → users | Changed by user |
| changed_at | TIMESTAMP | DEFAULT NOW() | Change timestamp |
| notes | TEXT | | Workflow notes |

**Indexes:** claim_id, new_status, workflow_stage, changed_at, tenant_id

---

### Table 40: work_queues
**Purpose:** Manage operational RCM work queues

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| queue_id | UUID | PRIMARY KEY | Queue identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| queue_name | VARCHAR(100) | NOT NULL | Queue name |
| queue_type | VARCHAR(50) | | Billing/AR/Coding |
| priority_level | VARCHAR(20) | | High/Medium/Low |
| assigned_team | VARCHAR(100) | | Assigned team |
| sla_hours | INTEGER | | SLA duration |
| escalation_enabled | BOOLEAN | DEFAULT FALSE | Escalation enabled |
| escalation_after_hours | INTEGER | | Escalation timing |
| queue_status | VARCHAR(20) | | Active/Paused |
| is_active | BOOLEAN | DEFAULT TRUE | Active flag |
| created_by | UUID | FOREIGN KEY → users | Created by |
| updated_by | UUID | FOREIGN KEY → users | Updated by |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update |

**Indexes:** queue_name, queue_type, queue_status, tenant_id

---

### Table 41: tasks
**Purpose:** Track workflow tasks and operational activities

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| task_id | UUID | PRIMARY KEY | Task identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| queue_id | UUID | FOREIGN KEY → work_queues | Related queue |
| related_claim_id | UUID | FOREIGN KEY → claims | Related claim |
| related_patient_id | UUID | FOREIGN KEY → patients | Related patient |
| related_denial_id | UUID | FOREIGN KEY → denials | Related denial |
| related_appeal_id | UUID | FOREIGN KEY → appeals | Related appeal |
| task_title | VARCHAR(255) | | Task title |
| task_description | TEXT | | Task details |
| task_type | VARCHAR(50) | | Follow-up/Appeal |
| task_status | VARCHAR(30) | | Open/In Progress |
| priority | VARCHAR(20) | | High/Medium/Low |
| assigned_to | UUID | FOREIGN KEY → users | Assigned user |
| assigned_date | TIMESTAMP | | Assignment timestamp |
| due_date | DATE | | Due date |
| reopened_flag | BOOLEAN | DEFAULT FALSE | Reopened task |
| completed_date | DATE | | Completion date |
| completion_notes | TEXT | | Resolution notes |
| notes | TEXT | | Internal notes |
| created_by | UUID | FOREIGN KEY → users | Created by |
| updated_by | UUID | FOREIGN KEY → users | Updated by |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update |

**Indexes:** assigned_to, task_status, priority, due_date, tenant_id

---

### Table 42: documents
**Purpose:** Centralized document management

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| document_id | UUID | PRIMARY KEY | Document identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| patient_id | UUID | FOREIGN KEY → patients | Patient |
| encounter_id | UUID | FOREIGN KEY → encounters | Encounter |
| claim_id | UUID | FOREIGN KEY → claims | Claim |
| document_type | VARCHAR(50) | | EOB/Medical Record |
| file_name | VARCHAR(255) | | Original file name |
| file_path | TEXT | | Storage path |
| file_size_kb | INTEGER | | File size |
| mime_type | VARCHAR(100) | | PDF/JPG |
| version_number | INTEGER | DEFAULT 1 | Document version |
| checksum_hash | VARCHAR(255) | | Integrity hash |
| encrypted_flag | BOOLEAN | DEFAULT TRUE | HIPAA encryption |
| document_status | VARCHAR(20) | | Active/Archived |
| retention_expiration_date | DATE | | Retention expiration |
| uploaded_by | UUID | FOREIGN KEY → users | Uploaded by |
| uploaded_at | TIMESTAMP | DEFAULT NOW() | Upload timestamp |
| is_confidential | BOOLEAN | DEFAULT TRUE | HIPAA flag |
| deleted_at | TIMESTAMP | | Soft delete |
| deleted_by | UUID | FOREIGN KEY → users | Deleted by |

**Indexes:** patient_id, claim_id, document_type, document_status, tenant_id

---

### Table 43: claim_notes
**Purpose:** Store claim follow-up notes

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| note_id | UUID | PRIMARY KEY | Note identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| claim_id | UUID | FOREIGN KEY → claims | Claim |
| note_type | VARCHAR(50) | | Payer Call/Internal |
| note_category | VARCHAR(50) | | Billing/Clinical |
| visibility_level | VARCHAR(20) | | Internal/External |
| note_text | TEXT | NOT NULL | Note content |
| followup_required | BOOLEAN | DEFAULT FALSE | Follow-up needed |
| followup_date | DATE | | Follow-up date |
| related_task_id | UUID | FOREIGN KEY → tasks | Linked task |
| created_by | UUID | FOREIGN KEY → users | Created by |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update |

**Indexes:** claim_id, note_category, followup_date, tenant_id

---

### Table 44: ar_followup_activities
**Purpose:** Track AR follow-up operations

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| followup_id | UUID | PRIMARY KEY | Follow-up identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| claim_id | UUID | FOREIGN KEY → claims | Claim |
| denial_id | UUID | FOREIGN KEY → denials | Denial |
| appeal_id | UUID | FOREIGN KEY → appeals | Appeal |
| payer_id | UUID | FOREIGN KEY → payers | Payer |
| followup_date | DATE | NOT NULL | Follow-up date |
| followup_method | VARCHAR(30) | | Call/Portal |
| representative_name | VARCHAR(100) | | Payer representative |
| reference_number | VARCHAR(100) | | Call reference |
| call_duration_minutes | INTEGER | | Call duration |
| payer_response_code | VARCHAR(50) | | Payer response |
| outcome | TEXT | | Follow-up result |
| recovery_probability | DECIMAL(5,2) | | Recovery prediction |
| escalation_required | BOOLEAN | DEFAULT FALSE | Escalation required |
| next_action_date | DATE | | Next action |
| assigned_to | UUID | FOREIGN KEY → users | Assigned user |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update |

**Indexes:** claim_id, payer_id, next_action_date, assigned_to, tenant_id

---

### Table 45: guarantors
**Purpose:** Store financially responsible parties

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| guarantor_id | UUID | PRIMARY KEY | Guarantor identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| patient_id | UUID | FOREIGN KEY → patients | Patient |
| first_name | VARCHAR(50) | NOT NULL | First name |
| last_name | VARCHAR(50) | NOT NULL | Last name |
| dob | DATE | | Date of birth |
| relationship_to_patient | VARCHAR(30) | | Parent/Spouse |
| ssn_encrypted | VARCHAR(255) | | Encrypted SSN |
| employer_name | VARCHAR(100) | | Employer |
| financial_class | VARCHAR(50) | | Financial class |
| phone | VARCHAR(20) | | Phone |
| email | VARCHAR(100) | | Email |
| preferred_contact_method | VARCHAR(20) | | Email/SMS |
| address_line1 | VARCHAR(100) | | Address |
| city | VARCHAR(50) | | City |
| state | VARCHAR(2) | | State |
| zip_code | VARCHAR(10) | | ZIP |
| consent_signed | BOOLEAN | DEFAULT FALSE | Consent signed |
| is_primary_guarantor | BOOLEAN | DEFAULT TRUE | Primary guarantor |
| created_by | UUID | FOREIGN KEY → users | Created by |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes:** patient_id, relationship_to_patient, tenant_id

---

### Table 46: bank_deposits
**Purpose:** Track EFT/check deposit reconciliation

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| deposit_id | UUID | PRIMARY KEY | Deposit identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| deposit_batch_number | VARCHAR(100) | | Batch number |
| deposit_date | DATE | NOT NULL | Deposit date |
| deposit_amount | DECIMAL(10,2) | NOT NULL | Deposit amount |
| deposit_method | VARCHAR(20) | | EFT/Check |
| deposit_source | VARCHAR(30) | | ERA/Manual |
| bank_reference_number | VARCHAR(100) | | Bank reference |
| bank_account_number_masked | VARCHAR(20) | | Masked account |
| reconciliation_status | VARCHAR(30) | | Pending/Matched |
| verified_by | UUID | FOREIGN KEY → users | Verified by |
| verified_at | TIMESTAMP | | Verification timestamp |
| created_by | UUID | FOREIGN KEY → users | Created by |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update |

**Indexes:** deposit_date, reconciliation_status, deposit_batch_number, tenant_id

---

### Table 47: reconciliation_batches
**Purpose:** Match ERA payments against deposits

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| reconciliation_id | UUID | PRIMARY KEY | Reconciliation identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| deposit_id | UUID | FOREIGN KEY → bank_deposits | Deposit |
| era_file_id | UUID | FOREIGN KEY → era_files | ERA file |
| expected_amount | DECIMAL(10,2) | | Expected amount |
| actual_amount | DECIMAL(10,2) | | Actual amount |
| variance_amount | DECIMAL(10,2) | | Variance |
| reconciliation_notes | TEXT | | Finance notes |
| auto_reconciled | BOOLEAN | DEFAULT FALSE | Auto reconciled |
| manual_review_required | BOOLEAN | DEFAULT FALSE | Manual review |
| reconciliation_status | VARCHAR(30) | | Matched/Variance |
| reviewed_by | UUID | FOREIGN KEY → users | Reviewed by |
| reconciled_by | UUID | FOREIGN KEY → users | Reconciled by |
| reconciled_at | TIMESTAMP | | Reconciliation timestamp |
| updated_at | TIMESTAMP | | Last update |

**Indexes:** deposit_id, reconciliation_status, auto_reconciled, tenant_id

---

### Table 48: notifications
**Purpose:** Manage notifications and alerts

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| notification_id | UUID | PRIMARY KEY | Notification identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| notification_type | VARCHAR(30) | | SMS/Email/System |
| notification_channel | VARCHAR(20) | | Email/SMS/Push |
| notification_priority | VARCHAR(20) | | High/Medium/Low |
| recipient_user_id | UUID | FOREIGN KEY → users | Recipient user |
| recipient_patient_id | UUID | FOREIGN KEY → patients | Recipient patient |
| related_entity_type | VARCHAR(50) | | Claim/Appointment |
| related_entity_id | UUID | | Linked entity |
| subject | VARCHAR(255) | | Subject |
| message_body | TEXT | | Notification content |
| delivery_provider | VARCHAR(50) | | Twilio/SendGrid |
| delivery_status | VARCHAR(30) | | Pending/Sent |
| retry_attempts | INTEGER | DEFAULT 0 | Retry attempts |
| opened_flag | BOOLEAN | DEFAULT FALSE | Opened status |
| opened_at | TIMESTAMP | | Open timestamp |
| sent_at | TIMESTAMP | | Sent timestamp |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes:** delivery_status, notification_priority, recipient_user_id, tenant_id

---

### Table 49: notification_templates
**Purpose:** Reusable notification templates

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| template_id | UUID | PRIMARY KEY | Template identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| template_name | VARCHAR(100) | NOT NULL | Template name |
| template_category | VARCHAR(50) | | Billing/Appointment |
| template_type | VARCHAR(30) | | SMS/Email |
| language_code | VARCHAR(10) | | Language |
| subject_template | TEXT | | Subject template |
| body_template | TEXT | | Body template |
| placeholders_supported | JSONB | | Dynamic placeholders |
| is_active | BOOLEAN | DEFAULT TRUE | Active template |
| created_by | UUID | FOREIGN KEY → users | Created by |
| updated_by | UUID | FOREIGN KEY → users | Updated by |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes:** template_name, template_category, template_type, tenant_id

---

### Table 50: api_integration_logs
**Purpose:** Track external API integrations

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| log_id | UUID | PRIMARY KEY | Log identifier |
| tenant_id | UUID | FOREIGN KEY → tenant_organizations | Multi-tenant organization |
| integration_name | VARCHAR(100) | | Integration name |
| integration_type | VARCHAR(50) | | Payment/Clearinghouse |
| request_method | VARCHAR(10) | | GET/POST |
| api_endpoint | TEXT | | API endpoint |
| correlation_id | VARCHAR(100) | | Distributed tracing |
| source_system | VARCHAR(50) | | Internal system |
| destination_system | VARCHAR(50) | | External API |
| request_payload | JSONB | | Request payload |
| response_payload | JSONB | | Response payload |
| response_status | INTEGER | | HTTP status |
| response_time_ms | INTEGER | | API latency |
| retry_status | VARCHAR(20) | | Retry workflow |
| retry_count | INTEGER | DEFAULT 0 | Retry attempts |
| processed_by_service | VARCHAR(100) | | Microservice |
| severity_level | VARCHAR(20) | | Info/Error/Critical |
| error_message | TEXT | | Error details |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes:** integration_name, integration_type, response_status, severity_level, tenant_id

---

## 3. Database Relationships

**Key Relationships:**

1. patients → patient_insurance (1:Many) - One patient can have multiple insurance policies
2. patients → appointments (1:Many) - One patient can schedule multiple appointments
3. patients → encounters (1:Many) - One patient can have many medical encounters/visits
4. patients → claims (1:Many) - One patient can generate multiple insurance claims
5. patients → payments (1:Many) - One patient can have multiple insurance-related payments
6. patients → patient_payments (1:Many) - One patient can make multiple direct payments
7. patients → patient_statements (1:Many) - One patient can receive multiple billing statements
8. patients → collections (1:Many) - One patient can have multiple collection records
9. patients → refunds (1:Many) - One patient can receive multiple refunds
10. patients → guarantors (1:Many) - One patient can have multiple guarantors
11. patients → documents (1:Many) - One patient can have multiple attached documents
12. patients → audit_logs (1:Many) - Patient activities tracked in audit logs
13. providers → appointments (1:Many) - One provider can have many appointments
14. providers → encounters (1:Many) - One provider can perform many encounters
15. providers → charges (1:Many) - One provider can generate many charges
16. providers → claims (1:Many) - One provider can submit many claims
17. providers → claim_lines (1:Many) - One provider can appear on multiple claim lines
18. providers → provider_credentials (1:Many) - One provider credentialed with multiple payers
19. providers → authorizations (1:Many) - One provider can request multiple authorizations
20. appointments → encounters (1:1 or 1:Many) - One appointment may create one or multiple encounters
21. encounters → encounter_diagnoses (1:Many) - One encounter can have multiple diagnoses
22. encounters → encounter_procedures (1:Many) - One encounter can have multiple procedures
23. encounters → charges (1:Many) - One encounter can generate many charges
24. encounters → claims (1:1 or 1:Many) - One encounter may generate multiple claims
25. encounters → documents (1:Many) - One encounter can have many attached documents
26. patient_insurance → eligibility_checks (1:Many) - One insurance can have multiple eligibility verifications
27. patient_insurance → claims (1:Many) - One insurance policy can be used for many claims
28. patient_insurance → authorizations (1:Many) - One insurance policy can have many authorizations
29. payers → patient_insurance (1:Many) - One payer linked to many patient insurance records
30. payers → claims (1:Many) - One payer receives many claims
31. payers → payments (1:Many) - One payer can issue many payments
32. payers → denials (1:Many) - One payer can deny many claims
33. payers → refunds (1:Many) - One payer can receive many refunds
34. payers → provider_credentials (1:Many) - One payer credentialing many providers
35. payers → payer_contracts (1:Many) - One payer can have multiple contracts
36. payer_contracts → payer_contract_rates (1:Many) - One contract can contain many CPT reimbursement rates
37. authorizations → claims (1:Many) - One authorization can support multiple claims
38. authorizations → charges (1:Many) - One authorization may apply to multiple charges
39. charges → claim_lines (1:Many) - One charge can create multiple claim lines
40. claims → claim_lines (1:Many) - One claim contains many claim lines
41. claims → claim_scrubbing_errors (1:Many) - One claim can generate multiple scrub errors
42. claims → payments (1:Many) - One claim can receive multiple payments
43. claims → denials (1:Many) - One claim can have multiple denials
44. claims → appeals (1:Many) - One claim can have multiple appeals
45. claims → claim_notes (1:Many) - One claim can contain many notes
46. claims → claim_status_history (1:Many) - One claim has multiple status changes
47. claims → clearinghouse_submissions (1:Many) - One claim can be submitted multiple times
48. claims → edi_transactions (1:Many) - One claim may have multiple EDI transactions
49. claims → ar_followup_activities (1:Many) - One claim can have many AR follow-ups
50. claims → tasks (1:Many) - One claim can generate many operational tasks
51. claims → documents (1:Many) - One claim can have many supporting documents
52. claim_lines → payment_line_items (1:Many) - One claim line can receive multiple payment postings
53. claim_lines → claim_scrubbing_errors (1:Many) - One claim line can generate multiple scrub errors
54. claim_lines → denials (1:Many) - One claim line can be denied multiple times
55. payments → payment_line_items (1:Many) - One payment contains multiple line item postings
56. payments → refunds (1:Many) - One payment can generate multiple refunds
57. payments → reconciliation_batches (1:Many) - One payment may participate in reconciliation
58. era_files → payments (1:Many) - One ERA file can contain many payments
59. era_files → reconciliation_batches (1:Many) - One ERA file can have multiple reconciliation batches
60. bank_deposits → reconciliation_batches (1:Many) - One bank deposit can match multiple reconciliation batches
61. denials → appeals (1:Many) - One denial can have multiple appeal levels
62. denials → ar_followup_activities (1:Many) - One denial can trigger many follow-up actions
63. denials → tasks (1:Many) - One denial can create many tasks
64. appeals → tasks (1:Many) - One appeal can create many workflow tasks
65. appeals → ar_followup_activities (1:Many) - One appeal can have multiple follow-ups
66. patient_statements → patient_payments (1:Many) - One statement can receive multiple payments
67. patient_statements → collections (1:Many) - One statement can move into collections
68. payment_plans → patient_payments (1:Many) - One payment plan contains multiple payments
69. guarantors → patient_statements (1:Many) - One guarantor can receive many statements
70. guarantors → collections (1:Many) - One guarantor can have many collection accounts
71. work_queues → tasks (1:Many) - One queue contains many tasks
72. users → tasks (1:Many) - One user can manage many tasks
73. users → notifications (1:Many) - One user can receive many notifications
74. notification_templates → notifications (1:Many) - One template generates many notifications
75. users → audit_logs (1:Many) - One user can create many audit entries
76. users → reports (1:Many) - One user can generate many reports
77. users → api_integration_logs (1:Many) - One user/system process can create many integration logs
78. tenant_organizations → users (1:Many) - One organization can contain many users
79. tenant_organizations → patients (1:Many) - One organization can contain many patients
80. tenant_organizations → providers (1:Many) - One organization can contain many providers
81. tenant_organizations → claims (1:Many) - One organization can contain many claims
82. tenant_organizations → payments (1:Many) - One organization can contain many payments
83. tenant_organizations → reports (1:Many) - One organization can contain many reports
84. tenant_organizations → documents (1:Many) - One organization can contain many documents
85. tenant_organizations → notifications (1:Many) - One organization can contain many notifications
86. code_sets → encounter_diagnoses (1:Many) - One code set can map to many diagnoses
87. code_sets → encounter_procedures (1:Many) - One code set can map to many procedures
88. code_sets → charges (1:Many) - One code set can map to many charges
89. ncci_edits → claim_scrubbing_errors (1:Many) - One NCCI rule can trigger many scrub errors
90. lcd_ncd_rules → claim_scrubbing_errors (1:Many) - One LCD/NCD rule can trigger many scrub errors
91. lcd_ncd_rules → authorizations (1:Many) - One LCD/NCD rule can apply to many authorizations

---

## 4. Indexes & Performance

**Critical Indexes:**
- All primary keys and foreign keys
- tenant_id fields for multi-tenant filtering
- Date fields used in queries (service_date, payment_date, submission_date, encounter_date, denial_date, appeal_date, statement_date)
- Status fields (claim.status, encounter.status, denial.status, payment.status)
- Search fields (patient.last_name, patient.mrn, claim.claim_number)
- Insurance verification fields (verification_status, authorization_number)
- Financial reconciliation fields (reconciliation_status, payment_reference_number)
- Queue and workflow fields (task_status, assigned_to, queue_type)
- EDI transaction tracking fields (transaction_type, submission_status, clearinghouse_name)
- Reporting fields (report_category, report_status)
- Notification delivery fields (delivery_status, notification_priority)

**Recommended Composite Indexes:**
- claims(patient_id, submission_date)
- claims(payer_id, status)
- claim_lines(claim_id, cpt_code)
- payments(claim_id, payment_date)
- denials(status, assigned_to)
- appointments(provider_id, appointment_date)
- encounters(patient_id, encounter_date)
- patient_insurance(patient_id, priority)
- tasks(assigned_to, task_status)
- audit_logs(user_id, timestamp)
- notifications(recipient_user_id, delivery_status)
- reports(report_category, generated_by)

**Full-Text Search Index Recommendations:**
- claim_notes.note_text
- denial.denial_reason
- appeals.appeal_letter
- documents.file_name
- tasks.task_description

**Partitioning Strategy:**
- claims table: Partition by submission_date (monthly partitions)
- payments table: Partition by payment_date (monthly partitions)
- audit_logs table: Partition by timestamp (monthly partitions)
- claim_status_history table: Partition by changed_at
- notifications table: Partition by created_at
- api_integration_logs table: Partition by created_at
- edi_transactions table: Partition by processed_date
- reports table: Partition by generation_end_time

**Database Optimization Recommendations:**
- Use PostgreSQL table partitioning for large transactional tables
- Enable connection pooling using PgBouncer
- Use Redis caching for eligibility checks and frequently accessed payer rules
- Use read replicas for analytics/reporting workloads
- Archive old audit_logs and EDI transactions periodically
- Use JSONB indexing (GIN indexes) for:
  - audit_logs.before_value
  - audit_logs.after_value
  - api_integration_logs.request_payload
  - api_integration_logs.response_payload
- Use asynchronous processing for:
  - ERA posting
  - claim scrubbing
  - eligibility checks
  - notifications
  - report generation

---

## 5. Data Retention Policy

| Table | Retention Period |
|-------|------------------|
| audit_logs | 7 years (HIPAA) |
| patients | Indefinite |
| encounters | 7–10 years |
| appointments | Indefinite |
| eligibility_checks | 5–7 years |
| authorizations | 7 years |
| claims | 10 years |
| claim_lines | 10 years |
| claim_scrubbing_errors | 5 years |
| payments | 10 years |
| payment_line_items | 10 years |
| era_files | 7 years |
| denials | 10 years |
| appeals | 10 years |
| patient_statements | 7 years |
| patient_payments | 7–10 years |
| payment_plans | 7 years after completion |
| collections | 7 years |
| refunds | 7 years |
| documents | Based on organization/legal policy |
| notifications | 1–2 years |
| notification_templates | Indefinite |
| api_integration_logs | 2–5 years |
| edi_transactions | 7 years |
| reconciliation_batches | 7 years |
| bank_deposits | 7 years |
| reports | 3 years |
| work_queues | 3–5 years |
| tasks | 3–5 years |
| claim_status_history | 10 years |
| ar_followup_activities | 7 years |
| code_sets | Indefinite |
| ncci_edits | Based on CMS update cycle |
| lcd_ncd_rules | Based on CMS update cycle |

---

## 6. Security & Encryption

**Encrypted Fields:**
- patients.ssn_encrypted
- patient_insurance.subscriber_ssn_encrypted
- guarantors.ssn_encrypted
- providers.ssn_encrypted
- users.password_hash
- users.mfa_secret
- api_integration_logs.request_payload
- api_integration_logs.response_payload
- documents.file_path (if containing PHI)
- bank_deposits.bank_account_number_masked
- Any PHI (Protected Health Information)
- Any PII (Personally Identifiable Information)
- Insurance policy/member numbers
- Authorization reference numbers
- Payment transaction references
- Uploaded medical documents
- Stored EDI transaction files

**Encryption Method:**
- AES-256 encryption at rest
- TLS 1.2+ / TLS 1.3 for data in transit
- Application-level encryption for:
  - SSN fields
  - insurance identifiers
  - payment-related sensitive fields
  - PHI/PII data
- Database-level Transparent Data Encryption (TDE)
- Encrypted database backups
- Encrypted object/document storage
- Signed URL access for secure document retrieval
- Key rotation policy for encryption keys
- Hardware Security Module (HSM) or cloud KMS support

**Authentication & Access Security:**
- BCrypt or Argon2 password hashing
- Multi-Factor Authentication (MFA)
- OAuth2 / OpenID Connect support
- JWT token-based authentication
- Role-Based Access Control (RBAC)
- Row-Level Security (RLS) for tenant isolation
- Session timeout and auto logout
- IP restriction support for admin access
- Failed login monitoring and account lockout

**Audit & Compliance Security:**
- Full audit logging for PHI access
- Immutable audit trail records
- Login history tracking
- Data export/download auditing
- API access auditing
- Security event monitoring
- Suspicious activity detection
- Legal hold support
- HIPAA compliance logging

**HIPAA Compliance Considerations:**
- Minimum necessary access principle
- Secure PHI storage and transmission
- Audit trail retention
- Backup disaster recovery planning
- Business Associate Agreement (BAA) support
- Secure archival storage
- Disaster recovery and failover planning
- Secure deletion and purge policies
- Tenant-level data isolation

**Recommended Security Infrastructure:**

| Security Area | Recommended Technology |
|---------------|------------------------|
| Encryption | AES-256 |
| Password Hashing | BCrypt / Argon2 |
| Transport Security | TLS 1.2+ / TLS 1.3 |
| Authentication | OAuth2 + JWT |
| MFA | TOTP / SMS / Authenticator Apps |
| Secrets Management | AWS KMS / Azure Key Vault / HashiCorp Vault |
| WAF | Cloudflare / AWS WAF |
| SIEM Monitoring | Splunk / ELK / Datadog |
| API Gateway Security | Kong / Apigee / AWS API Gateway |

---

## 7. Backup Strategy

**Backup Schedule:**
- Full Backup: Daily at 2:00 AM
- Incremental Backup: Every 4 hours
- Transaction Log Backup: Every 15 minutes
- Configuration Backup: Daily
- Encryption Key Backup: Daily secure backup
- Document/Object Storage Backup: Daily replication

**Backup Retention Policy:**
- Daily backups retained for 30 days
- Weekly backups retained for 6 months
- Monthly backups retained for 7 years (HIPAA/compliance)
- Transaction logs retained for 30–90 days
- Archived claim/payment backups retained for 7–10 years

**Disaster Recovery Strategy:**
- Geo-redundant backups stored in separate region
- Multi-region disaster recovery environment
- Cross-region database replication
- Point-in-Time Recovery (PITR) enabled
- Automatic failover support
- Standby disaster recovery database
- Recovery Time Objective (RTO): 1–4 hours
- Recovery Point Objective (RPO): 15 minutes

**Backup Security:**
- AES-256 encrypted backups
- TLS-secured backup transmission
- Immutable backup storage support
- Backup access restricted using RBAC
- Separate encryption key management
- Periodic backup integrity verification
- Backup audit logging enabled

**Backup Monitoring & Validation:**
- Automated backup success/failure alerts
- Backup checksum validation
- Scheduled restore testing
- Disaster recovery drill execution
- Backup performance monitoring
- Replication lag monitoring

---

**Next Step:** Create API Integration Requirements Document
