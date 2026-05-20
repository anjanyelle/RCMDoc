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

## 2. Foundational & Core Modules

### PRE-RCM / FOUNDATIONAL FLOW (4 Modules)
The Pre-RCM / Foundational Flow consists of 4 modules that prepare providers and insurance setups before the actual patient billing process starts.

#### Pre-RCM Module 1: Provider Management
**Who uses it:** Hospital Admin / System Admin  
**What it does:** Add and manage healthcare providers in the system before patient scheduling and billing begins.  
**Key Features:**
- Store provider NPI, licenses, certifications
- Store provider name, specialty, department, NPI number, license details, and experience
- Map providers to clinic locations and departments
- Provider profile management
- Document upload (provider licenses, certificates)
- Provider search interface
**Tech Stack:**
- PostgreSQL `providers`, `provider_specialties` tables
- NPI Registry API integration
**Common mistake:** Missing or invalid NPI number leading to initial claim validation failure.

---

#### Pre-RCM Module 2: Credentialing Management
**Who uses it:** Admin staff / Compliance Officer  
**What it does:** Verify provider qualifications and track credentialing status with various insurance payers.  
**Key Features:**
- Track medical licenses, board certifications, and education
- Automated alerts 90 days before credential or license expiration
- CAQH profile integration and status tracking
- Malpractice insurance tracking
- Provider status tracking
- License expiration alerts
**Tech Stack:**
- PostgreSQL `provider_licenses`, `provider_credentials` tables
- Email/notification service for expiration alerts
**Common mistake:** Letting medical licenses expire, causing 100% claim rejections.

---

#### Pre-RCM Module 3: Provider Enrollment
**Who uses it:** Admin staff / Enrollment Specialist  
**What it does:** Enroll providers with insurance companies for claim billing approval.  
**Key Features:**
- Payer-specific enrollment application tracking
- Enrollment status tracking (Pending, Approved, Rejected)
- Effective date and termination date tracking per payer
- Payer mapping to provider profiles
- Enrollment rejection handling
**Tech Stack:**
- PostgreSQL `provider_enrollment`, `payers` tables
- Celery tasks for enrollment status monitoring
**Common mistake:** Scheduling patients with a provider before enrollment approval is finalized.

---

#### Pre-RCM Module 4: Contract Management
**Who uses it:** Finance Manager / Practice Manager  
**What it does:** Manage reimbursement agreements, contracts, and custom fee schedules with insurance companies.  
**Key Features:**
- Digital storage of payer contracts and reimbursement rates
- Fee schedule management (procedure codes mapped to contracted rates)
- Contract renewal alerts and expiration tracking
- Underpayment detection rules based on contracted rates
- Track reimbursement rates per contract
**Tech Stack:**
- PostgreSQL `payer_contracts`, `fee_schedules` tables
- Redis cache for quick fee schedule lookups
**Common mistake:** Failing to update fee schedules in the billing system when new contracts are signed.

---

### Category 1: Patient Access Management (5 Modules)

#### Module 1: Appointment Scheduling
**Who uses it:** Front desk / Scheduling Team  
**What it does:** Schedule patient visits and manage provider calendars.  
**Key Features:**
- Provider calendars with availability templates
- Appointment types with custom durations
- Automated reminders (SMS via Twilio, email, phone)
- Waitlist and no-show tracking
- Calendar views (Day, Week, Month, drag-and-drop rescheduling)
- Rescheduling support
- Twilio integration for automated confirmations
**Tech Stack:**
- React.js frontend calendar component
- Python FastAPI calendar endpoints
- PostgreSQL `appointments`, `provider_schedules` tables
- Twilio API for SMS reminders
**Revenue impact:** SMS reminders reduce no-shows by 30% = less lost revenue.

---

#### Module 2: Patient Registration
**Who uses it:** Front desk (at check-in)  
**What it does:** Capture patient demographics, insurance info, and consent forms.  
**Key Features:**
- Form fields: Name, DOB, address, SSN, contact, emergency contacts
- Scan insurance card (AI-powered OCR extracts card details)
- Duplicate patient detection algorithm
- HIPAA consent forms with digital signature
- Patient photo upload
- Patient demographics search
**AI Feature:**
- Scan insurance card with phone camera, extract details via AWS Textract/OpenAI Vision API, auto-fill registration form (saves 2-3 minutes).
**Tech Stack:**
- AWS Textract or OpenAI Vision API for OCR
- PostgreSQL `patients`, `patient_insurance`, `patient_contacts` tables
**Common mistake:** Wrong insurance ID = claim denial.

---

#### Module 3: Insurance Eligibility Verification
**Who uses it:** Front desk (before appointment)  
**What it does:** Check if insurance is active and what the patient owes.  
**SLA/TAT:** Verification completed in <30 seconds.  
**Key Features:**
- Real-time eligibility check (EDI 270/271 via Waystar/Availity)
- Shows copay, deductible, coinsurance, and coverage limits
- Coordination of Benefits (primary vs. secondary)
- Cache results for 24 hours (Redis)
- Batch verification for scheduled appointments
**API Integration:**
- Waystar Eligibility API (primary), Availity API (backup). EDI 270 (inquiry) -> EDI 271 (response).
**Tech Stack:**
- Redis cache
- PostgreSQL `eligibility_checks` table
**Revenue impact:** Prevents treating patients with inactive insurance.

---

#### Module 4: Prior Authorization / Referral Management
**Who uses it:** Authorization team  
**What it does:** Get insurance approval before expensive procedures or specialist visits.  
**Key Features:**
- Identify services requiring authorization (by CPT code and payer)
- Submit authorization requests with clinical justification
- Track authorization number, approved units, and expiration date
- Automated authorization status checks (EDI 278)
- Authorization worklist (pending, approved, denied)
**Tech Stack:**
- EDI 278 transaction processor
- PostgreSQL `prior_authorizations` table
**Why critical:** Services without required authorization = 100% claim denial.

---

#### Module 5: Patient Check-In
**Who uses it:** Front desk / Patients (self-service kiosk)  
**What it does:** Confirm patient arrival, collect copays, check check-in status, and create encounter.  
**Key Features:**
- Confirm demographics and insurance are up-to-date
- Collect copays (Stripe integration)
- Update patient check-in status (Scheduled -> Checked In)
- Auto-populate patient, insurance, and provider info into encounter
- Queue management dashboard for clinical staff
**Tech Stack:**
- Stripe API for payment processing
- WebSockets for real-time check-in notifications
- PostgreSQL `encounters` table
**Common mistake:** Forgetting to collect copay at check-in (harder to collect after patient leaves).

---

### Category 2: Clinical & Mid-Cycle Management (3 Modules)

#### Module 6: Clinical Documentation / EMR
**Who uses it:** Doctors / Nurses  
**What it does:** Document the patient visit, write notes, and place orders.  
**Key Features:**
- Electronic medical record template system
- SOAP notes (Subjective, Objective, Assessment, Plan)
- Integrated CPT/ICD code search
- Order entry (lab tests, radiology, prescriptions)
- Electronic signature for note completion
- Encounter lock after signing (prevent unauthorized modifications)
- Document management integration for patient charts
**Tech Stack:**
- PostgreSQL `clinical_notes`, `orders`, `diagnoses`, `procedures` tables
- FHIR API for EHR integration (Epic, Cerner)
**Common mistake:** Incomplete or late clinical documentation leads to coding delays and claim denials.

---

#### Module 7: Medical Coding
**Who uses it:** Medical Coders  
**What it does:** Assign diagnosis (ICD-10) and procedure (CPT/HCPCS) codes based on doctor's notes.  
**SLA/TAT:** Codes assigned within 24 hours of encounter lock.  
**Key Features:**
- AI-assisted coding engine (reads clinical notes and suggests codes)
- Coding validation against NCCI edits and LCD/NCD rules
- Modifier management (-25, -59, etc.)
- Dual coding view (notes side-by-side with coding interface)
- Queries to providers for clarification
- Coding compliance and audit checks
**AI Feature:**
- LLM (OpenAI GPT-4 or AWS Bedrock) analyzes SOAP notes and extracts codes with confidence scores.
**Tech Stack:**
- PostgreSQL `medical_codes`, `ncci_edits` tables
- OpenAI GPT-4 API or AWS Bedrock
**Common mistake:** Upcoding (billing for higher service than provided) = fraud/audit risk.

---

#### Module 8: Charge Entry / Charge Capture
**Who uses it:** Billing team / AI engine  
**What it does:** Record billable services and map them to fee schedules.  
**Key Features:**
- Auto-generate charge lines from approved clinical codes
- Multi-facility fee schedule support
- Auto-calculate charge amount based on payer contract rules
- Charge reconciliation (matches clinical orders to billed charges)
- Missing charge detection algorithm
- Revenue integrity validation checks
**Tech Stack:**
- PostgreSQL `charges`, `fee_schedules` tables
- Celery tasks for auto-charge creation
**Revenue impact:** Catches missed charges (typically 5-10% of total revenue).

---

### Category 3: Claims Management (5 Modules)

#### Module 9: Claim Scrubbing
**Who uses it:** Billing team  
**What it does:** Check claims for errors before submitting to insurance.  
**Key Features:**
- Custom rule engine (validate patient info, subscriber ID format, NPIs)
- NCCI edit checking (detect unbundled codes)
- Payer-specific billing rules
- AI claim denial prediction (scores claims based on historical denial patterns)
- Error dashboard with direct correction tools
**AI Feature:**
- Machine learning model (XGBoost/LightGBM) trained on historical claim data predicts denial probability.
**Tech Stack:**
- Python pandas for rule processing
- Scikit-learn for denial prediction model
- PostgreSQL `claim_validation_rules`, `claim_errors` tables
**Success rate:** Target clean claim rate >95%.

---

#### Module 10: Claim Submission
**Who uses it:** Biller  
**What it does:** Submit claims electronically to insurance payers.  
**SLA/TAT:** Submissions completed daily.  
**Key Features:**
- Electronic claim generation (EDI 837 Professional and Institutional)
- Direct clearinghouse submission (Waystar, Availity)
- Batch claim processing (submitting hundreds of claims in one click)
- Submission logging and acknowledgment tracking (EDI 999)
- Timely filing deadline alerts
- Automated claim creation and validation
**Tech Stack:**
- Waystar Claims API / SFTP
- EDI 837 translation engine (Python)
- PostgreSQL `claims`, `claim_batches` tables
**Why critical:** Late submission = timely filing denial (100% loss).

---

#### Module 11: Clearinghouse Validation
**Who uses it:** Billing team  
**What it does:** Perform secondary validation and syntax checks at the clearinghouse level before claims reach payers.  
**Key Features:**
- Real-time clearinghouse integration (Waystar, Availity)
- Technical rejection queue (captures invalid formatting, wrong payer IDs)
- Syntax validation (compliance with EDI 5010 standards)
- Claim correction workflow (billers edit and resubmit within UI)
- Acknowledgment tracking (EDI 999 and 277CA)
**Tech Stack:**
- Waystar Claims and Rejections API
- WebSockets for instant rejection alerts
- PostgreSQL `clearinghouse_rejections` table
**Common mistake:** Ignoring clearinghouse rejections, meaning claims never reach the insurance company.

---

#### Module 12: Claim Status Tracking
**Who uses it:** Biller / AR team  
**What it does:** Track claim status automatically using EDI 276/277 transactions.  
**Key Features:**
- Automated status checks (EDI 276 requests sent every 3 days)
- Parse status responses (EDI 277) into clear categories (In Process, Approved, Rejected)
- Claim aging dashboard (current, 30 days, 60 days, 90+ days)
- Alerts for claims stuck in review status for >14 days
- Audit trail of claim status history
**Tech Stack:**
- Celery worker for scheduled EDI 276 requests
- PostgreSQL `claim_status_history` table
- Waystar Claim Status API
**Revenue impact:** Identifies delayed claims early, reducing Days in AR.

---

#### Module 13: Insurance Adjudication Tracking
**Who uses it:** Biller / AR team / Finance Manager  
**What it does:** Monitor how payers adjudicate claims, showing allowed amounts, patient responsibility, and contractual adjustments before payment posting.  
**Key Features:**
- Adjudication status monitoring (real-time tracking of claim processing status)
- Payer response tracking (interprets payer-specific adjudication codes)
- Medical necessity review visibility (flags claims held for clinical review)
- Contract rule validation (compares allowed amounts with contract fee schedules)
- Payer turnaround analytics (tracks average days from submission to adjudication decision)
**Tech Stack:**
- PostgreSQL `claim_adjudication` table
- Celery worker for daily adjudication checks via EDI 277
- Waystar Adjudication API integration
**Why critical:** Without adjudication tracking, you cannot detect underpayments or identify why claims are partially paid.

---

### Category 4: Payment & Revenue Management (7 Modules)

#### Module 14: ERA Processing
**Who uses it:** AR team / Finance team  
**What it does:** Retrieve and process Electronic Remittance Advice (EDI 835) files from clearinghouses.  
**Key Features:**
- Automated daily download of EDI 835 files
- Parse remittance data (payments, allowed amounts, co-insurance, copays)
- Reconcile ERA amounts with actual bank EFT deposits
- Denial code extraction (automatically routes denials to denial workflow)
- Rejection queue for ERA files that fail validation checks
**Tech Stack:**
- Python EDI 835 parsing library
- Waystar Remittance Auto-Download API
- PostgreSQL `era_files`, `reconciliation_logs` tables
**Common mistake:** Posting ERAs without EFT bank deposit confirmation, leading to reconciliation discrepancies.

---

#### Module 15: Payment Posting
**Who uses it:** AR team  
**What it does:** Post insurance payments and update balances.  
**SLA/TAT:** Payments posted within 24 hours of receipt.  
**Key Features:**
- Auto-match payments to claims using claim ID and patient info
- Post insurance payment, contractual adjustment, and patient balance
- Manual payment posting screen for paper checks (EOB scanning)
- Refund and credit balance management
- Daily posting reconciliation report
**Tech Stack:**
- PostgreSQL `payments`, `payment_details`, `adjustments` tables
- Redis cache for payment matching
**Success rate:** Auto-posting match rate goal >85%.

---

#### Module 16: Denial Management
**Who uses it:** Denial Specialist  
**What it does:** Manage claim denials, appeals, and corrections.  
**SLA/TAT:** Denials worked within 48 hours.  
**Key Features:**
- Auto-categorize denials by reason code (CO-50 medical necessity, CO-16 missing info)
- Appeal packet generator (merges claim data, denial code, and clinical notes)
- Corrected claim submission interface
- Denial tracking status (Pending Appeal, Appealed, Paid, Written Off)
- Payer denial trend analytics
**AI Feature:**
- AI suggests appeal letter templates and clinical evidence based on denial reason (saves 10 minutes/appeal).
**Tech Stack:**
- PostgreSQL `denials`, `appeals`, `denial_reason_codes` tables
- LLM (GPT-4) for auto-generating appeal letters
**Revenue impact:** Recovers 60% of denied revenue.

---

#### Module 17: Secondary Insurance Billing
**Who uses it:** Biller  
**What it does:** Bill secondary insurance after primary insurance pays.  
**Key Features:**
- Identify claims with active secondary insurance
- Auto-generate secondary claim (EDI 837) incorporating primary payment details (EDI 835)
- Attachment management (attaching primary EOB to secondary claim)
- Coordination of Benefits rules configuration
- Secondary claim status tracking
**Tech Stack:**
- PostgreSQL `secondary_claims` table
- EDI 837 secondary claim generator
**Common mistake:** Forgetting to attach primary EOB, causing secondary claim denial.

---

#### Module 18: Patient Billing
**Who uses it:** Patient billing staff  
**What it does:** Bill patients for remaining balances (copays, deductibles).  
**Key Features:**
- Patient statement generator (PDF statement layout)
- Electronic statement delivery (email, SMS with secure payment link)
- Paper statement batch generation for mailing
- Patient portal payment integration (Stripe)
- Flexible payment plans setup and tracking
- Custom installment reminders
**Tech Stack:**
- Python ReportLab for PDF statement generation
- Stripe API for payments
- SendGrid for email statements
- PostgreSQL `patient_statements`, `payment_plans` tables
**Success rate:** Patient portal payments increase patient collection rate by 25%.

---

#### Module 19: Accounts Receivable (AR) Follow-Up
**Who uses it:** AR Manager / Specialist  
**What it does:** Track aging accounts and manage collection follow-ups.  
**Key Features:**
- Interactive AR aging report (0-30, 31-60, 61-90, 91-120, 120+ days)
- Prioritized work queues (system sorts accounts by value and timely filing risk)
- Custom collector notes and follow-up reminders
- Custom follow-up actions log
- Write-off approvals and adjustment management
**Tech Stack:**
- PostgreSQL `ar_notes`, `ar_queues` tables
- React.js interactive charts and grids
**Goal:** Keep average Days in AR under 35 days.

---

#### Module 20: Collections / Refund / Write-Off Management
**Who uses it:** Collections Specialist / Finance team  
**What it does:** Manage collections, refunds, and financial adjustments.  
**Key Features:**
- Automated collection routing (claims to collections after 90 days)
- Refund request initiation and approval workflow
- Refund payment processing (Stripe refund or paper check generation)
- Small balance write-off batch utility
- Collection agency data export integration
**Tech Stack:**
- PostgreSQL `refunds`, `write_offs` tables
- Stripe API for refunds
**Common mistake:** Keeping credit balances/overpayments, which violates federal 60-day refund rules.

---

### Category 5: Reporting, Compliance & Governance (2 Modules)

#### Module 21: Reporting & Analytics
**Who uses it:** Finance Manager / Practice Manager  
**What it does:** Provide dashboards and financial reports to monitor revenue cycle health.  
**Key Features:**
- Standard reports (Net Collections, Days in AR, Denial Rate, Charge vs. Payment)
- Custom report builder (drag-and-drop fields, filters)
- Real-time KPI dashboard (auto-refresh)
- Export functionality (Excel, CSV, PDF)
- Scheduled reports emailed automatically to stakeholders
**Tech Stack:**
- Python pandas for data aggregation
- PostgreSQL reporting views and read-replicas
- Chart.js / Recharts for visualizations
**Revenue impact:** Highlights operational bottlenecks to recover lost revenue.

---

#### Module 22: Compliance & Audit
**Who uses it:** Compliance Officer  
**What it does:** Maintain HIPAA compliance and track system access.  
**Key Features:**
- Immutable audit logs (tracks every time PHI is viewed, edited, or deleted)
- Access monitoring dashboard (detects unusual access patterns, e.g. after-hours access)
- Automated compliance reports for audits
- Security alert logs (MFA bypass attempts, failed logins)
- Document version auditing
- Coding compliance checks and documentation standards audit
**Tech Stack:**
- PostgreSQL `audit_logs` table (read-only, write-once schema)
- AWS CloudTrail and CloudWatch integrations
**Why critical:** Failing audit logs = HIPAA non-compliance and heavy fines.

---

### Category 6: Administration & Platform Services (11 Modules)

#### Module 23: User Login & Authentication
**Who uses it:** All users  
**What it does:** Secure user login and authentication.  
**Key Features:**
- Secure password-based authentication (bcrypt)
- Multi-factor authentication (MFA) enforcement (SMS, Authenticator App)
- Single Sign-On (SSO) support (SAML 2.0, OpenID Connect)
- Automatic session timeout after 15 minutes of inactivity
- Password reset and account recovery workflow
**Tech Stack:**
- AWS Cognito or Auth0
- FastAPI OAuth2 password grant
- JWT tokens (8-hour expiration)
**Security requirement:** Essential for HIPAA compliance.

---

#### Module 24: User Management
**Who uses it:** System Admin  
**What it does:** Manage user profiles, roles, permissions, and multi-tenant configurations.  
**Key Features:**
- Role-based access control (RBAC) with 10+ predefined roles
- User creation, deactivation, and profile management
- Department and location access restrictions
- Temporary permission delegation
- Detailed user activity history dashboard
- Tenant-wise data isolation and hospital configuration settings
**Tech Stack:**
- PostgreSQL `users`, `roles`, `permissions`, `user_roles` tables
- React.js admin interface
**Common mistake:** Leaving inactive employee accounts open.

---

#### Module 25: Notification System
**Who uses it:** Staff and patients  
**What it does:** Send automated alerts and reminders.  
**Key Features:**
- Multi-channel notification delivery (SMS, email, in-app push)
- Real-time in-app alerts (WebSockets)
- Customizable staff notification preferences
- Patient appointment and payment reminders
- Automated delivery tracking (delivered, opened, failed)
**Tech Stack:**
- Twilio API for SMS
- SendGrid API for emails
- Firebase Cloud Messaging (FCM) for push notifications
- WebSockets (FastAPI) for in-app alerts
- PostgreSQL `notifications` log table
**Common mistake:** Sending notifications containing unencrypted PHI.

---

#### Module 26: Document Management
**Who uses it:** Front desk / Coders / Compliance  
**What it does:** Securely store and retrieve patient documents.  
**Key Features:**
- HIPAA-compliant document upload and storage
- Document classification tags (ID, Insurance Card, Consent, Clinical Note)
- Text search within scanned documents (OCR metadata indexing)
- Secure download links with expiration (S3 pre-signed URLs)
- Version control for updated forms
**Tech Stack:**
- AWS S3 bucket with server-side encryption (AES-256)
- AWS Textract / Tesseract OCR
- PostgreSQL `documents` metadata table
**Why critical:** Publicly readable S3 buckets containing patient documents lead to catastrophic security breaches.

---

#### Module 27: Third-Party Integrations
**Who uses it:** System Admin / Tech Team  
**What it does:** Manage external API connections and integrations.  
**Key Features:**
- Centralized API key and credentials manager (encrypted)
- Payer API connections (Waystar, Availity)
- EHR connection manager (HL7/FHIR integrations)
- Payment gateway manager (Stripe)
- API call log and error monitoring dashboard
- Interoperability protocol support (HL7, FHIR, DICOM)
**Tech Stack:**
- AWS Secrets Manager for credential storage
- Celery tasks for background syncs
- PostgreSQL `integration_logs` table
**Common mistake:** Hardcoding API keys in codebase.

---

#### Module 28: Patient Portal
**Who uses it:** Patients / Portal Admin  
**What it does:** Self-service portal for patients to view bills and pay.  
**Key Features:**
- Patient registration and portal login (SSO options)
- Interactive billing statement viewer
- Secure online payment portal (Stripe integration)
- Insurance card photo upload
- Setup payment plans and update payment methods
- iOS and Android mobile app portal support
- Push notifications and billing alerts
**Tech Stack:**
- React.js responsive web application / React Native for mobile app components
- Stripe elements checkout
- PostgreSQL `patient_portal_users`, `portal_payments` tables
**Success rate:** Saves admin time and increases patient payment collections by 30%.

---

#### Module 29: Revenue Cycle Dashboard
**Who uses it:** Practice Manager / Executives  
**What it does:** Real-time KPI visualization dashboard.  
**Key Features:**
- Live revenue cycle metrics (Gross charges, payments, denials, AR balance)
- Interactive visual charts (bar, line, pie)
- Multi-facility and provider performance comparison view
- Real-time WebSockets connection for live updates
- Export dashboard views as PDF/images
**Tech Stack:**
- Recharts / Chart.js in React.js
- FastAPIs with PostgreSQL read-replicas
- Redis cache for aggregated dashboard data
**Success rate:** High visibility enables quick recovery of bottlenecked accounts.

---

#### Module 30: Automated Workflows
**Who uses it:** Billing Manager / Admin  
**What it does:** Automate task routing and RCM business rules.  
**Key Features:**
- Workflow rule builder (define triggers, conditions, and actions)
- Automatic task routing (assign denials to specific specialists)
- System action automation (send payment reminder after 30 days)
- Claim hold/release engine (e.g., hold claim if missing modifier)
- Bottleneck tracking reports
**Tech Stack:**
- Python rule engine library
- Celery background tasks
- PostgreSQL `workflow_rules`, `workflow_tasks` tables
**Success rate:** Reduces manual claim handling time by 40%.

---

#### Module 31: Data Import/Export
**Who uses it:** System Admin / Finance Manager  
**What it does:** Bulk import historical billing data and export reports.  
**Key Features:**
- Bulk CSV/Excel data import (patients, providers, fee schedules)
- Data import validation engine (checks formatting, constraints, and duplicates)
- Custom data exporter (select columns, formats, and download)
- Scheduled automated exports to SFTP/S3
- Process progress bar and error log downloads
**Tech Stack:**
- pandas and openpyxl Python libraries
- Celery tasks for long-running imports/exports
- PostgreSQL copy/bulk insert queries
**Common mistake:** Importing dirty Excel data without validation, crashing system tables.

---

#### Module 32: System Configuration
**Who uses it:** System Admin / Practice Manager  
**What it does:** Manage system settings, billing configurations, fee schedules, and master lists.  
**Key Features:**
- Practice info and location configuration
- Fee schedule master list configuration
- Claim scrubbing rules builder
- Payer information and address settings
- Email templates and system-wide default configurations
**Tech Stack:**
- PostgreSQL `system_settings`, `payer_profiles`, `master_fee_schedules` tables
- React.js administration panels
**Common mistake:** Misconfiguring billing rules, causing widespread claim rejections.

---

#### Module 33: Backup & Recovery
**Who uses it:** System Admin / DevOps  
**What it does:** Automated backups and system restore monitoring.  
**Key Features:**
- Automated daily database backups (run at 3 AM)
- Multi-region backup redundancy (Primary: us-east-1, Backup: us-west-2)
- Incremental transaction logs backup (every 4 hours)
- Monthly automated backup restore drill and validation logs
- Disaster recovery failover dashboard (automated DNS failover)
**Tech Stack:**
- AWS RDS automated backups + cross-region replication
- AWS Route 53 failover DNS
- Python recovery scripts validation
**Common mistake:** Never testing backup restoration, only to find backups are corrupt when disaster strikes.

---

### Category 7: Advanced Enterprise Features (4 Modules)

#### Module 34: Eligibility Batch Processing
**Who uses it:** Scheduling / Front Desk  
**What it does:** Batch verification of insurance eligibility for all scheduled patients.  
**Key Features:**
- Bulk eligibility verification (runs automated EDI 270 queries in batches)
- Scheduled batch jobs (nightly or weekly schedules)
- Overnight processing for next-day appointments
- Exception reporting (flags patients with inactive coverage or failed inquiries)
- Automatic coverage updates in patient profiles
**Tech Stack:**
- Celery background tasks with Redis queue
- Waystar Bulk Eligibility API (EDI 270/271 batch integration)
- PostgreSQL `patient_eligibility_batches` table
**Common mistake:** Running batch checks during peak hours, causing API rate limit issues.

---

#### Module 35: ERA Automation
**Who uses it:** AR team / Finance team  
**What it does:** Automate ERA download, payment auto-posting, and reconciliation.  
**Key Features:**
- Automatic ERA download (fetches EDI 835 files from clearinghouse daily)
- Auto-posting engine (automatically matches and posts payments to patient accounts)
- Reconciliation automation (reconciles ERA amounts with actual bank EFT deposits)
- Adjustment automation (automatically applies contractual adjustments based on payer contract rules)
- Denial extraction (automatically pulls denial codes and redirects them to the Denial Management worklist)
**Tech Stack:**
- Python EDI 835 parsing library
- Waystar Remittance Auto-Download API
- PostgreSQL `era_files` and `reconciliation_logs` tables
**Common mistake:** Posting ERAs without EFT bank deposit confirmation, leading to reconciliation discrepancies.

---

#### Module 36: API Management
**Who uses it:** System Admin / Tech Team  
**What it does:** Manage external APIs, connections, usage metrics, and credential configurations.  
**Key Features:**
- Central API gateway and authentication key management
- Usage metrics and API call logs monitoring
- Automatic alerts for API endpoint downtime
- Payer connectivity manager (Epic/Cerner FHIR APIs, Waystar APIs, Stripe API)
- Access permission configuration for third-party API integrations
**Tech Stack:**
- Kong API Gateway or AWS API Gateway
- PostgreSQL `api_keys`, `api_logs` tables
**Common mistake:** Not logging API calls, making troubleshooting connection issues extremely difficult.

---

#### Module 37: Security & Compliance Monitoring
**Who uses it:** Compliance Officer / DevOps  
**What it does:** Active monitoring of compliance violations and security events.  
**Key Features:**
- Real-time threat detection (monitors unauthorized access, massive PHI exports)
- Automatic alerts for HIPAA violations
- Annual security audit report generation helper
- Access history visualizer (tracks user IP, device, location, and session activity)
- Multi-factor authentication compliance tracker
**Tech Stack:**
- AWS GuardDuty, CloudTrail, AWS WAF
- PostgreSQL `security_alerts`, `compliance_violations` tables
**Why critical:** Lack of compliance monitoring makes audit verification impossible.


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
| Wrong insurance ID at registration | Claim denial | Real-time eligibility check, OCR scanning | Module 2, 3 |
| Missing prior authorization | 100% denial | Authorization tracking, alerts | Module 4 |
| Incomplete documentation | Coding errors, denials | CDI alerts for providers | Module 6 |
| Missed charges | Revenue loss (5-10%) | Charge reconciliation, AI detection | Module 8 |
| Wrong CPT code | Denial or underpayment | AI coding assistant, encoder | Module 7 |
| NCCI edit violation | Claim rejection | Claim scrubbing with NCCI checks | Module 9 |
| Late claim submission | Timely filing denial | Timely filing alerts, automated submission | Module 10 |
| Not appealing denials | Lost revenue (60% recoverable) | Denial worklists, appeal tracking | Module 16 |
| Undercoding | Revenue loss | Revenue integrity logic, AI detection | Module 7, 8 |
| Poor patient communication | Low collections | Patient portal, cost estimates | Module 18, 28 |


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
- Pre-RCM Modules 1-4
- Main Modules 1-3, 5-8, 10, 12, 14-16, 18, 19, 21
- Core workflow: Patient → Claim → Payment
- Basic AI features (coding assistant)
- **Goal:** Launch with 3-5 pilot clinics

### Phase 2: Enhancement (Months 5-8)
- Main Modules 4, 9, 11, 13, 17, 20, 22-24, 26, 32
- Advanced AI features (error prediction, OCR)
- Denial management
- Patient billing
- **Goal:** 20-30 clinics

### Phase 3: Scale (Months 9-12)
- Main Modules 25, 27-29, 30, 31, 33-37
- Revenue cycle dashboard
- Patient portal
- Advanced analytics
- **Goal:** 100+ clinics

### Phase 4: Enterprise (Year 2)
- Multi-location support
- Deep EHR integration
- International billing
- Advanced compliance
- **Goal:** Enterprise customers


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
- ✅ Added Pre-RCM Foundational Flow (4 Modules)
- ✅ Added 12 new modules (26-37) to complete 37 modules in total
- ✅ Re-mapped all 37 modules in exact sequence matching the Complete Application Guide
- ✅ Added AI/ML features throughout
- ✅ Added specific API integrations (Waystar, Stripe, OpenAI, Twilio)
- ✅ Added detailed tech stack specifications
- ✅ Added performance requirements
- ✅ Added testing & QA section
- ✅ Added disaster recovery & backup
- ✅ Added cost estimates
- ✅ Added implementation roadmap
- ✅ Expanded all existing modules with more detail
