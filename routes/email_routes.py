from flask import redirect, url_for
from app import app, mail
from utils.email_utils import send_weekly_report

@app.route('/test-email')
def test_email():
    send_weekly_report(mail, app)
    return "✅ Письмо отправлено"