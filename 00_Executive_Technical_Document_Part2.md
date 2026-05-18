# Healthcare RCM Application - Executive Technical Document (Part 2)

**Continuation from Part 1**

---

## 3. System Architecture

### 3.1 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Web App    │  │  Mobile App  │  │ Patient      │          │
│  │   (React)    │  │ (React Native│  │ Portal       │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTPS/REST API
┌────────────────────────┼────────────────────────────────────────┐
│                    API GATEWAY LAYER                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  API Gateway (AWS API Gateway / Kong)                     │  │
│  │  - Rate Limiting                                          │  │
│  │  - Authentication (JWT)                                   │  │
│  │  - Request Routing                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────┼────────────────────────────────────────┐
│                  APPLICATION LAYER (Microservices)               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  Patient    │  │  Encounter  │  │  Coding     │            │
│  │  Service    │  │  Service    │  │  Service    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  Claim      │  │  Payment    │  │  Denial     │            │
│  │  Service    │  │  Service    │  │  Service    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  Reporting  │  │  AI/ML      │  │  Audit      │            │
│  │  Service    │  │  Service    │  │  Service    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────┼────────────────────────────────────────┐
│                     DATA LAYER                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ PostgreSQL   │  │ Redis Cache  │  │ S3 Storage   │          │
│  │ (Primary DB) │  │ (Session/    │  │ (Documents)  │          │
│  │              │  │  Cache)      │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────┼────────────────────────────────────────┐
│                  INTEGRATION LAYER                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ Clearinghouse│  │ EMR/EHR    │  │ Payment     │            │
│  │ (Waystar)   │  │ (HL7/FHIR) │  │ Gateway     │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ AI Services │  │ Notification│  │ Payer APIs  │            │
│  │ (OpenAI/AWS)│  │ (Twilio)    │  │             │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Detailed Component Architecture

#### **Frontend Architecture**

```
React Application
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── common/          # Buttons, inputs, modals
│   │   ├── patient/         # Patient-specific components
│   │   ├── claims/          # Claim-specific components
│   │   └── dashboard/       # Dashboard widgets
│   ├── pages/               # Page-level components
│   │   ├── PatientSearch.tsx
│   │   ├── EncounterDetail.tsx
│   │   ├── ClaimWorkList.tsx
│   │   └── Dashboard.tsx
│   ├── services/            # API integration
│   │   ├── api.ts           # Axios client
│   │   ├── patientService.ts
│   │   ├── claimService.ts
│   │   └── authService.ts
│   ├── store/               # Redux state management
│   │   ├── slices/
│   │   │   ├── authSlice.ts
│   │   │   ├── patientSlice.ts
│   │   │   └── claimSlice.ts
│   │   └── store.ts
│   ├── hooks/               # Custom React hooks
│   ├── utils/               # Helper functions
│   └── App.tsx              # Root component
```

**Key Technologies:**
- **React 18+** with TypeScript
- **Redux Toolkit** for state management
- **React Query** for server state caching
- **TailwindCSS** for styling
- **shadcn/ui** for component library
- **React Router** for navigation
- **Axios** for HTTP requests

#### **Backend Architecture (Microservices)**

```
Backend Services
├── patient-service/
│   ├── app/
│   │   ├── api/             # REST endpoints
│   │   ├── models/          # Database models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   └── utils/           # Helper functions
│   ├── tests/
│   └── main.py
├── claim-service/
├── payment-service/
├── ai-service/
└── shared/
    ├── auth/                # JWT authentication
    ├── database/            # DB connection
    └── messaging/           # RabbitMQ/Kafka
```

**Key Technologies:**
- **Python 3.11+** with FastAPI
- **SQLAlchemy** ORM
- **Pydantic** for data validation
- **Celery** for background tasks
- **RabbitMQ** for message queue
- **Redis** for caching
- **Alembic** for database migrations

#### **Database Architecture**

**PostgreSQL Schema:**
```
rcm_database
├── Core Tables (35 tables)
│   ├── users, roles
│   ├── patients, patient_insurance
│   ├── providers, facilities
│   ├── payers
│   ├── encounters, encounter_diagnoses, encounter_procedures
│   ├── charges, chargemaster
│   ├── claims, claim_lines
│   ├── payments, payment_lines
│   ├── denials, appeals
│   ├── authorizations
│   └── audit_logs
├── Indexes (50+ indexes)
│   ├── Primary keys (UUID)
│   ├── Foreign keys
│   ├── Composite indexes (patient_id + date)
│   └── Partial indexes (active records only)
└── Partitioning
    ├── audit_logs (by month)
    └── claims (by submission_date)
```

**Redis Cache Structure:**
```
Redis Keys
├── eligibility:{policy_number}:{date}    # TTL: 15 min
├── payers:all                             # TTL: 24 hours
├── providers:active                       # TTL: 24 hours
├── icd10_codes:{code}                     # TTL: 7 days
├── cpt_codes:{code}                       # TTL: 7 days
└── session:{user_id}                      # TTL: 15 min
```

---

## 4. Recommended Technology Stack

### 4.1 Frontend Stack

| Component | Technology | Why This Choice |
|-----------|-----------|-----------------|
| **Framework** | React.js 18+ | Industry standard, large ecosystem, component reusability |
| **Language** | TypeScript | Type safety, better IDE support, fewer runtime errors |
| **Styling** | TailwindCSS | Utility-first, fast development, consistent design |
| **UI Components** | shadcn/ui | Accessible, customizable, modern design |
| **State Management** | Redux Toolkit | Predictable state, DevTools, middleware support |
| **Data Fetching** | React Query | Automatic caching, background refetch, optimistic updates |
| **Routing** | React Router v6 | Standard routing library, nested routes |
| **Forms** | React Hook Form | Performance, validation, easy integration |
| **Charts** | Recharts | React-native charts, responsive, customizable |
| **HTTP Client** | Axios | Interceptors, request cancellation, timeout handling |

**Package.json:**
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.0.0",
    "@reduxjs/toolkit": "^1.9.5",
    "@tanstack/react-query": "^4.29.0",
    "react-router-dom": "^6.11.0",
    "react-hook-form": "^7.43.0",
    "axios": "^1.4.0",
    "tailwindcss": "^3.3.0",
    "recharts": "^2.5.0",
    "date-fns": "^2.30.0",
    "zod": "^3.21.0"
  }
}
```

### 4.2 Backend Stack

| Component | Technology | Why This Choice |
|-----------|-----------|-----------------|
| **Framework** | FastAPI (Python) | Fast, async support, automatic API docs, type hints |
| **Language** | Python 3.11+ | Rich healthcare libraries, AI/ML ecosystem, readable |
| **ORM** | SQLAlchemy 2.0 | Mature, supports complex queries, migrations |
| **Validation** | Pydantic v2 | Data validation, serialization, FastAPI integration |
| **Task Queue** | Celery + Redis | Distributed tasks, retry logic, scheduling |
| **API Docs** | OpenAPI/Swagger | Auto-generated from FastAPI, interactive testing |
| **Authentication** | OAuth2 + JWT | Industry standard, stateless, scalable |
| **Testing** | Pytest | Comprehensive, fixtures, async support |
| **Logging** | Loguru | Structured logging, easy configuration |

**Requirements.txt:**
```
fastapi==0.100.0
uvicorn[standard]==0.23.0
sqlalchemy==2.0.19
pydantic==2.1.0
alembic==1.11.1
celery==5.3.1
redis==4.6.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pytest==7.4.0
loguru==0.7.0
```

**Alternative: Node.js Stack**
```
- Express.js + TypeScript
- Prisma ORM
- Bull (job queue)
- Passport.js (auth)
- Jest (testing)
```

### 4.3 Database Stack

| Component | Technology | Why This Choice |
|-----------|-----------|-----------------|
| **Primary Database** | PostgreSQL 15+ | ACID compliance, JSON support, mature, HIPAA-ready |
| **Cache** | Redis 7+ | In-memory speed, pub/sub, session storage |
| **Search** | PostgreSQL Full-Text | Built-in, no additional service needed |
| **Data Warehouse** | PostgreSQL (separate instance) | Same technology, easier ETL |
| **File Storage** | AWS S3 / Azure Blob | Scalable, encrypted, versioned, HIPAA-compliant |

**PostgreSQL Extensions:**
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";      -- UUID generation
CREATE EXTENSION IF NOT EXISTS "pg_trgm";        -- Fuzzy text search
CREATE EXTENSION IF NOT EXISTS "btree_gin";      -- Index optimization
CREATE EXTENSION IF NOT EXISTS "timescaledb";    -- Time-series data
```

### 4.4 Cloud & DevOps Stack

| Component | Technology | Why This Choice |
|-----------|-----------|-----------------|
| **Cloud Provider** | AWS | HIPAA-compliant, comprehensive services, market leader |
| **Compute** | ECS Fargate | Serverless containers, auto-scaling, no server management |
| **Database** | RDS PostgreSQL | Managed, automated backups, Multi-AZ, encryption |
| **Cache** | ElastiCache Redis | Managed Redis, automatic failover |
| **Storage** | S3 | Encrypted, versioned, lifecycle policies |
| **Load Balancer** | Application Load Balancer | Layer 7, SSL termination, health checks |
| **CDN** | CloudFront | Global edge locations, HTTPS, caching |
| **Monitoring** | CloudWatch | Metrics, logs, alarms, dashboards |
| **Secrets** | AWS Secrets Manager | Encrypted, automatic rotation |
| **CI/CD** | GitHub Actions | Free, integrated, Docker support |
| **Containers** | Docker | Consistent environments, easy deployment |
| **Orchestration** | Kubernetes (EKS) | Production-grade, auto-scaling, self-healing |

**Alternative: Azure Stack**
```
- Azure App Service
- Azure Database for PostgreSQL
- Azure Cache for Redis
- Azure Blob Storage
- Azure Application Gateway
- Azure DevOps
```

### 4.5 Security Stack

| Component | Technology | Why This Choice |
|-----------|-----------|-----------------|
| **Authentication** | Auth0 / Okta | MFA, SSO, compliance certifications |
| **Authorization** | RBAC (custom) | Granular permissions, role-based |
| **API Security** | JWT tokens | Stateless, scalable, standard |
| **Encryption (Transit)** | TLS 1.3 | Industry standard, HIPAA required |
| **Encryption (Rest)** | AES-256 | NIST approved, HIPAA required |
| **Secrets Management** | AWS Secrets Manager | Automatic rotation, audit logging |
| **WAF** | AWS WAF | SQL injection, XSS protection |
| **DDoS Protection** | AWS Shield | Layer 3/4 protection |
| **Compliance** | Vanta | Automated HIPAA compliance monitoring |
| **Vulnerability Scanning** | Snyk | Dependency scanning, container scanning |

### 4.6 Integration Stack

| Component | Technology | Why This Choice |
|-----------|-----------|-----------------|
| **HL7 Integration** | Mirth Connect | Open-source, widely used, supports HL7 v2/v3/FHIR |
| **API Gateway** | Kong / AWS API Gateway | Rate limiting, authentication, routing |
| **Message Queue** | RabbitMQ / AWS SQS | Reliable messaging, retry logic |
| **Event Streaming** | Apache Kafka (optional) | High throughput, event sourcing |
| **ETL** | Apache Airflow | Workflow orchestration, scheduling |
| **API Documentation** | Swagger/OpenAPI | Interactive docs, client generation |

### 4.7 AI/ML Stack

| Component | Technology | Why This Choice |
|-----------|-----------|-----------------|
| **LLM Provider** | OpenAI GPT-4 | Best-in-class, medical knowledge, API |
| **Alternative LLM** | AWS Bedrock (Claude) | HIPAA-eligible, no data retention |
| **OCR** | AWS Textract | Medical form recognition, table extraction |
| **NLP** | spaCy + scispaCy | Medical entity recognition, free |
| **ML Framework** | scikit-learn | Denial prediction, classification |
| **Vector DB** | pgvector (PostgreSQL) | Semantic search, no additional service |

---

## 5. Third-Party APIs & Integrations

### 5.1 Clearinghouse APIs

#### **Waystar (Recommended)**

**Purpose:** Submit claims to insurance companies, check eligibility, track claim status

**Modules Using It:**
- Insurance Verification (EDI 270/271)
- Claim Submission (EDI 837)
- Claim Tracking (EDI 276/277)
- Payment Posting (EDI 835)

**API Type:** REST API + EDI file exchange  
**Cost Model:** Per-transaction pricing
- Eligibility check: $0.25-$0.50 per check
- Claim submission: $0.50-$2.00 per claim
- ERA processing: $0.25-$0.50 per ERA

**Enterprise vs Paid:**
- **Paid API:** Available to all customers, pay-per-transaction
- **Enterprise:** Volume discounts, dedicated support, SLA guarantees

**Integration Complexity:** Medium  
**Documentation:** https://www.waystar.com/developers

**Sample Code:**
```python
import requests

def check_eligibility(patient, insurance):
    response = requests.post(
        'https://api.waystar.com/v1/eligibility',
        headers={'Authorization': f'Bearer {WAYSTAR_API_KEY}'},
        json={
            'payer_id': insurance.payer_code,
            'provider_npi': '1234567890',
            'member': {
                'first_name': patient.first_name,
                'last_name': patient.last_name,
                'dob': patient.dob,
                'member_id': insurance.policy_number
            },
            'service_date': '2026-05-18'
        }
    )
    return response.json()
```

---

#### **Availity**

**Purpose:** Alternative clearinghouse, multi-payer connectivity

**Modules Using It:** Same as Waystar  
**Cost Model:** Similar to Waystar, sometimes lower fees  
**Enterprise vs Paid:** Paid API, enterprise contracts available  
**Integration Complexity:** Medium

**Why Use:** Some payers prefer Availity, good for multi-clearinghouse strategy

---

#### **Change Healthcare**

**Purpose:** Large clearinghouse, extensive payer network

**Modules Using It:** Same as Waystar  
**Cost Model:** Enterprise pricing, typically higher than Waystar/Availity  
**Enterprise vs Paid:** Primarily enterprise contracts  
**Integration Complexity:** High (more complex API)

**Why Use:** Required by some large hospital systems, comprehensive analytics

---

#### **Eligible API**

**Purpose:** Developer-friendly eligibility checking

**Modules Using It:** Insurance Verification only  
**Cost Model:** $0.25-$0.75 per eligibility check  
**Enterprise vs Paid:** Paid API, no enterprise requirement  
**Integration Complexity:** Low (simple REST API)

**Why Use:** Easier integration for startups, good for MVP

**Sample Code:**
```python
import requests

response = requests.post(
    'https://gw.eligibleapi.com/v1.5/coverage/all.json',
    auth=(ELIGIBLE_API_KEY, ''),
    json={
        'payer_id': '00001',
        'provider_npi': '1234567890',
        'member': {
            'first_name': 'John',
            'last_name': 'Doe',
            'dob': '1980-01-15',
            'member_id': 'POL123456'
        },
        'service_date': '2026-05-18'
    }
)
```

---

### 5.2 EMR/EHR Integration

#### **Epic Systems**

**Purpose:** Largest EMR vendor in US, clinical data exchange

**Modules Using It:**
- Patient Registration (ADT messages)
- Encounter Creation (ADT messages)
- Clinical Documentation (ORU messages)
- Order Management (ORM messages)

**API Type:** HL7 v2.x + FHIR R4  
**Cost Model:** Enterprise licensing (hospital already pays Epic)  
**Enterprise vs Paid:** Enterprise only (Epic is $500K-$50M+ implementation)  
**Integration Complexity:** High

**HL7 Message Types:**
- **ADT^A01:** Patient admission
- **ADT^A04:** Patient registration
- **ADT^A08:** Patient update
- **ORM^O01:** Order message
- **ORU^R01:** Results message

**Integration Method:**
- **HL7 v2.x:** Via Mirth Connect (free integration engine)
- **FHIR API:** Epic's App Orchard (OAuth 2.0)

**Sample HL7 Message:**
```
MSH|^~\&|EPIC|HOSPITAL|||20260518120000||ADT^A04|MSG123|P|2.5
EVN|A04|20260518120000
PID|1||MRN123456||DOE^JOHN^A||19800115|M|||123 MAIN ST^^BOSTON^MA^02101
PV1|1|O|||||1234567890^SMITH^JANE^^^MD
```

---

#### **Cerner (Oracle Health)**

**Purpose:** Second-largest EMR vendor

**Modules Using It:** Same as Epic  
**API Type:** HL7 v2.x + FHIR R4  
**Cost Model:** Enterprise licensing  
**Enterprise vs Paid:** Enterprise only  
**Integration Complexity:** High

**Similar to Epic integration**

---

#### **Athenahealth**

**Purpose:** Cloud-based EMR/RCM for small-medium practices

**Modules Using It:** Full RCM integration (they have built-in RCM)  
**API Type:** REST API (athenaNet API)  
**Cost Model:** Per-provider subscription  
**Enterprise vs Paid:** Paid subscription  
**Integration Complexity:** Medium

**Why Use:** If practice already uses Athenahealth, leverage their RCM features

---

### 5.3 HL7/FHIR Integration

#### **Mirth Connect (Recommended)**

**Purpose:** Open-source HL7 integration engine

**Modules Using It:** All EMR integrations  
**Cost Model:** **FREE** (open-source)  
**Enterprise vs Paid:** Free, optional paid support from NextGen  
**Integration Complexity:** Medium (learning curve)

**Why Use:**
- Industry standard (90% of hospitals use it)
- Supports HL7 v2.x, v3, FHIR, EDI, XML, JSON
- Visual workflow designer
- Large community support

**Installation:**
```bash
# Download from https://www.nextgen.com/products-and-services/mirth-connect
# Run installer
# Access web interface at http://localhost:8080
```

---

#### **Redox**

**Purpose:** Healthcare API integration platform (Mirth alternative)

**Modules Using It:** All EMR integrations  
**Cost Model:** $10,000-$50,000/year subscription  
**Enterprise vs Paid:** Paid subscription  
**Integration Complexity:** Low (managed service)

**Why Use:** Easier than Mirth, managed service, faster implementation

**Trade-off:** Mirth is free but requires expertise; Redox is paid but easier

---

### 5.4 Payment Processing

#### **Stripe (Recommended)**

**Purpose:** Patient payment processing (credit cards, ACH)

**Modules Using It:** Patient Billing, Collections  
**Cost Model:** 2.9% + $0.30 per transaction  
**Enterprise vs Paid:** Paid per-transaction, enterprise pricing available  
**Integration Complexity:** Low

**Why Use:**
- Developer-friendly API
- PCI-compliant (no need to handle card data)
- Supports payment plans, subscriptions
- Excellent documentation

**Sample Code:**
```python
import stripe

stripe.api_key = STRIPE_SECRET_KEY

# Create payment intent
payment_intent = stripe.PaymentIntent.create(
    amount=5000,  # $50.00 in cents
    currency='usd',
    payment_method_types=['card'],
    metadata={
        'patient_id': 'PAT123',
        'account_number': 'ACC456'
    }
)
```

---

#### **Cedar**

**Purpose:** Patient billing and payment platform

**Modules Using It:** Patient Billing, Collections, Payment Plans  
**Cost Model:** % of collected revenue (typically 3-5%)  
**Enterprise vs Paid:** Enterprise contracts  
**Integration Complexity:** Medium

**Why Use:** Full patient engagement platform, not just payments

---

### 5.5 Communication APIs

#### **Twilio**

**Purpose:** SMS appointment reminders, payment reminders

**Modules Using It:** Appointment Scheduling, Patient Billing  
**Cost Model:** $0.0079 per SMS (US)  
**Enterprise vs Paid:** Paid per-message, volume discounts  
**Integration Complexity:** Low

**Sample Code:**
```python
from twilio.rest import Client

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

message = client.messages.create(
    body='Reminder: You have an appointment tomorrow at 10:00 AM with Dr. Smith.',
    from_='+15551234567',
    to=patient.phone
)
```

---

#### **SendGrid**

**Purpose:** Email notifications (statements, reminders, receipts)

**Modules Using It:** All modules needing email  
**Cost Model:** Free tier (100 emails/day), then $0.0006 per email  
**Enterprise vs Paid:** Paid per-email  
**Integration Complexity:** Low

---

### 5.6 AI Services

#### **OpenAI API (GPT-4)**

**Purpose:** Medical coding assistance, clinical note summarization, denial prediction

**Modules Using It:**
- Medical Coding (suggest ICD-10/CPT codes)
- Clinical Documentation (summarize notes)
- Denial Management (predict denial reasons)
- Patient Communication (chatbot)

**Cost Model:**
- GPT-4: $0.03 per 1K input tokens, $0.06 per 1K output tokens
- GPT-3.5-turbo: $0.0015 per 1K input tokens, $0.002 per 1K output tokens

**Enterprise vs Paid:** Paid per-token, enterprise agreements available  
**Integration Complexity:** Low

**HIPAA Compliance:** **NOT HIPAA-compliant by default**
- Must sign Business Associate Agreement (BAA)
- Use Azure OpenAI Service (HIPAA-eligible) instead

**Sample Code:**
```python
import openai

openai.api_key = OPENAI_API_KEY

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a medical coding assistant."},
        {"role": "user", "content": f"Suggest ICD-10 codes for: {clinical_note}"}
    ]
)

suggested_codes = response.choices[0].message.content
```

---

#### **AWS Bedrock (Claude, Llama)**

**Purpose:** HIPAA-compliant alternative to OpenAI

**Modules Using It:** Same as OpenAI  
**Cost Model:** Pay-per-token (similar to OpenAI)  
**Enterprise vs Paid:** Paid per-token  
**Integration Complexity:** Low

**Why Use:**
- **HIPAA-eligible** (AWS signs BAA)
- No data retention (data not used for training)
- Multiple models (Claude, Llama, Titan)

**Recommended for Healthcare:** Use AWS Bedrock instead of OpenAI for PHI

---

#### **AWS Textract**

**Purpose:** OCR for insurance cards, medical forms, prescriptions

**Modules Using It:** Patient Registration (insurance card scanning)  
**Cost Model:** $0.0015 per page  
**Enterprise vs Paid:** Paid per-page  
**Integration Complexity:** Low

**Sample Code:**
```python
import boto3

textract = boto3.client('textract')

response = textract.detect_document_text(
    Document={'S3Object': {'Bucket': 'insurance-cards', 'Name': 'card123.jpg'}}
)

for item in response['Blocks']:
    if item['BlockType'] == 'LINE':
        print(item['Text'])  # Extract text from insurance card
```

---

### 5.7 Integration Summary Table

| API/Service | Purpose | Cost | HIPAA | Complexity | Recommendation |
|-------------|---------|------|-------|------------|----------------|
| **Waystar** | Clearinghouse | $0.50-$2/claim | Yes | Medium | **Must Have** |
| **Availity** | Clearinghouse | $0.50-$2/claim | Yes | Medium | Alternative |
| **Eligible API** | Eligibility only | $0.25-$0.75/check | Yes | Low | Good for MVP |
| **Epic/Cerner** | EMR integration | Enterprise | Yes | High | If hospital uses |
| **Mirth Connect** | HL7 engine | **Free** | Yes | Medium | **Must Have** |
| **Redox** | HL7 platform | $10K-$50K/year | Yes | Low | Alternative to Mirth |
| **Stripe** | Payments | 2.9% + $0.30 | PCI-DSS | Low | **Must Have** |
| **Cedar** | Patient billing | 3-5% of revenue | Yes | Medium | Optional |
| **Twilio** | SMS | $0.0079/SMS | No | Low | **Must Have** |
| **SendGrid** | Email | $0.0006/email | No | Low | **Must Have** |
| **OpenAI** | AI/ML | $0.03/1K tokens | **No*** | Low | Use Azure OpenAI |
| **AWS Bedrock** | AI/ML | $0.03/1K tokens | **Yes** | Low | **Recommended for AI** |
| **AWS Textract** | OCR | $0.0015/page | Yes | Low | Recommended |
| **Auth0** | Authentication | $200-$2K/month | Yes | Low | **Must Have** |

**Must Have (MVP):** Waystar, Mirth Connect, Stripe, Twilio, SendGrid, Auth0  
**Total MVP Cost:** ~$2,000-$5,000/month + per-transaction fees

---

*[Continue to Part 3 for AI Features, Development Plan, and Execution Strategy]*
