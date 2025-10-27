import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_email_settings():
    # Load .env file
    if not load_dotenv():
        print("❌ Error: Could not load .env file")
        return False
    
    # Get settings
    settings = {
        "SMTP_SERVER": os.getenv("SMTP_SERVER"),
        "SMTP_PORT": os.getenv("SMTP_PORT"),
        "EMAIL_USERNAME": os.getenv("EMAIL_USERNAME"),
        "EMAIL_PASSWORD": os.getenv("EMAIL_PASSWORD"),
        "ADMIN_EMAIL": os.getenv("ADMIN_EMAIL")
    }
    
    print("\n=== Current Email Settings ===")
    for key, value in settings.items():
        if key != "EMAIL_PASSWORD":
            print(f"{key}: {value}")
        else:
            print(f"{key}: {'SET' if value else 'NOT SET'} (length: {len(value) if value else 0})")
    
    try:
        print("\n=== Testing SMTP Connection ===")
        print(f"1. Connecting to {settings['SMTP_SERVER']}:{settings['SMTP_PORT']}...")
        server = smtplib.SMTP(settings['SMTP_SERVER'], int(settings['SMTP_PORT']))
        server.set_debuglevel(2)
        
        print("\n2. Starting TLS...")
        server.starttls()
        
        print("\n3. Attempting login...")
        server.login(settings['EMAIL_USERNAME'], settings['EMAIL_PASSWORD'])
        
        print("\n4. Creating test message...")
        msg = MIMEMultipart()
        msg['From'] = settings['EMAIL_USERNAME']
        msg['To'] = settings['ADMIN_EMAIL']
        msg['Subject'] = "Email Settings Test"
        msg.attach(MIMEText("This is a test email to verify SMTP settings.", 'plain'))
        
        print("\n5. Sending test message...")
        server.send_message(msg)
        
        print("\n6. Closing connection...")
        server.quit()
        
        print("\n✅ Success! All email settings are working correctly!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print("\n❌ Authentication Error!")
        print(f"Error details: {str(e)}")
        print("\nPossible solutions:")
        print("1. Verify EMAIL_USERNAME is correct")
        print("2. Check if EMAIL_PASSWORD is correct")
        print("3. For Gmail:")
        print("   - Ensure 2-Factor Authentication is enabled")
        print("   - Use an App Password, not your regular password")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    test_email_settings()