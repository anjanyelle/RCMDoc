# Module 3: Insurance Verification - Flow Documentation

**Version:** 1.0  
**Module ID:** MOD-003  
**Category:** Patient Management

---

## 1. Module Overview

**Purpose:** Verify patient's insurance coverage and eligibility before providing services.

**Why Hospitals Use It:** Prevent claim denials, confirm coverage, check copay/deductible amounts.

**Business Goal:** Reduce eligibility-related claim denials, avoid wrong patient billing, confirm patient responsibility before visit, and improve clean claim rate.

**Main Users:** Front Desk Staff, Billing Team, Authorization Team

---

## 2. Actors Involved

```
┌─────────────────────────────────────────────────┐
│ ACTORS IN INSURANCE VERIFICATION MODULE         │
├─────────────────────────────────────────────────┤
│                                                  │
│ 1. Front Desk Staff                             │
│    - Initiates verification                      │
│    - Reviews verification results                │
│                                                  │
│ 2. Billing Team                                  │
│    - Reviews coverage details                    │
│    - Checks authorization requirements           │
│                                                  │
│ 3. System                                        │
│    - Verification Engine                         │
│    - Database                                    │
│                                                  │
│ 4. External APIs                                 │
│    - Availity (Real-time eligibility - 270/271) │
│    - Waystar (Eligibility check)                 │
│    - Payer APIs (Direct connections)             │
│                                                  │
│ 5. Authorization Team                            │
│    - Reviews services requiring prior auth      │
│    - Starts prior auth workflow when required   │
│    - Tracks authorization approval/denial       │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 3. Step-by-Step Workflow

```
┌─────────────────────┐
│ Patient Registered  │
│ (from Module 2)     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Staff Opens         │
│ Insurance           │
│ Verification Screen │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ System Auto-loads   │
│ Patient Insurance   │
│ Details             │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Display:            │
│ - Payer Name        │
│ - Member ID         │
│ - Group Number      │
│ - Service Date      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Staff Clicks        │
│ "Verify Coverage"   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Check if Valid      │
│ Verification        │
│ Already Exists      │
└──────────┬──────────┘
           ├──────────────────────────────────┐
     [No]  │                                  │ [Yes]
           ▼                                  ▼
┌─────────────────────┐            ┌─────────────────────┐
│ Show Loading:       │            │ Load Saved Result   │
│ "Checking with      │            │ (Skip API Request)  │
│  insurance..."      │            └──────────┬──────────┘
└──────────┬──────────┘                       │
           ↓                                  │
┌─────────────────────┐                       │
│ Backend Builds      │                       │
│ EDI 270 Request     │                       │
│ (Eligibility Inquiry)                       │
└──────────┬──────────┘                       │
           ↓                                  │
┌─────────────────────┐                       │
│ Send to Availity    │                       │
│ API                 │                       │
└──────────┬──────────┘                       │
           ↓                                  │
┌─────────────────────┐                       │
│ Availity Forwards   │                       │
│ to Insurance Payer  │                       │
└──────────┬──────────┘                       │
           ↓                                  │
┌─────────────────────┐                       │
│ Payer Processes     │                       │
│ Request             │                       │
└──────────┬──────────┘                       │
           ↓                                  │
┌─────────────────────┐                       │
│ Payer Returns       │                       │
│ EDI 271 Response    │                       │
└──────────┬──────────┘                       │
           ↓                                  │
┌─────────────────────┐                       │
│ Availity Returns    │                       │
│ to Backend          │                       │
└──────────┬──────────┘                       │
           ↓                                  │
┌─────────────────────┐                       │
│ Backend Parses      │                       │
│ EDI 271 Response    │                       │
└──────────┬──────────┘                       │
    ┌──────┴──────┐                           │
    │             │                           │
    ▼             ▼                           │
┌─────────┐  ┌─────────────────┐              │
│ Active  │  │ Inactive/Error  │              │
│Coverage │  └────────┬────────┘              │
└────┬────┘           │                       │
     │                ▼                       │
     │       ┌─────────────────┐              │
     │       │ Show Error:     │              │
     │       │ - Not Active    │              │
     │       │ - Invalid ID    │              │
     │       │ - Payer Down    │              │
     │       └────────┬────────┘              │
     │                │                       │
     │                ▼                       │
     │       ┌─────────────────┐              │
     │       │ Options:        │              │
     │       │ 1. Retry        │              │
     │       │ 2. Manual Entry │              │
     │       │ 3. Self-Pay     │              │
     │       └─────────────────┘              │
     │                                        │
     ▼                                        │
┌─────────────────────┐                       │
│ Save Verification   │                       │
│ Results to Database │                       │
└──────────┬──────────┘                       │
           │                                  │
           ├──────────────────────────────────┘
           ↓
┌─────────────────────┐
│ Display Results:    │
│                     │
│ ✅ Coverage Active  │
│                     │
│ Plan Details:       │
│ - Plan Name: PPO    │
│ - Effective Date    │
│ - Copay: $25        │
│ - Deductible: $500  │
│ - Remaining: $200   │
│                     │
│ Coverage:           │
│ - Office Visit: ✅  │
│ - Surgery: ✅       │
│ - Lab: ✅           │
│ - Radiology: ✅     │
│                     │
│ Authorization:      │
│ - Required for MRI  │
│ - Required for CT   │
└──────────┬──────────┘
           ↓
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌─────────┐  ┌─────────────────┐
│ Auth    │  │ No Auth Required│
│Required │  └────────┬────────┘
└────┬────┘           │
     │                │
     ▼                │
┌─────────────────┐   │
│ Redirect to     │   │
│ Prior Auth      │   │
│ Module          │   │
└────┬────────────┘   │
     │                │
     └────────┬───────┘
              ↓
     ┌─────────────────┐
     │ Print Verification│
     │ Summary          │
     └────┬─────────────┘
          ↓
     ┌─────────────────┐
     │ Attach to Patient│
     │ Chart            │
     └────┬─────────────┘
          ↓
     ┌─────────────────┐
     │ Proceed to      │
     │ Appointment or  │
     │ Check-in        │
     └─────────────────┘
```

---

## 4. EDI 270/271 Transaction Flow

```
Hospital System          Availity API         Insurance Payer
       │                      │                      │
       │ Build EDI 270        │                      │
       │ Request:             │                      │
       │ - Member ID          │                      │
       │ - Service Date       │                      │
       │ - Service Type       │                      │
       │ - Trace/Trans ID     │                      │
       ├─────────────────────>│                      │
       │                      │                      │
       │                      │ Forward 270          │
       │                      ├─────────────────────>│
       │                      │                      │
       │                      │                      │
       │                      │      Process         │
       │                      │      Eligibility     │
       │                      │                      │
       │                      │                      │
       │                      │ EDI 271 Response     │
       │                      │<─────────────────────┤
       │                      │                      │
       │ EDI 271 Response     │                      │
       │<─────────────────────┤                      │
       │                      │                      │
       │ Parse Response:      │                      │
       │ - Active/Inactive    │                      │
       │ - Plan Details       │                      │
       │ - Copay/Deductible   │                      │
       │ - Coverage Limits    │                      │
       │ - Trace/Trans ID     │                      │
       │                      │                      │
```

---

## 5. Use Case Diagram

```
┌──────────────┐                          ┌──────────────────┐
│ Front Desk   │─────────────────────────>│ Verify Insurance │
│ Staff        │                          │ Eligibility      │
└──────────────┘                          └──────────────────┘
        │                                          │
        │                                 ┌────────┴────────┐
        │                                 │                 │
        │                                 ▼                 ▼
        │                         ┌──────────────┐  ┌──────────────┐
        │                         │ Check Active │  │ Get Coverage │
        │                         │ Coverage     │  │ Details      │
        │                         └──────────────┘  └──────────────┘
        │
        │                                 ┌──────────────────┐
        └────────────────────────────────>│ Manual           │
                                          │ Verification     │
                                          │ Entry            │
                                          └──────────────────┘

┌──────────────┐                          ┌──────────────────┐
│ Billing Team │─────────────────────────>│ Review Prior Auth│
│              │                          │ Requirements     │
└──────────────┘                          └──────────────────┘

┌──────────────┐                          ┌──────────────────┐
│ System       │─────────────────────────>│ Send EDI 270     │
│              │                          │ Request          │
└──────┬───────┘                          └──────────────────┘
       │
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Parse EDI 271    │
                                          │ Response         │
                                          └──────────────────┘

┌──────────────┐                          ┌──────────────────┐
│ Availity API │─────────────────────────>│ Forward to Payer │
│              │                          └──────────────────┘
└──────────────┘
```

---

## 6. Activity Flow Diagram

```
┌─────────┐
│  START  │
└────┬────┘
     │
     ▼
┌─────────────────────┐
│ Load Patient        │
│ Insurance Info      │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Enter Service Date  │
│ (Default: Today)    │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Select Service Type:│
│ - Office Visit      │
│ - Surgery           │
│ - Lab               │
│ - Radiology         │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Click "Verify"      │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Build EDI 270       │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ POST to Availity    │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Wait for Response   │
│ (2-10 seconds)      │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Success?╲───No──────┐
  ╲       ╱            │
   ╲     ╱             │
    ╲   ╱              │
     │Yes              │
     │                 ▼
     │         ┌─────────────────┐
     │         │ Show Error:     │
     │         │ - Timeout       │
     │         │ - Invalid ID    │
     │         │ - Payer Down    │
     │         └────┬────────────┘
     │              │
     │              ▼
     │         ┌─────────────────┐
     │         │ Save Failed     │
     │         │ Attempt & Reason│
     │         └────┬────────────┘
     │              │
     │              ▼
     │         ┌─────────────────┐
     │         │ Retry or Manual?│
     │         └─────────────────┘
     │
     ▼
┌─────────────────────┐
│ Parse EDI 271       │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Active?╱───No──────┐
  ╲      ╱            │
   ╲    ╱             │
    ╲  ╱              │
     │Yes             │
     │                ▼
     │         ┌─────────────────┐
     │         │ Coverage Inactive│
     │         │ Options:        │
     │         │ - Self-Pay      │
     │         │ - Update Info   │
     │         └─────────────────┘
     │
     ▼
┌─────────────────────┐
│ Extract Details:    │
│ - Plan Name         │
│ - Copay             │
│ - Deductible        │
│ - Out-of-Pocket Max │
│ - Coverage %        │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Save to Database    │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Display Results     │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Prior ╲───Yes──────┐
  ╲Auth  ╱            │
   ╲Req? ╱            │
    ╲  ╱              │
     │No              │
     │                ▼
     │         ┌─────────────────┐
     │         │ Flag for Prior  │
     │         │ Authorization   │
     │         └────┬────────────┘
     │              │
     │              │
     └──────┬───────┘
            ↓
     ┌─────────────────┐
     │ Print Summary   │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Proceed to      │
     │ Next Step       │
     └────┬────────────┘
          ↓
     ┌─────────┐
     │   END   │
     └─────────┘
```

---

## 7. Sequence Diagram

```
Staff    Frontend    Backend    Availity    Payer    Database
  │          │          │          │          │          │
  │ Click    │          │          │          │          │
  │ Verify   │          │          │          │          │
  ├─────────>│          │          │          │          │
  │          │          │          │          │          │
  │          │ POST /verify-insurance        │          │
  │          ├─────────>│          │          │          │
  │          │          │          │          │          │
  │          │          │ Build    │          │          │
  │          │          │ EDI 270  │          │          │
  │          │          │          │          │          │
  │          │          │ POST     │          │          │
  │          │          ├─────────>│          │          │
  │          │          │          │          │          │
  │          │          │          │ Forward  │          │
  │          │          │          │ 270      │          │
  │          │          │          ├─────────>│          │
  │          │          │          │          │          │
  │          │          │          │          │ Process  │
  │          │          │          │          │          │
  │          │          │          │ EDI 271  │          │
  │          │          │          │<─────────┤          │
  │          │          │          │          │          │
  │          │          │ Response │          │          │
  │          │          │<─────────┤          │          │
  │          │          │          │          │          │
  │          │          │ Parse    │          │          │
  │          │          │ 271      │          │          │
  │          │          │          │          │          │
  │          │          │ Save     │          │          │
  │          │          ├───────────────────────────────>│
  │          │          │ Audit Log    │          │          │
  │          │          ├──┐       │          │          │
  │          │          │  │       │          │          │
  │          │          │<─┘       │          │          │
  │          │          │          │          │          │
  │          │ Response │          │          │          │
  │          │<─────────┤          │          │          │
  │          │          │          │          │          │
  │ Display  │          │          │          │          │
  │ Results  │          │          │          │          │
  │<─────────┤          │          │          │          │
  │          │          │          │          │          │
```

---

## 8. API Flow

**Request:**
```http
POST /api/insurance/verify
{
  "patientId": "PAT-00001",
  "insuranceId": "INS-00001",
  "providerNpi": "1234567890",
  "payerId": "PAYER01",
  "traceId": "TRC-77665544",
  "serviceDate": "2026-05-20",
  "serviceType": "Office Visit"
}
```

**Response (Active):**
```json
{
  "status": "active",
  "verificationId": "VER-112233",
  "payerResponseCode": "AAA",
  "message": "Eligibility Active",
  "planName": "Aetna PPO",
  "effectiveDate": "2026-01-01",
  "copay": 25,
  "deductible": 500,
  "deductibleRemaining": 200,
  "outOfPocketMax": 3000,
  "outOfPocketRemaining": 1500,
  "coveragePercent": 80,
  "priorAuthRequired": false,
  "authorizationRequiredServices": [
    "MRI",
    "CT Scan"
  ],
  "rawResponseStored": true,
  "verifiedAt": "2026-05-18T19:45:00Z"
}
```

**Response (Inactive):**
```json
{
  "status": "inactive",
  "reason": "Coverage terminated",
  "terminationDate": "2025-12-31"
}
```

---

## 9. Database Flow

```sql
-- Save verification result
INSERT INTO insurance_verifications (
    verification_id,
    trace_id,
    payer_id,
    provider_npi,
    patient_id,
    insurance_id,
    service_type,
    service_date,
    verified_at,
    status,
    response_status,
    error_reason,
    plan_name,
    copay,
    deductible,
    deductible_remaining,
    coverage_percent,
    prior_auth_required,
    raw_edi_271,
    verified_by,
    created_at,
    updated_at
) VALUES (...);

-- Update insurance status
UPDATE patient_insurance
SET verification_status = 'verified',
    last_verified_at = NOW()
WHERE insurance_id = 'INS-00001';
```

---

## 10. Error Scenarios

```
Error 1: Payer Timeout
   ↓
Retry 3 times
   ↓
If still fails → Manual verification

Error 2: Invalid Member ID
   ↓
Show error to staff
   ↓
Update insurance info

Error 3: Coverage Inactive
   ↓
Offer self-pay option
   ↓
Or update insurance

Error 4: Duplicate patient or insurance record
   ↓
Prompt staff to merge/select correct record
   ↓
Flag duplicate for clean-up

Error 5: Missing Payer ID
   ↓
Identify correct payer ID via lookup/payer matrix
   ↓
Update insurance profile and retry

Error 6: Invalid Date of Birth
   ↓
Compare with registered DOB
   ↓
Prompt user to correct DOB in registration and retry

Error 7: API Authentication Failed
   ↓
Generate system alert for administrator
   ↓
Switch to fallback credential or manual check

Error 8: Availity/Payer Service Unavailable
   ↓
Route verification request to manual verification queue
   ↓
Notify staff and enable manual status update

Error 9: Partial Response Received
   ↓
Identify missing required fields (copay, deductible)
   ↓
Prompt staff to perform manual verification call

Error 10: Prior Authorization Required but Not Started
   ↓
Block clinical scheduling progression
   ↓
Route to Prior Auth team queue automatically
```

---

## 11. Dashboard & Status Flow

```
                             ┌──────────────────────┐
                             │ Pending Verification │
                             └──────────┬───────────┘
                                        │
                   ┌────────────────────┴─────────────────────┐
                   ▼                                           ▼
        ┌─────────────────────┐                     ┌─────────────────────┐
        │  Verification Sent  │                     │   Manual Pending    │
        └──────────┬──────────┘                     └──────────┬──────────┘
                   │                                           │
          ┌────────┴────────┬────────────────┐                 │
          ▼                 ▼                ▼                 │
    ┌───────────┐     ┌───────────┐    ┌───────────┐           │
    │  Active   │     │ Inactive  │    │   Payer   │           │
    └─────┬─────┘     └─────┬─────┘    │Unavailable│           │
          │                 │          └─────┬─────┘           │
          ▼                 ▼                ▼                 │
    ┌───────────┐     ┌───────────┐    ┌───────────┐           │
    │ Verified  │     │   Needs   │    │   Retry   │           │
    └─────┬─────┘     │  Update   │    │ Required  │           │
          │           └───────────┘    └───────────┘           │
          ▼                                                    │
    ┌───────────┐                                              │
    │   Auth    │                                              │
    │ Required  │<─────────────────────────────────────────────┘
    └─────┬─────┘
          ▼
   ┌─────────────┐
   │   Expired   │
   │Verification │
   └─────────────┘
```

---

**Next Module:** [Module 4: Appointment Scheduling](Flows_Module_04_Appointment_Scheduling.md)
