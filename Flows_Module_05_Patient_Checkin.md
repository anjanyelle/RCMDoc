# Module 5: Patient Check-in - Flow Documentation

**Version:** 1.0  
**Module ID:** MOD-005  
**Category:** Patient Management

---

## 1. Module Overview

**Purpose:** Check-in patients when they arrive for appointments, verify information, collect copay.

**Why Hospitals Use It:** Streamline patient flow, update information, collect payments upfront.

**Main Users:** Front Desk Staff, Patients (self-check-in kiosk)

---

## 2. Actors Involved

```
┌─────────────────────────────────────────────────┐
│ ACTORS IN PATIENT CHECK-IN MODULE               │
├─────────────────────────────────────────────────┤
│                                                  │
│ 1. Front Desk Staff                             │
│    - Checks in patients                          │
│    - Verifies information                        │
│    - Collects copay                              │
│                                                  │
│ 2. Patient                                       │
│    - Provides updated information                │
│    - Signs consent forms                         │
│    - Makes copay payment                         │
│                                                  │
│ 3. System                                        │
│    - Check-in Engine                             │
│    - Payment Processor                           │
│    - Queue Management                            │
│                                                  │
│ 4. External APIs                                 │
│    - Stripe (Payment processing)                 │
│    - Twilio (Notify doctor of patient arrival)   │
│    - E-signature API (DocuSign)                  │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 3. Step-by-Step Workflow

```
┌─────────────────────┐
│ Patient Arrives     │
│ at Front Desk       │
└──────────┬──────────┘
           ↓
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌─────────┐  ┌─────────────────┐
│ Staff   │  │ Self-Service    │
│ Check-in│  │ Kiosk           │
└────┬────┘  └────────┬────────┘
     │                │
     │                ▼
     │       ┌─────────────────┐
     │       │ Patient Scans   │
     │       │ QR Code or      │
     │       │ Enters Phone    │
     │       └────────┬────────┘
     │                │
     │                ▼
     │       ┌─────────────────┐
     │       │ System Finds    │
     │       │ Appointment     │
     │       └────────┬────────┘
     │                │
     └────────┬───────┘
              ↓
     ┌─────────────────┐
     │ Staff Opens     │
     │ Check-in Screen │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Search Patient  │
     │ by Name/Phone   │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Load Today's    │
     │ Appointments    │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Display:        │
     │ - Patient: John │
     │ - Doctor: Dr.Lee│
     │ - Time: 10:30 AM│
     │ - Type: Follow-up│
     │ - Copay: $25    │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Verify Patient  │
     │ Information:    │
     │ - Address       │
     │ - Phone         │
     │ - Insurance     │
     │ - Emergency     │
     │   Contact       │
     └────┬────────────┘
          ↓
    ╱ ╲
   ╱   ╲
  ╱Info  ╲───No──────┐
  ╲Correct?╱         │
   ╲     ╱           │
    ╲   ╱            │
     │Yes            │
     │               ▼
     │         ┌─────────────────┐
     │         │ Update Patient  │
     │         │ Information     │
     │         └────┬────────────┘
     │              │
     └──────┬───────┘
            ↓
     ┌─────────────────┐
     │ Check Insurance │
     │ Verification    │
     └────┬────────────┘
          ↓
    ╱ ╲
   ╱   ╲
  ╱Verif?╲───No──────┐
  ╲ied? ╱            │
   ╲   ╱             │
    ╲ ╱              │
     │Yes            │
     │               ▼
     │         ┌─────────────────┐
     │         │ Show Warning:   │
     │         │ "Insurance not  │
     │         │  verified"      │
     │         └────┬────────────┘
     │              │
     │              ▼
     │         ┌─────────────────┐
     │         │ Options:        │
     │         │ 1. Verify Now   │
     │         │ 2. Self-Pay     │
     │         │ 3. Continue     │
     │         └────┬────────────┘
     │              │
     └──────┬───────┘
            ↓
     ┌─────────────────┐
     │ Display Consent │
     │ Forms:          │
     │ - HIPAA         │
     │ - Treatment     │
     │ - Financial     │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Patient Signs   │
     │ (Tablet/Paper)  │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Save Signatures │
     │ to Database     │
     └────┬────────────┘
          ↓
    ╱ ╲
   ╱   ╲
  ╱Copay ╲───No──────┐
  ╲Due?  ╱           │
   ╲    ╱            │
    ╲  ╱             │
     │Yes            │
     │               │
     ▼               │
┌─────────────────┐  │
│ Display Copay   │  │
│ Amount: $25     │  │
└────┬────────────┘  │
     │               │
     ▼               │
┌─────────────────┐  │
│ Payment Method: │  │
│ - Cash          │  │
│ - Card          │  │
│ - Check         │  │
└────┬────────────┘  │
     │               │
     ▼               │
    ╱ ╲              │
   ╱   ╲             │
  ╱Card?╲───Yes──┐   │
  ╲     ╱        │   │
   ╲   ╱         │   │
    ╲ ╱          │   │
     │No         │   │
     │           ▼   │
     │    ┌─────────────────┐
     │    │ Process via     │
     │    │ Stripe          │
     │    └────┬────────────┘
     │         │            │
     │         ▼            │
     │    ┌─────────────────┐
     │    │ Payment Success?│
     │    └────┬────────────┘
     │         │            │
     │    ╱────┴────╲       │
     │   ╱          ╲      │
     │  ╱  Success?  ╲─No──┤
     │  ╲            ╱     │
     │   ╲          ╱      │
     │    ╲────┬───╱       │
     │         │Yes        │
     │         │           │
     ▼         │           │
┌─────────────────┐        │
│ Record Cash     │        │
│ Payment         │        │
└────┬────────────┘        │
     │         │           │
     └────┬────┘           │
          │                │
          ▼                │
     ┌─────────────────┐   │
     │ Print Receipt   │   │
     └────┬────────────┘   │
          │                │
          └────────┬───────┘
                   ↓
          ┌─────────────────┐
          │ Mark as         │
          │ "Checked In"    │
          └────┬────────────┘
               ↓
          ┌─────────────────┐
          │ Add to Waiting  │
          │ Queue           │
          └────┬────────────┘
               ↓
          ┌─────────────────┐
          │ Send SMS to     │
          │ Doctor:         │
          │ "Patient John   │
          │  checked in"    │
          └────┬────────────┘
               ↓
          ┌─────────────────┐
          │ Update Dashboard│
          │ - Waiting: 3    │
          │ - In Room: 2    │
          └────┬────────────┘
               ↓
          ┌─────────────────┐
          │ Give Patient    │
          │ Queue Number    │
          │ "You're #3"     │
          └────┬────────────┘
               ↓
          ┌─────────────────┐
          │ Patient Waits   │
          │ in Waiting Room │
          └─────────────────┘
```

---

## 4. Self-Service Kiosk Flow

```
┌─────────────────────┐
│ Patient Approaches  │
│ Kiosk               │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Welcome Screen:     │
│ "Check in for your  │
│  appointment"       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Options:            │
│ 1. Scan QR Code     │
│ 2. Enter Phone      │
│ 3. Enter DOB        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Patient Enters      │
│ Phone: 555-123-4567 │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ System Searches     │
│ Appointments        │
└──────────┬──────────┘
           ↓
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌─────────┐  ┌─────────────────┐
│ Found   │  │ Not Found       │
└────┬────┘  └────────┬────────┘
     │                │
     │                ▼
     │       ┌─────────────────┐
     │       │ "No appointment │
     │       │  found. Please  │
     │       │  see front desk"│
     │       └─────────────────┘
     │
     ▼
┌─────────────────────┐
│ Display:            │
│ "John Smith         │
│  Dr. Lee            │
│  10:30 AM"          │
│                     │
│ Is this you?        │
│ [Yes] [No]          │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Verify Address:     │
│ "123 Main St"       │
│ [Correct] [Update]  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Sign Consent Forms  │
│ (Touch screen)      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Copay Due: $25      │
│ [Pay Now] [Pay Later]│
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Insert Card         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Processing...       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ ✅ Payment Successful│
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Print Receipt       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ "You're checked in! │
│  Queue #3           │
│  Please wait"       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Return to Home      │
└─────────────────────┘
```

---

## 5. Use Case Diagram

```
┌──────────────┐                          ┌──────────────────┐
│ Front Desk   │─────────────────────────>│ Check In Patient │
│ Staff        │                          └──────────────────┘
└──────┬───────┘                                   │
       │                                  ┌────────┴────────┐
       │                                  │                 │
       │                                  ▼                 ▼
       │                          ┌──────────────┐  ┌──────────────┐
       │                          │ Verify Info  │  │ Collect Copay│
       │                          └──────────────┘  └──────────────┘
       │
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Update Patient   │
                                          │ Information      │
                                          └──────────────────┘

┌──────────────┐                          ┌──────────────────┐
│ Patient      │─────────────────────────>│ Self Check-in    │
│              │                          │ (Kiosk)          │
└──────┬───────┘                          └──────────────────┘
       │
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Sign Consent     │
                                          │ Forms            │
                                          └──────────────────┘

┌──────────────┐                          ┌──────────────────┐
│ System       │─────────────────────────>│ Add to Queue     │
│              │                          └──────────────────┘
└──────┬───────┘
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Notify Doctor    │
                                          └──────────────────┘

┌──────────────┐                          ┌──────────────────┐
│ Stripe API   │─────────────────────────>│ Process Payment  │
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
│ Search Patient      │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Load Appointment    │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Display Patient Info│
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Verify Address      │
│ Phone, Insurance    │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Need  ╲───Yes──────┐
  ╲Update?╱           │
   ╲    ╱             │
    ╲  ╱              │
     │No              │
     │                ▼
     │         ┌─────────────────┐
     │         │ Update Fields   │
     │         └────┬────────────┘
     │              │
     └──────┬───────┘
            ↓
     ┌─────────────────┐
     │ Check Insurance │
     │ Verification    │
     └────┬────────────┘
          ↓
    ╱ ╲
   ╱   ╲
  ╱Verif?╲───No──────┐
  ╲ied? ╱            │
   ╲   ╱             │
    ╲ ╱              │
     │Yes            │
     │               ▼
     │         ┌─────────────────┐
     │         │ Verify Now or   │
     │         │ Continue        │
     │         └────┬────────────┘
     │              │
     └──────┬───────┘
            ↓
     ┌─────────────────┐
     │ Display Consent │
     │ Forms           │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Patient Signs   │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Save Signatures │
     └────┬────────────┘
          ↓
    ╱ ╲
   ╱   ╲
  ╱Copay ╲───No──────┐
  ╲Due?  ╱           │
   ╲    ╱            │
    ╲  ╱             │
     │Yes            │
     │               │
     ▼               │
┌─────────────────┐  │
│ Collect Payment │  │
└────┬────────────┘  │
     │               │
     ▼               │
┌─────────────────┐  │
│ Process via     │  │
│ Stripe          │  │
└────┬────────────┘  │
     │               │
     ▼               │
    ╱ ╲              │
   ╱   ╲             │
  ╱Success?╲─No──┐   │
  ╲       ╱      │   │
   ╲     ╱       │   │
    ╲   ╱        │   │
     │Yes        │   │
     │           ▼   │
     │    ┌─────────────────┐
     │    │ Retry or Skip   │
     │    └────┬────────────┘
     │         │            │
     └────┬────┘            │
          │                 │
          ▼◄────────────────┘
     ┌─────────────────┐
     │ Print Receipt   │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Mark Checked In │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Add to Queue    │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Notify Doctor   │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Give Queue #    │
     └────┬────────────┘
          ↓
     ┌─────────┐
     │   END   │
     └─────────┘
```

---

## 7. Sequence Diagram

```
Staff    Frontend    Backend    Database    Stripe    Twilio
  │          │          │          │          │          │
  │ Check In │          │          │          │          │
  ├─────────>│          │          │          │          │
  │          │          │          │          │          │
  │          │ POST /checkin       │          │          │
  │          ├─────────>│          │          │          │
  │          │          │          │          │          │
  │          │          │ Load     │          │          │
  │          │          │ Appointment         │          │
  │          │          ├─────────>│          │          │
  │          │          │          │          │          │
  │          │          │ Update   │          │          │
  │          │          │ Status   │          │          │
  │          │          ├─────────>│          │          │
  │          │          │          │          │          │
  │          │ Copay Due│          │          │          │
  │          │<─────────┤          │          │          │
  │          │          │          │          │          │
  │ Enter    │          │          │          │          │
  │ Card     │          │          │          │          │
  ├─────────>│          │          │          │          │
  │          │          │          │          │          │
  │          │ POST /payment       │          │          │
  │          ├─────────>│          │          │          │
  │          │          │          │          │          │
  │          │          │ Create   │          │          │
  │          │          │ Charge   │          │          │
  │          │          ├──────────────────>│          │
  │          │          │          │          │          │
  │          │          │          │ Payment  │          │
  │          │          │          │ Success  │          │
  │          │          │<──────────────────┤          │
  │          │          │          │          │          │
  │          │          │ Save     │          │          │
  │          │          │ Payment  │          │          │
  │          │          ├─────────>│          │          │
  │          │          │          │          │          │
  │          │          │ Notify   │          │          │
  │          │          │ Doctor   │          │          │
  │          │          ├───────────────────────────────>│
  │          │          │          │          │          │
  │          │ Success  │          │          │          │
  │          │<─────────┤          │          │          │
  │          │          │          │          │          │
  │ Print    │          │          │          │          │
  │ Receipt  │          │          │          │          │
  │<─────────┤          │          │          │          │
  │          │          │          │          │          │
```

---

## 8. API Flow

**Request:**
```http
POST /api/checkin
{
  "appointmentId": "APT-00001",
  "updatedInfo": {
    "phone": "(555) 123-4567",
    "address": "123 Main St"
  },
  "consentSigned": true,
  "copayAmount": 25,
  "paymentMethod": "card"
}
```

**Response:**
```json
{
  "checkinId": "CHK-00001",
  "queueNumber": 3,
  "estimatedWaitTime": "15 minutes",
  "receiptUrl": "https://..."
}
```

---

## 9. Database Flow

```sql
-- Update appointment status
UPDATE appointments
SET status = 'checked_in',
    checkin_time = NOW(),
    queue_number = 3
WHERE appointment_id = 'APT-00001';

-- Record copay payment
INSERT INTO payments (
    payment_id,
    patient_id,
    appointment_id,
    amount,
    payment_method,
    stripe_charge_id,
    status
) VALUES (
    'PAY-00001',
    'PAT-00001',
    'APT-00001',
    25.00,
    'card',
    'ch_1234567890',
    'completed'
);

-- Add to queue
INSERT INTO waiting_queue (
    queue_id,
    appointment_id,
    queue_number,
    status,
    added_at
) VALUES (
    'Q-00001',
    'APT-00001',
    3,
    'waiting',
    NOW()
);
```

---

## 10. Error Scenarios

```
Error 1: Payment Failed
   ↓
Show error message
   ↓
Options:
1. Retry payment
2. Try different card
3. Pay later (mark as pending)

Error 2: No Appointment Found
   ↓
Show error
   ↓
Options:
1. Search manually
2. Walk-in registration

Error 3: Already Checked In
   ↓
Show message
   ↓
Display queue number
```

---

## 11. Dashboard & Status Flow

```
┌─────────────────────┐
│ Appointment         │
│ Scheduled           │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Patient Checked In  │
│ Queue #3            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Waiting in Queue    │
│ (15 min wait)       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Called to Room      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ In Consultation     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Consultation        │
│ Complete            │
└─────────────────────┘
```

---

**Next Module:** [Module 6: Medical Coding (AI-Assisted)](Flows_Module_06_Medical_Coding.md)
