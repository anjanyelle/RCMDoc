# Healthcare RCM Application - System Requirements Summary (v2.0)

**Version:** 2.0  
**Updated:** May 18, 2026  
**For:** Development Team (Non-Healthcare Background)  
**UAT Acceptance:** [ ] Pending Sign-off by Business Owner

---

## 1. What We're Building

A complete **AI-powered** Revenue Cycle Management system that helps hospitals:
- Register patients and verify insurance in real-time
- Capture all services provided automatically
- Code services using AI-assisted medical coding
- Submit claims electronically with error prediction
- Track payments and denials with predictive analytics
- Bill patients for remaining balances
- Generate financial reports and dashboards

**Goal:** Reduce claim denials from 10-15% to <5%, collect payments in <35 days (vs industry 50+ days)

**Key Differentiators:**
- ✅ AI-powered coding and error prediction
- ✅ Real-time insurance verification (<30 seconds)
- ✅ 99.5% clean claim rate
- ✅ Modern, intuitive UI
- ✅ Cloud-based, mobile-responsive

---

## 2. Core Modules (30 Main Features)

### Module 1: User Management, Security & Multi-Tenancy
**Who uses it:** Everyone / System Admin / Enterprise Hospitals  
**What it does:** Secure login, role-based permissions, audit logging, and managing multiple hospitals in one RCM system with separate data and configurations.  
**Key Features:**
- 10 user roles (Admin, Front Desk, Doctor, Coder, Biller, AR Manager, etc.)
- Multi-factor authentication (MFA)
- Single Sign-On (SSO) integration
- JWT token-based authentication
- Session timeout after 15 minutes (configurable)
- Password complexity requirements
- Audit logging (HIPAA requirement - 7 years retention)
- Role-based access control (RBAC) per tenant
- IP whitelisting for admin access
- Hospital/Tenant creation
- Tenant-wise data isolation
- Hospital-specific branding & configuration
- Tenant-wise billing setup
- Separate reports & dashboards per tenant
- Tenant-level security & access control
- Separate database/schema per hospital (or tenant_id isolation model)
- Tenant subscription & plan management
- Hospital-specific payer contracts

**AI Feature:**
- AI-based tenant onboarding assistant
- Auto-configure default hospital settings based on hospital type

**Tech Stack:**
- FastAPI authentication endpoints
- JWT tokens (8-hour expiration) with tenant claim
- bcrypt password hashing
- PostgreSQL user tables and multi-tenant isolation schema (or tenant_id model)
- AWS Cognito (Tenant-wise auth)
- AWS API Gateway + JWT tenant isolation

**Common mistake:**
- Tenant data mixing = HIPAA violation.

---

### Module 2: Provider Credentialing & Management
**Who uses it:** Admin staff / Scheduling Team  
**What it does:** Register doctors with insurance companies and manage doctor/provider details before scheduling and billing.  
**Key Features:**
- Store provider NPI, licenses, certifications
- Track credentialing status with each payer
- Alert 90 days before credential expiration (auto-alert for license expiration)
- CAQH integration
- Document management (upload licenses, certificates)
- Credentialing workflow (pending → approved → active)
- Provider profile management
- Provider availability & schedule mapping
- Department and specialty mapping assignment
- Provider status tracking
- Hospital affiliation mapping
- Taxonomy code management
- Provider workload tracking

**AI Feature:**
- AI recommends provider schedule optimization
- Auto-alert for license and credential expiration

**Tech Stack:**
- PostgreSQL tables: `providers`, `provider_specialties`, `provider_schedule`, `provider_licenses`
- NPI Registry API integration

**Common mistake:**
- Wrong provider NPI/license setup = claim rejection.

---

### Module 3: Fee Schedule & Master Data Management
**Who uses it:** Finance team / Admin Team  
**What it does:** Maintain hospital prices, insurance contract rates, and common healthcare master data used across all RCM modules.  
**Key Features:**
- Chargemaster (CDM): List of all services with prices
- Contract rates by payer and CPT code
- Automatic rate calculation during billing
- Contract variance analysis (detect underpayments)
- Fee schedule versioning (effective dates)
- Bulk import/export of fee schedules
- Payer master setup
- CPT / ICD / HCPCS code master setup
- Department & specialty setup
- Facility master
- Insurance plan setup
- Provider specialty mapping
- Revenue code setup
- Modifier master setup
- POS (Place of Service) code setup

**AI Feature:**
- AI suggests CPT/ICD updates based on CMS changes
- Smart search for medical codes

**Tech Stack:**
- PostgreSQL tables: `payer_master`, `cpt_codes`, `icd_codes`, `hcpcs_codes`, `facilities`, `departments`, `fee_schedules`
- Redis cache for fast code lookup

**Common mistake:**
- Wrong CPT/ICD master setup = claim denial.

---

### Module 4: Patient Registration
**Who uses it:** Front desk  
**What it does:** Capture patient demographics and insurance info  
**SLA/TAT:** Registration completed in <5 minutes.  
**Key Features:**
- Capture: Name, DOB, address, phone, insurance card
- Master Patient Index (MPI) prevents duplicate records
- Auto-generate unique Medical Record Number (MRN)
- Store primary, secondary, tertiary insurance
- Digital consent forms with e-signature
- **OCR for insurance card scanning** (AI-powered)
- **Duplicate patient detection** (fuzzy matching)
- Emergency contact management
- Patient photo upload

**AI Feature:**
- Scan insurance card with phone camera
- AI extracts: Insurance company, policy number, group number, member name
- Auto-fills registration form
- **Saves 2-3 minutes per registration**

**Tech Stack:**
- AWS Textract or OpenAI Vision API for OCR
- PostgreSQL tables: `patients`, `patient_insurance`, `patient_contacts`

**Common mistake:** Wrong insurance ID = claim denial

---

### Module 5: Insurance Verification (Real-Time)
**Who uses it:** Front desk (before appointment)  
**What it does:** Check if insurance is active and what patient owes  
**SLA/TAT:** Verification completed in <30 seconds.  
**Key Features:**
- **Real-time eligibility check** (EDI 270/271 via Waystar/Availity)
- Response time: <30 seconds
- Shows: Copay, deductible, coinsurance, coverage limits
- Coordination of Benefits (which insurance pays first)
- Network status (in-network vs out-of-network)
- Prior authorization requirements
- Store verification history
- **Cache results for 24 hours** (Redis)
- Batch verification for scheduled appointments

**API Integration:**
- **Waystar Eligibility API** (primary)
- **Availity API** (backup)
- EDI 270 (inquiry) → EDI 271 (response)

**Example API Call:**
```python
POST https://api.waystar.com/eligibility/v1/inquiries
{
  "patient": {"firstName": "John", "lastName": "Doe", "dob": "1980-05-15"},
  "payer": {"payerId": "00431"},
  "provider": {"npi": "1234567890"},
  "serviceDate": "2026-05-20"
}
```

**Revenue impact:** Prevents treating patients with inactive insurance

---

### Module 6: Prior Authorization
**Who uses it:** Authorization team  
**What it does:** Get insurance approval before expensive procedures  
**Key Features:**
- Identify services requiring authorization (by CPT code and payer)
- Submit authorization requests with clinical justification
- Track authorization number, approved units, expiration date
- Alert when authorization expiring or units exhausted
- Peer-to-peer review for denied authorizations
- **Automated authorization status checks** (EDI 278)
- Authorization worklist (pending, approved, denied)

**Why critical:** Services without required authorization = 100% claim denial

---

### Module 7: Appointment Scheduling
**Who uses it:** Front desk  
**What it does:** Schedule patient visits  
**Key Features:**
- Provider calendars with availability templates
- Appointment types with durations
- **Automated reminders** (SMS via Twilio, email, phone)
- Waitlist management
- **Patient self-scheduling portal**
- No-show tracking
- Drag-and-drop rescheduling
- Calendar views: Day, week, month
- Color-coded by appointment type
- Recurring appointments

**API Integration:**
- **Twilio API** for SMS reminders
- Example: "Hi John, your appointment with Dr. Smith is tomorrow at 10:00 AM. Reply CONFIRM to confirm."

**Revenue impact:** Reminders reduce no-shows by 30% = less lost revenue

---

### Module 8: Encounter Creation
**Who uses it:** Front desk (at check-in)  
**What it does:** Create visit record that holds all billing data  
**Key Features:**
- Auto-populate patient, insurance, provider info
- Encounter types: Office, Emergency, Inpatient, Outpatient, Telehealth
- Track encounter status: Scheduled → Checked In → In Progress → Completed
- Link all diagnoses, procedures, charges to encounter
- Encounter lock after billing (prevent changes)

**Think of it as:** The "shopping cart" for the hospital visit

---

### Module 9: Clinical Documentation (EMR Integration)
**Who uses it:** Doctors, nurses  
**What it does:** Receive clinical notes from EMR system  
**Key Features:**
- **HL7/FHIR integration** with EMR (Epic, Cerner, Allscripts)
- Receive: SOAP notes, diagnoses, procedures, orders, results
- Clinical Documentation Improvement (CDI) alerts for incomplete notes
- Problem lists, medication lists, allergy lists
- **Real-time data sync** (not batch)

**FHIR Resources:**
- Patient (demographics)
- Encounter (visits)
- Condition (diagnoses)
- Procedure (procedures)
- Observation (vitals, labs)
- MedicationRequest (prescriptions)

**Why critical:** Insurance only pays for documented services

---

### Module 10: Order Management
**Who uses it:** Doctors  
**What it does:** Track lab tests, imaging, medications ordered  
**Key Features:**
- CPOE (Computerized Physician Order Entry)
- Order types: Lab, imaging, meds, referrals, procedures
- Order sets for common conditions
- Track order status: Ordered → In Progress → Completed
- **Auto-generate charges when orders completed**
- Order results integration (HL7 ORU messages)

**Revenue impact:** Automatic charge capture prevents missed revenue (5-10% typically)

---

### Module 11: Charge Capture (Automated)
**Who uses it:** Clinical staff, billing team  
**What it does:** Convert every service into a billable charge  
**Key Features:**
- Manual charge entry (search CPT code, add to encounter)
- **Automatic charge capture from completed orders**
- Charge reconciliation (orders vs charges)
- Charge lag monitoring (time between service and charge entry)
- Charge hold/release for pending documentation
- **Missed charge detection** (AI-powered)
- Charge validation (valid CPT codes, units, modifiers)

**Revenue impact:** Missed charges = direct revenue loss (5-10% of revenue typically)

---

### Module 12: Medical Coding (AI-Assisted)
**Who uses it:** Medical coders  
**What it does:** Assign standardized codes to diagnoses and procedures  
**SLA/TAT:** Coding completed within 24 hours of encounter lock.  
**Key Features:**
- Coding worklist (encounters ready to code)
- Search ICD-10 (diagnosis codes) and CPT (procedure codes)
- Link diagnoses to procedures (medical necessity)
- DRG assignment for inpatient stays
- E&M level selection for office visits
- Encoder integration (3M, Optum)
- **AI-assisted coding suggestions** (OpenAI GPT-4)
- Code validation and compliance checks

**AI Feature: AI Medical Coding Assistant**
```python
# AI analyzes clinical notes and suggests codes
Input: "Patient presents with acute bronchitis, productive cough for 5 days. Prescribed antibiotics."

AI Output:
{
  "icd10_codes": [
    {"code": "J20.9", "description": "Acute bronchitis, unspecified", "confidence": 0.95},
    {"code": "R05", "description": "Cough", "confidence": 0.88}
  ],
  "cpt_codes": [
    {"code": "99213", "description": "Office visit, established patient", "confidence": 0.92}
  ],
  "reasoning": "Acute bronchitis is primary diagnosis. Office visit level 3 based on moderate complexity."
}
```

**Benefits:**
- ⚡ Reduces coding time from 10 minutes to 2 minutes
- ✅ 85-90% accuracy (always requires human review)
- 📚 Helps train new coders

**API Integration:**
- **OpenAI GPT-4 API** or **AWS Bedrock (Claude)**

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
- Medical necessity validation
- Modifier validation

**Compliance risk:** Upcoding/unbundling = fraud = fines/jail time

---

### Module 14: Claim Creation (Automated)
**Who uses it:** Billing team  
**What it does:** Generate insurance claim from coded encounter  
**SLA/TAT:** Claim generated within 12 hours of coding.  
**Key Features:**
- **Auto-generate CMS-1500** (professional) or **UB-04** (hospital) claim
- Populate all required fields from encounter data
- Include: Patient, insurance, provider NPIs, codes, charges
- Claim splitting (if >6 service lines on CMS-1500)
- **Generate EDI 837P/837I** format
- Claim preview (visual CMS-1500/UB-04 form)
- Bulk claim generation (1000+ claims in minutes)

**Tech Stack:**
- Python libraries for EDI 837 generation
- PostgreSQL tables: `claims`, `claim_lines`, `claim_diagnoses`

---

### Module 15: Claim Scrubbing & Error Prediction (AI-Powered)
**Who uses it:** Billing team  
**What it does:** Check claim for errors before submission  
**Key Features:**
- 200+ validation checks
- Check: Missing fields, invalid codes, NCCI edits, authorization, duplicates
- Error levels: Fatal (must fix), Warning (recommend fix), Info
- Clean claim indicator
- Bulk scrubbing (1000+ claims in <5 minutes)
- **AI Claim Error Prediction** (predict denial risk)

**AI Feature: Claim Error Prediction**
```python
# AI analyzes claim and predicts denial risk
Input: Claim with diagnosis J20.9, procedure 99215, no prior auth

AI Output:
{
  "risk_level": "High",
  "risk_score": 0.85,
  "issues": [
    {
      "issue": "CPT 99215 may not be supported by diagnosis J20.9",
      "severity": "High",
      "recommendation": "Consider CPT 99213 instead"
    },
    {
      "issue": "No prior authorization on file",
      "severity": "Medium",
      "recommendation": "Verify if prior auth required"
    }
  ]
}
```

**Benefits:**
- 🎯 Catch errors before submission
- 💰 Reduce denial rate from 10% to 5%
- ⚡ Faster claim resolution

**API Integration:**
- **Waystar Claim Scrubbing API**
- **OpenAI GPT-4** for AI prediction

**Goal:** 95%+ clean claim rate = fewer denials

---

### Module 16: Claim Submission (Electronic)
**Who uses it:** Billing team  
**What it does:** Send claims to insurance companies  
**SLA/TAT:** Claim submitted within 24 hours of generation.  
**Key Features:**
- **Clearinghouse integration** (Waystar, Availity, Change Healthcare)
- **EDI 837P** (professional claims) and **EDI 837I** (institutional claims)
- Batch submission (every 2 hours, configurable)
- **Real-time submission** (for urgent claims)
- Acknowledgment processing (EDI 999, EDI 277)
- Timely filing tracking (alert before deadline)
- Submission history and audit trail
- Failed submission retry logic

**API Integration:**
- **Waystar Claims API** (primary)
- **Availity API** (backup)

**Example API Call:**
```python
POST https://api.waystar.com/claims/v1/submit
{
  "claims": [{
    "claimId": "CLM-2026-001234",
    "ediContent": "ISA*00*...",  # Full EDI 837 content
    "payerId": "00431",
    "submissionDate": "2026-05-18"
  }]
}
```

**Timely filing:** Most payers require claims within 90-365 days of service

---

### Module 17: Claim Tracking & AR Follow-Up
**Who uses it:** Billing team / AR Team / Insurance Follow-Up Team  
**What it does:** Monitor claim status after submission and follow up on unpaid or pending insurance claims.  
**Key Features:**
- **Real-time claim status dashboard** (Submitted, Pending, Paid, Denied)
- Aging reports (0-30, 31-60, 61-90, 90+ days)
- **EDI 276/277 status inquiry** (automated daily checks)
- Payer portal integration and notes tracking
- AR worklists (claims pending >30/60/90 days)
- **Automated status updates** (WebSocket for real-time UI updates)
- Claim status alerts (email, SMS)
- Insurance follow-up tracking (calls, portal checks)
- Escalation management for unresolved claims
- Follow-up reminders and task assignment
- Resolution tracking (Paid / Reprocessed / Denied)
- Timely filing deadline monitoring
- Claim reprocessing tracking

**AI Feature:**
- AI predicts denial risk before aging increases
- Smart priority for high-value unpaid claims

**Tech Stack:**
- PostgreSQL tables: `ar_followup`, `claim_aging`, `followup_notes`
- Scheduler for reminder automation
- **Waystar Status API** (EDI 276/277)

**Common mistake:**
- No AR follow-up = delayed payment & increased Days in AR.

---

### Module 18: Payment Posting (ERA - Automated)
**Who uses it:** AR team  
**What it does:** Record insurance payments  
**SLA/TAT:** Payments posted within 48 hours of ERA receipt.  
**Key Features:**
- Import **EDI 835** (Electronic Remittance Advice)
- **Auto-posting** (match payment to claim automatically - 95% success rate)
- Manual posting (when auto-match fails)
- Adjustment reason codes (CARC/RARC)
- Underpayment/overpayment detection
- EFT reconciliation (match payment to bank deposit)
- **Batch ERA processing** (1000+ payments in <5 minutes)
- Payment variance analysis

**API Integration:**
- **Waystar Remittance API** (download ERA files)

**Adjustment types:**
- Contractual: Difference between billed and allowed amount
- Deductible: Patient's annual deductible
- Copay: Fixed patient payment
- Coinsurance: Patient's % share

**Tech Stack:**
- Python EDI 835 parser
- PostgreSQL tables: `claim_payments`, `payment_adjustments`

---

### Module 19: Denial & Appeals Management
**Who uses it:** Denial team  
**What it does:** Handle rejected claims and automate/manage appeals to insurance companies  
**SLA/TAT:** Appeals filed within 5 days of denial.  
**Key Features:**
- Denial tracking with reason codes
- Denial worklist (prioritize high $ denials)
- Root cause analysis (top denial reasons)
- **Appeal creation and tracking** (Level 1, 2, 3)
- **Automated appeal letter generation** (AI-powered)
- Corrected claim resubmission
- Appeal overturn rate tracking
- **Denial pattern analysis** (ML-based)
- **Predictive denial prevention** (flag before submission)
- Appeal template library
- Supporting document upload
- Appeal status tracking
- Appeal success analytics
- Denial reason categorization
- Appeal deadline tracking

**AI Feature: Automated Appeal Generation & Success Suggestion**
- AI suggests likely successful appeal reasons based on historical overturn rates
- Auto-generate appeal letter drafts:
```python
# AI generates appeal letter based on denial reason
Input: Claim denied for "Medical necessity not established"

AI Output:
"Dear [Payer],

We are writing to appeal the denial of claim [CLM-123] for patient [Name].

The claim was denied due to 'Medical necessity not established.' However, 
the patient's diagnosis of acute bronchitis (J20.9) clearly supports the 
medical necessity for an office visit (99213).

[Clinical justification with supporting documentation]

We respectfully request reconsideration of this claim.

Sincerely,
[Provider Name]"
```

**Tech Stack:**
- PostgreSQL tables: `appeals`, `appeal_documents`, `denials`
- OCR for denial letter reading (AWS Textract or OpenAI Vision API)

**Common denial reasons:**
- Missing authorization (30%)
- Incorrect coding (25%)
- Eligibility issues (20%)
- Timely filing (10%)
- Medical necessity (15%)

**Revenue impact & Common Mistake:**
- *Revenue impact:* 10-15% of claims denied, 60% recoverable through appeals
- *Common mistake:* Missing appeal deadline = permanent revenue loss.

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
- Coordination of Benefits (COB)

---

### Module 21: Patient Billing & Payment Collection
**Who uses it:** Patient accounts team  
**What it does:** Bill patients for their portion  
**Key Features:**
- Generate patient statements (monthly)
- Show: Total charges, insurance payments, patient responsibility
- Multiple delivery: Mail, email, patient portal
- **Payment processing** (credit card via Stripe, ACH, check, cash)
- Payment plans (installments)
- Point-of-service collections (collect copay at check-in)
- **Price transparency** (cost estimates before service)
- **Online payment portal** (patient self-service)
- Payment confirmation (email, SMS)

**API Integration:**
- **Stripe API** for credit card payments
- PCI-DSS compliant (Stripe handles card data)

**Example Stripe Integration:**
```python
import stripe

# Collect patient copay
payment_intent = stripe.PaymentIntent.create(
    amount=2500,  # $25.00 in cents
    currency="usd",
    payment_method_types=["card"],
    description="Copay for John Doe"
)
```

**Stripe Pricing:**
- 2.9% + $0.30 per transaction
- Example: $25 copay = $1.03 fee

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
- Payment negotiation tracking
- Settlement offers

**Compliance:** No Surprises Act limits collection practices

---

### Module 23: Reporting & Analytics (Advanced)
**Who uses it:** Management, finance team  
**What it does:** Track RCM performance with advanced analytics  

**Key Metrics (KPIs):**
- Clean claim rate (Target: >95%)
- Denial rate (Target: <5%)
- Days in AR (Target: <35 days)
- Net collection rate (Target: >95%)
- AR over 90 days (Target: <15%)
- Cost to collect (Target: <$0.05 per $1)

**Standard Reports:**
- Daily: Charges, payments, denials
- Weekly: Clean claim rate, denial rate
- Monthly: Revenue by department/provider/payer, AR aging
- Quarterly: Payer performance, denial trends
- Annual: Financial summary, compliance reports

**Advanced Analytics:**
- **Predictive analytics** (forecast revenue, denials)
- **Benchmarking** (compare to industry standards)
- **Custom report builder** (drag-and-drop)
- **Data visualization dashboards** (Chart.js, D3.js)
- **Executive dashboards** (C-suite metrics)
- **Trend analysis** (identify patterns over time)
- **Payer performance scorecards**

**Tech Stack:**
- PostgreSQL for data storage
- Python pandas for data analysis
- Chart.js for visualizations
- PDF export (ReportLab)
- Excel export (openpyxl)

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
- **No Surprises Act compliance** (price transparency)
- **Price Transparency Rule** (cost estimates)
- **21st Century Cures Act** (data blocking prevention)
- **SOC 2 Type II compliance**

**Audit Trail Includes:**
- User ID, action, timestamp, IP address
- Before/after values for data changes
- Failed login attempts
- Data exports and access

---

### Module 25: Interoperability
**Who uses it:** IT team  
**What it does:** Connect with other systems  
**Integrations:**
- **EMR/EHR** (HL7 v2, FHIR R4)
- **Lab systems** (HL7 ORM/ORU)
- **Radiology/PACS** (HL7 ORM/ORU, DICOM)
- **Pharmacy systems** (NCPDP)
- **Clearinghouses** (EDI 837, 835, 270/271, 276/277)
- **Payer portals** (API integration)
- **Patient portal** (FHIR API)
- **Health Information Exchange (HIE)**
- **CAQH** (provider credentialing)

**FHIR API Endpoints:**
- GET /Patient/{id}
- GET /Encounter/{id}
- GET /Condition/{id}
- GET /Procedure/{id}
- POST /Claim

---

### Module 26: AI & Machine Learning Features (NEW)
**Who uses it:** All users (behind the scenes)  
**What it does:** Leverage AI to improve efficiency and accuracy  

**AI Features:**

1. **AI-Assisted Medical Coding**
   - Analyzes clinical notes
   - Suggests ICD-10 and CPT codes
   - 85-90% accuracy
   - Saves 8 minutes per encounter

2. **Claim Error Prediction**
   - Predicts denial risk before submission
   - Identifies specific issues
   - Suggests corrections
   - Reduces denials by 50%

3. **OCR for Document Reading**
   - Scan insurance cards
   - Extract policy information
   - Auto-fill registration forms
   - Saves 2-3 minutes per patient

4. **AI Chatbot Support**
   - 24/7 user assistance
   - Answers billing questions
   - Guides users through workflows
   - Reduces support tickets by 30%

5. **Denial Pattern Analysis**
   - ML-based root cause analysis
   - Identifies trends and patterns
   - Recommends process improvements

6. **Predictive Analytics**
   - Forecast revenue
   - Predict denial rates
   - Identify at-risk claims

**API Integration:**
- **OpenAI GPT-4 API** (primary)
- **AWS Bedrock** (Claude, Llama) (alternative)
- **AWS Textract** (OCR)

**Cost Estimate:**
- OpenAI: $100-$200/month for 10,000 requests
- AWS Textract: $10/month for 500 documents

---

### Module 27: Revenue Integrity (NEW)
**Who uses it:** Revenue integrity team  
**What it does:** Prevent revenue leakage and ensure proper coding  
**Key Features:**
- **Charge capture validation** (ensure all services billed)
- **Undercoding detection** (identify missed revenue)
- **Charge master management** (maintain pricing)
- **Revenue leakage analysis** (identify gaps)
- **Compliance checks** (proper coding levels)
- **DRG validation** (inpatient coding accuracy)
- **Modifier usage analysis**
- **Charge reconciliation** (orders vs charges)

**Revenue Impact:**
- Typical revenue leakage: 5-10%
- Revenue integrity reduces to <2%
- For $50M hospital: $1.5M - $4M recovered annually

---

### Module 28: Patient Portal (NEW)
**Who uses it:** Patients  
**What it does:** Patient self-service portal  
**Key Features:**
- **Online appointment booking**
- **View bills and statements**
- **Make payments online** (credit card, ACH)
- **Upload insurance cards** via mobile
- **Secure messaging** with staff
- **View medical records** (FHIR integration)
- **Payment plan management**
- **Cost estimates** before service
- **Appointment reminders**
- **Download receipts and statements**

**Tech Stack:**
- React.js frontend
- FHIR API for data access
- Stripe for payments
- Mobile-responsive design

---

### Module 29: Mobile Application (NEW)
**Who uses it:** Staff and patients  
**What it does:** Mobile access to RCM system  
**Key Features:**
- **iOS and Android apps**
- **Mobile claim submission** (for staff)
- **Mobile payment posting** (for staff)
- **Patient mobile app** (view bills, pay, book appointments)
- **Push notifications**
- **Offline mode** (sync when online)
- **Mobile-optimized workflows**
- **Barcode scanning** (insurance cards, patient wristbands)

**Tech Stack:**
- React Native (cross-platform)
- Or: Native iOS (Swift) and Android (Kotlin)

---

### Module 30: Real-Time Dashboard & Notifications (NEW)
**Who uses it:** All users  
**What it does:** Real-time updates and alerts  
**Key Features:**
- **Real-time claim status updates** (WebSocket)
- **Live dashboard metrics** (auto-refresh every 30 seconds)
- **Push notifications** (browser, mobile)
- **Email alerts** (denials, payments, errors)
- **SMS alerts** (via Twilio)
- **Customizable alerts** (set thresholds)
- **Alert history and tracking**

**Tech Stack:**
- WebSocket for real-time updates
- Redis for pub/sub messaging
- Twilio for SMS
- SendGrid for email

---

## 3. Technology Stack (Detailed)

### Frontend
- **Framework:** React.js 18+ with TypeScript
- **Styling:** Tailwind CSS 3+
- **State Management:** React Query (for API calls), Context API
- **Routing:** React Router v6
- **Forms:** React Hook Form
- **Charts:** Chart.js or Recharts
- **UI Components:** shadcn/ui or Material-UI
- **Icons:** Lucide React
- **Build Tool:** Vite
- **Testing:** Jest, React Testing Library, Playwright

### Backend
- **Framework:** Python FastAPI 0.100+
- **ORM:** SQLAlchemy 2.0
- **Database Migrations:** Alembic
- **Authentication:** JWT (python-jose)
- **Password Hashing:** bcrypt
- **API Documentation:** Swagger UI (built-in)
- **Background Tasks:** Celery with Redis
- **Testing:** Pytest, pytest-asyncio

### Database
- **Primary:** PostgreSQL 15+
- **Caching:** Redis 7+
- **Search:** PostgreSQL full-text search (or Elasticsearch for advanced)
- **Backup:** Automated daily backups to S3

### Cloud Infrastructure (AWS)
- **Compute:** EC2 (t3.medium for MVP, scale to m5.large+)
- **Database:** RDS PostgreSQL (Multi-AZ for production)
- **Cache:** ElastiCache Redis
- **Storage:** S3 (documents, images, backups)
- **CDN:** CloudFront
- **Load Balancer:** Application Load Balancer (ALB)
- **Monitoring:** CloudWatch
- **Logging:** CloudWatch Logs
- **Secrets:** AWS Secrets Manager
- **Email:** SES (Simple Email Service)

### Third-Party APIs
- **Clearinghouse:** Waystar API (primary), Availity API (backup)
- **Payments:** Stripe API
- **SMS:** Twilio API
- **AI:** OpenAI GPT-4 API or AWS Bedrock
- **OCR:** AWS Textract or OpenAI Vision API
- **EHR:** FHIR APIs (Epic, Cerner, Allscripts)

### DevOps
- **Version Control:** Git (GitHub or GitLab)
- **CI/CD:** GitHub Actions or GitLab CI
- **Containerization:** Docker
- **Orchestration:** Docker Compose (MVP), Kubernetes (scale)
- **Infrastructure as Code:** Terraform or AWS CloudFormation
- **Monitoring:** Datadog or New Relic
- **Error Tracking:** Sentry

---

## 4. Performance Requirements

### Response Times
- **Page load:** <2 seconds (first contentful paint)
- **API response:** <500ms (95th percentile)
- **Insurance verification:** <30 seconds
- **Claim scrubbing:** 1000 claims in <5 minutes
- **ERA processing:** <1 minute per file
- **Database queries:** <100ms (simple), <500ms (complex)

### Scalability
- **Concurrent users:** 500+ (MVP), 5000+ (scale)
- **Claims per day:** 10,000+ (MVP), 100,000+ (scale)
- **Database size:** 1TB+ (5 years of data)
- **API rate limits:** 1000 requests/minute per user

### Availability
- **Uptime:** 99.9% (8.76 hours downtime per year)
- **Disaster recovery:** <4 hour RTO (Recovery Time Objective)
- **Backup frequency:** Daily automated backups
- **Backup retention:** 7 years (HIPAA requirement)

---

## 5. Security Requirements

### Data Encryption
- **At rest:** AES-256 encryption (AWS RDS, S3)
- **In transit:** TLS 1.2+ (HTTPS only)
- **Database:** Encrypted columns for PHI (SSN, DOB, etc.)
- **Backups:** Encrypted backups

### Authentication & Authorization
- **Multi-factor authentication (MFA):** Required for admin users
- **Single Sign-On (SSO):** SAML 2.0 support
- **JWT tokens:** 8-hour expiration, refresh tokens
- **Role-based access control (RBAC):** 10+ roles
- **IP whitelisting:** For admin access
- **Session management:** 15-minute timeout (configurable)

### Compliance
- **HIPAA:** Business Associate Agreement (BAA), encryption, audit logs
- **PCI-DSS:** For payment processing (Stripe handles card data)
- **SOC 2 Type II:** Annual audit
- **GDPR:** For international patients (if applicable)
- **No Surprises Act:** Price transparency
- **21st Century Cures Act:** Data blocking prevention

### Audit Logging
- **Log all user actions:** Create, read, update, delete
- **Retention:** 7 years (HIPAA requirement)
- **Log contents:** User ID, action, timestamp, IP address, before/after values
- **Tamper-proof:** Logs cannot be modified or deleted

### Penetration Testing
- **Frequency:** Annual (minimum)
- **Scope:** Full application, APIs, infrastructure
- **Remediation:** All critical/high vulnerabilities fixed within 30 days

---

## 6. User Roles & Permissions

| Role | Can Do |
|------|--------|
| **Front Desk** | Register patients, verify insurance, schedule appointments, collect copays, check-in patients |
| **Doctor** | Document visits, write orders, sign encounters, view patient records |
| **Nurse** | Document vitals, administer medications, view patient records |
| **Medical Coder** | Assign ICD/CPT codes, review documentation, use AI coding assistant |
| **Billing Specialist** | Create claims, scrub claims, submit claims, view claim status |
| **AR Manager** | Post payments, manage denials, follow up on aging claims, view AR reports |
| **Collections** | Bill patients, set up payment plans, send to collections, negotiate settlements |
| **Authorization Specialist** | Submit prior authorization requests, track authorization status |
| **Finance Manager** | View all reports, dashboards, financial analytics, export data |
| **Compliance Officer** | Audit logs, compliance reports, internal audits, coding audits |
| **System Admin** | User management, system configuration, role management, API keys |

---

## 7. Critical Business Rules

### Rule 1: Provider Credentialing
- Doctor MUST be credentialed with payer before billing
- If not credentialed → 100% claim rejection

### Rule 2: Insurance Verification
- MUST verify eligibility before service (within 24 hours)
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

### Rule 9: Coordination of Benefits (COB)
- Primary insurance MUST be billed first
- Secondary billed only after primary payment

### Rule 10: Price Transparency
- MUST provide cost estimates upon request (No Surprises Act)
- Good faith estimates for uninsured/self-pay patients

### Rule 11: Rejection vs Denial
- **Rejection:** Technical error *before* payer acceptance (handled by Billing).
- **Denial:** Coverage/Medical necessity issue *after* adjudication (handled by AR/Denials).

---

## 8. Revenue Cycle Flow (Detailed)

```
Pre-Service (Days -7 to 0)
1. Provider credentialed with insurance ✓
2. Patient schedules appointment
3. Automated appointment reminder sent (SMS/email)
4. Insurance verified 24-48 hours before appointment
5. Prior authorization obtained (if needed)
6. Cost estimate provided to patient

Day of Service (Day 0)
7. Patient checks in → Encounter created
8. Copay collected (Stripe payment)
9. Patient sees doctor → Clinical documentation
10. Services performed → Orders completed
11. Charges captured automatically

Post-Service (Days 1-5)
12. Medical coder assigns ICD/CPT codes (AI-assisted)
13. Claim created and auto-populated
14. Claim scrubbed for errors (AI error prediction)
15. Claim submitted to insurance (EDI 837)
16. Acknowledgment received (EDI 999)

Adjudication (Days 5-30)
17. Insurance reviews claim
18. Claim status checked automatically (EDI 276/277)
19. Insurance adjudicates and pays
20. ERA received (EDI 835)
21. Payment auto-posted to claim

Denial Management (If Denied)
22. Denial identified and categorized
23. Root cause analysis
24. Corrected claim or appeal submitted
25. Appeal tracking

Patient Billing (Days 30-60)
26. Patient statement generated
27. Statement sent (mail/email/portal)
28. Patient makes payment online (Stripe)
29. If overdue → Collection notices

Collections (Days 60-120)
30. Internal collections (phone calls)
31. Payment plan offered
32. If still unpaid → External collections
33. Bad debt write-off (last resort)
```

**Timeline Goal:** Service to payment in 30-35 days (vs industry 50+ days)

---

## 9. EDI Transaction Specifications

| EDI Code | Name | Purpose | Direction |
|----------|------|---------|-----------|
| **270** | Eligibility Inquiry | Check patient insurance eligibility | Outbound |
| **271** | Eligibility Response | Insurance eligibility results | Inbound |
| **276** | Claim Status Inquiry | Check status of submitted claim | Outbound |
| **277** | Claim Status Response | Claim status results | Inbound |
| **278** | Prior Authorization Request | Request authorization for service | Outbound |
| **278** | Prior Authorization Response | Authorization approval/denial | Inbound |
| **837P** | Professional Claim | Submit professional claim (CMS-1500) | Outbound |
| **837I** | Institutional Claim | Submit institutional claim (UB-04) | Outbound |
| **835** | ERA (Remittance Advice) | Payment information from insurance | Inbound |
| **999** | Acknowledgment | Confirm receipt of EDI transaction | Inbound |

**Clearinghouse:** Waystar or Availity handles EDI translation and routing

---

## 10. Common Mistakes & Prevention

| Mistake | Impact | Prevention | Module |
|---------|--------|------------|--------|
| Wrong insurance ID at registration | Claim denial | Real-time eligibility check, OCR scanning | Module 4, 5 |
| Missing prior authorization | 100% denial | Authorization tracking, alerts | Module 6 |
| Incomplete documentation | Coding errors, denials | CDI alerts for providers | Module 9 |
| Missed charges | Revenue loss (5-10%) | Charge reconciliation, AI detection | Module 11 |
| Wrong CPT code | Denial or underpayment | AI coding assistant, encoder | Module 12 |
| NCCI edit violation | Claim rejection | Claim scrubbing with NCCI checks | Module 15 |
| Late claim submission | Timely filing denial | Timely filing alerts, automated submission | Module 16 |
| Not appealing denials | Lost revenue (60% recoverable) | Denial worklists, appeal tracking | Module 19 |
| Undercoding | Revenue loss | Revenue integrity module, AI detection | Module 27 |
| Poor patient communication | Low collections | Patient portal, cost estimates | Module 28 |

---

## 11. Success Metrics & KPIs

### Before RCM System (Industry Average)
- Denial rate: 10-15%
- Days in AR: 50-60 days
- Clean claim rate: 75-80%
- Revenue leakage: 5-10%
- Net collection rate: 85-90%
- Cost to collect: $0.10-$0.15 per $1

### After RCM System (Target Goals)
- Denial rate: <5% ⚡
- Days in AR: <35 days ⚡
- Clean claim rate: >95% ⚡
- Revenue leakage: <2% ⚡
- Net collection rate: >95% ⚡
- Cost to collect: <$0.05 per $1 ⚡

### Financial Impact Example
**Hospital with $50M annual revenue:**
- Revenue leakage before: 5% = $2.5M lost
- Revenue leakage after: 2% = $1.0M lost
- **Annual recovery: $1.5M** 💰
- System cost: $500K (one-time) + $200K/year (maintenance)
- **ROI: System pays for itself in 6-12 months**

### AI Impact Metrics
- AI coding saves 8 min/encounter × 100 encounters/day = 13.3 hours/day
- AI error prediction reduces denials by 50% = $750K recovered annually
- OCR saves 2 min/patient × 100 patients/day = 3.3 hours/day
- **Total AI value: $1M+ annually**

---

## 12. Testing & Quality Assurance

### Testing Strategy
1. **Unit Testing**
   - Backend: Pytest (95%+ coverage)
   - Frontend: Jest, React Testing Library (90%+ coverage)

2. **Integration Testing**
   - API integration tests
   - Database integration tests
   - Third-party API mocks

3. **End-to-End Testing**
   - Playwright or Cypress
   - Complete workflow tests (patient → payment)

4. **Performance Testing**
   - Load testing (JMeter, Locust)
   - 500+ concurrent users
   - 10,000+ claims per day

5. **Security Testing**
   - Penetration testing (annual)
   - OWASP Top 10 vulnerabilities
   - SQL injection, XSS testing

6. **User Acceptance Testing (UAT)**
   - Real users test in staging
   - 2-week UAT period before launch
   - Feedback collection and bug fixes

### Test Environments
- **Development:** Local development
- **Staging:** Mirror of production (for testing)
- **Production:** Live system

---

## 13. Disaster Recovery & Backup

### Backup Strategy
- **Frequency:** Automated daily backups (3 AM)
- **Retention:** 7 years (HIPAA requirement)
- **Storage:** AWS S3 with versioning
- **Encryption:** AES-256 encrypted backups
- **Testing:** Monthly backup restore tests

### Disaster Recovery
- **RTO (Recovery Time Objective):** <4 hours
- **RPO (Recovery Point Objective):** <1 hour (last backup)
- **Multi-region:** Primary (us-east-1), DR (us-west-2)
- **Failover:** Automated DNS failover
- **Annual DR drill:** Full failover test

---

## 14. Cost Estimates

### Development Cost (MVP - 16 weeks)
- Frontend Developer (1): $128K
- Backend Developer (2): $256K
- AI Engineer (1): $128K
- QA Engineer (1): $96K
- DevOps Engineer (0.5): $64K
- Technical Lead (1): $160K
- **Total Team Cost:** $832K

### Infrastructure Cost (Monthly)
- AWS EC2 (t3.medium): $30
- AWS RDS PostgreSQL: $25
- AWS ElastiCache Redis: $15
- AWS S3 Storage: $5
- AWS CloudFront: $10
- **Total AWS:** ~$85/month

### Third-Party APIs (Monthly)
- Waystar: $500
- Stripe: Transaction-based (2.9% + $0.30)
- Twilio: $50
- OpenAI: $200
- AWS Textract: $10
- **Total APIs:** ~$760/month

### Total First Year Cost
- Development: $832K (one-time)
- Infrastructure: $1K/year
- APIs: $9K/year
- **Total Year 1:** ~$842K

### Ongoing Cost (Annual)
- Infrastructure: $1K
- APIs: $9K
- Maintenance: $200K (team)
- **Total Ongoing:** ~$210K/year

---

## 15. Implementation Roadmap

### Phase 1: MVP (Months 1-4)
- Modules 1-10, 12, 14-18, 23
- Core workflow: Patient → Claim → Payment
- Basic AI features (coding assistant)
- **Goal:** Launch with 3-5 pilot clinics

### Phase 2: Enhancement (Months 5-8)
- Modules 11, 19-22, 26
- Advanced AI features (error prediction, OCR)
- Denial management
- Patient billing
- **Goal:** 20-30 clinics

### Phase 3: Scale (Months 9-12)
- Modules 24, 25, 27-30
- Revenue integrity
- Patient portal
- Mobile app
- Advanced analytics
- **Goal:** 100+ clinics

### Phase 4: Enterprise (Year 2)
- Multi-location support
- Deep EHR integration
- International billing
- Advanced compliance
- **Goal:** Enterprise customers

---

## 16. Next Steps

1. ✅ **Review this requirements document** with stakeholders
2. ✅ **Finalize MVP scope** (which modules to include)
3. ✅ **Assemble development team** (6-7 people)
4. ✅ **Start Waystar API approval** (takes 2-4 weeks)
5. ✅ **Design database schema** (35+ tables)
6. ✅ **Create UI/UX wireframes** (all screens)
7. ✅ **Set up development environment** (AWS, Git, CI/CD)
8. ✅ **Begin Phase 1 development** (Week 1)

---

## 17. Questions for Discussion

1. **MVP Scope:** Should we include AI features in MVP or add later?
2. **Clearinghouse:** Waystar (broader coverage) or Availity (cheaper)?
3. **EHR Integration:** MVP or post-MVP?
4. **Mobile App:** MVP or post-MVP?
5. **Team:** In-house, contractors, or offshore?
6. **Budget:** Full team ($832K) or lean team ($400-500K)?
7. **Timeline:** 16 weeks realistic or need more time?
8. **Pilot Clinics:** Do we have 3-5 clinics ready to test?

---

**Document Prepared By:** AI Assistant  
**Version:** 2.0  
**Date:** May 18, 2026  
**Status:** Ready for Team Review

**Changes from v1.0:**
- ✅ Added 5 new modules (26-30)
- ✅ Added AI/ML features throughout
- ✅ Added specific API integrations (Waystar, Stripe, OpenAI, Twilio)
- ✅ Added detailed tech stack specifications
- ✅ Added performance requirements
- ✅ Added testing & QA section
- ✅ Added disaster recovery & backup
- ✅ Added cost estimates
- ✅ Added implementation roadmap
- ✅ Expanded all existing modules with more detail
