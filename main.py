from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Header
from fastapi.responses import JSONResponse, FileResponse
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from passlib.context import CryptContext
from typing import List, Optional
import uuid
import os
import base64

app = FastAPI()

# In-memory user/token store
users_db = {}
tokens_db = {}

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Upload settings
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {".pptx", ".docx", ".xlsx"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ----------------------- Models -----------------------
class User(BaseModel):
    username: str
    password: str
    role: str  # ops or client

# ------------------- Dependencies ---------------------
def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token = authorization.replace("Bearer ", "")
    username = tokens_db.get(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return username

def get_current_ops_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token = authorization.replace("Bearer ", "")
    username = tokens_db.get(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = users_db.get(username)
    if user["role"] != "ops":
        raise HTTPException(status_code=403, detail="Only Ops users can upload files")
    return username

# --------------------- Routes -------------------------
@app.post("/signup")
def signup(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = pwd_context.hash(user.password)
    users_db[user.username] = {"password": hashed_password, "role": user.role}
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: User):
    stored_user = users_db.get(user.username)
    if not stored_user or not pwd_context.verify(user.password, stored_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = str(uuid.uuid4())
    tokens_db[token] = user.username
    return {"message": "Login successful", "token": token}

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    username: str = Depends(get_current_ops_user)
):
    filename = file.filename
    ext = os.path.splitext(filename)[1]
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only .pptx, .docx, .xlsx allowed.")
    path = os.path.join(UPLOAD_FOLDER, filename)
    with open(path, "wb") as f:
        content = await file.read()
        f.write(content)
    return JSONResponse(content={"message": "File uploaded successfully!", "filename": filename})

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
        return FileResponse(path=file_path, filename=filename, media_type='application/octet-stream')
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or corrupted download link")

# ----------------- Helper Function --------------------
def generate_download_link(filename: str):
    encoded = base64.urlsafe_b64encode(filename.encode()).decode().rstrip("=")
    return f"http://127.0.0.1:8000/download/{encoded}"

# ---------------- Swagger Auth Setup ------------------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Secure File Upload API",
        version="1.0.0",
        description="FastAPI backend with token auth and encrypted file links.",
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
