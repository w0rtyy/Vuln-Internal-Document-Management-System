# Vulnerable Internal Document Management System

## Overview

This directory contains an intentionally vulnerable internal document management system designed to demonstrate common real-world web application security failures related to authorization and access control.

The application is built to appear secure at the user interface level, while retaining exploitable backend flaws. This reflects how many production systems fail due to misplaced trust in UI controls and inconsistent backend authorization enforcement.

---

## Security Scope

This application demonstrates the following classes of vulnerabilities:

- Insecure Direct Object References (IDOR)
- Broken Access Control
- Authorization Logic Flaws
- Information Disclosure (Reconnaissance)

Detailed analysis of each issue is documented in the `/reports` directory.

---

## Vulnerability Overview

### 1. Insecure Direct Object Reference (IDOR)

**Context**
- The UI restricts users to viewing only their own documents.

**Backend Flaw**
- Document ownership is not enforced at the data-access layer.
- Client-supplied identifiers are trusted without validation.

**Impact**
- Authenticated users can access documents owned by other users by manipulating object identifiers.

---

### 2. Broken Access Control – Administrative Functions

**Context**
- Administrative navigation is hidden from non-admin users in the UI.

**Backend Flaw**
- Backend routes do not consistently enforce role-based authorization.
- Administrative endpoints remain accessible via direct URL access.

**Impact**
- Privilege escalation
- Unauthorized document approval

---

### 3. Authorization Logic Flaws

**Context**
- UI logic restricts visible actions based on user role.

**Backend Flaw**
- Authorization checks are inconsistently applied across routes.
- Business-critical actions rely on UI gating rather than backend enforcement.

**Impact**
- Unauthorized state changes
- Abuse of application workflows

---

### 4. Information Disclosure (Reconnaissance)

**Backend Flaw**
- Internal file paths and metadata are exposed in responses and UI views.

**Impact**
- Disclosure of internal filesystem structure
- Easier enumeration and attack chaining

---

## Running the Application

### Database Setup

1. Create a PostgreSQL database.
2. Create users using application endpoints to ensure passwords are hashed.
3. Assign roles manually as needed, for example:

```sql
UPDATE users SET role = 'admin' WHERE email = 'admin@mail.com';
```

## Install dependencies

## Run `uvicorn app.main:app --reload`

## User Roles
- user
- manager
- admin
