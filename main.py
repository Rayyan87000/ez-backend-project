from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Header, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from typing import List, Optional
from uuid import uuid4
import os
import base64
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# In-memory storage
users_db = {}
tokens_db = {}
verification_tokens = {}

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# File upload configuration
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {".pptx", ".docx", ".xlsx"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------------- Models ----------------------
class User(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: str  # "ops" or "client"

class VerifyRequest(BaseModel):
    token: str

# ---------------------- Helpers ----------------------
def send_verification_email(email: str, token: str):
    print("🚀 [EMAIL] Sending to:", email)
    print("🔗 [EMAIL] Verification link: http://127.0.0.1:8000/verify?token=" + token)

    msg = EmailMessage()
    msg["Subject"] = "Verify your email"
    msg["From"] = os.getenv("SMTP_SENDER")
    msg["To"] = email
    msg.set_content(f"Click to verify: http://127.0.0.1:8000/verify?token={token}")

    try:
        with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as smtp:
            smtp.starttls()
            smtp.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
            smtp.send_message(msg)
            print("✅ [EMAIL] Sent successfully!")
    except Exception as e:
        print("❌ [EMAIL ERROR]:", str(e))


def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token = authorization.replace("Bearer ", "")
    username = tokens_db.get(token)
    if not username or not users_db[username]["verified"]:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return username

def get_current_ops_user(authorization: Optional[str] = Header(None)):
    username = get_current_user(authorization)
    if users_db[username]["role"] != "ops":
        raise HTTPException(status_code=403, detail="Only Ops users can upload files")
    return username

def generate_download_link(filename: str) -> str:
    encoded = base64.urlsafe_b64encode(filename.encode()).decode().rstrip("=")
    return f"http://127.0.0.1:8000/download/{encoded}"

# ---------------------- Routes ----------------------
@app.post("/signup")
def signup(user: User, background_tasks: BackgroundTasks):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = pwd_context.hash(user.password)
    users_db[user.username] = {
        "password": hashed_password,
        "role": user.role,
        "email": user.email,
        "verified": False
    }
    verify_token = str(uuid4())
    verification_tokens[verify_token] = user.username
    background_tasks.add_task(send_verification_email, user.email, verify_token)
    return {"message": "Signup successful. Check your email for verification link."}

@app.get("/verify")
def verify_email(token: str):
    username = verification_tokens.pop(token, None)
    if not username or username not in users_db:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")
    users_db[username]["verified"] = True
    return {"message": "Email verified successfully!"}

@app.post("/login")
def login(user: User):
    stored_user = users_db.get(user.username)
    if not stored_user or not pwd_context.verify(user.password, stored_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not stored_user["verified"]:
        raise HTTPException(status_code=403, detail="Please verify your email before logging in")
    token = str(uuid4())
    tokens_db[token] = user.username
    return {"message": "Login successful", "token": token}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), username: str = Depends(get_current_ops_user)):
    filename = file.filename
    ext = os.path.splitext(filename)[1]
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only .pptx, .docx, .xlsx allowed")
    path = os.path.join(UPLOAD_FOLDER, filename)
    with open(path, "wb") as f:
        content = await file.read()
        f.write(content)
    return JSONResponse(content={"message": "File uploaded successfully", "filename": filename})

@app.get("/files")
def list_files(username: str = Depends(get_current_user)) -> List[str]:
    try:
        files = os.listdir(UPLOAD_FOLDER)
        return JSONResponse(content={"user": username, "files": files})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{encoded_filename}")
def download_file(encoded_filename: str, username: str = Depends(get_current_user)):
    try:
        filename = base64.urlsafe_b64decode(encoded_filename + "==").decode()
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(path=file_path, filename=filename, media_type="application/octet-stream")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or corrupted download link")

# ------------------- Swagger UI Auth -------------------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Secure File Upload API",
        version="1.1.0",
        description="Secure FastAPI file upload with email verification and token auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "UUID"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
