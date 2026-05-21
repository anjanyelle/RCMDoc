# Pre-RCM Modules 1-4: Provider Onboarding, Credentialing, Enrollment, & Contract Management

**Version:** 1.0
**Module ID:** MOD-PRE-01-04
**Category:** Pre-RCM / Foundational Flow

---

# 1. Module Overview

## Purpose

The Provider Credentialing & Management module manages the complete lifecycle of healthcare provider onboarding, verification, enrollment, compliance monitoring, privileging, and recredentialing.

This module ensures providers are legally authorized, clinically qualified, and insurance-enrolled before they begin patient care and billing.

It validates:

* Medical licenses
* DEA registrations
* NPI numbers
* Board certifications
* Malpractice insurance
* Sanction checks
* CAQH profiles
* Insurance payer enrollment eligibility

---

## Why Hospitals Use It

Hospitals use provider credentialing to:

* Prevent claim denials
* Maintain CMS/NCQA compliance
* Ensure patient safety
* Avoid fraud and sanctions
* Verify provider qualifications
* Enable provider billing eligibility
* Maintain payer contracts
* Support medical staff governance

Without credentialing:

* Insurance claims are rejected
* Providers cannot bill payers
* Hospitals lose revenue
* Compliance violations occur
* Legal risks increase

---

## Business Goal

The business goals of this module are:

* Reduce provider onboarding delays
* Accelerate payer enrollment
* Achieve high clean claim rates
* Prevent compliance violations
* Automate verification workflows
* Reduce manual credentialing effort
* Maintain continuous provider compliance
* Improve reimbursement eligibility

---

## Main Users

* Credentialing Staff
* Provider Enrollment Team
* Compliance Team
* Medical Staff Office
* Supervisors
* Auditors
* Insurance Payers
* Healthcare Providers
* Hospital Administrators

---

# 2. Actors Involved

```text
┌───────────────────────────────────────────────────────┐
│ ACTORS IN PROVIDER CREDENTIALING MODULE              │
├───────────────────────────────────────────────────────┤
│                                                       │
│ 1. Credentialing Team                                │
│ 2. Provider Enrollment Team                          │
│ 3. Compliance Team                                   │
│ 4. Medical Staff Office                              │
│ 5. Insurance Payers                                  │
│ 6. CAQH Platform                                     │
│ 7. System                                            │
│ 8. External APIs                                     │
│ 9. Provider                                          │
│ 10. Supervisor                                       │
│ 11. Auditor                                          │
│                                                       │
└───────────────────────────────────────────────────────┘
```

---

# 3. Step-by-Step Workflow

```text
┌─────────────────────┐
│ Provider Added      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Collect Provider    │
│ Demographics        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Upload Documents    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ OCR & Metadata      │
│ Extraction          │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Verify License      │
└──────────┬──────────┘
           ↓
      ╱ ╲
     ╱   ╲
    ╱Valid?╲
    ╲       ╱
     ╲     ╱
      │Yes
      ▼
┌─────────────────────┐
│ Verify DEA          │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Verify Board Cert   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Sanction Check      │
│ (OIG/SAM)           │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Malpractice         │
│ Verification        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Verify NPI          │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ CAQH Validation     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Primary Source      │
│ Verification (PSV)  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Payer Enrollment    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Contract Approval   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Privilege Granting  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Provider Activated  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Ongoing Monitoring  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Recredentialing     │
│ Trigger             │
└─────────────────────┘
```

---

# 4. Credentialing Workflow Logic

## License Verification Flow

```text
Provider Added
       ↓
Call FSMB / State Board API
       ↓
Validate License Number
       ↓
Check Status
       ↓
Active / Expired / Revoked
       ↓
Store Verification Result
       ↓
Generate Alerts if Failed
```

Verification Rules:

* License must be active
* Expiration date required
* PSV required per NCQA
* Re-verification every 90 days

---

## DEA Validation Flow

```text
Validate DEA Format
       ↓
Call DEA Validation Service
       ↓
Verify Provider Match
       ↓
Check DEA Schedules
       ↓
Store Result
```

Validation Includes:

* DEA number format
* Provider name match
* Address match
* Authorized schedules
* Expiration tracking

---

## Board Certification Flow

* Verify through ABMS or AOA
* Validate specialty and subspecialty
* Track MOC status
* Generate expiration alerts
* Support multiple certifications

---

## Sanction Check Flow

```text
Run OIG Check
       ↓
Run SAM Check
       ↓
Run State Medicaid Exclusion Check
       ↓
Match Found?
       ↓
Yes → Immediate Suspension
No  → Continue Workflow
```

---

## Exclusion List Validation

Sources:

* OIG LEIE
* SAM.gov
* State Medicaid Lists
* OFAC

Checks:

* NPI match
* Name match
* DOB match
* Fuzzy matching

---

## Malpractice Insurance Validation

Required Fields:

* Carrier name
* Policy number
* Coverage dates
* Coverage limits
* COI document

Rules:

* Coverage must meet hospital minimums
* Tail coverage validation required
* Expiration alerts at 90/60/30 days

---

## Enrollment Approval Workflow

```text
Credentialing Review
        ↓
Supervisor Approval
        ↓
Peer Review
        ↓
Medical Executive Committee
        ↓
Board Approval
        ↓
Medical Staff Approval
        ↓
Final Activation
```

---

## Privileging Workflow

```text
┌─────────────────────┐
│ Credential Approved │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Department Review   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Medical Committee   │
│ Approval            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Privileges Granted  │
└─────────────────────┘
```

Purpose:
- Define provider procedure access
- Control hospital privileges
- Ensure patient safety
- Prevent unauthorized procedures

---

# 5. CAQH Integration Flow

```text
Provider System            CAQH Platform
       │                         │
       │ Authenticate OAuth2     │
       ├────────────────────────▶│
       │                         │
       │ Fetch Provider Profile  │
       ├────────────────────────▶│
       │                         │
       │ Return Profile Data     │
       │◀────────────────────────┤
       │                         │
       │ Update Local Database   │
       │                         │
```

## CAQH Data Sync

Sync Fields:

* Demographics
* Licenses
* DEA
* Board Certifications
* Work History
* Malpractice Insurance
* Hospital Affiliations

Sync Frequency:

* Daily automated sync
* Manual on-demand sync

---

## CAQH Re-Attestation Workflow

```text
120-Day Timer Reached
        ↓
Send Reminder Notifications
        ↓
Provider Updates Profile
        ↓
Provider Attests CAQH
        ↓
Sync Updated Data
```

---

## CAQH Expiration Handling

If CAQH expires:

* Enrollment paused
* Credentialing team alerted
* Provider notified
* Payer updates blocked

---

# 6. Payer Enrollment Workflow

```text
┌─────────────────────┐
│ Select Insurance    │
│ Payer               │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Generate Enrollment │
│ Packet              │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Submit Enrollment   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Payer Review        │
└──────────┬──────────┘
           ↓
      ╱ ╲
     ╱   ╲
    ╱Approved?╲
    ╲         ╱
     ╲       ╱
      │Yes
      ▼
┌─────────────────────┐
│ Provider Number     │
│ Assigned            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ ERA / EFT Setup     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Enrollment Approved │
└─────────────────────┘
```

Enrollment Features:

* Individual enrollment
* Group enrollment
* Multi-location enrollment
* Re-enrollment support
* Status tracking
* Payer-specific workflows

---

# Provider Contract Management

Includes:
- Payer contracts
- Effective dates
- Termination dates
- Fee schedules
- Renewal reminders
- Contract amendments
- Reimbursement models
- Contract versioning

Purpose:
- Manage reimbursement agreements
- Track payer negotiations
- Prevent expired contracts

---

# 7. Use Case Diagram

```text
Credentialing Staff
        │
        ├── Add Provider
        ├── Upload Documents
        ├── Verify Credentials
        ├── Run Sanction Checks
        ├── Monitor Expirations
        └── Initiate Recredentialing

Enrollment Team
        │
        ├── Submit Enrollments
        ├── Track Enrollment Status
        ├── Manage Rejections
        └── Configure ERA/EFT

Compliance Team
        │
        ├── Review Sanction Matches
        ├── Audit Provider Files
        └── Generate Compliance Reports
```

---

# 8. Activity Flow Diagram

```text
START
   ↓
Provider Registration
   ↓
Document Upload
   ↓
Credential Verification
   ↓
Compliance Validation
   ↓
Enrollment Submission
   ↓
Approval Workflow
   ↓
Provider Activation
   ↓
END
```

---

# 9. Sequence Diagram

```text
Credentialing Staff
        ↓
Frontend UI
        ↓
Backend API
        ↓
External APIs
        ↓
Database
        ↓
Notification Service
```

## Provider Verification Sequence

```text
Credentialing Staff → Frontend
Frontend → Backend API
Backend API → FSMB API
FSMB API → Backend API
Backend API → Database
Backend API → Notification Service
Notification Service → Credentialing Staff
```

---

# 10. API Flow

## Provider Registration API

Endpoint:

```http
POST /api/v1/providers
```

Request Fields:

* first_name
* last_name
* npi
* specialty
* taxonomy_code
* facility_id
* tenant_id

---

## License Verification API

```http
POST /api/v1/providers/{id}/verify/license
```

---

## DEA Verification API

```http
POST /api/v1/providers/{id}/verify/dea
```

---

## NPI Validation API

```http
POST /api/v1/providers/{id}/verify/npi
```

---

## CAQH Integration API

```http
GET /api/v1/providers/{id}/caqh
```

---

## Payer Enrollment API

```http
POST /api/v1/providers/{id}/enrollments
```

---

## Recredentialing API

```http
POST /api/v1/providers/{id}/recredential
```

---

## Request Example

```json
{
  "provider_id": "PROV-1001",
  "license_number": "MD123456",
  "state": "CA"
}
```

---

## Response Example

```json
{
  "status": "active",
  "expiration_date": "2026-12-31",
  "verified_at": "2025-05-19T10:30:00Z"
}
```

---

# 11. Database Flow

## Provider Tables

* providers
* provider_credentials
* provider_licenses
* provider_dea
* provider_board_certifications
* provider_malpractice
* provider_enrollments
* provider_contracts
* provider_specialties
* provider_documents
* provider_recredentialing

---

## Multi-Tenant Architecture

Every table contains:

* tenant_id
* organization_id
* facility_id

Purpose:

* SaaS isolation
* Multi-hospital deployment
* Secure tenant separation

---

## Credential Expiration Tracking

```text
Daily Expiration Job
         ↓
Find Expiring Credentials
         ↓
Generate Alerts
         ↓
Notify Teams
```

---

## Recredentialing Tracking

Rules:

* Every 2–3 years
* NCQA-compliant schedule
* Automated reminders
* Supervisor approval required

---

# Provider Master Index

Includes:
- Duplicate detection
- Cross-facility identity matching
- NPI uniqueness validation
- Enterprise provider registry
- Provider identity merge workflows

Purpose:
- Prevent duplicate provider records
- Maintain enterprise provider identity
- Support multi-facility systems

---

# State Licensing Rules Engine

Includes:
- State-specific expiration rules
- Controlled substance rules
- Telehealth state laws
- Medicaid enrollment differences
- State-specific supervision rules
- License renewal validation

Purpose:
- Support multi-state health systems
- Ensure state compliance
- Automate state-specific workflows

---

# 12. Error Scenarios

## Error 1: Expired License

```text
Expiration Scan Detects Expired License
        ↓
Block Billing Eligibility
        ↓
Notify Provider & Credentialing Team
```

---

## Error 2: DEA Validation Failure

```text
DEA Validation Failed
        ↓
Manual Review Required
        ↓
Update DEA Information
```

---

## Error 3: Board Certification Expired

* Generate alerts
* Notify payers
* Re-verify certification

---

## Error 4: OIG Exclusion Match

```text
OIG Match Found
        ↓
Immediate Provider Suspension
        ↓
Notify Compliance Team
```

---

## Error 5: CAQH Profile Incomplete

* Pause enrollment
* Notify provider
* Resume after correction

---

## Error 6: Enrollment Rejected by Payer

* Capture rejection reason
* Correct data
* Resubmit enrollment

---

## Error 7: Missing Malpractice Insurance

* Prevent activation
* Request updated COI

---

## Error 8: Duplicate Provider Record

* Block duplicate creation
* Merge existing records

---

## Error 9: NPI Validation Failure

* Block provider activation
* Verify correct NPI

---

## Error 10: Recredentialing Overdue

* Suspend privileges
* Escalate to supervisor

---

# 13. Dashboard & Status Flow

```text
┌─────────────────────┐
│ New Provider        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Documents Uploaded  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Verification In     │
│ Progress            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Enrollment Pending  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Privileges Approved │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Active Provider     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Recredentialing Due │
└─────────────────────┘
```

## Credentialing KPI Dashboard

* Providers Pending Review
* Expiring Licenses
* Enrollment Approval Rate
* CAQH Expiration Alerts
* Recredentialing Due
* Provider Activation Time
* Payer Enrollment Status
* Sanction Match Alerts
* Missing Documents
* Average Enrollment Days
* Revenue Delayed Due to Enrollment
* Providers Pending Activation
* Enrollment Approval %
* Payer-wise Delays
* Credential Expiration Risk
* Revenue Loss Due to Expired Credentials

---

# 14. Automation & Background Jobs

## Daily License Expiration Scan

Schedule:

* Daily at 2:00 AM

---

## CAQH Sync Scheduler

Schedule:

* Daily at 3:00 AM

---

## Recredentialing Reminder Job

Alert Tiers:

* 90 days
* 60 days
* 30 days
* Critical overdue

---

## Enrollment Status Polling

* Every 4 hours
* Poll payer APIs
* Update statuses automatically

---

## OIG/SAM Exclusion Monitoring

* Monthly batch validation
* Immediate suspension on match

---

## Document Expiration Alerts

* Daily scans
* Automated reminders

---

# Notification & Alert Management

Alert Types:
- License expiration
- DEA expiration
- Board certification expiration
- Enrollment rejection
- Missing documents
- CAQH re-attestation due
- Privilege renewal alerts
- Contract expiration alerts

Channels:
- Email
- SMS
- In-app notifications
- Dashboard alerts
- Mobile push notifications

Purpose:
- Reduce missed expirations
- Improve provider compliance
- Accelerate issue resolution

---

# 15. Audit & Compliance

## HIPAA Compliance

* PHI protection
* Access controls
* Audit tracking
* Breach monitoring

---

## NCQA Compliance

* Primary Source Verification
* Recredentialing cycles
* Credentialing standards

---

## CMS Compliance

* OIG checks
* NPI requirements
* Medicare enrollment compliance

---

## Audit Logging

Capture:

* User ID
* Timestamp
* Before/After Changes
* IP Address
* Device Information
* Document Access Logs

---

# 16. Role-Based Access Control

| Role                | Access             |
| ------------------- | ------------------ |
| Credentialing Staff | Manage credentials |
| Enrollment Team     | Submit enrollments |
| Compliance Team     | Compliance audits  |
| Supervisor          | Final approvals    |
| Admin               | Full access        |
| Auditor             | Read-only          |

Sensitive Restrictions:

* Only supervisors activate providers
* Compliance overrides restricted
* Audit logs immutable

---

# 17. Document Management

Supported Documents:

* Medical License
* DEA Certificate
* Board Certification
* Malpractice Insurance
* CAQH Documents
* W9 Forms
* Payer Contracts
* CV / Resume

---

## OCR & Metadata Indexing

OCR Extracts:

* License numbers
* Expiration dates
* Provider names
* Board details

---

## Secure S3 Storage

Features:

* AES-256 encryption
* Versioning
* Lifecycle rules
* Signed URL access

---

# 18. Third-Party Integrations

* CAQH ProView
* NPPES Registry
* FSMB
* DEA Validation
* OIG LEIE
* SAM.gov
* DocuSign
* Twilio
* Email Services

---

# Provider Self-Service Portal

Features:
- Document upload
- License renewal submission
- CAQH status tracking
- Enrollment tracking
- Credential expiration alerts
- E-signature support
- Provider profile updates
- Tax form uploads
- Credential checklist tracking

Portal Benefits:
- Reduce credentialing delays
- Reduce manual communication
- Improve provider engagement
- Faster enrollment completion

---

# Telehealth Credentialing

Includes:
- Multi-state licensing validation
- Compact state verification
- Telemedicine privileges
- Virtual care payer enrollment
- Telehealth compliance validation
- State telehealth rule engine

Supported:
- Remote providers
- Virtual clinics
- Telemedicine physicians
- Interstate care delivery

---

# Delegated Credentialing

Includes:
- Delegated entity agreements
- NCQA delegated audits
- Shared credential repositories
- External review workflows
- Health system credential sharing
- Centralized provider governance

Purpose:
- Support large hospital systems
- Reduce duplicate credentialing
- Share provider approvals across entities

---

# Provider Type Matrix

| Provider Type       | Credential Requirements     |
|---------------------|-----------------------------|
| MD/DO               | License + DEA + Board       |
| NP                  | APRN License                |
| PA                  | Supervising Physician       |
| Therapist           | State Therapy License       |
| Dentist             | Dental License              |
| Locum               | Temporary Privileges        |
| Telehealth Provider | Multi-State Validation      |
| Behavioral Health   | Behavioral License          |

Purpose:
- Support multi-specialty systems
- Handle provider-specific workflows
- Enable enterprise provider onboarding

---

# 19. Security & Encryption

## Security Controls

* AES-256 encryption
* TLS 1.2+
* MFA authentication
* JWT authorization
* RBAC enforcement
* PHI audit tracking

---

# 20. Disaster Recovery & Backup

## Recovery Objectives

* RPO: 1 hour
* RTO: 4 hours

---

## Backup Strategy

* Daily DB backup
* Geo-redundant replication
* Audit log retention
* Point-in-time recovery

---

# 21. Enterprise Enhancements

* AI Credential Validation
* Automated Recredentialing
* Smart Expiration Prediction
* AI Fraud Detection
* Cross-Facility Sharing
* Workflow Automation Engine

---

# 22. Revenue Cycle Impact

## Why This Module Is Critical

Without credentialing:

* Claims are denied
* Billing blocked
* Revenue lost
* Compliance risks increase

---

## Revenue Impact Areas

* Clean claim rate
* Faster reimbursement
* Reduced denials
* Faster provider activation
* Reduced compliance penalties

---

# 23. Additional Enterprise Sections

## Primary Source Verification (PSV)

## Provisional Credentialing

## Peer Review & Committee Approval

## Privileging Workflow

## Provider Self-Service Portal

## Telehealth Credentialing

## Delegated Credentialing

## Ongoing Monitoring

## Provider Type Matrix

## Glossary

## Reporting Module

---

# 24. Summary

The Provider Credentialing & Management module is a foundational healthcare RCM component.

It ensures:

* providers are legally verified,
* insurance enrollment is completed,
* compliance is maintained,
* billing eligibility is active,
* and healthcare organizations can receive reimbursements successfully.

This module directly impacts:

* provider activation,
* payer reimbursement,
* claim acceptance,
* compliance,
* and enterprise operational readiness.

---

**Next Module:** [Module 1: Appointment Scheduling](Flows_Module_04_Appointment_Scheduling.md)