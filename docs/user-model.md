
## User Module (Model, Registration, Authentication, Login)

### Overview

This module implements authentication and role-based access control (RBAC) for the Smart Farmer-to-Buyer platform. It connects our React frontend with Django REST Framework (DRF) backend to register, authenticate, and direct users (FARMER or BUYER) to their respective dashboards.

---

### Component Architecture & System Flow

[ Frontend: React / React Router ]
  ├── Register.jsx / Login.jsx
  │     │ (REST Requests: POST /register/, POST /login/)
  │     ▼
  └── ProtectedRoute.jsx ──(Bearer Token)──► [ Django REST Framework ]
                                                   │
                                                   ├── serializers.py (Validation & Mapping)
                                                   ├── views.py (JWT Token Generation)
                                                   └── models.py (CustomUser Schema)

---

### Component Roles & Interactions

#### Backend Component Breakdown

**models.py** (**CustomUser**): Extends AbstractUser to enforce unique emails and store role choices (FARMER, BUYER) with helper properties (is_farmer, is_buyer). 
**serializers.py**: 
-(**RegisterSerializer**): Validates matching passwords, maps frontend camelCase input (firstName, lastName) to backend snake_case model fields, normalizes role strings to uppercase, and creates user accounts securely. 
-(**LoginSerializer**): Authenticates active users via email and password. UserSerializer: Formats user profile attributes for output responses. 
**views.py**: 
-(**RegisterView & LoginView**): Execute user actions and generate JWT access/refresh token pairs via SimpleJWT. 
-(**UserProfileView**): Serves authenticated profile data for authorization checks. 
**urls.py**: Exposes /api/user/register/, /api/user/login/, /api/user/token/refresh/, and /api/user/profile/ endpoints. 

#### Frontend Component Breakdown
**Register.jsx**: Collects user registration fields (including role selection), posts to /register/, stores returned JWT tokens in localStorage, and routes the user based on their assigned role. 
**Login.jsx**: Handles credential submission to /login/, stores tokens on success, and routes the user to /farmer- dashboard or /buyer-dashboard. 
**ProtectedRoute.jsx**: Enforces access control on target routes by verifying tokens with /profile/, automatically requesting new access tokens via /token/refresh/ if needed, and enforcing matching role permissions before rendering protected dashboard components.
**FarmerDashboard.jsx & BuyerDashboard.jsx**: Secure landing pages for authenticated users post- login/registration.

---

### End-to-End Execution Workflows

#### 1. User Registration Flow

1. User submits details via Register.jsx.
2. Frontend sends payload to POST /api/user/register/.
3. RegisterSerializer validates password confirmation, converts role input to uppercase, and creates the CustomUser.
4. RegisterView returns user data and JWT tokens (access and refresh).
5. Register.jsx saves tokens to localStorage and routes the user based on role.

#### 2. Login Flow

1. User submits credentials via Login.jsx.
2. Frontend sends credentials to POST /api/user/login/.
3. LoginSerializer validates credentials and active status.
4. LoginView returns JWT tokens and user profile.
5. Login.jsx stores tokens in localStorage and navigates to the assigned dashboard.

#### 3. Protected Route Verification Flow

1. ProtectedRoute.jsx fetches the access token from localStorage.
2. If expired or missing, it attempts token refresh via POST /api/user/token/refresh/.
3. Requests profile details from GET /api/user/profile/ using the access token.
4. Compares the retrieved user role against the required route role: 
- **Authorized** Renders protected content. 
- **Unauthorized Role**: Redirects user to their appropriate dashboard. 
- **Unauthenticated**: Clears storage and redirects to /login.

---

### Automated Testing

Tests in `apps/user/tests.py` validate key system behavior: 
Successful creation of users with valid token issuance (test_registration_returns_user_and_tokens). 
User authentication and JWT retrieval (test_login_returns_tokens_for_registered_user). Authenticated profile access using Bearer tokens (test_access_token_authenticates_profile_request). 
Access token renewal through refresh tokens (test_refresh_token_returns_new_access_token).
