from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from vulnerable.app.database import get_db
from vulnerable.app.auth import get_current_user
from vulnerable.app import models

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users")
def list_users(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403)
    return db.query(models.User).all()


# APPROVAL BYPASS POSSIBILITY
@router.post("/approve/{doc_id}")
def approve_doc(
    doc_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(models.Document).get(doc_id)
    doc.is_approved = True
    db.commit()
    return {"approved": True}
