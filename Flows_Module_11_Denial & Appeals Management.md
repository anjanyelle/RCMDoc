# Module 16: Denial & Appeals Management - Flow Documentation

**Version:** 1.0  
**Module ID:** MOD-016  
**Category:** Category 4: Payment & Revenue Management

---

## 1. Module Overview

**Purpose:** Manage insurance claim denials, track appeal processes, and maximize revenue recovery through systematic denial management.

**Why Hospitals Use It:** Reduce revenue loss from denials, improve claim acceptance rates, ensure timely appeals, maintain compliance with payer requirements.

**Main Users:** Billing Team, Claims Analysts, Denial Management Specialists, Revenue Cycle Managers

---

## 2. Actors Involved

```
┌─────────────────────────────────────────────────┐
│ ACTORS IN DENIAL & APPEALS MODULE              │
├─────────────────────────────────────────────────┤
│                                                 │
│ 1. Denial Management Team                       │
│    - Reviews denied claims                      │
│    - Identifies denial reasons                  │
│    - Corrects claim issues                      │
│    - Resubmits claims                           │
│                                                 │
│ 2. AR (Accounts Receivable) Team               │
│    - Follows unpaid denied claims               │
│    - Escalates aging denials                    │
│    - Tracks payer follow-ups                    │
│                                                 │
│ 3. Billing Team                                 │
│    - Updates claim corrections                  │
│    - Fixes demographic/billing issues           │
│                                                 │
│ 4. Medical Coder                                │
│    - Fixes ICD/CPT/HCPCS errors                 │
│    - Corrects modifiers                         │
│                                                 │
│ 5. Doctor / Provider                            │
│    - Provides missing medical records           │
│    - Adds medical necessity documentation       │
│                                                 │
│ 6. Compliance / QA Team                         │
│    - Reviews high-risk denials                  │
│    - Validates appeal compliance                │
│                                                 │
│ 7. Insurance / Payer                            │
│    - Sends denial reason                        │
│    - Reviews appeals                            │
│    - Approves / rejects payment                 │
│                                                 │
│ 8. Patient (Optional)                           │
│    - Provides updated insurance                 │
│    - Pays balance if denial final               │
│                                                 │
│ 9. AI System                                    │
│    - Predicts denial root cause                 │
│    - Suggests fixes                             │
│    - Auto-generates appeal letter               │
│                                                 │
│ 10. System                                      │
│    - Denial Rules Engine                        │
│    - Appeal Tracking Engine                     │
│    - Workflow Management                        │
│    - SLA Tracker                                │
│    - Audit Logs                                 │
│                                                 │
│ 11. External APIs                               │
│    - Waystar API                                │
│    - Availity API                               │
│    - Change Healthcare API                      │
│    - CMS Rules API                              │
│    - ERA / EOB Integration                      │
│    - Payer Portal APIs                          │
│                                                 │
└─────────────────────────────────────────────────┘

```

---

## 3. Step-by-Step Workflow

```
┌─────────┐
│ START   │
└────┬────┘
     │
     ▼
┌─────────────────────┐
│ Claim Submitted     │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Claim Denied by     │
│ Insurance Payer     │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Receive Denial      │
│ ERA / EOB / 277CA   │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Auto Categorize     │
│ Denial Type         │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Identify Denial     │
│ Reason              │
│ - Coding Error      │
│ - Authorization     │
│ - Eligibility       │
│ - Duplicate Claim   │
│ - Missing Docs      │
│ - Medical Necessity │
│ - Modifier Error    │
│ - NCCI/Bundling     │
│ - Timely Filing     │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ AI Root Cause       │
│ Prediction          │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Assign Priority     │
│ High $ / Aging      │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Route to Correct    │
│ Team                │
│ - Billing           │
│ - Coding            │
│ - AR                │
│ - Provider          │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Denial Analyst      │
│ Reviews Claim       │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Root Cause Analysis │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Fixable?╲───No─────────────┐
  ╲       ╱                   │
   ╲     ╱                    │
    ╲   ╱                     │
     │Yes                     ▼
     │               ┌─────────────────┐
     │               │ Start Appeal    │
     │               │ Process         │
     │               └────┬────────────┘
     │                    │
     ▼                    │
┌─────────────────────┐   │
│ Fix Claim Errors    │   │
│ - ICD/CPT           │   │
│ - Demographics      │   │
│ - Modifier           │   │
│ - Authorization     │   │
└────┬────────────────┘   │
     │                    │
     ▼                    │
┌─────────────────────┐   │
│ Request Missing     │   │
│ Documentation       │   │
└────┬────────────────┘   │
     │                    │
     ▼                    │
┌─────────────────────┐   │
│ Internal QA Review  │   │
└────┬────────────────┘   │
     │                    │
     ▼                    │
┌─────────────────────┐   │
│ Revalidate Claim    │   │
└────┬────────────────┘   │
     │                    │
     ▼                    │
┌─────────────────────┐   │
│ Resubmit Claim      │   │
└────┬────────────────┘   │
     │                    │
     └─────────┬──────────┘
               ↓
┌─────────────────────┐
│ Generate Appeal     │
│ Letter (AI)         │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Attach Documents    │
│ - Notes             │
│ - Labs              │
│ - Authorization     │
│ - Referral          │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Submit Appeal       │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Track Appeal SLA    │
│ 15 / 30 / 45 Days   │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Wait Payer Response │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Approved?╲──No─────────────┐
  ╲        ╱                  │
   ╲      ╱                   │
    ╲    ╱                    │
     │Yes                     ▼
     │                ┌────────────────┐
     │                │ Final Denial   │
     │                │ Patient Bill / │
     │                │ Write-Off      │
     │                └────────────────┘
     ▼
┌─────────────────────┐
│ Payment Posted      │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Save Audit Logs     │
└────┬────────────────┘
     │
     ▼
┌─────────┐
│ END     │
└─────────┘


---

## 4. AI / Rules Engine Flow

```
┌─────────────────────┐
│ Denied Claim        │
│ Input               │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Preprocess Claim:   │
│ - Extract denial    │
│   reason            │
│ - Read ERA / EOB    │
│ - Parse payer notes │
│ - Extract claim data│
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Build AI Prompt:    │
│                     │
│ "You are an RCM     │
│ denial expert.      │
│ Analyze denial and  │
│ identify root cause │
│ and correction      │
│ steps. Return JSON" │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Call OpenAI API     │
│ (GPT-4)             │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Parse AI Response:  │
│ {                   │
│ "denial_type":      │
│ "Authorization",    │
│ "root_cause":       │
│ "Missing Prior Auth"│
│ "fix_steps":[...]   │
│ "appeal_needed":true│
│ "confidence":0.92   │
│ }                   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Validate Denial:    │
│ - Valid denial code?│
│ - Appeal allowed?   │
│ - Timely filing ok? │
│ - Payer rules check │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Enrich with Details:│
│ - Denial category   │
│ - Appeal deadline   │
│ - Required docs     │
│ - Responsible team  │
│ - Recovery priority │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Generate Appeal     │
│ Letter (AI)         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Return to Frontend  │
│ Denial Resolution UI│
└─────────────────────┘
```

---

## 5. Use Case Diagram

```
┌──────────────┐                          ┌──────────────────┐
│ Denial       │─────────────────────────>│ Review Denied    │
│ Analyst      │                          │ Claim            │
└──────┬───────┘                          └──────────────────┘
       │
       │                                  ┌──────────────────┐
       ├─────────────────────────────────>│ Request AI       │
       │                                  │ Root Cause       │
       │                                  └──────────────────┘
       │
       │                                  ┌──────────────────┐
       ├─────────────────────────────────>│ Fix Claim Errors │
       │                                  │ / Add Documents  │
       │                                  └──────────────────┘
       │
       │                                  ┌──────────────────┐
       ├─────────────────────────────────>│ Generate Appeal  │
       │                                  │ Letter           │
       │                                  └──────────────────┘
       │
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Submit Appeal /  │
                                          │ Resubmit Claim   │
                                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ AI System    │─────────────────────────>│ Analyze Denial   │
│ (OpenAI)     │                          │ Reason           │
└──────┬───────┘                          └──────────────────┘
       │
       │                                  ┌──────────────────┐
       ├─────────────────────────────────>│ Predict Root     │
       │                                  │ Cause            │
       │                                  └──────────────────┘
       │
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Suggest Fix /    │
                                          │ Appeal Strategy  │
                                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ System       │─────────────────────────>│ Validate Denial  │
│              │                          │ Rules            │
└──────┬───────┘                          └──────────────────┘
       │
       │                                  ┌──────────────────┐
       ├─────────────────────────────────>│ Check Timely     │
       │                                  │ Filing Deadline  │
       │                                  └──────────────────┘
       │
       │                                  ┌──────────────────┐
       ├─────────────────────────────────>│ Validate Appeal  │
       │                                  │ Eligibility      │
       │                                  └──────────────────┘
       │
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Track Appeal SLA │
                                          │ & Recovery       │
                                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ Billing Team │─────────────────────────>│ Correct Billing  │
│              │                          │ Errors           │
└──────────────┘                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ Medical      │─────────────────────────>│ Correct ICD/CPT  │
│ Coder        │                          │ Modifier Errors  │
└──────────────┘                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ Doctor /     │─────────────────────────>│ Upload Missing   │
│ Provider     │                          │ Documentation    │
└──────────────┘                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ AR Team      │─────────────────────────>│ Follow-up Payer  │
│              │                          │ Response         │
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
│ Load Denied Claim   │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Read Denial Details │
│ ERA / EOB / 277CA   │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Click "AI Analyze"  │
│ Denial              │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Call OpenAI API     │
│ / Rules Engine      │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Wait for Response   │
│ (3-5 seconds)       │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Success?╲───No────────┐
  ╲       ╱              │
   ╲     ╱               │
    ╲   ╱                │
     │Yes                ▼

     │          ┌─────────────────┐
     │          │ Show Error:     │
     │          │ "AI unavailable"│
     │          │ Manual Review   │
     │          └─────────────────┘
     │
     ▼
┌─────────────────────┐
│ Display AI Result   │
│ - Denial Type       │
│ - Root Cause        │
│ - Fix Steps         │
│ - Appeal Needed?    │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Review Denial       │
│ Recommendation      │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Accept?╲───No────────┐
  ╲      ╱              │
   ╲    ╱               │
    ╲  ╱                │
     │Yes               ▼
     │          ┌─────────────────┐
     │          │ Manually Select │
     │          │ Correct Reason  │
     │          └────┬────────────┘
     │               │
     └──────┬────────┘
            ↓
┌─────────────────────┐
│ Add to Denial Work  │
│ Plan                │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ More Issues?        │
│ Coding/Auth/Docs    │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Done? ╲───No────────┐
  ╲      ╱             │
   ╲    ╱              │
    ╲  ╱               │
     │Yes              │
     │                 └────────┐
     ▼       

                   │
┌─────────────────────┐         │
│ Validate Work Plan  │         │
│ - Appeal allowed?   │         │
│ - Timely filing ok? │         │
│ - Required docs?    │         │
└────┬────────────────┘         │
     │                          │
     ▼                          │
    ╱ ╲                         │
   ╱   ╲                        │
  ╱Valid?╲───No──────┐          │
  ╲      ╱           │          │
   ╲    ╱            │          │
    ╲  ╱             │          │
     │Yes            ▼          │
     │        ┌─────────────────┐
     │        │ Fix Errors /    │
     │        │ Add Missing Docs│
     │        └────┬────────────┘
     │             │
     └─────────────┘
     │
     ▼
┌─────────────────────┐
│ Generate Appeal     │
│ Letter if Needed    │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Attach Documents    │
│ Notes/Auth/Labs     │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Submit Appeal or    │
│ Resubmit Claim      │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Save to Database    │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Track SLA / Payer   │
│ Response            │
└────┬────────────────┘
     │
     ▼
┌─────────┐
│   END   │
└─────────┘

---

## 7. Sequence Diagram

```
Denial Team  Frontend    Backend    OpenAI    Database
    │            │           │          │          │
    │ Open       │           │          │          │
    │ Denied     │           │          │          │
    │ Claim      │           │          │          │
    ├───────────>│           │          │          │
    │            │ GET /claim           │          │
    │            ├──────────>│          │          │
    │            │           │ Load     │          │
    │            │           │ Denial   │          │
    │            │           ├───────────────────>│
    │            │           │ Claim Data        │
    │            │           │<──────────────────┤
    │            │           │                   │
    │ Click AI   │           │                   │
    │ Analyze    │           │                   │
    ├───────────>│           │                   │
    │            │ POST /ai-denial              │
    │            ├──────────>│                  │
    │            │           │ Extract Denial   │
    │            │           │ Reason           │
    │            │           │ Parse ERA/EOB    │
    │            │           │                  │
    │            │           │ Build Prompt     │
    │            │           │ Root Cause       │
    │            │           │ Appeal Strategy  │
    │            │           │                  │
    │            │           │ POST             │
    │            │           ├─────────>│       │
    │            │           │          │ AI    │
    │            │           │          │Process│
    │            │           │ Response │       │
    │            │           │<─────────┤       │
    │            │           │                  │
    │            │           │ Validate Denial  │
    │            │           │ Timely Filing    │
    │            │           │ Appeal Allowed?  │
    │            │           ├──────────────────>│
    │            │           │ Payer Rules      │
    │            │           │<──────────────────┤
    │            │ AI Result │                  │
    │            │ Root Cause│                  │
    │            │<──────────┤                  │
    │ Review     │           │                  │
    │ Result     │           │                  │
    │<───────────┤           │                  │
    │            │           │                  │
    │ Fix Errors │           │                  │
    │ / Upload   │           │                  │
    │ Docs       │           │                  │
    ├───────────>│           │                  │
    │            │ POST /fix-denial            │
    │            ├──────────>│                 │
    │            │           │ Save Updates    │
    │            │           ├──────────────────>│
    │            │           │                  │
    │ Submit     │           │                  │
    │ Appeal     │           │                  │
    ├───────────>│           │                  │
    │            │ POST /submit-appeal         │
    │            ├──────────>│                 │
    │            │           │ Generate Appeal │
    │            │           │ Letter          │
    │            │           │ Save Appeal     │
    │            │           ├──────────────────>│
    │            │           │                  │
    │            │ Success   │                  │
    │            │<──────────┤                  │
    │ Done       │           │                  │
    │<───────────┤           │                  │
    │            │           │                  │


```

---

## 8. API Flow

**Request:**

```http
POST /api/denials/ai-analyze
{
  "claimId": "CLM-00001",
  "denialId": "DEN-00001",
  "payerId": "PAY-001",
  "denialCode": "CO-197",
  "denialReason": "Authorization missing",
  "eraEobText": "Claim denied because prior authorization was not obtained.",
  "claimAmount": 2500.00,
  "submittedDate": "2026-05-01",
  "denialDate": "2026-05-10"
}
```

**Response:**

```json
{
  "denialType": "Authorization",
  "rootCause": "Missing prior authorization",
  "confidence": 0.92,
  "appealNeeded": true,
  "fixSteps": [
    "Check if retro authorization is allowed",
    "Collect authorization proof or provider notes",
    "Attach medical necessity documentation",
    "Submit appeal before deadline"
  ],
  "requiredDocuments": [
    "Provider notes",
    "Medical necessity letter",
    "Authorization request proof"
  ],
  "appealDeadline": "2026-06-09",
  "priority": "High",
  "estimatedRecoveryAmount": 2500.00,
  "aiModel": "gpt-4",
  "processingTime": "3.4s"
}
```

---

## 9. Database Flow

```sql
-- Log denial
Save denial record
INSERT INTO claim_denials (
    denial_id,
    claim_id,
    payer_id,
    denial_code,
    denial_reason,
    denial_type,
    claim_amount,
    denial_date,
    status
) VALUES (
    'DEN-00001',
    'CLM-00001',
    'PAY-001',
    'CO-197',
    'Authorization missing',
    'Authorization',
    2500.00,
    '2026-05-10',
    'UNDER_REVIEW'
);

-- Save AI denial analysis
INSERT INTO ai_denial_analysis_logs (
    denial_id,
    claim_id,
    predicted_root_cause,
    confidence_score,
    appeal_needed,
    priority,
    estimated_recovery_amount,
    processing_time
) VALUES (
    'DEN-00001',
    'CLM-00001',
    'Missing prior authorization',
    0.92,
    true,
    'High',
    2500.00,
    3.4
);

-- Save appeal record
INSERT INTO appeals (
    appeal_id,
    denial_id,
    claim_id,
    appeal_status,
    appeal_deadline,
    required_documents,
    submitted_by
) VALUES (
    'APL-00001',
    'DEN-00001',
    'CLM-00001',
    'DRAFT',
    '2026-06-09',
    'Provider notes, Medical necessity letter, Authorization request proof',
    'USR-001'
);

-- Save denial workqueue task
INSERT INTO denial_workqueue (
    task_id,
    denial_id,
    assigned_team,
    priority,
    status,
    due_date
) VALUES (
    'TASK-00001',
    'DEN-00001',
    'Denial Management Team',
    'High',
    'OPEN',
    '2026-05-20'
);

-- Save audit log
INSERT INTO denial_audit_logs (
    denial_id,
    action,
    performed_by,
    notes
) VALUES (
    'DEN-00001',
    'AI_ANALYSIS_COMPLETED',
    'SYSTEM',
    'AI analyzed denial and recommended appeal'
);
```

---

## 10. Error Scenarios

```
Error 1: AI API Down
   ↓
Show error
   ↓
Fall back to manual denial review

Error 2: Low Confidence (<70%)
   ↓
Flag for senior review
   ↓
Denial analyst validates root cause manually

Error 3: Invalid Denial Code
   ↓
Validation catches it
   ↓
Show error to denial analyst
   ↓
Analyst selects correct denial reason

Error 4: Missing Appeal Documents
   ↓
System shows missing documents
   ↓
Request documents from provider / billing team
   ↓
Attach documents before appeal submission

Error 5: Appeal Deadline Missed
   ↓
System blocks appeal submission
   ↓
Move to write-off / patient responsibility review

Error 6: Payer No Response
   ↓
SLA tracker alerts AR team
   ↓
AR team follows up with payer

Error 7: Repeated Denial
   ↓
Escalate to senior analyst / compliance team
   ↓
Review payer rules and root cause
```

---

## 11. Dashboard & Status Flow

```
┌─────────┐
│ START   │
└────┬────┘
     │
     ▼
┌─────────────────────┐
│ Claim Submitted     │
│ Status: Submitted   │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Claim Accepted?     │
│ by Payer            │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Denied?╲───No──────────────┐
  ╲       ╱                   │
   ╲     ╱                    │
    ╲   ╱                     │
     │Yes                     ▼
     │                ┌─────────────────┐
     │                │ Claim Approved  │
     │                │ Status: Paid    │
     │                └────────┬────────┘
     │                         │
     │                         ▼
     │                 ┌──────────────┐
     │                 │    CLOSED    │
     │                 └──────────────┘
     │
     ▼
┌─────────────────────┐
│ Denied Claim        │
│ Status: Denied      │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Denial Review       │
│ Status: Under       │
│ Review              │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Denial Categorized  │
│ - Coding Error      │
│ - Authorization     │
│ - Missing Docs      │
│ - Eligibility       │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Correction in       │
│ Progress            │
│ Status: Fixing      │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Fixable?╲───No────────────┐
  ╲       ╱                  │
   ╲     ╱                   │
    ╲   ╱                    │
     │Yes                    ▼
     │                ┌─────────────────┐
     │                │ Appeal Required │
     │                │ Status: Appeal  │
     │                │ Needed          │
     │                └────────┬────────┘
     │                         │
     ▼                         │
┌─────────────────────┐        │
│ Claim Corrected     │        │
│ Status: Corrected   │        │
└────┬────────────────┘        │
     │                         │
     ▼                         │
┌─────────────────────┐        │
│ QA Validation       │        │
│ Status: QA Review   │        │
└────┬────────────────┘        │
     │                         │
     ▼                         │
┌─────────────────────┐        │
│ Resubmitted to      │        │
│ Payer               │        │
│ Status: Resubmitted │        │
└────┬────────────────┘        │
     │                         │
     └──────────┬──────────────┘
                ↓
┌─────────────────────┐
│ Appeal Generated    │
│ Status: Appeal      │
│ Created             │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Appeal Submitted    │
│ Status: Appeal Sent │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Awaiting Payer      │
│ Response            │
│ Status: Pending     │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Approved?╲───No──────────────┐
  ╲        ╱                    │
   ╲      ╱                     │
    ╲    ╱                      │
     │Yes                       ▼
     │                  ┌─────────────────┐
     │                  │ Final Denial    │
     │                  │ Status: Closed  │
     │                  │ (Write-off /    │
     │                  │ Patient Bill)   │
     │                  └────────┬────────┘
     │                           │
     ▼                           ▼
┌─────────────────────┐   ┌──────────────┐
│ Payment Posted      │   │    CLOSED    │
│ Status: Paid        │   └──────────────┘
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Recovery Success    │
│ Status: Recovered   │
└────┬────────────────┘
     │
     ▼
┌──────────────┐
│    CLOSED    │
└──────────────┘
```

---

**Next Module:** [Module 17: Secondary Insurance Billing](Flows_Module_20_Secondary_Billing.md)