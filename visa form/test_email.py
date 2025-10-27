import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

# Email settings from .env
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

def test_email_connection():
    """Test SMTP connection and send a test email"""
    try:
        print("\nStarting email test...")
        print(f"SMTP Server: {SMTP_SERVER}:{SMTP_PORT}")
        print(f"From: {EMAIL_USERNAME}")
        print(f"To: {ADMIN_EMAIL}")
        
        # Create test message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USERNAME
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = "Test Email - Visa Form Application"
        
        body = """
        This is a test email from your Visa Form Application.
        If you receive this, email sending is working correctly!
        
        Best regards,
        Your Application System
        """
        msg.attach(MIMEText(body, 'plain'))
        
        print("\nConnecting to SMTP server...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.set_debuglevel(1)  # Show detailed SMTP interaction
        
        print("Starting TLS encryption...")
        server.starttls()
        
        print("Attempting login...")
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        
        print("Sending test message...")
        server.send_message(msg)
        
        print("Closing connection...")
        server.quit()
        
        print("\n✅ Success! Test email sent. Check your inbox.")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print("\n❌ Authentication failed!")
        print(f"Error details: {str(e)}")
        print("\nPossible solutions:")
        print("1. Check if the EMAIL_PASSWORD in .env is correct")
        print("2. For Gmail accounts:")
        print("   - Enable 2-Factor Authentication")
        print("   - Generate an App Password: Google Account → Security → App passwords")
        print("   - Use the 16-character App Password instead of your regular password")
        return False
        
    except Exception as e:
        print(f"\n❌ Error sending email: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    test_email_connection()