from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


def generate_notes_pdf(notes_text: str, output_path: str):
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    for line in notes_text.split("\n"):
        if line.strip() == "":
            story.append(Spacer(1, 12))
        else:
            story.append(Paragraph(line, styles["Normal"]))

    doc.build(story)