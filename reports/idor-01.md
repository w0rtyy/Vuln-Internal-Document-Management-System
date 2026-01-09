# IDOR-01: Broken Object-Level Authorization in Document Retrieval

## Severity
High

## Description
The application fails to enforce object ownership checks when retrieving documents, allowing authenticated users to access documents owned by other users.

## Affected Endpoints
- GET /documents/{doc_id}
- GET /documents?owner_id={id}

## Root Cause
Authorization is not enforced at the data-access layer. Client-supplied identifiers are trusted without validating ownership against the authenticated user’s identity.

## Proof of Concept
1. Authenticate as a normal user
2. Request `/documents/3`
3. Observe document data belonging to another user

## Impact
- Unauthorized access to sensitive internal documents
- Cross-user data exposure
- Potential privacy and compliance violations

## Recommended Fix
Enforce ownership validation at the query level by scoping document access to the authenticated user’s identity rather than trusting client-supplied identifiers.
