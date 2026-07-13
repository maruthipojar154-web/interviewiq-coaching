# ============================================================
# Mailer — sends emails via Gmail SMTP using smtplib
# ============================================================
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config


def send_mail(to, subject, html):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f'"{Config.MAIL_FROM_NAME}" <{Config.GMAIL_USER}>'
    msg["To"] = to
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(Config.GMAIL_USER, Config.GMAIL_APP_PASSWORD)
        server.sendmail(Config.GMAIL_USER, [to], msg.as_string())


def otp_email_template(name, code, purpose):
    heading = "Reset your password" if purpose == "reset" else "Verify your email"
    message = (
        "Use the code below to reset your InterviewIQ password."
        if purpose == "reset"
        else "Use the code below to verify your email and finish creating your InterviewIQ account."
    )
    return f"""
    <div style="font-family:Arial,sans-serif;max-width:480px;margin:0 auto;padding:24px;">
      <h2 style="color:#6366F1;">InterviewIQ</h2>
      <h3>{heading}</h3>
      <p>Hi {name or 'there'},</p>
      <p>{message}</p>
      <div style="font-size:32px;font-weight:bold;letter-spacing:6px;background:#13161F;color:#ffffff;
                  padding:16px;border-radius:10px;text-align:center;margin:20px 0;">
        {code}
      </div>
      <p>This code expires in {Config.OTP_EXPIRY_MINUTES} minutes.</p>
      <p style="color:#888;font-size:12px;">If you didn't request this, you can safely ignore this email.</p>
    </div>
    """
