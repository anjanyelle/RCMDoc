# Healthcare RCM Application - Development Phase Guide
## Part 1: Introduction & Phase 1 (Foundation Setup)

**Version:** 1.0  
**For:** Technical Lead & Development Team  
**Purpose:** Step-by-step development guide from scratch

---

## 1. Project Overview

### What We're Building
A **Healthcare Revenue Cycle Management (RCM)** system that helps hospitals and clinics:
- Register patients and verify their insurance
- Track doctor visits and services provided
- Convert services into medical codes
- Create and submit insurance claims
- Receive and track payments
- Handle claim denials and appeals
- Bill patients for their portion

**Think of it like:** An automated billing system for hospitals that reduces errors and speeds up payment collection.

### Business Goals
- **Reduce claim denials** from 15% to <5%
- **Speed up payment collection** from 60 days to 30 days
- **Increase revenue** by capturing all charges correctly
- **Reduce manual work** by 70% through automation

### Technical Goals
- Build a modern, cloud-based web application
- Use AI to assist with medical coding and error detection
- Integrate with insurance companies via APIs
- Ensure HIPAA compliance and data security
- Create an intuitive, easy-to-use interface

---

## 2. Development Approach

### Why NOT Build All Modules at Once? ❌

**Problem with building everything:**
1. **Takes too long** (12-18 months)
   - Team gets exhausted
   - Market changes during development
   - Technology becomes outdated

2. **Too risky** ($1M+ investment)
   - What if users don't like it?
   - What if we built wrong features?
   - Hard to change direction later

3. **Too complex to manage**
   - More bugs to fix
   - Harder to test
   - Difficult to coordinate team

4. **No feedback until the end**
   - Can't learn from real users
   - Might build features nobody wants
   - Wasted development time

**Real-world example:**
Imagine building a house. You wouldn't build all rooms, pool, garden, and garage at once. You'd build the essential rooms first (bedroom, bathroom, kitchen), move in, then add more rooms based on what you actually need.

---

### Why MVP (Minimum Viable Product) Approach? ✅

**MVP = Build the smallest version that works**

**Benefits:**
1. **Launch faster** (3-4 months instead of 18 months)
2. **Lower cost** ($400K instead of $1M+)
3. **Get real user feedback** early
4. **Prove the concept** before investing more
5. **Start earning revenue** sooner
6. **Easier to manage** with smaller team

**MVP Strategy:**
```
Build → Launch → Learn → Improve → Repeat
  ↓        ↓        ↓        ↓        ↓
3 months  Test   Feedback  Add     Next
         users            features version
```

**What to include in MVP:**
- ✅ Patient registration
- ✅ Insurance verification
- ✅ Basic appointment scheduling
- ✅ Medical coding
- ✅ Claim creation and submission
- ✅ Payment posting
- ✅ Basic reports

**What to add AFTER MVP:**
- ❌ Advanced analytics
- ❌ Patient portal
- ❌ Mobile app
- ❌ Revenue integrity
- ❌ Advanced AI features

---

### How to Divide Development into Phases

**Phase-by-Phase Approach:**

```
Phase 1: Foundation (Weeks 1-6)
├── Setup infrastructure
├── Build authentication
├── Patient registration
└── Insurance verification

Phase 2: Clinical & Billing (Weeks 7-12)
├── Medical coding
├── Claim creation
├── Claim submission
└── AI integration

Phase 3: Payment & Denials (Weeks 13-16)
├── Payment posting
├── Denial management
└── Patient billing

Phase 4: Reports & Launch (Weeks 17-20)
├── Reports and dashboards
├── Testing
├── Deployment
└── Training
```

**Why this order?**
1. **Foundation first** - Can't build anything without login and database
2. **Core workflow next** - Patient → Claim → Payment is the main flow
3. **Money features** - Payment and denials directly impact revenue
4. **Polish last** - Reports and analytics help monitor performance

**Think of it like building a car:**
- Phase 1: Engine, wheels, steering (must have to move)
- Phase 2: Body, seats, windows (makes it usable)
- Phase 3: Fuel system, brakes (makes it safe)
- Phase 4: Radio, AC, paint (makes it nice)

---

## 3. Phase 1 — Foundation Setup (Weeks 1-6)

**Goal:** Set up the project infrastructure and build the first working modules

**What we'll build:**
- Project setup (React, FastAPI, PostgreSQL)
- User authentication (login/logout)
- Patient registration
- Insurance verification
- Basic appointment scheduling

**Why start here?**
- These are the foundation for everything else
- Can't submit claims without patients
- Can't bill without insurance verification
- Need authentication to secure the system

---

### A. Requirement Understanding (Week 1)

Before writing any code, the team must understand how healthcare billing works.

#### 1. Hospital Workflow Understanding

**What happens when a patient visits a hospital:**

```
Step 1: Patient arrives at front desk
   ↓
Step 2: Front desk registers patient (name, insurance, etc.)
   ↓
Step 3: Front desk verifies insurance (is it active?)
   ↓
Step 4: Front desk collects copay ($25)
   ↓
Step 5: Patient sees doctor
   ↓
Step 6: Doctor documents visit (diagnosis, treatment)
   ↓
Step 7: Medical coder assigns codes (ICD-10, CPT)
   ↓
Step 8: Biller creates claim
   ↓
Step 9: Claim submitted to insurance
   ↓
Step 10: Insurance pays (or denies)
   ↓
Step 11: Payment posted to account
   ↓
Step 12: Patient billed for remaining balance
```

**Key roles to understand:**
- **Front Desk:** First point of contact, registers patients
- **Doctor:** Provides medical care, documents visit
- **Medical Coder:** Translates doctor's notes into billing codes
- **Biller:** Creates and submits claims to insurance
- **AR Manager:** Tracks payments and follows up on unpaid claims

**Team Activity:**
- Watch YouTube videos on "healthcare revenue cycle"
- Read articles on medical billing basics
- Interview a medical biller (if possible)
- Create a flowchart of the entire process

---

#### 2. Billing Workflow Understanding

**How billing works (simplified):**

**Example: John Doe visits for flu**

1. **Service provided:**
   - Doctor diagnoses: Influenza (flu)
   - Doctor prescribes: Antiviral medication
   - Visit type: Office visit, 20 minutes

2. **Medical coding:**
   - Diagnosis code: J11.1 (Influenza with respiratory symptoms)
   - Procedure code: 99213 (Office visit, moderate complexity)
   - Charge: $150

3. **Claim creation:**
   - Patient: John Doe
   - Insurance: Blue Cross Blue Shield
   - Service date: May 20, 2026
   - Diagnosis: J11.1
   - Procedure: 99213
   - Charge: $150

4. **Claim submission:**
   - Sent electronically to insurance company
   - Format: EDI 837 (electronic claim format)

5. **Insurance payment:**
   - Insurance pays: $120 (contracted rate)
   - Patient owes: $25 (copay, already collected)
   - Write-off: $30 (contractual adjustment)

**Key concepts to understand:**
- **ICD-10 codes:** Diagnosis codes (what's wrong with patient)
- **CPT codes:** Procedure codes (what doctor did)
- **EDI 837:** Electronic claim format
- **EDI 835:** Electronic payment format (ERA)
- **Copay:** Fixed amount patient pays
- **Deductible:** Amount patient pays before insurance kicks in
- **Coinsurance:** Percentage patient pays (e.g., 20%)

---

#### 3. Insurance Workflow Understanding

**How insurance verification works:**

**Before patient visit:**
```
Hospital → Sends eligibility inquiry (EDI 270)
              ↓
         Insurance Company
              ↓
Hospital ← Receives eligibility response (EDI 271)
```

**What we check:**
- Is insurance active?
- What's the copay amount?
- How much deductible is left?
- Is prior authorization needed?
- Is provider in-network?

**Why it's critical:**
- If insurance is inactive → Patient becomes self-pay
- If we don't collect copay → Lost revenue
- If prior auth needed but not obtained → Claim denied (100%)

**Real example:**
```
Patient: Sarah Johnson
Insurance: Aetna
Policy: ABC123456789

Verification Result:
✅ Status: Active
✅ Copay: $25
✅ Deductible: $1,500 annual
   - Met: $800
   - Remaining: $700
✅ Prior Auth: Not required for office visit
```

---

#### 4. Claim Lifecycle Understanding

**What happens to a claim after submission:**

```
Day 0: Claim submitted
   ↓
Day 1: Acknowledgment received (claim accepted by clearinghouse)
   ↓
Day 3-7: Insurance reviews claim
   ↓
Day 7-14: Insurance adjudicates (decides to pay or deny)
   ↓
Day 14-21: Payment sent (if approved)
   ↓
Day 21-30: Payment posted to account
```

**Possible outcomes:**
1. **Paid in full** ✅
   - Insurance pays agreed amount
   - Patient portion collected
   - Claim closed

2. **Partially paid** ⚠️
   - Insurance pays less than expected
   - Need to investigate why
   - May need to appeal

3. **Denied** ❌
   - Insurance rejects claim
   - Reason code provided
   - Need to fix and resubmit or appeal

**Common denial reasons:**
- Missing information (30%)
- Incorrect coding (25%)
- Eligibility issues (20%)
- Prior authorization missing (15%)
- Timely filing (10%)

**Team Activity:**
- Study sample claims (CMS-1500 form)
- Learn common denial codes
- Understand appeal process

---

### B. Documentation Preparation (Week 1-2)

Before coding, create these documents:

#### 1. SRS Document (Software Requirements Specification)

**What it contains:**
- List of all features
- User roles and permissions
- Business rules
- Success criteria

**Example section:**
```
Feature: Patient Registration

Description:
Front desk staff should be able to register new patients and 
store their demographic and insurance information.

Requirements:
1. Capture patient name, DOB, gender, SSN
2. Capture address, phone, email
3. Capture insurance information (primary, secondary)
4. Validate required fields
5. Check for duplicate patients
6. Generate unique patient ID

Acceptance Criteria:
- Registration completes in <3 minutes
- No duplicate patients created
- All required fields validated
- Insurance card can be scanned (OCR)
```

**Who creates it:** Business Analyst + Technical Lead  
**Time needed:** 1 week

---

#### 2. API Document

**What it contains:**
- List of all API endpoints
- Request/response formats
- Authentication requirements
- Error codes

**Example:**
```
POST /api/v1/patients
Description: Create new patient

Request:
{
  "firstName": "John",
  "lastName": "Doe",
  "dob": "1980-05-15",
  "gender": "M",
  "ssn": "123-45-6789",
  "phone": "(555) 123-4567",
  "email": "john@email.com",
  "insurance": {
    "payerName": "Blue Cross",
    "policyNumber": "ABC123456789",
    "groupNumber": "GRP5000"
  }
}

Response (Success):
{
  "patientId": "PAT-2026-001",
  "message": "Patient created successfully"
}

Response (Error):
{
  "error": "Duplicate patient found",
  "existingPatientId": "PAT-2026-000"
}
```

**Who creates it:** Backend Developer + Technical Lead  
**Time needed:** 3-4 days

---

#### 3. Database Design Document

**What it contains:**
- All database tables
- Table relationships
- Field definitions
- Indexes and constraints

**Example table:**
```sql
Table: patients

Columns:
- patient_id (VARCHAR, PRIMARY KEY) - Unique patient identifier
- first_name (VARCHAR, NOT NULL) - Patient first name
- last_name (VARCHAR, NOT NULL) - Patient last name
- dob (DATE, NOT NULL) - Date of birth
- gender (CHAR, NOT NULL) - M/F/O
- ssn (VARCHAR, ENCRYPTED) - Social security number
- phone (VARCHAR) - Phone number
- email (VARCHAR) - Email address
- created_at (TIMESTAMP) - Record creation time
- updated_at (TIMESTAMP) - Last update time
- created_by (VARCHAR) - User who created record

Indexes:
- idx_patient_name (first_name, last_name)
- idx_patient_dob (dob)
- idx_patient_ssn (ssn)

Relationships:
- Has many: patient_insurance (one patient, multiple insurances)
- Has many: encounters (one patient, multiple visits)
- Has many: claims (one patient, multiple claims)
```

**Total tables needed:** 35-40 tables  
**Who creates it:** Database Architect + Backend Developer  
**Time needed:** 1 week

---

#### 4. Screen Flow Document

**What it contains:**
- Wireframes for all screens
- User navigation flow
- Button actions
- Form validations

**Example flow:**
```
Login Screen
   ↓ (successful login)
Dashboard
   ↓ (click "New Patient")
Patient Registration Form
   ↓ (fill form, click "Save")
Patient Details Screen
   ↓ (click "Verify Insurance")
Insurance Verification Results
   ↓ (click "Schedule Appointment")
Appointment Scheduler
```

**Tools to use:**
- Figma (for wireframes)
- Draw.io (for flowcharts)
- Miro (for collaboration)

**Who creates it:** UI/UX Designer + Frontend Developer  
**Time needed:** 1 week

---

#### 5. Module Document

**What it contains:**
- List of all modules
- Module dependencies
- Development priority
- Integration points

**Example:**
```
Module: Patient Registration

Priority: High (Phase 1)

Dependencies:
- User Authentication (must be built first)
- Database setup (must be ready)

Sub-features:
1. Patient demographics form
2. Insurance information form
3. Emergency contact form
4. Duplicate patient check
5. OCR for insurance card scanning

Integration Points:
- OCR API (AWS Textract)
- Master Patient Index (MPI)

Estimated Time: 1 week
```

**Who creates it:** Technical Lead  
**Time needed:** 2-3 days

---

### C. System Architecture (Week 2)

#### 1. Frontend Architecture

**Technology Stack:**
- **Framework:** React.js 18+
- **Language:** TypeScript (for type safety)
- **Styling:** Tailwind CSS
- **State Management:** React Query (for API calls) + Context API
- **Routing:** React Router v6
- **Forms:** React Hook Form
- **Charts:** Chart.js
- **Icons:** Lucide React

**Folder Structure:**
```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/          # Reusable components
│   │   ├── common/         # Buttons, inputs, modals
│   │   ├── layout/         # Header, sidebar, footer
│   │   └── forms/          # Form components
│   ├── pages/              # Page components
│   │   ├── Login.tsx
│   │   ├── Dashboard.tsx
│   │   ├── PatientRegistration.tsx
│   │   └── ...
│   ├── services/           # API calls
│   │   ├── api.ts          # Axios configuration
│   │   ├── authService.ts
│   │   ├── patientService.ts
│   │   └── ...
│   ├── hooks/              # Custom React hooks
│   ├── utils/              # Utility functions
│   ├── types/              # TypeScript types
│   ├── context/            # React Context
│   ├── App.tsx             # Main app component
│   └── index.tsx           # Entry point
├── package.json
└── tailwind.config.js
```

**Why this structure?**
- **Organized:** Easy to find files
- **Scalable:** Can add more features easily
- **Maintainable:** Clear separation of concerns
- **Team-friendly:** Multiple developers can work without conflicts

---

#### 2. Backend Architecture

**Technology Stack:**
- **Framework:** Python FastAPI
- **ORM:** SQLAlchemy 2.0
- **Database:** PostgreSQL 15
- **Authentication:** JWT tokens
- **Validation:** Pydantic models
- **Background Tasks:** Celery + Redis
- **API Documentation:** Swagger UI (built-in)

**Folder Structure:**
```
backend/
├── app/
│   ├── api/                # API endpoints
│   │   ├── v1/
│   │   │   ├── auth.py     # Login, logout
│   │   │   ├── patients.py # Patient CRUD
│   │   │   ├── claims.py   # Claim operations
│   │   │   └── ...
│   ├── core/               # Core functionality
│   │   ├── config.py       # Configuration
│   │   ├── security.py     # JWT, password hashing
│   │   └── database.py     # Database connection
│   ├── models/             # Database models
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── claim.py
│   │   └── ...
│   ├── schemas/            # Pydantic schemas
│   │   ├── user.py
│   │   ├── patient.py
│   │   └── ...
│   ├── services/           # Business logic
│   │   ├── auth_service.py
│   │   ├── patient_service.py
│   │   └── ...
│   ├── utils/              # Utility functions
│   │   ├── validators.py
│   │   ├── formatters.py
│   │   └── ...
│   └── main.py             # FastAPI app
├── tests/                  # Test files
├── alembic/                # Database migrations
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables
```

**API Structure:**
```
/api/v1/auth/login          POST   - User login
/api/v1/auth/logout         POST   - User logout
/api/v1/patients            POST   - Create patient
/api/v1/patients/{id}       GET    - Get patient
/api/v1/patients/{id}       PUT    - Update patient
/api/v1/patients/search     GET    - Search patients
/api/v1/eligibility/verify  POST   - Verify insurance
/api/v1/claims              POST   - Create claim
/api/v1/claims/{id}         GET    - Get claim
/api/v1/claims/submit       POST   - Submit claim
...
```

---

#### 3. Database Architecture

**Database:** PostgreSQL 15

**Why PostgreSQL?**
- Reliable and proven (30+ years)
- Handles complex relationships well
- ACID compliant (data integrity)
- JSON support (flexible data)
- Free and open-source

**Core Tables (Phase 1):**

```sql
-- Users and Authentication
users
user_roles
user_sessions

-- Patients
patients
patient_insurance
patient_contacts
patient_addresses

-- Providers
providers
provider_credentials

-- Appointments
appointments
appointment_types

-- Insurance
insurance_payers
insurance_plans
eligibility_checks

-- Audit
audit_logs
```

**Database Design Principles:**
1. **Normalization:** Avoid data duplication
2. **Indexes:** Fast queries on frequently searched columns
3. **Constraints:** Enforce data integrity
4. **Encryption:** Sensitive data (SSN, DOB) encrypted
5. **Audit trail:** Track all changes

---

#### 4. Security Architecture

**Security Layers:**

1. **Network Security:**
   - HTTPS only (TLS 1.2+)
   - Firewall rules (AWS Security Groups)
   - VPC (Virtual Private Cloud)

2. **Authentication:**
   - JWT tokens (8-hour expiration)
   - Password hashing (bcrypt)
   - Multi-factor authentication (optional)

3. **Authorization:**
   - Role-based access control (RBAC)
   - Permission checks on every API call
   - Row-level security (users see only their data)

4. **Data Security:**
   - Encryption at rest (AES-256)
   - Encryption in transit (TLS)
   - Encrypted database columns (SSN, DOB)

5. **HIPAA Compliance:**
   - Audit logging (all actions logged)
   - Access controls (who can see what)
   - Data retention (7 years)
   - Breach notification procedures

**Security Checklist:**
- ✅ No passwords in code (use environment variables)
- ✅ SQL injection prevention (use ORM)
- ✅ XSS prevention (sanitize inputs)
- ✅ CSRF protection (CSRF tokens)
- ✅ Rate limiting (prevent abuse)
- ✅ Session timeout (15 minutes)

---

### D. Project Setup (Week 2-3)

#### Frontend Setup (React.js)

**Step 1: Create React App**
```bash
# Create new React app with TypeScript
npx create-react-app rcm-frontend --template typescript

# Navigate to project
cd rcm-frontend

# Install dependencies
npm install react-router-dom react-query axios
npm install -D tailwindcss postcss autoprefixer
npm install react-hook-form lucide-react chart.js
```

**Step 2: Configure Tailwind CSS**
```bash
# Initialize Tailwind
npx tailwindcss init -p
```

**tailwind.config.js:**
```javascript
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#10B981',
        danger: '#EF4444',
      }
    },
  },
  plugins: [],
}
```

**Step 3: Setup Routing**
```typescript
// src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import PatientRegistration from './pages/PatientRegistration';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/patients/new" element={<PatientRegistration />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

**Step 4: Setup API Service**
```typescript
// src/services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add JWT token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

---

#### Backend Setup (Python FastAPI)

**Step 1: Create Project Structure**
```bash
# Create project folder
mkdir rcm-backend
cd rcm-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Create folder structure
mkdir -p app/api/v1 app/core app/models app/schemas app/services
touch app/__init__.py app/main.py
```

**Step 2: Install Dependencies**
```bash
# Create requirements.txt
cat > requirements.txt << EOF
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
alembic==1.12.1
redis==5.0.1
celery==5.3.4
EOF

# Install dependencies
pip install -r requirements.txt
```

**Step 3: Create FastAPI App**
```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, patients

app = FastAPI(
    title="Healthcare RCM API",
    description="Revenue Cycle Management System",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(patients.router, prefix="/api/v1/patients", tags=["patients"])

@app.get("/")
def read_root():
    return {"message": "Healthcare RCM API is running"}
```

**Step 4: Database Configuration**
```python
# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/rcm_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency for API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Step 5: Run the Application**
```bash
# Run FastAPI server
uvicorn app.main:app --reload --port 8000

# API documentation available at:
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

---

#### Database Setup (PostgreSQL)

**Step 1: Install PostgreSQL**
```bash
# On Mac
brew install postgresql@15

# On Ubuntu
sudo apt-get install postgresql-15

# On Windows
# Download installer from postgresql.org
```

**Step 2: Create Database**
```bash
# Start PostgreSQL
brew services start postgresql@15  # Mac

# Create database
psql postgres
CREATE DATABASE rcm_db;
CREATE USER rcm_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE rcm_db TO rcm_user;
\q
```

**Step 3: Create Initial Tables**
```python
# app/models/user.py
from sqlalchemy import Column, String, Boolean, DateTime
from app.core.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(String(50), primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200))
    role = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**Step 4: Run Migrations**
```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Create users table"

# Run migration
alembic upgrade head
```

---

### E. Authentication & Security (Week 3)

#### 1. User Login System

**What we're building:**
- Login page (username + password)
- JWT token generation
- Token storage in browser
- Protected routes (require login)
- Logout functionality

**Backend: Login API**
```python
# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.models.user import User

router = APIRouter()

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Find user
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Verify password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Create JWT token
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "user_id": user.user_id,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role
        }
    }
```

**Security Module:**
```python
# app/core/security.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    """Create JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """Decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

**Frontend: Login Page**
```typescript
// src/pages/Login.tsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await api.post('/auth/login', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      // Store token
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));

      // Redirect to dashboard
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-center mb-6">
          Healthcare RCM Login
        </h2>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Username
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
```

---

#### 2. Role-Based Access Control (RBAC)

**User Roles:**
1. **Admin** - Full system access
2. **Front Desk** - Patient registration, appointments
3. **Medical Coder** - Coding and charge capture
4. **Biller** - Claim creation and submission
5. **AR Manager** - Payment posting, denials
6. **Finance Manager** - Reports and analytics

**Implementation:**
```python
# app/core/permissions.py
from fastapi import HTTPException, status
from functools import wraps

def require_role(*allowed_roles):
    """Decorator to check user role"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user=None, **kwargs):
            if current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# Usage in API:
@router.post("/patients")
@require_role("admin", "front_desk")
async def create_patient(
    patient_data: PatientCreate,
    current_user: User = Depends(get_current_user)
):
    # Only admin and front_desk can create patients
    ...
```

---

**Continue to Part 2 for remaining modules...**

---

**Document Navigation:**
- **Part 1:** Introduction & Phase 1 Foundation (This document)
- **Part 2:** Phase 1 Core Modules (Patient, Insurance, Appointments)
- **Part 3:** Phase 2 Clinical & Billing
- **Part 4:** Phase 3 Payment & Denials
- **Part 5:** Phase 4 Reports & Deployment
