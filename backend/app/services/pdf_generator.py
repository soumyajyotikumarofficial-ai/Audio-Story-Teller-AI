import os
import time
from fpdf import FPDF


def generate_story_pdf(story_text: str, language: str = 'en') -> str:
    pdf_dir = 'data/pdf'
    os.makedirs(pdf_dir, exist_ok=True)

    timestamp = int(time.time())
    filename = f'story_{language}_{timestamp}.pdf'
    file_path = os.path.join(pdf_dir, filename)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Generated Story', ln=True, align='C')
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)

    for line in story_text.split('\n'):
        text = line.strip()
        if not text:
            pdf.ln(6)
            continue
        pdf.multi_cell(0, 8, text)
        pdf.ln(2)

    pdf.output(file_path)
    return f'/pdf/{filename}'
