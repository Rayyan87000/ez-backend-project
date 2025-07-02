import smtplib
from email.message import EmailMessage

# Email details
EMAIL_SENDER = "rayyankaif8092@gmail.com"
EMAIL_PASSWORD = "bzhp meon vcan gupx"  # Gmail App Password
EMAIL_RECEIVER = "rayyankaif8092@gmail.com"

msg = EmailMessage()
msg["Subject"] = "✅ Test Email from FastAPI Project"
msg["From"] = EMAIL_SENDER
msg["To"] = EMAIL_RECEIVER
msg.set_content("This is a test email sent directly from Python to test SMTP config.")

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("✅ Test email sent successfully!")
except Exception as e:
    print("❌ Error sending email:", str(e))
