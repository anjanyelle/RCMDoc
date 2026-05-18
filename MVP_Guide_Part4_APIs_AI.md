# Healthcare RCM Application - MVP Guide (Part 4: APIs & AI Integration)

**Version:** 1.0  
**For:** Development Team & Technical Lead

---

## 6. Third-Party APIs for MVP

### Overview of API Strategy

**Philosophy:** Use third-party APIs for complex, specialized tasks. Build in-house for core business logic.

**Benefits:**
- ✅ Faster development (don't reinvent the wheel)
- ✅ Lower maintenance (vendor handles updates)
- ✅ Better reliability (enterprise-grade services)
- ✅ Compliance built-in (HIPAA, EDI standards)

---

### API 1: Waystar (Primary Clearinghouse) 🏥

**What is Waystar?**
Waystar is a healthcare payment software company that acts as a clearinghouse between providers and insurance payers.

**Why We Use Waystar:**
1. Connects to 2,500+ payers (insurance companies)
2. Handles EDI transactions (270/271, 837, 835, 276/277)
3. HIPAA compliant
4. Real-time eligibility verification
5. Claim scrubbing (error checking)
6. 99.5% clean claim rate

**Which Modules Use Waystar:**

| Module | Waystar API | Purpose |
|--------|-------------|---------|
| Insurance Verification | ✅ Eligibility API | Check patient coverage (EDI 270/271) |
| Claim Submission | ✅ Claims API | Submit claims electronically (EDI 837) |
| Claim Status | ✅ Status API | Check claim status (EDI 276/277) |
| Payment Posting | ✅ Remittance API | Download ERA files (EDI 835) |

**API Integration Examples:**

#### 1. Insurance Eligibility Check
```python
import requests

# Waystar Eligibility API
def check_eligibility(patient, insurance, service_date):
    url = "https://api.waystar.com/eligibility/v1/inquiries"
    
    headers = {
        "Authorization": f"Bearer {WAYSTAR_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "patient": {
            "firstName": patient.first_name,
            "lastName": patient.last_name,
            "dateOfBirth": patient.dob,
            "memberId": insurance.policy_number
        },
        "payer": {
            "payerId": insurance.payer_id,  # e.g., "00431" for Aetna
            "payerName": insurance.payer_name
        },
        "provider": {
            "npi": "1234567890",
            "taxId": "12-3456789",
            "organizationName": "ABC Medical Clinic"
        },
        "serviceDate": service_date,
        "serviceType": "30"  # 30 = Health Benefit Plan Coverage
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "status": data["eligibilityStatus"],  # Active/Inactive
            "copay": data.get("copay", 0),
            "deductible": data.get("deductible", {}),
            "out_of_pocket_max": data.get("outOfPocketMax", {}),
            "prior_auth_required": data.get("priorAuthRequired", False)
        }
    else:
        raise Exception(f"Eligibility check failed: {response.text}")
```

#### 2. Claim Submission
```python
# Waystar Claims Submission API
def submit_claim(claim):
    url = "https://api.waystar.com/claims/v1/submit"
    
    headers = {
        "Authorization": f"Bearer {WAYSTAR_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Convert claim to EDI 837 format
    edi_content = generate_edi_837(claim)
    
    payload = {
        "claims": [{
            "claimId": claim.claim_id,
            "ediContent": edi_content,
            "payerId": claim.payer_id,
            "submissionDate": datetime.now().isoformat()
        }]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "batch_id": data["batchId"],
            "tracking_number": data["trackingNumber"],
            "status": data["status"]  # Accepted/Rejected
        }
    else:
        raise Exception(f"Claim submission failed: {response.text}")
```

#### 3. Download ERA (Payment Information)
```python
# Waystar Remittance API - Download ERA files
def download_era_files(date_range):
    url = "https://api.waystar.com/remittance/v1/files"
    
    headers = {
        "Authorization": f"Bearer {WAYSTAR_API_KEY}"
    }
    
    params = {
        "startDate": date_range["start"],
        "endDate": date_range["end"],
        "fileType": "835"  # EDI 835 (ERA)
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        era_files = response.json()["files"]
        
        for era_file in era_files:
            # Download and parse each ERA file
            era_content = download_file(era_file["fileUrl"])
            parse_and_post_payments(era_content)
        
        return len(era_files)
    else:
        raise Exception(f"ERA download failed: {response.text}")
```

**Waystar Pricing:**
- Setup fee: $500-$1,000
- Monthly fee: $200-$500
- Per-transaction fee: $0.25-$0.50 per claim
- **MVP Estimate:** ~$500/month for 1,000 claims

**Waystar Alternatives:**
- Change Healthcare
- Availity (see below)
- Trizetto

---

### API 2: Availity (Alternative Clearinghouse) 🔄

**What is Availity?**
Another major healthcare clearinghouse, owned by Elevance Health (formerly Anthem).

**Why We Use Availity:**
1. Free for some payers (Anthem, Blue Cross plans)
2. Good for smaller practices
3. Real-time eligibility
4. Claim submission and status

**When to Use Availity vs Waystar:**
- **Use Availity:** If most patients have Anthem/Blue Cross insurance (free)
- **Use Waystar:** For broader payer coverage and advanced features

**Which Modules Use Availity:**
- Insurance Verification
- Claim Submission
- Claim Status

**API Integration Example:**
```python
# Availity Eligibility API
def check_eligibility_availity(patient, insurance):
    url = "https://api.availity.com/availity/v1/coverages"
    
    headers = {
        "Authorization": f"Bearer {AVAILITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "payerId": insurance.payer_id,
        "provider": {
            "npi": "1234567890"
        },
        "subscriber": {
            "memberId": insurance.policy_number,
            "firstName": patient.first_name,
            "lastName": patient.last_name,
            "dateOfBirth": patient.dob
        },
        "encounter": {
            "serviceType": "30"
        }
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    return response.json()
```

**Availity Pricing:**
- Free for Anthem/Blue Cross
- $200-$400/month for other payers
- Per-transaction fees apply

**MVP Recommendation:**
- Start with **Waystar** for broader coverage
- Add Availity later if needed for cost savings

---

### API 3: Stripe (Payment Processing) 💳

**What is Stripe?**
Online payment processing platform for credit cards, debit cards, and ACH transfers.

**Why We Use Stripe:**
1. Easy integration (5 lines of code)
2. PCI compliant (secure card handling)
3. Low fees (2.9% + $0.30 per transaction)
4. Supports all major cards
5. Excellent documentation

**Which Modules Use Stripe:**
- Patient Payment Collection (copays, deductibles)
- Online payment portal (future)

**API Integration Example:**
```python
import stripe

stripe.api_key = STRIPE_SECRET_KEY

# Collect patient copay
def collect_copay(patient, amount):
    try:
        # Create payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency="usd",
            payment_method_types=["card"],
            description=f"Copay for {patient.name}",
            metadata={
                "patient_id": patient.patient_id,
                "payment_type": "copay"
            }
        )
        
        return {
            "client_secret": payment_intent.client_secret,
            "payment_intent_id": payment_intent.id
        }
    
    except stripe.error.CardError as e:
        # Card declined
        return {"error": e.user_message}
```

**Frontend Integration (React):**
```jsx
import { loadStripe } from '@stripe/stripe-js';
import { Elements, CardElement, useStripe, useElements } from '@stripe/react-stripe-js';

const stripePromise = loadStripe('pk_test_...');

function PaymentForm({ amount, patientId }) {
  const stripe = useStripe();
  const elements = useElements();
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Get client secret from backend
    const { client_secret } = await fetch('/api/v1/payments/create-intent', {
      method: 'POST',
      body: JSON.stringify({ amount, patientId })
    }).then(r => r.json());
    
    // Confirm payment
    const { error, paymentIntent } = await stripe.confirmCardPayment(client_secret, {
      payment_method: {
        card: elements.getElement(CardElement)
      }
    });
    
    if (error) {
      alert('Payment failed: ' + error.message);
    } else {
      alert('Payment successful!');
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <CardElement />
      <button type="submit">Pay ${amount}</button>
    </form>
  );
}
```

**Stripe Pricing:**
- 2.9% + $0.30 per transaction
- No monthly fees
- **Example:** $25 copay = $1.03 fee

**Stripe Alternatives:**
- Square
- PayPal
- Authorize.net

---

### API 4: Twilio (SMS Notifications) 📱

**What is Twilio?**
Cloud communications platform for SMS, voice, and video.

**Why We Use Twilio:**
1. Reliable SMS delivery (99.95% uptime)
2. Simple API
3. Low cost ($0.0075 per SMS)
4. Two-way messaging support

**Which Modules Use Twilio:**
- Appointment reminders
- Payment confirmations
- Claim status updates

**API Integration Example:**
```python
from twilio.rest import Client

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Send appointment reminder
def send_appointment_reminder(patient, appointment):
    message = client.messages.create(
        body=f"Hi {patient.first_name}, your appointment with Dr. {appointment.provider} "
             f"is tomorrow at {appointment.time}. Reply CONFIRM to confirm.",
        from_="+15551234567",  # Your Twilio number
        to=patient.phone
    )
    
    return message.sid

# Send payment confirmation
def send_payment_confirmation(patient, amount):
    message = client.messages.create(
        body=f"Payment of ${amount} received. Thank you! "
             f"Receipt: {generate_receipt_url()}",
        from_="+15551234567",
        to=patient.phone
    )
    
    return message.sid
```

**Twilio Pricing:**
- SMS: $0.0075 per message (US)
- Phone number: $1/month
- **MVP Estimate:** ~$50/month for 5,000 messages

**Twilio Alternatives:**
- AWS SNS
- MessageBird
- Plivo

---

### API 5: OpenAI API (AI Features) 🤖

**What is OpenAI API?**
Access to GPT-4 and other AI models for natural language processing.

**Why We Use OpenAI:**
1. State-of-the-art AI models
2. Easy to integrate
3. Supports medical terminology
4. Fast response times

**Which Modules Use OpenAI:**
- AI-assisted medical coding
- Claim error prediction
- Chatbot support
- Document summarization

**API Integration Examples:**

#### 1. AI Medical Coding Assistant
```python
import openai

openai.api_key = OPENAI_API_KEY

def suggest_medical_codes(encounter_notes, patient_age, patient_gender):
    prompt = f"""
You are a medical coding expert. Based on the following clinical notes, 
suggest appropriate ICD-10 diagnosis codes and CPT procedure codes.

Patient: {patient_age} year old {patient_gender}

Clinical Notes:
{encounter_notes}

Provide your response in JSON format:
{{
  "icd10_codes": [
    {{"code": "J20.9", "description": "Acute bronchitis", "confidence": 0.95}}
  ],
  "cpt_codes": [
    {{"code": "99213", "description": "Office visit", "confidence": 0.90}}
  ]
}}
"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a medical coding expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,  # Lower temperature for more consistent results
        max_tokens=500
    )
    
    # Parse JSON response
    suggested_codes = json.loads(response.choices[0].message.content)
    return suggested_codes
```

#### 2. Claim Error Prediction
```python
def predict_claim_errors(claim):
    prompt = f"""
Analyze this medical claim for potential errors or denial risks:

Patient Age: {claim.patient_age}
Diagnosis Codes: {claim.diagnosis_codes}
Procedure Codes: {claim.procedure_codes}
Place of Service: {claim.place_of_service}
Insurance: {claim.insurance_type}

Identify potential issues that might cause claim denial.
"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a medical billing expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    
    return response.choices[0].message.content
```

#### 3. AI Chatbot Support
```python
def chatbot_response(user_question, context):
    prompt = f"""
You are a helpful assistant for a medical billing system.

User Question: {user_question}

Context: {context}

Provide a clear, concise answer.
"""
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Cheaper model for chatbot
        messages=[
            {"role": "system", "content": "You are a helpful medical billing assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content
```

**OpenAI Pricing:**
- GPT-4: $0.03 per 1K input tokens, $0.06 per 1K output tokens
- GPT-3.5-turbo: $0.0015 per 1K input tokens, $0.002 per 1K output tokens
- **MVP Estimate:** ~$100-$200/month for 10,000 AI-assisted coding requests

**OpenAI Alternatives:**
- AWS Bedrock (Claude, Llama models)
- Google Vertex AI (PaLM models)
- Azure OpenAI Service

---

### API 6: FHIR APIs (EHR Integration) 🏥

**What is FHIR?**
Fast Healthcare Interoperability Resources - a standard for exchanging healthcare data.

**Why We Use FHIR:**
1. Industry standard for EHR integration
2. Supported by Epic, Cerner, Allscripts
3. RESTful API (easy to integrate)
4. Structured data format

**Which Modules Use FHIR:**
- Pull patient demographics from EHR
- Pull encounter notes from EHR
- Pull diagnosis/procedure codes from EHR

**API Integration Example:**
```python
import requests

# Get patient data from EHR via FHIR
def get_patient_from_ehr(patient_mrn):
    url = f"https://fhir.ehr-system.com/Patient?identifier={patient_mrn}"
    
    headers = {
        "Authorization": f"Bearer {FHIR_ACCESS_TOKEN}",
        "Accept": "application/fhir+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        fhir_patient = response.json()
        
        # Extract patient data
        return {
            "first_name": fhir_patient["name"][0]["given"][0],
            "last_name": fhir_patient["name"][0]["family"],
            "dob": fhir_patient["birthDate"],
            "gender": fhir_patient["gender"],
            "phone": fhir_patient["telecom"][0]["value"]
        }
```

**FHIR Resources We'll Use:**
- Patient (demographics)
- Encounter (visits)
- Condition (diagnoses)
- Procedure (procedures)
- Coverage (insurance)

**FHIR Pricing:**
- Varies by EHR vendor
- Epic: $5,000-$10,000 setup + $500/month
- Cerner: Similar pricing
- **MVP:** Can be mocked initially, integrate later

---

## API Mocking Strategy for MVP

**Not all APIs need to be integrated on Day 1.** Here's what we can mock:

### Can Be Mocked Initially ✅

1. **FHIR APIs (EHR Integration)**
   - **Why:** Complex setup, requires EHR vendor coordination
   - **Mock:** Manual data entry for patient demographics
   - **Integrate:** Phase 3 (after MVP launch)

2. **Twilio (SMS Notifications)**
   - **Why:** Nice-to-have, not critical for core workflow
   - **Mock:** Email notifications instead
   - **Integrate:** Phase 2

3. **Advanced AI Features**
   - **Why:** Can start with basic rule-based coding
   - **Mock:** Manual code selection with search
   - **Integrate:** Phase 4

### Must Be Real from Day 1 ❌

1. **Waystar/Availity (Clearinghouse)**
   - **Why:** Core functionality - can't submit claims without it
   - **Must integrate:** Phase 1

2. **Stripe (Payments)**
   - **Why:** Need to collect copays
   - **Must integrate:** Phase 2

3. **PostgreSQL Database**
   - **Why:** Core data storage
   - **Must integrate:** Phase 1

---

## 7. AI Usage in MVP

### AI Feature 1: OCR for Document Reading 📄

**Use Case:** Extract data from insurance cards, ID cards, referral forms.

**How It Works:**
1. User uploads image of insurance card
2. OCR extracts text
3. AI parses and structures data
4. Auto-fills patient/insurance form

**Technology Options:**

#### Option 1: AWS Textract (Recommended for MVP)
```python
import boto3

textract = boto3.client('textract')

def extract_insurance_card_data(image_bytes):
    # Call AWS Textract
    response = textract.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['FORMS', 'TABLES']
    )
    
    # Extract key-value pairs
    insurance_data = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = block.get('Key', '')
            value = block.get('Value', '')
            
            if 'member id' in key.lower():
                insurance_data['policy_number'] = value
            elif 'group' in key.lower():
                insurance_data['group_number'] = value
            # ... more parsing logic
    
    return insurance_data
```

**AWS Textract Pricing:**
- $1.50 per 1,000 pages
- **MVP Estimate:** ~$10/month for 500 cards

#### Option 2: OpenAI Vision API
```python
import openai

def extract_insurance_card_with_gpt4_vision(image_url):
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract insurance information from this card. "
                                "Return JSON with: insurance_company, policy_number, "
                                "group_number, member_name, effective_date"
                    },
                    {
                        "type": "image_url",
                        "image_url": image_url
                    }
                ]
            }
        ],
        max_tokens=300
    )
    
    return json.loads(response.choices[0].message.content)
```

**Benefits:**
- ⚡ Saves 2-3 minutes per patient registration
- ✅ Reduces data entry errors
- 😊 Better user experience

---

### AI Feature 2: AI Medical Coding Suggestion 🏥

**Use Case:** Suggest ICD-10 and CPT codes based on doctor's notes.

**How It Works:**
1. Doctor documents encounter in EHR
2. AI analyzes clinical notes
3. Suggests diagnosis and procedure codes
4. Coder reviews and confirms

**Implementation (OpenAI GPT-4):**
```python
def ai_suggest_codes(clinical_notes, patient_info):
    prompt = f"""
You are an expert medical coder. Analyze these clinical notes and suggest 
appropriate ICD-10 diagnosis codes and CPT procedure codes.

Patient: {patient_info['age']} year old {patient_info['gender']}

Clinical Notes:
{clinical_notes}

Guidelines:
- Suggest primary diagnosis first
- Include all relevant secondary diagnoses
- Suggest appropriate E&M code (99201-99215)
- Consider medical necessity
- Provide confidence scores

Return JSON format:
{{
  "icd10_codes": [
    {{"code": "...", "description": "...", "confidence": 0.95, "is_primary": true}}
  ],
  "cpt_codes": [
    {{"code": "...", "description": "...", "confidence": 0.90}}
  ],
  "reasoning": "Brief explanation"
}}
"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert medical coder with 10 years of experience."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,  # Low temperature for consistency
        max_tokens=800
    )
    
    return json.loads(response.choices[0].message.content)
```

**Benefits:**
- ⚡ Reduces coding time from 10 minutes to 2 minutes
- ✅ Improves coding accuracy (fewer denials)
- 📚 Helps train new coders

**Accuracy:**
- GPT-4 achieves ~85-90% accuracy on medical coding
- Always requires human review
- Learns from corrections over time

---

### AI Feature 3: Claim Error Prediction 🔍

**Use Case:** Predict which claims are likely to be denied before submission.

**How It Works:**
1. Claim is created
2. AI analyzes claim data
3. Predicts denial risk (low/medium/high)
4. Suggests corrections

**Implementation:**
```python
def predict_claim_denial_risk(claim):
    # Prepare claim data for AI analysis
    claim_summary = f"""
Claim Analysis:
- Patient Age: {claim.patient_age}
- Gender: {claim.patient_gender}
- Insurance: {claim.insurance_name}
- Diagnosis Codes: {', '.join(claim.diagnosis_codes)}
- Procedure Codes: {', '.join(claim.procedure_codes)}
- Place of Service: {claim.place_of_service}
- Total Charge: ${claim.total_charge}
- Prior Authorization: {'Yes' if claim.has_prior_auth else 'No'}
"""
    
    prompt = f"""
You are a medical billing expert. Analyze this claim for potential denial risks.

{claim_summary}

Identify:
1. Denial risk level (Low/Medium/High)
2. Specific issues that might cause denial
3. Recommendations to fix issues

Return JSON format:
{{
  "risk_level": "Low|Medium|High",
  "risk_score": 0.0-1.0,
  "issues": [
    {{"issue": "...", "severity": "...", "recommendation": "..."}}
  ]
}}
"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a medical billing expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    
    return json.loads(response.choices[0].message.content)
```

**Example Output:**
```json
{
  "risk_level": "High",
  "risk_score": 0.85,
  "issues": [
    {
      "issue": "Diagnosis code J20.9 may not support medical necessity for CPT 99215",
      "severity": "High",
      "recommendation": "Consider using CPT 99213 instead, or add supporting diagnosis"
    },
    {
      "issue": "No prior authorization on file",
      "severity": "Medium",
      "recommendation": "Verify if prior auth is required for this procedure"
    }
  ]
}
```

**Benefits:**
- 🎯 Catch errors before submission
- 💰 Reduce denial rate from 10% to 5%
- ⚡ Faster claim resolution

---

### AI Feature 4: AI Chatbot Support 💬

**Use Case:** Help users navigate the system and answer billing questions.

**How It Works:**
1. User asks question in chat widget
2. AI searches knowledge base
3. Provides answer with sources
4. Escalates to human if needed

**Implementation:**
```python
def chatbot_answer(user_question, user_context):
    # Search knowledge base for relevant info
    knowledge_base_results = search_knowledge_base(user_question)
    
    prompt = f"""
You are a helpful assistant for a medical billing system.

User Question: {user_question}

User Context:
- Role: {user_context['role']}
- Current Page: {user_context['current_page']}

Relevant Information:
{knowledge_base_results}

Provide a clear, step-by-step answer. If you don't know, say so and suggest 
contacting support.
"""
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Cheaper for chatbot
        messages=[
            {"role": "system", "content": "You are a helpful medical billing assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content
```

**Example Conversations:**

**User:** "How do I verify insurance?"  
**Bot:** "To verify insurance:
1. Open the patient record
2. Click the 'Verify Insurance' button
3. Wait 10-30 seconds for results
4. Review coverage status and copay amount

Would you like me to show you a video tutorial?"

**User:** "Why was my claim denied?"  
**Bot:** "I can help you understand claim denials. Please provide the claim number, and I'll look up the denial reason and suggest next steps."

**Benefits:**
- 📞 Reduces support tickets by 30%
- ⚡ Instant answers 24/7
- 😊 Better user experience

---

## AWS Bedrock as Alternative to OpenAI

**What is AWS Bedrock?**
AWS service providing access to multiple AI models (Claude, Llama, etc.)

**Why Consider Bedrock:**
1. Multiple model options
2. Better for high-volume usage
3. Integrated with AWS infrastructure
4. HIPAA eligible

**Example with Claude:**
```python
import boto3

bedrock = boto3.client('bedrock-runtime')

def suggest_codes_with_claude(clinical_notes):
    prompt = f"Suggest ICD-10 and CPT codes for: {clinical_notes}"
    
    response = bedrock.invoke_model(
        modelId='anthropic.claude-v2',
        body=json.dumps({
            "prompt": prompt,
            "max_tokens_to_sample": 500
        })
    )
    
    return json.loads(response['body'].read())
```

**Pricing Comparison:**

| Service | Model | Cost per 1M tokens |
|---------|-------|-------------------|
| OpenAI | GPT-4 | $30 (input) + $60 (output) |
| OpenAI | GPT-3.5-turbo | $1.50 (input) + $2 (output) |
| AWS Bedrock | Claude 2 | $8 (input) + $24 (output) |
| AWS Bedrock | Llama 2 | $0.75 (input) + $1 (output) |

**MVP Recommendation:**
- Start with **OpenAI GPT-4** (easier integration, better results)
- Switch to **AWS Bedrock** later if cost becomes an issue

---

**Next:** Part 5 will cover the Development Plan, Team Responsibilities, and Timeline.

---

**Document Navigation:**
- **Part 1:** Introduction & Goals
- **Part 2:** Modules & Features
- **Part 3:** Workflow & Tech Stack
- **Part 4:** APIs & AI Integration (This document)
- **Part 5:** Development Plan & Timeline
