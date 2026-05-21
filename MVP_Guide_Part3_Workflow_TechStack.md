# Healthcare RCM Application - MVP Guide (Part 3: Workflow & Tech Stack)

**Version:** 1.0  
**For:** Development Team & Technical Lead

---

## 4. MVP Workflow - Complete Step-by-Step Flow

### Real-Time Example: Patient "Sarah Johnson" Visit

Let me explain the complete workflow using a real example:

---

#### **Step 1: Patient Registration** 📝

**Scenario:** Sarah Johnson calls to book her first appointment.

**What Happens:**
1. Front desk staff opens the application
2. Clicks "New Patient"
3. Enters Sarah's information:
   - Name: Sarah Johnson
   - DOB: March 15, 1985 (41 years old)
   - Phone: (555) 123-4567
   - Email: sarah.j@email.com
   - Address: 123 Main St, Austin, TX 78701
   - Insurance: Blue Cross Blue Shield
   - Policy Number: ABC123456789
   - Group Number: GRP5000

4. System generates Patient ID: PAT-2026-5678
5. Patient record saved ✅

**Time Taken:** 2-3 minutes

---

#### **Step 2: Insurance Verification** 🔍

**What Happens:**
1. Staff clicks "Verify Insurance" button
2. System sends request to **Waystar API**:
   ```
   Patient: Sarah Johnson
   DOB: 03/15/1985
   Insurance: Blue Cross Blue Shield
   Policy: ABC123456789
   Service Date: May 20, 2026
   ```

3. Waystar sends EDI 270 to Blue Cross
4. Blue Cross responds with EDI 271 in 10 seconds
5. System displays results:
   ```
   ✅ Coverage Status: ACTIVE
   ✅ Copay: $25.00
   ✅ Deductible: $1,500 annual
      - Met: $800
      - Remaining: $700
   ✅ Out-of-Pocket Max: $5,000
      - Met: $1,200
      - Remaining: $3,800
   ✅ Network Status: IN-NETWORK
   ⚠️  Prior Auth: NOT REQUIRED for office visit
   ```

6. Staff notes: "Collect $25 copay at check-in"

**Time Taken:** 30 seconds

---

#### **Step 3: Appointment Scheduling** 📅

**What Happens:**
1. Staff opens calendar
2. Selects date: May 20, 2026, 10:00 AM
3. Selects provider: Dr. Smith
4. Selects appointment type: "New Patient Office Visit"
5. Adds note: "Patient has cough and fever"
6. System creates appointment ✅
7. System sends SMS reminder via **Twilio API** (optional):
   ```
   "Hi Sarah, your appointment with Dr. Smith is on 
   May 20 at 10:00 AM. Please bring your insurance card. 
   Reply CONFIRM to confirm."
   ```

**Time Taken:** 1 minute

---

#### **Step 4: Patient Check-In (Day of Visit)** ✅

**What Happens:**
1. Sarah arrives at 9:50 AM
2. Front desk checks her in
3. Collects $25 copay (credit card via **Stripe API**)
4. System creates encounter record:
   ```
   Encounter ID: ENC-2026-9876
   Patient: Sarah Johnson (PAT-2026-5678)
   Provider: Dr. Smith
   Date: May 20, 2026
   Time: 10:00 AM
   Type: Office Visit
   Status: Checked In
   ```

**Time Taken:** 2 minutes

---

#### **Step 5: Doctor Documentation** 👨‍⚕️

**What Happens:**
1. Dr. Smith sees Sarah at 10:00 AM
2. Examines patient
3. Diagnosis: Acute bronchitis
4. Treatment: Prescribed antibiotics
5. Dr. Smith documents in EHR:
   ```
   Chief Complaint: Cough and fever for 5 days
   
   History: 41-year-old female presents with productive 
   cough, yellow sputum, fever (101°F), chest discomfort. 
   No shortness of breath.
   
   Examination:
   - Lungs: Rhonchi in both lower lobes
   - No wheezing
   - O2 saturation: 98%
   
   Assessment: Acute bronchitis (J20.9)
   
   Plan:
   - Azithromycin 500mg daily x 5 days
   - Increase fluids
   - Follow up if symptoms worsen
   ```

6. Visit ends at 10:20 AM

**Time Taken:** 20 minutes

---

#### **Step 6: Medical Coding** 🏥

**What Happens:**
1. Medical coder opens encounter ENC-2026-9876
2. Reviews Dr. Smith's notes
3. **AI-Assisted Coding** (using **OpenAI API**):
   - System analyzes notes
   - Suggests codes:
     ```
     Suggested ICD-10:
     ✅ J20.9 - Acute bronchitis, unspecified (95% confidence)
     ✅ R05 - Cough (88% confidence)
     ✅ R50.9 - Fever, unspecified (85% confidence)
     
     Suggested CPT:
     ✅ 99203 - New patient office visit, moderate complexity
     ```

4. Coder reviews and confirms:
   - **ICD-10 Codes:**
     - J20.9 (Primary diagnosis)
     - R05 (Secondary)
     - R50.9 (Secondary)
   - **CPT Code:**
     - 99203 (Office visit, 30-44 minutes)
   - **Charge:** $150.00

5. Codes saved to encounter ✅

**Time Taken:** 3 minutes (with AI assistance)  
**Without AI:** 10-15 minutes

---

#### **Step 7: Claim Scrubbing** ✅

**What Happens:**
1. System automatically prepares claim for validation
2. Claim data pulled from patient encounter:
   ```
   Patient: Sarah Johnson
   Encounter ID: ENC-2026-9876
   Insurance: Blue Cross Blue Shield
   CPT Code: 99203
   ICD-10 Codes:
   - J20.9 (Acute bronchitis)
   - R05 (Cough)
   - R50.9 (Fever)
   Charge Amount: $150.00
   ```

3. System runs automated claim scrubbing checks:
   - Validates ICD-10 diagnosis codes
   - Validates CPT procedure code
   - Checks insurance eligibility
   - Verifies provider NPI number
   - Validates patient demographics
   - Checks required modifiers
   - Detects duplicate claims
   - Confirms medical necessity

4. **Waystar API** performs advanced validation:
   ```
   ✅ 47 validation rules passed
   ✅ Code compatibility verified
   ✅ Insurance coverage verified
   ✅ Required fields completed
   ✅ No duplicate claims found
   ```

5. System displays result:
   ```
   ✅ Claim Status: READY TO SUBMIT
   Claim ID: CLM-2026-001234
   ```

6. Claim moved to submission queue automatically

**Time Taken:** 1 minute

---

#### **Step 8: Claim Submission** 📤

**What Happens:**
1. Biller selects claim CLM-2026-001234
2. Clicks "Submit Claim"
3. System converts to EDI 837 format
4. Sends to **Waystar API**
5. Waystar forwards to Blue Cross Blue Shield
6. Receives acknowledgment (EDI 999):
   ```
   Status: ACCEPTED
   Tracking Number: TRK-987654321
   Submission Date: 05/20/2026 11:30 AM
   ```

7. Claim status updated: "Submitted" ✅

**Time Taken:** 30 seconds

---

#### **Step 9: Claim Status Tracking** 🔄

**What Happens:**
1. System automatically monitors submitted claim:
   ```
   Claim ID: CLM-2026-001234
   Patient: Sarah Johnson
   Insurance: Blue Cross Blue Shield
   Submission Date: 05/20/2026
   ```

2. System sends automated EDI 276 claim status inquiry to payer every 3 days

3. Insurance payer responds with EDI 277 status updates

4. Claim tracking updates displayed in dashboard:
   ```
   Day 3:
   Status: RECEIVED
   Message: Claim received successfully by payer
   ```

   ```
   Day 5:
   Status: IN REVIEW
   Message: Claim under medical review
   ```

   ```
   Day 7:
   Status: APPROVED – PAYMENT PENDING
   Expected Payment: $120.00
   ```

5. Billing team receives automatic notifications for status changes

6. System updates claim timeline and tracking history automatically

**Behind the Scenes:**
- EDI 276 inquiry sent to payer
- EDI 277 response received from payer
- Claim status updated in real-time dashboard
- Alerts generated for delayed or denied claims

**Time Taken:** Automatic background process

---

#### **Step 10: Payment Posting** 💰

**What Happens:**
1. On May 25, system receives ERA (EDI 835) from **Waystar API**
2. System parses ERA:
   ```
   Claim: CLM-2026-001234
   Patient: Sarah Johnson
   Service Date: 05/20/2026
   
   Billed Amount: $150.00
   Allowed Amount: $120.00 (contracted rate)
   Insurance Paid: $95.00 (80% after copay)
   Patient Copay: $25.00 (already collected)
   Contractual Adjustment: -$30.00
   
   Adjustment Codes:
   - CO-45: Charge exceeds fee schedule (-$30.00)
   - PR-3: Copay amount ($25.00)
   
   Total Paid: $95.00
   Patient Balance: $0.00 (copay already collected)
   ```

3. System auto-matches payment to claim
4. Biller reviews and posts payment
5. Claim status: "PAID" ✅
6. Updates accounts receivable

**Time Taken:** 1 minute

---

#### **Step 11: Patient Billing** 💳

**What Happens:**
1. System generates patient statement for remaining balance:
   ```
   Patient: Sarah Johnson
   Claim ID: CLM-2026-001234
   
   Total Charges: $150.00
   Insurance Paid: $120.00
   Copay Collected: $0.00
   
   Remaining Patient Balance: $30.00
   Due Date: June 05, 2026
   ```

2. System emails statement and payment link to Sarah:
   ```
   Subject: Patient Statement Available
   
   Dear Sarah Johnson,
   
   Your remaining balance of $30.00 is now available.
   Please use the secure payment link below to complete payment.
   
   [Pay Now]
   ```

3. Sarah logs into patient portal
4. Pays balance online using credit card via **Stripe API**
5. System confirms successful payment:
   ```
   Payment Status: SUCCESS
   Amount Paid: $30.00
   Transaction ID: TXN-2026-456789
   ```

6. Receipt emailed automatically to Sarah
7. Account status updated:
   ```
   Claim Status: PAID IN FULL ✅
   Patient Balance: $0.00
   ```

**Behind the Scenes:**
- Statement generated automatically
- Email notification sent
- Payment processed securely via Stripe
- Receipt generated and emailed
- Patient ledger updated in real time
- Account marked as fully paid

**Time Taken:** 1 minute for online payment

---

### **Complete Timeline Summary**

| Date | Event | Status |
|------|-------|--------|
| May 18 | Patient registration | ✅ Patient ID generated |
| May 18 | Insurance verification | ✅ Active coverage verified |
| May 18 | Appointment scheduled | ✅ May 20, 10:00 AM with Dr. Smith |
| May 20 | Patient check-in | ✅ $25 copay collected |
| May 20 | Doctor consultation | ✅ Acute bronchitis diagnosed |
| May 20 | Medical coding with AI | ✅ ICD-10 & CPT codes assigned |
| May 20 | Claim scrubbing | ✅ 47 validation checks passed |
| May 20 | Claim submitted | ✅ Accepted by payer |
| May 25 | Payment posting | ✅ ERA processed & payment posted |
| May 26 | Patient billing generated | ✅ Statement emailed |
| May 27 | Final patient payment received | ✅ Paid in Full |

**Total Days from Service to Final Payment:** 11 days ⚡  
**Traditional Industry Average:** 60–90 days

**Total Revenue Collected:** $150.00 ($120 insurance + $30 patient payment)  
**Write-off (Contractual):** $30.00  
**Net Collection Rate:** 100% ✅

---

## 5. Recommended Tech Stack for MVP

### Frontend Technologies

#### **React.js** ⚛️

**Why React.js?**

1. **Fast Development**
   - Component-based architecture
   - Reusable UI components
   - Large ecosystem of libraries

2. **Great for Healthcare Apps**
   - Handles complex forms easily
   - Real-time updates (claim status, payments)
   - Excellent performance

3. **Strong Community**
   - 200,000+ npm packages
   - Easy to find developers
   - Lots of tutorials and support

4. **Modern Features**
   - React Hooks for state management
   - React Query for API calls
   - React Router for navigation

**Example React Component:**
```jsx
// Patient Registration Form Component
import React, { useState } from 'react';

function PatientRegistration() {
  const [patient, setPatient] = useState({
    firstName: '',
    lastName: '',
    dob: '',
    insurance: ''
  });

  const handleSubmit = async () => {
    const response = await fetch('/api/v1/patients', {
      method: 'POST',
      body: JSON.stringify(patient)
    });
    // Handle response
  };

  return (
    <form onSubmit={handleSubmit}>
      <input 
        placeholder="First Name"
        value={patient.firstName}
        onChange={(e) => setPatient({...patient, firstName: e.target.value})}
      />
      {/* More fields */}
      <button type="submit">Save Patient</button>
    </form>
  );
}
```

---

#### **Tailwind CSS** 🎨

**Why Tailwind CSS?**

1. **Rapid UI Development**
   - Utility-first CSS framework
   - No need to write custom CSS
   - Build UI in minutes, not hours

2. **Consistent Design**
   - Pre-defined spacing, colors, fonts
   - Responsive by default
   - Professional look out of the box

3. **Small Bundle Size**
   - Only includes CSS you actually use
   - Faster page loads
   - Better performance

4. **Easy to Customize**
   - Configure colors, fonts, spacing
   - Add custom utilities
   - Matches any brand

**Example Tailwind Usage:**
```jsx
// Beautiful form with Tailwind
<div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg">
  <h2 className="text-2xl font-bold text-gray-800 mb-4">
    Patient Registration
  </h2>
  
  <input 
    className="w-full px-4 py-2 border border-gray-300 rounded-lg 
               focus:ring-2 focus:ring-blue-500 focus:border-transparent"
    placeholder="First Name"
  />
  
  <button className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg 
                     hover:bg-blue-700 transition-colors">
    Save Patient
  </button>
</div>
```

**Result:** Professional, modern UI without writing CSS files!

---

### Backend Technologies

#### **Python FastAPI** 🚀

**Why FastAPI?**

1. **Extremely Fast**
   - Built on Starlette and Pydantic
   - Performance comparable to Node.js and Go
   - Async support for concurrent requests

2. **Easy to Learn**
   - Simple, clean syntax
   - Automatic API documentation (Swagger UI)
   - Type hints for better code quality

3. **Perfect for Healthcare**
   - Great for data processing (claims, ERA parsing)
   - Easy integration with ML/AI libraries
   - Strong data validation

4. **Built-in Features**
   - Automatic request validation
   - OAuth2 authentication
   - WebSocket support
   - Background tasks

**Example FastAPI Endpoint:**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date

app = FastAPI()

class Patient(BaseModel):
    first_name: str
    last_name: str
    dob: date
    insurance_policy: str

@app.post("/api/v1/patients")
async def create_patient(patient: Patient):
    # Validate patient data (automatic)
    # Save to database
    patient_id = save_to_db(patient)
    
    return {
        "patient_id": patient_id,
        "message": "Patient created successfully"
    }

@app.get("/api/v1/patients/{patient_id}")
async def get_patient(patient_id: str):
    patient = get_from_db(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
```

**Automatic API Documentation:**
- Visit `http://localhost:8000/docs` → Interactive Swagger UI
- Test APIs directly in browser
- No extra work needed!

---

### Database

#### **PostgreSQL** 🐘

**Why PostgreSQL?**

1. **Reliable & Proven**
   - 30+ years of development
   - Used by Apple, Instagram, Spotify
   - ACID compliant (data integrity guaranteed)

2. **Perfect for Healthcare Data**
   - Handles complex relationships (patients, claims, payments)
   - JSON support for flexible data
   - Full-text search for patient records

3. **Scalable**
   - Handles millions of records
   - Supports partitioning for large tables
   - Replication for high availability

4. **Advanced Features**
   - Foreign keys and constraints
   - Triggers for business rules
   - Views for complex queries
   - Excellent performance

**Example Database Schema:**
```sql
-- Patients table
CREATE TABLE patients (
    patient_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    ssn VARCHAR(11) ENCRYPTED,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Claims table
CREATE TABLE claims (
    claim_id VARCHAR(50) PRIMARY KEY,
    patient_id VARCHAR(50) REFERENCES patients(patient_id),
    service_date DATE NOT NULL,
    billed_amount DECIMAL(10,2),
    paid_amount DECIMAL(10,2),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index for fast lookups
CREATE INDEX idx_claims_patient ON claims(patient_id);
CREATE INDEX idx_claims_status ON claims(status);
```

---

### Cloud Platform

#### **AWS (Amazon Web Services)** ☁️

**Why AWS?**

1. **Industry Leader**
   - Most mature cloud platform
   - Used by Netflix, Airbnb, NASA
   - 200+ services available

2. **HIPAA Compliant**
   - BAA (Business Associate Agreement) available
   - Encryption at rest and in transit
   - Audit logging with CloudTrail
   - Perfect for healthcare data

3. **Cost-Effective for MVP**
   - Free tier for 12 months
   - Pay only for what you use
   - Start small, scale later

4. **Services We'll Use:**
   - **EC2:** Virtual servers for backend
   - **RDS:** Managed PostgreSQL database
   - **S3:** Store documents, images
   - **CloudFront:** Fast content delivery
   - **Lambda:** Serverless functions for background tasks
   - **API Gateway:** API management
   - **Cognito:** User authentication (optional)

**MVP AWS Architecture:**
```
Internet
   ↓
CloudFront (CDN)
   ↓
Load Balancer
   ↓
EC2 Instances (FastAPI backend)
   ↓
RDS PostgreSQL (Database)
   ↓
S3 (Document storage)
```

**Estimated Monthly Cost for MVP:**
- EC2 (t3.medium): $30
- RDS PostgreSQL (db.t3.small): $25
- S3 Storage (100 GB): $2
- CloudFront: $5
- **Total: ~$62/month** 💰

---

### Why This Stack is Perfect for MVP

| Requirement | Solution | Benefit |
|-------------|----------|---------|
| **Fast Development** | React + Tailwind | Build UI in days, not weeks |
| **High Performance** | FastAPI + PostgreSQL | Handle 1000+ requests/sec |
| **Scalability** | AWS | Scale from 10 to 10,000 users |
| **Security** | AWS + PostgreSQL | HIPAA compliant |
| **Cost** | All open-source + AWS free tier | < $100/month for MVP |
| **Developer Availability** | Popular technologies | Easy to hire developers |
| **AI Integration** | Python ecosystem | Easy to add OpenAI, ML models |

---

**Next:** Part 4 will cover Third-Party APIs and AI Integration details.

---

**Document Navigation:**
- **Part 1:** Introduction & Goals
- **Part 2:** Modules & Features
- **Part 3:** Workflow & Tech Stack (This document)
- **Part 4:** APIs & AI Integration
- **Part 5:** Development Plan & Timeline
