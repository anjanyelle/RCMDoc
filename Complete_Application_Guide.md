# Healthcare RCM Application - Complete Guide for Everyone
## Understanding the Entire System from Start to Finish

**Version:** 1.0  
**For:** Everyone - Technical & Non-Technical Readers  
**Purpose:** Understand the complete application, every feature, every flow

---

## 🎯 What is This Application?

### Simple Explanation:
Imagine a hospital or clinic. When you visit a doctor:
1. You register at the front desk
2. They check your insurance
3. Doctor treats you
4. Hospital sends bill to insurance
5. Insurance pays the hospital
6. You pay remaining amount

**This entire process takes 60-90 days and has many errors.**

**Our Application:** Automates this entire process and reduces time to 5-7 days with 95%+ accuracy.

---

## 📖 Complete Patient Journey (Real Example)

### Meet Sarah Johnson
- Age: 41 years old
- Problem: Cough and fever for 3 days
- Insurance: Blue Cross Blue Shield

### Step-by-Step Journey Through Our Application:

#### **Step 1: Patient Registration (3 minutes)**
**What Happens:**
- Sarah walks into clinic
- Front desk staff opens our application
- Enters Sarah's information:
  - Name, Date of Birth, Address, Phone
  - Takes photo of insurance card
  - Our AI reads the card automatically (OCR)
  - System checks if Sarah visited before (duplicate check)

**Behind the Scenes:**
- Data saved in database
- Insurance card scanned using AWS Textract
- Duplicate patient check runs
- Patient ID generated: PAT-2024-001234

**Screen:** Patient Registration Form
**Time:** 3 minutes (vs 10 minutes manual)

---

#### **Step 2: Insurance Verification (30 seconds)**
**What Happens:**
- Staff clicks "Verify Insurance" button
- System connects to insurance company
- Gets real-time eligibility information

**Result Shown:**
- ✅ Insurance Active
- Copay: $25
- Deductible Remaining: $700
- Coverage: 80% after deductible

**Behind the Scenes:**
- EDI 270 request sent to Waystar/Availity
- EDI 271 response received
- Data parsed and displayed
- Saved to database

**Screen:** Insurance Verification Dashboard
**Time:** 30 seconds (vs 15 minutes phone call)

---

#### **Step 3: Appointment Scheduling (1 minute)**
**What Happens:**
- Staff opens calendar
- Selects available slot: May 20, 10:00 AM
- Assigns doctor: Dr. Smith
- Books appointment

**Automatic Actions:**
- SMS reminder sent to Sarah: "Appointment on May 20 at 10 AM"
- Email confirmation sent
- Doctor's calendar updated
- Reminder set for 24 hours before

**Behind the Scenes:**
- Appointment saved in database
- Twilio API sends SMS
- Email service sends confirmation
- Calendar slot marked as booked

**Screen:** Appointment Calendar
**Time:** 1 minute

---

#### **Step 4: Patient Check-in (2 minutes)**
**What Happens (May 20, 9:55 AM):**
- Sarah arrives at clinic
- Uses self-service kiosk OR front desk
- Confirms personal information
- Signs consent forms digitally
- Pays $25 copay via credit card

**Behind the Scenes:**
- Check-in status updated
- Payment processed via Stripe
- Receipt generated
- Doctor notified patient is ready
- Queue updated

**Screen:** Check-in Kiosk / Front Desk Dashboard
**Time:** 2 minutes

---

#### **Step 5: Doctor Consultation (20 minutes)**
**What Happens:**
- Dr. Smith examines Sarah
- Diagnosis: Acute Bronchitis
- Prescribes: Antibiotics
- Doctor enters notes in system

**Doctor Enters:**
- Chief Complaint: "Cough and fever for 3 days"
- Examination findings
- Diagnosis: Acute Bronchitis
- Treatment Plan: Antibiotics, rest, fluids
- Prescription: Amoxicillin 500mg

**Behind the Scenes:**
- Clinical notes saved
- Prescription sent to pharmacy
- Encounter marked complete
- Ready for coding

**Screen:** Doctor's EHR Interface
**Time:** 20 minutes

---

#### **Step 6: Medical Coding with AI (3 minutes)**
**What Happens:**
- Medical coder opens Sarah's encounter
- AI analyzes doctor's notes
- AI suggests codes automatically

**AI Suggestions:**
- **ICD-10 Code:** J20.9 (Acute bronchitis, unspecified)
- **CPT Code:** 99203 (Office visit, new patient, moderate complexity)
- **Charge:** $150

**Coder Reviews:**
- Checks AI suggestions
- Confirms codes are correct
- Approves codes
- Adds modifiers if needed

**Behind the Scenes:**
- OpenAI GPT-4 analyzes clinical notes
- Code suggestions generated
- Coder reviews and approves
- Codes linked to encounter
- Charge amount calculated from fee schedule

**Screen:** Medical Coding Dashboard with AI Suggestions
**Time:** 3 minutes (vs 15 minutes manual)

---

#### **Step 7: Charge Capture (1 minute)**
**What Happens:**
- System automatically links codes to charges
- Looks up contracted rate with Blue Cross
- Calculates expected payment

**Calculation:**
- Service: Office Visit (99203)
- Standard Charge: $150
- Contracted Rate with Blue Cross: $120
- Patient Copay (already collected): $25
- Expected Insurance Payment: $95

**Behind the Scenes:**
- Charge master lookup
- Contract rate verification
- Charge created and linked to encounter
- Ready for claim creation

**Screen:** Charge Capture Summary
**Time:** Automatic (1 minute to review)

---

#### **Step 8: Claim Creation (1 minute)**
**What Happens:**
- Billing staff clicks "Create Claim"
- System auto-generates claim form
- All information pre-filled

**Claim Includes:**
- Patient: Sarah Johnson
- Insurance: Blue Cross Blue Shield
- Provider: Dr. Smith
- Diagnosis: J20.9
- Procedure: 99203
- Charge: $120 (contracted rate)
- Date of Service: May 20, 2024

**Behind the Scenes:**
- EDI 837 file generated
- CMS-1500 form created
- All required fields validated
- Claim ID assigned: CLM-2024-567890

**Screen:** Claim Creation Form (Auto-filled)
**Time:** 1 minute (vs 10 minutes manual)

---

#### **Step 9: Claim Scrubbing with AI (30 seconds)**
**What Happens:**
- AI checks claim for errors before submission
- Validates all fields
- Checks for common denial reasons

**AI Checks:**
- ✅ Patient demographics correct
- ✅ Insurance policy active
- ✅ Diagnosis code valid
- ✅ Procedure code matches diagnosis
- ✅ Modifiers correct
- ✅ All required fields present
- ✅ No duplicate claim

**Result:** ✅ Claim Ready to Submit (95% clean claim score)

**Behind the Scenes:**
- AI validation engine runs 50+ checks
- Waystar clearinghouse pre-validation
- Error prediction algorithm
- Claim marked as "Ready"

**Screen:** Claim Scrubbing Dashboard
**Time:** 30 seconds automatic

---

#### **Step 10: Claim Submission (30 seconds)**
**What Happens:**
- Billing staff clicks "Submit Claim"
- Claim sent to insurance electronically
- Immediate acknowledgment received

**Submission:**
- Claim sent to Waystar clearinghouse
- Waystar forwards to Blue Cross Blue Shield
- Acknowledgment (ACK) received: "Claim accepted"
- Tracking number assigned

**Behind the Scenes:**
- EDI 837 file transmitted
- Waystar API processes claim
- ACK/NAK response received
- Claim status updated to "Submitted"
- Tracking started

**Screen:** Claim Submission Dashboard
**Time:** 30 seconds

---

#### **Step 11: Claim Tracking (Automatic - 5 days)**
**What Happens:**
- System automatically checks claim status daily
- Updates status in real-time

**Status Updates:**
- Day 1: Submitted
- Day 2: Received by Payer
- Day 3: In Adjudication
- Day 5: Approved for Payment

**Behind the Scenes:**
- EDI 276 status inquiry sent daily
- EDI 277 status response received
- Status updated in database
- Alerts sent if issues detected

**Screen:** Claim Tracking Dashboard
**Time:** Automatic monitoring

---

#### **Step 12: Payment Posting (1 minute)**
**What Happens (Day 5):**
- Insurance processes claim
- Payment sent electronically (ERA/835)
- System auto-posts payment

**Payment Details:**
- Claim Amount: $120
- Insurance Paid: $95
- Patient Responsibility: $25 (already collected)
- Adjustment: $25 (contractual)

**Behind the Scenes:**
- ERA/835 file received from Waystar
- Payment auto-posted to patient account
- Adjustment codes applied
- Account balanced
- Receipt generated

**Screen:** Payment Posting Dashboard
**Time:** 1 minute (automatic posting)

---

#### **Step 13: Account Reconciliation (Automatic)**
**What Happens:**
- System checks if account is balanced
- All payments received
- No outstanding balance

**Sarah's Account Summary:**
- Total Charge: $150
- Contractual Adjustment: -$30
- Insurance Payment: $95
- Patient Copay: $25
- Balance: $0 ✅

**Behind the Scenes:**
- Account reconciliation runs
- All transactions verified
- Account closed
- Archived for records

**Screen:** Patient Account Summary
**Status:** Complete ✅

---

## ⏱️ Total Time: 5 Days from Visit to Payment

**Traditional Process:** 30-45 days  
**Our Application:** 5 days  
**Time Saved:** 85%

**Error Rate:**
- Traditional: 15-20% claims denied
- Our Application: <5% claims denied

---

## 🏗️ Complete Application Architecture

### The Application Has 38 Modules Organized in 7 Categories:

#### **Category 1: Front-End Patient Access Management (5 Modules)**

##### **Module 1: Appointment Scheduling**
This module manages patient appointments, provider calendars, and visit scheduling. It supports walk-ins, rescheduling, and automated reminders to reduce no-shows.
* **Features:**
  * Appointment booking
  * Provider calendar management
  * SMS/email reminders
  * Rescheduling support
  * No-show tracking

##### **Module 2: Patient Registration**
This module captures patient demographics, insurance information, emergency contacts, and consent forms before treatment.
* **Features:**
  * Demographic data entry
  * Insurance information capture
  * Patient ID generation
  * Emergency contacts
  * Duplicate patient detection

##### **Module 3: Insurance Eligibility Verification**
This module verifies patient insurance coverage in real time using EDI 270/271 transactions.
* **Features:**
  * Real-time eligibility verification
  * Copay and deductible checking
  * Coverage validation
  * Multi-payer support
  * Eligibility history tracking

##### **Module 4: Prior Authorization / Referral Management**
This module obtains approval from insurance companies before expensive procedures, specialist visits, or inpatient admissions.
* **Features:**
  * Authorization request submission
  * Referral tracking
  * Approval status monitoring
  * Authorization expiry tracking
  * Payer communication

##### **Module 5: Patient Check-In**
This module confirms patient arrival, verifies information, collects copays, and updates patient queue status.
* **Features:**
  * Front-desk check-in
  * Self-service kiosk support
  * Digital consent forms
  * Copay collection
  * Queue management

#### **Category 2: Clinical & Mid-Cycle Management (3 Modules)**

##### **Module 6: Clinical Documentation / EMR**
This module stores doctor notes, diagnoses, prescriptions, lab orders, and treatment plans inside the Electronic Medical Record system.
* **Features:**
  * Doctor notes management
  * Diagnosis documentation
  * Prescription records
  * Lab/radiology orders
  * Treatment plan tracking

##### **Module 7: Medical Coding**
This module converts clinical documentation into ICD-10, CPT, and HCPCS medical billing codes for insurance claim generation.
* **Features:**
  * ICD-10 coding
  * CPT/HCPCS coding
  * AI-assisted coding suggestions
  * Coding validation
  * Modifier management

##### **Module 8: Charge Entry / Charge Capture**
This module records billable services, procedures, medications, and provider charges for claim generation.
* **Features:**
  * Procedure charge entry
  * Fee schedule management
  * Modifier support
  * Automated charge capture
  * Charge validation

#### **Category 3: Claims Management (4 Modules)**

##### **Module 9: Claim Scrubbing**
This module validates claims before submission to reduce claim rejection and denial rates.
* **Features:**
  * Claim validation rules
  * Error detection
  * Missing information alerts
  * Code compatibility checks
  * Pre-submission review

##### **Module 10: Claim Submission**
This module electronically submits claims to insurance companies using EDI 837 transactions.
* **Features:**
  * EDI 837 claim submission
  * Clearinghouse integration
  * Batch claim processing
  * Submission tracking
  * Rejection handling

##### **Module 11: Clearinghouse Validation**
This module validates claims through clearinghouses before claims reach insurance payers.
* **Features:**
  * Clearinghouse integration
  * Rejection queue handling
  * Syntax validation
  * Claim correction workflow
  * Submission acknowledgment tracking

##### **Module 12: Claim Status Tracking**
This module monitors payer claim processing status using EDI 276/277 transactions.
* **Features:**
  * Real-time claim tracking
  * Status inquiry automation
  * Aging reports
  * Follow-up alerts
  * Claim history tracking

#### **Category 4: Payment & Revenue Management (7 Modules)**

##### **Module 13: ERA Processing**
This module processes Electronic Remittance Advice (EDI 835) files received from insurance payers.
* **Features:**
  * ERA file processing
  * Payment reconciliation
  * Denial extraction
  * Adjustment processing
  * Auto-posting support

##### **Module 14: Payment Posting**
This module posts insurance and patient payments into the billing system and updates balances.
* **Features:**
  * Insurance payment posting
  * Patient payment entry
  * Payment reconciliation
  * Adjustment posting
  * Balance updates

##### **Module 15: Denial Management**
This module identifies denied claims, categorizes denial reasons, and manages appeals and corrections.
* **Features:**
  * Denial tracking
  * Appeal workflow
  * Denial categorization
  * Root-cause analysis
  * AI denial prediction

##### **Module 16: Secondary Insurance Billing**
This module submits remaining balances to secondary or tertiary insurance payers after primary payer processing.
* **Features:**
  * COB processing
  * Secondary claim generation
  * Balance transfer automation
  * Multi-payer billing
  * Secondary ERA tracking

##### **Module 17: Patient Billing**
This module generates patient statements and collects remaining patient balances after insurance payments.
* **Features:**
  * Statement generation
  * Online payment portal
  * Payment plans
  * SMS/email reminders
  * Multiple payment methods

##### **Module 18: Accounts Receivable (AR) Follow-Up**
This module tracks unpaid balances and manages follow-up activities for overdue accounts.
* **Features:**
  * AR aging reports
  * Collection prioritization
  * Follow-up work queues
  * Bad debt tracking
  * Write-off management

##### **Module 19: Collections / Refund / Write-Off Management**
This module manages overdue collections, patient refunds, credit balances, and financial write-offs.
* **Features:**
  * Collection workflows
  * Refund processing
  * Credit balance management
  * Small balance write-offs
  * Collection agency integration

#### **Category 5: Reporting, Compliance & Governance (2 Modules)**

##### **Module 20: Reporting & Analytics**
This module provides operational dashboards and financial reports for monitoring RCM performance and revenue cycle efficiency.
* **Features:**
  * KPI dashboards
  * Revenue analysis
  * Denial trend reports
  * AR analytics
  * Export functionality

##### **Module 21: Compliance & Audit**
This module maintains HIPAA compliance, audit trails, access logs, and security monitoring across the RCM system.
* **Features:**
  * HIPAA audit logging
  * Access monitoring
  * Security alerts
  * Compliance reporting
  * Activity tracking

#### **Category 6: Administration & Platform Services (11 Modules)**

##### **Module 22: User Login & Authentication**
This module handles secure user access to the system with username/password and optional two-factor authentication.
* **Features:**
  * Username/password login
  * Two-factor authentication
  * Role-based access control
  * Session timeout management
  * Password reset functionality

##### **Module 23: User Management**
This module allows administrators to create user accounts, assign roles, and manage permissions.
* **Features:**
  * User creation
  * Role assignment
  * Permission management
  * User activity tracking
  * Account deactivation

##### **Module 24: Notification System**
This module sends automated alerts and reminders to staff and patients.
* **Features:**
  * SMS notifications
  * Email alerts
  * Appointment reminders
  * Billing reminders
  * Delivery tracking

##### **Module 25: Document Management**
This module securely stores patient documents, insurance cards, and medical records.
* **Features:**
  * Secure document storage
  * OCR scanning
  * Document categorization
  * Search functionality
  * Version control

##### **Module 26: Third-Party Integrations**
This module integrates the RCM platform with external healthcare and payment systems.
* **Features:**
  * Clearinghouse integration
  * Payment gateway integration
  * SMS service integration
  * OCR integration
  * API connectivity

##### **Module 27: Patient Portal**
This module provides patients with online access to billing, appointments, and communication services.
* **Features:**
  * Online bill payment
  * Appointment scheduling
  * Patient messaging
  * Document access
  * Secure login

##### **Module 28: Revenue Cycle Dashboard**
This module displays real-time KPIs and operational revenue cycle metrics.
* **Features:**
  * KPI dashboards
  * AR tracking
  * Denial monitoring
  * Collection tracking
  * Trend visualization

##### **Module 29: Automated Workflows**
This module automates common RCM business processes and task routing.
* **Features:**
  * Workflow automation
  * Task assignment
  * Trigger-based actions
  * Business rule engine
  * Process optimization

##### **Module 30: Data Import/Export**
This module supports bulk data migration and report export operations.
* **Features:**
  * CSV/Excel import
  * Bulk data migration
  * Export scheduling
  * Data validation
  * Format conversion

##### **Module 31: System Configuration**
This module allows administrators to configure workflows, fee schedules, and system settings.
* **Features:**
  * Practice configuration
  * Workflow customization
  * Fee schedule setup
  * Integration settings
  * Business rule configuration

##### **Module 32: Backup & Recovery**
This module protects system data through automated backups and disaster recovery planning.
* **Features:**
  * Automated backups
  * Disaster recovery
  * Point-in-time restoration
  * Backup monitoring
  * Data integrity verification

#### **Category 7: Advanced Enterprise Features (6 Modules)**

##### **Module 33: Contract Management**
This module manages payer contracts, reimbursement schedules, and underpayment detection.
* **Features:**
  * Payer contract storage
  * Reimbursement tracking
  * Fee schedule management
  * Underpayment detection
  * Contract renewal alerts

##### **Module 34: Credentialing Management**
This module tracks provider licenses, certifications, and insurance network enrollments.
* **Features:**
  * Provider credential tracking
  * License expiration alerts
  * Insurance enrollment
  * Document repository
  * Renewal reminders

##### **Module 35: Eligibility Batch Processing**
This module performs automated bulk insurance eligibility verification jobs.
* **Features:**
  * Bulk eligibility verification
  * Scheduled jobs
  * Overnight processing
  * Exception reporting
  * Coverage updates

##### **Module 36: ERA Automation**
This module automates ERA downloading, reconciliation, and payment posting workflows.
* **Features:**
  * Automatic ERA download
  * Auto-posting
  * Reconciliation automation
  * Adjustment automation
  * Denial extraction

##### **Module 37: API Management**
This module manages external APIs, integrations, authentication, and API monitoring.
* **Features:**
  * API gateway management
  * API monitoring
  * Authentication management
  * Usage tracking
  * Secure connectivity

##### **Module 38: Security & Compliance Monitoring**
This module continuously monitors security events, compliance violations, and suspicious activities.
* **Features:**
  * Threat monitoring
  * Security auditing
  * Compliance enforcement
  * Event tracking
  * Risk alerts

---

## 👥 Who Uses This Application?

### 1. **Front Desk Staff**
**What They Do:**
- Register patients
- Verify insurance
- Schedule appointments
- Check-in patients
- Collect payments

**Modules They Use:** 1-5, 23

---

### 2. **Doctors/Providers**
**What They Do:**
- See patients
- Enter clinical notes
- Order tests
- Write prescriptions
- Refer to specialists

**Modules They Use:** 6-9

---

### 3. **Medical Coders**
**What They Do:**
- Review clinical notes
- Assign diagnosis codes (ICD-10)
- Assign procedure codes (CPT)
- Review AI suggestions
- Ensure coding accuracy

**Modules They Use:** 10-11

---

### 4. **Billing Staff**
**What They Do:**
- Create claims
- Submit claims
- Track claim status
- Post payments
- Handle denials

**Modules They Use:** 12-22

---

### 5. **AR Specialists**
**What They Do:**
- Follow up on unpaid claims
- Work denials
- File appeals
- Manage aging accounts
- Patient collections

**Modules They Use:** 18-25

---

### 6. **Practice Manager**
**What They Do:**
- Monitor operations
- Review reports
- Manage staff
- Ensure compliance
- Track revenue

**Modules They Use:** 26-27

---

### 7. **Patients**
**What They Do:**
- Book appointments online
- View bills
- Make payments
- Access medical records
- Communicate with clinic

**Modules They Use:** 28

---

## 🔄 Complete Data Flow

### Where Does Data Come From?

1. **Patient enters clinic** → Front desk enters data
2. **Insurance card** → Scanned by AI (OCR)
3. **Insurance company** → Real-time verification (API)
4. **Doctor** → Clinical notes entered
5. **AI** → Code suggestions generated
6. **Fee schedule** → Charges calculated
7. **Clearinghouse** → Claims transmitted
8. **Insurance** → Payments received
9. **Patient** → Copay/balance paid

### Where Does Data Go?

1. **Database** → All data stored securely
2. **Insurance companies** → Claims sent
3. **Clearinghouse** → Claims routed
4. **Patients** → Statements sent
5. **Reports** → Management dashboards
6. **Audit logs** → Compliance tracking
7. **Backups** → Daily backups to cloud

---

## 🔐 Security & Privacy

### How We Protect Patient Data:

1. **Encryption**
   - All data encrypted at rest
   - All data encrypted in transit
   - 256-bit AES encryption

2. **Access Control**
   - Role-based permissions
   - Each user sees only what they need
   - Audit trail of all access

3. **HIPAA Compliance**
   - All requirements met
   - Regular security audits
   - Staff training
   - Business Associate Agreements

4. **Backups**
   - Daily automated backups
   - 30-day retention
   - Disaster recovery plan

---

## 💡 Key Features That Make Us Different

### 1. **AI-Powered Coding**
- AI reads doctor's notes
- Suggests correct codes
- 85-90% accuracy
- Saves 8 minutes per encounter

### 2. **Real-Time Insurance Verification**
- Instant eligibility check
- No phone calls needed
- 30 seconds vs 15 minutes

### 3. **Automated Claim Scrubbing**
- AI checks claims before submission
- 50+ validation rules
- 95%+ clean claim rate

### 4. **Electronic Payment Posting**
- Auto-post ERA/835 files
- No manual entry
- Instant reconciliation

### 5. **Denial Prevention**
- AI predicts denial risk
- Suggests corrections
- 50% fewer denials

### 6. **Real-Time Dashboards**
- See all metrics live
- Revenue tracking
- Claim status
- AR aging

---

## 📊 Business Impact

### For a Small Clinic (5 Doctors, 100 Patients/Day):

**Before Our Application:**
- Days to Payment: 45 days
- Denial Rate: 18%
- Staff Needed: 8 people
- Revenue Loss: $50K/month
- Manual Errors: High

**After Our Application:**
- Days to Payment: 7 days
- Denial Rate: 4%
- Staff Needed: 5 people
- Revenue Loss: $10K/month
- Manual Errors: Minimal

**Savings:**
- Time: 85% faster
- Staff: 3 fewer people ($180K/year)
- Revenue: $40K/month recovered
- ROI: 400% in first year

---

## 🚀 How to Get Started

### Week 1-2: Setup
- Install application
- Configure settings
- Import existing patients
- Train staff

### Week 3-4: Go Live
- Start with new patients
- Gradually migrate existing
- Monitor closely
- Adjust as needed

### Month 2-3: Optimize
- Review reports
- Fine-tune workflows
- Add advanced features
- Scale up

---

## 📞 Support & Training

### Training Provided:
- 2-hour initial training per role
- Video tutorials
- User manuals
- Live chat support
- Phone support

### Ongoing Support:
- 24/7 technical support
- Regular updates
- New feature training
- Best practice guidance

---

## ✅ Success Metrics

### We Track:
- Days in AR (Target: <30 days)
- Clean Claim Rate (Target: >95%)
- Denial Rate (Target: <5%)
- Collection Rate (Target: >98%)
- Patient Satisfaction (Target: >90%)
- Staff Efficiency (Target: +50%)

---

## 🎯 Summary

This application is a **complete Revenue Cycle Management system** that:

1. **Automates** the entire billing process
2. **Reduces** time from 45 days to 7 days
3. **Increases** clean claim rate to 95%+
4. **Decreases** denials by 50%
5. **Saves** money on staff and lost revenue
6. **Improves** patient and staff satisfaction

**Bottom Line:** Get paid faster, with fewer errors, using less staff.

---

**For More Details:**
- Technical Specifications → See System Requirements documents
- Implementation Plan → See Development Phase Guides
- Module Details → See Module Flow Diagrams
- MVP Plan → See MVP Guide documents
