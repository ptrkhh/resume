import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


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
