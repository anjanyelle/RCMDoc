# Healthcare RCM Application - System Requirements Summary

**Version:** 1.0  
**Date:** May 18, 2026  
**For:** Development Team (Non-Healthcare Background)

---

## 1. What We're Building

A complete Revenue Cycle Management system that helps hospitals:
- Register patients and verify insurance
- Capture all services provided
- Code services using medical codes
- Submit claims to insurance companies
- Track payments and denials
- Bill patients for remaining balances
- Generate financial reports

**Goal:** Reduce claim denials from 10-15% to <5%, collect payments in <40 days

---

## 2. Core Modules (20 Main Features)

### Module 1: User Management
**Who uses it:** Everyone  
**What it does:** Login, passwords, role-based permissions  
**Key Features:**
- 10 user roles (Admin, Front Desk, Doctor, Coder, Biller, AR Manager, etc.)
- Multi-factor authentication
- Audit logging (HIPAA requirement)
- Session timeout after 15 minutes

---

### Module 2: Provider Credentialing
**Who uses it:** Admin staff  
**What it does:** Register doctors with insurance companies  
**Key Features:**
- Store provider NPI, licenses, certifications
- Track credentialing status with each payer
- Alert 90 days before credential expiration
- CAQH integration

**Why critical:** Without credentialing, ALL claims from that doctor get rejected

---

### Module 3: Fee Schedule Management
**Who uses it:** Finance team  
**What it does:** Maintain hospital prices and insurance contract rates  
**Key Features:**
- Chargemaster (CDM): List of all services with prices
- Contract rates by payer and CPT code
- Automatic rate calculation during billing
- Contract variance analysis (detect underpayments)

---

### Module 4: Patient Registration
**Who uses it:** Front desk  
**What it does:** Collect patient demographics and insurance info  
**Key Features:**
- Capture: Name, DOB, address, phone, insurance card
- Master Patient Index (MPI) prevents duplicate records
- Auto-generate unique Medical Record Number (MRN)
- Store primary, secondary, tertiary insurance
- Digital consent forms

**Common mistake:** Wrong insurance ID = claim denial

---

### Module 5: Insurance Verification
**Who uses it:** Front desk (before appointment)  
**What it does:** Check if insurance is active and what patient owes  
**Key Features:**
- Real-time eligibility check (EDI 270/271)
- Shows: Copay, deductible, coinsurance, coverage limits
- Coordination of Benefits (which insurance pays first)
- Network status (in-network vs out-of-network)
- Store verification history

**Revenue impact:** Prevents treating patients with inactive insurance

---

### Module 6: Prior Authorization
**Who uses it:** Authorization team  
**What it does:** Get insurance approval before expensive procedures  
**Key Features:**
- Identify services requiring authorization
- Submit authorization requests with clinical justification
- Track authorization number, approved units, expiration date
- Alert when authorization expiring or units exhausted
- Peer-to-peer review for denied authorizations

**Why critical:** Services without required authorization = 100% claim denial

---

### Module 7: Appointment Scheduling
**Who uses it:** Front desk  
**What it does:** Schedule patient visits  
**Key Features:**
- Provider calendars with availability templates
- Appointment types with durations
- Automated reminders (SMS, email, phone)
- Waitlist management
- Patient self-scheduling portal
- No-show tracking

**Revenue impact:** Reminders reduce no-shows = less lost revenue

---

### Module 8: Encounter Creation
**Who uses it:** Front desk (at check-in)  
**What it does:** Create visit record that holds all billing data  
**Key Features:**
- Auto-populate patient, insurance, provider info
- Encounter types: Office, Emergency, Inpatient, Outpatient, Telehealth
- Track encounter status: Scheduled → Checked In → Completed
- Link all diagnoses, procedures, charges to encounter

**Think of it as:** The "shopping cart" for the hospital visit

---

### Module 9: Clinical Documentation (EMR Integration)
**Who uses it:** Doctors, nurses  
**What it does:** Receive clinical notes from EMR system  
**Key Features:**
- HL7/FHIR integration with EMR
- Receive: SOAP notes, diagnoses, procedures, orders, results
- Clinical Documentation Improvement (CDI) alerts for incomplete notes
- Problem lists, medication lists, allergy lists

**Why critical:** Insurance only pays for documented services

---

### Module 10: Order Management
**Who uses it:** Doctors  
**What it does:** Track lab tests, imaging, medications ordered  
**Key Features:**
- CPOE (Computerized Physician Order Entry)
- Order types: Lab, imaging, meds, referrals, procedures
- Order sets for common conditions
- Track order status: Ordered → Completed
- Auto-generate charges when orders completed

**Revenue impact:** Automatic charge capture prevents missed revenue

---

### Module 11: Charge Capture
**Who uses it:** Clinical staff, billing team  
**What it does:** Convert every service into a billable charge  
**Key Features:**
- Manual charge entry (search CPT code, add to encounter)
- Automatic charge capture from completed orders
- Charge reconciliation (orders vs charges)
- Charge lag monitoring (time between service and charge entry)
- Charge hold/release for pending documentation

**Revenue impact:** Missed charges = direct revenue loss (5-10% of revenue typically)

---

### Module 12: Medical Coding
**Who uses it:** Medical coders  
**What it does:** Assign standardized codes to diagnoses and procedures  
**Key Features:**
- Coding worklist (encounters ready to code)
- Search ICD-10 (diagnosis codes) and CPT (procedure codes)
- Link diagnoses to procedures (medical necessity)
- DRG assignment for inpatient stays
- E&M level selection for office visits
- Encoder integration (3M, Optum)

**Code types:**
- ICD-10: Diagnosis codes (e.g., E11.9 = Type 2 Diabetes)
- CPT: Procedure codes (e.g., 99213 = Office visit level 3)
- HCPCS: Additional services (e.g., J1234 = Drug injection)
- DRG: Inpatient payment groups

**Why critical:** Wrong codes = claim denial or underpayment

---

### Module 13: Coding Compliance
**Who uses it:** Coders, compliance team  
**What it does:** Prevent coding errors and fraud  
**Key Features:**
- NCCI edits (prevent billing incompatible codes together)
- LCD/NCD rules (Medicare coverage rules)
- MUE limits (max units per day)
- Upcoding detection
- Unbundling detection

**Compliance risk:** Upcoding/unbundling = fraud = fines/jail time

---

### Module 14: Claim Creation
**Who uses it:** Billing team  
**What it does:** Generate insurance claim from coded encounter  
**Key Features:**
- Auto-generate CMS-1500 (professional) or UB-04 (hospital) claim
- Populate all required fields from encounter data
- Include: Patient, insurance, provider NPIs, codes, charges
- Claim splitting (if >6 service lines on CMS-1500)

---

### Module 15: Claim Scrubbing
**Who uses it:** Billing team  
**What it does:** Check claim for errors before submission  
**Key Features:**
- 200+ validation checks
- Check: Missing fields, invalid codes, NCCI edits, authorization, duplicates
- Error levels: Fatal (must fix), Warning (recommend fix), Info
- Clean claim indicator
- Bulk scrubbing (1000+ claims in <5 minutes)

**Goal:** 95%+ clean claim rate = fewer denials

---

### Module 16: Claim Submission
**Who uses it:** Billing team  
**What it does:** Send claims to insurance companies  
**Key Features:**
- Clearinghouse integration (Waystar, Availity, Change Healthcare)
- EDI 837 format (electronic claims)
- Batch submission (every 2 hours)
- Acknowledgment processing (EDI 999, EDI 277)
- Timely filing tracking (alert before deadline)

**Timely filing:** Most payers require claims within 90-365 days of service

---

### Module 17: Claim Tracking
**Who uses it:** Billing team  
**What it does:** Monitor claim status after submission  
**Key Features:**
- Claim status dashboard (Submitted, Pending, Paid, Denied)
- Aging reports (0-30, 31-60, 61-90, 90+ days)
- EDI 276/277 status inquiry
- Payer portal integration
- Worklists (claims pending >30/60/90 days)

---

### Module 18: Payment Posting (ERA)
**Who uses it:** AR team  
**What it does:** Record insurance payments  
**Key Features:**
- Import EDI 835 (Electronic Remittance Advice)
- Auto-posting (match payment to claim automatically)
- Manual posting (when auto-match fails)
- Adjustment reason codes (CARC/RARC)
- Underpayment/overpayment detection
- EFT reconciliation (match payment to bank deposit)

**Adjustment types:**
- Contractual: Difference between billed and allowed amount
- Deductible: Patient's annual deductible
- Copay: Fixed patient payment
- Coinsurance: Patient's % share

---

### Module 19: Denial Management
**Who uses it:** Denial team  
**What it does:** Handle rejected claims  
**Key Features:**
- Denial tracking with reason codes
- Denial worklist (prioritize high $ denials)
- Root cause analysis (top denial reasons)
- Appeal creation and tracking (Level 1, 2, 3)
- Corrected claim resubmission
- Appeal overturn rate tracking

**Common denial reasons:**
- Missing authorization (30%)
- Incorrect coding (25%)
- Eligibility issues (20%)
- Timely filing (10%)

**Revenue impact:** 10-15% of claims denied, 60% recoverable through appeals

---

### Module 20: Secondary Billing
**Who uses it:** Billing team  
**What it does:** Bill second/third insurance after primary pays  
**Key Features:**
- Auto-generate secondary claim after primary payment
- Include primary payment info on secondary claim
- Medicare crossover (auto-forward to Medicaid)
- Medicare Secondary Payer (MSP) rules
- Tertiary billing

---

### Module 21: Patient Billing
**Who uses it:** Patient accounts team  
**What it does:** Bill patients for their portion  
**Key Features:**
- Generate patient statements (monthly)
- Show: Total charges, insurance payments, patient responsibility
- Multiple delivery: Mail, email, patient portal
- Payment processing (credit card, ACH, check, cash)
- Payment plans (installments)
- Point-of-service collections (collect copay at check-in)
- Price transparency (cost estimates before service)

**Patient responsibility = Deductible + Copay + Coinsurance**

---

### Module 22: Collections
**Who uses it:** Collections team  
**What it does:** Collect overdue patient balances  
**Key Features:**
- Automated collection notices (30, 60, 90, 120 days)
- Internal collections (phone calls)
- External collections (transfer to agency after 120 days)
- Bad debt write-off
- Charity care screening (before collections)

**Compliance:** No Surprises Act limits collection practices

---

### Module 23: Reporting & Analytics
**Who uses it:** Management, finance team  
**What it does:** Track RCM performance  
**Key Metrics (KPIs):**
- Clean claim rate (Target: >95%)
- Denial rate (Target: <5%)
- Days in AR (Target: <40 days)
- Net collection rate (Target: >95%)
- AR over 90 days (Target: <15%)
- Cost to collect (Target: <$0.05 per $1)

**Reports:**
- Daily: Charges, payments, denials
- Weekly: Clean claim rate, denial rate
- Monthly: Revenue by department/provider/payer, AR aging
- Ad-hoc: Custom reports, dashboards

---

### Module 24: Audit & Compliance
**Who uses it:** Compliance team  
**What it does:** Track all activities for audits  
**Key Features:**
- Audit log (all user actions for 7 years)
- HIPAA compliance (encryption, access controls)
- Internal audit tools (coding audits, billing audits)
- External audit support (RAC, MAC, OIG)
- Compliance alerts (upcoding, unbundling, overpayments)

---

### Module 25: Interoperability
**Who uses it:** IT team  
**What it does:** Connect with other systems  
**Integrations:**
- EMR/EHR (HL7, FHIR)
- Lab systems (HL7 ORM/ORU)
- Radiology/PACS (HL7 ORM/ORU)
- Pharmacy systems
- Clearinghouses (EDI 837, 835, 270/271, 276/277)
- Payer portals
- Patient portal
- Health Information Exchange (HIE)

---

## 3. Technology Requirements

### Performance
- Page load: <2 seconds
- Support 500+ concurrent users
- Process 1000 claims in <5 minutes

### Security
- AES-256 encryption (data at rest)
- TLS 1.2+ (data in transit)
- Multi-factor authentication
- HIPAA compliant
- PCI-DSS compliant (for payments)

### Availability
- 99.9% uptime
- Disaster recovery: <4 hour recovery time

---

## 4. User Roles & Permissions

| Role | Can Do |
|------|--------|
| **Front Desk** | Register patients, verify insurance, schedule appointments, collect copays |
| **Doctor** | Document visits, write orders, sign encounters |
| **Medical Coder** | Assign ICD/CPT codes, review documentation |
| **Billing Specialist** | Create claims, scrub claims, submit claims |
| **AR Manager** | Post payments, manage denials, follow up on aging claims |
| **Collections** | Bill patients, set up payment plans, send to collections |
| **Finance Manager** | View reports, dashboards, financial analytics |
| **Compliance Officer** | Audit logs, compliance reports, internal audits |
| **System Admin** | User management, system configuration |

---

## 5. Critical Business Rules

### Rule 1: Provider Credentialing
- Doctor MUST be credentialed with payer before billing
- If not credentialed → 100% claim rejection

### Rule 2: Insurance Verification
- MUST verify eligibility before service
- If insurance inactive → Patient becomes self-pay

### Rule 3: Prior Authorization
- MUST obtain authorization for services requiring it
- If no authorization → 100% claim denial

### Rule 4: Medical Necessity
- Diagnosis MUST support procedure (per LCD/NCD)
- If not supported → Claim denial

### Rule 5: Timely Filing
- Claims MUST be submitted within payer deadline (90-365 days)
- If late → Permanent denial, no appeal

### Rule 6: Clean Claims
- Claims MUST pass all scrubbing checks
- Clean claims pay 3x faster than dirty claims

### Rule 7: Contractual Adjustment
- CANNOT bill patient for contractual write-off (in-network)
- Balance billing = contract violation

### Rule 8: Refunds
- Overpayments MUST be refunded within 60 days
- Keeping overpayments = fraud

---

## 6. Revenue Cycle Flow (Simple)

```
1. Doctor credentialed with insurance ✓
2. Patient registers → Verify insurance ✓
3. Get prior authorization (if needed) ✓
4. Patient visits → Encounter created
5. Doctor documents visit → Diagnoses + procedures
6. Services performed → Charges captured
7. Coder assigns ICD/CPT codes
8. Claim created and scrubbed
9. Claim submitted to insurance
10. Insurance reviews and pays
11. Payment posted to account
12. If denied → Appeal
13. Bill patient for remaining balance
14. Patient pays or goes to collections
```

---

## 7. Common Mistakes & How to Prevent

| Mistake | Impact | Prevention |
|---------|--------|------------|
| Wrong insurance ID at registration | Claim denial | Real-time eligibility check |
| Missing prior authorization | 100% denial | Authorization tracking system |
| Incomplete documentation | Coding errors, denials | CDI alerts for providers |
| Missed charges | Revenue loss | Charge reconciliation reports |
| Wrong CPT code | Denial or underpayment | Encoder integration, coding audits |
| NCCI edit violation | Claim rejection | Claim scrubbing with NCCI checks |
| Late claim submission | Timely filing denial | Timely filing alerts |
| Not appealing denials | Lost revenue | Denial worklists, appeal tracking |

---

## 8. Success Metrics

**Before RCM System:**
- Denial rate: 10-15%
- Days in AR: 50-60 days
- Clean claim rate: 75-80%
- Revenue leakage: 5-10%

**After RCM System (Goals):**
- Denial rate: <5%
- Days in AR: <40 days
- Clean claim rate: >95%
- Revenue leakage: <2%

**Financial Impact Example:**
- Hospital with $50M annual revenue
- 5% revenue leakage = $2.5M lost
- RCM system reduces leakage to 2% = $1.5M recovered
- ROI: System pays for itself in 6-12 months

---

## 9. Next Documents Needed

1. **Database Design** - Tables, relationships, fields for all modules
2. **API Specifications** - Integration with EMR, clearinghouse, payers
3. **UI/UX Wireframes** - Screen designs for each module
4. **User Stories** - Detailed requirements for each feature
5. **Test Cases** - How to verify each feature works correctly

---

**Questions for Development Team?**
- Which module should we build first? (Recommendation: Start with Patient Registration → Encounter → Charge Capture → Claim Creation)
- What technology stack? (Recommendation: React frontend, Node.js/Python backend, PostgreSQL database)
- Cloud or on-premise? (Recommendation: Cloud for scalability)
