# Visa Application Form

A Flask web application for handling visa applications with email notifications.

## Environment Setup

1. Create the Python virtual environment:
   ```powershell
   & "python" -m venv .venv
   ```

2. Activate the virtual environment:
   - PowerShell:
     ```powershell
     & ".\.venv\Scripts\Activate.ps1"
     ```
   - CMD:
     ```cmd
     .\.venv\Scripts\activate.bat
     ```

3. Install dependencies:
   ```powershell
   & ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
   & ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Edit `.env` and fill in your values:
     ```ini
     FLASK_SECRET=your-secret-key-here
     SMTP_SERVER=smtp.gmail.com
     SMTP_PORT=587
     EMAIL_USERNAME=your-email@gmail.com
     EMAIL_PASSWORD=your-app-password  # Use App Password for Gmail
     ADMIN_EMAIL=your-email@gmail.com
     ```

5. Run the application:
   ```powershell
   & ".\.venv\Scripts\python.exe" app.py
   ```
   The app will start at http://127.0.0.1:5000

## Security Notes

- Never commit `.env` to version control
- For Gmail, use an App Password instead of your account password
- In production, use a proper secret key for FLASK_SECRET
