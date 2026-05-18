# Healthcare RCM Application - Development Phase Guide
## Part 4: Phase 3 - Payment & Denial Management

**Version:** 1.0  
**For:** Technical Lead & Development Team

---

## 5. Phase 3 — Payment & Denial Management (Weeks 13-16)

**Goal:** Handle insurance payments and denied claims

**What we'll build:**
- Payment posting (ERA/835 processing)
- Denial management
- Appeals workflow
- AR (Accounts Receivable) management
- Patient billing
- Payment collection

**Why this phase?**
This is where we actually collect money. Without payment posting and denial management, revenue sits uncollected.

---

### Module 9: Payment Posting (ERA/835 Processing) (Week 13-14)

#### What This Module Does
Records insurance payments and adjustments when they arrive.

**Payment Flow:**
```
Insurance Company → Sends payment (check or EFT)
                 → Sends ERA file (EDI 835)
                 → We download ERA
                 → Parse ERA
                 → Auto-post payment to claims
```

**What's in an ERA (EDI 835)?**
- Claim ID
- Amount paid
- Amount adjusted (contractual write-off)
- Patient responsibility (copay, deductible)
- Adjustment reason codes (CARC/RARC)
- Check number and date

**Example ERA Data:**
```
Claim: CLM-2026-001234
Billed: $150.00
Allowed: $120.00
Paid: $95.00
Adjustments:
  - Contractual: -$30.00 (difference between billed and allowed)
  - Deductible: -$25.00 (patient owes)
Patient Responsibility: $25.00
```

---

#### Frontend Screen

**Screen: Payment Posting**
```
┌─────────────────────────────────────────────────┐
│  Payment Posting                                │
├─────────────────────────────────────────────────┤
│                                                  │
│  [📥 Import ERA File] [Manual Posting]          │
│                                                  │
│  Recent ERA Files:                              │
│  ┌──────────────────────────────────────────┐  │
│  │ ERA_20260520_001.835                     │  │
│  │ Date: 05/20/2026                         │  │
│  │ Payer: Blue Cross                        │  │
│  │ Claims: 45                               │  │
│  │ Total: $12,450.00                        │  │
│  │ Status: ✅ Posted (43) ⚠️ Review (2)    │  │
│  │ [View Details]                           │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │ ERA_20260519_002.835                     │  │
│  │ Date: 05/19/2026                         │  │
│  │ Payer: Aetna                             │  │
│  │ Claims: 32                               │  │
│  │ Total: $8,900.00                         │  │
│  │ Status: ✅ Posted (32)                   │  │
│  │ [View Details]                           │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
└─────────────────────────────────────────────────┘

When viewing ERA details:
┌─────────────────────────────────────────────────┐
│  ERA Details - ERA_20260520_001.835             │
├─────────────────────────────────────────────────┤
│                                                  │
│  Payer: Blue Cross Blue Shield                  │
│  Check #: 123456789                             │
│  Check Date: 05/20/2026                         │
│  Total Amount: $12,450.00                       │
│                                                  │
│  Claims (45):                                   │
│  ┌──────────────────────────────────────────┐  │
│  │ CLM-001 | John Doe | $150 → $120 ✅      │  │
│  │ CLM-002 | Jane Smith | $200 → $180 ✅    │  │
│  │ CLM-003 | Bob Johnson | $0 → DENIED ❌   │  │
│  │ ...                                      │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  [Auto-Post All] [Review Denials]               │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

#### Backend Implementation

**Step 1: Download ERA from Waystar**
```python
# app/services/era_service.py
import httpx
import os
from datetime import datetime, timedelta

class ERAService:
    def __init__(self):
        self.waystar_api_key = os.getenv("WAYSTAR_API_KEY")
        self.base_url = "https://api.waystar.com/remittance/v1"
    
    async def download_eras(self, start_date: str, end_date: str):
        """
        Download ERA files from Waystar
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/files",
                params={
                    "startDate": start_date,
                    "endDate": end_date
                },
                headers={
                    "Authorization": f"Bearer {self.waystar_api_key}"
                },
                timeout=60.0
            )
        
        if response.status_code == 200:
            return response.json()["files"]
        else:
            raise Exception(f"Failed to download ERAs: {response.text}")
    
    async def get_era_content(self, file_id: str):
        """
        Get ERA file content
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/files/{file_id}",
                headers={
                    "Authorization": f"Bearer {self.waystar_api_key}"
                }
            )
        
        return response.text  # EDI 835 content
```

**Step 2: Parse EDI 835**
```python
# app/services/edi835_parser.py
import re

class EDI835Parser:
    def parse(self, edi_content: str):
        """
        Parse EDI 835 file
        
        In production, use a library like 'edi-835-parser' or 'pyx12'
        This is a simplified version
        """
        payments = []
        
        # Split into segments
        segments = edi_content.split('~')
        
        current_payment = {}
        
        for segment in segments:
            fields = segment.split('*')
            segment_id = fields[0]
            
            if segment_id == 'BPR':
                # Payment header
                current_payment = {
                    'total_amount': float(fields[2]),
                    'payment_method': fields[3],
                    'check_number': fields[7],
                    'check_date': fields[16],
                    'claims': []
                }
            
            elif segment_id == 'CLP':
                # Claim payment info
                claim = {
                    'claim_id': fields[1],
                    'status_code': fields[2],
                    'billed_amount': float(fields[3]),
                    'paid_amount': float(fields[4]),
                    'patient_responsibility': float(fields[5]),
                    'adjustments': []
                }
                current_payment['claims'].append(claim)
            
            elif segment_id == 'CAS':
                # Claim adjustment
                adjustment = {
                    'group_code': fields[1],
                    'reason_code': fields[2],
                    'amount': float(fields[3])
                }
                current_payment['claims'][-1]['adjustments'].append(adjustment)
        
        payments.append(current_payment)
        
        return payments
```

**Step 3: Auto-Post Payments**
```python
# app/services/payment_posting_service.py
from sqlalchemy.orm import Session
from app.models.claim import Claim
from app.models.payment import ClaimPayment, PaymentAdjustment
from datetime import datetime

class PaymentPostingService:
    def __init__(self, db: Session):
        self.db = db
    
    def auto_post_era(self, era_data: dict):
        """
        Automatically post payments from ERA
        """
        posted_count = 0
        review_count = 0
        
        for claim_payment in era_data['claims']:
            # Find claim
            claim = self.db.query(Claim).filter(
                Claim.claim_id == claim_payment['claim_id']
            ).first()
            
            if not claim:
                review_count += 1
                continue
            
            # Check if payment matches expected amount
            if self.validate_payment(claim, claim_payment):
                # Auto-post
                self.post_payment(claim, claim_payment, era_data)
                posted_count += 1
            else:
                # Flag for manual review
                claim.payment_status = 'review_required'
                self.db.commit()
                review_count += 1
        
        return {
            'posted': posted_count,
            'review': review_count
        }
    
    def validate_payment(self, claim, payment_data):
        """
        Validate payment matches expected amount
        """
        # Check if paid amount is reasonable
        paid_amount = payment_data['paid_amount']
        billed_amount = claim.total_charge
        
        # Payment should be between 50% and 100% of billed
        if paid_amount < (billed_amount * 0.5) or paid_amount > billed_amount:
            return False
        
        return True
    
    def post_payment(self, claim, payment_data, era_data):
        """
        Post payment to claim
        """
        # Create payment record
        payment = ClaimPayment(
            claim_id=claim.claim_id,
            payment_date=datetime.strptime(era_data['check_date'], '%Y%m%d'),
            check_number=era_data['check_number'],
            paid_amount=payment_data['paid_amount'],
            patient_responsibility=payment_data['patient_responsibility'],
            payment_method='ERA',
            posted_by='SYSTEM'
        )
        
        self.db.add(payment)
        self.db.flush()
        
        # Create adjustment records
        for adj in payment_data['adjustments']:
            adjustment = PaymentAdjustment(
                payment_id=payment.payment_id,
                adjustment_group=adj['group_code'],
                adjustment_reason=adj['reason_code'],
                adjustment_amount=adj['amount']
            )
            self.db.add(adjustment)
        
        # Update claim status
        claim.payment_status = 'paid'
        claim.paid_amount = payment_data['paid_amount']
        claim.patient_balance = payment_data['patient_responsibility']
        
        self.db.commit()
```

---

#### Database Tables

**Table: claim_payments**
```sql
CREATE TABLE claim_payments (
    payment_id SERIAL PRIMARY KEY,
    claim_id VARCHAR(50) NOT NULL REFERENCES claims(claim_id),
    payment_date DATE NOT NULL,
    check_number VARCHAR(50),
    paid_amount DECIMAL(10,2) NOT NULL,
    patient_responsibility DECIMAL(10,2) DEFAULT 0,
    payment_method VARCHAR(20) NOT NULL,  -- ERA, CHECK, CASH, CARD
    posted_by VARCHAR(50) NOT NULL,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

CREATE INDEX idx_claim_payments_claim ON claim_payments(claim_id);
CREATE INDEX idx_claim_payments_date ON claim_payments(payment_date);
```

**Table: payment_adjustments**
```sql
CREATE TABLE payment_adjustments (
    adjustment_id SERIAL PRIMARY KEY,
    payment_id INTEGER NOT NULL REFERENCES claim_payments(payment_id),
    adjustment_group VARCHAR(10) NOT NULL,  -- CO, PR, OA, PI
    adjustment_reason VARCHAR(10) NOT NULL,  -- CARC code
    adjustment_amount DECIMAL(10,2) NOT NULL,
    adjustment_description TEXT
);

-- Common adjustment codes:
-- CO = Contractual Obligation (insurance write-off)
-- PR = Patient Responsibility (deductible, copay)
-- OA = Other Adjustment
-- PI = Payer Initiated
```

---

### Module 10: Denial Management (Week 14-15)

#### What This Module Does
Tracks denied claims and manages the appeal process.

**Common Denial Reasons:**
1. **Missing information** (30%) - Easy to fix
2. **Incorrect coding** (25%) - Need to correct codes
3. **Eligibility issues** (20%) - Patient not covered
4. **Timely filing** (10%) - Submitted too late (permanent)
5. **Medical necessity** (15%) - Diagnosis doesn't support procedure

**Denial Workflow:**
```
Claim Denied
   ↓
Identify Reason
   ↓
Can it be fixed?
   ↓ Yes          ↓ No
Correct & Resubmit  Write Off
   ↓
Or Appeal
   ↓
Level 1 Appeal
   ↓ Denied
Level 2 Appeal
   ↓ Denied
Level 3 Appeal (External Review)
```

---

#### Frontend Screen

**Screen: Denial Worklist**
```
┌─────────────────────────────────────────────────┐
│  Denial Management                              │
├─────────────────────────────────────────────────┤
│                                                  │
│  Filter: [All Denials ▼] [High Value First ▼]  │
│                                                  │
│  Denied Claims (23):                            │
│  ┌──────────────────────────────────────────┐  │
│  │ CLM-001 | $1,250 | Missing Auth | Work   │  │
│  │ CLM-005 | $890 | Wrong Code | Work       │  │
│  │ CLM-012 | $650 | Timely Filing | Write Off│ │
│  │ CLM-018 | $450 | Eligibility | Appeal     │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  Denial Analytics:                              │
│  ┌──────────────────────────────────────────┐  │
│  │ Total Denied: $45,000                    │  │
│  │ Recoverable: $35,000 (78%)               │  │
│  │ Write-off: $10,000 (22%)                 │  │
│  │                                          │  │
│  │ Top Denial Reasons:                      │  │
│  │ 1. Missing Authorization (35%)           │  │
│  │ 2. Incorrect Coding (28%)                │  │
│  │ 3. Eligibility (20%)                     │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
└─────────────────────────────────────────────────┘

When clicking "Work" on a denial:
┌─────────────────────────────────────────────────┐
│  Denial Details - CLM-001                       │
├─────────────────────────────────────────────────┤
│                                                  │
│  Claim: CLM-2026-001234                         │
│  Patient: John Doe                              │
│  Billed: $1,250.00                              │
│  Paid: $0.00                                    │
│                                                  │
│  Denial Information:                            │
│  ┌──────────────────────────────────────────┐  │
│  │ Reason Code: 197                         │  │
│  │ Description: Precertification/authorization│ │
│  │              absent                       │  │
│  │                                          │  │
│  │ Denial Date: 05/18/2026                  │  │
│  │ Days Since Denial: 2                     │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  [🤖 Get AI Recommendation]                     │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │ AI Recommendation:                       │  │
│  │                                          │  │
│  │ Action: Obtain Retroactive Authorization│  │
│  │ Success Rate: 75%                        │  │
│  │ Estimated Recovery: $1,250               │  │
│  │                                          │  │
│  │ Steps:                                   │  │
│  │ 1. Contact payer for retro auth          │  │
│  │ 2. Submit clinical documentation         │  │
│  │ 3. Resubmit claim with auth number       │  │
│  │                                          │  │
│  │ Alternative: Appeal (Success: 40%)       │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  Actions:                                       │
│  [Request Retro Auth] [Appeal] [Write Off]      │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

#### Backend Implementation

**Denial Service:**
```python
# app/services/denial_service.py
from sqlalchemy.orm import Session
from app.models.claim import Claim
from app.models.denial import Denial, DenialAppeal
import openai

class DenialService:
    def __init__(self, db: Session):
        self.db = db
    
    def process_denial(self, claim_id: str, denial_code: str, denial_reason: str):
        """
        Process a denied claim
        """
        claim = self.db.query(Claim).filter(Claim.claim_id == claim_id).first()
        
        if not claim:
            raise Exception("Claim not found")
        
        # Create denial record
        denial = Denial(
            claim_id=claim_id,
            denial_code=denial_code,
            denial_reason=denial_reason,
            denial_date=datetime.utcnow(),
            denied_amount=claim.total_charge,
            status='pending'
        )
        
        self.db.add(denial)
        
        # Update claim status
        claim.status = 'denied'
        claim.denial_reason = denial_reason
        
        self.db.commit()
        
        return denial
    
    async def get_ai_recommendation(self, denial_id: int):
        """
        Get AI recommendation for handling denial
        """
        denial = self.db.query(Denial).filter(Denial.denial_id == denial_id).first()
        claim = denial.claim
        
        prompt = f"""
Analyze this denied insurance claim and recommend the best action:

Claim Information:
- Claim ID: {claim.claim_id}
- Billed Amount: ${claim.total_charge}
- Denial Code: {denial.denial_code}
- Denial Reason: {denial.denial_reason}
- Diagnosis Codes: {claim.diagnosis_codes}
- Procedure Codes: {claim.procedure_codes}
- Payer: {claim.insurance.payer_name}

Provide:
1. Recommended action (Correct & Resubmit, Appeal, Request Retro Auth, Write Off)
2. Success rate (%)
3. Estimated recovery amount
4. Step-by-step instructions
5. Alternative actions

Format as JSON.
"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in medical billing denials and appeals."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            recommendation = json.loads(response.choices[0].message.content)
            return recommendation
            
        except Exception as e:
            return {
                "action": "Manual Review",
                "successRate": 50,
                "estimatedRecovery": float(claim.total_charge),
                "steps": ["Review denial reason", "Consult with billing manager"],
                "alternatives": []
            }
    
    def create_appeal(self, denial_id: int, appeal_level: int, appeal_text: str):
        """
        Create an appeal for denied claim
        """
        denial = self.db.query(Denial).filter(Denial.denial_id == denial_id).first()
        
        appeal = DenialAppeal(
            denial_id=denial_id,
            appeal_level=appeal_level,
            appeal_date=datetime.utcnow(),
            appeal_text=appeal_text,
            status='submitted'
        )
        
        self.db.add(appeal)
        
        denial.status = f'appeal_level_{appeal_level}'
        
        self.db.commit()
        
        return appeal
    
    async def generate_appeal_letter(self, denial_id: int):
        """
        AI-generated appeal letter
        """
        denial = self.db.query(Denial).filter(Denial.denial_id == denial_id).first()
        claim = denial.claim
        
        prompt = f"""
Write a professional appeal letter for this denied insurance claim:

Claim Information:
- Patient: {claim.patient.first_name} {claim.patient.last_name}
- Claim ID: {claim.claim_id}
- Service Date: {claim.service_date}
- Denial Reason: {denial.denial_reason}
- Diagnosis: {claim.diagnosis_codes}
- Procedure: {claim.procedure_codes}

Write a formal appeal letter that:
1. States the claim details
2. Explains why the denial is incorrect
3. Provides clinical justification
4. Requests reconsideration
5. Is professional and persuasive

Format as a business letter.
"""
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert medical billing appeal writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content
```

---

### Module 11: AR Management (Week 15)

#### What This Module Does
Tracks outstanding accounts receivable and follows up on unpaid claims.

**AR Aging Categories:**
- **0-30 days:** New claims, normal processing time
- **31-60 days:** Follow up with payer
- **61-90 days:** Escalate, may need appeal
- **90+ days:** High risk, may be uncollectible

**Goal:** Keep AR over 90 days below 15% of total AR

---

#### Frontend Screen

**Screen: AR Dashboard**
```
┌─────────────────────────────────────────────────┐
│  Accounts Receivable Dashboard                  │
├─────────────────────────────────────────────────┤
│                                                  │
│  Total AR: $1,250,000                           │
│                                                  │
│  AR Aging:                                      │
│  ┌──────────────────────────────────────────┐  │
│  │ 0-30 days:   $650,000 (52%) ✅          │  │
│  │ 31-60 days:  $350,000 (28%) ⚠️          │  │
│  │ 61-90 days:  $150,000 (12%) ⚠️          │  │
│  │ 90+ days:    $100,000 (8%)  ❌          │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  [View 90+ Days Claims]                         │
│                                                  │
│  Key Metrics:                                   │
│  ┌──────────────────────────────────────────┐  │
│  │ Days in AR: 38 days (Target: <35)       │  │
│  │ Collection Rate: 94% (Target: >95%)      │  │
│  │ Denial Rate: 6% (Target: <5%)           │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

### Module 12: Patient Billing (Week 16)

#### What This Module Does
Bills patients for their portion (copay, deductible, coinsurance) and collects payments.

**Patient Responsibility:**
```
Total Charge: $150
Insurance Paid: $95
Contractual Adjustment: -$30
Patient Owes: $25 (copay)
```

**Billing Process:**
1. Insurance pays their portion
2. System calculates patient balance
3. Generate patient statement
4. Send statement (mail, email, portal)
5. Patient pays online or by mail
6. Post payment to account

---

#### Frontend Screen

**Screen: Patient Statement**
```
┌─────────────────────────────────────────────────┐
│  Patient Statement                              │
├─────────────────────────────────────────────────┤
│                                                  │
│  Patient: John Doe                              │
│  Account #: PAT-2026-001                        │
│  Statement Date: 05/20/2026                     │
│                                                  │
│  Previous Balance: $0.00                        │
│                                                  │
│  New Charges:                                   │
│  ┌──────────────────────────────────────────┐  │
│  │ 05/15/26 | Office Visit | $150.00        │  │
│  │ 05/15/26 | Insurance Payment | -$95.00   │  │
│  │ 05/15/26 | Adjustment | -$30.00          │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  Amount Due: $25.00                             │
│  Due Date: 06/20/2026                           │
│                                                  │
│  [Pay Online] [Set Up Payment Plan]             │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Online Payment (Stripe Integration):**
```typescript
// src/pages/PatientPayment.tsx
import { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import { Elements, CardElement, useStripe, useElements } from '@stripe/react-stripe-js';
import api from '../services/api';

const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_PUBLIC_KEY!);

function PaymentForm({ amount, patientId }: { amount: number, patientId: string }) {
  const stripe = useStripe();
  const elements = useElements();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!stripe || !elements) return;
    
    setLoading(true);
    setError('');

    try {
      // Create payment intent on backend
      const { data } = await api.post('/payments/create-intent', {
        amount: amount * 100, // Convert to cents
        patientId
      });

      // Confirm payment with Stripe
      const result = await stripe.confirmCardPayment(data.clientSecret, {
        payment_method: {
          card: elements.getElement(CardElement)!,
        }
      });

      if (result.error) {
        setError(result.error.message || 'Payment failed');
      } else {
        // Payment successful
        alert('Payment successful!');
        window.location.href = '/payment-confirmation';
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Payment failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto p-6 bg-white rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-4">Pay Your Bill</h2>
      
      <div className="mb-4">
        <p className="text-lg">Amount Due: <strong>${amount.toFixed(2)}</strong></p>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">Card Information</label>
        <div className="border border-gray-300 rounded-lg p-3">
          <CardElement options={{
            style: {
              base: {
                fontSize: '16px',
                color: '#424770',
                '::placeholder': {
                  color: '#aab7c4',
                },
              },
            },
          }} />
        </div>
      </div>

      {error && (
        <div className="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <button
        type="submit"
        disabled={!stripe || loading}
        className="w-full bg-blue-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? 'Processing...' : `Pay $${amount.toFixed(2)}`}
      </button>

      <p className="mt-4 text-sm text-gray-600 text-center">
        Secure payment powered by Stripe
      </p>
    </form>
  );
}

function PatientPayment() {
  return (
    <Elements stripe={stripePromise}>
      <PaymentForm amount={25.00} patientId="PAT-2026-001" />
    </Elements>
  );
}

export default PatientPayment;
```

**Backend (Stripe Integration):**
```python
# app/api/v1/payments.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
import stripe
import os

router = APIRouter()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@router.post("/create-intent")
def create_payment_intent(
    amount: int,  # Amount in cents
    patient_id: str,
    db: Session = Depends(get_db)
):
    """
    Create Stripe payment intent
    """
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            metadata={
                "patient_id": patient_id
            }
        )
        
        return {
            "clientSecret": intent.client_secret
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Handle Stripe webhook events
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET")
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle successful payment
    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        patient_id = payment_intent["metadata"]["patient_id"]
        amount = payment_intent["amount"] / 100  # Convert from cents
        
        # Record payment in database
        payment = PatientPayment(
            patient_id=patient_id,
            amount=amount,
            payment_method="card",
            payment_date=datetime.utcnow(),
            stripe_payment_id=payment_intent["id"]
        )
        db.add(payment)
        db.commit()
    
    return {"status": "success"}
```

---

## Summary of Phase 3

**What we built:**
✅ Payment posting with ERA/835 processing  
✅ Auto-posting (95% success rate)  
✅ Denial management with AI recommendations  
✅ Appeal workflow and letter generation  
✅ AR management and aging reports  
✅ Patient billing and statements  
✅ Online payment collection (Stripe)  

**Time:** 4 weeks  
**Team:** 5-7 people  
**Cost:** ~$150K (team) + $500/month (APIs)  

**Next:** Phase 4 - Reports, Analytics & Deployment

---

**Continue to Part 5 for Phase 4...**

---

**Document Navigation:**
- **Part 1:** Introduction & Phase 1 Foundation
- **Part 2:** Phase 1 Core Modules
- **Part 3:** Phase 2 Clinical & Billing
- **Part 4:** Phase 3 Payment & Denials (This document)
- **Part 5:** Phase 4 Reports & Deployment
