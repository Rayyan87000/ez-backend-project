# ez-backend-project
A FastAPI-based secure backend for file upload, listing, and download with token-based authentication

🔐 FastAPI Secure File Sharing Backend
A secure file-sharing backend built with FastAPI featuring:

User role-based access (ops and client)

Token-based authentication

Encrypted file download links

Email verification for clients

🚀 Features
✅ User Signup & Login
✅ Email Verification for Client Users
✅ JWT-style Token Authentication via Authorization header
✅ Upload .pptx, .docx, .xlsx (Only ops role)
✅ List Files (Authenticated clients)
✅ Encrypted File Download using base64 filename encoding

🛠️ Technologies Used
FastAPI – Web Framework

Uvicorn – ASGI Server

Passlib – Secure password hashing

Pydantic – Data validation

Python Dotenv – Manage environment variables

smtplib – Send email

Base64 – Filename encryption for secure links

🔧 How to Run
1. 📁 Clone the Repository
bash
Copy
Edit
git clone https://github.com/Rayyan87000/ez-backend-project.git
cd ez-backend-project
2. 🐍 Create Virtual Environment
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate  # For Windows
3. 📦 Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
4. 📄 Configure .env File
Create a .env file in the root directory with:

ini
Copy
Edit
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
SMTP_SENDER=your_email@gmail.com
🔐 Use Gmail App Password (not your actual password)

🔌 Start the Server
bash
Copy
Edit
uvicorn main:app --reload
Go to http://127.0.0.1:8000/docs for the Swagger UI.

📂 API Endpoints
Endpoint	Method	Role	Description
/signup	POST	client	Register user and send email verification
/verify?token=	GET	client	Verify email via token link
/login	POST	both	Get token after login
/upload	POST	ops only	Upload .pptx, .docx, .xlsx files
/files	GET	authenticated	List all uploaded files
/download/{encoded}	GET	authenticated	Download file from secure encoded URL

📥 Example Secure Download Link
After listing files, generate a link using:

python
Copy
Edit
import base64

def generate_download_link(filename):
    encoded = base64.urlsafe_b64encode(filename.encode()).decode().rstrip("=")
    return f"http://127.0.0.1:8000/download/{encoded}"
👮 Authorization in Swagger
Click "Authorize" in top right of Swagger.

Paste token:

nginx
Copy
Edit
Bearer your-token-here
💡 Notes
You cannot log in or access file actions without email verification.

Upload is restricted to .pptx, .docx, .xlsx only.

Client users cannot upload files.

