# BAC-01: Broken Access Control in Administrative Functions

## Severity
High

## Description
The application exposes administrative functionality without enforcing role-based authorization checks at the backend. While administrative actions are hidden in the user interface, backend routes remain accessible to any authenticated user.

## Affected Endpoints
- GET /admin-ui
- POST /approve/{doc_id}

## Root Cause
Role-based authorization is enforced inconsistently. The application relies on UI navigation restrictions rather than backend authorization checks, resulting in implicit trust of user intent.

## Proof of Concept
1. Authenticate as a normal user
2. Manually access `/admin-ui` via the browser
3. Submit a document approval request
4. Observe unauthorized document state changes in the database

## Impact
- Privilege escalation
- Unauthorized administrative actions
- Integrity violations of business workflows

## Recommended Fix
Enforce role-based authorization checks at the backend for all administrative routes. Authorization decisions must be independent of UI navigation controls.
