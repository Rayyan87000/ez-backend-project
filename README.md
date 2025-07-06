# ez-backend-project
A FastAPI-based secure backend for file upload, listing, and download with token-based authentication

🔐 FastAPI Secure File Upload Backend
A secure backend system built using FastAPI that allows file uploading, listing, and encrypted downloading with token-based authentication and role-based access control.



🚀 Features
🧾 User Signup & Login with hashed passwords

🔐 Token-based Auth using Authorization headers

🛡️ Role-based Access: Only ops users can upload

📁 Upload files (.pptx, .docx, .xlsx) securely

📄 List uploaded files (authenticated users only)

📥 Encrypted File Download using Base64 URL encoding

💻 Interactive Swagger UI with authorization support

⚙️ Technologies Used
FastAPI

Pydantic

Passlib (bcrypt)

Uvicorn

Python 3.13+

📂 API Endpoints
Endpoint	Method	Description	Auth Required	Role
/signup	POST	Register a new user	❌ No	—
/login	POST	Get token by logging in	❌ No	—
/upload	POST	Upload file (.pptx, .docx, .xlsx)	✅ Yes	ops
/files	GET	List uploaded files	✅ Yes	all
/download/{encoded}	GET	Download file using Base64 encoded name	✅ Yes	all

🧪 Swagger UI + Token Auth
Open: http://127.0.0.1:8000/docs

Click the Authorize button (top-right)

Enter your token:

php-template
Copy
Edit
Bearer <your-token>
🛠️ How to Run This Project on Any Device
✅ 1. Clone the Repo
bash
Copy
Edit
git clone https://github.com/Rayyan87000/ez-backend-project.git
cd ez-backend-project
✅ 2. Create and Activate Virtual Environment (Windows)
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate
Or on macOS/Linux:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
✅ 3. Install Requirements
If you have a requirements.txt file, run:

bash
Copy
Edit
pip install -r requirements.txt
If not, install manually:

bash
Copy
Edit
pip install fastapi uvicorn python-multipart passlib[bcrypt]
✅ 4. Run the Server
bash
Copy
Edit
uvicorn main:app --reload
Visit http://127.0.0.1:8000/docs

🔁 Sample Workflow
✅ Signup
json
Copy
Edit
POST /signup
{
  "username": "rayyan123",
  "password": "mypassword",
  "role": "ops"
}
✅ Login
json
Copy
Edit
POST /login
{
  "username": "rayyan123",
  "password": "mypassword",
  "role": "ops"
}
Response:

json
Copy
Edit
{
  "message": "Login successful",
  "token": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
Use this token in the Authorize section or as a header:

makefile
Copy
Edit
Authorization: Bearer <token>
✅ Download Link Generator (Python)
Use this snippet to generate encrypted download links:

python
Copy
Edit
import base64
def generate_download_link(filename):
    encoded = base64.urlsafe_b64encode(filename.encode()).decode().rstrip("=")
    return f"http://127.0.0.1:8000/download/{encoded}"
📦 Folder Structure
bash
Copy
Edit
ez-backend-project/
│
├── main.py                # FastAPI app
├── uploads/               # Folder for storing uploaded files
├── venv/                  # Virtual environment (ignored in GitHub)
└── README.md              # This file


## 🔁 API Testing with Postman

This project includes a ready-to-use Postman collection for testing all endpoints.

### 📦 Import Instructions

1. Open Postman
2. Click `Import` (top left)
3. Choose `SecureFileSharing.postman_collection.json` from the project folder
4. Use the requests under the collection to test:
   - `Sign Up`
   - `Verify Email`
   - `Login`
   - `Upload File`
   - `List All Uploaded Files`
   - `Download File`

### 🔐 Auth Token

Make sure to copy the token returned from `/login` and add it in the `Authorization` header as:
