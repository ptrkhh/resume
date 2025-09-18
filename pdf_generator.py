import io
import qrcode
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image


def generate_resume_pdf(patrick_data):
    start_time = datetime.now()
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, spaceAfter=12,
                                 alignment=TA_CENTER)
    subtitle_style = ParagraphStyle('CustomSubtitle', parent=styles['Heading2'], fontSize=14, spaceAfter=6,
                                    alignment=TA_CENTER)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=16, spaceAfter=12,
                                   textColor=colors.darkblue)

    story = []

    # Header
    story.append(Paragraph(patrick_data['name'], title_style))
    story.append(Paragraph(patrick_data['title'], subtitle_style))

    # Contact Info
    contact_info = f"{patrick_data['personal_data']['email']} | {patrick_data['personal_data']['phone_number']} | {patrick_data['personal_data']['current_location']}"
    story.append(Paragraph(contact_info, styles['Normal']))
    story.append(Spacer(1, 12))

    # Summary
    story.append(Paragraph("Professional Summary", heading_style))
    story.append(Paragraph(patrick_data['summary'], styles['Normal']))
    story.append(Spacer(1, 12))

    # Experience
    story.append(Paragraph("Professional Experience", heading_style))
    for exp in patrick_data['experience'][:3]:
        story.append(Paragraph(f"<b>{exp['position']}</b> - {exp['company']}, {exp['location']}", styles['Normal']))
        story.append(Paragraph(f"{exp['year_from']} - {exp['year_to']}", styles['Italic']))
        story.append(Paragraph(exp['description'], styles['Normal']))
        if exp['description_details']:
            for detail in exp['description_details']:
                story.append(Paragraph(f"• {detail}", styles['Normal']))
        story.append(Spacer(1, 6))

    # Education
    story.append(Paragraph("Education", heading_style))
    for edu in patrick_data['education'][:3]:
        story.append(Paragraph(f"<b>{edu['degree']}</b> - {edu['institute']}, {edu['location']}", styles['Normal']))
        story.append(Paragraph(f"{edu['year_from']} - {edu['year_to']}", styles['Italic']))
        story.append(Paragraph(edu['description'], styles['Normal']))
        story.append(Spacer(1, 6))

    # Skills
    story.append(Paragraph("Technical Skills", heading_style))
    for skill_cat in patrick_data['skill']:
        skills_text = f"<b>{skill_cat['title']}:</b> {', '.join(skill_cat['list'])}"
        story.append(Paragraph(skills_text, styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    print(f"PDF generation takes {datetime.now() - start_time} seconds")
    return buffer


def generate_contact_card_pdf(patrick_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=(4 * inch, 2.5 * inch), rightMargin=0.2 * inch, leftMargin=0.2 * inch,
                            topMargin=0.15 * inch, bottomMargin=0.15 * inch)

    # Modern color palette
    primary_color = colors.Color(0.2, 0.3, 0.5)  # Professional blue
    accent_color = colors.Color(0.4, 0.6, 0.8)  # Light blue
    text_color = colors.Color(0.2, 0.2, 0.2)  # Dark gray

    styles = getSampleStyleSheet()

    # Modern typography styles
    name_style = ParagraphStyle(
        'Name',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        textColor=primary_color,
        fontName='Helvetica-Bold',
        spaceAfter=4
    )

    title_style = ParagraphStyle(
        'Title',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_CENTER,
        textColor=accent_color,
        fontName='Helvetica',
        spaceAfter=6
    )

    story = []

    # Header section
    story.append(Paragraph(patrick_data['name'].upper(), name_style))
    story.append(Paragraph(patrick_data['title'], title_style))

    # Generate QR code for Streamlit app
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data("https://resumepatrick.streamlit.app")
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_buffer = io.BytesIO()
    qr_image.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)
    qr_img = Image(qr_buffer, width=0.89 * inch, height=0.89 * inch)

    # Contact information in clean format
    contact_data = [
        ["Email", patrick_data['personal_data']['email']],
        ["Phone", patrick_data['personal_data']['phone_number']],
        ["Location", patrick_data['personal_data']['current_location']],
        ["LinkedIn", patrick_data['contact']['LinkedIn']['link'].replace("https://www.", "")],
        ["Instagram", patrick_data['contact']['Instagram']['link'].replace("https://www.", "")],
        ["GitHub", patrick_data['contact']['GitHub']['link'].replace("https://www.", "")],
    ]

    contact_table = Table(contact_data, colWidths=[0.65 * inch, 1.95 * inch])
    contact_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Times-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (0, -1), primary_color),
        ('TEXTCOLOR', (1, 0), (1, -1), text_color),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))

    # Layout with contact info and QR code side by side
    main_table = Table([[contact_table, qr_img]], colWidths=[2.5 * inch, 0.9 * inch])
    main_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))

    story.append(main_table)

    doc.build(story)
    buffer.seek(0)
    return buffer


if __name__ == "__main__":
    import yaml
    pdf_buffer = generate_contact_card_pdf(yaml.safe_load(open("patrick.yaml")))

    with open("test.pdf", "wb") as f:
        f.write(pdf_buffer.getvalue())

