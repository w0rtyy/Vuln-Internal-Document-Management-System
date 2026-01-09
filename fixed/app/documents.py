from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app import models

router = APIRouter(prefix="/documents", tags=["documents"])

# Fixed IDOR 
@router.get("/{doc_id}")
def get_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Access is checked
    doc = db.query(models.Document).filter(
        models.Document.id == doc_id,
        models.Document.owner_id == current_user.id
    ).first()

    if not doc:
        raise HTTPException(status_code=404)

    return doc



# Fixed BULK IDOR
#
@router.get("/")
def list_documents(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Document).filter(
        models.Document.owner_id == current_user.id
    ).all()

# CREATE DOCUMENT (NO VALIDATION)
@router.post("/create")
def create_doc(
    filename: str,
    file_path: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    d = models.Document(
        owner_id=current_user.id,
        filename=filename,
        file_path=file_path
    )
    db.add(d)
    db.commit()
    return {"status": "created"}
