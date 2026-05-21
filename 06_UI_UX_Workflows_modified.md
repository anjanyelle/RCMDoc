Healthcare RCM Application - UI/UX Workflows & Screen Designs
Version: 1.0

For: Development Team

1. Overview
This document describes the user interface design, navigation structure, and screen-by-screen workflows for the RCM application.

Design Principles:

Simple & Clean: Minimal clutter, focus on task completion
Role-Based: Each user sees only what they need
Fast: <2 second page loads, keyboard shortcuts
Mobile-Responsive: Works on desktop, tablet, phone
Accessible: WCAG 2.1 Level AA compliant
2. Navigation Structure
Main Navigation (Left Sidebar):
┌─────────────────────────────────────────┐
│  [Logo] RCM Application                 │
├─────────────────────────────────────────┤
│  🏠 Dashboard                           │
│  👥 Patients                            │
│  📅 Appointments                        │
│  🏥 Encounters                          │
│  🧾 Orders                              │
│  💰 Charges                             │
│  🏷️ Coding (Medical Coding)            │
│  📋 Claims                              │
│  🧹 Claim Scrubbing                    │
│  ❌ Denials                             │
│  📝 Appeals                             │
│  💳 Payments                            │
│  💸 Adjustments                         │
│  📑 Contracts (Fee Schedule)           │
│  📊 AR / AR Aging                      │
│  📈 Reports                             │
│  🤖 AI Insights                        │
│  🔐 Audit Logs                         │
│  ⚙️ Settings                           │
│  👤 User Menu ▼                        │
│     - Profile                          │
│     - Logout                           │
└─────────────────────────────────────────┘
Navigation varies by role:

•	Front Desk: Dashboard, Patients, Appointments, Payments, Insurance Eligibility
•	Coder: Dashboard, Encounters, Claims (view only), Coding, Denials (view only)
•	Biller: Dashboard, Claims, Payments (view only), Adjustments
•	AR Manager: Dashboard, Claims, Payments, Denials, Reports, Appeals, AR Aging
•	Denial Specialist: Dashboard, Denials, Appeals, Claims (view only), Reports
•	Finance Manager: Dashboard, Reports, Revenue Analytics, AR Summary, Contract Performance

3. Screen Designs by Module
Module 1: Dashboard
Purpose: Role-specific overview of daily operations, patient flow, insurance status, and financial collection.

Front Desk Dashboard:
┌──────────────────────────────────────────────────────────────┐
│  Dashboard - Front Desk                        [Date: Today] │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Today's Appts│  │ Checked In   │  │ Copays       │       │
│  │     45       │  │     32        │  │  $1,240      │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ No Show Rate │  │ Pending Ins  │  │ Collection % │       │
│  │    8%        │  │     12        │  │    92%       │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  Today's Appointments                      [Search Patient]  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Time  │ Patient Name    │ Provider   │ Status  │ Action│  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ 9:00  │ John Doe        │ Dr. Smith  │ Waiting │[Check]│  │
│  │ 9:30  │ Jane Smith      │ Dr. Jones  │ Checked  │       │  │
│  │ 10:00 │ Bob Johnson     │ Dr. Smith  │ Pending  │[Check]│  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Insurance Verification Status                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Verified: 28 │ Pending: 10 │ Failed: 4                │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Alerts / Notifications                                      │
│  • 5 patients missing insurance details                      │
│  • 3 appointments require copay collection                  │
│  • 2 eligibility verification failures                      │
│                                                              │
│  Quick Actions                                               │
│  [+ New Patient]  [+ Schedule Appointment]  [Verify Ins.]   │
│  [Collect Copay]  [Check Eligibility]  [Print Forms]        │
└──────────────────────────────────────────────────────────────┘
Billing Dashboard:
┌──────────────────────────────────────────────────────────────┐
│  Dashboard - Billing                           [Date: Today] │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ Clean Claim │  │ Denial Rate │  │ Submitted   │          │
│  │    96.2%    │  │    4.1%     │  │    142      │          │
│  │  ↑ 2.1%     │  │  ↓ 0.8%     │  │   Today     │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ AR Balance  │  │ Rejections  │  │ Collections │          │
│  │  $245,000   │  │     12      │  │  $18,450    │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                              │
│  Claims Requiring Action                                     │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Claim #   │ Patient      │ Amount  │ Status   │ Action │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ CLM12345  │ John Doe     │ $450    │ Error    │ [Fix]  │  │
│  │ CLM12346  │ Jane Smith   │ $1,200  │ Rejected │[Review]│  │
│  │ CLM12347  │ Bob Johnson  │ $850    │ Ready    │[Submit]│  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Denial Trends                                               │
│  • Coding Errors: 35%                                        │
│  • Eligibility Issues: 28%                                   │
│  • Authorization Missing: 15%                                │
│                                                              │
│  Alerts / Notifications                                      │
│  • 8 claims pending > 5 days                                 │
│  • 3 high-value claims rejected                              │
│  • Batch submission failed for 2 claims                      │
│                                                              │
│  Quick Actions                                               │
│  [Scrub Claims]  [Submit Batch]  [Check Status]              │
│  [Post Payments] [View Denials] [Generate Report]            │
└──────────────────────────────────────────────────────────────┘
AR Manager Dashboard:
┌──────────────────────────────────────────────────────────────┐
│  Dashboard - AR Management                     [Date: Today] │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Total AR │  │ Days in  │  │ AR >90   │  │ Denials  │    │
│  │ $2.4M    │  │ AR: 38   │  │ Days:12% │  │ Pending  │    │
│  │          │  │ ↓ 3 days │  │ ↓ 2%     │  │   47     │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Cash Col │  │ Appeals  │  │ Underpay │  │ Follow-Up│    │
│  │ $185K    │  │ Pending  │  │ Alerts:9 │  │ Tasks:24 │    │
│  │ Today    │  │    16    │  │          │  │          │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                              │
│  AR Aging                                                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ 0-30 days:  $1.2M (50%) ████████████                  │  │
│  │ 31-60 days: $720K (30%) ███████                       │  │
│  │ 61-90 days: $240K (10%) ██                            │  │
│  │ 90+ days:   $240K (10%) ██                            │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  High Priority Denials                                      │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Claim #   │ Patient    │ Amount  │ Reason    │ Action │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ CLM12340  │ John Doe   │ $5,400  │ Auth Mis  │[Appeal]│  │
│  │ CLM12341  │ Jane Smith │ $3,200  │ Coding    │[Review]│  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Payer Performance Alerts                                    │
│  • Aetna claims averaging 45 days reimbursement              │
│  • Medicare denial rate increased by 3%                      │
│  • 9 underpaid claims detected                               │
│                                                              │
│  Quick Actions                                               │
│  [Post Payments] [Work Denials] [Follow Up >60 Days]         │
│  [Review Appeals] [Export AR Report] [Assign Tasks]          │
└──────────────────────────────────────────────────────────────┘
Module 2: Patient Registration
Screen: Patient Search/Create

┌──────────────────────────────────────────────────────────────┐
│  Patients                                  [+ New Patient]  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Search Patient                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ 🔍 Search by Name, MRN, DOB, Phone, Insurance ID...   │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Filters: [Active ▼] [Today’s Patients ▼] [Provider ▼]      │
│                                                              │
│  Search Results                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ MRN      │ Name         │ DOB      │ Insurance │ Act │ │
│  ├────────────────────────────────────────────────────────┤  │
│  │ MRN12345 │ Doe, John A  │01/15/80  │ Verified  │[View│ │
│  │ MRN12346 │ Doe, Jane M  │03/22/85  │ Pending   │[Edit│ │
│  │ MRN12347 │ Doe, Robert J│07/10/75  │ Expired   │[View│ │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Alerts / Notifications                                      │
│  • 2 patients missing insurance details                      │
│  • 1 duplicate patient match detected                        │
│  • 3 insurance verifications pending                         │
│                                                              │
│  Quick Actions                                               │
│  [+ New Patient] [Verify Insurance] [Print Registration]     │
│  [Merge Duplicate] [Schedule Appointment]                    │
│                                                              │
│  [Showing 3 of 3 results]                                    │
└──────────────────────────────────────────────────────────────┘
Screen: New Patient Registration

┌──────────────────────────────────────────────────────────────┐
│  New Patient Registration                    [Save] [Close] │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Demographics                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ First Name*   [__________] MI [_] Last Name* [______] │  │
│  │ DOB* [MM/DD/YYYY]   Gender* [Male ▼] Marital [▼]      │  │
│  │ SSN [___-__-____] (encrypted)                          │  │
│  │ Phone (Mobile)* [(___) ___-____]                       │  │
│  │ Email [___________________________]                    │  │
│  │ Preferred Language [English ▼]                         │  │
│  │ Address* [____________________________________]        │  │
│  │ City* [________] State* [MA ▼] ZIP* [_____]            │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Emergency Contact                                           │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Name* [_________________________]                     │  │
│  │ Relationship* [Spouse ▼]                              │  │
│  │ Phone* [(___) ___-____]                               │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Insurance Information                                       │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Primary Insurance                                     │  │
│  │ Payer* [Blue Cross Blue Shield ▼]                     │  │
│  │ Policy Number* [_____________________]                │  │
│  │ Group Number [_____________________]                  │  │
│  │ Subscriber Name* [___________________]                │  │
│  │ Relationship* [Self ▼]                                │  │
│  │ Effective Date [MM/DD/YYYY]                           │  │
│  │ Copay [$____] Deductible [$______]                    │  │
│  │ Upload Card [Choose File] [Front] [Back]              │  │
│  │                                                        │  │
│  │ [+ Add Secondary Insurance]                            │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Consent & Compliance                                        │
│  ☐ HIPAA Consent Signed                                      │
│  ☐ Financial Responsibility Accepted                         │
│  ☐ Consent to Treat                                          │
│                                                              │
│  Alerts / Validation                                         │
│  • Duplicate patient check enabled                           │
│  • Insurance eligibility pending                             │
│                                                              │
│  Quick Actions                                               │
│  [Verify Insurance Now] [Check Eligibility] [Print Forms]    │
│                                                              │
│                                [Save] [Save & Schedule]      │
└──────────────────────────────────────────────────────────────┘
Duplicate Detection Alert:

┌──────────────────────────────────────────────────────────────┐
│  ⚠️ Possible Duplicate Patient                               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  A similar patient record already exists:                    │
│                                                              │
│  Name: John A Doe                                            │
│  DOB: 01/15/1980                                             │
│  MRN: MRN12345                                               │
│  Phone: (***) ***-1234                                       │
│  Insurance: Blue Cross Blue Shield                           │
│                                                              │
│  Match Confidence: 92%                                       │
│                                                              │
│  Matching Fields:                                            │
│  • First/Last Name                                           │
│  • Date of Birth                                             │
│  • Phone Number                                               │
│                                                              │
│  Recommended Action: Review existing chart before creating   │
│  a new patient record.                                       │
│                                                              │
│  [View Existing Chart]  [Merge Records]                      │
│  [Yes, Use Existing]   [No, Create New]                      │
└──────────────────────────────────────────────────────────────┘
Module 3: Insurance Verification
Screen: Eligibility Check

┌──────────────────────────────────────────────────────────────┐
│  Insurance Verification - John Doe (MRN12345)                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Primary Insurance: Blue Cross Blue Shield                  │
│  Policy Number: POL987654                                   │
│  Service Date: [05/18/2026]        [Verify Eligibility]     │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ✅ Verification Results (05/18/2026 2:30 PM)          │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ Coverage Status:    ✅ ACTIVE                          │  │
│  │ Effective Date:     01/01/2026                         │  │
│  │ Plan Type:          PPO                                │  │
│  │                                                        │  │
│  │ Financial Responsibility:                             │  │
│  │ ├─ Copay:           $30.00                            │  │
│  │ ├─ Deductible:      $1,500 / $500 remaining           │  │
│  │ ├─ Coinsurance:     20% after deductible              │  │
│  │ └─ OOP Max:         $5,000 / $3,200 remaining         │  │
│  │                                                        │  │
│  │ Network Status:     ✅ IN-NETWORK                     │  │
│  │ Prior Auth Req:     ⚠️ YES (>$1,000 services)        │  │
│  │ Referral Req:       ❌ NO                             │  │
│  │                                                        │  │
│  │ Coverage Limitations:                                  │  │
│  │ • Imaging: Requires prior authorization                │  │
│  │ • Specialist visits: Covered                          │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Eligibility Alerts                                          │
│  • Prior authorization required for upcoming procedure       │
│  • Deductible partially met                                 │
│  • Coverage active but high OOP remaining                   │
│                                                              │
│  Verification History                                        │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Date/Time         │ Status  │ Verified By              │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ 05/18/2026 2:30PM │ Active  │ Sarah Johnson            │  │
│  │ 04/15/2026 9:15AM │ Active  │ Sarah Johnson            │  │
│  │ 03/10/2026 1:45PM │ Active  │ Mike Davis               │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Payer Response Details                                      │
│  • Eligibility Source: Availity / Waystar API              │
│  • Response Code: 271 Eligibility Response                  │
│  • Last Sync Status: Success                                │
│                                                              │
│  Quick Actions                                               │
│  [Print Verification] [Email Patient] [Create Authorization] │
│  [Schedule Follow-up] [Update Coverage] [Close]              │
└──────────────────────────────────────────────────────────────┘
Module 4: Appointment Scheduling
Screen: Schedule Appointment

┌──────────────────────────────────────────────────────────────┐
│  Schedule Appointment                            [Save] [X]   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Patient*         [John Doe (MRN12345) ▼]   [+ New Patient]  │
│  Provider*        [Dr. Jane Smith ▼]                        │
│  Location/Dept*   [Outpatient Clinic - Room 2 ▼]           │
│  Appointment Type*[Office Visit - Follow Up ▼]             │
│  Visit Category   [Consultation ▼]                         │
│  Duration         [30 minutes]                             │
│                                                              │
│  Insurance Status   ✅ Verified | ⚠️ Needs Authorization    │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Calendar - May 2026                  [Week] [Month]    │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ Mon 5/18  │ Tue 5/19  │ Wed 5/20  │ Thu 5/21 │ Fri 5/22│ │
│  ├────────────────────────────────────────────────────────┤  │
│  │ 9:00  ✅  │ 9:00  ✅  │ 9:00  ❌  │ 9:00  ✅ │ 9:00  ✅│ │
│  │ 9:30  ✅  │ 9:30  ❌  │ 9:30  ❌  │ 9:30  ✅ │ 9:30  ❌│ │
│  │ 10:00 ❌  │ 10:00 ✅  │ 10:00 ❌  │ 10:00 ❌ │ 10:00 ✅│ │
│  │ 10:30 ✅  │ 10:30 ✅  │ 10:30 ❌  │ 10:30 ✅ │ 10:30 ✅│ │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Selected Slot: Tuesday, May 19, 2026 - 10:00 AM            │
│                                                              │
│  Reason for Visit [Annual checkup                        ]   │
│  Chief Complaint  [____________________________________]    │
│  Notes            [Patient prefers morning appointments]    │
│                                                              │
│  Pre-Visit Checks                                           │
│  ☐ Insurance Verified                                        │
│  ☐ Referral Required                                         │
│  ☐ Prior Authorization Checked                               │
│  ☐ Copay Collected                                           │
│                                                              │
│  Reminders                                                  │
│  ☑ SMS   ☑ Email   ☑ Phone Call                             │
│  Reminder Schedule: [24 hrs before ▼]                       │
│                                                              │
│  Alerts / Conflicts                                         │
│  • Provider has high patient load that day                  │
│  • Slot may exceed recommended wait time                   │
│                                                              │
│  Quick Actions                                             │
│  [Check Eligibility] [Verify Insurance] [Collect Copay]    │
│  [Save Appointment]  [Cancel]                               │
└──────────────────────────────────────────────────────────────┘┘
Module 5: Encounter Management
Screen: Check-In Patient

┌──────────────────────────────────────────────────────────────┐
│  Check-In - John Doe                                 [Save] │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Patient: John Doe (MRN12345)                               │
│  Appointment: 05/18/2026 10:00 AM with Dr. Jane Smith       │
│                                                              │
│  Arrival Status: 🟡 Waiting → Check-In In Progress          │
│                                                              │
│  ✅ Step 1: Verify Demographics                             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Name:    John A Doe                                     │  │
│  │ DOB:     01/15/1980                                     │  │
│  │ Address: 123 Main St, Boston, MA 02101                 │  │
│  │ Phone:   (555) 123-4234                                │  │
│  │                                                          │  │
│  │ ☑ Patient confirms information is correct              │  │
│  │ ☑ ID Proof Verified (Optional)                         │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ✅ Step 2: Verify Insurance                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Primary: Blue Cross Blue Shield (POL987654)            │  │
│  │ Status:  ✅ ACTIVE (Verified today at 9:45 AM)         │  │
│  │ Copay:   $30.00                                         │  │
│  │ Authorization: ⚠️ Required for procedure               │  │
│  │                                                          │  │
│  │ [Re-verify Insurance]                                   │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  💳 Step 3: Collect Copay                                  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Copay Amount: $30.00                                    │  │
│  │ Payment Method: [Credit Card ▼]                         │  │
│  │ Receipt: ☑ Email / ☑ SMS                                │  │
│  │                                                          │  │
│  │ [Process Payment]                                       │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  🏥 Step 4: Create Encounter                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Encounter Type: [Office Visit ▼]                       │  │
│  │ Visit Status: [Checked-In ▼]                           │  │
│  │ Chief Complaint: [Annual checkup                   ]   │  │
│  │ Provider Notes: [______________________________]       │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ⚠️ Alerts / Validation                                     │
│  • Prior authorization required before service              │
│  • Copay collected successfully                             │
│  • Insurance verified within last 24 hours                 │
│                                                              │
│  🔄 Workflow Status                                         │
│  Check-In → Insurance → Payment → Encounter Created         │
│                                                              │
│  Quick Actions                                             │
│  [Print Wristband] [Verify Eligibility] [Send to Provider] │
│  [Complete Check-In]  [Cancel]                             │
└──────────────────────────────────────────────────────────────┘

Module 6: Orders Management
Screen: Create / Manage Orders

┌──────────────────────────────────────────────────────────────┐
│  Orders - Create / Manage                        [Save] [X]  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Patient: John Doe (MRN12345)                              │
│  Encounter: ENC12345 | 05/18/2026 | Dr. Smith              │
│                                                              │
│  Order Type: [Lab ▼] [Imaging ▼] [Medication ▼] [Procedure] │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Order Entry                                            │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ Search Order: [ HbA1c / CBC / X-Ray / MRI        ]     │  │
│  │                                                        │  │
│  │ Selected Orders:                                      │  │
│  │ ☑ HbA1c Test                                          │  │
│  │ ☑ Lipid Panel                                         │  │
│  │                                                        │  │
│  │ Diagnosis Link: [E11.9 ▼] (Type 2 Diabetes)          │  │
│  │ Priority: [Routine ▼] [Urgent ▼]                      │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Clinical Notes                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Reason: Annual diabetes monitoring                      │  │
│  │ Instructions: Fasting required for lipid panel         │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Order Status                                                │
│  • Order Validation: ✅ Passed                             │
│  • Medical Necessity: ⚠ Review Suggested                  │
│  • Billing Eligibility: ⏳ Pending Scrub                  │
│                                                              │
│  Integration Routing                                         │
│  • Sent to Lab System (HL7/FHIR)                           │
│  • Sent to Billing System                                   │
│                                                              │
│  Quick Actions                                              │
│  [Place Order]  [Print Requisition]  [Send to Lab]         │
│  [Hold Order]  [Cancel]                                    │
└──────────────────────────────────────────────────────────────┘

Module 7: Charges
Screen: Charge Entry / Charges Management

┌──────────────────────────────────────────────────────────────┐
│  Charge Capture - Encounter ENC12345            [Save] [X]   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Patient: John Doe (MRN12345)                              │
│  Provider: Dr. Jane Smith                                  │
│  Encounter Date: 05/18/2026                                │
│                                                              │
│  Charge Status: 🟡 In Progress → Not Submitted              │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Add Charges                                            │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ CPT Search: [ office visit / lab / procedure      ]    │  │
│  │                                                        │  │
│  │ Selected Charges:                                     │  │
│  │ Code    Description                Qty   Amount       │  │
│  │ 99214   Office Visit Level 4        1     $150        │  │
│  │ 83036   HbA1c                      1      $45        │  │
│  │                                                        │  │
│  │ Modifier: [None ▼]  POS: [11 - Office ▼]             │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Diagnosis Linkage                                          │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ICD-10 Mapping:                                       │  │
│  │ ☑ E11.9  Type 2 Diabetes                              │  │
│  │ ☑ I10    Hypertension                                 │  │
│  │                                                        │  │
│  │ Dx ↔ CPT Linking: VALIDATED                            │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Charge Summary                                             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Total Charges:        $195                            │  │
│  │ Contract Adjustment:  $35 (estimated)                │  │
│  │ Net Expected:        $160                            │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Validation Checks                                          │
│  • CPT-ICD Link: ✅ Valid                                  │
│  • Missing Modifier: ⚠ None required                      │
│  • Medical Necessity: ⚠ Review suggested                 │
│  • Scrubbing Status: ⏳ Pending                            │
│                                                              │
│  Integration Status                                         │
│  • Sent to Claim Engine                                    │
│  • Ready for Scrubbing                                     │
│                                                              │
│  Quick Actions                                              │
│  [Validate Charges]  [Hold]  [Send to Claims]              │
│  [Save Draft]  [Cancel]                                    │
└──────────────────────────────────────────────────────────────┘
Module 8: Medical Coding
Screen: Coding Worklist

┌──────────────────────────────────────────────────────────────┐
│  Coding Worklist                                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Filter: [All Providers ▼] [Last 7 Days ▼] [Not Coded ▼]    │
│  Priority: [All ▼] [High Value ▼] [Denial Risk ▼]           │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Enc ID   │ Date   │ Patient     │ Provider │ Type │ Act │ │
│  ├────────────────────────────────────────────────────────┤  │
│  │ ENC12345 │ 5/18   │ Doe, John   │ Dr. Smith│ Off  │[Code│ │
│  │ ENC12346 │ 5/18   │ Smith, Jane │ Dr. Jones│ Off  │[Code│ │
│  │ ENC12347 │ 5/17   │ Johnson, B  │ Dr. Smith│ Proc │[Code│ │
│  │ ENC12348 │ 5/17   │ Davis, Mary  │ Dr. Brown│ Off  │[Code│ │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Coding Alerts                                              │
│  • 3 encounters missing documentation                        │
│  • 2 high-value claims pending coding                       │
│  • 1 encounter flagged for possible upcoding risk          │
│                                                              │
│  AI Coding Assistance                                       │
│  • Suggested codes available for 5 encounters              │
│  • Documentation completeness: 82%                        │
│                                                              │
│  Work Queue Summary                                         │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Not Started: 25   │ In Progress: 12  │ Completed: 10   │ │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Quick Actions                                              │
│  [Batch Code] [Run AI Suggestion] [Validate Codes]          │
│  [Send to Billing] [Flag for Review]                        │
│                                                              │
│  [Showing 4 of 47 encounters]            [Next Page →]      │
└──────────────────────────────────────────────────────────────┘
Screen: Code Encounter

┌──────────────────────────────────────────────────────────────┐
│  Code Encounter - ENC12345                     [Save] [X]    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Patient: John Doe (MRN12345) │ Provider: Dr. Jane Smith    │
│  Date: 05/18/2026            │ Type: Office Visit           │
│                                                              │
│  Encounter Status: 🟡 Pending Coding → In Review            │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Clinical Documentation                                 │ │
│  ├─────────────────────────────────────────────────────────┤ │
│  │ Chief Complaint: Annual checkup                        │ │
│  │                                                         │ │
│  │ HPI: 46-year-old male presents for annual physical.    │ │
│  │ No acute complaints. Reports feeling well overall.     │ │
│  │                                                         │ │
│  │ PMH: Type 2 Diabetes (controlled), Hypertension        │ │
│  │                                                         │ │
│  │ Exam: BP 128/82, HR 72, Wt 185 lbs                     │ │
│  │ General: Well-appearing                                │ │
│  │ CV: Normal                                             │ │
│  │ Lungs: Clear                                           │ │
│  │                                                         │ │
│  │ Orders: HbA1c, Lipid Panel                             │ │
│  │                                                         │ │
│  │ Assessment:                                             │ │
│  │ 1. Type 2 Diabetes, controlled                         │ │
│  │ 2. Hypertension, controlled                            │ │
│  │                                                         │ │
│  │ Plan:                                                   │ │
│  │ - Continue meds                                        │ │
│  │ - Follow up 3 months                                   │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Diagnosis Codes (ICD-10)                               │ │
│  ├─────────────────────────────────────────────────────────┤ │
│  │ [Search ICD-10: diabetes type 2         ] [Search]      │ │
│  │                                                         │ │
│  │ ☑ E11.9  Type 2 diabetes (Primary)                     │ │
│  │ ☑ I10    Essential hypertension                        │ │
│  │                                                         │ │
│  │ Risk Adjustment: HCC Score Calculated                 │ │
│  │ HCC Flags: Diabetes, Hypertension                      │ │
│  │                                                         │ │
│  │ [+ Add Diagnosis]                                      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Procedure Codes (CPT)                                  │ │
│  ├─────────────────────────────────────────────────────────┤ │
│  │ [Search CPT: office visit            ] [Search]        │ │
│  │                                                         │ │
│  │ Code    Description              Modifier  Dx Link  Amt │ │
│  │ 99214   Office visit level 4      -       [1,2]   $150 │ │
│  │                                                         │ │
│  │ [+ Add Procedure]                                      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  Coding Intelligence                                         │
│  • Suggested E&M Level: 99214 (Supported)                   │
│  • Alternative Suggestion: 99215 (High complexity flag)     │
│  • Documentation Completeness: 94%                          │
│  • Missing: Social history detail (optional)                │
│                                                              │
│  Compliance Checks                                           │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ ✅ Medical necessity supported                          │ │
│  │ ✅ NCCI edits passed                                   │ │
│  │ ⚠️ Modifier review recommended                         │ │
│  │ ⚠️ Risk adjustment coding opportunity                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Audit Trail                                                │
│  • Created by: Dr. Jane Smith                               │
│  • Last edited: 05/18/2026 2:10 PM                          │
│                                                              │
│  Quick Actions                                              │
│  [Validate Codes] [Run AI Suggestion] [Check HCC Risk]      │
│  [Mark as Coded - Ready to Bill] [Save Draft] [Cancel]      │
└──────────────────────────────────────────────────────────────┘
Module 9: Claim Management
Screen: Claim Scrubbing

┌──────────────────────────────────────────────────────────────┐
│  Claim Scrubbing                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Payer: [All Payers ▼]   Batch: [Today’s Claims ▼]          │
│  Scrubbing Rule Set: [Standard Rules ▼]                     │
│                                                              │
│  [Select Claims to Scrub]                                   │
│  ☑ All Ready Claims (47)   ☐ Selected Claims               │
│                                                              │
│  [Start Scrubbing]                                          │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ⏳ Scrubbing in progress... 35 of 47 complete (74%)     │  │
│  │ ████████████████████░░░░░░░                             │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Results Summary                                             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ✅ Clean Claims:    42 (89%)                            │  │
│  │ ⚠️ Warnings:         3 (6%)                             │  │
│  │ ❌ Errors:           2 (5%)                             │  │
│  │ 🔁 Rejected by Payer Rules: 1                           │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Top Scrubbing Rules Triggered                               │
│  • Missing prior authorization (2 claims)                   │
│  • Invalid ICD-10 to CPT linkage (2 claims)                 │
│  • Demographic mismatch (1 claim)                           │
│                                                              │
│  Claims with Errors                                          │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Claim #   │ Patient    │ Error                  │ Act   │ │
│  ├────────────────────────────────────────────────────────┤  │
│  │ CLM12345  │ Doe, John  │ Missing authorization  │[Fix] │ │
│  │ CLM12346  │ Smith, Jane│ Invalid diagnosis code │[Fix] │ │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  AI Scrubbing Suggestions                                   │
│  • 2 claims can be auto-corrected                          │
│  • 1 claim needs coder review                               │
│  • 1 claim requires eligibility re-check                   │
│                                                              │
│  Risk Indicators                                            │
│  • High denial probability claims: 3                        │
│  • High-value at risk: $8,450                               │
│                                                              │
│  Quick Actions                                              │
│  [Auto-Fix Warnings] [Send to Coding] [Hold Claims]        │
│  [Submit Clean Claims (42)] [Export Report] [Close]         │
└──────────────────────────────────────────────────────────────┘
Screen: Claim Detail with Errors

┌──────────────────────────────────────────────────────────────┐
│  Claim CLM12345 - John Doe                        [Save] [X] │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Claim Status: ❌ Failed Scrubbing → Requires Action        │
│  Priority: 🔴 High Risk (High Denial Probability)           │
│                                                              │
│  ❌ Scrubbing Errors (1 Fatal, 0 Warnings)                  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ❌ FATAL: Prior authorization required but missing      │  │
│  │    CPT code 99214 requires authorization               │  │
│  │    Payer Rule: Blue Cross Blue Shield policy #BC-44    │  │
│  │    Action: Obtain authorization or modify CPT code     │  │
│  │    Impact: Claim will be denied if submitted           │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Claim Information                                           │
│  Patient:     John Doe (MRN12345)                           │
│  Payer:       Blue Cross Blue Shield                        │
│  Service Date: 05/18/2026                                   │
│  Provider:     Dr. Jane Smith                               │
│  Total Charge: $150.00                                      │
│  Claim Type:   Professional Claim (CMS-1500)                │
│                                                              │
│  Authorization Section                                       │
│  Authorization Number: [____________]                       │
│  Status: ❌ Not Found                                       │
│  [Search Authorizations] [Request New Auth]                 │
│                                                              │
│  Suggested Fixes (AI Assistance)                            │
│  • Option 1: Request prior authorization (recommended)      │
│  • Option 2: Change CPT to 99213 (lower complexity)         │
│  • Option 3: Add medical necessity justification            │
│                                                              │
│  Risk Impact Analysis                                        │
│  • Denial Probability: 92%                                  │
│  • Revenue at Risk: $150                                    │
│  • Payer Turnaround Delay: 14–21 days                       │
│                                                              │
│  Audit Trail                                                │
│  • Scrubbed by: System Rule Engine                          │
│  • Timestamp: 05/18/2026 02:45 PM                           │
│                                                              │
│  Quick Actions                                              │
│  [Request Authorization] [Edit Claim] [Re-Scrub]            │
│  [Hold Claim] [Send to Coding] [Cancel Claim]               │
│                                                              │
│  [Re-Scrub]  [Save]  [Cancel]                               │
└──────────────────────────────────────────────────────────────┘

Module 10: Denial Management
Screen: Denial Worklist

┌──────────────────────────────────────────────────────────────┐
│  Denial Management                                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Filter: [All Payers ▼] [Last 30 Days ▼] [Not Worked ▼]     │
│  Severity: [All ▼] [High Risk ▼] [High Value ▼]             │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Total    │  │ High $   │  │ Appeal   │  │ Overturn │    │
│  │ Denials  │  │ (>$1K)   │  │ Deadline │  │ Rate     │    │
│  │   47     │  │   12     │  │ <7 Days  │  │   62%    │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Appeal   │  │ Write-Off│  │ Recover  │  │ Aging    │    │
│  │ Success  │  │ Risk     │  │ Potential│  │ >60 Days │    │
│  │ 58%      │  │ $18K     │  │ $42K     │  │ 22%      │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                              │
│  Denial Worklist                                             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Claim#│Patient│Amount│Reason│Deadline│Assigned│Action │ │
│  ├────────────────────────────────────────────────────────┤  │
│  │CLM1234│Doe, J │$5,400│Auth  │5/25/26 │Sarah J │[Appeal│ │
│  │CLM1235│Smith,J│$3,200│Coding│5/27/26 │Mike D  │[Review│ │
│  │CLM1236│Johns,B│$2,100│Elig  │5/30/26 │Sarah J │[Appeal│ │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Denial Intelligence                                         │
│  • Repeat Denials (same reason): 8 claims                   │
│  • Auto-appeal eligible: 5 claims                           │
│  • High probability reversal: 3 claims                     │
│                                                              │
│  Top Denial Reasons (Last 30 Days)                          │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Missing Authorization:      15 (32%) ████████          │  │
│  │ Incorrect Coding:           12 (26%) ██████            │  │
│  │ Eligibility Issues:         10 (21%) █████             │  │
│  │ Timely Filing:               6 (13%) ███               │  │
│  │ Other:                       4 (8%)  ██                │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Payer Performance Insights                                  │
│  • BCBS denial rate increased by 4%                         │
│  • Medicare overturn rate highest in appeals                │
│  • UHC slowest response time (18 days avg)                 │
│                                                              │
│  Alerts / Risks                                             │
│  • 3 appeals nearing deadline (<48 hours)                  │
│  • $18K at risk due to unworked denials                   │
│                                                              │
│  Quick Actions                                              │
│  [Work Next Denial] [Auto-Generate Appeal] [Batch Review]  │
│  [Assign Queue] [Export Report] [Close Aging Denials]      │
└──────────────────────────────────────────────────────────────┘

Module 11: Appeals
Screen: Appeal Workbench

┌──────────────────────────────────────────────────────────────┐
│  Appeals Management                              [Submit] [X]│
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Filter: [All Denials ▼] [High Value ▼] [Pending ▼]         │
│                                                              │
│  Appeal Summary                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Total    │  │ Submitted │  │ Approved │  │ Pending  │    │
│  │ Appeals  │  │ This Month │  │ Rate     │  │ Review   │    │
│  │   18     │  │    6       │  │ 58%      │  │   9      │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                              │
│  Appeal Worklist                                            │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Claim#│Patient│Amount│Denial Reason│Deadline│Action   │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │CLM1234│Doe, J │$5,400│Auth Missing │5/25/26 │[Appeal] │  │
│  │CLM1235│Smith,J│$3,200│Coding Error │5/27/26 │[Appeal] │  │
│  │CLM1236│Johns,B│$2,100│Elig Issue   │5/30/26 │[Appeal] │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Selected Appeal Details                                     │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Claim #: CLM1234                                       │  │
│  │ Payer: Blue Cross Blue Shield                          │  │
│  │ Original Amount: $5,400                                 │  │
│  │ Denial Code: AUTH-01                                   │  │
│  │                                                        │  │
│  │ Appeal Type: [First Level ▼]                          │  │
│  │ Reason for Appeal:                                    │  │
│  │ [Medical necessity clearly documented            ]     │  │
│  │                                                        │  │
│  │ Attachments:                                          │  │
│  │ [Upload Medical Records] [Upload Notes]              │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Appeal Letter Preview                                      │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Auto-generated appeal letter based on denial reason   │  │
│  │ Includes: clinical notes, diagnosis, CPT justification│  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  AI Recommendation                                          │
│  • Appeal Success Probability: 72%                         │
│  • Suggested Attachments: Clinical Notes, Lab Results     │
│  • Best Argument Type: Medical Necessity                   │
│                                                              │
│  Quick Actions                                              │
│  [Generate Appeal Letter] [Submit to Payer]                │
│  [Save Draft] [Escalate] [Cancel Appeal]                   │
└──────────────────────────────────────────────────────────────┘
Module 12: Payment Posting
Screen: ERA Import

┌──────────────────────────────────────────────────────────────┐
│  Payment Posting - ERA Import                                 │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Upload ERA File (EDI 835)                                  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Payer: [Blue Cross Blue Shield ▼]                     │  │
│  │ Check/EFT #: [______________]                          │  │
│  │ Deposit Date: [05/20/2026]                             │  │
│  │                                                          │  │
│  │ [Choose File] 835_BCBS_05202026.txt                   │  │
│  │                                                          │  │
│  │ [Validate ERA]  [Upload and Process]                  │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ERA Processing Status                                      │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ⏳ Parsing EDI 835 file...                              │  │
│  │ ████████████████░░░░░░░                                │  │
│  │ Claims Matched: 15 / 15                                │  │
│  │ Unmatched Claims: 1                                    │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Payment Summary                                            │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Total Paid:      $12,450                               │  │
│  │ Contractual Adj:  $2,100                                │  │
│  │ Patient Resp:    $850                                   │  │
│  │ Denied Amount:   $300                                   │  │
│  │ Net Posting:     $12,450                                │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Recent ERA Files                                           │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Date     │ Payer │ Check#  │ Amount   │ Claims │ Status│ │
│  ├────────────────────────────────────────────────────────┤  │
│  │ 5/20/26  │ BCBS  │ CHK1234 │ $12,450  │ 15     │ Posted│ │
│  │ 5/19/26  │ UHC   │ CHK1235 │ $8,200   │ 12     │ Posted│ │
│  │ 5/18/26  │ Aetna │ CHK1236 │ $5,600   │ 8      │ Posted│ │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Alerts / Exceptions                                         │
│  • 1 claim not matched to system                             │
│  • 2 underpayment differences detected                       │
│  • 1 patient responsibility mismatch                        │
│                                                              │
│  Quick Actions                                              │
│  [View Unmatched Claims] [Post Payments] [Create Adjustments]│
│  [Download ERA Report] [Reprocess File]                     │
└──────────────────────────────────────────────────────────────┘
Screen: ERA Auto-Posting Results

┌──────────────────────────────────────────────────────────────┐
│  ERA Processing Results - CHK1234                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Payer: Blue Cross Blue Shield                              │
│  Check Number: CHK1234                                      │
│  Check Date: 05/20/2026                                     │
│  Deposit Type: EFT / ERA (EDI 835)                          │
│  Total Amount: $12,450.00                                   │
│                                                              │
│  Matching Confidence: 96%                                   │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ✅ Auto-Posted:     12 claims ($10,200)               │  │
│  │ ⚠️ Manual Review:    3 claims ($2,250)                │  │
│  │ ❌ Denials:          2 claims ($1,500)                │  │
│  │ 💰 Underpayments:    1 claim ($300)                   │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Financial Summary                                           │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Total Billed:        $14,800                            │  │
│  │ Allowed Amount:      $12,750                            │  │
│  │ Paid Amount:         $12,450                            │  │
│  │ Contractual Adj:     $2,350                             │  │
│  │ Patient Responsibility: $850                            │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Claims Requiring Manual Review                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Claim #   │ Patient    │ Billed │ Paid  │ Reason  │ Act │ │
│  ├────────────────────────────────────────────────────────┤  │
│  │ CLM12340  │ Doe, John  │ $450   │ $0    │ No Match│[Post│ │
│  │ CLM12341  │ Smith, Jane│ $800   │ $750  │ Variance│[Post│ │
│  │ CLM12342  │ Johnson, B │ $1,000 │ $1,000│ Dup Claim[Post│ │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Denial Summary                                             │
│  • Timely Filing Exceeded                                   │
│  • Eligibility Not Active                                   │
│                                                              │
│  Root Cause Analysis                                        │
│  • 60% Variance: Contractual adjustments                    │
│  • 25% Variance: Coding differences                         │
│  • 15% Variance: Missing authorizations                    │
│                                                              │
│  Alerts / Insights                                          │
│  • 1 recurring underpayment pattern detected               │
│  • 2 claims eligible for appeal                             │
│                                                              │
│  Quick Actions                                              │
│  [Review Manual Items] [Post Adjustments] [Create Appeals]  │
│  [View Denials] [Export ERA Report] [Close]                │
└──────────────────────────────────────────────────────────────┘

Module 13: Adjustments
Screen: Adjustment Entry & Review

┌──────────────────────────────────────────────────────────────┐
│  Adjustments Management                          [Post] [X]  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Filter: [All Claims ▼] [Unposted ▼] [Contractual ▼]        │
│                                                              │
│  Adjustment Summary                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Total    │  │ Contract │  │ Write-off│  │ Patient  │    │
│  │ Adj.     │  │ Adj.     │  │ Amount   │  │ Resp.    │    │
│  │ $18,450  │  │ $12,300  │  │ $4,200   │  │ $1,950   │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                              │
│  Adjustment Worklist                                         │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Claim#│Patient│Charge│Paid │Adj Type│Reason    │Action ││
│  ├────────────────────────────────────────────────────────┤  │
│  │CLM1234│Doe, J │$450  │$300 │Contract│Payer Rate│[Post] ││
│  │CLM1235│Smith,J│$800  │$500 │WriteOff│Denial    │[Post] ││
│  │CLM1236│Johns,B│$1,200│$1,200│PatResp│Copay Due │[Post] ││
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Selected Adjustment Details                                 │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Claim #: CLM1234                                      │  │
│  │ Payer: Blue Cross Blue Shield                         │  │
│  │ Charge Amount: $450                                    │  │
│  │ Paid Amount: $300                                      │  │
│  │ Adjustment Type: [Contractual ▼]                      │  │
│  │ Adjustment Code: [CO-45 ▼]                            │  │
│  │ Adjustment Amount: $150                                │  │
│  │ Reason: Contractual rate difference                    │  │
│  │                                                        │  │
│  │ Notes: [Auto-calculated from contract rules      ]     │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Adjustment Intelligence                                     │
│  • Auto-calculated from contract rates                     │
│  • 3 claims eligible for auto-posting                      │
│  • 1 adjustment requires manual review                     │
│                                                              │
│  Compliance Checks                                           │
│  • Adjustment code valid: ✅                               │
│  • Contract rule applied: ✅                               │
│  • Write-off threshold check: ⚠ Review > $500            │
│                                                              │
│  Quick Actions                                              │
│  [Auto-Post Adjustments] [Recalculate]                     │
│  [Send to Accounting] [Export Report] [Hold Adjustments]   │
└──────────────────────────────────────────────────────────────┘

Module 14: Contract & Fee Schedule Management
Screen: Contract / Fee Schedule Setup

┌──────────────────────────────────────────────────────────────┐
│  Contract & Fee Schedule Management            [Save] [X]    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Payer: [Blue Cross Blue Shield ▼]                         │
│  Contract Type: [Professional ▼] [Facility ▼]              │
│  Effective Date: [01/01/2026]   End Date: [12/31/2026]     │
│                                                              │
│  Contract Summary                                           │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Total CPT Codes:      1,250                             │  │
│  │ Loaded Rates:         1,180                             │  │
│  │ Missing Rates:        70                                │  │
│  │ Contract Status:      🟡 Incomplete                     │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Fee Schedule (CPT Rates)                                   │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ CPT Code │ Description                  │ Allowed Rate │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ 99213    │ Office Visit (Est. Patient) │ $90.00       │  │
│  │ 99214    │ Office Visit (Moderate)     │ $120.00      │  │
│  │ 85025    │ CBC Automated               │ $25.00       │  │
│  │ 80053    │ Comprehensive Metabolic     │ $35.00       │  │
│  │ 71020    │ Chest X-Ray                 │ $75.00       │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Rate Management                                             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Search CPT: [ 99213 / 85025 / 80053              ]     │  │
│  │                                                        │  │
│  │ Selected Code: 99213                                  │  │
│  │ Allowed Rate: [$90.00]                                │  │
│  │ Effective From: [01/01/2026]                          │  │
│  │ Notes: [Annual contract rate update]                 │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Contract Rules                                              │
│  • Annual escalation: 3%                                    │
│  • Bundling rules applied                                  │
│  • Prior authorization required for selected codes         │
│                                                              │
│  Integration Routing                                         │
│  • Sent to Claims Pricing Engine                            │
│  • Synced with Billing System                               │
│                                                              │
│  Quick Actions                                               │
│  [Load Contract]  [Validate Rates]  [Export Fee Schedule]   │
│  [Publish Contract]  [Cancel]                               │
└──────────────────────────────────────────────────────────────┘

Module 15: AR Management
Screen: AR Aging Dashboard

┌──────────────────────────────────────────────────────────────┐
│  Accounts Receivable (AR) Aging Dashboard     [Run Report]  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Filters: [Payer ▼] [Provider ▼] [Facility ▼] [Date ▼]     │
│                                                              │
│  AR Summary                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Total AR │  │ Days in  │  │ >90 Days │  │ Denials  │    │
│  │ $2.4M    │  │ 38 Days  │  │ $240K    │  │ $180K    │    │
│  │ ↓ 4%     │  │ ↓ 3 days │  │ 10%      │  │ Pending  │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                              │
│  AR Aging Breakdown                                          │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ 0–30 Days   │ $1.2M (50%) █████████████              │  │
│  │ 31–60 Days  │ $720K (30%) ███████                   │  │
│  │ 61–90 Days  │ $240K (10%) ███                      │  │
│  │ 90+ Days    │ $240K (10%) ███                      │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Top Outstanding Accounts                                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Claim#│Patient│Payer│Amount│Age│Status│Action        │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │CLM1001│Doe,J  │BCBS │$5,400│45 │Open  │[Follow Up]   │  │
│  │CLM1002│Smith,J│UHC  │$3,200│62 │Denied│[Appeal]      │  │
│  │CLM1003│Johns,B│Aetna│$2,100│95 │Open  │[Escalate]    │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  AR Intelligence                                             │
│  • High Risk AR (>90 days): $240K                         │
│  • Potential Write-offs: $85K                              │
│  • Recoverable AR: $1.8M                                   │
│                                                              │
│  Payer Performance                                           │
│  • BCBS: Slow payment trend ↑                              │
│  • UHC: High denial conversion rate                        │
│  • Medicare: Stable                                        │
│                                                              │
│  Work Queue                                                 │
│  [Work Oldest First] [Follow Up Calls] [Send Statements]   │
│  [Create Appeals] [Export AR Report]                        │
└──────────────────────────────────────────────────────────────┘

Module 16: Reports
Screen: Reports Dashboard

┌──────────────────────────────────────────────────────────────┐
│  Reports & Analytics                                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Report Filters                                              │
│  Date Range: [Last 30 Days ▼]  Facility: [All ▼]            │
│  Payer: [All ▼]  Provider: [All ▼]                          │
│                                                              │
│  KPI Snapshot                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Revenue  │  │ Denial   │  │ Clean    │  │ AR Days  │    │
│  │ $1.2M    │  │ Rate 4%  │  │ Claims   │  │ 38 Days  │    │
│  │ ↑ 8%     │  │ ↓ 1.2%   │  │ 96.2%    │  │ ↓ 3 days │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                              │
│  Standard Reports                                            │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Financial Reports                                     │  │
│  │ ├─ Daily Revenue Report                        [Run]  │  │
│  │ ├─ Monthly Revenue by Department               [Run]  │  │
│  │ ├─ Monthly Revenue by Provider                 [Run]  │  │
│  │ ├─ Monthly Revenue by Payer                    [Run]  │  │
│  │ └─ AR Aging Report                             [Run]  │  │
│  │                                                      │  │
│  │ Operational Reports                                 │  │
│  │ ├─ Clean Claim Rate                            [Run]  │  │
│  │ ├─ Denial Rate Analysis                        [Run]  │  │
│  │ ├─ Coding Productivity                         [Run]  │  │
│  │ ├─ Billing Productivity                        [Run]  │  │
│  │ └─ Charge Capture Report                       [Run]  │  │
│  │                                                      │  │
│  │ Compliance Reports                                  │  │
│  │ ├─ Coding Accuracy Audit                       [Run]  │  │
│  │ ├─ HIPAA Access Audit                          [Run]  │  │
│  │ ├─ Overpayment Report                          [Run]  │  │
│  │ └─ Audit Trail Report                          [Run]  │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Advanced Analytics                                         │
│  • Revenue Leakage Detection                                │
│  • Underpayment Analysis                                    │
│  • Payer Performance Scorecard                              │
│  • Denial Root Cause Dashboard                              │
│                                                              │
│  Custom Reports                                              │
│  [+ Create Custom Report]                                   │
│  [AI Generate Report from Query]                            │
│                                                              │
│  Scheduled Reports                                           │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Report Name     │ Schedule │ Recipients │ Action      │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ Daily Revenue   │ Daily    │ CFO        │ [Edit]      │  │
│  │ AR Aging        │ Weekly   │ AR Team    │ [Edit]      │  │
│  │ Denial Analysis  │ Monthly  │ Mgmt       │ [Edit]      │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Export Options                                              │
│  [PDF] [Excel] [CSV] [Email]                                │
└──────────────────────────────────────────────────────────────┘

Module 17: AI Insights
Screen: RCM Intelligence Dashboard

┌──────────────────────────────────────────────────────────────┐
│  AI Insights & Revenue Intelligence                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Date Range: [Last 30 Days ▼]   Confidence: High           │
│                                                              │
│  AI Summary KPIs                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Revenue  │  │ Denial   │  │ Leakage  │  │ Recovery │    │
│  │ +8.2%    │  │ -1.5%    │  │ $42K     │  │ $28K     │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                              │
│  🔥 AI Alerts (High Priority)                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ⚠ High denial spike detected for BCBS (Coding issue)  │  │
│  │ ⚠ $18K underpayments found in last 7 days              │  │
│  │ ⚠ 12 claims missing authorization risk                │  │
│  │ ⚠ AR >90 days increasing trend detected               │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Revenue Leakage Analysis                                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Category                 │ Amount │ Impact            │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ Missing Charges         │ $12K   │ High             │  │
│  │ Underpayments           │ $18K   │ High             │  │
│  │ Coding Underbilling     │ $7K    │ Medium           │  │
│  │ Timely Filing Loss      │ $5K    │ High             │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  AI Predictions                                              │
│  • Next 7 days revenue forecast: $320K                     │
│  • Expected denial rate: 4.8%                               │
│  • AR >90 days may increase by 6%                           │
│                                                              │
│  Smart Recommendations                                       │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ • Fix coding patterns for Dr. Smith (↓ denials 22%)    │  │
│  │ • Re-scrub 14 pending claims (high failure risk)       │  │
│  │ • Prioritize BCBS appeals ($15K recovery)              │  │
│  │ • Re-check eligibility before claim submission         │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Automation Actions                                          │
│  [Auto-Fix Claims] [Generate Appeals] [Re-Scrub Batch]      │
│  [Optimize Coding Rules] [Run Forecast Model]               │
│                                                              │
│  Model Performance                                           │
│  Accuracy: 93%   |   Training Data: 2M claims              │
│  Last Updated: 05/18/2026                                   │
└──────────────────────────────────────────────────────────────┘

Module 18: Audit & Compliance
Screen: System Audit Logs

┌──────────────────────────────────────────────────────────────┐
│  Audit Logs & System Activity                                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Filters: [User ▼] [Module ▼] [Action ▼] [Date Range ▼]     │
│                                                              │
│  Quick Summary                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Total    │  │ Login    │  │ Data     │  │ Security │    │
│  │ Events   │  │ Events   │  │ Changes  │  │ Alerts   │    │
│  │ 12,450   │  │ 3,210    │  │ 7,980    │  │ 45       │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                              │
│  Audit Trail                                                 │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Time       │ User        │ Module   │ Action  │ Result │ │
│  ├────────────────────────────────────────────────────────┤  │
│  │ 10:12 AM   │ Sarah J     │ Claims   │ Edit    │ Success│ │
│  │ 10:10 AM   │ Mike D      │ Coding   │ Add CPT │ Success│ │
│  │ 10:05 AM   │ Admin       │ Patients │ Update  │ Success│ │
│  │ 09:58 AM   │ System      │ Claims   │ Scrub   │ Success│ │
│  │ 09:45 AM   │ John User   │ Login    │ Access  │ Success│ │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Security Alerts                                             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ⚠ Multiple failed login attempts (User: billing01)    │  │
│  │ ⚠ Access to restricted claim data                      │  │
│  │ ⚠ Bulk export of patient records                       │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Data Change Tracking                                        │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Record Type │ Field Changed │ Old Value │ New Value    │ │
│  ├────────────────────────────────────────────────────────┤  │
│  │ Claim       │ Amount        │ $120      │ $150         │ │
│  │ Patient     │ Address       │ Old Addr  │ New Addr     │ │
│  │ Coding      │ CPT Code      │ 99213     │ 99214        │ │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Compliance Actions                                          │
│  [Export Logs] [Download Report] [Investigate User]         │
│  [Lock Account] [Generate HIPAA Report]                     │
│                                                              │
│  Retention Policy                                            │
│  Logs Retained: 7 Years (HIPAA Compliant)                  │
│  Encryption: AES-256 Enabled                               │
└──────────────────────────────────────────────────────────────┘
4. Mobile Responsive Design
Mobile View: Dashboard (Front Desk)

┌─────────────────────┐
│ ☰  RCM App   [🔔]   │
├─────────────────────┤
│                     │
│ Today’s Overview    │
│                     │
│ Appts:     45       │
│ Checked In: 32      │
│ Copays:   $1,240    │
│ No Shows:   3       │
│                     │
│ ┌─────────────────┐ │
│ │ Next Appointment│ │
│ │ 10:00 AM        │ │
│ │ John Doe        │ │
│ │ Dr. Smith       │ │
│ │ Status: Waiting │ │
│ │ [Check In]      │ │
│ └─────────────────┘ │
│                     │
│ Alerts              │
│ ⚠ 2 Insurance Pending│
│ ❌ 1 Payment Failed │
│ 🔔 3 Reminders Sent │
│                     │
│ Quick Actions       │
│ [New Patient]       │
│ [Schedule Appt]     │
│ [Verify Insurance]  │
│ [Collect Copay]     │
│                     │
│ Recent Activity     │
│ • John Doe checked in│
│ • Jane Smith paid    │
│ • Claim submitted    │
│                     │
└─────────────────────┘
5. UI Component Library
Buttons:
Primary: Blue background, white text (Save, Submit, Create)
Secondary: White background, blue border (Cancel, Back)
Danger: Red background, white text (Delete, Reject)
Success: Green background, white text (Approve, Complete)
Colors:
Primary Blue: #0066CC
Success Green: #28A745
Warning Yellow: #FFC107
Danger Red: #DC3545
Gray: #6C757D
Icons:
Use Lucide Icons or Font Awesome
Consistent icon usage across app
Forms:
Clear labels above fields
Required fields marked with *
Inline validation with error messages
Placeholder text for guidance
6. Accessibility Features
Keyboard Navigation: Tab through all interactive elements
Screen Reader Support: ARIA labels on all inputs
Color Contrast: WCAG AA compliant (4.5:1 ratio)
Focus Indicators: Clear blue outline on focused elements
Error Announcements: Screen reader announces validation errors
7. Performance Optimization
Lazy Loading: Load data as user scrolls
Pagination: Max 50 records per page
Caching: Cache frequently accessed data (payers, providers, codes)
Debouncing: Search inputs debounced by 300ms
Summary:

This document provides the complete UI/UX blueprint for your RCM application. Each screen is designed for:

Efficiency: Minimal clicks to complete tasks
Clarity: Clear visual hierarchy and status indicators
Error Prevention: Validation and alerts before submission
Role Optimization: Each user sees only what they need
Your development team can now build the frontend using these wireframes as a guide.

All 5 Pre-Development Documents Complete! ✅

✅ System Requirements Summary
✅ Database Design
✅ User Roles & Permissions
✅ API Integration Requirements
✅ UI/UX Workflows
Ready to start development!