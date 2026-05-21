# Module: Clinical Documentation / EMR

**Version:** 1.0
**Module ID:** MOD-007
**Category:** Clinical Documentation & Patient Care

---

## 1. Module Overview

**Purpose:** Capture and manage patient clinical information such as symptoms, vitals, doctor notes, diagnosis, medications, procedures, orders, and treatment plans.

**Why Hospitals Use It:** Clinical documentation is the base for patient care, medical coding, charge capture, claim creation, compliance, and audit proof.

**Main Users:** Doctor, Nurse, Medical Assistant, Clinical Staff, Medical Coder, Billing Team, Compliance Team, Patient

---

## 2. Actors Involved

```
┌─────────────────────────────────────────────────┐
│ ACTORS IN CLINICAL DOCUMENTATION / EMR          │
├─────────────────────────────────────────────────┤
│                                                 │
│ 1. Doctor / Provider                            │
│    - Reviews patient history                    │
│    - Adds diagnosis and treatment notes         │
│    - Prescribes medication                      │
│    - Signs encounter documentation              │
│                                                 │
│ 2. Nurse                                        │
│    - Records vitals                             │
│    - Adds nursing notes                         │
│    - Updates patient status                     │
│                                                 │
│ 3. Medical Assistant                            │
│    - Captures chief complaint                   │
│    - Updates intake details                     │
│                                                 │
│ 4. Patient                                      │
│    - Provides symptoms and history              │
│                                                 │
│ 5. Medical Coder                                │
│    - Uses documentation for ICD/CPT coding      │
│                                                 │
│ 6. Billing Team                                 │
│    - Uses documentation for claim support       │
│                                                 │
│ 7. Compliance Team                              │
│    - Reviews documentation completeness         │
│                                                 │
│ 8. AI System                                    │
│    - Suggests SOAP notes                        │
│    - Summarizes clinical notes                  │
│    - Flags missing documentation                │
│                                                 │
│ 9. System                                       │
│    - EMR Engine                                 │
│    - Documentation Service                      │
│    - Order Management                           │
│    - Audit Log Service                          │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 3. Step-by-Step Workflow

```
┌─────────────────────┐
│ Patient Checked In  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Nurse / MA Opens    │
│ Encounter           │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Capture Intake      │
│ Chief Complaint     │
│ Symptoms / History  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Record Vitals       │
│ BP / Pulse / Temp   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Doctor Opens EMR    │
│ Reviews History     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Doctor Examines     │
│ Patient             │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Add Clinical Notes  │
│ SOAP Format         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Add Diagnosis       │
│ ICD Mapping Ready   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Add Orders          │
│ Lab / Radiology     │
│ Medication          │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Create Treatment    │
│ Plan                │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Documentation       │
│ Completeness Check  │
└──────────┬──────────┘
           ↓
    ╱ ╲
   ╱   ╲
  ╱Complete?╲──No──────────┐
  ╲        ╱               │
   ╲      ╱                │
    ╲    ╱                 │
     │Yes                  ▼
     │              ┌─────────────────┐
     │              │ Show Missing    │
     │              │ Fields to Doctor│
     │              └────────┬────────┘
     │                       │
     └──────────────┬────────┘
                    ↓
┌─────────────────────┐
│ Provider Signature  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Encounter Complete  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Send to Medical     │
│ Coding Queue        │
└─────────────────────┘
```

---

## 4. EMR / Clinical Documentation AI Engine Flow

```
┌─────────────────────┐
│ Encounter Input     │
│ Patient + Visit     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Load Patient Data:  │
│ - Demographics      │
│ - Allergies         │
│ - Past History      │
│ - Medications       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Capture Clinical    │
│ Data                │
│ - Chief Complaint   │
│ - Symptoms          │
│ - Vitals            │
│ - Exam Findings     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ AI Assist:          │
│ - SOAP Suggestions  │
│ - Summarization     │
│ - Missing Fields    │
│ - Risk Alerts       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Add Orders / Plan   │
│ Labs / Imaging / Rx │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Validate Required   │
│ Fields              │
│ - Diagnosis         │
│ - Notes             │
│ - Signature         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Save Documentation  │
│ to EMR              │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Update Encounter    │
│ Status              │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Return to Frontend  │
│ EMR Dashboard       │
└─────────────────────┘
```

---

## 5. Use Case Diagram

```
┌──────────────┐                          ┌──────────────────┐
│ Doctor       │─────────────────────────>│ Review Patient   │
│ / Provider   │                          │ History          │
└──────┬───────┘                          └──────────────────┘
       │
       ├─────────────────────────────────>│ Create Clinical  │
       │                                  │ Notes            │
       │                                  └──────────────────┘
       │
       ├─────────────────────────────────>│ Add Diagnosis    │
       │                                  └──────────────────┘
       │
       ├─────────────────────────────────>│ Add Orders / Rx  │
       │                                  └──────────────────┘
       │
       └─────────────────────────────────>│ Sign Encounter   │
                                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ Nurse        │─────────────────────────>│ Record Vitals    │
└──────┬───────┘                          └──────────────────┘
       │
       └─────────────────────────────────>│ Add Nursing Note │
                                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ Medical      │─────────────────────────>│ Capture Intake   │
│ Assistant    │                          │ Details          │
└──────────────┘                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ AI System    │─────────────────────────>│ Suggest SOAP     │
│              │                          │ Notes            │
└──────┬───────┘                          └──────────────────┘
       │
       └─────────────────────────────────>│ Flag Missing     │
                                          │ Documentation    │
                                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ Medical Coder│─────────────────────────>│ Use Notes for    │
│              │                          │ Coding           │
└──────────────┘                          └──────────────────┘
```

---

## 6. Activity Flow Diagram

```
┌─────────┐
│ START   │
└────┬────┘
     │
     ▼
┌─────────────────────┐
│ Open Encounter      │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Load Patient        │
│ History             │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Capture Chief       │
│ Complaint / Intake  │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Record Vitals       │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Add Clinical Notes  │
│ SOAP Format         │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Add Diagnosis       │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Add Orders / Rx     │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Complete?╲──No──────────┐
  ╲ Notes? ╱               │
   ╲     ╱                 │
    ╲   ╱                  │
     │Yes                  ▼
     │              ┌─────────────────┐
     │              │ Show Missing    │
     │              │ Documentation   │
     │              └────┬────────────┘
     │                   │
     └──────────────┬────┘
                    ▼
┌─────────────────────┐
│ Save Documentation  │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Provider Signature  │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Mark Encounter      │
│ Complete            │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Send to Coding      │
│ Queue               │
└────┬────────────────┘
     │
     ▼
┌─────────┐
│ END     │
└─────────┘
```

---

## 7. Sequence Diagram

```
Doctor/Nurse  Frontend    Backend    AI Engine    Database
    │             │           │           │           │
    │ Open EMR    │           │           │           │
    ├────────────>│           │           │           │
    │             │ GET /emr/encounter   │           │
    │             ├──────────>│           │           │
    │             │           │ Load      │           │
    │             │           │ Patient   │           │
    │             │           │ Data      │           │
    │             │           ├──────────────────────>│
    │             │ Encounter │                       │
    │             │ Data      │                       │
    │             │<──────────┤                       │
    │             │           │                       │
    │ Add Notes   │           │                       │
    ├────────────>│           │                       │
    │             │ POST /emr/notes                   │
    │             ├──────────>│                       │
    │             │           │ AI Assist             │
    │             │           ├──────────>│           │
    │             │           │ SOAP Suggestions      │
    │             │           │<──────────┤           │
    │             │           │ Save Notes            │
    │             │           ├──────────────────────>│
    │             │ Saved     │                       │
    │             │<──────────┤                       │
    │ Sign        │           │                       │
    │ Encounter   │           │                       │
    ├────────────>│           │                       │
    │             │ POST /emr/sign                    │
    │             ├──────────>│                       │
    │             │           │ Update Status         │
    │             │           ├──────────────────────>│
    │             │ Success   │                       │
    │<────────────┤                       │
```

---

## 8. API Flow

**Request:**

```http
POST /api/emr/save-documentation
{
  "encounterId": "ENC-00001",
  "patientId": "PAT-00001",
  "providerId": "DOC-00001",
  "chiefComplaint": "Chest pain",
  "vitals": {
    "bloodPressure": "140/90",
    "pulse": 92,
    "temperature": 98.6,
    "oxygenSaturation": 96
  },
  "clinicalNotes": {
    "subjective": "Patient reports chest pain for 2 hours.",
    "objective": "ECG ordered. Vitals stable.",
    "assessment": "Chest pain, rule out cardiac cause.",
    "plan": "Order ECG, blood work, prescribe medication."
  },
  "diagnosis": [
    {
      "description": "Chest pain",
      "status": "Primary"
    }
  ],
  "orders": [
    {
      "type": "LAB",
      "name": "CBC"
    },
    {
      "type": "RADIOLOGY",
      "name": "ECG"
    }
  ]
}
```

**Response:**

```json
{
  "status": "SUCCESS",
  "encounterId": "ENC-00001",
  "documentationStatus": "DOCUMENTED",
  "missingFields": [],
  "nextStep": "PROVIDER_SIGNATURE",
  "processingTime": "1.6s"
}
```

---

## 9. Database Flow

```sql
-- Save clinical documentation
INSERT INTO clinical_documentation (
    encounter_id,
    patient_id,
    provider_id,
    chief_complaint,
    subjective_note,
    objective_note,
    assessment_note,
    plan_note,
    documentation_status,
    created_at
)
VALUES (
    'ENC-00001',
    'PAT-00001',
    'DOC-00001',
    'Chest pain',
    'Patient reports chest pain for 2 hours.',
    'ECG ordered. Vitals stable.',
    'Chest pain, rule out cardiac cause.',
    'Order ECG, blood work, prescribe medication.',
    'DOCUMENTED',
    NOW()
);

-- Save vitals
INSERT INTO encounter_vitals (
    encounter_id,
    blood_pressure,
    pulse,
    temperature,
    oxygen_saturation
)
VALUES (
    'ENC-00001',
    '140/90',
    92,
    98.6,
    96
);

-- Save orders
INSERT INTO clinical_orders (
    order_id,
    encounter_id,
    order_type,
    order_name,
    status
)
VALUES
    ('ORD-00001', 'ENC-00001', 'LAB', 'CBC', 'ORDERED'),
    ('ORD-00002', 'ENC-00001', 'RADIOLOGY', 'ECG', 'ORDERED');

-- Update encounter status
UPDATE encounters
SET status = 'READY_FOR_SIGNATURE'
WHERE encounter_id = 'ENC-00001';
```

---

## 10. Error Scenarios

```
Error 1: Missing Diagnosis
   ↓
Show validation error
   ↓
Doctor adds diagnosis
   ↓
Continue documentation

Error 2: Missing Provider Signature
   ↓
Cannot close encounter
   ↓
Provider signs documentation
   ↓
Encounter complete

Error 3: Incomplete SOAP Notes
   ↓
AI flags missing section
   ↓
Doctor updates missing details
   ↓
Save notes again

Error 4: Order Missing Details
   ↓
System blocks order
   ↓
Doctor adds required details
   ↓
Order saved

Error 5: Unauthorized EMR Access
   ↓
Block access
   ↓
Save audit log
   ↓
Alert security/compliance team
```

---

## 11. Dashboard Status Flow

```
┌─────────────────────┐
│ Patient Checked In  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Encounter Started   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Intake Completed    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Vitals Added        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Documentation       │
│ In Progress         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Orders Added        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Provider Review     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Signed              │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Encounter Complete  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Ready for Coding    │
└─────────────────────┘
```

---

**Next Module:** [Module 8: Charge Capture](Flows_Module_08_Charge_Capture.md)
