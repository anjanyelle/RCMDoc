# Module: Encounter Creation - Flow Documentation

**Version:** 1.0
**Module ID:** MOD-005
**Category:** Clinical & Documentation

---

## 1. Module Overview

**Purpose:** Create a clinical encounter when the patient meets the doctor, capture visit details, diagnosis, procedures, orders, and prepare the encounter for documentation, coding, and billing.

---

## 2. Actors Involved

```
┌─────────────────────────────────────────────────┐
│ ACTORS IN ENCOUNTER CREATION MODULE             │
├─────────────────────────────────────────────────┤
│                                                 │
│ 1. Doctor / Provider                            │
│    - Starts patient encounter                   │
│    - Adds diagnosis and procedures              │
│    - Writes clinical notes                      │
│                                                 │
│ 2. Nurse / Medical Assistant                    │
│    - Captures vitals                            │
│    - Adds chief complaint                       │
│    - Updates triage notes                       │
│                                                 │
│ 3. Patient                                      │
│    - Explains symptoms                          │
│    - Provides medical history                   │
│                                                 │
│ 4. Front Desk Staff                             │
│    - Completes check-in                         │
│    - Sends patient to queue                     │
│                                                 │
│ 5. System                                       │
│    - Encounter Engine                           │
│    - Visit Status Tracker                       │
│    - Documentation Service                      │
│    - Audit Log Service                          │
│                                                 │
│ 6. External APIs                                │
│    - EHR / EMR API                              │
│    - Lab API                                    │
│    - Radiology API                              │
│    - Pharmacy API                               │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 3. Step-by-Step Workflow

```
┌─────────────────────┐
│ Patient Checked In  │
│ Queue Assigned      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Nurse Opens Patient │
│ from Queue          │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Capture Vitals      │
│ BP / Temp / Pulse   │
│ Weight / Height     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Add Chief Complaint │
│ Example: Chest Pain │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Doctor Opens Visit  │
│ Starts Encounter    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ System Creates      │
│ Encounter ID        │
│ ENC-00001           │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Load Patient Data   │
│ History / Allergies │
│ Insurance / Orders  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Doctor Documents    │
│ Symptoms & Findings │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Add Diagnosis       │
│ ICD Suggestions     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Add Procedures      │
│ CPT Suggestions     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Create Orders       │
│ Lab / Radiology / Rx │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Save Encounter      │
│ Status: In Progress │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Doctor Completes    │
│ Documentation       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Validate Encounter  │
│ Required Fields     │
└──────────┬──────────┘
           ↓
    ╱ ╲
   ╱   ╲
  ╱Valid?╲───No──────────┐
  ╲      ╱               │
   ╲    ╱                │
    ╲  ╱                 │
     │Yes                ▼
     │            ┌─────────────────┐
     │            │ Show Missing    │
     │            │ Fields to Doctor│
     │            └─────────────────┘
     │
     ▼
┌─────────────────────┐
│ Sign Encounter      │
│ Provider Signature  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Status: Encounter   │
│ Complete            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Move to Medical     │
│ Coding Queue        │
└─────────────────────┘
```

---

## 4. Encounter Rules Engine Flow

```
┌─────────────────────┐
│ Encounter Data      │
│ Input               │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Validate Visit      │
│ - Patient checked in│
│ - Provider assigned │
│ - Visit type valid  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Validate Clinical   │
│ Documentation       │
│ - Chief complaint   │
│ - Diagnosis         │
│ - Assessment        │
│ - Plan              │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Validate Orders     │
│ - Lab orders        │
│ - Radiology orders  │
│ - Medication orders │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Validate Billing    │
│ Readiness           │
│ - Diagnosis present │
│ - Procedure present │
│ - Provider signed   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Return Status       │
│ Complete / Missing  │
└─────────────────────┘
```

---

## 5. Use Case Diagram

```
┌──────────────┐                          ┌──────────────────┐
│ Doctor /     │─────────────────────────>│ Start Encounter  │
│ Provider     │                          └──────────────────┘
└──────┬───────┘
       │                                  ┌──────────────────┐
       ├─────────────────────────────────>│ Add Diagnosis    │
       │                                  └──────────────────┘
       │                                  ┌──────────────────┐
       ├─────────────────────────────────>│ Add Procedures   │
       │                                  └──────────────────┘
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Sign Encounter   │
                                          └──────────────────┘

┌──────────────┐                          ┌──────────────────┐
│ Nurse / MA   │─────────────────────────>│ Capture Vitals   │
└──────┬───────┘                          └──────────────────┘
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Add Triage Notes │
                                          └──────────────────┘

┌──────────────┐                          ┌──────────────────┐
│ System       │─────────────────────────>│ Create Encounter │
└──────┬───────┘                          └──────────────────┘
       │                                  ┌──────────────────┐
       ├─────────────────────────────────>│ Validate Fields  │
       │                                  └──────────────────┘
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Move to Coding   │
                                          └──────────────────┘
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
│ Load Checked-In     │
│ Patient             │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Start Encounter     │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Generate Encounter  │
│ ID                  │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Capture Vitals      │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Add Chief Complaint │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Add Clinical Notes  │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Add Diagnosis /     │
│ Procedures          │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Add Orders          │
│ Lab / Rad / Rx      │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Validate Encounter  │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Valid?╲───No────────┐
  ╲      ╱             │
   ╲    ╱              │
    ╲  ╱               │
     │Yes              ▼
     │          ┌─────────────────┐
     │          │ Fix Missing     │
     │          │ Fields          │
     │          └────┬────────────┘
     │               │
     └───────────────┘
     │
     ▼
┌─────────────────────┐
│ Provider Signs      │
│ Encounter           │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Save to Database    │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Update Status       │
│ Encounter Complete  │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Send to Medical     │
│ Coding Queue        │
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
Doctor    Nurse     Frontend    Backend    Database
  │         │          │          │          │
  │         │ Open     │          │          │
  │         │ Patient  │          │          │
  │         ├─────────>│          │          │
  │         │          │ GET /patient        │
  │         │          ├─────────>│          │
  │         │          │          │ Load Patient Data
  │         │          │          ├─────────>│
  │         │          │ Patient Data        │
  │         │          │<─────────┤          │
  │ Capture │          │          │          │
  │ Vitals  │          │          │          │
  │<────────┤          │          │          │
  │         │ POST /vitals        │          │
  │         ├─────────>│          │          │
  │         │          ├─────────>│          │
  │         │          │          │ Save Vitals
  │         │          │          ├─────────>│
  │ Start   │          │          │          │
  │ Encounter          │          │          │
  ├─────────>│          │          │          │
  │          │ POST /encounter    │          │
  │          ├─────────>│          │          │
  │          │          │ Create Encounter
  │          │          ├─────────>│          │
  │          │          │ Encounter Created
  │          │<─────────┤          │
  │ Add Notes          │          │          │
  ├─────────>│          │          │          │
  │          │ PUT /encounter     │          │
  │          ├─────────>│          │          │
  │          │          │ Save Notes
  │          │          ├─────────>│          │
  │ Add Dx / CPT       │          │          │
  ├─────────>│          │          │          │
  │          │ PUT /diagnosis     │          │
  │          ├─────────>│          │          │
  │          │          │ Save Dx / CPT
  │          │          ├─────────>│          │
  │ Sign     │          │          │          │
  │ Encounter          │          │          │
  ├─────────>│          │          │          │
  │          │ POST /sign         │          │
  │          ├─────────>│          │          │
  │          │          │ Validate Encounter
  │          │          │ Update Complete
  │          │          ├─────────>│          │
  │ Success  │          │          │          │
  │<─────────┤          │          │          │
```

---

## 8. API Flow

**Request:**

```http
POST /api/encounters
{
  "patientId": "PAT-00001",
  "appointmentId": "APT-00001",
  "providerId": "PROV-00001",
  "visitType": "Office Visit",
  "chiefComplaint": "Chest pain",
  "vitals": {
    "bp": "120/80",
    "temperature": "98.6",
    "pulse": 82,
    "weight": 72
  }
}
```

**Response:**

```json
{
  "encounterId": "ENC-00001",
  "status": "IN_PROGRESS",
  "patientId": "PAT-00001",
  "providerId": "PROV-00001",
  "message": "Encounter created successfully"
}
```

---

## 9. Database Flow

```sql
-- Create encounter
INSERT INTO encounters (
    encounter_id,
    patient_id,
    appointment_id,
    provider_id,
    visit_type,
    chief_complaint,
    status
) VALUES (
    'ENC-00001',
    'PAT-00001',
    'APT-00001',
    'PROV-00001',
    'Office Visit',
    'Chest pain',
    'IN_PROGRESS'
);

-- Save vitals
INSERT INTO encounter_vitals (
    encounter_id,
    blood_pressure,
    temperature,
    pulse,
    weight
) VALUES (
    'ENC-00001',
    '120/80',
    '98.6',
    82,
    72
);

-- Save documentation
INSERT INTO encounter_notes (
    encounter_id,
    note_type,
    note_text,
    created_by
) VALUES (
    'ENC-00001',
    'SOAP',
    'Patient presents with chest pain...',
    'PROV-00001'
);
```

---

## 10. Error Scenarios

```
Error 1: Patient Not Checked In
   ↓
Show error
   ↓
Cannot create encounter

Error 2: Provider Not Assigned
   ↓
Show error
   ↓
Assign provider before encounter

Error 3: Missing Clinical Notes
   ↓
Show warning
   ↓
Doctor completes notes

Error 4: Encounter Already Exists
   ↓
Open existing encounter
   ↓
Prevent duplicate encounter
```

---

## 11. Dashboard & Status Flow

```
┌─────────────────────┐
│ Patient Checked In  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Vitals Captured     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Encounter In        │
│ Progress            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Documentation       │
│ Pending             │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Provider Signed     │
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

**Next Module:** [Module 15: Medical Coding](Flows_Module_15_Medical_Coding.md)
