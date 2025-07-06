# ⚙️ Project Setup Guide — Secure File Sharing API

Follow these simple steps to run this project on any device.

---

## ✅ 1. Clone the Repository


git clone https://github.com/Rayyan87000/ez-backend-project.git
cd ez-backend-project

 2. Set Up Virtual Environment
 ## ✅ 2. Set Up Virtual Environment

### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```



 3. Install Dependencies
 pip install -r requirements.txt

Or manually:
pip install fastapi uvicorn python-multipart passlib[bcrypt] python-dotenv

4. Create .env File (Optional for Email)
Create a .env file in the root directory with the following content:
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
SMTP_SENDER=your_email@gmail.com

If you don’t provide SMTP credentials, the app will simulate email by printing links in the terminal.

✅ 5. Create Uploads Folder
If not already present:
mkdir uploads

6. Run the Server
uvicorn main:app --reload

Then open your browser:
http://127.0.0.1:8000/docs
Use the Swagger UI to test the APIs.

Common Issues
ModuleNotFoundError: Make sure you're inside the virtual environment.

uploads not found: Create the uploads/ folder manually.

Email not sending: Either skip .env or configure SMTP properly.

---

### ✅ Now save and push it:
```bash
git add SETUP.md
git commit -m "Fixed formatting in SETUP.md"
git push origin main
