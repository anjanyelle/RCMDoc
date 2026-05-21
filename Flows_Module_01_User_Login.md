# Module 1: User Login & Authentication - Complete Flow Documentation

**Version:** 1.0  
**Module ID:** MOD-001  
**Category:** Authentication & Security

---

## 1. Module Overview

### Purpose
Secure user authentication system that verifies user credentials and provides role-based access to the RCM application.

### Why Hospitals Use It
- **Security:** Protects sensitive patient data (HIPAA compliance)
- **Access Control:** Different users see different features based on roles
- **Audit Trail:** Track who accessed what and when
- **Compliance:** Required for healthcare regulations

### Main Users Involved
- All system users (Front Desk, Doctors, Billing Staff, Admin, etc.)

---

## 2. Actors Involved

```
┌─────────────────────────────────────────────────┐
│ ACTORS IN LOGIN MODULE                          │
├─────────────────────────────────────────────────┤
│                                                  │
│ 1. User (Any Role)                              │
│    - Front Desk Staff                           │
│    - Doctor                                      │
│    - Medical Coder                               │
│    - Billing Manager                             │
│    - AR Team                                     │
│    - Admin                                       │
│                                                  │
│ 2. System                                        │
│    - Authentication Service                      │
│    - Database                                    │
│    - Session Manager                             │
│                                                  │
│ 3. External Systems                              │
│    - Active Directory (Optional)                 │
│    - SSO Provider (Optional)                     │
│    - 2FA Service (Twilio for SMS)               │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 3. Step-by-Step Workflow

### Flow Diagram

```
┌─────────────────────┐
│   User Opens App    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Login Page Loads   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Enter Username &    │
│ Password            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Click Login Button  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Frontend Validates  │
│ (Not Empty)         │
└──────────┬──────────┘
           ↓
    ┌──────┴──────┐
    │ Valid?      │
    └──┬──────┬───┘
  No   │      │ Yes
       ↓      ↓
┌──────────┐ ┌──────────────────┐
│Show Error│ │Send to Backend   │
└──────────┘ │POST /auth/login  │
             └────────┬─────────┘
                      ↓
             ┌──────────────────┐
             │Backend Validates │
             │Credentials       │
             └────────┬─────────┘
                      ↓
               ┌──────┴──────┐
               │ Valid?      │
               └──┬──────┬───┘
             No   │      │ Yes
                  ↓      ↓
          ┌──────────┐ ┌──────────────────┐
          │Return 401│ │Check 2FA Enabled?│
          └──────────┘ └────────┬─────────┘
                                ↓
                         ┌──────┴──────┐
                         │ 2FA?        │
                         └──┬──────┬───┘
                       No   │      │ Yes
                            ↓      ↓
                    ┌──────────┐ ┌──────────────────┐
                    │Generate  │ │Send OTP via SMS  │
                    │JWT Token │ └────────┬─────────┘
                    └────┬─────┘          ↓
                         │       ┌──────────────────┐
                         │       │User Enters OTP   │
                         │       └────────┬─────────┘
                         │                ↓
                         │       ┌──────────────────┐
                         │       │Verify OTP        │
                         │       └────────┬─────────┘
                         │                ↓
                         │         ┌──────┴──────┐
                         │         │ Valid?      │
                         │         └──┬──────┬───┘
                         │       No   │      │ Yes
                         │            ↓      ↓
                         │    ┌──────────┐ ┌──────────┐
                         │    │Show Error│ │Generate  │
                         │    └──────────┘ │JWT Token │
                         │                 └────┬─────┘
                         └──────────────────────┘
                                  ↓
                         ┌──────────────────┐
                         │Create Session    │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │Log Audit Entry   │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │Return User Data  │
                         │& Token           │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │Frontend Stores   │
                         │Token in Cookie   │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │Redirect to       │
                         │Dashboard         │
                         └──────────────────┘
```

---

## 4. Action Plan

### Frontend Actions

**Technology:** React.js + TypeScript

**File:** `src/pages/Login.tsx`

```typescript
// What Frontend Does:

1. Display login form
   - Username/Email field
   - Password field
   - Remember Me checkbox
   - Login button
   - Forgot Password link

2. Validate inputs
   - Check if fields are not empty
   - Check email format (if using email)
   - Check password minimum length

3. Submit credentials
   - POST request to /api/auth/login
   - Send { username, password }

4. Handle response
   - Success: Store JWT token in localStorage/cookie
   - Success: Redirect to dashboard
   - Failure: Show error message
   - 2FA Required: Show OTP input screen

5. Handle 2FA
   - Display OTP input field
   - Submit OTP to /api/auth/verify-otp
   - Verify and complete login

6. Store user session
   - Save JWT token
   - Save user info (name, role, permissions)
   - Set session timeout (15 minutes)
```

**Code Example:**
```typescript
const handleLogin = async (e: FormEvent) => {
  e.preventDefault();
  
  // Frontend validation
  if (!username || !password) {
    setError('Please enter username and password');
    return;
  }
  
  setLoading(true);
  
  try {
    // API call
    const response = await api.post('/auth/login', {
      username,
      password
    });
    
    if (response.data.requires2FA) {
      // Show OTP screen
      setShow2FA(true);
    } else {
      // Store token and redirect
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      navigate('/dashboard');
    }
  } catch (err) {
    setError(err.response?.data?.message || 'Login failed');
  } finally {
    setLoading(false);
  }
};
```

---

### Refresh Token Architecture

#### Purpose
Improve security by separating short-lived access tokens and long-lived refresh tokens.

#### Workflow

```text
User Login
    ↓
Generate Access Token (15 min)
    ↓
Generate Refresh Token (7 days)
    ↓
Store Refresh Token in Database/Redis
    ↓
Return Both Tokens
    ↓
Access Token Expires
    ↓
Frontend Calls /refresh-token
    ↓
Backend Verifies Refresh Token
    ↓
Generate New Access Token
```

#### Database Table
```sql
CREATE TABLE refresh_tokens (
    refresh_token_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    token_hash TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    is_revoked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Security Features
- Token rotation
- Token revocation
- Logout-all-devices
- Device-specific refresh tokens

---

### Backend Actions

**Technology:** Python FastAPI

**File:** `app/api/v1/auth.py`

```python
# What Backend Does:

1. Receive login request
   - Extract username and password from request body
   - Validate request format

2. Find user in database
   - Query users table by username/email
   - Check if user exists

3. Verify password
   - Hash submitted password
   - Compare with stored hash
   - Use bcrypt for hashing

4. Check account status
   - Is account active?
   - Is account locked?
   - Is password expired?

5. Check 2FA requirement
   - If enabled, generate OTP
   - Send OTP via Twilio SMS
   - Store OTP in Redis (5 min expiry)

6. Generate JWT token
   - Create token with user_id, role, permissions
   - Set expiration (24 hours)
   - Sign with secret key

7. Create session
   - Store session in Redis
   - Set session timeout (15 minutes)

8. Log audit entry
   - Record login attempt
   - Store IP address, timestamp
   - Store user agent

9. Return response
   - Send token, user data, permissions
```

**Code Example:**
```python
@router.post("/login")
async def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
    request: Request = None
):
    # Find user
    user = db.query(User).filter(
        User.username == credentials.username
    ).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        # Log failed attempt
        log_failed_login(user.user_id, request.client.host)
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Check if account is active
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled")
    
    # Check 2FA
    if user.two_factor_enabled:
        # Generate and send OTP
        otp = generate_otp()
        send_sms(user.phone, f"Your OTP: {otp}")
        redis_client.setex(f"otp:{user.user_id}", 300, otp)
        
        return {
            "requires2FA": True,
            "userId": user.user_id
        }
    
    # Generate JWT token
    token = create_access_token(
        data={
            "user_id": user.user_id,
            "role": user.role,
            "permissions": user.permissions
        }
    )
    
    # Create session
    create_session(user.user_id, token)
    
    # Log successful login
    log_audit(
        user_id=user.user_id,
        action="LOGIN",
        ip_address=request.client.host
    )
    
    return {
        "token": token,
        "user": {
            "userId": user.user_id,
            "name": user.full_name,
            "role": user.role,
            "permissions": user.permissions
        }
    }
```

---

### Database Actions

**Tables Updated:**

1. **users** - Read user record
2. **user_sessions** - Create new session
3. **audit_logs** - Insert login audit entry
4. **failed_login_attempts** - Track failed attempts (if failed)

**SQL Operations:**

```sql
-- 1. Find user
SELECT user_id, username, password_hash, role, is_active, two_factor_enabled
FROM users
WHERE username = 'john.doe';

-- 2. Create session
INSERT INTO user_sessions (user_id, token, ip_address, created_at, expires_at)
VALUES ('USR-001', 'jwt_token_here', '192.168.1.1', NOW(), NOW() + INTERVAL '15 minutes');

-- 3. Log audit entry
INSERT INTO audit_logs (user_id, action, ip_address, timestamp)
VALUES ('USR-001', 'LOGIN', '192.168.1.1', NOW());

-- 4. Track failed attempt (if password wrong)
INSERT INTO failed_login_attempts (username, ip_address, attempted_at)
VALUES ('john.doe', '192.168.1.1', NOW());
```

---

### Additional Security Tables

#### trusted_devices

```sql
CREATE TABLE trusted_devices (
    device_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    device_name VARCHAR(255),
    browser VARCHAR(100),
    os VARCHAR(100),
    ip_address VARCHAR(50),
    last_used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### password_reset_tokens

```sql
CREATE TABLE password_reset_tokens (
    reset_token_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    token_hash TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### API Calls

**Internal APIs:**
- `POST /api/auth/login` - Main login endpoint
- `POST /api/auth/verify-otp` - Verify 2FA code
- `POST /api/auth/refresh-token` - Refresh expired token
- `POST /api/auth/logout` - End session

**External APIs:**
- **Twilio SMS API** (if 2FA enabled)
  - Endpoint: `https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json`
  - Purpose: Send OTP via SMS
  - Cost: $0.0079 per SMS

**Example Twilio Call:**
```python
from twilio.rest import Client

def send_otp_sms(phone: str, otp: str):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    message = client.messages.create(
        body=f"Your RCM login code is: {otp}. Valid for 5 minutes.",
        from_=TWILIO_PHONE_NUMBER,
        to=phone
    )
    
    return message.sid
```

---

### Validations

**Frontend Validations:**
```
1. Username/Email:
   - Not empty
   - Valid email format (if using email)
   - Min 3 characters

2. Password:
   - Not empty
   - Min 8 characters
   - Contains uppercase, lowercase, number, special char

3. OTP (if 2FA):
   - Exactly 6 digits
   - Only numbers
```

**Backend Validations:**
```
1. Request Format:
   - Valid JSON
   - Required fields present

2. User Existence:
   - User exists in database
   - Account is active
   - Account not locked

3. Password:
   - Matches stored hash
   - Not expired (if policy enabled)

4. Rate Limiting:
   - Max 5 attempts per 15 minutes
   - Lock account after 10 failed attempts

5. IP Whitelisting (Optional):
   - Check if IP is allowed
```

---

### Notifications

**Success Notifications:**
```
1. Email (Optional):
   - "New login detected from [IP] at [Time]"
   - Sent to user's email
   - Include "Not you?" link

2. SMS (if 2FA):
   - "Your OTP: 123456"
   - Valid for 5 minutes

3. In-App:
   - "Welcome back, [Name]!"
   - Show last login time
```

**Failure Notifications:**
```
1. Failed Login Alert:
   - After 3 failed attempts
   - Email to user: "Multiple failed login attempts detected"

2. Account Locked:
   - After 10 failed attempts
   - Email to user and admin
   - "Your account has been locked. Contact support."

3. Suspicious Activity:
   - Login from new location
   - Login from new device
   - Email: "New login from [Location]. Was this you?"
```

---

## 5. Use Case Diagram

```
                    ┌─────────────────────────────────────┐
                    │   LOGIN & AUTHENTICATION SYSTEM     │
                    └─────────────────────────────────────┘

┌──────────┐                                        ┌──────────────┐
│          │                                        │              │
│   User   │───────────────────────────────────────│ Enter Login  │
│          │                                        │ Credentials  │
└────┬─────┘                                        └──────────────┘
     │                                                      │
     │                                              ┌───────┴───────┐
     │                                              │               │
     │                                         ┌────▼────┐    ┌────▼────┐
     │                                         │ Username│    │Password │
     │                                         │Validation│    │Validation│
     │                                         └─────────┘    └─────────┘
     │                                                      
     │                                              ┌──────────────┐
     ├──────────────────────────────────────────────│ Authenticate │
     │                                              │ User         │
     │                                              └──────┬───────┘
     │                                                     │
     │                                              ┌──────┴───────┐
     │                                              │              │
     │                                         ┌────▼────┐    ┌────▼────┐
     │                                         │ Verify  │    │ Check   │
     │                                         │Password │    │Account  │
     │                                         └─────────┘    │Status   │
     │                                                        └─────────┘
     │                                                      
     │                                              ┌──────────────┐
     ├──────────────────────────────────────────────│ Handle 2FA   │
     │                                              │ (Optional)   │
     │                                              └──────┬───────┘
     │                                                     │
     │                                              ┌──────┴───────┐
     │                                              │              │
     │                                         ┌────▼────┐    ┌────▼────┐
     │                                         │Generate │    │ Verify  │
     │                                         │  OTP    │    │  OTP    │
     │                                         └─────────┘    └─────────┘
     │                                                      
     │                                              ┌──────────────┐
     ├──────────────────────────────────────────────│ Create       │
     │                                              │ Session      │
     │                                              └──────┬───────┘
     │                                                     │
     │                                              ┌──────┴───────┐
     │                                              │              │
     │                                         ┌────▼────┐    ┌────▼────┐
     │                                         │Generate │    │  Store  │
     │                                         │JWT Token│    │ Session │
     │                                         └─────────┘    └─────────┘
     │                                                      
     │                                              ┌──────────────┐
     └──────────────────────────────────────────────│ Access       │
                                                    │ Dashboard    │
                                                    └──────────────┘

┌──────────┐                                        ┌──────────────┐
│          │                                        │              │
│  System  │───────────────────────────────────────│ Log Audit    │
│          │                                        │ Entry        │
└──────────┘                                        └──────────────┘

┌──────────┐                                        ┌──────────────┐
│          │                                        │              │
│ Twilio   │───────────────────────────────────────│ Send OTP SMS │
│   API    │                                        │              │
└──────────┘                                        └──────────────┘
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
│ User Opens Login    │
│ Page                │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Display Login Form  │
│ - Username field    │
│ - Password field    │
│ - Login button      │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ User Enters         │
│ Credentials         │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ User Clicks Login   │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Valid?╲────No────┐
  ╲     ╱           │
   ╲   ╱            │
    ╲ ╱             │
     │Yes           │
     │              ▼
     │         ┌─────────────────────┐
     │         │ Show Error Message  │
     │         │ "Please fill all    │
     │         │  fields"            │
     │         └────┬────────────────┘
     │              │
     │              │
     ▼              │
┌─────────────────────┐
│ Send POST Request   │
│ to Backend          │
│ /api/auth/login     │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Backend Queries     │
│ Database for User   │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱User  ╲────No────┐
  ╲Exists?╱         │
   ╲   ╱            │
    ╲ ╱             │
     │Yes           │
     │              ▼
     │         ┌─────────────────────┐
     │         │ Return 401 Error    │
     │         │ "Invalid credentials"│
     │         └────┬────────────────┘
     │              │
     ▼              │
┌─────────────────────┐
│ Verify Password     │
│ (bcrypt compare)    │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Pass  ╲────No────┐
  ╲Valid? ╱         │
   ╲   ╱            │
    ╲ ╱             │
     │Yes           │
     │              ▼
     │         ┌─────────────────────┐
     │         │ Log Failed Attempt  │
     │         │ Return 401 Error    │
     │         └────┬────────────────┘
     │              │
     ▼              │
┌─────────────────────┐
│ Check Account       │
│ Status              │
└────┬────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱Active?╲────No────┐
  ╲     ╱            │
   ╲   ╱             │
    ╲ ╱              │
     │Yes            │
     │               ▼
     │         ┌─────────────────────┐
     │         │ Return 403 Error    │
     │         │ "Account disabled"  │
     │         └─────────────────────┘
     │
     ▼
    ╱ ╲
   ╱   ╲
  ╱ 2FA  ╲────No─────┐
  ╲Enabled?╱         │
   ╲   ╱             │
    ╲ ╱              │
     │Yes            │
     │               │
     ▼               │
┌─────────────────────┐
│ Generate 6-digit    │
│ OTP                 │
└────┬────────────────┘
     │                │
     ▼                │
┌─────────────────────┐
│ Send OTP via        │
│ Twilio SMS          │
└────┬────────────────┘
     │                │
     ▼                │
┌─────────────────────┐
│ Store OTP in Redis  │
│ (5 min expiry)      │
└────┬────────────────┘
     │                │
     ▼                │
┌─────────────────────┐
│ Return Response:    │
│ requires2FA: true   │
└────┬────────────────┘
     │                │
     ▼                │
┌─────────────────────┐
│ User Enters OTP     │
└────┬────────────────┘
     │                │
     ▼                │
┌─────────────────────┐
│ Verify OTP from     │
│ Redis               │
└────┬────────────────┘
     │                │
     ▼                │
    ╱ ╲               │
   ╱   ╲              │
  ╱ OTP  ╲────No──────┤
  ╲Valid? ╱           │
   ╲   ╱              │
    ╲ ╱               │
     │Yes             │
     │                │
     ▼◄───────────────┘
┌─────────────────────┐
│ Generate JWT Token  │
│ - user_id           │
│ - role              │
│ - permissions       │
│ - expires: 24h      │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Create Session in   │
│ Redis               │
│ - timeout: 15 min   │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Insert Audit Log    │
│ - action: LOGIN     │
│ - timestamp         │
│ - IP address        │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Return Response:    │
│ - token             │
│ - user data         │
│ - permissions       │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Frontend Stores     │
│ Token in localStorage│
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Redirect to         │
│ Dashboard           │
└────┬────────────────┘
     │
     ▼
┌─────────┐
│   END   │
└─────────┘
```

---

## 7. Sequence Diagram

```
User          Frontend         Backend API      Database       Redis        Twilio
 │                │                │               │             │            │
 │  Open App      │                │               │             │            │
 ├───────────────>│                │               │             │            │
 │                │                │               │             │            │
 │                │ Load Login Page│               │             │            │
 │                │                │               │             │            │
 │  Enter         │                │               │             │            │
 │  Credentials   │                │               │             │            │
 ├───────────────>│                │               │             │            │
 │                │                │               │             │            │
 │  Click Login   │                │               │             │            │
 ├───────────────>│                │               │             │            │
 │                │                │               │             │            │
 │                │ Validate Form  │               │             │            │
 │                │                │               │             │            │
 │                │ POST /auth/login               │             │            │
 │                ├───────────────>│               │             │            │
 │                │                │               │             │            │
 │                │                │ SELECT user   │             │            │
 │                │                ├──────────────>│             │            │
 │                │                │               │             │            │
 │                │                │ User Record   │             │            │
 │                │                │<──────────────┤             │            │
 │                │                │               │             │            │
 │                │                │ Verify Password             │            │
 │                │                │ (bcrypt)      │             │            │
 │                │                │               │             │            │
 │                │                │ Check 2FA     │             │            │
 │                │                │               │             │            │
 │                │                │ Generate OTP  │             │            │
 │                │                │               │             │            │
 │                │                │               │ Store OTP   │            │
 │                │                │               ├────────────>│            │
 │                │                │               │             │            │
 │                │                │               │             │ Send SMS   │
 │                │                │               │             ├───────────>│
 │                │                │               │             │            │
 │                │                │               │             │ SMS Sent   │
 │                │                │               │             │<───────────┤
 │                │                │               │             │            │
 │                │ Response:      │               │             │            │
 │                │ requires2FA    │               │             │            │
 │                │<───────────────┤               │             │            │
 │                │                │               │             │            │
 │  Show OTP      │                │               │             │            │
 │  Input         │                │               │             │            │
 │<───────────────┤                │               │             │            │
 │                │                │               │             │            │
 │  Enter OTP     │                │               │             │            │
 ├───────────────>│                │               │             │            │
 │                │                │               │             │            │
 │                │ POST /auth/verify-otp          │             │            │
 │                ├───────────────>│               │             │            │
 │                │                │               │             │            │
 │                │                │               │ Get OTP     │            │
 │                │                │               ├────────────>│            │
 │                │                │               │             │            │
 │                │                │               │ OTP Value   │            │
 │                │                │               │<────────────┤            │
 │                │                │               │             │            │
 │                │                │ Verify OTP    │             │            │
 │                │                │               │             │            │
 │                │                │ Generate JWT  │             │            │
 │                │                │               │             │            │
 │                │                │               │ Store Session            │
 │                │                │               ├────────────>│            │
 │                │                │               │             │            │
 │                │                │ INSERT audit_log            │            │
 │                │                ├──────────────>│             │            │
 │                │                │               │             │            │
 │                │ Response:      │               │             │            │
 │                │ token, user    │               │             │            │
 │                │<───────────────┤               │             │            │
 │                │                │               │             │            │
 │                │ Store Token    │               │             │            │
 │                │                │               │             │            │
 │  Redirect to   │                │               │             │            │
 │  Dashboard     │                │               │             │            │
 │<───────────────┤                │               │             │            │
 │                │                │               │             │            │
```

---

## 8. API Flow

### API Endpoint 1: Login

**Request:**
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "john.doe",
  "password": "SecurePass123!"
}
```

**Response (Success - No 2FA):**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "userId": "USR-001",
    "username": "john.doe",
    "fullName": "John Doe",
    "role": "front_desk",
    "permissions": ["patient.create", "patient.read", "appointment.create"]
  },
  "expiresAt": "2026-05-19T19:13:00Z"
}
```

**Response (Success - 2FA Required):**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "requires2FA": true,
  "userId": "USR-001",
  "message": "OTP sent to your phone ending in ****1234"
}
```

**Response (Error - Invalid Credentials):**
```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "error": "Invalid credentials",
  "message": "Username or password is incorrect"
}
```

**Response (Error - Account Locked):**
```http
HTTP/1.1 403 Forbidden
Content-Type: application/json

{
  "error": "Account locked",
  "message": "Your account has been locked due to multiple failed login attempts. Contact support."
}
```

---

### API Endpoint 2: Verify OTP

**Request:**
```http
POST /api/auth/verify-otp
Content-Type: application/json

{
  "userId": "USR-001",
  "otp": "123456"
}
```

**Response (Success):**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "userId": "USR-001",
    "username": "john.doe",
    "fullName": "John Doe",
    "role": "front_desk",
    "permissions": ["patient.create", "patient.read"]
  }
}
```

**Response (Error - Invalid OTP):**
```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "error": "Invalid OTP",
  "message": "The OTP you entered is incorrect or has expired"
}
```

---

### API Endpoint 3: Logout

**Request:**
```http
POST /api/auth/logout
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "Logged out successfully"
}
```

---

## 8.1 Password Reset Flow

### Workflow

```text
User Clicks Forgot Password
        ↓
Enter Email Address
        ↓
Backend Validates User
        ↓
Generate Reset Token
        ↓
Send Email Link
        ↓
User Opens Reset Link
        ↓
Enter New Password
        ↓
Password Updated
        ↓
Audit Log Created
```

### API Endpoints
- Request Reset: `POST /api/auth/forgot-password`
- Reset Password: `POST /api/auth/reset-password`

### Security Features
- Token expiry (15 minutes)
- Single-use reset tokens
- Audit logging
- Password history validation

---

## 9. Database Flow

### Tables Involved

**1. users**
```sql
CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    role VARCHAR(50) NOT NULL,
    permissions TEXT[],
    is_active BOOLEAN DEFAULT TRUE,
    two_factor_enabled BOOLEAN DEFAULT FALSE,
    phone VARCHAR(20),
    last_login TIMESTAMP,
    password_expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**2. user_sessions**
```sql
CREATE TABLE user_sessions (
    session_id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES users(user_id),
    token TEXT NOT NULL,
    ip_address VARCHAR(50),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);
```

**3. audit_logs**
```sql
CREATE TABLE audit_logs (
    log_id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(50),
    action VARCHAR(100) NOT NULL,
    ip_address VARCHAR(50),
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details JSONB
);
```

**4. failed_login_attempts**
```sql
CREATE TABLE failed_login_attempts (
    attempt_id SERIAL PRIMARY KEY,
    username VARCHAR(100),
    ip_address VARCHAR(50),
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reason VARCHAR(100)
);
```

### Database Operations Flow

```
┌─────────────────────┐
│ 1. SELECT from      │
│    users table      │
│    WHERE username   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ 2. If password      │
│    wrong:           │
│    INSERT into      │
│    failed_login_    │
│    attempts         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ 3. If success:      │
│    INSERT into      │
│    user_sessions    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ 4. INSERT into      │
│    audit_logs       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ 5. UPDATE users     │
│    SET last_login   │
└─────────────────────┘
```

---

### Multi-Tenant Architecture

Purpose

Support multiple hospitals, clinics, provider groups, and healthcare organizations within a single RCM platform while maintaining complete data isolation and security.

Architecture Features

- Tenant-level data isolation
- Organization-based access control
- Facility-level segregation
- Shared application architecture
- Secure tenant-specific APIs
- Role-based tenant permissions
- Cross-facility restrictions
- Tenant-aware reporting

Tenant Hierarchy

```
Tenant
   ↓
Organization
   ↓
Facility
   ↓
Department
   ↓
Users
```

Database Isolation

Every major table contains:

- tenant_id
- organization_id
- facility_id

Purpose

- Prevent cross-hospital data leakage
- Support SaaS deployment
- Enable enterprise scalability
- Maintain HIPAA compliance
- Support multi-hospital systems

Security Controls

- Row-level security
- JWT tenant validation
- Tenant-aware API filtering
- Separate audit trails
- Encrypted tenant data

Example

Hospital A users cannot access:
- Hospital B patients
- claims
- payments
- providers
- reports

---

## 10. Error Scenarios

### Scenario 1: Invalid Credentials

**Trigger:** User enters wrong password

**Flow:**
```
User enters wrong password
   ↓
Backend verifies password → Fails
   ↓
INSERT into failed_login_attempts
   ↓
Check attempt count (last 15 min)
   ↓
If < 5 attempts:
   Return 401 "Invalid credentials"
   
If >= 5 attempts:
   Lock account (UPDATE users SET is_active = FALSE)
   Send email notification
   Return 403 "Account locked"
```

**Error Response:**
```json
{
  "error": "Invalid credentials",
  "message": "Username or password is incorrect",
  "attemptsRemaining": 2
}
```

---

### Scenario 2: Account Locked

**Trigger:** Too many failed login attempts

**Flow:**
```
Failed attempt count >= 5
   ↓
UPDATE users SET is_active = FALSE
   ↓
Send email to user
   ↓
Send email to admin
   ↓
Return 403 error
```

**Error Response:**
```json
{
  "error": "Account locked",
  "message": "Your account has been locked due to multiple failed login attempts. Please contact support at support@hospital.com"
}
```

**Unlock Process:**
```
Admin receives notification
   ↓
Admin verifies user identity
   ↓
Admin runs: UPDATE users SET is_active = TRUE WHERE user_id = 'USR-001'
   ↓
DELETE FROM failed_login_attempts WHERE username = 'john.doe'
   ↓
Send email to user: "Your account has been unlocked"
```

---

### Scenario 3: OTP Expired

**Trigger:** User enters OTP after 5 minutes

**Flow:**
```
User enters OTP
   ↓
Backend checks Redis for OTP
   ↓
OTP not found (expired after 5 min)
   ↓
Return 401 error
```

**Error Response:**
```json
{
  "error": "OTP expired",
  "message": "Your OTP has expired. Please request a new one."
}
```

**Retry Process:**
```
User clicks "Resend OTP"
   ↓
Generate new OTP
   ↓
Send new SMS
   ↓
Store in Redis (5 min expiry)
```

---

### Scenario 4: Session Expired

**Trigger:** User inactive for 15 minutes

**Flow:**
```
User makes API request
   ↓
Backend checks session in Redis
   ↓
Session expired (> 15 min)
   ↓
Return 401 "Session expired"
   ↓
Frontend redirects to login
```

**Error Response:**
```json
{
  "error": "Session expired",
  "message": "Your session has expired. Please login again."
}
```

---

### Scenario 5: Twilio API Failure

**Trigger:** SMS service is down

**Flow:**
```
Generate OTP
   ↓
Call Twilio API to send SMS
   ↓
Twilio returns error (500)
   ↓
Log error
   ↓
Fallback: Send OTP via email instead
   ↓
If email also fails:
   Return error to user
```

**Error Response:**
```json
{
  "error": "SMS service unavailable",
  "message": "Unable to send OTP via SMS. We've sent it to your email instead."
}
```

---

## 11. Dashboard & Status Flow

### User Status States

```
┌─────────────────────┐
│   User Created      │
│   (is_active: true) │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│   First Login       │
│   (force password   │
│    change)          │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│   Active User       │
│   (normal login)    │
└──────────┬──────────┘
           ↓
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌─────────┐  ┌─────────────────┐
│ Locked  │  │ Password Expired│
│ (failed │  │ (90 days)       │
│ attempts)│  └──────┬──────────┘
└────┬────┘         │
     │              ▼
     │     ┌─────────────────┐
     │     │ Force Password  │
     │     │ Change          │
     │     └──────┬──────────┘
     │            │
     ▼            ▼
┌─────────────────────┐
│   Admin Unlocks     │
│   or                │
│   Password Reset    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│   Active Again      │
└─────────────────────┘
```

### Session Status Flow

```
┌─────────────────────┐
│  Login Successful   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Session Created    │
│  (expires: 15 min)  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  User Active        │
│  (making requests)  │
└──────────┬──────────┘
           ↓
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌─────────┐  ┌─────────────────┐
│Activity │  │ No Activity     │
│Detected │  │ (15 min)        │
└────┬────┘  └──────┬──────────┘
     │              │
     ▼              ▼
┌─────────┐  ┌─────────────────┐
│ Extend  │  │ Session Expired │
│Session  │  └──────┬──────────┘
└────┬────┘         │
     │              ▼
     │     ┌─────────────────┐
     │     │ Redirect to     │
     │     │ Login           │
     │     └─────────────────┘
     │
     └──────────────┐
                    ▼
           ┌─────────────────┐
           │ User Logs Out   │
           └──────┬──────────┘
                  ↓
           ┌─────────────────┐
           │ Session Deleted │
           └─────────────────┘
```

---

## 12. Security & Compliance

### HIPAA Compliance

```
✅ Audit Logging
   - All login attempts logged
   - IP address recorded
   - Timestamp recorded
   - User agent recorded

✅ Session Management
   - 15-minute timeout
   - Automatic logout
   - Secure token storage

✅ Password Security
   - Bcrypt hashing (cost factor: 12)
   - Min 8 characters
   - Complexity requirements
   - 90-day expiration

✅ Account Lockout
   - 5 failed attempts = lock
   - Admin unlock required
   - Email notifications

✅ 2FA Support
   - Optional SMS-based OTP
   - 6-digit code
   - 5-minute expiry
```

### Role-Based Access Control

```
After Login → Check user.role → Load permissions

Roles:
- admin → Full access
- front_desk → Patient registration, appointments
- doctor → Clinical documentation, orders
- medical_coder → Coding, charge capture
- billing_manager → Claims, payments
- ar_team → AR management, collections
```

---

## 12.1 Advanced HIPAA Security

### Break-Glass Access

Emergency access workflow for critical patient care situations.

```text
Doctor Emergency Access Request
        ↓
Temporary Elevated Permissions
        ↓
Mandatory Reason Entry
        ↓
Audit Logging
        ↓
Automatic Expiration
```

### PHI Access Monitoring

Monitor:
- Patient chart access
- Failed access attempts
- Unauthorized access
- Bulk record exports

### Security Monitoring
- Suspicious login detection
- Impossible travel detection
- Brute-force attack monitoring
- Geo-location monitoring
- Device fingerprinting

### Session Security
- Concurrent session limits
- Forced logout
- Token revocation
- Session inactivity timeout

---

## 13. Third-Party APIs Used

### Twilio SMS API

**Purpose:** Send OTP for 2FA

**Endpoint:** `https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json`

**Request:**
```http
POST /Accounts/AC1234.../Messages.json
Authorization: Basic {base64(AccountSid:AuthToken)}
Content-Type: application/x-www-form-urlencoded

Body=Your%20RCM%20login%20code%20is%3A%20123456&From=%2B15551234567&To=%2B15559876543
```

**Response:**
```json
{
  "sid": "SM1234567890abcdef",
  "status": "queued",
  "to": "+15559876543",
  "from": "+15551234567"
}
```

**Cost:** $0.0079 per SMS

**Error Handling:**
- If Twilio fails → Fallback to email
- If both fail → Show error, allow manual OTP entry

---

## 13.1 Enterprise SSO Integration

### Supported Providers

- Microsoft Azure AD
- Okta
- Google Workspace
- Active Directory
- SAML Providers

### SSO Workflow

```text
User Clicks SSO Login
        ↓
Redirect to Identity Provider
        ↓
User Authenticates
        ↓
Provider Returns SAML/OAuth Token
        ↓
Backend Verifies Token
        ↓
Create Session
        ↓
Redirect to Dashboard
```

### Supported Standards
- OAuth2
- OpenID Connect
- SAML 2.0

---

## 14. Performance Metrics

### Target Metrics

```
Login Response Time: < 500ms
OTP Delivery Time: < 10 seconds
Session Creation: < 100ms
Database Query Time: < 50ms
JWT Generation: < 10ms
Success Rate: > 99.9%
```

### Monitoring

```
CloudWatch Metrics:
- Login attempts per minute
- Failed login rate
- Average response time
- OTP delivery success rate
- Session creation rate

Alerts:
- Failed login rate > 10%
- Response time > 1 second
- OTP delivery failure > 5%
```

---

## 14.1 Security Monitoring & Rate Limiting

### Rate Limiting

```text
Login Attempts:
- Max 5 attempts per 15 minutes
- CAPTCHA after repeated failures
- IP-based throttling
```

### Security Monitoring Stack

```
Security Monitoring
├── AWS WAF
├── CloudWatch
├── Datadog
├── Splunk
├── Sentry
└── SIEM Integration
```

### Monitoring Alerts
- Brute-force attack detection
- Multiple failed logins
- Suspicious geo-location login
- Excessive OTP requests
- Token abuse detection

---

## Enterprise Production Enhancements

### Recommended Enterprise Tools

| Area | Tool |
|---|---|
| Authentication | Auth0 / Keycloak |
| Session Store | Redis |
| Secrets Management | AWS Secrets Manager |
| API Gateway | Kong / AWS API Gateway |
| Security Monitoring | Splunk / Datadog |
| SSO | Azure AD / Okta |

### Enterprise Features

- Multi-tenant authentication
- Device management
- Refresh token rotation
- SSO integration
- Session revocation
- Security analytics
- Advanced audit logging
- HIPAA emergency access workflows

---

## Summary

**Module:** User Login & Authentication  
**Complexity:** Medium  
**Development Time:** 1 week  
**Dependencies:** Database, Redis, Twilio (optional)  
**Critical:** Yes (required for all other modules)  

**Key Features:**
✅ Secure password authentication  
✅ JWT token-based sessions  
✅ Optional 2FA via SMS  
✅ Account lockout protection  
✅ Audit logging  
✅ Role-based access control  
✅ Session management  
✅ HIPAA compliant  

---
