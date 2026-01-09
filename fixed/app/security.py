from fastapi import HTTPException, status

def require_role(user, role: str):
    if user.role != role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient privileges"
        )
