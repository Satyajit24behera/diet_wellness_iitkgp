from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Frame, PageTemplate
from reportlab.lib.units import inch
import os
import re
from reportlab.platypus import Flowable
from reportlab.lib import colors

class HorizontalLine(Flowable):
    def __init__(self, width=450, thickness=1):
        Flowable.__init__(self)
        self.width = width
        self.thickness = thickness

    def draw(self):
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)

# --------- TEXT CLEANER ---------
def clean_text(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove bold markers
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Remove italic markers
    return text.strip()

# --------- PARSE LLM OUTPUT ---------
def parse_recommendations(llm_output: str) -> dict:
    sections = {
        "Note": "",
        "Health Conditions": "",
        "Food Plan": "",
        "Exercise Plan": "",
        "Supplement Plan": ""
    }

    current_key = None
    for line in llm_output.splitlines():
        line = line.strip()
        if not line:
            continue
        for key in sections:
            if line.lower().startswith(key.lower()):
                current_key = key
                line = line[len(key):].lstrip(":").strip()
                if line:
                    sections[current_key] += line + "\n"
                break
        else:
            if current_key:
                sections[current_key] += line + "\n"
    return sections

# --------- FOOTER DRAW FUNCTION ---------


def draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica-Oblique", 8)
    canvas.setFillGray(0.3)
    
    width, height = A4

    line1 = "Developed by Satyajit Behera, a fourth-year undergraduate student from IIT Kharagpur."
    line2 = "Disclaimer: This is a recommendation system. Kindly verify with a doctor/dietitian before applying."

    canvas.drawCentredString(width / 2, 40, line1)
    canvas.drawCentredString(width / 2, 28, line2)
    
    
    canvas.setStrokeColor(colors.black)
    canvas.setLineWidth(1)
    margin = 20
    canvas.rect(margin, margin, width - 2 * margin, height - 2 * margin)

    canvas.restoreState()
    

# --------- PDF GENERATOR USING REPORTLAB ---------
def generate_pdf(content, output_path="wellness_guide.pdf"):
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            rightMargin=30, leftMargin=30,
                            topMargin=30, bottomMargin=50)

    width, height = A4
    frame = Frame(doc.leftMargin, doc.bottomMargin + 30, doc.width, doc.height - 50, id='normal')
    template = PageTemplate(id='with_footer', frames=[frame], onPage=draw_footer)
    doc.addPageTemplates([template])

    Story = []

    # Custom Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=18, alignment=TA_CENTER, spaceAfter=12))
    styles.add(ParagraphStyle(name='HeadingStyle', fontName='Helvetica-Bold', fontSize=14, alignment=TA_CENTER, spaceBefore=20, spaceAfter=8))
    styles.add(ParagraphStyle(name='NormalStyle', fontName='Helvetica', fontSize=11, leading=16))
    styles.add(ParagraphStyle(name='BulletStyle', fontName='Helvetica', fontSize=11, leading=16, leftIndent=14, bulletIndent=8))

    # Header Image Full Width
    header_img = "assets/iitkgp_header.png"
    if os.path.exists(header_img):
        header = Image(header_img, width=width - 60, height=1 * inch)
        Story.append(header)

    # Title
    Story.append(Paragraph("Personalized Wellness Guide", styles['TitleStyle']))
    Story.append(Spacer(1, 12))

    # Basic Info
    name = content.get("Name", "User")
    goal = content.get("Goal", "Wellness")
    age = content.get("Age", "N/A")

    Story.append(Paragraph(f"<i><b>Name:</b></i> {name}", styles['NormalStyle']))
    Story.append(Paragraph(f"<i><b>Age:</b></i> {age}", styles['NormalStyle']))
    Story.append(Paragraph(f"<i><b>Goal:</b></i> {goal}", styles['NormalStyle']))
    Story.append(Spacer(1, 10))

    # Optional Sections
    if content.get("Note"):
        Story.append(Spacer(1, 12))
        Story.append(HorizontalLine(width=doc.width))  # Add line before the heading
        Story.append(Spacer(1, 8))
        Story.append(Paragraph("Important Note", styles['HeadingStyle']))
        for line in content["Note"].splitlines():
            Story.append(Paragraph(clean_text(line), styles['NormalStyle']))

    if content.get("Health Conditions"):
        Story.append(Paragraph("Confirmed Health Conditions & Next Steps", styles['HeadingStyle']))
        for line in content["Health Conditions"].splitlines():
            Story.append(Paragraph(f"• {clean_text(line)}", styles['BulletStyle']))

    for section in ["Food Plan", "Exercise Plan", "Supplement Plan"]:
        if content.get(section):
            Story.append(Paragraph(section, styles['HeadingStyle']))
            for line in content[section].splitlines():
                Story.append(Paragraph(f"• {clean_text(line)}", styles['BulletStyle']))

    doc.build(Story)
    return output_path
