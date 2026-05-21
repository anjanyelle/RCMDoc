# Module: Compliance & Audit

**Version:** 1.0
**Module ID:** MOD-019
**Category:** Security, Compliance & Governance

---

## 1. Module Overview

**Purpose:** Track, monitor, and validate all user/system actions to ensure HIPAA, CMS, payer, billing, coding, and internal compliance rules are followed.

**Why Hospitals Use It:** Hospitals need this module to prevent HIPAA violations, fraud, unauthorized access, billing mistakes, audit failures, and compliance penalties.

**Main Users:** Compliance Team, Internal Auditor, Security Team, Admin Team, Billing Team, Coding Team, Providers, System Admin

---

## 2. Actors Involved

```
┌─────────────────────────────────────────────────┐
│ ACTORS IN COMPLIANCE & AUDIT MODULE            │
├─────────────────────────────────────────────────┤
│                                                 │
│ 1. Compliance Team                              │
│    - Reviews compliance alerts                  │
│    - Investigates violations                    │
│    - Ensures HIPAA/CMS compliance               │
│                                                 │
│ 2. Internal Auditor                             │
│    - Reviews audit logs                         │
│    - Performs internal audits                   │
│    - Generates audit reports                    │
│                                                 │
│ 3. Security Team                                │
│    - Monitors unauthorized access               │
│    - Detects suspicious login/activity          │
│    - Handles security incidents                 │
│                                                 │
│ 4. Admin Team                                   │
│    - Manages users and roles                    │
│    - Controls permissions                       │
│    - Reviews access changes                     │
│                                                 │
│ 5. Billing Team                                 │
│    - Ensures compliant billing actions          │
│    - Reviews claim/billing changes              │
│                                                 │
│ 6. Medical Coding Team                          │
│    - Ensures compliant coding                   │
│    - Reviews modifier/code changes              │
│                                                 │
│ 7. Doctor / Provider                            │
│    - Maintains proper documentation             │
│    - Responds to documentation queries          │
│                                                 │
│ 8. AI System                                    │
│    - Detects fraud patterns                     │
│    - Flags risky actions                        │
│    - Predicts compliance risk                   │
│                                                 │
│ 9. System                                       │
│    - Audit Logging Engine                       │
│    - Compliance Rules Engine                    │
│    - Risk Detection Engine                      │
│    - Alert Notification Service                 │
│                                                 │
│ 10. External APIs                               │
│    - CMS Rules API                              │
│    - NCCI Rules API                             │
│    - HIPAA Policy Rules                         │
│    - Security Monitoring Tools                  │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 3. Step-by-Step Workflow

```
┌─────────────────────┐
│ User Performs       │
│ Action              │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ System Captures     │
│ Activity            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Store Basic Details │
│ - User ID           │
│ - Role              │
│ - Module            │
│ - Action            │
│ - Timestamp         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Compliance Rule     │
│ Validation          │
│ - HIPAA             │
│ - CMS               │
│ - Payer Rules       │
│ - RBAC Rules        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ AI Risk Detection   │
│ - Fraud Pattern     │
│ - Suspicious Access │
│ - Abnormal Billing  │
└──────────┬──────────┘
           ↓
      ╱ ╲
     ╱   ╲
    ╱Risk?╲──No────────────┐
    ╲Found?╱               │
     ╲   ╱                 │
      ╲ ╱                  │
       │Yes                ▼
       │           ┌─────────────────┐
       │           │ Save Audit Log  │
       │           │ Status: Passed  │
       │           └────────┬────────┘
       │                    ↓
       │           ┌─────────────────┐
       │           │ Continue Normal │
       │           │ Workflow        │
       │           └─────────────────┘
       │
       ▼
┌─────────────────────┐
│ Generate Compliance │
│ Alert               │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Assign Review Task  │
│ to Compliance Team  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Investigation       │
│ Started             │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Corrective Action   │
│ if Required         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Final Review        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Close Compliance    │
│ Case                │
└─────────────────────┘
```

---

## 4. Compliance & Audit Engine Flow

```
┌─────────────────────┐
│ User Activity       │
│ Input               │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Capture Activity:   │
│ - Login             │
│ - View PHI          │
│ - Claim Edit        │
│ - Coding Update     │
│ - Payment Change    │
│ - Role Change       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Normalize Event     │
│ Data                │
│ - User              │
│ - IP Address        │
│ - Device            │
│ - Module            │
│ - Before/After Data │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Run Compliance      │
│ Rules Engine        │
│ - HIPAA             │
│ - CMS               │
│ - RBAC              │
│ - Payer Rules       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ AI Risk Analysis    │
│ - Fraud Detection   │
│ - Unusual Activity  │
│ - Duplicate Changes │
│ - Excessive Access  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Calculate Risk      │
│ Score               │
│ Low / Medium / High │
└──────────┬──────────┘
           ↓
      ╱ ╲
     ╱   ╲
    ╱High ╲──No────────────┐
    ╲Risk?╱                │
     ╲   ╱                 │
      ╲ ╱                  │
       │Yes                ▼
       │           ┌─────────────────┐
       │           │ Save Audit Log  │
       │           │ No Alert Needed │
       │           └────────┬────────┘
       │                    ↓
       │           ┌─────────────────┐
       │           │ Return Success  │
       │           │ to Frontend     │
       │           └─────────────────┘
       │
       ▼
┌─────────────────────┐
│ Create Compliance   │
│ Alert               │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Notify Compliance / │
│ Security Team       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Return Alert Status │
│ to Frontend         │
└─────────────────────┘
```

---

## 5. Use Case Diagram

```
┌──────────────┐                          ┌──────────────────┐
│ Compliance   │─────────────────────────>│ Review Alerts    │
│ Team         │                          └──────────────────┘
└──────┬───────┘
       │
       │                                  ┌──────────────────┐
       ├─────────────────────────────────>│ Investigate      │
       │                                  │ Violations       │
       │                                  └──────────────────┘
       │
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Close Compliance │
                                          │ Case             │
                                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ Internal     │─────────────────────────>│ Review Audit     │
│ Auditor      │                          │ Logs             │
└──────┬───────┘                          └──────────────────┘
       │
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Generate Audit   │
                                          │ Report           │
                                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ Security Team│─────────────────────────>│ Monitor Access   │
│              │                          │ Risk             │
└──────┬───────┘                          └──────────────────┘
       │
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Investigate      │
                                          │ Unauthorized Use │
                                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ Admin Team   │─────────────────────────>│ Manage Roles     │
│              │                          │ Permissions      │
└──────┬───────┘                          └──────────────────┘
       │
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Review Access    │
                                          │ Changes          │
                                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ AI System    │─────────────────────────>│ Detect Fraud /   │
│              │                          │ Risk Pattern     │
└──────┬───────┘                          └──────────────────┘
       │
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Generate Risk    │
                                          │ Score            │
                                          └──────────────────┘


┌──────────────┐                          ┌──────────────────┐
│ System       │─────────────────────────>│ Save Audit Logs  │
│              │                          └──────────────────┘
└──────┬───────┘
       │
       │                                  ┌──────────────────┐
       └─────────────────────────────────>│ Trigger Alerts   │
                                          └──────────────────┘
```

---

## 6. Activity Flow Diagram

```
┌─────────┐
│ START   │
└────┬────┘
     │
     ▼
┌─────────────────────┐
│ User Action         │
│ Occurs              │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Capture Audit Event │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Validate User Role  │
│ and Permission      │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Allowed?╲──No─────────┐
  ╲       ╱              │
   ╲     ╱               │
    ╲   ╱                │
     │Yes                ▼
     │          ┌─────────────────┐
     │          │ Block Action    │
     │          │ Alert Security  │
     │          └────┬────────────┘
     │               ↓
     │          ┌─────────────────┐
     │          │ Save Audit Log  │
     │          └────┬────────────┘
     │               ↓
     │          ┌─────────┐
     │          │  END    │
     │          └─────────┘
     │
     ▼
┌─────────────────────┐
│ Run Compliance      │
│ Rule Check          │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ AI Risk / Fraud     │
│ Analysis            │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Risk? ╲──No──────────┐
  ╲Found?╱              │
   ╲   ╱                │
    ╲ ╱                 │
     │Yes               ▼
     │          ┌─────────────────┐
     │          │ Save Normal     │
     │          │ Audit Log       │
     │          └────┬────────────┘
     │               ↓
     │          ┌─────────┐
     │          │  END    │
     │          └─────────┘
     │
     ▼
┌─────────────────────┐
│ Create Compliance   │
│ Alert               │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Assign to           │
│ Compliance Team     │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Investigation       │
│ Started             │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Corrective Action   │
│ Required?           │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Final Review        │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Save Final Audit    │
│ Log                 │
└────┬────────────────┘
     │
     ▼
┌─────────┐
│ END     │
└─────────┘
```

---

## 7. Sequence Diagram

```
User    Frontend    Backend    AI Engine    Database
 │           │           │           │           │
 │ Perform   │           │           │           │
 │ Action    │           │           │           │
 ├──────────>│           │           │           │
 │           │ POST /audit/check    │           │
 │           ├──────────>│           │           │
 │           │           │ Validate  │           │
 │           │           │ Permission│           │
 │           │           │           │           │
 │           │           │ Run Rules │           │
 │           │           │ Check     │           │
 │           │           │           │           │
 │           │           │ Risk      │           │
 │           │           │ Analysis  │           │
 │           │           ├──────────>│           │
 │           │           │           │ AI Checks │
 │           │           │           │ Fraud/Risk│
 │           │           │ Risk Score│           │
 │           │           │<──────────┤           │
 │           │           │           │           │
 │           │           │ Save Log  │           │
 │           │           ├──────────────────────>│
 │           │           │           │           │
 │           │           │ Risk?     │           │
 │           │           │           │           │
 │           │           │ If High   │           │
 │           │           │ Create    │           │
 │           │           │ Alert     │           │
 │           │           ├──────────────────────>│
 │           │           │           │           │
 │ Success / │           │           │           │
 │ Alert     │           │           │           │
 │<──────────┤           │           │           │
 │           │           │           │           │
```

---

## 8. API Flow

**Request:**

```http
POST /api/compliance/audit-check
{
  "userId": "USR-001",
  "userRole": "Billing Team",
  "module": "Claims",
  "action": "UPDATE_CLAIM_AMOUNT",
  "entityId": "CLM-00001",
  "ipAddress": "192.168.1.20",
  "deviceId": "DEV-001",
  "beforeValue": {
    "claimAmount": 1200.00
  },
  "afterValue": {
    "claimAmount": 2500.00
  },
  "timestamp": "2026-05-21T10:30:00Z"
}
```

**Response:**

```json
{
  "auditLogId": "AUD-00001",
  "status": "ALERT",
  "riskLevel": "HIGH",
  "riskScore": 87,
  "complianceChecks": {
    "rbacCheck": "PASS",
    "hipaaCheck": "PASS",
    "cmsBillingCheck": "WARNING",
    "payerRuleCheck": "WARNING"
  },
  "alerts": [
    {
      "alertId": "ALT-00001",
      "reason": "Claim amount increased by more than allowed threshold",
      "assignedTo": "Compliance Team",
      "priority": "High"
    }
  ],
  "nextAction": "Compliance review required",
  "processingTime": "1.8s"
}
```

---

## 9. Database Flow

```sql
-- Save audit log
INSERT INTO audit_logs (
    audit_log_id,
    user_id,
    user_role,
    module,
    action,
    entity_id,
    ip_address,
    device_id,
    before_value,
    after_value,
    risk_level,
    risk_score,
    status,
    created_at
) VALUES (
    'AUD-00001',
    'USR-001',
    'Billing Team',
    'Claims',
    'UPDATE_CLAIM_AMOUNT',
    'CLM-00001',
    '192.168.1.20',
    'DEV-001',
    '{"claimAmount":1200.00}',
    '{"claimAmount":2500.00}',
    'HIGH',
    87,
    'ALERT',
    NOW()
);

-- Save compliance alert
INSERT INTO compliance_alerts (
    alert_id,
    audit_log_id,
    alert_type,
    severity,
    reason,
    assigned_team,
    status,
    created_at
) VALUES (
    'ALT-00001',
    'AUD-00001',
    'BILLING_RISK',
    'HIGH',
    'Claim amount increased by more than allowed threshold',
    'Compliance Team',
    'OPEN',
    NOW()
);

-- Save investigation task
INSERT INTO compliance_investigation_tasks (
    task_id,
    alert_id,
    assigned_to,
    priority,
    status,
    due_date
) VALUES (
    'TASK-00001',
    'ALT-00001',
    'Compliance Team',
    'High',
    'ASSIGNED',
    '2026-05-23'
);

-- Save final compliance review
INSERT INTO compliance_reviews (
    review_id,
    alert_id,
    reviewed_by,
    review_status,
    resolution_notes,
    reviewed_at
) VALUES (
    'REV-00001',
    'ALT-00001',
    'USR-COMP-001',
    'RESOLVED',
    'Claim amount verified with corrected charge documentation',
    NOW()
);
```

---

## 10. Error Scenarios

```
Error 1: Unauthorized Access
   ↓
System blocks action
   ↓
Save audit log
   ↓
Alert security team

Error 2: HIPAA Violation Risk
   ↓
PHI access flagged
   ↓
Compliance team review
   ↓
Investigation started

Error 3: Suspicious Billing Pattern
   ↓
AI detects abnormal billing change
   ↓
Create compliance alert
   ↓
Internal audit review

Error 4: Role Permission Mismatch
   ↓
User action not allowed
   ↓
Block request
   ↓
Notify admin/security team

Error 5: Audit Log Save Failed
   ↓
Block sensitive transaction
   ↓
Retry log save
   ↓
Escalate system alert

Error 6: Repeated Failed Login
   ↓
Lock user account
   ↓
Notify security team
   ↓
Require admin review

Error 7: Excessive PHI Access
   ↓
AI flags abnormal access
   ↓
Security investigation
   ↓
Compliance report generated
```

---

## 11. Dashboard Status Flow

```
┌─────────┐
│ START   │
└────┬────┘
     │
     ▼
┌─────────────────────┐
│ Monitoring Started  │
│ Status: Active      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ User Activity       │
│ Captured            │
│ Login / Edit / View │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Compliance Rule     │
│ Validation          │
│ HIPAA / CMS / Payer │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Risk Analysis       │
│ AI Fraud Detection  │
└──────────┬──────────┘
           ↓
      ╱ ╲
     ╱   ╲
    ╱Risk? ╲──No────────────┐
    ╲Found?╱                │
     ╲   ╱                  │
      ╲ ╱                   │
       │Yes                 ▼
       │            ┌─────────────────┐
       │            │ Compliance Pass │
       │            │ Status: Passed  │
       │            └────────┬────────┘
       │                     ↓
       │            ┌─────────────────┐
       │            │ Save Audit Log  │
       │            └────────┬────────┘
       │                     ↓
       │            ┌─────────────────┐
       │            │ Closed          │
       │            └─────────────────┘
       │
       ▼
┌─────────────────────┐
│ Violation Detected  │
│ Status: Alert       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Assign Compliance   │
│ Investigation       │
│ Status: Assigned    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Under Review        │
│ Status: Reviewing   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Investigation       │
│ In Progress         │
└──────────┬──────────┘
           ↓
      ╱ ╲
     ╱   ╲
    ╱Valid?╲──No─────────────┐
    ╲Issue?╱                 │
     ╲   ╱                   │
      ╲ ╱                    │
       │Yes                  ▼
       │             ┌─────────────────┐
       │             │ False Alert     │
       │             │ Status: Closed  │
       │             └─────────────────┘
       │
       ▼
┌─────────────────────┐
│ Corrective Action   │
│ Required            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Action Completed    │
│ Training / Fix /    │
│ Access Removed      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Final Compliance    │
│ Review              │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Resolved            │
│ Status: Completed   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Save Audit Log      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ CLOSED              │
│ Status: Closed      │
└─────────────────────┘
```

---

**Next Module:** [Module 20: Reporting & Analytics](Flows_Module_20_Reporting_Analytics.md)
