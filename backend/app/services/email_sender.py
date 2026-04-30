import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import settings


def render_offer_html(candidate_name: str, role: str) -> str:
    return f"""
    <html><body>
    <p>Dear {candidate_name},</p>
    <p>We are thrilled to inform you that after a rigorous selection process, you have been selected for the position of <b>{role}</b> at GH Pvt Ltd.</p>
    <p>Your skills and experience stood out among many applicants. Please find attached your offer letter.</p>
    <p>Welcome to the team!</p>
    <p>Best regards,<br/>Ghania Tanveer & Muhammad Haseeb<br/>CEOs, GH Pvt Ltd</p>
    </body></html>
    """


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def send_offer_email(recipient: str, candidate_name: str, role: str, pdf_path: str) -> None:
    msg = MIMEMultipart()
    msg["From"] = settings.smtp_user or settings.smtp_from
    msg["To"] = recipient
    msg["Subject"] = f"Congratulations! You are appointed as {role} at GH Pvt Ltd"
    msg.attach(MIMEText(render_offer_html(candidate_name, role), "html"))

    with open(pdf_path, "rb") as f:
        attachment = MIMEApplication(f.read(), _subtype="pdf")
        attachment.add_header("Content-Disposition", "attachment", filename="offer_letter.pdf")
        msg.attach(attachment)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        if settings.smtp_user and settings.smtp_pass:
            server.login(settings.smtp_user, settings.smtp_pass)
        server.sendmail(msg["From"], [recipient], msg.as_string())
