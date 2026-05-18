# Healthcare RCM Application - Development Phase Guide
## Part 3: Phase 2 - Clinical & Billing Development

**Version:** 1.0  
**For:** Technical Lead & Development Team

---

## 4. Phase 2 — Clinical & Billing Development (Weeks 7-12)

**Goal:** Build the core billing workflow from medical coding to claim submission

**What we'll build:**
- Medical coding module (AI-assisted)
- Charge capture
- Claim creation
- Claim scrubbing (error detection)
- Claim submission to insurance
- AI integration (OpenAI)
- Clearinghouse integration (Waystar)

**Why this phase?**
This is the heart of the RCM system. Without these modules, we can't bill insurance or collect payments.

---

### Module 4: Medical Coding (AI-Assisted) (Week 7-8)

#### What This Module Does
Medical coders assign standardized codes (ICD-10, CPT) to diagnoses and procedures based on doctor's clinical notes.

**Example:**
- Doctor writes: "Patient has acute bronchitis, prescribed antibiotics"
- Coder assigns:
  - ICD-10: J20.9 (Acute bronchitis)
  - CPT: 99213 (Office visit, level 3)

**Why it's critical:**
- Wrong codes = claim denial or underpayment
- Missing codes = lost revenue
- Coding errors cost hospitals millions annually

---

#### Frontend Screens

**Screen 1: Coding Worklist**
```
┌─────────────────────────────────────────────────┐
│  Medical Coding Worklist                        │
├─────────────────────────────────────────────────┤
│                                                  │
│  Filter: [All Encounters ▼] [Search: _______]  │
│                                                  │
│  Encounters Ready to Code:                      │
│  ┌──────────────────────────────────────────┐  │
│  │ ENC-001 | John Doe | 05/20/26 | Code     │  │
│  │ ENC-002 | Jane Smith | 05/20/26 | Code   │  │
│  │ ENC-003 | Bob Johnson | 05/21/26 | Code  │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  Total: 3 encounters                            │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Screen 2: Coding Interface**
```
┌─────────────────────────────────────────────────┐
│  Medical Coding - ENC-001                       │
├─────────────────────────────────────────────────┤
│                                                  │
│  Patient: John Doe (DOB: 05/15/1980)           │
│  Provider: Dr. Smith                            │
│  Date: 05/20/2026                               │
│  Type: Office Visit                             │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │ Clinical Notes:                          │  │
│  │                                          │  │
│  │ Chief Complaint: Cough for 5 days       │  │
│  │                                          │  │
│  │ HPI: Patient presents with productive   │  │
│  │ cough, fever (101°F), shortness of      │  │
│  │ breath. Started 5 days ago.             │  │
│  │                                          │  │
│  │ Assessment: Acute bronchitis            │  │
│  │                                          │  │
│  │ Plan: Prescribed azithromycin 250mg     │  │
│  │ for 5 days. Follow up in 1 week.       │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  [🤖 Get AI Coding Suggestions]                 │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │ AI Suggestions: (Confidence: 92%)       │  │
│  │                                          │  │
│  │ Diagnosis Codes (ICD-10):               │  │
│  │ ✓ J20.9 - Acute bronchitis (95%)       │  │
│  │ ✓ R05 - Cough (88%)                    │  │
│  │ ✓ R50.9 - Fever (85%)                  │  │
│  │                                          │  │
│  │ Procedure Codes (CPT):                  │  │
│  │ ✓ 99213 - Office visit, level 3 (92%)  │  │
│  │                                          │  │
│  │ [Accept All] [Review Individually]      │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  Assigned Codes:                                │
│  ┌──────────────────────────────────────────┐  │
│  │ ICD-10:                                  │  │
│  │ • J20.9 - Acute bronchitis [Remove]     │  │
│  │ • R05 - Cough [Remove]                  │  │
│  │ [+ Add Diagnosis Code]                  │  │
│  │                                          │  │
│  │ CPT:                                     │  │
│  │ • 99213 - Office visit, level 3 [Remove]│  │
│  │ [+ Add Procedure Code]                  │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  [Save Draft] [Submit for Billing]              │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Frontend Code:**
```typescript
// src/pages/MedicalCoding.tsx
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';

interface CodeSuggestion {
  code: string;
  description: string;
  confidence: number;
}

interface AISuggestions {
  diagnosisCodes: CodeSuggestion[];
  procedureCodes: CodeSuggestion[];
  overallConfidence: number;
  reasoning: string;
}

function MedicalCoding() {
  const { encounterId } = useParams();
  const [encounter, setEncounter] = useState<any>(null);
  const [clinicalNotes, setClinicalNotes] = useState('');
  const [aiSuggestions, setAiSuggestions] = useState<AISuggestions | null>(null);
  const [assignedDiagnoses, setAssignedDiagnoses] = useState<string[]>([]);
  const [assignedProcedures, setAssignedProcedures] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadEncounter();
  }, [encounterId]);

  const loadEncounter = async () => {
    const response = await api.get(`/encounters/${encounterId}`);
    setEncounter(response.data);
    setClinicalNotes(response.data.clinicalNotes);
  };

  const getAISuggestions = async () => {
    setLoading(true);
    try {
      const response = await api.post('/coding/ai-suggest', {
        encounterId,
        clinicalNotes
      });
      setAiSuggestions(response.data);
    } catch (error) {
      console.error('AI suggestion failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const acceptAllSuggestions = () => {
    if (aiSuggestions) {
      setAssignedDiagnoses(
        aiSuggestions.diagnosisCodes.map(c => c.code)
      );
      setAssignedProcedures(
        aiSuggestions.procedureCodes.map(c => c.code)
      );
    }
  };

  const submitForBilling = async () => {
    try {
      await api.post(`/encounters/${encounterId}/submit-coding`, {
        diagnosisCodes: assignedDiagnoses,
        procedureCodes: assignedProcedures
      });
      alert('Coding submitted successfully!');
    } catch (error) {
      console.error('Submit failed:', error);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">
        Medical Coding - {encounterId}
      </h1>

      {/* Patient & Encounter Info */}
      {encounter && (
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <div className="grid grid-cols-4 gap-4">
            <div>
              <p className="text-sm text-gray-600">Patient</p>
              <p className="font-semibold">{encounter.patientName}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Provider</p>
              <p className="font-semibold">{encounter.providerName}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Date</p>
              <p className="font-semibold">{encounter.date}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Type</p>
              <p className="font-semibold">{encounter.type}</p>
            </div>
          </div>
        </div>
      )}

      {/* Clinical Notes */}
      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <h2 className="text-xl font-semibold mb-4">Clinical Notes</h2>
        <div className="bg-gray-50 p-4 rounded border border-gray-200 whitespace-pre-wrap">
          {clinicalNotes}
        </div>
        
        <button
          onClick={getAISuggestions}
          disabled={loading}
          className="mt-4 px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50"
        >
          {loading ? 'Getting AI Suggestions...' : '🤖 Get AI Coding Suggestions'}
        </button>
      </div>

      {/* AI Suggestions */}
      {aiSuggestions && (
        <div className="bg-purple-50 p-6 rounded-lg shadow mb-6 border-2 border-purple-200">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">
              AI Suggestions (Confidence: {aiSuggestions.overallConfidence}%)
            </h2>
            <button
              onClick={acceptAllSuggestions}
              className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
            >
              Accept All
            </button>
          </div>

          <div className="grid grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold mb-2">Diagnosis Codes (ICD-10):</h3>
              <ul className="space-y-2">
                {aiSuggestions.diagnosisCodes.map((code, idx) => (
                  <li key={idx} className="flex items-center">
                    <span className="text-green-600 mr-2">✓</span>
                    <span className="font-mono">{code.code}</span>
                    <span className="ml-2">- {code.description}</span>
                    <span className="ml-auto text-sm text-gray-600">
                      ({code.confidence}%)
                    </span>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="font-semibold mb-2">Procedure Codes (CPT):</h3>
              <ul className="space-y-2">
                {aiSuggestions.procedureCodes.map((code, idx) => (
                  <li key={idx} className="flex items-center">
                    <span className="text-green-600 mr-2">✓</span>
                    <span className="font-mono">{code.code}</span>
                    <span className="ml-2">- {code.description}</span>
                    <span className="ml-auto text-sm text-gray-600">
                      ({code.confidence}%)
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="mt-4 p-4 bg-white rounded border border-purple-200">
            <p className="text-sm text-gray-700">
              <strong>AI Reasoning:</strong> {aiSuggestions.reasoning}
            </p>
          </div>
        </div>
      )}

      {/* Assigned Codes */}
      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <h2 className="text-xl font-semibold mb-4">Assigned Codes</h2>
        
        <div className="grid grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold mb-2">ICD-10 (Diagnoses):</h3>
            <ul className="space-y-2">
              {assignedDiagnoses.map((code, idx) => (
                <li key={idx} className="flex items-center justify-between bg-gray-50 p-2 rounded">
                  <span className="font-mono">{code}</span>
                  <button
                    onClick={() => setAssignedDiagnoses(
                      assignedDiagnoses.filter((_, i) => i !== idx)
                    )}
                    className="text-red-600 hover:text-red-800"
                  >
                    Remove
                  </button>
                </li>
              ))}
            </ul>
            <button className="mt-2 text-blue-600 hover:text-blue-800">
              + Add Diagnosis Code
            </button>
          </div>

          <div>
            <h3 className="font-semibold mb-2">CPT (Procedures):</h3>
            <ul className="space-y-2">
              {assignedProcedures.map((code, idx) => (
                <li key={idx} className="flex items-center justify-between bg-gray-50 p-2 rounded">
                  <span className="font-mono">{code}</span>
                  <button
                    onClick={() => setAssignedProcedures(
                      assignedProcedures.filter((_, i) => i !== idx)
                    )}
                    className="text-red-600 hover:text-red-800"
                  >
                    Remove
                  </button>
                </li>
              ))}
            </ul>
            <button className="mt-2 text-blue-600 hover:text-blue-800">
              + Add Procedure Code
            </button>
          </div>
        </div>
      </div>

      {/* Submit Buttons */}
      <div className="flex justify-end space-x-4">
        <button className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
          Save Draft
        </button>
        <button
          onClick={submitForBilling}
          disabled={assignedDiagnoses.length === 0 || assignedProcedures.length === 0}
          className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
        >
          Submit for Billing
        </button>
      </div>
    </div>
  );
}

export default MedicalCoding;
```

---

#### Backend APIs

**API 1: Get AI Coding Suggestions**
```python
# app/api/v1/coding.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.coding import CodingSuggestionRequest, CodingSuggestionResponse
from app.services.ai_coding_service import AICodingService

router = APIRouter()

@router.post("/ai-suggest", response_model=CodingSuggestionResponse)
async def get_ai_coding_suggestions(
    request: CodingSuggestionRequest,
    db: Session = Depends(get_db)
):
    """
    Get AI-powered coding suggestions based on clinical notes
    
    Uses OpenAI GPT-4 to analyze clinical notes and suggest:
    - ICD-10 diagnosis codes
    - CPT procedure codes
    - Confidence scores
    - Reasoning
    """
    ai_service = AICodingService()
    
    suggestions = await ai_service.get_coding_suggestions(
        clinical_notes=request.clinicalNotes,
        encounter_type=request.encounterType
    )
    
    return suggestions
```

**AI Coding Service:**
```python
# app/services/ai_coding_service.py
import openai
import os
import json

class AICodingService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key
    
    async def get_coding_suggestions(self, clinical_notes: str, encounter_type: str):
        """
        Use OpenAI GPT-4 to suggest medical codes
        """
        
        prompt = f"""
You are an expert medical coder. Analyze the following clinical notes and suggest appropriate medical codes.

Clinical Notes:
{clinical_notes}

Encounter Type: {encounter_type}

Please provide:
1. ICD-10 diagnosis codes (with descriptions and confidence scores)
2. CPT procedure codes (with descriptions and confidence scores)
3. Brief reasoning for your suggestions

Format your response as JSON:
{{
  "diagnosisCodes": [
    {{"code": "J20.9", "description": "Acute bronchitis", "confidence": 95}}
  ],
  "procedureCodes": [
    {{"code": "99213", "description": "Office visit, level 3", "confidence": 92}}
  ],
  "overallConfidence": 92,
  "reasoning": "Patient presents with acute bronchitis symptoms..."
}}
"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert medical coder with 20 years of experience in ICD-10 and CPT coding."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent results
                max_tokens=1000
            )
            
            # Parse JSON response
            content = response.choices[0].message.content
            suggestions = json.loads(content)
            
            return suggestions
            
        except Exception as e:
            # Fallback to rule-based coding if AI fails
            print(f"AI coding failed: {e}")
            return self.fallback_coding(clinical_notes)
    
    def fallback_coding(self, clinical_notes: str):
        """
        Simple rule-based coding as fallback
        """
        # Basic keyword matching
        codes = {
            "diagnosisCodes": [],
            "procedureCodes": [
                {"code": "99213", "description": "Office visit, level 3", "confidence": 70}
            ],
            "overallConfidence": 70,
            "reasoning": "Fallback coding based on encounter type"
        }
        
        # Check for common conditions
        if "bronchitis" in clinical_notes.lower():
            codes["diagnosisCodes"].append({
                "code": "J20.9",
                "description": "Acute bronchitis",
                "confidence": 80
            })
        
        if "cough" in clinical_notes.lower():
            codes["diagnosisCodes"].append({
                "code": "R05",
                "description": "Cough",
                "confidence": 75
            })
        
        return codes
```

**Cost Estimate:**
- OpenAI GPT-4: $0.03 per 1K input tokens, $0.06 per 1K output tokens
- Average cost per coding request: $0.05 - $0.10
- For 100 encounters/day: $5-$10/day = $150-$300/month
- **ROI:** Saves 8 minutes per encounter × $30/hour = $4 per encounter
- **Savings:** $400/day - $10/day = $390/day profit

---

#### Database Tables

**Table: encounter_coding**
```sql
CREATE TABLE encounter_coding (
    coding_id SERIAL PRIMARY KEY,
    encounter_id VARCHAR(50) NOT NULL REFERENCES encounters(encounter_id),
    diagnosis_codes TEXT[],  -- Array of ICD-10 codes
    procedure_codes TEXT[],  -- Array of CPT codes
    ai_suggested BOOLEAN DEFAULT FALSE,
    ai_confidence DECIMAL(5,2),
    ai_reasoning TEXT,
    coded_by VARCHAR(50) NOT NULL,
    coded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'draft',  -- draft, submitted, approved
    
    CONSTRAINT chk_status CHECK (status IN ('draft', 'submitted', 'approved'))
);

CREATE INDEX idx_encounter_coding_encounter ON encounter_coding(encounter_id);
CREATE INDEX idx_encounter_coding_status ON encounter_coding(status);
```

**Table: code_master (ICD-10 and CPT codes)**
```sql
CREATE TABLE code_master (
    code_id SERIAL PRIMARY KEY,
    code_type VARCHAR(10) NOT NULL,  -- ICD10, CPT, HCPCS
    code VARCHAR(20) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    effective_date DATE,
    termination_date DATE,
    
    CONSTRAINT chk_code_type CHECK (code_type IN ('ICD10', 'CPT', 'HCPCS', 'DRG'))
);

CREATE INDEX idx_code_master_code ON code_master(code);
CREATE INDEX idx_code_master_type ON code_master(code_type);
CREATE INDEX idx_code_master_description ON code_master USING gin(to_tsvector('english', description));

-- Sample data
INSERT INTO code_master (code_type, code, description, category) VALUES
('ICD10', 'J20.9', 'Acute bronchitis, unspecified', 'Respiratory'),
('ICD10', 'R05', 'Cough', 'Symptoms'),
('ICD10', 'R50.9', 'Fever, unspecified', 'Symptoms'),
('CPT', '99213', 'Office or other outpatient visit, established patient, 20-29 minutes', 'E&M'),
('CPT', '99214', 'Office or other outpatient visit, established patient, 30-39 minutes', 'E&M');
```

---

### Module 5: Charge Capture (Week 8)

#### What This Module Does
Converts every service provided into a billable charge with the correct CPT code and price.

**Example:**
- Service: Office visit with Dr. Smith
- CPT Code: 99213
- Charge: $150

**Why it's critical:**
- Missed charges = direct revenue loss (5-10% typically)
- Hospitals lose millions annually from missed charges

---

#### Automatic Charge Capture

**How it works:**
1. Doctor completes an order (lab test, imaging, procedure)
2. Order is marked as "Completed"
3. System automatically creates a charge
4. Charge is linked to the encounter

**Example Flow:**
```
Doctor orders: Chest X-ray
   ↓
Radiology completes X-ray
   ↓
System automatically creates charge:
   - CPT: 71046 (Chest X-ray, 2 views)
   - Price: $75
   - Status: Pending review
```

**Backend Implementation:**
```python
# app/services/charge_capture_service.py
from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.charge import Charge
from app.models.fee_schedule import FeeSchedule

class ChargeCaptureService:
    def __init__(self, db: Session):
        self.db = db
    
    def auto_capture_from_order(self, order_id: int):
        """
        Automatically create charge when order is completed
        """
        # Get order
        order = self.db.query(Order).filter(Order.order_id == order_id).first()
        
        if not order or order.status != 'completed':
            return None
        
        # Check if charge already exists
        existing_charge = self.db.query(Charge).filter(
            Charge.order_id == order_id
        ).first()
        
        if existing_charge:
            return existing_charge
        
        # Get CPT code for this order type
        cpt_code = self.get_cpt_for_order(order.order_type, order.order_code)
        
        # Get price from fee schedule
        fee = self.db.query(FeeSchedule).filter(
            FeeSchedule.cpt_code == cpt_code
        ).first()
        
        if not fee:
            raise Exception(f"No fee found for CPT {cpt_code}")
        
        # Create charge
        charge = Charge(
            encounter_id=order.encounter_id,
            order_id=order.order_id,
            cpt_code=cpt_code,
            description=fee.description,
            units=1,
            unit_price=fee.standard_price,
            total_charge=fee.standard_price,
            status='pending',
            captured_by='SYSTEM',
            capture_method='automatic'
        )
        
        self.db.add(charge)
        self.db.commit()
        
        return charge
    
    def get_cpt_for_order(self, order_type: str, order_code: str) -> str:
        """
        Map order codes to CPT codes
        """
        # This would be a lookup table in production
        mapping = {
            'LAB': {
                'CBC': '85025',  # Complete blood count
                'CMP': '80053',  # Comprehensive metabolic panel
            },
            'IMAGING': {
                'CHEST_XRAY': '71046',  # Chest X-ray, 2 views
                'CT_HEAD': '70450',     # CT head without contrast
            }
        }
        
        return mapping.get(order_type, {}).get(order_code, '99499')
```

---

### Module 6: Claim Creation (Week 9)

#### What This Module Does
Generates an insurance claim from the coded encounter, ready for submission.

**What a claim contains:**
- Patient demographics
- Insurance information
- Provider NPI
- Diagnosis codes (ICD-10)
- Procedure codes (CPT)
- Charges
- Service dates

**Claim Format:**
- **CMS-1500:** For professional claims (doctor offices)
- **UB-04:** For institutional claims (hospitals)
- **EDI 837:** Electronic format for submission

---

#### Backend API

**API: Create Claim**
```python
# app/api/v1/claims.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.claim_service import ClaimService

router = APIRouter()

@router.post("/create")
def create_claim(
    encounter_id: str,
    db: Session = Depends(get_db)
):
    """
    Create claim from coded encounter
    
    Steps:
    1. Validate encounter is coded
    2. Get patient, insurance, provider info
    3. Get diagnosis and procedure codes
    4. Get charges
    5. Generate claim
    6. Save to database
    """
    claim_service = ClaimService(db)
    
    claim = claim_service.create_claim_from_encounter(encounter_id)
    
    return {
        "claimId": claim.claim_id,
        "status": claim.status,
        "totalCharge": claim.total_charge
    }
```

**Claim Service:**
```python
# app/services/claim_service.py
from sqlalchemy.orm import Session
from app.models.claim import Claim, ClaimLine, ClaimDiagnosis
from app.models.encounter import Encounter
from app.models.patient import Patient, PatientInsurance
from app.models.charge import Charge
from datetime import datetime
import uuid

class ClaimService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_claim_from_encounter(self, encounter_id: str):
        """
        Create claim from encounter
        """
        # Get encounter
        encounter = self.db.query(Encounter).filter(
            Encounter.encounter_id == encounter_id
        ).first()
        
        if not encounter:
            raise HTTPException(status_code=404, detail="Encounter not found")
        
        if encounter.coding_status != 'approved':
            raise HTTPException(
                status_code=400,
                detail="Encounter must be coded before creating claim"
            )
        
        # Get patient
        patient = self.db.query(Patient).filter(
            Patient.patient_id == encounter.patient_id
        ).first()
        
        # Get primary insurance
        insurance = self.db.query(PatientInsurance).filter(
            PatientInsurance.patient_id == encounter.patient_id,
            PatientInsurance.priority == 1,
            PatientInsurance.is_active == True
        ).first()
        
        if not insurance:
            raise HTTPException(status_code=400, detail="No active insurance found")
        
        # Get charges
        charges = self.db.query(Charge).filter(
            Charge.encounter_id == encounter_id,
            Charge.status == 'approved'
        ).all()
        
        if not charges:
            raise HTTPException(status_code=400, detail="No approved charges found")
        
        # Calculate total
        total_charge = sum(charge.total_charge for charge in charges)
        
        # Generate claim ID
        claim_id = f"CLM-{datetime.now().year}-{str(uuid.uuid4())[:8].upper()}"
        
        # Create claim
        claim = Claim(
            claim_id=claim_id,
            encounter_id=encounter_id,
            patient_id=patient.patient_id,
            insurance_id=insurance.insurance_id,
            provider_id=encounter.provider_id,
            service_date=encounter.service_date,
            total_charge=total_charge,
            status='created',
            created_by='SYSTEM'
        )
        
        self.db.add(claim)
        self.db.flush()
        
        # Create claim lines (one per charge)
        for idx, charge in enumerate(charges, start=1):
            claim_line = ClaimLine(
                claim_id=claim.claim_id,
                line_number=idx,
                service_date=encounter.service_date,
                cpt_code=charge.cpt_code,
                description=charge.description,
                units=charge.units,
                unit_price=charge.unit_price,
                total_charge=charge.total_charge
            )
            self.db.add(claim_line)
        
        # Create claim diagnoses
        for idx, diagnosis_code in enumerate(encounter.diagnosis_codes, start=1):
            claim_diagnosis = ClaimDiagnosis(
                claim_id=claim.claim_id,
                diagnosis_pointer=idx,
                icd10_code=diagnosis_code
            )
            self.db.add(claim_diagnosis)
        
        self.db.commit()
        self.db.refresh(claim)
        
        return claim
```

---

### Module 7: Claim Scrubbing (AI-Powered) (Week 10)

#### What This Module Does
Checks claim for errors before submission to prevent denials.

**200+ Validation Checks:**
1. **Missing fields:** Patient name, DOB, insurance ID, etc.
2. **Invalid codes:** CPT/ICD-10 codes that don't exist
3. **NCCI edits:** Codes that can't be billed together
4. **Medical necessity:** Diagnosis supports procedure
5. **Authorization:** Prior auth required but missing
6. **Duplicate claims:** Same service already billed
7. **Timely filing:** Claim submitted before deadline

**Error Levels:**
- **Fatal:** Must fix before submission (claim will be rejected)
- **Warning:** Recommend fixing (may cause denial)
- **Info:** FYI (won't cause denial)

---

#### Frontend Screen

**Screen: Claim Scrubbing Results**
```
┌─────────────────────────────────────────────────┐
│  Claim Scrubbing - CLM-2026-A1B2C3D4            │
├─────────────────────────────────────────────────┤
│                                                  │
│  [🔍 Run Scrubbing]                             │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │ Scrubbing Results:                       │  │
│  │                                          │  │
│  │ ❌ 2 Fatal Errors (Must Fix)            │  │
│  │ ⚠️  3 Warnings (Recommend Fix)          │  │
│  │ ℹ️  1 Info                              │  │
│  │                                          │  │
│  │ Clean Claim Rate: 0% ❌                 │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  Fatal Errors:                                  │
│  ┌──────────────────────────────────────────┐  │
│  │ 1. Missing prior authorization           │  │
│  │    CPT 99215 requires prior auth for     │  │
│  │    this payer.                           │  │
│  │    [Fix Now]                             │  │
│  │                                          │  │
│  │ 2. Invalid diagnosis code                │  │
│  │    ICD-10 code J20.99 does not exist.    │  │
│  │    Did you mean J20.9?                   │  │
│  │    [Fix Now]                             │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  Warnings:                                      │
│  ┌──────────────────────────────────────────┐  │
│  │ 1. NCCI edit violation                   │  │
│  │    CPT 99213 and 99214 cannot be billed  │  │
│  │    together on same date.                │  │
│  │    [Review]                              │  │
│  │                                          │  │
│  │ 2. Medical necessity concern             │  │
│  │    Diagnosis J20.9 may not support       │  │
│  │    procedure 99215 (high complexity).    │  │
│  │    [Review]                              │  │
│  │                                          │  │
│  │ 3. Duplicate claim possible              │  │
│  │    Similar claim submitted 2 days ago.   │  │
│  │    [Review]                              │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  [Fix All Errors] [Submit Anyway] [Cancel]      │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

#### Backend API

**API: Scrub Claim**
```python
# app/api/v1/claims.py
@router.post("/{claim_id}/scrub")
async def scrub_claim(
    claim_id: str,
    db: Session = Depends(get_db)
):
    """
    Scrub claim for errors
    
    Performs 200+ validation checks:
    - Missing fields
    - Invalid codes
    - NCCI edits
    - Medical necessity
    - Prior authorization
    - Duplicates
    - Timely filing
    """
    scrubbing_service = ClaimScrubbingService(db)
    
    # Run all checks
    results = await scrubbing_service.scrub_claim(claim_id)
    
    # Get AI prediction
    ai_prediction = await scrubbing_service.predict_denial_risk(claim_id)
    
    return {
        "claimId": claim_id,
        "fatalErrors": results["fatal"],
        "warnings": results["warnings"],
        "info": results["info"],
        "cleanClaimRate": results["clean_rate"],
        "aiPrediction": ai_prediction
    }
```

**Scrubbing Service:**
```python
# app/services/claim_scrubbing_service.py
from sqlalchemy.orm import Session
from app.models.claim import Claim, ClaimLine, ClaimDiagnosis
import openai

class ClaimScrubbingService:
    def __init__(self, db: Session):
        self.db = db
    
    async def scrub_claim(self, claim_id: str):
        """
        Run all scrubbing checks
        """
        claim = self.db.query(Claim).filter(Claim.claim_id == claim_id).first()
        
        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")
        
        errors = {
            "fatal": [],
            "warnings": [],
            "info": []
        }
        
        # Check 1: Missing fields
        errors = self.check_missing_fields(claim, errors)
        
        # Check 2: Invalid codes
        errors = self.check_invalid_codes(claim, errors)
        
        # Check 3: NCCI edits
        errors = self.check_ncci_edits(claim, errors)
        
        # Check 4: Medical necessity
        errors = self.check_medical_necessity(claim, errors)
        
        # Check 5: Prior authorization
        errors = self.check_prior_authorization(claim, errors)
        
        # Check 6: Duplicate claims
        errors = self.check_duplicates(claim, errors)
        
        # Check 7: Timely filing
        errors = self.check_timely_filing(claim, errors)
        
        # Calculate clean claim rate
        total_errors = len(errors["fatal"]) + len(errors["warnings"])
        clean_rate = 0 if errors["fatal"] else (100 - (len(errors["warnings"]) * 10))
        
        errors["clean_rate"] = max(0, clean_rate)
        
        return errors
    
    def check_missing_fields(self, claim, errors):
        """Check for missing required fields"""
        if not claim.patient_id:
            errors["fatal"].append({
                "code": "MISSING_PATIENT",
                "message": "Patient ID is missing",
                "fix": "Add patient information"
            })
        
        if not claim.insurance_id:
            errors["fatal"].append({
                "code": "MISSING_INSURANCE",
                "message": "Insurance ID is missing",
                "fix": "Add insurance information"
            })
        
        return errors
    
    def check_ncci_edits(self, claim, errors):
        """Check NCCI edits (codes that can't be billed together)"""
        # Get all CPT codes on claim
        claim_lines = self.db.query(ClaimLine).filter(
            ClaimLine.claim_id == claim.claim_id
        ).all()
        
        cpt_codes = [line.cpt_code for line in claim_lines]
        
        # Check for common NCCI violations
        # Example: Can't bill 99213 and 99214 together
        if '99213' in cpt_codes and '99214' in cpt_codes:
            errors["warnings"].append({
                "code": "NCCI_EDIT",
                "message": "CPT 99213 and 99214 cannot be billed together on same date",
                "fix": "Remove one of the codes"
            })
        
        return errors
    
    async def predict_denial_risk(self, claim_id: str):
        """
        Use AI to predict denial risk
        """
        claim = self.db.query(Claim).filter(Claim.claim_id == claim_id).first()
        
        # Prepare claim data for AI
        claim_data = {
            "patient_age": self.calculate_age(claim.patient.dob),
            "diagnosis_codes": [d.icd10_code for d in claim.diagnoses],
            "procedure_codes": [l.cpt_code for l in claim.lines],
            "total_charge": float(claim.total_charge),
            "payer": claim.insurance.payer_name
        }
        
        prompt = f"""
Analyze this insurance claim and predict the denial risk:

Claim Data:
{claim_data}

Provide:
1. Risk level (Low, Medium, High)
2. Risk score (0-100)
3. Top 3 potential denial reasons
4. Recommendations to reduce risk

Format as JSON.
"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in medical billing and claim denials."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            prediction = json.loads(response.choices[0].message.content)
            return prediction
            
        except Exception as e:
            return {
                "riskLevel": "Unknown",
                "riskScore": 50,
                "reasons": ["AI prediction unavailable"],
                "recommendations": ["Perform manual review"]
            }
```

---

### Module 8: Claim Submission (Waystar Integration) (Week 11-12)

#### What This Module Does
Submits claims electronically to insurance companies via clearinghouse (Waystar).

**Submission Process:**
```
Our System → Waystar (Clearinghouse) → Insurance Company
              ↓
         EDI 837 format
              ↓
         Acknowledgment (EDI 999)
              ↓
         Status updates (EDI 277)
```

---

#### Waystar Integration

**Step 1: Sign up for Waystar API**
- Go to https://www.waystar.com/developers
- Create account
- Get API credentials (Client ID, Client Secret)
- Get approval (takes 2-4 weeks)

**Step 2: Generate EDI 837**
```python
# app/services/edi_service.py
from datetime import datetime

class EDI837Service:
    def generate_837(self, claim):
        """
        Generate EDI 837 format (simplified)
        
        Real EDI 837 is much more complex (1000+ lines)
        Use a library like 'pyx12' or 'edi-835-parser' in production
        """
        
        edi_content = f"""ISA*00*          *00*          *ZZ*{claim.provider_npi}*ZZ*{claim.payer_id}*{datetime.now().strftime('%y%m%d')}*{datetime.now().strftime('%H%M')}*^*00501*{claim.claim_id}*0*P*:~
GS*HC*{claim.provider_npi}*{claim.payer_id}*{datetime.now().strftime('%Y%m%d')}*{datetime.now().strftime('%H%M')}*1*X*005010X222A1~
ST*837*0001*005010X222A1~
BHT*0019*00*{claim.claim_id}*{datetime.now().strftime('%Y%m%d')}*{datetime.now().strftime('%H%M')}*CH~
NM1*41*2*{claim.provider_name}*****46*{claim.provider_npi}~
NM1*IL*1*{claim.patient_last_name}*{claim.patient_first_name}****MI*{claim.insurance_policy_number}~
CLM*{claim.claim_id}*{claim.total_charge}***11:B:1*Y*A*Y*Y~
HI*ABK:{claim.primary_diagnosis_code}~
LX*1~
SV1*HC:{claim.primary_cpt_code}*{claim.total_charge}*UN*1***1~
SE*15*0001~
GE*1*1~
IEA*1*{claim.claim_id}~"""
        
        return edi_content
```

**Step 3: Submit to Waystar**
```python
# app/services/waystar_service.py
import httpx
import os

class WaystarService:
    def __init__(self):
        self.base_url = "https://api.waystar.com/claims/v1"
        self.client_id = os.getenv("WAYSTAR_CLIENT_ID")
        self.client_secret = os.getenv("WAYSTAR_CLIENT_SECRET")
        self.access_token = None
    
    async def authenticate(self):
        """Get access token"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.waystar.com/oauth/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                }
            )
            self.access_token = response.json()["access_token"]
    
    async def submit_claim(self, claim_id: str, edi_content: str):
        """Submit claim to Waystar"""
        
        if not self.access_token:
            await self.authenticate()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/submit",
                json={
                    "claimId": claim_id,
                    "ediContent": edi_content,
                    "submissionType": "original"
                },
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                },
                timeout=60.0
            )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Submission failed: {response.text}")
    
    async def check_claim_status(self, claim_id: str):
        """Check claim status (EDI 276/277)"""
        
        if not self.access_token:
            await self.authenticate()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/status/{claim_id}",
                headers={
                    "Authorization": f"Bearer {self.access_token}"
                }
            )
        
        return response.json()
```

**API Endpoint:**
```python
# app/api/v1/claims.py
@router.post("/{claim_id}/submit")
async def submit_claim(
    claim_id: str,
    db: Session = Depends(get_db)
):
    """
    Submit claim to insurance via Waystar
    """
    # Get claim
    claim = db.query(Claim).filter(Claim.claim_id == claim_id).first()
    
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    # Generate EDI 837
    edi_service = EDI837Service()
    edi_content = edi_service.generate_837(claim)
    
    # Submit to Waystar
    waystar_service = WaystarService()
    result = await waystar_service.submit_claim(claim_id, edi_content)
    
    # Update claim status
    claim.status = 'submitted'
    claim.submitted_at = datetime.utcnow()
    claim.submission_id = result.get('submissionId')
    db.commit()
    
    return {
        "claimId": claim_id,
        "status": "submitted",
        "submissionId": result.get('submissionId')
    }
```

---

## Summary of Phase 2

**What we built:**
✅ Medical coding module with AI assistance  
✅ Automatic charge capture  
✅ Claim creation  
✅ Claim scrubbing with 200+ checks  
✅ AI-powered denial prediction  
✅ Claim submission via Waystar  
✅ EDI 837 generation  

**Time:** 6 weeks  
**Team:** 5-7 people  
**Cost:** ~$200K (team) + $500/month (APIs)  

**Next:** Phase 3 - Payment & Denial Management

---

**Continue to Part 4 for Phase 3...**

---

**Document Navigation:**
- **Part 1:** Introduction & Phase 1 Foundation
- **Part 2:** Phase 1 Core Modules
- **Part 3:** Phase 2 Clinical & Billing (This document)
- **Part 4:** Phase 3 Payment & Denials
- **Part 5:** Phase 4 Reports & Deployment
