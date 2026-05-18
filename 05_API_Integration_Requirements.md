# Healthcare RCM Application - API Integration Requirements

**Version:** 1.0  
**Date:** May 18, 2026  
**For:** Development Team

---

## 1. Overview

This document defines all external system integrations required for the RCM application.

**Total Integrations:** 8 major integration points  
**Integration Standards:** HL7 v2.x, HL7 FHIR, EDI X12, REST APIs

---

## 2. Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     RCM Application                          │
└─────────────────────────────────────────────────────────────┘
         │           │           │           │           │
         ▼           ▼           ▼           ▼           ▼
    ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
    │  EMR   │  │  Lab   │  │Imaging │  │ Payer  │  │Clearing│
    │ System │  │ System │  │ (PACS) │  │ Portal │  │ house  │
    └────────┘  └────────┘  └────────┘  └────────┘  └────────┘
```

---

## 3. Integration 1: EMR/EHR System

### Purpose:
Bi-directional integration with Electronic Medical Record system to exchange patient demographics, clinical documentation, and encounter data.

### Integration Standard:
- **Primary:** HL7 v2.x messages
- **Alternative:** HL7 FHIR REST API

### Data Flow Direction:
**EMR → RCM (Inbound):**
- Patient demographics (ADT messages)
- Encounter details
- Clinical documentation (SOAP notes)
- Diagnoses (ICD-10 codes)
- Procedures (CPT codes)
- Orders (lab, imaging, medications)
- Results (lab, imaging)

**RCM → EMR (Outbound):**
- Insurance eligibility status
- Authorization status
- Claim status
- Payment status
- Patient balance

---

### HL7 v2.x Message Types:

#### ADT Messages (Patient Administration):

**ADT^A01 - Patient Admission**
```
MSH|^~\&|EMR_SYSTEM|HOSPITAL|RCM_SYSTEM|HOSPITAL|20260518143000||ADT^A01|MSG00001|P|2.5
EVN|A01|20260518143000
PID|1||MRN123456||Doe^John^A||19800115|M|||123 Main St^^Boston^MA^02101||555-1234|||S
PV1|1|I|ICU^101^01||||123456^Smith^Jane^MD
IN1|1|BCBS001|BCBS|Blue Cross Blue Shield||||GRP123456|POL987654
```

**ADT^A04 - Patient Registration**
**ADT^A08 - Patient Information Update**
**ADT^A11 - Cancel Admission**

#### DFT Messages (Financial Transactions):

**DFT^P03 - Post Detail Financial Transaction**
```
MSH|^~\&|EMR_SYSTEM|HOSPITAL|RCM_SYSTEM|HOSPITAL|20260518143000||DFT^P03|MSG00002|P|2.5
PID|1||MRN123456||Doe^John^A
FT1|1||99213|20260518|20260518|CG|1|150.00||CPT|99213^Office Visit Level 3
```

#### ORM Messages (Orders):

**ORM^O01 - General Order Message**
```
MSH|^~\&|EMR_SYSTEM|HOSPITAL|LAB_SYSTEM|HOSPITAL|20260518143000||ORM^O01|MSG00003|P|2.5
PID|1||MRN123456||Doe^John^A
ORC|NW|ORD123456|||||^^^20260518143000
OBR|1|ORD123456||CBC^Complete Blood Count^CPT|||20260518143000
```

#### ORU Messages (Results):

**ORU^R01 - Observation Result**
```
MSH|^~\&|LAB_SYSTEM|HOSPITAL|RCM_SYSTEM|HOSPITAL|20260518150000||ORU^R01|MSG00004|P|2.5
PID|1||MRN123456||Doe^John^A
OBR|1|ORD123456||CBC^Complete Blood Count^CPT|||20260518143000
OBX|1|NM|WBC^White Blood Count||7.5|10^3/uL|4.0-11.0|N|||F
OBX|2|NM|RBC^Red Blood Count||4.8|10^6/uL|4.2-5.4|N|||F
```

---

### HL7 FHIR API (Alternative):

**Base URL:** `https://emr-system.hospital.com/fhir/R4`

**Authentication:** OAuth 2.0 with client credentials

#### FHIR Resources:

**1. Patient Resource**
```http
GET /Patient/123456
Authorization: Bearer {access_token}
```

Response:
```json
{
  "resourceType": "Patient",
  "id": "123456",
  "identifier": [
    {
      "system": "http://hospital.com/mrn",
      "value": "MRN123456"
    }
  ],
  "name": [
    {
      "family": "Doe",
      "given": ["John", "A"]
    }
  ],
  "birthDate": "1980-01-15",
  "gender": "male",
  "address": [
    {
      "line": ["123 Main St"],
      "city": "Boston",
      "state": "MA",
      "postalCode": "02101"
    }
  ]
}
```

**2. Encounter Resource**
```http
GET /Encounter/789012
```

**3. Condition Resource (Diagnoses)**
```http
GET /Condition?patient=123456&encounter=789012
```

**4. Procedure Resource**
```http
GET /Procedure?patient=123456&encounter=789012
```

**5. DiagnosticReport Resource (Lab/Imaging Results)**
```http
GET /DiagnosticReport?patient=123456
```

---

### Implementation Requirements:

**HL7 v2.x:**
- **Protocol:** MLLP (Minimum Lower Layer Protocol) over TCP/IP
- **Port:** 6661 (configurable)
- **Message Encoding:** ER7 (pipe-delimited)
- **Acknowledgment:** ACK messages required for all inbound messages

**FHIR API:**
- **Protocol:** HTTPS REST
- **Authentication:** OAuth 2.0
- **Data Format:** JSON
- **Pagination:** Support for large result sets

**Error Handling:**
- Retry failed messages 3 times with exponential backoff
- Log all failed messages for manual review
- Alert integration team if >10 messages fail in 1 hour

**Data Mapping:**
- Map HL7 PID segment → patients table
- Map HL7 DFT segment → charges table
- Map HL7 OBR/OBX segments → orders and results

---

## 4. Integration 2: Clearinghouse

### Purpose:
Submit insurance claims electronically and receive acknowledgments and payments.

### Supported Clearinghouses:
- Waystar
- Availity
- Change Healthcare
- Office Ally
- Trizetto

### Integration Standard:
**EDI X12 (HIPAA 5010)**

---

### EDI Transaction Sets:

#### 1. EDI 837 - Claims Submission

**837P (Professional Claims - CMS-1500)**
**837I (Institutional Claims - UB-04)**

**Transmission Method:** SFTP or API

**File Format:**
```
ISA*00*          *00*          *ZZ*SENDER_ID      *ZZ*RECEIVER_ID    *260518*1430*^*00501*000000001*0*P*:~
GS*HC*SENDER_ID*RECEIVER_ID*20260518*1430*1*X*005010X222A1~
ST*837*0001*005010X222A1~
BHT*0019*00*CLM123456*20260518*1430*CH~
NM1*41*2*HOSPITAL_NAME*****46*1234567890~
NM1*40*2*BLUE_CROSS*****46*BCBS001~
HL*1**20*1~
NM1*85*2*BILLING_PROVIDER*****XX*1234567890~
N3*123 Hospital Ave~
N4*Boston*MA*02101~
HL*2*1*22*0~
SBR*P*18*GRP123456******CI~
NM1*IL*1*DOE*JOHN*A***MI*POL987654~
NM1*PR*2*BLUE_CROSS*****PI*BCBS001~
CLM*CLM123456*150.00***11:B:1*Y*A*Y*Y~
DTP*472*D8*20260518~
REF*D9*AUTH123456~
HI*ABK:E119~
LX*1~
SV1*HC:99213*150.00*UN*1***1~
DTP*472*D8*20260518~
SE*25*0001~
GE*1*1~
IEA*1*000000001~
```

**Submission Frequency:** Every 2 hours (configurable)

---

#### 2. EDI 270/271 - Eligibility Inquiry/Response

**270 - Eligibility Inquiry (Outbound)**
```
ISA*00*          *00*          *ZZ*SENDER_ID      *ZZ*PAYER_ID       *260518*1430*^*00501*000000001*0*P*:~
GS*HS*SENDER_ID*PAYER_ID*20260518*1430*1*X*005010X279A1~
ST*270*0001*005010X279A1~
BHT*0022*13*ELG123456*20260518*1430~
HL*1**20*1~
NM1*PR*2*BLUE_CROSS*****PI*BCBS001~
HL*2*1*21*1~
NM1*1P*2*HOSPITAL_NAME*****XX*1234567890~
HL*3*2*22*0~
TRN*1*ELG123456*SENDER_ID~
NM1*IL*1*DOE*JOHN*A***MI*POL987654~
DMG*D8*19800115*M~
DTP*291*D8*20260518~
EQ*30~
SE*12*0001~
GE*1*1~
IEA*1*000000001~
```

**271 - Eligibility Response (Inbound)**
```
ISA*00*          *00*          *ZZ*PAYER_ID       *ZZ*SENDER_ID      *260518*1431*^*00501*000000002*0*P*:~
GS*HB*PAYER_ID*SENDER_ID*20260518*1431*2*X*005010X279A1~
ST*271*0002*005010X279A1~
BHT*0022*11*ELG123456*20260518*1431~
HL*1**20*1~
NM1*PR*2*BLUE_CROSS*****PI*BCBS001~
HL*2*1*21*1~
NM1*1P*2*HOSPITAL_NAME*****XX*1234567890~
HL*3*2*22*0~
TRN*2*ELG123456*SENDER_ID~
NM1*IL*1*DOE*JOHN*A***MI*POL987654~
N3*123 Main St~
N4*Boston*MA*02101~
DMG*D8*19800115*M~
EB*1**30**BLUE_CROSS PPO~
EB*C**30**DEDUCTIBLE~
AMT*D8*1500.00~
AMT*D9*500.00~
EB*C**30**COPAY~
AMT*D8*30.00~
SE*18*0002~
GE*1*2~
IEA*1*000000002~
```

**Real-Time:** Response within 5 seconds

---

#### 3. EDI 276/277 - Claim Status Inquiry/Response

**276 - Claim Status Inquiry (Outbound)**
**277 - Claim Status Response (Inbound)**

---

#### 4. EDI 835 - Payment/Remittance Advice (ERA)

**Inbound from Clearinghouse**

```
ISA*00*          *00*          *ZZ*PAYER_ID       *ZZ*RECEIVER_ID    *260520*1000*^*00501*000000003*0*P*:~
GS*HP*PAYER_ID*RECEIVER_ID*20260520*1000*3*X*005010X221A1~
ST*835*0003*005010X221A1~
BPR*I*1500.00*C*ACH*CCP*01*123456789*DA*987654321**01*987654321*DA*123456789*20260520~
TRN*1*CHK123456*1234567890~
REF*EV*BCBS001~
DTM*405*20260520~
N1*PR*BLUE_CROSS~
N3*PO Box 12345~
N4*Boston*MA*02101~
N1*PE*HOSPITAL_NAME*XX*1234567890~
LX*1~
CLP*CLM123456*1*150.00*120.00**12*ICN987654321*11~
NM1*QC*1*DOE*JOHN*A~
NM1*82*1*SMITH*JANE*MD***XX*9876543210~
DTM*232*20260518~
DTM*233*20260518~
AMT*AU*150.00~
AMT*D*30.00~
SVC*HC:99213*150.00*120.00**1~
DTM*472*20260518~
CAS*CO*45*30.00~
CAS*PR*1*30.00~
AMT*B6*120.00~
SE*23*0003~
GE*1*3~
IEA*1*000000003~
```

**Adjustment Reason Codes (CARC):**
- CO-45: Contractual adjustment
- PR-1: Deductible
- PR-2: Coinsurance
- PR-3: Copay
- CO-16: Claim lacks information
- CO-97: Service not covered

---

### Clearinghouse API Integration (Alternative to EDI):

**Example: Waystar API**

**Base URL:** `https://api.waystar.com/v1`

**Authentication:** API Key + OAuth 2.0

**Submit Claim:**
```http
POST /claims
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "claim": {
    "claimNumber": "CLM123456",
    "patient": {
      "firstName": "John",
      "lastName": "Doe",
      "dob": "1980-01-15",
      "memberId": "POL987654"
    },
    "payer": {
      "payerId": "BCBS001",
      "payerName": "Blue Cross Blue Shield"
    },
    "provider": {
      "npi": "1234567890",
      "name": "Hospital Name"
    },
    "serviceLines": [
      {
        "cptCode": "99213",
        "chargeAmount": 150.00,
        "units": 1,
        "serviceDate": "2026-05-18",
        "diagnosisCodes": ["E11.9"]
      }
    ]
  }
}
```

**Check Eligibility:**
```http
POST /eligibility
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "patient": {
    "firstName": "John",
    "lastName": "Doe",
    "dob": "1980-01-15",
    "memberId": "POL987654"
  },
  "payer": {
    "payerId": "BCBS001"
  },
  "serviceDate": "2026-05-18"
}
```

---

## 5. Integration 3: Payer Portals

### Purpose:
Direct integration with major insurance payers for eligibility, authorization, claim submission, and status checks.

### Supported Payers:
- Medicare (CMS)
- Medicaid (state-specific)
- Blue Cross Blue Shield
- UnitedHealthcare
- Aetna
- Cigna
- Humana

---

### Medicare Integration:

**Medicare Provider Portal API**

**Base URL:** `https://api.cms.gov/v1`

**Authentication:** OAuth 2.0 + Provider NPI

**Check Eligibility:**
```http
GET /eligibility?beneficiaryId={MBI}&serviceDate={date}
Authorization: Bearer {access_token}
```

**Submit Claim:**
```http
POST /claims
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "claimType": "professional",
  "beneficiaryMBI": "1EG4TE5MK73",
  "providerNPI": "1234567890",
  "serviceDate": "2026-05-18",
  "diagnosisCodes": ["E11.9"],
  "serviceLinesLines": [
    {
      "cptCode": "99213",
      "chargeAmount": 150.00
    }
  ]
}
```

---

### Commercial Payer Integration:

**Example: Availity API (Multi-Payer Gateway)**

**Base URL:** `https://api.availity.com/v1`

**Real-Time Eligibility:**
```http
POST /eligibility
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "payerId": "BCBS001",
  "provider": {
    "npi": "1234567890"
  },
  "subscriber": {
    "memberId": "POL987654",
    "firstName": "John",
    "lastName": "Doe",
    "dob": "1980-01-15"
  },
  "serviceDate": "2026-05-18"
}
```

**Prior Authorization Status:**
```http
GET /authorizations/{authNumber}
Authorization: Bearer {access_token}
```

---

## 6. Integration 4: Laboratory System

### Purpose:
Receive lab orders and results.

### Integration Standard:
**HL7 v2.x ORM/ORU messages**

**Outbound (RCM → Lab):**
- ORM^O01: Lab order

**Inbound (Lab → RCM):**
- ORU^R01: Lab result

**Charge Capture Trigger:**
When ORU^R01 received → Auto-generate lab charge based on CPT code in OBR segment

---

## 7. Integration 5: Radiology/PACS System

### Purpose:
Receive imaging orders and results.

### Integration Standard:
**HL7 v2.x ORM/ORU messages**

**Outbound (RCM → PACS):**
- ORM^O01: Imaging order

**Inbound (PACS → RCM):**
- ORU^R01: Imaging result

**Charge Capture Trigger:**
When ORU^R01 received → Auto-generate imaging charge

---

## 8. Integration 6: Pharmacy System

### Purpose:
Receive medication dispensing records for charge capture.

### Integration Standard:
**HL7 v2.x RDE/RDS messages**

**Inbound (Pharmacy → RCM):**
- RDS^O13: Pharmacy dispense

**Charge Capture Trigger:**
When medication dispensed → Auto-generate medication charge (HCPCS J-code)

---

## 9. Integration 7: Payment Gateway

### Purpose:
Process patient credit card and ACH payments.

### Supported Gateways:
- Stripe
- Square
- Authorize.Net
- PayPal

---

### Stripe Integration:

**Base URL:** `https://api.stripe.com/v1`

**Authentication:** API Secret Key

**Create Payment Intent:**
```http
POST /payment_intents
Authorization: Bearer {secret_key}
Content-Type: application/x-www-form-urlencoded

amount=5000&currency=usd&payment_method_types[]=card
```

**Confirm Payment:**
```http
POST /payment_intents/{intent_id}/confirm
Authorization: Bearer {secret_key}
Content-Type: application/x-www-form-urlencoded

payment_method=pm_card_visa
```

**Webhooks:**
- `payment_intent.succeeded`
- `payment_intent.payment_failed`
- `charge.refunded`

**Webhook Endpoint:** `https://rcm-app.hospital.com/api/webhooks/stripe`

---

## 10. Integration 8: Health Information Exchange (HIE)

### Purpose:
Share patient data with regional/national health information networks.

### Integration Standard:
**HL7 FHIR**

**Query Patient Data:**
```http
GET /Patient?identifier=MRN123456
Authorization: Bearer {access_token}
```

**Submit Encounter Data:**
```http
POST /Encounter
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "resourceType": "Encounter",
  "status": "finished",
  "class": {
    "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
    "code": "AMB"
  },
  "subject": {
    "reference": "Patient/123456"
  },
  "period": {
    "start": "2026-05-18T14:30:00Z",
    "end": "2026-05-18T15:00:00Z"
  }
}
```

---

## 11. Integration Summary Table

| Integration | Standard | Direction | Frequency | Critical? |
|-------------|----------|-----------|-----------|-----------|
| EMR/EHR | HL7 v2.x / FHIR | Bi-directional | Real-time | ✅ Yes |
| Clearinghouse | EDI X12 | Bi-directional | Batch (2 hours) | ✅ Yes |
| Payer Portals | REST API / EDI | Bi-directional | Real-time | ✅ Yes |
| Lab System | HL7 v2.x | Bi-directional | Real-time | ⚠️ Medium |
| PACS | HL7 v2.x | Bi-directional | Real-time | ⚠️ Medium |
| Pharmacy | HL7 v2.x | Inbound | Real-time | ⚠️ Medium |
| Payment Gateway | REST API | Outbound | Real-time | ✅ Yes |
| HIE | FHIR | Bi-directional | On-demand | ❌ No |

---

## 12. Error Handling & Monitoring

### Retry Logic:
- Failed API calls: Retry 3 times with exponential backoff (1s, 5s, 15s)
- Failed HL7 messages: Retry 3 times, then move to error queue
- Failed EDI transmissions: Retry next batch cycle

### Monitoring:
- Integration health dashboard
- Alert if >10% of messages fail
- Alert if no messages received in 1 hour (for real-time integrations)
- Daily integration summary report

### Logging:
- Log all inbound/outbound messages
- Log all API requests/responses
- Retention: 90 days

---

## 13. Security Requirements

### Authentication:
- OAuth 2.0 for REST APIs
- API keys for clearinghouse/payer portals
- Mutual TLS for HL7 connections

### Encryption:
- TLS 1.2+ for all connections
- Encrypt sensitive data in logs

### Compliance:
- HIPAA-compliant data transmission
- Business Associate Agreements (BAA) with all vendors

---

## 14. Testing Requirements

### Integration Testing:
- Test environment for each integration
- Sample HL7/EDI messages for unit testing
- Mock API responses for development

### Certification:
- Clearinghouse certification testing
- Payer connectivity testing
- HL7 conformance testing

---

**Next Document:** UI/UX Workflow Wireframes
