# Module 4: Appointment Scheduling - Flow Documentation

**Version:** 1.0  
**Module ID:** MOD-004  
**Category:** Patient Management

---

## 1. Module Overview

**Purpose:** Schedule patient appointments with doctors, manage calendar, send reminders.

**Why Hospitals Use It:** Optimize doctor schedules, reduce no-shows, improve patient experience.

**Business Goal:** Reduce no-shows, improve doctor schedule utilization, avoid double-booking, and improve patient appointment experience.

**Main Users:** Front Desk Staff, Patients (via portal), Scheduling Team

---

## 2. Actors Involved

```
┌─────────────────────────────────────────────────┐
│ ACTORS IN APPOINTMENT SCHEDULING MODULE         │
├─────────────────────────────────────────────────┤
│                                                  │
│ 1. Front Desk Staff                             │
│    - Books appointments                          │
│    - Reschedules appointments                    │
│    - Cancels appointments                        │
│                                                  │
│ 2. Patient                                       │
│    - Requests appointment                        │
│    - Receives confirmation                       │
│    - Receives reminders                          │
│                                                  │
│ 3. Doctor                                        │
│    - Views schedule                              │
│    - Blocks time slots                           │
│                                                  │
│ 4. System                                        │
│    - Calendar Engine                             │
│    - Reminder Service                            │
│    - Database                                    │
│                                                  │
│ 5. External APIs                                 │
│    - Twilio (SMS reminders)                      │
│    - SendGrid (Email reminders)                  │
│    - Google Calendar (Optional sync)             │
│                                                  │
│ 6. Scheduling Team / Call Center                 │
│    - Handles phone appointment requests          │
│    - Manages reschedule/cancellation requests    │
│    - Helps patients find doctors/time slots      │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 3. Step-by-Step Workflow

```
┌─────────────────────┐
│ Patient Calls or    │
│ Walks In            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Staff Opens         │
│ Appointment Screen  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Search for Patient  │
│ by Name/ID/Phone    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Load Patient Profile│
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Select:             │
│ - Department        │
│ - Doctor (Optional) │
│ - Visit Type        │
│ - Visit Reason      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ System Shows        │
│ Available Slots     │
│ (Next 30 days)      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Calendar View:      │
│                     │
│ May 20 (Mon)        │
│ ✅ 9:00 AM          │
│ ✅ 9:30 AM          │
│ ❌ 10:00 AM (Booked)│
│ ✅ 10:30 AM         │
│ ✅ 11:00 AM         │
│                     │
│ May 21 (Tue)        │
│ ✅ 9:00 AM          │
│ ❌ 9:30 AM (Blocked)│
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Staff Selects Slot  │
│ Example: May 20,    │
│ 10:30 AM            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Check Insurance     │
│ Verification Status │
└──────────┬──────────┘
           ↓
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌─────────┐  ┌─────────────────┐
│Verified │  │ Not Verified    │
└────┬────┘  └────────┬────────┘
     │                │
     │                ▼
     │       ┌─────────────────┐
     │       │ Show Warning:   │
     │       │ "Insurance not  │
     │       │  verified"      │
     │       └────────┬────────┘
     │                │
     │                ▼
     │       ┌─────────────────┐
     │       │ Options:        │
     │       │ 1. Verify Now   │
     │       │ 2. Self-Pay     │
     │       │ 3. Continue     │
     │       └────────┬────────┘
     │                │
     └────────┬───────┘
              ↓
     ┌─────────────────┐
     │ Enter Notes     │
     │ (Optional)      │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Review:         │
     │ - Patient: John │
     │ - Doctor: Dr.Lee│
     │ - Date: May 20  │
     │ - Time: 10:30 AM│
     │ - Type: Follow-up│
     │ - Copay: $25    │
     └────┬────────────┘
          ↓
      ┌─────────────────┐
      │ Click "Confirm" │
      └────┬────────────┘
           ↓
      ┌─────────────────┐
      │ Backend Runs    │
      │ Pre-book Checks │
      │ (Avail, Dups,   │
      │  Prior Auth)    │
      └────┬────────────┘
           ├──────────────────────────────┐
     [Pass]│                              │ [Warning/Fail]
           ▼                              ▼
      ┌─────────────────┐          ┌─────────────────┐
      │ Backend Saves   │          │ Show Booking    │
      │ Appointment     │          │ Alert & Warning │
      └────┬────────────┘          └────────┬────────┘
           │                                │
           │                                ▼
           │                       ┌─────────────────┐
           │                       │ Options:        │
           │                       │ 1. Override     │
           │                       │ 2. Cancel/Edit  │
           │                       │ 3. Link to Auth │
           │                       └────────┬────────┘
           │                                │
           ├────────────────────────────────┘
           ↓
      ┌─────────────────┐
      │ Backend Saves   │
      │ Appointment     │
      └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Generate        │
     │ Appointment ID  │
     │ (APT-00001)     │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Send SMS        │
     │ Confirmation    │
     │ (via Twilio)    │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Send Email      │
     │ Confirmation    │
     │ (via SendGrid)  │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Add to Doctor's │
     │ Calendar        │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Show Success:   │
     │ "Appointment    │
     │  confirmed!"    │
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Print           │
     │ Appointment Card│
     └────┬────────────┘
          ↓
     ┌─────────────────┐
     │ Schedule Auto   │
     │ Reminders:      │
     │ - 24 hrs before │
     │ - 2 hrs before  │
     └─────────────────┘
```

---

## 4. Calendar Availability Logic

```
┌─────────────────────┐
│ Get Doctor Schedule │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Load:               │
│ - Working Hours     │
│   (9 AM - 5 PM)     │
│ - Working Days      │
│   (Mon-Fri)         │
│ - Slot Duration     │
│   (30 minutes)      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Generate Time Slots │
│ 9:00, 9:30, 10:00...│
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Check Existing      │
│ Appointments        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Mark Booked Slots   │
│ as Unavailable      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Check Doctor Blocks │
│ (Lunch, Meetings)   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Mark Blocked Slots  │
│ as Unavailable      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Apply Buffer Time   │
│ Between Appts       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Check Overbooking   │
│ Rules (Doc/Dept/    │
│ Visit Type)         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Block Double-Booking│
│ (Unless Authorized) │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Return Available    │
│ Slots Only          │
└─────────────────────┘
```

---

## 5. Use Case Diagram

```
┌──────────────┐                          ┌──────────────────┐
│ Front Desk   │─────────────────────────>│ Book Appointment │
│ Staff        │                          └──────────────────┘
└──────┬───────┘                                   │
       │                                  ┌────────┴────────┐
       │                                  │                 │
       │                                  ▼                 ▼
       │                          ┌──────────────┐  ┌──────────────┐
       │                          │ Check        │  │ Select Time  │
       │                          │ Availability │  │ Slot         │
       │                          └──────────────┘  └──────────────┘
       │
       │                                  ┌──────────────────┐
       ├─────────────────────────────────>│ Reschedule       │
       │                                  │ Appointment      │
       │                                  └──────────────────┘
       │
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Cancel           │
                                          │ Appointment      │
                                          └──────────────────┘

┌──────────────┐                          ┌──────────────────┐
│ Patient      │─────────────────────────>│ Request Appt     │
│              │                          │ from Portal      │
└──────────────┘                          └──────────────────┘
        │                                          │
        │                                 ┌─────────┴─────────┐
        │                                 │                   │
        │                                 ▼                   ▼
        │                         ┌──────────────┐    ┌──────────────┐
        │                         │ Staff        │    │ Auto         │
        │                         │ Approval     │    │ Confirmation │
        │                         └──────────────┘    └──────────────┘
        │
        │                                 ┌──────────────────┐
        └────────────────────────────────>│ Receive          │
                                          │ Confirmation     │
                                          └──────────────────┘
                                                   │
                                          ┌────────┴────────┐
                                          │                 │
                                          ▼                 ▼
                                  ┌──────────────┐  ┌──────────────┐
                                  │ SMS Reminder │  │Email Reminder│
                                  └──────────────┘  └──────────────┘

┌──────────────┐                          ┌──────────────────┐
│ Doctor       │─────────────────────────>│ View Schedule    │
│              │                          └──────────────────┘
└──────┬───────┘
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Block Time Slots │
                                          └──────────────────┘

┌──────────────┐                          ┌──────────────────┐
│ System       │─────────────────────────>│ Send Auto        │
│              │                          │ Reminders        │
└──────────────┘                          └──────────────────┘
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
│ Select Patient      │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Action╲───Reschedule───>┌─────────────────────┐
  ╲ Type ╱                 │ Select New Slot &   │
   ╲   ╱                   │ Confirm booking.    │
    │New                   │ Then release old    │
    │                      │ slot in database.   │
    │                      └──────────┬──────────┘
    ├────────Cancel───────>┌──────────▼──────────┐
    │                      │ Capture Cancellation│
    │                      │ Reason              │
    │                      └──────────┬──────────┘
    │                                 │
    │                                 ▼
    │                      ┌─────────────────────┐
    │                      │ Release Slot &      │
    │                      │ Update Status to    │
    │                      │ 'Cancelled'         │
    │                      └──────────┬──────────┘
    │                                 │
    │                                 ▼
    │                             ┌───────┐
    │                             │  END  │
    │                             └───────┘
    ▼
┌─────────────────────┐
│ Select Department   │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Select Doctor       │
│ (or Any Available)  │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Select Visit Type:  │
│ - New Patient       │
│ - Follow-up         │
│ - Annual Physical   │
│ - Urgent Care       │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Load Calendar       │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Filter Available    │
│ Slots               │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Display Calendar    │
│ with Green/Red Dots │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ User Selects Slot   │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Slot  ╲───No──────┐
  ╲Avail?╱           │
   ╲able?╱            │
    ╲  ╱              │
     │Yes             │
     │                ▼
     │         ┌─────────────────┐
     │         │ Show Error:     │
     │         │ "Slot just      │
     │         │  booked"        │
     │         └────┬────────────┘
     │              │
     │              └─────────────┐
     │                            │
     ▼                            │
┌─────────────────────┐          │
│ Check Insurance     │          │
└────┬────────────────┘          │
     │                            │
     ▼                            │
    ╱ ╲                           │
   ╱   ╲                          │
  ╱Verif?╲───No──────┐            │
  ╲ied? ╱            │            │
   ╲   ╱             │            │
    ╲ ╱              │            │
     │Yes            │            │
     │               ▼            │
     │         ┌─────────────────┐│
     │         │ Show Warning    ││
     │         │ Continue anyway?││
     │         └────┬────────────┘│
     │              │             │
     │              │             │
     └──────┬───────┘             │
            ↓                     │
     ┌─────────────────┐          │
     │ Enter Notes     │          │
     └────┬────────────┘          │
          ↓                       │
     ┌─────────────────┐          │
     │ Review Details  │          │
     └────┬────────────┘          │
          ↓                       │
     ┌─────────────────┐          │
     │ Click Confirm   │          │
     └────┬────────────┘          │
          ↓                       │
     ┌─────────────────┐          │
     │ Save to Database│          │
     └────┬────────────┘          │
          ↓                       │
     ┌─────────────────┐          │
     │ Generate APT-ID │          │
     └────┬────────────┘          │
          ↓                       │
     ┌─────────────────┐          │
     │ Send SMS        │          │
     └────┬────────────┘          │
          ↓                       │
     ┌─────────────────┐          │
     │ Send Email      │          │
     └────┬────────────┘          │
          ↓                       │
     ┌─────────────────┐          │
     │ Schedule        │          │
     │ Reminders       │          │
     └────┬────────────┘          │
          ↓                       │
     ┌─────────────────┐          │
     │ Show Success    │          │
     └────┬────────────┘          │
          ↓◄────────────────────┘
     ┌─────────────────┐
     │ Print Card      │
     └────┬────────────┘
          ↓
     ┌─────────┐
     │   END   │
     └─────────┘
```

---

## 7. Sequence Diagram

```
Staff    Frontend    Backend    Database    Twilio    SendGrid
  │          │          │          │          │          │
  │ Select   │          │          │          │          │
  │ Slot     │          │          │          │          │
  ├─────────>│          │          │          │          │
  │          │          │          │          │          │
  │          │ POST /appointments  │          │          │
  │          ├─────────>│          │          │          │
  │          │          │          │          │          │
  │          │          │ Check    │          │          │
  │          │          │ Availability        │          │
  │          │          ├─────────>│          │          │
  │          │          │          │          │          │
  │          │          │ Available│          │          │
  │          │          │<─────────┤          │          │
  │          │          │          │          │          │
  │          │          │ INSERT   │          │          │
  │          │          │ appointment         │          │
  │          │          ├─────────>│          │          │
  │          │          │ Audit Log    │          │          │
  │          │          │ ├──┐       │          │          │
  │          │          │ │  │       │          │          │
  │          │          │ │<─┘       │          │          │
  │          │          │          │          │          │
  │          │          │ Send SMS │          │          │
  │          │          ├──────────────────>│          │
  │          │          │ SMS Deliv│          │          │
  │          │          │<──────────────────┤          │
  │          │          │ Update   │          │          │
  │          │          ├─────────>│          │          │
  │          │          │          │          │          │
  │          │          │ Send Email          │          │
  │          │          ├───────────────────────────────>│
  │          │          │ Email Deliv                    │
  │          │          │<───────────────────────────────┤
  │          │          │ Update   │          │          │
  │          │          ├─────────>│          │          │
  │          │          │          │          │          │
  │          │ Response │          │          │          │
  │          │<─────────┤          │          │          │
  │          │          │          │          │          │
  │ Success  │          │          │          │          │
  │<─────────┤          │          │          │          │
  │          │          │          │          │          │
```

---

## 8. API Flow

**Request:**
```http
POST /api/appointments
{
  "patientId": "PAT-00001",
  "doctorId": "DOC-001",
  "departmentId": "DEP-005",
  "locationId": "LOC-002",
  "appointmentDate": "2026-05-20",
  "appointmentTime": "10:30",
  "visitType": "Follow-up",
  "visitReason": "Check blood pressure",
  "insuranceVerified": true,
  "priorAuthRequired": false,
  "source": "Portal",
  "notes": "Patient prefers morning slots"
}
```

**Response:**
```json
{
  "appointmentId": "APT-00001",
  "confirmationNumber": "CNF-88990011",
  "status": "confirmed",
  "calendarStatus": "synced",
  "smsStatus": "pending",
  "emailStatus": "sent",
  "confirmationSent": true,
  "reminderScheduled": true
}
```

---

## 9. Database Flow

```sql
-- Check availability
SELECT * FROM appointments
WHERE doctor_id = 'DOC-001'
  AND appointment_date = '2026-05-20'
  AND appointment_time = '10:30';

-- Insert appointment
INSERT INTO appointments (
    appointment_id,
    patient_id,
    doctor_id,
    department_id,
    location_id,
    appointment_date,
    appointment_time,
    visit_type,
    visit_reason,
    status,
    appointment_source,
    insurance_verification_status,
    prior_auth_required,
    cancellation_reason,
    rescheduled_from_appointment_id,
    created_by,
    created_at,
    updated_at
) VALUES (
    'APT-00001',
    'PAT-00001',
    'DOC-001',
    'DEP-005',
    'LOC-002',
    '2026-05-20',
    '10:30',
    'Follow-up',
    'Check blood pressure',
    'confirmed',
    'Portal',
    'verified',
    false,
    NULL,
    NULL,
    'USR-001',
    NOW(),
    NOW()
);

-- Schedule reminders
INSERT INTO scheduled_notifications (
    appointment_id,
    send_at,
    type,
    status
) VALUES
    ('APT-00001', '2026-05-19 10:30', 'sms', 'pending'),
    ('APT-00001', '2026-05-20 08:30', 'sms', 'pending');
```

---

## 10. Error Scenarios

```
Error 1: Slot Already Booked
   ↓
Show error
   ↓
Refresh calendar
   ↓
Select different slot

Error 2: Doctor Not Available
   ↓
Show alternative doctors
   ↓
Or select different date

Error 3: SMS Failed
   ↓
Log error
   ↓
Continue (don't fail booking)
   ↓
Staff informs patient manually

Error 4: Duplicate Appointment Found
   ↓
Show duplicate warning to user
   ↓
Provide options to view existing or override and continue

Error 5: Patient Not Found
   ↓
Redirect to Patient Registration module
   ↓
Register patient and return to scheduling

Error 6: Insurance Not Verified
   ↓
Prompt to run real-time verification (RTE)
   ↓
Or flag as self-pay/pending verification

Error 7: Prior Authorization Required
   ↓
Show prior authorization alert
   ↓
Provide link to Prior Auth module to start request

Error 8: Email Failed
   ↓
Log error and mark emailStatus as 'failed'
   ↓
Retry via queue or notify staff to print confirmation

Error 9: Calendar Sync Failed
   ↓
Queue sync request for background retry
   ↓
Alert administrator if sync remains pending > 1 hour

Error 10: Reminder Job Failed
   ↓
Trigger system alert and log failure reason
   ↓
Retry job run for missed reminders

Error 11: User Not Authorized to Overbook
   ↓
Block double-booking save action
   ↓
Prompt for supervisor override code/credentials
```

---

## 11. Dashboard & Status Flow

```
                     ┌───────────────────────┐
                     │  Requested (Portal)   │
                     └──────────┬────────────┘
                                │
                                ▼
                     ┌───────────────────────┐
                     │ Pending Confirmation  │
                     └──────────┬────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              ▼                                   ▼
  ┌───────────────────────┐           ┌───────────────────────┐
  │  Awaiting Insurance   │           │  Prior Auth Required  │
  └──────────┬────────────┘           └────────┬──────────────┘
             │                                 │
             └─────────────────┬───────────────┘
                               ▼
                     ┌───────────────────────┐
                     │ Confirmed / Booked    │
                     └──────────┬────────────┘
                                │
                       ┌────────┴────────┐
                       ▼                 ▼
             ┌──────────────────┐  ┌───────────┐
             │  Reminder Sent   │  │ Reminder  │
             └────────┬─────────┘  │  Failed   │
                      │            └───────────┘
                      ▼
               ┌──────────────┐
               │ Checked-in   │
               └──────┬───────┘
                      │
         ┌────────────┼──────────────┬──────────────┐
         ▼            ▼              ▼              ▼
   ┌──────────┐   ┌───────────┐  ┌───────────┐  ┌───────────┐
   │    In    │   │  No-Show  │  │ Cancelled │  │Rescheduled│
   │ Progress │   └───────────┘  │by Patient │  └───────────┘
   └────┬─────┘                  ├───────────┤
        │                        │ Cancelled │
        ▼                        │ by Clinic │
   ┌──────────┐                  └───────────┘
   │Completed │
   └──────────┘
```

---

## 12. Reminder System Flow

```
┌─────────────────────┐
│ Cron Job Runs       │
│ Every 15 Minutes    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Query Pending       │
│ Reminders           │
│ WHERE send_at <= NOW│
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ For Each Reminder:  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Load Appointment    │
│ Details             │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Build Message:      │
│ "Hi John, reminder  │
│  for your appt with │
│  Dr. Lee tomorrow   │
│  at 10:30 AM"       │
└──────────┬──────────┘
           ↓
    ╱ ╲
   ╱   ╲
  ╱Patient╲───Yes (Opt-out)──┐
  ╲Opted  ╱                  │
   ╲Out? ╱                   │
    │No                      │
    ▼                        ▼
┌─────────┐          ┌───────────────┐
│ Send to │          │ Mark Status   │
│ Twilio/ │          │ 'Opted-Out'   │
│ SendGrid│          └───────┬───────┘
└────┬────┘                  │
     ├───────────────────────┘
     ▼
    ╱ ╲
   ╱   ╲
  ╱Success?╲───No (Fail)────┐
  ╲       ╱                 │
   ╲     ╱                  │
    │Yes                    ▼
    ▼               ┌───────────────┐
┌─────────┐         │ Trigger Retry │
│ Store   │         │ Policy (Max 3)│
│ Delivery│         └───────┬───────┘
│ Response│                 │
└────┬────┘                 ▼
     │              ┌───────────────┐
     │              │ Save Failure  │
     │              │ Reason & Alert│
     │              └───────┬───────┘
     │                      │
     ├──────────────────────┘
     ▼
┌─────────┐
│ Mark as │
│ Sent/   │
│ Failed  │
└────┬────┘
     ↓
┌─────────────────────┐
│ Log Delivery Status │
└─────────────────────┘
```

---

**Next Module:** [Module 5: Patient Check-in](Flows_Module_05_Patient_Checkin.md)
