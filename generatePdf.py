import json
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# Sample JSON input as a string (you can load this from a file or API)
json_input = ''''''
with open("demo.json", "r") as f:
    json_input = f.read()

# Load the JSON data
data = json.loads(json_input)

# Function to generate resume PDF
def generate_resume(data, output_filename):
    # Create the PDF document with reduced top margin
    doc = SimpleDocTemplate(output_filename, pagesize=letter, topMargin=30, bottomMargin=10)
    styles = getSampleStyleSheet()
    
    # Create a centered style for email, phone, and address
    centered_style = ParagraphStyle(name="centered", alignment=1, fontSize=12)
    name_style = ParagraphStyle(name="name_style", alignment=1, fontSize=24, spaceAfter=18)

    story = []

    # Personal Information
    personal_info = data.get('personal_information', {})
    story.append(Paragraph(f"<b>{personal_info.get('name', 'N/A')}</b>", name_style))  # Centered Name
    story.append(Paragraph(f"<b>Email: </b>{personal_info.get('email', 'N/A')}", centered_style))  # Centered Email
    story.append(Paragraph(f"<b>Phone: </b>{personal_info.get('phone', 'N/A')}", centered_style))  # Centered Phone
    story.append(Paragraph(f"<b>Address: </b>{personal_info.get('address', 'N/A')}", centered_style))  # Centered Address
    story.append(Spacer(1, 3))  # Space after personal info

    # Education Section (Check if it exists)
    education_data = data.get('education')
    if education_data:
        story.append(Paragraph("<b>Education</b>", styles['Heading2']))
        for edu in education_data:
            story.append(Paragraph(f"<b>{edu.get('name', 'N/A')} </b>({edu.get('graduation_year', 'N/A')})", styles['Normal']))
            story.append(Paragraph(f"Course: {edu.get('couse', 'N/A')} | GPA: {edu.get('gpa', 'N/A')}", styles['Normal']))
            story.append(Spacer(1, 3))

    # Experience Section (Check if it exists)
    experience_data = data.get('experience')
    if experience_data:
        story.append(Paragraph("<b>Experience</b>", styles['Heading2']))
        for exp in experience_data:
            story.append(Paragraph(f"<b>{exp.get('title', 'N/A')} - {exp.get('organization', 'N/A')}</b> ({exp.get('date', 'N/A')})", styles['Normal']))
            story.append(Paragraph(exp.get('description', 'N/A'), styles['Normal']))
            story.append(Spacer(1, 3))

    # Projects Section (Check if it exists)
    projects_data = data.get('projects')
    if projects_data:
        story.append(Paragraph("<b>Projects</b>", styles['Heading2']))
        for project in projects_data:
            story.append(Paragraph(f"<b>{project.get('title', 'N/A')}</b>", styles['Normal']))
            story.append(Paragraph(f"{project.get('description', 'N/A')}", styles['Normal']))
            story.append(Spacer(1, 3))

    # Achievements Section (Check if it exists)
    achievements_data = data.get('achievements')
    if achievements_data:
        story.append(Paragraph("<b>Achievements</b>", styles['Heading2']))
        for achievement in achievements_data:
            story.append(Paragraph(f"<b>{achievement.get('title', 'N/A')}</b>", styles['Normal']))
            story.append(Paragraph(f"{achievement.get('description', 'N/A')}", styles['Normal']))
            story.append(Spacer(1, 3))

    # Skills Section (Check if it exists)
    skills_data = data.get('skills')
    if skills_data:
        story.append(Paragraph("<b>Skills</b>", styles['Heading2']))
        story.append(Paragraph(skills_data, styles['Normal']))
        story.append(Spacer(1, 3))

    # Certificates Section (Check if it exists)
    certificates_data = data.get('certificates')
    if certificates_data:
        story.append(Paragraph("<b>Certificates</b>", styles['Heading2']))
        for certificate in certificates_data:
            story.append(Paragraph(f"<b>{certificate.get('title', 'N/A')}</b> - {certificate.get('link', 'N/A')}", styles['Normal']))
            story.append(Spacer(1, 3))

    # Build the PDF
    doc.build(story)

# Call the function to generate the resume PDF
generate_resume(data, "testresume.pdf")
