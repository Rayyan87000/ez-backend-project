# ez-backend-project
A FastAPI-based secure backend for file upload, listing, and download with token-based authentication

# 🔐 FastAPI Secure File Upload Backend

This is a secure file upload and download backend built with **FastAPI**. It includes token-based authentication, user roles (`ops` and `client`), and file encryption features.

## 🚀 Features

- 🧾 **User Signup & Login** with hashed passwords
- 🔐 **JWT-style Token Auth** using Authorization headers
- 🛡️ **Role-based Access**: Only `ops` users can upload files
- 📁 **Secure File Upload** (`.pptx`, `.docx`, `.xlsx`)
- 📄 **List Uploaded Files** (authenticated users)
- 📥 **Encrypted File Download** using Base64 URLs

## 🔧 Technologies Used

- FastAPI
- Pydantic
- Passlib (bcrypt)
- Uvicorn
- Python 3.13+

## 📂 API Endpoints

### `/signup` `POST`
Register a new user. Provide `username`, `password`, and `role`.

### `/login` `POST`
Login to receive a `token`. Use this token in the header:  
`Authorization: Bearer <your-token>`

### `/upload` `POST` (Protected)
Upload `.pptx`, `.docx`, or `.xlsx` files.  
🔒 Only accessible by `ops` users.

### `/files` `GET` (Protected)
Returns list of uploaded files. Accessible by all authenticated users.

### `/download/{encoded_filename}` `GET` (Protected)
Download a file securely using an encoded filename (Base64).

## 🔐 Swagger UI with Token Auth

- Visit `http://127.0.0.1:8000/docs`
- Click **Authorize** (top right)
- Paste token in the format: `Bearer <your-token>`

## 🛠️ How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Rayyan87000/ez-backend-project.git
   cd ez-backend-project

