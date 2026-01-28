from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


def generate_notes_pdf(notes_text: str, output_path: str):
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["Normal"]

    story.append(Paragraph("AI Generated Study Notes", title_style))
    story.append(Spacer(1, 24))

    bullets = []

    for line in notes_text.split("\n"):
        line = line.strip()

        if not line:
            story.append(Spacer(1, 12))
            continue


        if line.startswith("##"):
            
            if bullets:
                story.append(ListFlowable(bullets))
                bullets = []

            heading = line.replace("##", "").strip()
            story.append(Paragraph(heading, heading_style))
            story.append(Spacer(1, 12))


        elif line.startswith("-"):
            bullet_text = line.replace("-", "").strip()
            bullets.append(ListItem(Paragraph(bullet_text, normal_style)))

        else:
  
            if bullets:
                story.append(ListFlowable(bullets))
                bullets = []

            story.append(Paragraph(line, normal_style))
            story.append(Spacer(1, 12))

    if bullets:
        story.append(ListFlowable(bullets))

    doc.build(story)