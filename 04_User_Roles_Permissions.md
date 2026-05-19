# Healthcare RCM Application - User Roles & Permissions Matrix

**Version:** 1.0  

**For:** Development Team

---

## 1. Overview

This document defines all user roles, their responsibilities, and granular permissions for each module in the RCM application.

**Total Roles:** 10  
**Permission Model:** Role-Based Access Control (RBAC)

*Note: For production, roles may expand to include Prior Authorization Specialist, Tenant/Branch Admin, External Auditor, Collections Manager, and Financial Counselor based on business need.

---

## 2. User Roles Summary

| Role ID | Role Name | Primary Responsibility | Typical User Count |
|---------|-----------|------------------------|-------------------|
| 1 | System Administrator | System configuration, user management | 1-2 |
| 2 | Front Desk Staff | Patient registration, scheduling, check-in | 5-20 |
| 3 | Clinical Staff | Order entry, clinical documentation | 10-50 |
| 4 | Medical Coder | Code assignment, coding compliance | 3-15 |
| 5 | Billing Specialist | Claim creation, scrubbing, submission | 5-20 |
| 6 | AR Manager | Payment posting, denial management, AR follow-up | 3-10 |
| 7 | Collections Staff | Patient billing, payment plans, collections | 2-10 |
| 8 | Finance Manager | Reporting, analytics, financial oversight | 1-5 |
| 9 | Compliance Officer | Audits, compliance monitoring | 1-3 |
| 10 | Provider (Doctor) | Clinical documentation, encounter review | 5-100 |
| 11 | Prior Authorization Specialist | Manage prior authorizations | 2-10 |
| 12 | Tenant/Branch Admin | Admin for specific tenant/branch | 1-5 |
| 13 | External Auditor | Read-only audit access | 1-5 |
| 14 | Collections Manager | Approve refunds and external collections | 1-2 |
| 15 | Financial Counselor | Screen for charity care | 1-5 |

---

## 3. Detailed Role Permissions

### Role 1: System Administrator

**Responsibilities:**
- Manage all users and roles
- Configure system settings
- Manage integrations
- Monitor system health
- Full access to all modules

**Permissions:**

| Module | Create | Read | Update | Delete | Notes |
|--------|--------|------|--------|--------|-------|
| Users | ✅ | ✅ | ✅ | ✅ | Full user management |
| Roles | ✅ | ✅ | ✅ | ✅ | Manage roles and permissions |
| Providers | ✅ | ✅ | ✅ | ❌ | Can add/edit providers |
| Payers | ✅ | ✅ | ✅ | ❌ | Manage payer list |
| Contracts | ✅ | ✅ | ✅ | ❌ | Manage payer contracts |
| Chargemaster | ✅ | ✅ | ✅ | ❌ | Manage fee schedule |
| Patients | ✅ | ✅ | ✅ | ❌ | Full patient access |
| Encounters | ✅ | ✅ | ✅ | ❌ | Full encounter access |
| Claims | ✅ | ✅ | ✅ | ❌ | Full claim access |
| Payments | ✅ | ✅ | ✅ | ❌ | Full payment access |
| Reports | ✅ | ✅ | ✅ | ✅ | Full reporting access |
| Audit Logs | ❌ | ✅ | ❌ | ❌ | View-only audit logs |
| System Config | ✅ | ✅ | ✅ | ❌ | Configure system settings |

**Special Permissions:**
- Reset user passwords
- Unlock user accounts
- View all audit logs
- Export all data
- Configure integrations (EMR, clearinghouse, payers)
- Deactivate users instead of delete where possible
- MFA required for login
- All admin actions are audited
- Tenant/branch scope applies if the platform is multi-tenant

---

### Role 2: Front Desk Staff

**Responsibilities:**
- Register new patients
- Update patient demographics
- Verify insurance eligibility
- Schedule appointments
- Check in patients
- Collect copays at point of service

**Permissions:**

| Module | Create | Read | Update | Delete | Notes |
|--------|--------|------|--------|--------|-------|
| Patients | ✅ | ✅ | ✅ | ❌ | Register and update patients |
| Patient Insurance | ✅ | ✅ | ✅ | ❌ | Add/update insurance info |
| Eligibility Checks | ✅ | ✅ | ❌ | ❌ | Run eligibility verification |
| Appointments | ✅ | ✅ | ✅ | ❌ | Full appointment management (Cancel instead of Delete) |
| Encounters | ✅ | ✅ | ⚠️ | ❌ | Create encounter at check-in, limited update |
| Authorizations | ⚠️ | ✅ | ⚠️ | ❌ | View auth status, limited create |
| Patient Payments | ✅ | ✅ | ❌ | ❌ | Collect copays/payments |
| Patient Statements | ❌ | ✅ | ❌ | ❌ | View patient balance |
| Reports | ❌ | ⚠️ | ❌ | ❌ | Limited reports (daily check-in report) |

**Restrictions:**
- Cannot view financial reports
- Cannot access coding or billing modules
- Cannot modify charges or claims
- Can only view encounters they created
- Appointments should be cancelled, not deleted. Cancellation reason must be captured and audited.

**Workflow:**
1. Patient arrives → Search patient or create new
2. Verify insurance → Run eligibility check
3. Collect copay → Record payment
4. Check in patient → Create encounter
5. Patient sees doctor

---

### Role 3: Clinical Staff (Nurses, Medical Assistants)

**Responsibilities:**
- Enter clinical orders (labs, imaging, medications)
- Document vital signs
- Assist providers with documentation
- Manage referrals

**Permissions:**

| Module | Create | Read | Update | Delete | Notes |
|--------|--------|------|--------|--------|-------|
| Patients | ❌ | ✅ | ❌ | ❌ | View patient demographics |
| Encounters | ❌ | ✅ | ⚠️ | ❌ | View and add clinical notes |
| Orders | ✅ | ✅ | ✅ | ⚠️ | Create and manage orders |
| Referrals | ✅ | ✅ | ✅ | ❌ | Manage referrals |
| Authorizations | ⚠️ | ✅ | ❌ | ❌ | View auth status |
| Charges | ❌ | ❌ | ❌ | ❌ | No access to charges |
| Claims | ❌ | ❌ | ❌ | ❌ | No access to claims |

**Restrictions:**
- Cannot access financial data
- Cannot create or modify charges
- Cannot view payment information
- Some orders may require provider review/co-sign based on clinic policy.
- Clinical staff cannot finalize provider documentation unless authorized.

---

### Role 4: Medical Coder

**Responsibilities:**
- Assign ICD-10 diagnosis codes
- Assign CPT procedure codes
- Review clinical documentation for completeness
- Ensure coding compliance (NCCI, LCD/NCD)
- Assign DRG codes for inpatient encounters

**Permissions:**

| Module | Create | Read | Update | Delete | Notes |
|--------|--------|------|--------|--------|-------|
| Patients | ❌ | ✅ | ❌ | ❌ | View demographics |
| Encounters | ❌ | ✅ | ⚠️ | ❌ | View encounter, add codes |
| Encounter Diagnoses | ✅ | ✅ | ✅ | ✅ | Full coding access |
| Encounter Procedures | ✅ | ✅ | ✅ | ✅ | Full coding access |
| Charges | ❌ | ✅ | ⚠️ | ❌ | View charges, link codes |
| Code Sets | ❌ | ✅ | ❌ | ❌ | Search ICD/CPT codes |
| NCCI Edits | ❌ | ✅ | ❌ | ❌ | View edit rules |
| LCD/NCD Rules | ❌ | ✅ | ❌ | ❌ | View coverage rules |
| Claims | ❌ | ⚠️ | ❌ | ❌ | View claim status only |
| Reports | ❌ | ⚠️ | ❌ | ❌ | Coding productivity reports |
| Coding Worklist | ❌ | ✅ | ✅ | ❌ | Access assigned worklist |
| Provider Query | ✅ | ✅ | ✅ | ❌ | Send queries to providers |
| Coding Review Status | ❌ | ✅ | ✅ | ❌ | Update coding status |

**Restrictions:**
- Cannot create or submit claims
- Cannot post payments
- Cannot view financial reports
- Can only code encounters assigned to them

**Workflow:**
1. Open coding worklist → Select encounter
2. Review clinical documentation
3. If documentation is incomplete, send query to provider before final coding.
4. Assign diagnosis codes (ICD-10)
5. Assign procedure codes (CPT)
6. Link diagnoses to procedures
7. Mark encounter as "Coded - Ready to Bill"

---

### Role 5: Billing Specialist

**Responsibilities:**
- Create insurance claims
- Scrub claims for errors
- Submit claims to clearinghouse
- Track claim status
- Correct and resubmit rejected claims
- Track 999/277CA/clearinghouse acknowledgment
- Fix claim rejections (separate from denial workflow)

**Permissions:**

| Module | Create | Read | Update | Delete | Notes |
|--------|--------|------|--------|--------|-------|
| Patients | ❌ | ✅ | ❌ | ❌ | View demographics |
| Patient Insurance | ❌ | ✅ | ⚠️ | ❌ | View insurance, limited update |
| Encounters | ❌ | ✅ | ❌ | ❌ | View coded encounters |
| Charges | ❌ | ✅ | ⚠️ | ❌ | View charges, limited edit |
| Claims | ✅ | ✅ | ✅ | ❌ | Full claim management |
| Claim Lines | ✅ | ✅ | ✅ | ❌ | Manage claim line items |
| Claim Scrubbing | ✅ | ✅ | ❌ | ❌ | Run scrubbing, view errors |
| Authorizations | ❌ | ✅ | ❌ | ❌ | View auth numbers |
| Payers | ❌ | ✅ | ❌ | ❌ | View payer info |
| Contracts | ❌ | ✅ | ❌ | ❌ | View contract rates |
| Reports | ❌ | ⚠️ | ❌ | ❌ | Claim status reports |

**Restrictions:**
- Cannot post payments (AR team responsibility)
- Cannot manage denials (AR team responsibility)
- Cannot modify patient demographics
- Cannot delete claims

**Workflow:**
1. Review coded encounters → Create claim
2. Scrub claim → Fix errors
3. Mark as clean → Submit to clearinghouse
4. Monitor acknowledgments (999, 277CA) → Update claim status
5. Fix claim rejections immediately (rejection workflow is separate from denial workflow)

---

### Role 6: AR Manager (Accounts Receivable)

**Responsibilities:**
- Post insurance payments (ERA)
- Manage denied claims
- Submit appeals
- Follow up on aging claims
- Monitor AR metrics

**Permissions:**

| Module | Create | Read | Update | Delete | Notes |
|--------|--------|------|--------|--------|-------|
| Patients | ❌ | ✅ | ❌ | ❌ | View demographics |
| Claims | ❌ | ✅ | ⚠️ | ❌ | View claims, update status |
| Payments | ✅ | ✅ | ✅ | ❌ | Full payment posting |
| Payment Line Items | ✅ | ✅ | ✅ | ❌ | Post line-level payments |
| ERA Files | ✅ | ✅ | ❌ | ❌ | Import and process ERAs |
| Denials | ✅ | ✅ | ✅ | ❌ | Manage denials |
| Appeals | ✅ | ✅ | ✅ | ❌ | Create and track appeals |
| Adjustments | ✅ | ✅ | ✅ | ❌ | Post adjustments |
| Payers | ❌ | ✅ | ❌ | ❌ | View payer info |
| AR Follow-up Worklist | ❌ | ✅ | ✅ | ❌ | Manage follow-up tasks |
| Contracts | ❌ | ✅ | ❌ | ❌ | View contract rates |
| Reports | ❌ | ✅ | ❌ | ❌ | AR aging, denial reports |

**Restrictions:**
- Cannot create or submit claims
- Cannot modify patient demographics
- Cannot delete payments

**Workflow:**
1. Import ERA file → Auto-post payments
2. Review unapplied payments → Manually post
3. Identify denials → Assign to denial worklist with denial reason category and appeal deadline
4. Review denial → Create appeal or correct claim, log payer call notes and next action date
5. Monitor AR aging → Follow up with payers

---

### Role 7: Collections Staff

**Responsibilities:**
- Generate patient statements
- Process patient payments
- Set up payment plans
- Make collection calls
- Send accounts to external collections

**Permissions:**

| Module | Create | Read | Update | Delete | Notes |
|--------|--------|------|--------|--------|-------|
| Patients | ❌ | ✅ | ⚠️ | ❌ | View demographics, update contact info |
| Patient Statements | ✅ | ✅ | ❌ | ❌ | Generate statements |
| Patient Payments | ✅ | ✅ | ❌ | ❌ | Process payments |
| Payment Plans | ✅ | ✅ | ✅ | ❌ | Manage payment plans |
| Collections | ✅ | ✅ | ✅ | ❌ | Manage collection accounts (External collections require approval) |
| Charity Care | ⚠️ | ✅ | ⚠️ | ❌ | Screen for charity care |
| Refunds | ⚠️ | ✅ | ❌ | ❌ | Request refunds (Requires approval from Collections Manager, AR Manager, or Finance Manager) |
| Claims | ❌ | ⚠️ | ❌ | ❌ | View claim status only |
| Reports | ❌ | ⚠️ | ❌ | ❌ | Patient AR reports |

**Restrictions:**
- Cannot access insurance claims
- Cannot post insurance payments
- Cannot modify charges or clinical data

**Workflow:**
1. Generate monthly statements → Mail/email to patients
2. Patient calls → Process payment or set up plan
3. Account >90 days → Make collection call
4. Account >120 days → Send to external collections

---

### Role 8: Finance Manager

**Responsibilities:**
- Monitor RCM performance metrics
- Generate financial reports
- Analyze revenue trends
- Oversee AR and collections
- Strategic decision-making

**Permissions:**

| Module | Create | Read | Update | Delete | Notes |
|--------|--------|------|--------|--------|-------|
| Patients | ❌ | ✅ | ❌ | ❌ | View demographics |
| Encounters | ❌ | ✅ | ❌ | ❌ | View encounter data |
| Charges | ❌ | ✅ | ❌ | ❌ | View charge data |
| Claims | ❌ | ✅ | ❌ | ❌ | View claim data |
| Payments | ❌ | ✅ | ❌ | ❌ | View payment data |
| Denials | ❌ | ✅ | ❌ | ❌ | View denial data |
| Collections | ❌ | ✅ | ❌ | ❌ | View collection data |
| Contracts | ❌ | ✅ | ⚠️ | ❌ | View contracts, approve changes |
| Reports | ✅ | ✅ | ✅ | ❌ | Full reporting access (Archive/Disable instead of Delete) |
| Dashboards | ✅ | ✅ | ✅ | ❌ | Create custom dashboards |

**Restrictions:**
- Cannot modify operational data (read-only for most modules)
- Cannot create claims or post payments
- Cannot modify patient records

**Key Reports:**
- Daily revenue report
- Monthly revenue by department/provider/payer
- AR aging report
- Denial rate and overturn rate
- Clean claim rate
- Days in AR
- Net collection rate
- Cost to collect

---

### Role 9: Compliance Officer

**Responsibilities:**
- Conduct internal audits
- Monitor compliance alerts
- Review audit logs
- Ensure HIPAA compliance
- Investigate fraud/abuse

**Permissions:**

| Module | Create | Read | Update | Delete | Notes |
|--------|--------|------|--------|--------|-------|
| Patients | ❌ | ✅ | ❌ | ❌ | View for audits |
| Encounters | ❌ | ✅ | ❌ | ❌ | View for coding audits |
| Charges | ❌ | ✅ | ❌ | ❌ | View for billing audits |
| Claims | ❌ | ✅ | ❌ | ❌ | View for compliance audits |
| Payments | ❌ | ✅ | ❌ | ❌ | View for payment audits |
| Audit Logs | ❌ | ✅ | ❌ | ❌ | Full audit log access |
| Compliance Alerts | ❌ | ✅ | ✅ | ❌ | Review and resolve alerts |
| NCCI Edits | ❌ | ✅ | ❌ | ❌ | View edit violations |
| LCD/NCD Rules | ❌ | ✅ | ❌ | ❌ | View coverage rules |
| Reports | ✅ | ✅ | ❌ | ❌ | Compliance reports |

**Special Permissions:**
- View all audit logs (including admin actions)
- Run random audit samples
- Flag accounts for review
- Generate compliance reports
- Review emergency access (Break-the-Glass) logs
- Monitor unusual access patterns
- Review role changes
- Close compliance alerts with a mandatory reason

**Key Reports:**
- Coding accuracy audit
- Upcoding detection report
- Unbundling detection report
- HIPAA access audit
- Overpayment report

---

### Role 10: Provider (Doctor)

**Responsibilities:**
- Document patient encounters
- Write orders (labs, imaging, medications)
- Review and sign encounters
- Approve charges

**Permissions:**

| Module | Create | Read | Update | Delete | Notes |
|--------|--------|------|--------|--------|-------|
| Patients | ❌ | ✅ | ❌ | ❌ | View patient demographics |
| Encounters | ⚠️ | ✅ | ✅ | ❌ | View own encounters, document visits |
| Orders | ✅ | ✅ | ✅ | ⚠️ | Full order management |
| Diagnoses | ✅ | ✅ | ✅ | ⚠️ | Document diagnoses |
| Procedures | ✅ | ✅ | ✅ | ⚠️ | Document procedures |
| Referrals | ✅ | ✅ | ✅ | ❌ | Create referrals |
| Authorizations | ❌ | ✅ | ❌ | ❌ | View auth status |
| Charges | ❌ | ⚠️ | ❌ | ❌ | View charges for own encounters |
| Claims | ❌ | ❌ | ❌ | ❌ | No claim access |
| Reports | ❌ | ⚠️ | ❌ | ❌ | Provider productivity report |

**Restrictions:**
- Can only view own encounters (not other providers')
- Cannot access billing or payment modules
- Cannot view financial data
- Cannot modify patient demographics

**Workflow:**
1. Patient checked in → Open encounter
2. Document visit (SOAP notes)
3. Enter diagnoses and procedures
4. Write orders (labs, meds, imaging)
5. Sign encounter (with e-signature timestamp) → Confirms clinical services and sends to coding.

*Note: Provider signs encounter and confirms clinical services. Billing/coding team validates charge/coding rules.*

---

## 4. Permission Levels Explained

| Symbol | Meaning | Description |
|--------|---------|-------------|
| ✅ | Full Access | Can perform action without restrictions |
| ⚠️ | Limited Access | Can perform action with restrictions (e.g., only own records) |
| ❌ | No Access | Cannot perform action |

*Note: Limited access can be based on own records, assigned worklist, department, branch, tenant, or emergency access.*

---

## 5. Data Access Restrictions

### Patient Data Access Rules:

| Role | Access Scope |
|------|--------------|
| System Administrator | All patients |
| Front Desk | All patients |
| Clinical Staff | Patients they are treating |
| Medical Coder | Encounters assigned to them |
| Billing Specialist | All patients (for billing) |
| AR Manager | All patients (for AR) |
| Collections Staff | Patients with balances |
| Finance Manager | All patients (aggregated data) |
| Compliance Officer | All patients (for audits) |
| Provider | Only their own patients |
| Tenant/Branch Admin | Only assigned tenant/branch |
| Prior Authorization Specialist | Patients/orders assigned for authorization |
| External Auditor | Temporary read-only access |

### Break-the-Glass Access:
- Emergency access to any patient record
- User must enter a reason before access is granted.
- Automatically logged and flagged for review.
- Compliance Officer must review break-the-glass access within a defined timeframe.
- Available to: Providers, Clinical Staff (in emergencies only)

---

## 6. Approval Workflows

### Approval Status Flow:
Requested -> Pending Review -> Approved -> Processed -> Completed or Rejected

### Rules:
- **Maker-Checker Rule:** The request creator cannot approve the same request.

### Actions Requiring Approval:

| Action | Requires Approval From | Approval Method |
|--------|------------------------|-----------------|
| Write-off >$1,000 | AR Manager or Finance Manager | In-app approval |
| Refund >$500 | Finance Manager | In-app approval |
| Delete user | System Administrator | In-app approval |
| Modify contract rates | Finance Manager | In-app approval |
| Send to external collections | Collections Manager | In-app approval |
| Charity care approval | Financial Counselor | In-app approval |

---

## 7. Session Management

### Session Rules:
- **Session Timeout:** 15 minutes of inactivity
- **Maximum Concurrent Sessions:** 1 per user (prevent account sharing)
- **Password Expiration:** Every 90 days
- **Failed Login Lockout:** 5 failed attempts → Account locked for 30 minutes
- **Password Complexity:** Minimum 8 characters, uppercase, lowercase, number, special character

---

## 8. Audit Requirements

**General Logged Fields:**
In addition to specific data, all audit logs must include: module name, record ID, device/browser, IP/location, old value, new value, and reason for change (where applicable).

### Actions That Are Audited:

| Action | Logged Data |
|--------|-------------|
| Patient record access | User, patient, timestamp, IP address |
| Patient data modification | User, patient, field changed, before/after values |
| Claim submission | User, claim ID, timestamp |
| Payment posting | User, payment amount, claim ID, timestamp |
| Write-off | User, amount, reason, timestamp |
| Refund | User, amount, recipient, timestamp |
| User login/logout | User, timestamp, IP address |
| Report generation | User, report type, parameters, timestamp |

**Additional Audited Actions:**
- Authorization request submitted
- Document uploaded
- Status updated
- Authorization number updated

**Audit Log Retention:** 7 years (HIPAA requirement)

---

## 9. Implementation Notes for Developers

### Database Schema:
```sql
CREATE TABLE roles (
  role_id UUID PRIMARY KEY,
  role_name VARCHAR(50) UNIQUE NOT NULL,
  permissions JSONB NOT NULL
);

CREATE TABLE users (
  user_id UUID PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  role_id UUID REFERENCES roles(role_id),
  user_status VARCHAR(20) NOT NULL,
  tenant_id UUID,
  branch_id UUID,
  mfa_enabled BOOLEAN DEFAULT FALSE,
  last_login_at TIMESTAMP,
  failed_login_count INT DEFAULT 0
);
```

### Permissions JSON Structure:
```json
{
  "patients": {
    "create": true,
    "read": true,
    "update": true,
    "delete": false,
    "scope": "all",
    "conditions": {}
  },
  "encounters": {
    "create": false,
    "read": true,
    "update": false,
    "delete": false,
    "scope": "assigned"
  }
}
```

### Middleware Example (Node.js):
```javascript
function checkPermission(resource, action) {
  return (req, res, next) => {
    const userRole = req.user.role;
    const permissions = userRole.permissions;
    
    if (permissions[resource]?.[action]) {
      next();
    } else {
      res.status(403).json({ error: 'Forbidden' });
    }
  };
}

// Usage:
app.post('/api/patients', 
  checkPermission('patients', 'create'), 
  createPatient
);
```

---

## 10. Security Best Practices

1. **Principle of Least Privilege:** Users only get permissions they need
2. **Separation of Duties:** No single user can complete entire billing cycle alone. Billing and payment duties must stay separated.
3. **Regular Access Reviews:** Quarterly review of user permissions. Access review evidence must be documented.
4. **Immediate Revocation:** Disable access immediately upon termination.
5. **Role Assignment Approval:** New user role assignments require manager approval.
6. **Access Requests:** New access requires manager approval.
7. **Temporary Access:** Temporary access must expire automatically.

---

**Next Document:** API Integration Requirements
