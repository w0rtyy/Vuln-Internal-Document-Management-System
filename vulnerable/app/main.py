from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Request, Form, Cookie


from vulnerable.app.database import engine, Base, get_db
from vulnerable.app import auth, documents, admin, models
from sqlalchemy.orm import Session
from fastapi import Depends

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vulnerable Internal DMS")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(admin.router)

@app.get("/")
def home():
    return RedirectResponse("/login-ui")


@app.get("/login-ui")
def login_ui(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login-ui")
def login_ui_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    from vulnerable.app.auth import verify_password
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid credentials"}
        )

    response = RedirectResponse("/dashboard", status_code=302)
    from vulnerable.app.auth import create_session_id
    sid = create_session_id()

    session = models.Session(
        session_id=sid,
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=2)
    )
    db.add(session)
    db.commit()

    response.set_cookie("session_id", sid, httponly=True)
    return response

@app.get("/dashboard")
def dashboard(
    request: Request,
    current_user=Depends(auth.get_current_user)
):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": current_user}
    )

@app.get("/documents-ui")
def documents_ui(
    request: Request,
    owner_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    if owner_id:
        docs = db.query(models.Document).filter(models.Document.owner_id == owner_id).all()
    else:
        docs = db.query(models.Document).filter(models.Document.owner_id == current_user.id).all()

    return templates.TemplateResponse(
        "documents.html",
        {"request": request, "documents": docs, "user": current_user}
    )


@app.get("/documents-ui/{doc_id}")
def document_detail(
    request: Request,
    doc_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    docs = db.query(models.Document).get(doc_id)
    return templates.TemplateResponse(
        "documents.html",
        {"request": request, "documents": docs, "user": current_user}
    )

@app.get("/admin-ui")
def admin_ui(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    users = db.query(models.User).all()
    documents = db.query(models.Document).all()

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "users": users,
            "documents": documents,
            "user": current_user
        }
    )

@app.get("/logout")
def logout(
    request: Request,
    db: Session = Depends(get_db),
    session_id: str | None = Cookie(default=None)
):
    if session_id:
        db.query(models.Session).filter(
            models.Session.session_id == session_id
        ).delete()
        db.commit()

    response = RedirectResponse("/login-ui", status_code=302)
    response.delete_cookie("session_id")
    return response
