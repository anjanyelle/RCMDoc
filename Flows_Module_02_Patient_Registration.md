# Module 2: Patient Registration - Complete Flow Documentation

**Version:** 1.0  
**Module ID:** MOD-002  
**Category:** Patient Management

---

## 1. Module Overview

### Purpose
Capture and store complete patient demographic and insurance information for billing and clinical purposes.

### Why Hospitals Use It
- **Accurate Billing:** Correct patient info ensures claims get paid
- **Insurance Verification:** Need patient details to verify coverage
- **Legal Compliance:** Required for medical records
- **Patient Identification:** Prevent duplicate records and medical errors

### Main Users Involved
- Front Desk Staff (primary user)
- Registration Team
- Admissions Staff

---

## 2. Actors Involved

```
┌─────────────────────────────────────────────────┐
│ ACTORS IN PATIENT REGISTRATION MODULE           │
├─────────────────────────────────────────────────┤
│                                                  │
│ 1. Front Desk Staff                             │
│    - Registers new patients                      │
│    - Updates existing patient info               │
│    - Scans insurance cards                       │
│                                                  │
│ 2. Patient                                       │
│    - Provides personal information               │
│    - Provides insurance cards                    │
│    - Signs consent forms                         │
│                                                  │
│ 3. System                                        │
│    - Database (stores patient data)              │
│    - OCR Service (reads insurance cards)         │
│    - Duplicate Check Service                     │
│                                                  │
│ 4. External APIs                                 │
│    - AWS Textract (OCR for insurance cards)      │
│    - Address Validation API                      │
│    - Availity (insurance verification)           │
│                                                  │
│ 5. Self-Service Kiosk                           │
│    - Patient self check-in                       │
│    - ID scan                                     │
│    - Insurance scan                              │
│    - Digital signature                           │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 2.1 Pre-Registration Workflow

In real hospitals:
* Registration starts before patient arrival
* Appointments trigger pre-registration
* Insurance is partially verified before visit

```
┌──────────────────────────┐
│ Appointment Scheduled    │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Pre-Registration Link    │
│ Sent to Patient          │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Patient Completes        │
│ Demographics             │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Insurance Information    │
│ Uploaded                 │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Consent Forms Signed     │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Eligibility Verification │
│ Triggered                │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Financial Estimate       │
│ Generated                │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Patient Ready for Visit  │
└──────────────────────────┘
```

---

## 3. Step-by-Step Workflow

### Flow Diagram

```
┌─────────────────────┐
│ Patient Arrives at  │
│ Front Desk          │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Staff Opens Patient │
│ Registration Screen │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Check: New or       │
│ Existing Patient?   │
└──────────┬──────────┘
           ↓
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌─────────┐  ┌─────────────────┐
│Existing │  │ New Patient     │
│Patient  │  └────────┬────────┘
└────┬────┘           │
     │                ▼
     │       ┌─────────────────┐
     │       │ Search for      │
     │       │ Duplicate       │
     │       │ (Name, DOB, SSN)│
     │       └────────┬────────┘
     │                ↓
     │         ┌──────┴──────┐
     │         │ Found?      │
     │         └──┬──────┬───┘
     │       No   │      │ Yes
     │            │      │
     │            │      ▼
     │            │  ┌─────────────────┐
     │            │  │ Show Existing   │
     │            │  │ Record - Update?│
     │            │  └────────┬────────┘
     │            │           │
     │            ▼           │
     │   ┌─────────────────┐ │
     │   │ Create New      │ │
     │   │ Patient Record  │ │
     │   └────────┬────────┘ │
     │            │           │
     │            ▼           │
     │   ┌─────────────────┐ │
     │   │ Enter Patient   │ │
     │   │ Demographics:   │ │
     │   │ - First Name    │ │
     │   │ - Last Name     │ │
     │   │ - DOB           │ │
     │   │ - Gender        │ │
     │   │ - SSN           │ │
     │   │ - Address       │ │
     │   │ - Phone         │ │
     │   │ - Email         │ │
     │   └────────┬────────┘ │
     │            │           │
     │            ▼           │
     │   ┌─────────────────┐ │
     │   │ Validate Data   │ │
     │   │ - Required      │ │
     │   │   fields filled │ │
     │   │ - Valid formats │ │
     │   └────────┬────────┘ │
     │            │           │
     │            ▼           │
     │     ┌──────┴──────┐   │
     │     │ Valid?      │   │
     │     └──┬──────┬───┘   │
     │   No   │      │ Yes   │
     │        ↓      │       │
     │   ┌─────────┐│       │
     │   │Show     ││       │
     │   │Errors   ││       │
     │   └────┬────┘│       │
     │        │     │       │
     │        └─────┘       │
     │            │         │
     │            ▼         │
     │   ┌─────────────────┐│
     │   │ Scan Insurance  ││
     │   │ Card (Front &   ││
     │   │ Back)           ││
     │   └────────┬────────┘│
     │            │         │
     │            ▼         │
     │   ┌─────────────────┐│
     │   │ Upload to AWS   ││
     │   │ Textract OCR    ││
     │   └────────┬────────┘│
     │            │         │
     │            ▼         │
     │   ┌─────────────────┐│
     │   │ OCR Extracts:   ││
     │   │ - Member ID     ││
     │   │ - Payer Name    ││
     │   │ - Group Number  ││
     │   │ - Plan Name     ││
     │   └────────┬────────┘│
     │            │         │
     │            ▼         │
     │   ┌─────────────────┐│
     │   │ Auto-fill       ││
     │   │ Insurance Fields││
     │   └────────┬────────┘│
     │            │         │
     │            ▼         │
     │   ┌─────────────────┐│
     │   │ Staff Reviews & ││
     │   │ Corrects OCR    ││
     │   │ Data            ││
     │   └────────┬────────┘│
     │            │         │
     │            ▼         │
     │   ┌─────────────────┐│
     │   │ Enter Insurance ││
     │   │ Details:        ││
     │   │ - Payer Name    ││
     │   │ - Member ID     ││
     │   │ - Group Number  ││
     │   │ - Plan Type     ││
     │   │ - Effective Date││
     │   └────────┬────────┘│
     │            │         │
     │            ▼         │
     │   ┌─────────────────┐│
     │   │ Add Emergency   ││
     │   │ Contact:        ││
     │   │ - Name          ││
     │   │ - Relationship  ││
     │   │ - Phone         ││
     │   └────────┬────────┘│
     │            │         │
     │            ▼         │
     │   ┌─────────────────┐│
     │   │ Add Guarantor   ││
     │   │ (if different   ││
     │   │  from patient)  ││
     │   └────────┬────────┘│
     │            │         │
     │            ▼         │
     │   ┌─────────────────┐│
     │   │ Present Consent ││
     │   │ Forms           ││
     │   └────────┬────────┘│
     │            │         │
     │            ▼         │
     │   ┌─────────────────┐│
     │   │ HIPAA Consent   ││
     │   │ Financial       ││
     │   │ Consent         ││
     │   │ Treatment       ││
     │   │ Consent         ││
     │   └────────┬────────┘│
     │            │         │
     │            ▼         │
     │   ┌─────────────────┐│
     │   │ Capture Digital ││
     │   │ Signature       ││
     │   └────────┬────────┘│
     │            │         │
     │            ▼         │
     │   ┌─────────────────┐│
     │   │ Save Consent PDF││
     │   │ to Document     ││
     │   │ Management      ││
     │   └────────┬────────┘│
     │            │         │
     └────────────┼─────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ Review All Data │
         └────────┬────────┘
                  ↓
         ┌─────────────────┐
         │ Click Save      │
         └────────┬────────┘
                  ↓
         ┌─────────────────┐
         │ Backend Saves   │
         │ to Database     │
         └────────┬────────┘
                  ↓
         ┌─────────────────────────┐
         │ Trigger Real-Time       │
         │ Eligibility Verification│
         └────────┬────────────────┘
                  ↓
         ┌─────────────────────────┐
         │ Verify Active Insurance │
         │ Coverage                │
         └────────┬────────────────┘
                  ↓
         ┌─────────────────────────┐
         │ Store Eligibility       │
         │ Response                │
         └────────┬────────────────┘
                  ↓
         ┌─────────────────────────┐
         │ Calculate Copay         │
         │ Deductible              │
         │ Coinsurance             │
         └────────┬────────────────┘
                  ↓
         ┌─────────────────────────┐
         │ Show Estimated Patient  │
         │ Balance                 │
         └────────┬────────────────┘
                  ↓
         ┌─────────────────┐
         │ Generate Patient│
         │ ID (PAT-00001)  │
         └────────┬────────┘
                  ↓
         ┌─────────────────┐
         │ Send Welcome SMS│
         │ (via Twilio)    │
         └────────┬────────┘
                  ↓
         ┌─────────────────┐
         │ Show Success    │
         │ Message         │
         └────────┬────────┘
                  ↓
         ┌─────────────────┐
         │ Print Patient   │
         │ Wristband       │
         │ (Optional)      │
         └────────┬────────┘
                  ↓
         ┌─────────────────┐
         │ Redirect to     │
         │ Insurance       │
         │ Verification    │
         └─────────────────┘
```

---

## 4. Action Plan

### Frontend Actions

**Technology:** React.js + TypeScript

**File:** `src/pages/PatientRegistration.tsx`

```typescript
// What Frontend Does:

1. Display registration form with sections:
   - Patient Demographics
   - Insurance Information
   - Emergency Contact
   - Guarantor Information

2. Duplicate check on blur:
   - When user enters Last Name + DOB
   - Call GET /api/patients/check-duplicate
   - Show warning if potential duplicate found

3. Insurance card upload:
   - Allow image upload (JPG, PNG)
   - Show preview
   - Send to backend for OCR processing
   - Display extracted data for review

4. Identity verification:
   - Driver license scan
   - Government ID validation
   - Face match (optional)
   - Fraud detection

5. Real-time validation:
   - SSN format: XXX-XX-XXXX
   - Phone format: (XXX) XXX-XXXX
   - Email format: valid email
   - DOB: Must be in past
   - Zip code: 5 digits

6. Address autocomplete:
   - Use Google Places API
   - Auto-fill city, state, zip

7. Save patient:
   - POST /api/patients
   - Show loading spinner
   - Handle success/error

8. Print wristband:
   - Generate PDF with patient info + barcode
   - Send to printer
```

**Code Example:**
```typescript
const PatientRegistration = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    dob: '',
    gender: '',
    ssn: '',
    address: '',
    phone: '',
    email: '',
    insurance: {
      payerName: '',
      memberId: '',
      groupNumber: '',
      planType: ''
    }
  });

  // Duplicate check
  const checkDuplicate = async () => {
    if (formData.lastName && formData.dob) {
      const response = await api.get('/patients/check-duplicate', {
        params: {
          lastName: formData.lastName,
          dob: formData.dob
        }
      });
      
      if (response.data.exists) {
        setShowDuplicateWarning(true);
        setDuplicatePatients(response.data.patients);
      }
    }
  };

  // Handle insurance card upload
  const handleCardUpload = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    
    setOcrLoading(true);
    
    try {
      const response = await api.post('/patients/ocr-insurance-card', formData);
      
      // Auto-fill insurance fields
      setFormData(prev => ({
        ...prev,
        insurance: {
          payerName: response.data.payerName,
          memberId: response.data.memberId,
          groupNumber: response.data.groupNumber,
          planType: response.data.planType
        }
      }));
    } catch (error) {
      toast.error('OCR failed. Please enter manually.');
    } finally {
      setOcrLoading(false);
    }
  };

  // Submit form
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    
    // Validate
    const errors = validateForm(formData);
    if (errors.length > 0) {
      setErrors(errors);
      return;
    }
    
    setLoading(true);
    
    try {
      const response = await api.post('/patients', formData);
      
      toast.success(`Patient registered: ${response.data.patientId}`);
      
      // Redirect to insurance verification
      navigate(`/insurance-verification/${response.data.patientId}`);
    } catch (error) {
      toast.error(error.response?.data?.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
    </form>
  );
};
```

---

### Backend Actions

**Technology:** Python FastAPI

**File:** `app/api/v1/patients.py`

```python
# What Backend Does:

1. Receive patient registration request
   - Validate request format
   - Check required fields

2. Check for duplicates
   - Search by: Last Name + DOB + SSN
   - Use fuzzy matching for names
   - Return potential matches

3. Validate data
   - SSN format and checksum
   - Phone number format
   - Email format
   - DOB is valid date in past
   - Zip code exists

4. Process insurance card OCR
   - Upload image to AWS S3
   - Call AWS Textract
   - Extract text fields
   - Parse insurance data using regex
   - Return structured data

5. Generate Patient ID
   - Format: PAT-{sequential_number}
   - Example: PAT-00001, PAT-00002

6. Save to database
   - Insert into patients table
   - Insert into patient_insurance table
   - Insert into emergency_contacts table
   - Insert into guarantors table (if different)

7. Send welcome notification
   - SMS via Twilio
   - Email with patient portal link

8. Log audit entry
   - Record patient creation
   - Store who created it

9. Advanced audit logging:
   - Before/after values
   - Field-level changes
   - User IP address
   - Device information
   - Record access tracking

10. Return response
    - Patient ID
    - Success message
```

**Code Example:**
```python
@router.post("/patients")
async def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check for duplicates
    existing = db.query(Patient).filter(
        Patient.last_name == patient.lastName,
        Patient.dob == patient.dob
    ).first()
    
    if existing:
        # Check if SSN also matches
        if existing.ssn == patient.ssn:
            raise HTTPException(
                status_code=409,
                detail=f"Patient already exists: {existing.patient_id}"
            )
    
    # Validate SSN
    if not validate_ssn(patient.ssn):
        raise HTTPException(status_code=400, detail="Invalid SSN format")
    
    # Generate Patient ID
    last_patient = db.query(Patient).order_by(
        Patient.patient_id.desc()
    ).first()
    
    if last_patient:
        last_num = int(last_patient.patient_id.split('-')[1])
        new_num = last_num + 1
    else:
        new_num = 1
    
    patient_id = f"PAT-{new_num:05d}"
    
    # Create patient record
    db_patient = Patient(
        patient_id=patient_id,
        first_name=patient.firstName,
        last_name=patient.lastName,
        dob=patient.dob,
        gender=patient.gender,
        ssn=encrypt_ssn(patient.ssn),  # Encrypt SSN
        address=patient.address,
        phone=patient.phone,
        email=patient.email,
        created_by=current_user.user_id
    )
    
    db.add(db_patient)
    
    # Add insurance
    if patient.insurance:
        db_insurance = PatientInsurance(
            patient_id=patient_id,
            payer_name=patient.insurance.payerName,
            member_id=patient.insurance.memberId,
            group_number=patient.insurance.groupNumber,
            plan_type=patient.insurance.planType,
            effective_date=patient.insurance.effectiveDate,
            is_primary=True
        )
        db.add(db_insurance)
    
    # Add emergency contact
    if patient.emergencyContact:
        db_contact = EmergencyContact(
            patient_id=patient_id,
            name=patient.emergencyContact.name,
            relationship=patient.emergencyContact.relationship,
            phone=patient.emergencyContact.phone
        )
        db.add(db_contact)
    
    db.commit()
    
    # Send welcome SMS
    send_welcome_sms(patient.phone, patient.firstName, patient_id)
    
    # Log audit
    log_audit(
        user_id=current_user.user_id,
        action="PATIENT_CREATED",
        details={"patient_id": patient_id}
    )
    
    return {
        "patientId": patient_id,
        "message": "Patient registered successfully"
    }


@router.post("/patients/ocr-insurance-card")
async def ocr_insurance_card(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    # Upload to S3
    s3_key = f"insurance-cards/{uuid.uuid4()}.jpg"
    s3_client.upload_fileobj(file.file, BUCKET_NAME, s3_key)
    
    # Call AWS Textract
    textract = boto3.client('textract')
    response = textract.detect_document_text(
        Document={'S3Object': {'Bucket': BUCKET_NAME, 'Name': s3_key}}
    )
    
    # Extract text
    text_blocks = [block['Text'] for block in response['Blocks'] 
                   if block['BlockType'] == 'LINE']
    
    # Parse insurance data
    insurance_data = parse_insurance_card(text_blocks)
    
    return insurance_data


def parse_insurance_card(text_blocks: List[str]) -> dict:
    """Parse insurance card text using regex patterns"""
    
    data = {
        "payerName": None,
        "memberId": None,
        "groupNumber": None,
        "planType": None
    }
    
    # Common payer names
    payers = ["Aetna", "UnitedHealthcare", "Blue Cross", "Cigna", "Humana"]
    
    for line in text_blocks:
        # Find payer name
        for payer in payers:
            if payer.lower() in line.lower():
                data["payerName"] = payer
        
        # Find Member ID (various patterns)
        if re.search(r'member.*id|id.*number', line, re.I):
            # Next line usually has the ID
            idx = text_blocks.index(line)
            if idx + 1 < len(text_blocks):
                data["memberId"] = text_blocks[idx + 1]
        
        # Find Group Number
        if re.search(r'group.*number|grp', line, re.I):
            match = re.search(r'\d+', line)
            if match:
                data["groupNumber"] = match.group()
    
    return data
```

---

### Database Actions

**Tables Updated:**

1. **patients** - Insert new patient
2. **patient_insurance** - Insert insurance info
3. **emergency_contacts** - Insert emergency contact
4. **guarantors** - Insert guarantor (if different)
5. **audit_logs** - Log patient creation

**SQL Operations:**

```sql
-- 1. Check for duplicates
SELECT patient_id, first_name, last_name, dob, ssn
FROM patients
WHERE last_name = 'Smith' AND dob = '1985-05-15';

-- 2. Insert patient
INSERT INTO patients (
    patient_id, first_name, last_name, dob, gender, ssn,
    address, city, state, zip, phone, email, created_by, created_at
) VALUES (
    'PAT-00001', 'John', 'Smith', '1985-05-15', 'M', 'encrypted_ssn',
    '123 Main St', 'Boston', 'MA', '02101', '(555) 123-4567',
    'john@email.com', 'USR-001', NOW()
);

-- 3. Insert insurance
INSERT INTO patient_insurance (
    insurance_id, patient_id, payer_name, member_id, group_number,
    plan_type, effective_date, is_primary
) VALUES (
    'INS-00001', 'PAT-00001', 'Aetna', 'W123456789', 'GRP12345',
    'PPO', '2026-01-01', TRUE
);

-- 4. Insert emergency contact
INSERT INTO emergency_contacts (
    contact_id, patient_id, name, relationship, phone
) VALUES (
    'EC-00001', 'PAT-00001', 'Jane Smith', 'Spouse', '(555) 987-6543'
);

-- 5. Log audit
INSERT INTO audit_logs (user_id, action, details, timestamp)
VALUES ('USR-001', 'PATIENT_CREATED', '{"patient_id": "PAT-00001"}', NOW());
```

---

### API Calls

**Internal APIs:**
- `POST /api/patients` - Create patient
- `GET /api/patients/check-duplicate` - Check for duplicates
- `POST /api/patients/ocr-insurance-card` - OCR insurance card
- `GET /api/patients/{patientId}` - Get patient details
- `PUT /api/patients/{patientId}` - Update patient

**External APIs:**

1. **AWS Textract** (OCR)
   - Endpoint: `textract.detect_document_text()`
   - Purpose: Extract text from insurance cards
   - Cost: $1.50 per 1,000 pages

2. **Twilio SMS** (Welcome message)
   - Endpoint: `https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json`
   - Purpose: Send welcome SMS
   - Cost: $0.0079 per SMS

3. **Google Places API** (Address autocomplete - Optional)
   - Endpoint: `https://maps.googleapis.com/maps/api/place/autocomplete`
   - Purpose: Validate and autocomplete addresses
   - Cost: $2.83 per 1,000 requests

---

### Validations

**Frontend Validations:**
```javascript
1. First Name:
   - Required
   - Min 2 characters
   - Only letters and spaces

2. Last Name:
   - Required
   - Min 2 characters
   - Only letters and spaces

3. Date of Birth:
   - Required
   - Valid date format (MM/DD/YYYY)
   - Must be in the past
   - Patient must be born (not future date)

4. Gender:
   - Required
   - Options: Male, Female, Other

5. SSN:
   - Required
   - Format: XXX-XX-XXXX
   - 9 digits
   - Valid SSN checksum

6. Phone:
   - Required
   - Format: (XXX) XXX-XXXX
   - 10 digits

7. Email:
   - Optional
   - Valid email format

8. Address:
   - Required
   - Min 5 characters

9. Zip Code:
   - Required
   - 5 digits
   - Valid US zip code

10. Insurance Member ID:
    - Required if insurance added
    - Min 5 characters
```

**Backend Validations:**
```python
1. Duplicate Check:
   - Check Last Name + DOB + SSN
   - Fuzzy match on name (Levenshtein distance)
   - Warn if 80% match

2. SSN Validation:
   - Not all zeros
   - Not sequential (123-45-6789)
   - Valid area number
   - Valid group number

3. Age Validation:
   - Must be >= 0 years old
   - Must be < 150 years old

4. Insurance Validation:
   - Payer must exist in payers table
   - Effective date not in far future

5. Data Sanitization:
   - Remove special characters from names
   - Trim whitespace
   - Capitalize names properly
```

---

### Notifications

**Success Notifications:**

1. **Welcome SMS** (via Twilio)
```
Hi John! Welcome to Boston General Hospital. 
Your Patient ID is PAT-00001. 
Access your portal: https://portal.hospital.com
```

2. **Welcome Email**
```
Subject: Welcome to Boston General Hospital

Dear John Smith,

Thank you for registering with us!

Patient ID: PAT-00001
Portal: https://portal.hospital.com
Username: john@email.com

Please set your password to access your medical records.

Best regards,
Boston General Hospital
```

3. **Portal Activation Email:**
   - Activation link
   - Temporary password
   - MFA enrollment
   - Portal setup instructions

```
┌──────────────────────────┐
│ Patient Registered       │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Portal Account Created   │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Activation Email Sent    │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Patient Sets Password    │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ MFA Enrollment           │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Portal Activated         │
└──────────────────────────┘
```

4. **In-App Success**
```
✅ Patient registered successfully!
Patient ID: PAT-00001
```

---

## 5. Use Case Diagram

```
                    ┌─────────────────────────────────────┐
                    │   PATIENT REGISTRATION SYSTEM       │
                    └─────────────────────────────────────┘

┌──────────────┐                                    ┌──────────────┐
│              │                                    │              │
│ Front Desk   │────────────────────────────────────│ Register New │
│ Staff        │                                    │ Patient      │
└──────┬───────┘                                    └──────────────┘
       │                                                    │
       │                                            ┌───────┴────────┐
       │                                            │                │
       │                                     ┌──────▼──────┐  ┌──────▼──────┐
       │                                     │ Enter       │  │ Scan        │
       │                                     │Demographics │  │Insurance    │
       │                                     └─────────────┘  │Card         │
       │                                                      └─────────────┘
       │                                                    
       │                                            ┌──────────────┐
       ├────────────────────────────────────────────│ Check for    │
       │                                            │ Duplicates   │
       │                                            └──────────────┘
       │                                                    
       │                                            ┌──────────────┐
       ├────────────────────────────────────────────│ Update       │
       │                                            │ Existing     │
       │                                            │ Patient      │
       │                                            └──────────────┘
       │                                                    
       │                                            ┌──────────────┐
       └────────────────────────────────────────────│ Print        │
                                                    │ Wristband    │
                                                    └──────────────┘

┌──────────────┐                                    ┌──────────────┐
│              │                                    │              │
│   System     │────────────────────────────────────│ Validate     │
│              │                                    │ Data         │
└──────┬───────┘                                    └──────────────┘
       │                                                    
       │                                            ┌──────────────┐
       ├────────────────────────────────────────────│ Generate     │
       │                                            │ Patient ID   │
       │                                            └──────────────┘
       │                                                    
       │                                            ┌──────────────┐
       └────────────────────────────────────────────│ Store in     │
                                                    │ Database     │
                                                    └──────────────┘

┌──────────────┐                                    ┌──────────────┐
│              │                                    │              │
│ AWS Textract │────────────────────────────────────│ OCR          │
│              │                                    │ Insurance    │
└──────────────┘                                    │ Card         │
                                                    └──────────────┘

┌──────────────┐                                    ┌──────────────┐
│              │                                    │              │
│ Twilio API   │────────────────────────────────────│ Send Welcome │
│              │                                    │ SMS          │
└──────────────┘                                    └──────────────┘
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
│ Patient Arrives     │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Staff Opens         │
│ Registration Screen │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱ New  ╲────No (Existing)────┐
  ╲Patient?╱                   │
   ╲   ╱                       │
    ╲ ╱                        │
     │Yes                      │
     │                         ▼
     │                  ┌─────────────────────┐
     │                  │ Search for Patient  │
     │                  │ by Name/DOB/MRN     │
     │                  └────┬────────────────┘
     │                       │
     │                       ▼
     │                  ┌─────────────────────┐
     │                  │ Load Patient Record │
     │                  │ Update if needed    │
     │                  └────┬────────────────┘
     │                       │
     │                       └──────────┐
     │                                  │
     ▼                                  │
┌─────────────────────┐                │
│ Enter Last Name     │                │
│ and DOB             │                │
└────┬────────────────┘                │
     │                                  │
     ▼                                  │
┌─────────────────────┐                │
│ Auto Duplicate Check│                │
│ (on blur)           │                │
└────┬────────────────┘                │
     │                                  │
     ▼                                  │
    ╱ ╲                                 │
   ╱   ╲                                │
  ╱Dup  ╲────Yes────┐                  │
  ╲Found?╱          │                  │
   ╲   ╱            │                  │
    ╲ ╱             │                  │
     │No            │                  │
     │              ▼                  │
     │         ┌─────────────────────┐ │
     │         │ Show Warning:       │ │
     │         │ "Similar patient    │ │
     │         │  found. Continue?"  │ │
     │         └────┬────────────────┘ │
     │              │                  │
     │              ▼                  │
     │             ╱ ╲                 │
     │            ╱   ╲                │
     │           ╱Cont?╲───No──────────┤
     │           ╲inue?╱               │
     │            ╲   ╱                │
     │             ╲ ╱                 │
     │              │Yes               │
     │              │                  │
     ▼              │                  │
┌─────────────────────┐               │
│ Fill Demographics:  │               │
│ - First Name        │               │
│ - Middle Name       │               │
│ - Gender            │               │
│ - SSN               │               │
│ - Address           │               │
│ - City, State, Zip  │               │
│ - Phone             │               │
│ - Email             │               │
└────┬────────────────┘               │
     │                                 │
     ▼                                 │
┌─────────────────────┐               │
│ Real-time           │               │
│ Validation          │               │
└────┬────────────────┘               │
     │                                 │
     ▼                                 │
    ╱ ╲                                │
   ╱   ╲                               │
  ╱Valid?╲────No────┐                 │
  ╲     ╱           │                 │
   ╲   ╱            │                 │
    ╲ ╱             │                 │
     │Yes           │                 │
     │              ▼                 │
     │         ┌─────────────────────┐│
     │         │ Show Inline Errors  ││
     │         │ (red highlights)    ││
     │         └────┬────────────────┘│
     │              │                 │
     │              └─────────────────┘
     │                                 │
     ▼                                 │
┌─────────────────────┐               │
│ Upload Insurance    │               │
│ Card Image          │               │
└────┬────────────────┘               │
     │                                 │
     ▼                                 │
┌─────────────────────┐               │
│ Show Loading:       │               │
│ "Processing OCR..." │               │
└────┬────────────────┘               │
     │                                 │
     ▼                                 │
┌─────────────────────┐               │
│ Backend Calls       │               │
│ AWS Textract        │               │
└────┬────────────────┘               │
     │                                 │
     ▼                                 │
┌─────────────────────┐               │
│ OCR Extracts Data   │               │
└────┬────────────────┘               │
     │                                 │
     ▼                                 │
┌─────────────────────┐               │
│ Auto-fill Insurance │               │
│ Fields:             │               │
│ - Payer Name        │               │
│ - Member ID         │               │
│ - Group Number      │               │
└────┬────────────────┘               │
     │                                 │
     ▼                                 │
┌─────────────────────┐               │
│ Staff Reviews &     │               │
│ Corrects OCR Data   │               │
└────┬────────────────┘               │
     │                                 │
     ▼                                 │
┌─────────────────────┐               │
│ Add Emergency       │               │
│ Contact (Optional)  │               │
└────┬────────────────┘               │
     │                                 │
     ▼                                 │
┌─────────────────────┐               │
│ Add Guarantor       │               │
│ (if different)      │               │
└────┬────────────────┘               │
     │                                 │
     ▼                                 │
┌─────────────────────┐               │
│ Present Consent     │               │
│ Forms               │               │
└────┬────────────────┘               │
     │                                 │
     ▼                                 │
┌─────────────────────┐               │
│ HIPAA Consent       │               │
│ Financial Consent   │               │
│ Treatment Consent   │               │
└────┬────────────────┘               │
     │                                 │
     ▼                                 │
┌─────────────────────┐               │
│ Capture Digital     │               │
│ Signature           │               │
└────┬────────────────┘               │
     │                                 │
     ▼                                 │
┌─────────────────────┐               │
│ Save Consent PDF    │               │
│ to Document Mgmt    │               │
└────┬────────────────┘               │
     │                                 │
     ▼◄────────────────────────────────┘
┌─────────────────────┐
│ Review All Data     │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Click "Save Patient"│
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Show Loading        │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Backend Validates   │
│ All Data            │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Valid?╲────No────┐
  ╲     ╱           │
   ╲   ╱            │
    ╲ ╱             │
     │Yes           │
     │              ▼
     │         ┌─────────────────────┐
     │         │ Return Errors       │
     │         │ Show Error Messages │
     │         └─────────────────────┘
     │
     ▼
┌─────────────────────┐
│ Generate Patient ID │
│ (PAT-00001)         │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Save to Database:   │
│ - patients          │
│ - patient_insurance │
│ - emergency_contacts│
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Send Welcome SMS    │
│ via Twilio          │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Log Audit Entry     │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Show Success:       │
│ "Patient PAT-00001  │
│  registered!"       │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Print ╲────No─────┐
  ╲Wrist?╱           │
   ╲band?╱            │
    ╲ ╱               │
     │Yes             │
     │                │
     ▼                │
┌─────────────────────┐
│ Generate PDF        │
│ Wristband           │
└────┬────────────────┘
     │                │
     ▼                │
┌─────────────────────┐
│ Send to Printer     │
└────┬────────────────┘
     │                │
     ▼◄───────────────┘
┌─────────────────────┐
│ Redirect to         │
│ Insurance           │
│ Verification        │
└────┬────────────────┘
     │
     ▼
┌─────────┐
│   END   │
└─────────┘
```

---

## 7. Sequence Diagram

```
Front Desk    Frontend      Backend API    Database    AWS Textract   Twilio
    │             │              │            │             │            │
    │ Open        │              │            │             │            │
    │ Registration│              │            │             │            │
    ├────────────>│              │            │             │            │
    │             │              │            │             │            │
    │             │ Load Form    │            │             │            │
    │             │              │            │             │            │
    │ Enter       │              │            │             │            │
    │ Last Name   │              │            │             │            │
    │ + DOB       │              │            │             │            │
    ├────────────>│              │            │             │            │
    │             │              │            │             │            │
    │             │ On Blur:     │            │             │            │
    │             │ Check Dup    │            │             │            │
    │             │              │            │             │            │
    │             │ GET /patients/check-duplicate           │            │
    │             ├─────────────>│            │             │            │
    │             │              │            │             │            │
    │             │              │ SELECT     │             │            │
    │             │              ├───────────>│             │            │
    │             │              │            │             │            │
    │             │              │ Results    │             │            │
    │             │              │<───────────┤             │            │
    │             │              │            │             │            │
    │             │ Response:    │            │             │            │
    │             │ exists=false │            │             │            │
    │             │<─────────────┤            │             │            │
    │             │              │            │             │            │
    │ Fill        │              │            │             │            │
    │ Demographics│              │            │             │            │
    ├────────────>│              │            │             │            │
    │             │              │            │             │            │
    │             │ Real-time    │            │             │            │
    │             │ Validation   │            │             │            │
    │             │              │            │             │            │
    │ Upload      │              │            │             │            │
    │ Insurance   │              │            │             │            │
    │ Card        │              │            │             │            │
    ├────────────>│              │            │             │            │
    │             │              │            │             │            │
    │             │ POST /patients/ocr-insurance-card       │            │
    │             ├─────────────>│            │             │            │
    │             │              │            │             │            │
    │             │              │ Upload to S3             │            │
    │             │              │            │             │            │
    │             │              │ Call Textract            │            │
    │             │              ├────────────────────────>│            │
    │             │              │            │             │            │
    │             │              │            │ OCR Process │            │
    │             │              │            │             │            │
    │             │              │            │ Extracted   │            │
    │             │              │            │ Text        │            │
    │             │              │<────────────────────────┤            │
    │             │              │            │             │            │
    │             │              │ Parse Data │             │            │
    │             │              │            │             │            │
    │             │ Response:    │            │             │            │
    │             │ Insurance    │            │             │            │
    │             │ Data         │            │             │            │
    │             │<─────────────┤            │             │            │
    │             │              │            │             │            │
    │             │ Auto-fill    │            │             │            │
    │             │ Fields       │            │             │            │
    │             │              │            │             │            │
    │ Review &    │              │            │             │            │
    │ Correct     │              │            │             │            │
    ├────────────>│              │            │             │            │
    │             │              │            │             │            │
    │ Click Save  │              │            │             │            │
    ├────────────>│              │            │             │            │
    │             │              │            │             │            │
    │             │ POST /patients             │             │            │
    │             ├─────────────>│            │             │            │
    │             │              │            │             │            │
    │             │              │ Validate   │             │            │
    │             │              │            │             │            │
    │             │              │ Generate ID│             │            │
    │             │              │            │             │            │
    │             │              │ INSERT     │             │            │
    │             │              │ patients   │             │            │
    │             │              ├───────────>│             │            │
    │             │              │            │             │            │
    │             │              │ INSERT     │             │            │
    │             │              │ insurance  │             │            │
    │             │              ├───────────>│             │            │
    │             │              │            │             │            │
    │             │              │ INSERT     │             │            │
    │             │              │ emergency  │             │            │
    │             │              ├───────────>│             │            │
    │             │              │            │             │ Send SMS   │
    │             │              │            │             ├───────────>│
    │             │              │            │             │            │
    │             │              │            │             │ SMS Sent   │
    │             │              │            │             │<───────────┤
    │             │              │            │             │            │
    │             │ Response:    │            │             │            │
    │             │ patientId    │            │             │            │
    │             │<─────────────┤            │             │            │
    │             │              │            │             │            │
    │ Show Success│              │            │             │            │
    │ "PAT-00001" │              │            │             │            │
    │<────────────┤              │            │             │            │
    │             │              │            │             │            │
    │ Redirect to │              │            │             │            │
    │ Insurance   │              │            │             │            │
    │ Verification│              │            │             │            │
    │<────────────┤              │            │             │            │
    │             │              │            │             │            │
```

---

## 8. API Flow

### API 1: Check Duplicate

**Request:**
```http
GET /api/patients/check-duplicate?lastName=Smith&dob=1985-05-15
Authorization: Bearer {token}
```

**Response (No Duplicate):**
```json
{
  "exists": false,
  "message": "No duplicate found"
}
```

**Response (Duplicate Found):**
```json
{
  "exists": true,
  "message": "Potential duplicate found",
  "patients": [
    {
      "patientId": "PAT-00123",
      "firstName": "John",
      "lastName": "Smith",
      "dob": "1985-05-15",
      "ssn": "***-**-6789",
      "matchScore": 95
    }
  ]
}
```

---

### API 2: OCR Insurance Card

**Request:**
```http
POST /api/patients/ocr-insurance-card
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: [insurance_card.jpg]
```

**Response (Success):**
```json
{
  "payerName": "Aetna",
  "memberId": "W123456789",
  "groupNumber": "GRP12345",
  "planType": "PPO",
  "confidence": 0.92,
  "rawText": ["Aetna", "Member ID: W123456789", "Group: GRP12345"]
}
```

**Response (OCR Failed):**
```json
{
  "error": "OCR failed",
  "message": "Could not extract insurance data. Please enter manually.",
  "rawText": []
}
```

---

### API 3: Create Patient

**Request:**
```http
POST /api/patients
Authorization: Bearer {token}
Content-Type: application/json

{
  "firstName": "John",
  "lastName": "Smith",
  "dob": "1985-05-15",
  "gender": "M",
  "ssn": "123-45-6789",
  "address": "123 Main St",
  "city": "Boston",
  "state": "MA",
  "zip": "02101",
  "phone": "(555) 123-4567",
  "email": "john@email.com",
  "insurance": {
    "payerName": "Aetna",
    "memberId": "W123456789",
    "groupNumber": "GRP12345",
    "planType": "PPO",
    "effectiveDate": "2026-01-01"
  },
  "emergencyContact": {
    "name": "Jane Smith",
    "relationship": "Spouse",
    "phone": "(555) 987-6543"
  }
}
```

**Response (Success):**
```json
{
  "patientId": "PAT-00001",
  "message": "Patient registered successfully",
  "createdAt": "2026-05-18T19:30:00Z"
}
```

**Response (Validation Error):**
```json
{
  "error": "Validation failed",
  "details": [
    {
      "field": "ssn",
      "message": "Invalid SSN format"
    },
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ]
}
```

**Response (Duplicate Error):**
```json
{
  "error": "Duplicate patient",
  "message": "Patient with same SSN already exists: PAT-00123"
}
```

---

## 9. Database Flow

### Tables and Relationships

```
patients (Main table)
    ├── patient_insurance (1:Many)
    ├── emergency_contacts (1:Many)
    ├── guarantors (1:1 or 1:0)
    └── appointments (1:Many)
```

### Multi-Tenant Architecture

Every table contains:
- tenant_id
- organization_id
- facility_id

Purpose:
- Isolate hospital data
- Support SaaS architecture
- Enable multi-hospital deployment

### Table Schemas

**patients:**
```sql
CREATE TABLE patients (
    patient_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    ssn VARCHAR(255) NOT NULL,  -- Encrypted
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(2),
    zip VARCHAR(10),
    phone VARCHAR(20),
    email VARCHAR(255),
    created_by VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_patients_name_dob ON patients(last_name, dob);
CREATE INDEX idx_patients_ssn ON patients(ssn);
```

**patient_insurance:**
```sql
CREATE TABLE patient_insurance (
    insurance_id VARCHAR(50) PRIMARY KEY,
    patient_id VARCHAR(50) REFERENCES patients(patient_id),
    payer_name VARCHAR(200) NOT NULL,
    member_id VARCHAR(100) NOT NULL,
    group_number VARCHAR(100),
    plan_type VARCHAR(50),
    effective_date DATE,
    termination_date DATE,
    is_primary BOOLEAN DEFAULT TRUE,
    card_front_url VARCHAR(500),
    card_back_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**emergency_contacts:**
```sql
CREATE TABLE emergency_contacts (
    contact_id VARCHAR(50) PRIMARY KEY,
    patient_id VARCHAR(50) REFERENCES patients(patient_id),
    name VARCHAR(200) NOT NULL,
    relationship VARCHAR(50),
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    is_primary BOOLEAN DEFAULT TRUE
);
```

---

## 10. Error Scenarios

### Scenario 1: Duplicate Patient

**Trigger:** Patient with same SSN already exists

**Flow:**
```
User enters patient data
   ↓
Backend checks for duplicate (SSN match)
   ↓
Duplicate found
   ↓
Return 409 Conflict error
   ↓
Frontend shows warning:
"Patient with this SSN already exists: PAT-00123"
   ↓
Options:
1. View existing record
2. Update existing record
3. Contact admin if error
```

---

### Scenario 1a: Duplicate Merge Workflow

```
┌──────────────────────────┐
│ Duplicate Patient        │
│ Detected                 │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Send to MPI Review Queue │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ HIM Team Review          │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Merge Approval           │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Record Reconciliation    │
└──────────────────────────┘
```

---

### Scenario 2: OCR Fails

**Trigger:** Insurance card image is blurry or unsupported format

**Flow:**
```
User uploads insurance card
   ↓
Backend calls AWS Textract
   ↓
Textract returns low confidence (<70%)
   ↓
Backend returns partial data with warning
   ↓
Frontend shows:
"OCR confidence low. Please review and correct."
   ↓
User manually corrects fields
```

---

### Scenario 3: Invalid SSN

**Trigger:** User enters invalid SSN format

**Flow:**
```
User enters SSN: "000-00-0000"
   ↓
Frontend validation fails
   ↓
Show error: "Invalid SSN format"
   ↓
User corrects
   ↓
Backend also validates
   ↓
If still invalid, return 400 error
```

---

### Scenario 4: Twilio SMS Fails

**Trigger:** Twilio API is down or phone number invalid

**Flow:**
```
Patient saved successfully
   ↓
Try to send welcome SMS
   ↓
Twilio returns error
   ↓
Log error
   ↓
Continue (don't fail registration)
   ↓
Show warning to staff:
"Patient saved but SMS failed. Please inform patient manually."
```

---

### Scenario 5: Emergency Patient Registration

```
┌──────────────────────────┐
│ Unknown Patient Arrives  │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Generate Temporary MRN   │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Minimal Demographics     │
│ Collected                │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Emergency Treatment      │
│ Begins                   │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Full Registration        │
│ Completed Later          │
└──────────────────────────┘
```

---

## 11. Dashboard & Status Flow

### Registration Queue Management

Queue Types:
- Walk-in queue
- Appointment queue
- Emergency queue
- VIP queue
- Kiosk queue

Features:
- Wait time tracking
- Queue priority
- Real-time dashboard

### Enterprise Registration Status Lifecycle

```
┌──────────────────────────┐
│      Pre-Registered      │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│         Arrived          │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│       Checked-In         │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Registration Complete    │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Eligibility Verified     │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Financial Clearance      │
│ Complete                 │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Ready for Encounter      │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│     In Consultation      │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│       Discharged         │
└──────────────────────────┘
```

---

## 12. Third-Party APIs

### AWS Textract

**Purpose:** Extract text from insurance card images

**Setup:**
```python
import boto3

textract = boto3.client(
    'textract',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name='us-east-1'
)

response = textract.detect_document_text(
    Document={'S3Object': {'Bucket': 'bucket-name', 'Name': 'card.jpg'}}
)
```

**Cost:** $1.50 per 1,000 pages  
**Response Time:** 2-5 seconds

---

### Twilio SMS

**Purpose:** Send welcome message to patient

**Setup:**
```python
from twilio.rest import Client

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

message = client.messages.create(
    body=f"Welcome to Hospital! Your Patient ID is {patient_id}",
    from_=TWILIO_PHONE,
    to=patient_phone
)
```

**Cost:** $0.0079 per SMS  
**Response Time:** < 10 seconds

---

### HL7 / FHIR Integration

```
┌──────────────────────────┐
│ Registration Completed   │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Generate HL7 ADT A04     │
│ Message                  │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Send to EMR / EHR        │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Create FHIR Patient      │
│ Resource                 │
└──────────────────────────┘
```

---

## 13. Document Management

- Insurance cards
- Consent PDFs
- Driver licenses
- Referral documents
- Prior authorization files
- Secure S3 storage
- Signed URL access
- OCR metadata indexing

---

## Summary

**Module:** Patient Registration  
**Complexity:** Medium  
**Development Time:** 1.5 weeks  
**Dependencies:** AWS Textract, Twilio, Database  
**Critical:** Yes (first step in RCM)  

**Security Features:**
- AES-256 encryption
- TLS 1.2+
- MFA authentication
- RBAC authorization
- PHI audit tracking
- Signed URL document access
- HIPAA retention policies

**Key Features:**
✅ Pre-registration workflow
✅ Duplicate detection
✅ Duplicate merge workflow
✅ OCR for insurance cards (Front & Back)
✅ Real-time validation
✅ Identity verification
✅ Consent management
✅ Real-time eligibility verification
✅ Financial responsibility estimation
✅ Welcome notifications
✅ Portal activation with MFA
✅ Emergency contacts
✅ Guarantor support
✅ Audit logging (advanced)
✅ HIPAA compliant (SSN encryption)
✅ Multi-tenant architecture
✅ HL7 / FHIR integration
✅ Document management
✅ Queue management
✅ Self-service kiosk support
✅ Emergency patient registration

---

**Next Module:** [Module 3: Insurance Verification](Flows_Module_03_Insurance_Verification.md)
