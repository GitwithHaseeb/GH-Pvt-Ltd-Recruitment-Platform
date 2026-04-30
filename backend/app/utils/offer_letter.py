from datetime import date
from pathlib import Path

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

from app.config import settings


def generate_offer_letter(candidate_name: str, role: str) -> str:
    Path(settings.offer_letters_dir).mkdir(parents=True, exist_ok=True)
    file_name = f"offer_{candidate_name.replace(' ', '_')}_{role.replace(' ', '_')}.pdf"
    output_path = str(Path(settings.offer_letters_dir) / file_name)

    c = canvas.Canvas(output_path, pagesize=LETTER)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, 740, "GH Pvt Ltd - Offer Letter")
    c.setFont("Helvetica", 12)
    c.drawString(72, 710, f"Date: {date.today().isoformat()}")
    c.drawString(72, 680, f"Dear {candidate_name},")
    c.drawString(72, 650, f"We are pleased to offer you the position of {role}.")
    c.drawString(72, 620, "Welcome to GH Pvt Ltd. We are excited to work with you.")
    c.drawString(72, 560, "Sincerely,")
    c.drawString(72, 540, "Ghania Tanveer & Muhammad Haseeb")
    c.drawString(72, 520, "CEOs, GH Pvt Ltd")
    c.save()
    return output_path
