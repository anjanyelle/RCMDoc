# Healthcare RCM Application - Development Phase Guide
## Part 2: Phase 1 Core Modules (Patient, Insurance, Appointments)

**Version:** 1.0  
**For:** Technical Lead & Development Team

---

## F. First Core Modules to Build (Week 3-6)

### Module 1: Patient Registration (Week 3-4)

#### What This Module Does
Allows front desk staff to register new patients and store their information in the system.

**User Story:**
"As a front desk staff member, I want to register new patients quickly so that we can schedule their appointments and verify insurance."

---

#### Frontend Screens

**Screen 1: Patient Search/List**
```
┌─────────────────────────────────────────────────┐
│  Healthcare RCM - Patient Management            │
├─────────────────────────────────────────────────┤
│                                                  │
│  [Search: _______________] [🔍 Search]          │
│                                                  │
│  [+ New Patient]                                │
│                                                  │
│  Recent Patients:                               │
│  ┌──────────────────────────────────────────┐  │
│  │ John Doe    | DOB: 05/15/1980 | View     │  │
│  │ Jane Smith  | DOB: 03/22/1975 | View     │  │
│  │ Bob Johnson | DOB: 11/08/1990 | View     │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Screen 2: Patient Registration Form**
```
┌─────────────────────────────────────────────────┐
│  New Patient Registration                       │
├─────────────────────────────────────────────────┤
│                                                  │
│  Personal Information                           │
│  ┌──────────────────────────────────────────┐  │
│  │ First Name: [___________]                │  │
│  │ Last Name:  [___________]                │  │
│  │ DOB:        [MM/DD/YYYY]                 │  │
│  │ Gender:     [○ Male ○ Female ○ Other]   │  │
│  │ SSN:        [___-__-____]                │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  Contact Information                            │
│  ┌──────────────────────────────────────────┐  │
│  │ Phone:      [(___) ___-____]             │  │
│  │ Email:      [___________]                │  │
│  │ Address:    [___________]                │  │
│  │ City:       [___________]                │  │
│  │ State:      [__]  ZIP: [_____]          │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  Insurance Information                          │
│  ┌──────────────────────────────────────────┐  │
│  │ Insurance:  [Select Payer ▼]            │  │
│  │ Policy #:   [___________]                │  │
│  │ Group #:    [___________]                │  │
│  │ [📷 Scan Insurance Card]                 │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  [Cancel]                    [Save Patient]     │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Frontend Code:**
```typescript
// src/pages/PatientRegistration.tsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import api from '../services/api';

interface PatientFormData {
  firstName: string;
  lastName: string;
  dob: string;
  gender: string;
  ssn: string;
  phone: string;
  email: string;
  address: string;
  city: string;
  state: string;
  zipCode: string;
  insurance: {
    payerName: string;
    policyNumber: string;
    groupNumber: string;
  };
}

function PatientRegistration() {
  const { register, handleSubmit, formState: { errors } } = useForm<PatientFormData>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const onSubmit = async (data: PatientFormData) => {
    setLoading(true);
    setError('');

    try {
      const response = await api.post('/patients', data);
      
      // Show success message
      alert(`Patient created successfully! ID: ${response.data.patientId}`);
      
      // Navigate to patient details
      navigate(`/patients/${response.data.patientId}`);
    } catch (err: any) {
      if (err.response?.status === 409) {
        setError('Duplicate patient found. Please search for existing patient.');
      } else {
        setError(err.response?.data?.detail || 'Failed to create patient');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">New Patient Registration</h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Personal Information */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Personal Information</h2>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">
                First Name <span className="text-red-500">*</span>
              </label>
              <input
                {...register('firstName', { required: 'First name is required' })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
              {errors.firstName && (
                <p className="text-red-500 text-sm mt-1">{errors.firstName.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                Last Name <span className="text-red-500">*</span>
              </label>
              <input
                {...register('lastName', { required: 'Last name is required' })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
              {errors.lastName && (
                <p className="text-red-500 text-sm mt-1">{errors.lastName.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                Date of Birth <span className="text-red-500">*</span>
              </label>
              <input
                type="date"
                {...register('dob', { required: 'DOB is required' })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
              {errors.dob && (
                <p className="text-red-500 text-sm mt-1">{errors.dob.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                Gender <span className="text-red-500">*</span>
              </label>
              <select
                {...register('gender', { required: 'Gender is required' })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              >
                <option value="">Select...</option>
                <option value="M">Male</option>
                <option value="F">Female</option>
                <option value="O">Other</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                SSN
              </label>
              <input
                {...register('ssn', {
                  pattern: {
                    value: /^\d{3}-\d{2}-\d{4}$/,
                    message: 'SSN must be in format: 123-45-6789'
                  }
                })}
                placeholder="123-45-6789"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
              {errors.ssn && (
                <p className="text-red-500 text-sm mt-1">{errors.ssn.message}</p>
              )}
            </div>
          </div>
        </div>

        {/* Contact Information */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Contact Information</h2>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">
                Phone <span className="text-red-500">*</span>
              </label>
              <input
                {...register('phone', { required: 'Phone is required' })}
                placeholder="(555) 123-4567"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                Email
              </label>
              <input
                type="email"
                {...register('email')}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>

            <div className="col-span-2">
              <label className="block text-sm font-medium mb-1">
                Address
              </label>
              <input
                {...register('address')}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                City
              </label>
              <input
                {...register('city')}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">
                  State
                </label>
                <input
                  {...register('state')}
                  maxLength={2}
                  placeholder="CA"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">
                  ZIP Code
                </label>
                <input
                  {...register('zipCode')}
                  placeholder="12345"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Insurance Information */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Insurance Information</h2>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">
                Insurance Payer
              </label>
              <select
                {...register('insurance.payerName')}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              >
                <option value="">Select payer...</option>
                <option value="Blue Cross Blue Shield">Blue Cross Blue Shield</option>
                <option value="Aetna">Aetna</option>
                <option value="UnitedHealthcare">UnitedHealthcare</option>
                <option value="Cigna">Cigna</option>
                <option value="Medicare">Medicare</option>
                <option value="Medicaid">Medicaid</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                Policy Number
              </label>
              <input
                {...register('insurance.policyNumber')}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                Group Number
              </label>
              <input
                {...register('insurance.groupNumber')}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>
          </div>
        </div>

        {/* Submit Buttons */}
        <div className="flex justify-end space-x-4">
          <button
            type="button"
            onClick={() => navigate('/patients')}
            className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Saving...' : 'Save Patient'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default PatientRegistration;
```

---

#### Backend APIs

**API Endpoint 1: Create Patient**
```python
# app/api/v1/patients.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.patient import PatientCreate, PatientResponse
from app.services.patient_service import PatientService
from app.models.user import User
from app.core.auth import get_current_user

router = APIRouter()

@router.post("", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(
    patient_data: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new patient
    
    Required role: front_desk, admin
    """
    patient_service = PatientService(db)
    
    # Check for duplicate patient
    existing_patient = patient_service.find_duplicate(
        first_name=patient_data.firstName,
        last_name=patient_data.lastName,
        dob=patient_data.dob
    )
    
    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Duplicate patient found: {existing_patient.patient_id}"
        )
    
    # Create patient
    patient = patient_service.create_patient(patient_data, current_user.user_id)
    
    return patient
```

**Pydantic Schemas:**
```python
# app/schemas/patient.py
from pydantic import BaseModel, EmailStr, validator
from datetime import date
from typing import Optional

class InsuranceInfo(BaseModel):
    payerName: Optional[str] = None
    policyNumber: Optional[str] = None
    groupNumber: Optional[str] = None

class PatientCreate(BaseModel):
    firstName: str
    lastName: str
    dob: date
    gender: str
    ssn: Optional[str] = None
    phone: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zipCode: Optional[str] = None
    insurance: Optional[InsuranceInfo] = None
    
    @validator('gender')
    def validate_gender(cls, v):
        if v not in ['M', 'F', 'O']:
            raise ValueError('Gender must be M, F, or O')
        return v
    
    @validator('ssn')
    def validate_ssn(cls, v):
        if v and not v.replace('-', '').isdigit():
            raise ValueError('SSN must contain only numbers and hyphens')
        return v

class PatientResponse(BaseModel):
    patientId: str
    firstName: str
    lastName: str
    dob: date
    gender: str
    phone: str
    email: Optional[str]
    
    class Config:
        from_attributes = True
```

**Service Layer:**
```python
# app/services/patient_service.py
from sqlalchemy.orm import Session
from app.models.patient import Patient, PatientInsurance
from app.schemas.patient import PatientCreate
from datetime import datetime
import uuid

class PatientService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_patient(self, patient_data: PatientCreate, created_by: str) -> Patient:
        """Create a new patient"""
        
        # Generate patient ID
        patient_id = f"PAT-{datetime.now().year}-{str(uuid.uuid4())[:6].upper()}"
        
        # Create patient record
        patient = Patient(
            patient_id=patient_id,
            first_name=patient_data.firstName,
            last_name=patient_data.lastName,
            dob=patient_data.dob,
            gender=patient_data.gender,
            ssn=patient_data.ssn,
            phone=patient_data.phone,
            email=patient_data.email,
            address=patient_data.address,
            city=patient_data.city,
            state=patient_data.state,
            zip_code=patient_data.zipCode,
            created_by=created_by
        )
        
        self.db.add(patient)
        self.db.flush()  # Get patient_id
        
        # Create insurance record if provided
        if patient_data.insurance and patient_data.insurance.payerName:
            insurance = PatientInsurance(
                patient_id=patient.patient_id,
                payer_name=patient_data.insurance.payerName,
                policy_number=patient_data.insurance.policyNumber,
                group_number=patient_data.insurance.groupNumber,
                priority=1,  # Primary insurance
                is_active=True,
                created_by=created_by
            )
            self.db.add(insurance)
        
        self.db.commit()
        self.db.refresh(patient)
        
        return patient
    
    def find_duplicate(self, first_name: str, last_name: str, dob: date):
        """Check for duplicate patient"""
        return self.db.query(Patient).filter(
            Patient.first_name == first_name,
            Patient.last_name == last_name,
            Patient.dob == dob
        ).first()
```

---

#### Database Tables

**Table 1: patients**
```sql
CREATE TABLE patients (
    patient_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    gender CHAR(1) NOT NULL CHECK (gender IN ('M', 'F', 'O')),
    ssn VARCHAR(11),  -- Encrypted
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(2),
    zip_code VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50),
    
    CONSTRAINT chk_phone CHECK (phone ~ '^\(\d{3}\) \d{3}-\d{4}$')
);

-- Indexes for fast searching
CREATE INDEX idx_patient_name ON patients(last_name, first_name);
CREATE INDEX idx_patient_dob ON patients(dob);
CREATE INDEX idx_patient_phone ON patients(phone);
```

**Table 2: patient_insurance**
```sql
CREATE TABLE patient_insurance (
    insurance_id SERIAL PRIMARY KEY,
    patient_id VARCHAR(50) NOT NULL REFERENCES patients(patient_id),
    payer_name VARCHAR(200) NOT NULL,
    policy_number VARCHAR(100),
    group_number VARCHAR(100),
    priority INTEGER NOT NULL DEFAULT 1,  -- 1=Primary, 2=Secondary, 3=Tertiary
    is_active BOOLEAN DEFAULT TRUE,
    effective_date DATE,
    termination_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    
    CONSTRAINT chk_priority CHECK (priority IN (1, 2, 3))
);

CREATE INDEX idx_patient_insurance_patient ON patient_insurance(patient_id);
```

**SQLAlchemy Models:**
```python
# app/models/patient.py
from sqlalchemy import Column, String, Date, Boolean, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Patient(Base):
    __tablename__ = "patients"
    
    patient_id = Column(String(50), primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(String(1), nullable=False)
    ssn = Column(String(11))
    phone = Column(String(20), nullable=False)
    email = Column(String(255))
    address = Column(String(255))
    city = Column(String(100))
    state = Column(String(2))
    zip_code = Column(String(10))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(50), nullable=False)
    updated_by = Column(String(50))
    
    # Relationships
    insurances = relationship("PatientInsurance", back_populates="patient")
    encounters = relationship("Encounter", back_populates="patient")

class PatientInsurance(Base):
    __tablename__ = "patient_insurance"
    
    insurance_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String(50), ForeignKey("patients.patient_id"), nullable=False)
    payer_name = Column(String(200), nullable=False)
    policy_number = Column(String(100))
    group_number = Column(String(100))
    priority = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    effective_date = Column(Date)
    termination_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(50), nullable=False)
    
    # Relationships
    patient = relationship("Patient", back_populates="insurances")
```

---

#### Validation Rules

**Frontend Validation:**
1. **Required fields:** First name, last name, DOB, gender, phone
2. **Format validation:**
   - Phone: (555) 123-4567
   - SSN: 123-45-6789
   - Email: valid email format
   - Date: MM/DD/YYYY
3. **Age validation:** Patient must be born before today
4. **Duplicate check:** Before submitting, check if patient exists

**Backend Validation:**
1. **Data type validation:** Pydantic models
2. **Business rules:**
   - DOB cannot be in future
   - Gender must be M, F, or O
   - Phone is required
   - SSN is optional but must be valid format if provided
3. **Duplicate prevention:** Check name + DOB combination
4. **SQL injection prevention:** Use ORM (SQLAlchemy)

---

#### User Workflow

**Step-by-Step Process:**

1. **Front desk clicks "New Patient"**
   - System opens registration form
   - All fields are empty

2. **Front desk enters patient information**
   - Types name, DOB, gender
   - Types contact information
   - Enters insurance details (if available)

3. **Optional: Scan insurance card**
   - Click "Scan Insurance Card" button
   - Use phone camera to take photo
   - OCR extracts: Payer name, policy number, group number
   - Auto-fills insurance fields

4. **Front desk clicks "Save Patient"**
   - Frontend validates all fields
   - If validation fails → Show error messages
   - If validation passes → Send to backend

5. **Backend processes request**
   - Validates data again
   - Checks for duplicate patient
   - If duplicate → Return error
   - If unique → Create patient record
   - Generate patient ID (e.g., PAT-2026-A1B2C3)
   - Save to database

6. **System shows success message**
   - Display: "Patient created successfully! ID: PAT-2026-A1B2C3"
   - Redirect to patient details page
   - Front desk can now verify insurance or schedule appointment

**Time to complete:** 2-3 minutes per patient

---

### Module 2: Insurance Verification (Week 4)

#### What This Module Does
Checks if patient's insurance is active and retrieves coverage details before the appointment.

**Why it's critical:**
- If insurance is inactive → Patient becomes self-pay
- Prevents treating patients who can't pay
- Determines how much patient owes (copay, deductible)

---

#### Frontend Screens

**Screen: Insurance Verification**
```
┌─────────────────────────────────────────────────┐
│  Insurance Verification - John Doe              │
├─────────────────────────────────────────────────┤
│                                                  │
│  Patient: John Doe (DOB: 05/15/1980)           │
│  Insurance: Blue Cross Blue Shield              │
│  Policy #: ABC123456789                         │
│                                                  │
│  Service Date: [05/20/2026] [Today]            │
│                                                  │
│  [🔄 Verify Insurance]                          │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │ Verification Results:                    │  │
│  │                                          │  │
│  │ ✅ Status: ACTIVE                        │  │
│  │                                          │  │
│  │ Coverage Details:                        │  │
│  │ • Copay: $25.00                         │  │
│  │ • Deductible: $1,500 annual             │  │
│  │   - Met: $800                           │  │
│  │   - Remaining: $700                     │  │
│  │ • Out-of-Pocket Max: $5,000             │  │
│  │   - Met: $1,200                         │  │
│  │   - Remaining: $3,800                   │  │
│  │ • Network: IN-NETWORK                   │  │
│  │ • Prior Auth: Not required              │  │
│  │                                          │  │
│  │ Verified: 05/18/2026 10:30 AM           │  │
│  │ Valid until: 05/19/2026 10:30 AM        │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  [Print] [Schedule Appointment]                 │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Frontend Code:**
```typescript
// src/pages/InsuranceVerification.tsx
import { useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';

interface VerificationResult {
  status: string;
  copay: number;
  deductible: {
    annual: number;
    met: number;
    remaining: number;
  };
  oopMax: {
    annual: number;
    met: number;
    remaining: number;
  };
  networkStatus: string;
  priorAuthRequired: boolean;
  verifiedAt: string;
  validUntil: string;
}

function InsuranceVerification() {
  const { patientId } = useParams();
  const [serviceDate, setServiceDate] = useState(new Date().toISOString().split('T')[0]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<VerificationResult | null>(null);
  const [error, setError] = useState('');

  const handleVerify = async () => {
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await api.post('/eligibility/verify', {
        patientId,
        serviceDate
      });

      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Verification failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Insurance Verification</h1>

      {/* Patient Info */}
      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <h2 className="text-xl font-semibold mb-4">Patient Information</h2>
        {/* Display patient details */}
      </div>

      {/* Verification Form */}
      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <div className="flex items-end space-x-4">
          <div className="flex-1">
            <label className="block text-sm font-medium mb-1">
              Service Date
            </label>
            <input
              type="date"
              value={serviceDate}
              onChange={(e) => setServiceDate(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <button
            onClick={handleVerify}
            disabled={loading}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Verifying...' : '🔄 Verify Insurance'}
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}

      {/* Verification Results */}
      {result && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Verification Results</h2>
          
          <div className="space-y-4">
            <div className="flex items-center">
              <span className="text-2xl mr-2">
                {result.status === 'ACTIVE' ? '✅' : '❌'}
              </span>
              <span className="text-xl font-semibold">
                Status: {result.status}
              </span>
            </div>

            {result.status === 'ACTIVE' && (
              <>
                <div className="border-t pt-4">
                  <h3 className="font-semibold mb-2">Coverage Details:</h3>
                  <ul className="space-y-2 ml-4">
                    <li>• Copay: ${result.copay.toFixed(2)}</li>
                    <li>
                      • Deductible: ${result.deductible.annual.toFixed(2)} annual
                      <ul className="ml-6 text-sm text-gray-600">
                        <li>- Met: ${result.deductible.met.toFixed(2)}</li>
                        <li>- Remaining: ${result.deductible.remaining.toFixed(2)}</li>
                      </ul>
                    </li>
                    <li>
                      • Out-of-Pocket Max: ${result.oopMax.annual.toFixed(2)}
                      <ul className="ml-6 text-sm text-gray-600">
                        <li>- Met: ${result.oopMax.met.toFixed(2)}</li>
                        <li>- Remaining: ${result.oopMax.remaining.toFixed(2)}</li>
                      </ul>
                    </li>
                    <li>• Network: {result.networkStatus}</li>
                    <li>
                      • Prior Auth: {result.priorAuthRequired ? 'Required' : 'Not required'}
                    </li>
                  </ul>
                </div>

                <div className="border-t pt-4 text-sm text-gray-600">
                  <p>Verified: {new Date(result.verifiedAt).toLocaleString()}</p>
                  <p>Valid until: {new Date(result.validUntil).toLocaleString()}</p>
                </div>
              </>
            )}
          </div>

          <div className="mt-6 flex justify-end space-x-4">
            <button className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              Print
            </button>
            <button className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">
              Schedule Appointment
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default InsuranceVerification;
```

---

#### Backend APIs

**API Endpoint: Verify Eligibility**
```python
# app/api/v1/eligibility.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.eligibility import EligibilityRequest, EligibilityResponse
from app.services.eligibility_service import EligibilityService
from app.models.user import User
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/verify", response_model=EligibilityResponse)
async def verify_eligibility(
    request: EligibilityRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Verify patient insurance eligibility
    
    This endpoint:
    1. Gets patient and insurance info from database
    2. Calls Waystar/Availity API (EDI 270/271)
    3. Parses response
    4. Caches result for 24 hours
    5. Returns eligibility details
    """
    eligibility_service = EligibilityService(db)
    
    # Check cache first (Redis)
    cached_result = eligibility_service.get_cached_result(
        request.patientId,
        request.serviceDate
    )
    
    if cached_result:
        return cached_result
    
    # Call external API
    result = await eligibility_service.verify(
        patient_id=request.patientId,
        service_date=request.serviceDate
    )
    
    # Cache result for 24 hours
    eligibility_service.cache_result(result)
    
    return result
```

**Service Layer:**
```python
# app/services/eligibility_service.py
from sqlalchemy.orm import Session
from app.models.patient import Patient, PatientInsurance
from app.models.eligibility import EligibilityCheck
from datetime import datetime, timedelta
import httpx
import os

class EligibilityService:
    def __init__(self, db: Session):
        self.db = db
        self.waystar_api_key = os.getenv("WAYSTAR_API_KEY")
        self.waystar_base_url = "https://api.waystar.com/eligibility/v1"
    
    async def verify(self, patient_id: str, service_date: str):
        """Verify insurance eligibility via Waystar API"""
        
        # Get patient and insurance info
        patient = self.db.query(Patient).filter(
            Patient.patient_id == patient_id
        ).first()
        
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        insurance = self.db.query(PatientInsurance).filter(
            PatientInsurance.patient_id == patient_id,
            PatientInsurance.priority == 1,  # Primary insurance
            PatientInsurance.is_active == True
        ).first()
        
        if not insurance:
            raise HTTPException(status_code=404, detail="No active insurance found")
        
        # Prepare EDI 270 request
        request_payload = {
            "patient": {
                "firstName": patient.first_name,
                "lastName": patient.last_name,
                "dob": patient.dob.isoformat(),
                "gender": patient.gender
            },
            "insurance": {
                "payerName": insurance.payer_name,
                "policyNumber": insurance.policy_number,
                "groupNumber": insurance.group_number
            },
            "serviceDate": service_date
        }
        
        # Call Waystar API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.waystar_base_url}/inquiries",
                json=request_payload,
                headers={
                    "Authorization": f"Bearer {self.waystar_api_key}",
                    "Content-Type": "application/json"
                },
                timeout=30.0
            )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Eligibility verification failed"
            )
        
        # Parse EDI 271 response
        data = response.json()
        
        result = {
            "status": data.get("status", "UNKNOWN"),
            "copay": data.get("copay", 0),
            "deductible": {
                "annual": data.get("deductible", {}).get("annual", 0),
                "met": data.get("deductible", {}).get("met", 0),
                "remaining": data.get("deductible", {}).get("remaining", 0)
            },
            "oopMax": {
                "annual": data.get("oopMax", {}).get("annual", 0),
                "met": data.get("oopMax", {}).get("met", 0),
                "remaining": data.get("oopMax", {}).get("remaining", 0)
            },
            "networkStatus": data.get("networkStatus", "UNKNOWN"),
            "priorAuthRequired": data.get("priorAuthRequired", False),
            "verifiedAt": datetime.utcnow().isoformat(),
            "validUntil": (datetime.utcnow() + timedelta(hours=24)).isoformat()
        }
        
        # Save to database
        eligibility_check = EligibilityCheck(
            patient_id=patient_id,
            insurance_id=insurance.insurance_id,
            service_date=service_date,
            status=result["status"],
            copay=result["copay"],
            deductible_annual=result["deductible"]["annual"],
            deductible_met=result["deductible"]["met"],
            deductible_remaining=result["deductible"]["remaining"],
            verified_at=datetime.utcnow()
        )
        self.db.add(eligibility_check)
        self.db.commit()
        
        return result
```

---

#### Database Tables

**Table: eligibility_checks**
```sql
CREATE TABLE eligibility_checks (
    check_id SERIAL PRIMARY KEY,
    patient_id VARCHAR(50) NOT NULL REFERENCES patients(patient_id),
    insurance_id INTEGER NOT NULL REFERENCES patient_insurance(insurance_id),
    service_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,  -- ACTIVE, INACTIVE, UNKNOWN
    copay DECIMAL(10,2),
    deductible_annual DECIMAL(10,2),
    deductible_met DECIMAL(10,2),
    deductible_remaining DECIMAL(10,2),
    oop_max_annual DECIMAL(10,2),
    oop_max_met DECIMAL(10,2),
    oop_max_remaining DECIMAL(10,2),
    network_status VARCHAR(20),  -- IN-NETWORK, OUT-OF-NETWORK
    prior_auth_required BOOLEAN,
    verified_at TIMESTAMP NOT NULL,
    verified_by VARCHAR(50) NOT NULL,
    raw_response TEXT,  -- Store full EDI 271 response
    
    CONSTRAINT chk_status CHECK (status IN ('ACTIVE', 'INACTIVE', 'UNKNOWN'))
);

CREATE INDEX idx_eligibility_patient ON eligibility_checks(patient_id);
CREATE INDEX idx_eligibility_date ON eligibility_checks(service_date);
```

---

### Module 3: Appointment Scheduling (Week 5)

#### What This Module Does
Allows front desk to schedule patient appointments with providers.

**Key Features:**
- View provider calendars
- Schedule appointments
- Send automated reminders (SMS, email)
- Track no-shows

---

#### Frontend Screens

**Screen: Appointment Scheduler**
```
┌─────────────────────────────────────────────────┐
│  Appointment Scheduler                          │
├─────────────────────────────────────────────────┤
│                                                  │
│  Provider: [Dr. Smith ▼]    Date: [05/20/2026] │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │ Time Slots:                              │  │
│  │                                          │  │
│  │ 09:00 AM - Available [Book]             │  │
│  │ 09:30 AM - Available [Book]             │  │
│  │ 10:00 AM - BOOKED (Jane Doe)            │  │
│  │ 10:30 AM - Available [Book]             │  │
│  │ 11:00 AM - Available [Book]             │  │
│  │ 11:30 AM - LUNCH BREAK                  │  │
│  │ 12:00 PM - LUNCH BREAK                  │  │
│  │ 01:00 PM - Available [Book]             │  │
│  │ 01:30 PM - Available [Book]             │  │
│  │ 02:00 PM - BOOKED (Bob Johnson)         │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
└─────────────────────────────────────────────────┘

When clicking [Book]:
┌─────────────────────────────────────────────────┐
│  Book Appointment - 09:00 AM                    │
├─────────────────────────────────────────────────┤
│                                                  │
│  Patient: [Search patient...] [🔍]             │
│           John Doe (DOB: 05/15/1980)           │
│                                                  │
│  Appointment Type: [Office Visit ▼]            │
│  Duration: [30 minutes]                         │
│  Reason: [___________]                          │
│                                                  │
│  Send Reminders:                                │
│  ☑ SMS (24 hours before)                       │
│  ☑ Email (24 hours before)                     │
│                                                  │
│  [Cancel]                    [Book Appointment] │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Backend API:**
```python
# app/api/v1/appointments.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.services.appointment_service import AppointmentService

router = APIRouter()

@router.post("", response_model=AppointmentResponse)
def create_appointment(
    appointment_data: AppointmentCreate,
    db: Session = Depends(get_db)
):
    """Create new appointment"""
    service = AppointmentService(db)
    appointment = service.create_appointment(appointment_data)
    
    # Send reminders (background task)
    service.schedule_reminders(appointment)
    
    return appointment

@router.get("/availability")
def get_availability(
    provider_id: str,
    date: str,
    db: Session = Depends(get_db)
):
    """Get provider availability for a date"""
    service = AppointmentService(db)
    slots = service.get_available_slots(provider_id, date)
    return slots
```

---

### G. Third-Party APIs in Phase 1 (Week 5-6)

#### 1. Availity API (Insurance Verification)

**What it does:** Checks insurance eligibility (EDI 270/271)

**When to use:** Every time we verify insurance

**API Documentation:** https://www.availity.com/developers

**Example Request:**
```python
import httpx

async def verify_with_availity(patient, insurance, service_date):
    url = "https://api.availity.com/eligibility/v1/check"
    
    payload = {
        "patient": {
            "firstName": patient.first_name,
            "lastName": patient.last_name,
            "dob": patient.dob.isoformat()
        },
        "insurance": {
            "payerId": "00431",  # Payer ID from Availity
            "policyNumber": insurance.policy_number
        },
        "serviceDate": service_date
    }
    
    headers = {
        "Authorization": f"Bearer {AVAILITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        return response.json()
```

**Can we mock it initially?** YES
- Create a mock service that returns fake eligibility data
- Replace with real API later
- Saves time and money during development

**Mock Implementation:**
```python
# app/services/mock_eligibility.py
def mock_eligibility_check(patient_id, service_date):
    """Mock eligibility response for testing"""
    return {
        "status": "ACTIVE",
        "copay": 25.00,
        "deductible": {
            "annual": 1500.00,
            "met": 800.00,
            "remaining": 700.00
        },
        "oopMax": {
            "annual": 5000.00,
            "met": 1200.00,
            "remaining": 3800.00
        },
        "networkStatus": "IN-NETWORK",
        "priorAuthRequired": False
    }
```

---

#### 2. Twilio API (SMS Notifications)

**What it does:** Sends SMS reminders to patients

**When to use:** 24 hours before appointment

**API Documentation:** https://www.twilio.com/docs/sms

**Example:**
```python
from twilio.rest import Client

def send_appointment_reminder(patient_phone, appointment_time):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    message = client.messages.create(
        body=f"Reminder: You have an appointment tomorrow at {appointment_time}. Reply CONFIRM to confirm.",
        from_=TWILIO_PHONE_NUMBER,
        to=patient_phone
    )
    
    return message.sid
```

**Cost:** $0.0079 per SMS (very cheap)

**Can we mock it initially?** YES
- Just log the message to console
- Don't actually send SMS during development

---

#### 3. FHIR APIs (EHR Integration)

**What it does:** Connects to Electronic Health Record systems (Epic, Cerner)

**When to use:** Get patient clinical data (diagnoses, procedures, medications)

**API Documentation:** https://www.hl7.org/fhir/

**Example:**
```python
async def get_patient_from_ehr(patient_mrn):
    url = f"https://fhir.epic.com/Patient/{patient_mrn}"
    
    headers = {
        "Authorization": f"Bearer {EPIC_ACCESS_TOKEN}",
        "Accept": "application/fhir+json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()
```

**Can we mock it initially?** YES - HIGHLY RECOMMENDED
- FHIR integration is complex
- Requires hospital approval
- Mock it in Phase 1, integrate in Phase 2

---

#### 4. OCR APIs (Insurance Card Scanning)

**What it does:** Extracts text from insurance card photos

**Options:**
- **AWS Textract** (recommended)
- **Google Cloud Vision**
- **OpenAI Vision API**

**Example with AWS Textract:**
```python
import boto3

def extract_insurance_card(image_bytes):
    textract = boto3.client('textract')
    
    response = textract.detect_document_text(
        Document={'Bytes': image_bytes}
    )
    
    # Extract text
    text = ""
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + "\n"
    
    # Parse insurance info (use regex or AI)
    insurance_info = parse_insurance_text(text)
    
    return insurance_info
```

**Can we mock it initially?** YES
- Manual entry is fine for MVP
- Add OCR in Phase 2 or 3

---

### H. Deliverables of Phase 1 (Week 6)

**Before moving to Phase 2, you must have:**

✅ **1. Working Authentication System**
- Users can login/logout
- JWT tokens working
- Role-based access control
- Session management

✅ **2. Patient Registration Module**
- Create new patients
- Store demographics
- Store insurance info
- Duplicate patient detection
- Search patients

✅ **3. Insurance Verification Module**
- Verify eligibility (mock or real API)
- Display coverage details
- Cache results
- Store verification history

✅ **4. Appointment Scheduling Module**
- View provider calendars
- Book appointments
- Send reminders (mock or real)
- View scheduled appointments

✅ **5. Database Setup**
- All tables created
- Migrations working
- Indexes added
- Sample data loaded

✅ **6. API Documentation**
- Swagger UI working
- All endpoints documented
- Request/response examples
- Error codes documented

✅ **7. Basic UI/UX**
- Responsive design (works on desktop/tablet)
- Clean, professional look
- Easy navigation
- Form validations

✅ **8. Testing**
- Unit tests for critical functions
- API integration tests
- Manual testing completed
- Bug list created and prioritized

✅ **9. Deployment**
- Code deployed to staging environment
- Database deployed
- Environment variables configured
- Health checks working

✅ **10. Documentation**
- Setup instructions
- API documentation
- User guide (basic)
- Known issues list

**Demo Readiness:**
You should be able to demonstrate:
1. Login as front desk user
2. Register a new patient
3. Verify their insurance
4. Schedule an appointment
5. View the appointment on calendar

**Time:** 2-3 minutes for complete demo

---

**Continue to Part 3 for Phase 2 (Clinical & Billing)...**

---

**Document Navigation:**
- **Part 1:** Introduction & Phase 1 Foundation Setup
- **Part 2:** Phase 1 Core Modules (This document)
- **Part 3:** Phase 2 Clinical & Billing
- **Part 4:** Phase 3 Payment & Denials
- **Part 5:** Phase 4 Reports & Deployment
