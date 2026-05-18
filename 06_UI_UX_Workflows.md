# Healthcare RCM Application - UI/UX Workflows & Screen Designs

**Version:** 1.0  
**Date:** May 18, 2026  
**For:** Development Team

---

## 1. Overview

This document describes the user interface design, navigation structure, and screen-by-screen workflows for the RCM application.

**Design Principles:**
- **Simple & Clean:** Minimal clutter, focus on task completion
- **Role-Based:** Each user sees only what they need
- **Fast:** <2 second page loads, keyboard shortcuts
- **Mobile-Responsive:** Works on desktop, tablet, phone
- **Accessible:** WCAG 2.1 Level AA compliant

---

## 2. Navigation Structure

### Main Navigation (Left Sidebar):

```
┌─────────────────────────────────────────┐
│  [Logo] RCM Application                 │
├─────────────────────────────────────────┤
│  🏠 Dashboard                            │
│  👥 Patients                             │
│  📅 Appointments                         │
│  🏥 Encounters                           │
│  💰 Charges                              │
│  📋 Claims                               │
│  💳 Payments                             │
│  ❌ Denials                              │
│  📊 Reports                              │
│  ⚙️  Settings                            │
│  👤 [User Name] ▼                        │
│     - Profile                            │
│     - Logout                             │
└─────────────────────────────────────────┘
```

**Navigation varies by role:**
- **Front Desk:** Dashboard, Patients, Appointments, Payments
- **Coder:** Dashboard, Encounters, Claims (view only)
- **Biller:** Dashboard, Claims, Payments (view only)
- **AR Manager:** Dashboard, Claims, Payments, Denials, Reports
- **Finance Manager:** Dashboard, Reports

---

## 3. Screen Designs by Module

### Module 1: Dashboard

**Purpose:** Role-specific overview of key metrics and tasks

#### Front Desk Dashboard:

```
┌──────────────────────────────────────────────────────────────┐
│  Dashboard - Front Desk                        [Date: Today]  │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Today's Appts   │  │ Checked In      │  │ Copays       │ │
│  │      45         │  │      32         │  │  $1,240      │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
│                                                                │
│  Today's Appointments                      [Search Patient]   │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Time  │ Patient Name    │ Provider   │ Status  │ Action│  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ 9:00  │ John Doe        │ Dr. Smith  │ Waiting │[Check]│  │
│  │ 9:30  │ Jane Smith      │ Dr. Jones  │ Checked │       │  │
│  │ 10:00 │ Bob Johnson     │ Dr. Smith  │ Pending │[Check]│  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  Quick Actions                                                 │
│  [+ New Patient]  [+ Schedule Appointment]  [Verify Insurance]│
└──────────────────────────────────────────────────────────────┘
```

#### Billing Dashboard:

```
┌──────────────────────────────────────────────────────────────┐
│  Dashboard - Billing                           [Date: Today]  │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ Clean Claim │  │ Denial Rate │  │ Submitted   │          │
│  │    96.2%    │  │    4.1%     │  │    142      │          │
│  │  ↑ 2.1%     │  │  ↓ 0.8%     │  │   Today     │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                                │
│  Claims Requiring Action                                      │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Claim #   │ Patient      │ Amount  │ Status   │ Action │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ CLM12345  │ John Doe     │ $450    │ Error    │ [Fix]  │  │
│  │ CLM12346  │ Jane Smith   │ $1,200  │ Error    │ [Fix]  │  │
│  │ CLM12347  │ Bob Johnson  │ $850    │ Ready    │[Submit]│  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  Quick Actions                                                 │
│  [Scrub Claims]  [Submit Batch]  [Check Status]               │
└──────────────────────────────────────────────────────────────┘
```

#### AR Manager Dashboard:

```
┌──────────────────────────────────────────────────────────────┐
│  Dashboard - AR Management                     [Date: Today]  │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Total AR │  │ Days in  │  │ AR >90   │  │ Denials  │    │
│  │ $2.4M    │  │ AR: 38   │  │ Days:12% │  │ Pending  │    │
│  │          │  │ ↓ 3 days │  │ ↓ 2%     │  │   47     │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                                │
│  AR Aging                                                      │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ 0-30 days:  $1.2M (50%) ████████████                   │  │
│  │ 31-60 days: $720K (30%) ███████                        │  │
│  │ 61-90 days: $240K (10%) ██                             │  │
│  │ 90+ days:   $240K (10%) ██                             │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  High Priority Denials                                        │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Claim #   │ Patient    │ Amount  │ Reason    │ Action  │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ CLM12340  │ John Doe   │ $5,400  │ Auth Mis  │ [Appeal]│  │
│  │ CLM12341  │ Jane Smith │ $3,200  │ Coding    │ [Review]│  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  Quick Actions                                                 │
│  [Post Payments]  [Work Denials]  [Follow Up >60 Days]        │
└──────────────────────────────────────────────────────────────┘
```

---

### Module 2: Patient Registration

**Screen: Patient Search/Create**

```
┌──────────────────────────────────────────────────────────────┐
│  Patients                                      [+ New Patient] │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  Search Patient                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ 🔍 Search by Name, MRN, DOB, Phone...                  │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  Search Results                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ MRN      │ Name           │ DOB        │ Phone    │ Act │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ MRN12345 │ Doe, John A    │ 01/15/1980 │ 555-1234 │[View│  │
│  │ MRN12346 │ Doe, Jane M    │ 03/22/1985 │ 555-5678 │[View│  │
│  │ MRN12347 │ Doe, Robert J  │ 07/10/1975 │ 555-9012 │[View│  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  [Showing 3 of 3 results]                                     │
└──────────────────────────────────────────────────────────────┘
```

**Screen: New Patient Registration**

```
┌──────────────────────────────────────────────────────────────┐
│  New Patient Registration                          [Save] [X] │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  Demographics                                                  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ First Name*     [____________]  MI [_]  Last Name* [___]│  │
│  │ Date of Birth*  [MM/DD/YYYY]    Gender* [Male ▼]       │  │
│  │ SSN             [___-__-____]   (encrypted)             │  │
│  │ Phone (Mobile)* [(___) ___-____]                        │  │
│  │ Email           [_____________________]                 │  │
│  │ Address*        [_____________________]                 │  │
│  │ City*           [__________]  State* [MA ▼] ZIP* [____] │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  Emergency Contact                                             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Name*           [_____________________]                 │  │
│  │ Relationship*   [Spouse ▼]                              │  │
│  │ Phone*          [(___) ___-____]                        │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  Insurance Information                                         │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Primary Insurance                                       │  │
│  │ Payer*          [Blue Cross Blue Shield ▼]             │  │
│  │ Policy Number*  [_____________________]                 │  │
│  │ Group Number    [_____________________]                 │  │
│  │ Subscriber Name*[_____________________]                 │  │
│  │ Relationship*   [Self ▼]                                │  │
│  │ Upload Card     [Choose File] [Front] [Back]            │  │
│  │                                                          │  │
│  │ [+ Add Secondary Insurance]                             │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  [Verify Insurance Now]                    [Save] [Cancel]    │
└──────────────────────────────────────────────────────────────┘
```

**Duplicate Detection Alert:**

```
┌──────────────────────────────────────────────┐
│  ⚠️  Possible Duplicate Patient              │
├──────────────────────────────────────────────┤
│                                              │
│  A similar patient already exists:           │
│                                              │
│  Name: John A Doe                            │
│  DOB:  01/15/1980                            │
│  MRN:  MRN12345                              │
│                                              │
│  Is this the same patient?                   │
│                                              │
│  [Yes, Use Existing]  [No, Create New]       │
└──────────────────────────────────────────────┘
```

---

### Module 3: Insurance Verification

**Screen: Eligibility Check**

```
┌──────────────────────────────────────────────────────────────┐
│  Insurance Verification - John Doe (MRN12345)                 │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  Primary Insurance: Blue Cross Blue Shield                    │
│  Policy Number: POL987654                                     │
│  Service Date: [05/18/2026]              [Verify Eligibility] │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ✅ Verification Results (Checked: 05/18/2026 2:30 PM)  │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ Coverage Status:    ✅ ACTIVE                          │  │
│  │ Effective Date:     01/01/2026                          │  │
│  │ Plan Type:          PPO                                 │  │
│  │                                                          │  │
│  │ Financial Responsibility:                               │  │
│  │ ├─ Copay:           $30.00                              │  │
│  │ ├─ Deductible:      $1,500 annual / $500 remaining     │  │
│  │ ├─ Coinsurance:     20% after deductible               │  │
│  │ └─ Out-of-Pocket:   $5,000 annual / $3,200 remaining   │  │
│  │                                                          │  │
│  │ Network Status:     ✅ IN-NETWORK                       │  │
│  │ Prior Auth Req:     ⚠️  YES (for procedures >$1,000)   │  │
│  │ Referral Req:       ❌ NO                               │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  Verification History                                          │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Date/Time         │ Status  │ Verified By              │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ 05/18/2026 2:30PM │ Active  │ Sarah Johnson            │  │
│  │ 04/15/2026 9:15AM │ Active  │ Sarah Johnson            │  │
│  │ 03/10/2026 1:45PM │ Active  │ Mike Davis               │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  [Print Verification]  [Email to Patient]  [Close]            │
└──────────────────────────────────────────────────────────────┘
```

---

### Module 4: Appointment Scheduling

**Screen: Schedule Appointment**

```
┌──────────────────────────────────────────────────────────────┐
│  Schedule Appointment                              [Save] [X] │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  Patient*         [John Doe (MRN12345) ▼]     [+ New Patient] │
│  Provider*        [Dr. Jane Smith ▼]                          │
│  Appointment Type*[Office Visit - Follow Up ▼]                │
│  Duration         [30 minutes]                                │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Calendar - May 2026                    [Week] [Month]   │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ Mon 5/18  │ Tue 5/19  │ Wed 5/20  │ Thu 5/21  │ Fri 5/22│  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ 9:00  ✅  │ 9:00  ✅  │ 9:00  ❌  │ 9:00  ✅  │ 9:00  ✅│  │
│  │ 9:30  ✅  │ 9:30  ❌  │ 9:30  ❌  │ 9:30  ✅  │ 9:30  ❌│  │
│  │ 10:00 ❌  │ 10:00 ✅  │ 10:00 ❌  │ 10:00 ❌  │ 10:00 ✅│  │
│  │ 10:30 ✅  │ 10:30 ✅  │ 10:30 ❌  │ 10:30 ✅  │ 10:30 ✅│  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  Selected: Tuesday, May 19, 2026 at 10:00 AM                  │
│                                                                │
│  Reason for Visit [Annual checkup                         ]   │
│  Special Notes    [Patient prefers morning appointments   ]   │
│                                                                │
│  Send Reminders:  ☑ SMS  ☑ Email  ☐ Phone Call               │
│                                                                │
│  [Save Appointment]  [Cancel]                                 │
└──────────────────────────────────────────────────────────────┘
```

---

### Module 5: Encounter Management

**Screen: Check-In Patient**

```
┌──────────────────────────────────────────────────────────────┐
│  Check-In - John Doe                                   [Save] │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  Patient: John Doe (MRN12345)                                 │
│  Appointment: 05/18/2026 10:00 AM with Dr. Jane Smith         │
│                                                                │
│  ✅ Step 1: Verify Demographics                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Name:    John A Doe                                     │  │
│  │ DOB:     01/15/1980                                     │  │
│  │ Address: 123 Main St, Boston, MA 02101                 │  │
│  │ Phone:   (555) 123-4234                                │  │
│  │                                                          │  │
│  │ ☑ Patient confirms information is correct              │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  ✅ Step 2: Verify Insurance                                  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Primary: Blue Cross Blue Shield (POL987654)            │  │
│  │ Status:  ✅ ACTIVE (Verified today at 9:45 AM)         │  │
│  │ Copay:   $30.00                                         │  │
│  │                                                          │  │
│  │ [Re-verify Insurance]                                   │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  ⚠️  Step 3: Collect Copay                                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Copay Amount: $30.00                                    │  │
│  │ Payment Method: [Credit Card ▼]                         │  │
│  │                                                          │  │
│  │ [Process Payment]                                       │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  ✅ Step 4: Create Encounter                                  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Encounter Type: [Office Visit ▼]                       │  │
│  │ Chief Complaint: [Annual checkup                    ]   │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  [Complete Check-In]  [Cancel]                                │
└──────────────────────────────────────────────────────────────┘
```

---

### Module 6: Medical Coding

**Screen: Coding Worklist**

```
┌──────────────────────────────────────────────────────────────┐
│  Coding Worklist                                              │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  Filter: [All Providers ▼] [Last 7 Days ▼] [Not Coded ▼]     │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Enc ID   │ Date   │ Patient    │ Provider  │ Type │ Act │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ ENC12345 │ 5/18   │ Doe, John  │ Dr. Smith │ Off  │[Code│  │
│  │ ENC12346 │ 5/18   │ Smith, Jane│ Dr. Jones │ Off  │[Code│  │
│  │ ENC12347 │ 5/17   │ Johnson, B │ Dr. Smith │ Proc │[Code│  │
│  │ ENC12348 │ 5/17   │ Davis, Mary│ Dr. Brown │ Off  │[Code│  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  [Showing 4 of 47 encounters]                [Next Page →]    │
└──────────────────────────────────────────────────────────────┘
```

**Screen: Code Encounter**

```
┌──────────────────────────────────────────────────────────────┐
│  Code Encounter - ENC12345                         [Save] [X] │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  Patient: John Doe (MRN12345)  │  Provider: Dr. Jane Smith   │
│  Date: 05/18/2026              │  Type: Office Visit         │
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Clinical Documentation                                   │ │
│  ├─────────────────────────────────────────────────────────┤ │
│  │ Chief Complaint: Annual checkup                          │ │
│  │                                                           │ │
│  │ HPI: 46-year-old male presents for annual physical.      │ │
│  │ No acute complaints. Reports feeling well overall.       │ │
│  │                                                           │ │
│  │ PMH: Type 2 Diabetes (controlled), Hypertension          │ │
│  │                                                           │ │
│  │ Exam: BP 128/82, HR 72, Wt 185 lbs                       │ │
│  │ General: Well-appearing, no distress                     │ │
│  │ CV: Regular rate and rhythm                              │ │
│  │ Lungs: Clear bilaterally                                 │ │
│  │                                                           │ │
│  │ Assessment:                                               │ │
│  │ 1. Type 2 Diabetes, controlled                           │ │
│  │ 2. Essential Hypertension, controlled                    │ │
│  │                                                           │ │
│  │ Plan:                                                     │ │
│  │ - Continue current medications                           │ │
│  │ - HbA1c ordered                                          │ │
│  │ - Follow up 3 months                                     │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Diagnosis Codes (ICD-10)                                 │ │
│  ├─────────────────────────────────────────────────────────┤ │
│  │ [Search ICD-10: diabetes type 2          ] [Search]      │ │
│  │                                                           │ │
│  │ ☑ E11.9  Type 2 diabetes without complications (Primary) │ │
│  │ ☑ I10    Essential hypertension                          │ │
│  │                                                           │ │
│  │ [+ Add Diagnosis]                                        │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Procedure Codes (CPT)                                    │ │
│  ├─────────────────────────────────────────────────────────┤ │
│  │ [Search CPT: office visit            ] [Search]          │ │
│  │                                                           │ │
│  │ Code    Description              Modifier  Dx Link  Amt  │ │
│  │ 99214   Office visit, level 4    [None ▼] [1,2]  $150   │ │
│  │                                                           │ │
│  │ [+ Add Procedure]                                        │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                                │
│  ⚠️  Coding Alerts:                                           │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ ✅ Medical necessity supported                           │ │
│  │ ✅ No NCCI edits                                         │ │
│  │ ⚠️  Consider E&M level 5 (99215) based on complexity    │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                                │
│  [Mark as Coded - Ready to Bill]  [Save Draft]  [Cancel]     │
└──────────────────────────────────────────────────────────────┘
```

---

### Module 7: Claim Management

**Screen: Claim Scrubbing**

```
┌──────────────────────────────────────────────────────────────┐
│  Claim Scrubbing                                              │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  [Select Claims to Scrub]                                     │
│  ☑ All Ready Claims (47)  ☐ Selected Claims                  │
│                                                                │
│  [Start Scrubbing]                                            │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ⏳ Scrubbing in progress... 35 of 47 complete (74%)     │  │
│  │ ████████████████████░░░░░░░                             │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  Results:                                                      │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ✅ Clean Claims:    42 (89%)                            │  │
│  │ ⚠️  Warnings:        3 (6%)                             │  │
│  │ ❌ Errors:          2 (5%)                              │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  Claims with Errors                                            │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Claim #   │ Patient    │ Error                   │ Act  │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ CLM12345  │ Doe, John  │ Missing authorization   │ [Fix]│  │
│  │ CLM12346  │ Smith, Jane│ Invalid diagnosis code  │ [Fix]│  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  [Submit Clean Claims (42)]  [Export Report]  [Close]         │
└──────────────────────────────────────────────────────────────┘
```

**Screen: Claim Detail with Errors**

```
┌──────────────────────────────────────────────────────────────┐
│  Claim CLM12345 - John Doe                         [Save] [X] │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  ❌ Scrubbing Errors (1 Fatal, 0 Warnings)                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ❌ FATAL: Prior authorization required but missing      │  │
│  │    CPT code 99214 requires authorization for this payer │  │
│  │    Action: Obtain authorization or remove procedure     │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  Claim Information                                             │
│  Patient:     John Doe (MRN12345)                             │
│  Payer:       Blue Cross Blue Shield                          │
│  Service Date: 05/18/2026                                     │
│  Total Charge: $150.00                                        │
│                                                                │
│  Authorization Number: [____________]  [Search Authorizations]│
│                                                                │
│  [Re-Scrub]  [Save]  [Cancel]                                 │
└──────────────────────────────────────────────────────────────┘
```

---

### Module 8: Payment Posting

**Screen: ERA Import**

```
┌──────────────────────────────────────────────────────────────┐
│  Payment Posting - ERA Import                                 │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  Upload ERA File (EDI 835)                                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ [Choose File] 835_BCBS_05202026.txt                     │  │
│  │                                                          │  │
│  │ [Upload and Process]                                    │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  Recent ERA Files                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Date     │ Payer  │ Check#  │ Amount   │ Claims │ Status│  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ 5/20/26  │ BCBS   │ CHK1234 │ $12,450  │ 15     │ Posted│  │
│  │ 5/19/26  │ UHC    │ CHK1235 │ $8,200   │ 12     │ Posted│  │
│  │ 5/18/26  │ Aetna  │ CHK1236 │ $5,600   │ 8      │ Posted│  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

**Screen: ERA Auto-Posting Results**

```
┌──────────────────────────────────────────────────────────────┐
│  ERA Processing Results - CHK1234                             │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  Payer: Blue Cross Blue Shield                                │
│  Check Number: CHK1234                                        │
│  Check Date: 05/20/2026                                       │
│  Total Amount: $12,450.00                                     │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ✅ Auto-Posted:     12 claims ($10,200)                 │  │
│  │ ⚠️  Manual Review:   3 claims ($2,250)                  │  │
│  │ ❌ Denials:         2 claims ($1,500)                   │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  Claims Requiring Manual Review                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Claim #   │ Patient    │ Billed │ Paid  │ Reason  │ Act │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ CLM12340  │ Doe, John  │ $450   │ $0    │ No Match│[Post│  │
│  │ CLM12341  │ Smith, Jane│ $800   │ $750  │ Variance│[Post│  │
│  │ CLM12342  │ Johnson, B │ $1,000 │ $1,000│ Dup Claim[Post│  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  [Review Manual Items]  [View Denials]  [Close]               │
└──────────────────────────────────────────────────────────────┘
```

---

### Module 9: Denial Management

**Screen: Denial Worklist**

```
┌──────────────────────────────────────────────────────────────┐
│  Denial Management                                            │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  Filter: [All Payers ▼] [Last 30 Days ▼] [Not Worked ▼]      │
│                                                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Total    │  │ High $   │  │ Appeal   │  │ Overturn │    │
│  │ Denials  │  │ (>$1K)   │  │ Deadline │  │ Rate     │    │
│  │   47     │  │   12     │  │ <7 Days  │  │   62%    │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                                │
│  Denial Worklist                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Claim#│Patient│Amount│Reason│Deadline│Assigned│Action │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │CLM1234│Doe, J │$5,400│Auth  │5/25/26 │Sarah J │[Appeal│  │
│  │CLM1235│Smith,J│$3,200│Coding│5/27/26 │Mike D  │[Review│  │
│  │CLM1236│Johns,B│$2,100│Elig  │5/30/26 │Sarah J │[Appeal│  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  Top Denial Reasons (Last 30 Days)                            │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Missing Authorization:      15 (32%) ████████           │  │
│  │ Incorrect Coding:           12 (26%) ██████             │  │
│  │ Eligibility Issues:         10 (21%) █████              │  │
│  │ Timely Filing:               6 (13%) ███                │  │
│  │ Other:                       4 (8%)  ██                 │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  [Work Next Denial]  [Export Report]                          │
└──────────────────────────────────────────────────────────────┘
```

---

### Module 10: Reports

**Screen: Reports Dashboard**

```
┌──────────────────────────────────────────────────────────────┐
│  Reports & Analytics                                          │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  Standard Reports                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Financial Reports                                       │  │
│  │ ├─ Daily Revenue Report                        [Run]    │  │
│  │ ├─ Monthly Revenue by Department               [Run]    │  │
│  │ ├─ Monthly Revenue by Provider                 [Run]    │  │
│  │ ├─ Monthly Revenue by Payer                    [Run]    │  │
│  │ └─ AR Aging Report                             [Run]    │  │
│  │                                                          │  │
│  │ Operational Reports                                     │  │
│  │ ├─ Clean Claim Rate                            [Run]    │  │
│  │ ├─ Denial Rate Analysis                        [Run]    │  │
│  │ ├─ Coding Productivity                         [Run]    │  │
│  │ ├─ Billing Productivity                        [Run]    │  │
│  │ └─ Charge Capture Report                       [Run]    │  │
│  │                                                          │  │
│  │ Compliance Reports                                      │  │
│  │ ├─ Coding Accuracy Audit                       [Run]    │  │
│  │ ├─ HIPAA Access Audit                          [Run]    │  │
│  │ └─ Overpayment Report                          [Run]    │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  Custom Reports                                                │
│  [+ Create Custom Report]                                     │
│                                                                │
│  Scheduled Reports                                             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Report Name          │ Schedule │ Recipients  │ Action  │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │ Daily Revenue        │ Daily    │ CFO, Finance│ [Edit]  │  │
│  │ AR Aging             │ Weekly   │ AR Team     │ [Edit]  │  │
│  │ Denial Analysis      │ Monthly  │ Management  │ [Edit]  │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. Mobile Responsive Design

**Mobile View: Dashboard (Front Desk)**

```
┌─────────────────────┐
│ ☰  RCM App   [User]│
├─────────────────────┤
│                     │
│ Today's Appts: 45   │
│ Checked In: 32      │
│ Copays: $1,240      │
│                     │
│ ┌─────────────────┐ │
│ │ Next Appt       │ │
│ │ 10:00 AM        │ │
│ │ John Doe        │ │
│ │ Dr. Smith       │ │
│ │ [Check In]      │ │
│ └─────────────────┘ │
│                     │
│ Quick Actions       │
│ [New Patient]       │
│ [Schedule]          │
│ [Verify Insurance]  │
│                     │
└─────────────────────┘
```

---

## 5. UI Component Library

### Buttons:
- **Primary:** Blue background, white text (Save, Submit, Create)
- **Secondary:** White background, blue border (Cancel, Back)
- **Danger:** Red background, white text (Delete, Reject)
- **Success:** Green background, white text (Approve, Complete)

### Colors:
- **Primary Blue:** #0066CC
- **Success Green:** #28A745
- **Warning Yellow:** #FFC107
- **Danger Red:** #DC3545
- **Gray:** #6C757D

### Icons:
- Use **Lucide Icons** or **Font Awesome**
- Consistent icon usage across app

### Forms:
- Clear labels above fields
- Required fields marked with *
- Inline validation with error messages
- Placeholder text for guidance

---

## 6. Accessibility Features

- **Keyboard Navigation:** Tab through all interactive elements
- **Screen Reader Support:** ARIA labels on all inputs
- **Color Contrast:** WCAG AA compliant (4.5:1 ratio)
- **Focus Indicators:** Clear blue outline on focused elements
- **Error Announcements:** Screen reader announces validation errors

---

## 7. Performance Optimization

- **Lazy Loading:** Load data as user scrolls
- **Pagination:** Max 50 records per page
- **Caching:** Cache frequently accessed data (payers, providers, codes)
- **Debouncing:** Search inputs debounced by 300ms

---

**Summary:**

This document provides the complete UI/UX blueprint for your RCM application. Each screen is designed for:
- **Efficiency:** Minimal clicks to complete tasks
- **Clarity:** Clear visual hierarchy and status indicators
- **Error Prevention:** Validation and alerts before submission
- **Role Optimization:** Each user sees only what they need

Your development team can now build the frontend using these wireframes as a guide.

---

**All 5 Pre-Development Documents Complete! ✅**

1. ✅ System Requirements Summary
2. ✅ Database Design
3. ✅ User Roles & Permissions
4. ✅ API Integration Requirements
5. ✅ UI/UX Workflows

**Ready to start development!**
