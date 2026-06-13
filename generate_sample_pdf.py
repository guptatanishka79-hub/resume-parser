"""
generate_sample_pdf.py
-----------------------
Utility script to generate a sample PDF resume for testing the parser.
Run once after installation:  python generate_sample_pdf.py

Requires: pip install reportlab
"""

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


def generate_pdf(output_path: str = "sample_resumes/john_doe_resume.pdf") -> None:
    """Generate a realistic sample PDF resume."""
    if not HAS_REPORTLAB:
        print("reportlab not installed. Run:  pip install reportlab")
        return

    doc    = SimpleDocTemplate(output_path, pagesize=A4,
                               topMargin=1.5*cm, bottomMargin=1.5*cm,
                               leftMargin=2*cm, rightMargin=2*cm)
    styles = getSampleStyleSheet()

    # Custom styles
    name_style = ParagraphStyle("Name", parent=styles["Title"],
                                fontSize=22, textColor=colors.HexColor("#1a1a2e"),
                                spaceAfter=4)
    contact_style = ParagraphStyle("Contact", parent=styles["Normal"],
                                   fontSize=9, textColor=colors.grey, spaceAfter=8)
    section_style = ParagraphStyle("Section", parent=styles["Heading2"],
                                   fontSize=11, textColor=colors.HexColor("#7c83fd"),
                                   spaceBefore=12, spaceAfter=4)
    body_style = ParagraphStyle("Body", parent=styles["Normal"],
                                fontSize=9.5, leading=14, spaceAfter=3)

    story = []

    # ── Header ──────────────────────────────────────────
    story.append(Paragraph("John Doe", name_style))
    story.append(Paragraph(
        "john.doe@email.com &nbsp;|&nbsp; +91-9876543210 &nbsp;|&nbsp; "
        "linkedin.com/in/johndoe &nbsp;|&nbsp; github.com/johndoe",
        contact_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#7c83fd")))

    # ── Summary ──────────────────────────────────────────
    story.append(Paragraph("Summary", section_style))
    story.append(Paragraph(
        "Motivated Computer Science graduate with hands-on experience in Python, "
        "Machine Learning, and Web Development. Passionate about building scalable "
        "data-driven solutions and open-source contribution.",
        body_style,
    ))

    # ── Education ──────────────────────────────────────────
    story.append(Paragraph("Education", section_style))
    story.append(Paragraph(
        "<b>Bachelor of Technology — Computer Science Engineering</b><br/>"
        "Delhi Technological University, New Delhi | 2020 – 2024 | CGPA: 8.6/10",
        body_style,
    ))

    # ── Skills ──────────────────────────────────────────
    story.append(Paragraph("Skills", section_style))
    skills_text = (
        "<b>Programming:</b> Python, Java, JavaScript, C++<br/>"
        "<b>Web:</b> React, Django, Flask, HTML, CSS, Node.js<br/>"
        "<b>Data & ML:</b> Machine Learning, Deep Learning, NLP, TensorFlow, "
        "PyTorch, Scikit-Learn, Pandas, NumPy<br/>"
        "<b>Databases:</b> MySQL, MongoDB, PostgreSQL, Redis<br/>"
        "<b>Tools:</b> Git, GitHub, Docker, AWS, Linux, Jupyter"
    )
    story.append(Paragraph(skills_text, body_style))

    # ── Experience ──────────────────────────────────────────
    story.append(Paragraph("Work Experience", section_style))
    story.append(Paragraph(
        "<b>Machine Learning Intern — TechStartup Pvt. Ltd.</b><br/>"
        "June 2023 – August 2023<br/>"
        "• Developed NLP pipeline to classify support tickets with 92% accuracy.<br/>"
        "• Reduced pipeline runtime by 40% through workflow automation.<br/>"
        "• Deployed model as REST API using FastAPI and Docker.",
        body_style,
    ))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "<b>Data Science Intern — Analytics Corp</b><br/>"
        "December 2022 – February 2023<br/>"
        "• Built EDA dashboards in Python using Pandas, Matplotlib, and Plotly.<br/>"
        "• Created recommendation engine for e-commerce using collaborative filtering.",
        body_style,
    ))

    # ── Certifications ──────────────────────────────────────────
    story.append(Paragraph("Certifications", section_style))
    for cert in [
        "Deep Learning Specialization — Coursera / DeepLearning.AI (2023)",
        "AWS Cloud Practitioner — Amazon Web Services (2023)",
        "Python for Data Science — IBM / Coursera (2022)",
    ]:
        story.append(Paragraph(f"• {cert}", body_style))

    doc.build(story)
    print(f"✅ Sample PDF created: {output_path}")


if __name__ == "__main__":
    generate_pdf()
