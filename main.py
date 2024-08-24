from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

app = Flask(__name__)

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    data = request.json
    
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    skills = data.get('skills')
    
    education = data.get('Education', [])
    education_details = ""
    for edu in education:
        edu_type = edu.get('type')
        edu_name = edu.get('name')
        graduation_year = edu.get('graduation_year')
        gpa = edu.get('GPA')
        education_details += f"\n- **{edu_type}**: {edu_name}, Graduation Year: {graduation_year}, GPA: {gpa}\n"

    experience = data.get('experience', [])
    experience_details = ""
    for exp in experience:
        exp_title = exp.get('title')
        exp_company = exp.get('company')
        exp_duration = exp.get('duration')
        exp_description = exp.get('description')
        experience_details += f"\n- **{exp_title}** at **{exp_company}** ({exp_duration}): {exp_description}\n"
    
    projects = data.get('projects', [])
    project_details = ""
    for project in projects:
        proj_title = project.get('title')
        proj_description = project.get('description')
        project_details += f"\n- **{proj_title}**: {proj_description}\n"
    
    achievements = data.get('Achievements', [])
    achievement_details = ""
    for achievement in achievements:
        ach_title = achievement.get('title')
        ach_description = achievement.get('description')
        achievement_details += f"\n- **{ach_title}**: {ach_description}\n"

    certificates = data.get('certificates', [])
    certificate_details = ""
    for certificate in certificates:
        cert_title = certificate.get('title')
        cert_link = certificate.get('link')
        certificate_details += f"\n- **{cert_title}**: {cert_link}\n"

    message_content = (
        f"Create a professional, ATS-friendly resume with the following information. "
        f"Ensure the resume has a high chance of getting selected by recruiters by using industry-relevant keywords and quantifiable metrics where applicable. "
        f"Do not invent any details not provided in this prompt. Structure the resume with the following sections: Contact Information, Professional Summary, Skills, Education, Experience, Projects, Achievements, and Certificates.\n\n"
        f"**Contact Information**:\n"
        f"- Name: {name}\n"
        f"- Email: {email}\n"
        f"- Phone: {phone}\n"
        f"- Address: {address}\n\n"
        f"**Professional Summary**: Write a concise summary highlighting key strengths, expertise, and career goals relevant to the job role.\n\n"
        f"**Skills**: List key skills (both technical and soft skills) relevant to the job role. Use bullet points and include proficiency levels or years of experience where possible: {skills}\n\n"
        f"**Education**: Provide details on the educational background, including degrees, institutions, graduation dates, and any honors or relevant coursework: {education_details}\n\n"
        f"**Experience**: Describe past work experience, including job titles, company names, locations, dates of employment, and bullet points detailing responsibilities and achievements. Focus on using action verbs and quantifiable results to showcase impact: {experience_details}\n\n"
        f"**Projects**: Detail key projects with their objectives, your role, technologies used, and the outcomes or impact. Use quantifiable metrics to demonstrate success: {project_details}\n\n"
        f"**Achievements**: Highlight significant professional achievements or recognitions. Include details such as awards, recognitions, publications, or contributions that set you apart: {achievement_details}\n\n"
        f"**Certificates**: List any certifications or courses completed that are relevant to the job role. Include the issuing organization and completion date: {certificate_details}\n"
    )


    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": message_content}],
    )

    resume_content = response.choices[0].message.content

    return jsonify({"resume": resume_content})

if __name__ == '__main__':
    app.run(debug=True)