from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.security import require_role
from app import models

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users")
def list_users(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403)
    return db.query(models.User).all()


# 🔥 APPROVAL BYPASS POSSIBILITY
@router.post("/approve/{doc_id}")
def approve_doc(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    require_role(current_user, "admin")

    doc = db.query(models.Document).filter(
        models.Document.id == doc_id
    ).first()

    if not doc:
        raise HTTPException(status_code=404)

    doc.is_approved = True
    db.commit()

    return {"status": "approved"}
