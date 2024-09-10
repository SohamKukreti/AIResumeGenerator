from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import requests

app = Flask(__name__)

load_dotenv()

azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")


@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    data = request.json
    
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    skills = data.get('skills')
    
    job_role = data.get('role')

    education = data.get('Education', [])
    education_details = ""
    for edu in education:
        edu_type = edu.get('type')
        edu_name = edu.get('name')
        edu_course = edu.get('course')
        graduation_year = edu.get('graduation_year')
        gpa = edu.get('GPA')
        education_details += f"\n- **{edu_type}**: {edu_name},Course : {edu_course}, Graduation Year: {graduation_year}, GPA: {gpa}\n"
    experience = data.get('experience', [])
    experience_details = ""
    for exp in experience:
        exp_title = exp.get('title')
        exp_company = exp.get('company')
        exp_duration = exp.get('duration')
        exp_description = exp.get('description')
        experience_details += f"\n- **{exp_title}** at **{exp_company}** ({exp_duration}): {exp_description}\n"
    
    coursework = data.get('coursework', [])
    coursework_details = ""
    for course in coursework:
        course_title = course.get('title')
        coursework_details += f"\n- **{course_title}**\n"

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

    with open('templates/latex_template_5.txt', 'r') as f:
        latex_template = f.read()

    project_coursework_prompt = ""
    experience_prompt = ""
    certificate_prompt = ""   

    if project_details:
        project_coursework_prompt = f"**Projects**: Detail key projects with their objectives, your role, technologies used, and the outcomes or impact. Use quantifiable metrics to demonstrate success: {project_details}\n\n"

    elif coursework_details:
        project_coursework_prompt = f"**Coursework**: Give a 1 line summary describing the relevant coursework that showcases your knowledge and skills in the field. Include the course name, topics covered, and any practical applications or projects completed. Mention any notable outcomes, presentations, or research work that demonstrates your expertise and commitment: {coursework_details}\n\n"
    
    if experience_details:
        experience_prompt = f"**Experience**: Describe past work experience, including job titles, company names, locations, dates of employment, and bullet points detailing responsibilities and achievements. Focus on using action verbs and quantifiable results to showcase impact: {experience_details}\n\n"

    if certificate_details:
        certificate_prompt = f"**Certificates**: List any certifications or courses completed that are relevant to the job role. Include the issuing organization and completion date: {certificate_details}\n"
    
    if skills:
        skills_prompt = "**Skills**: List key skills (both technical and soft skills) relevant to the job role. Use bullet points and include proficiency levels or years of experience where possible: {skills} add more skills you feel relevant based on the other information.3\n\n"
    else:
        skills_prompt = "write some soft and technical skills based on the rest of the data provided in the prompt\n\n"

    message_content =  f"""Use the following LaTeX template to create a professional, ATS-friendly resume with the given information. 
        Ensure the resume has a high chance of getting selected by recruiters by using industry-relevant keywords and quantifiable metrics where applicable. 
        Do not invent any details not provided in this prompt. Structure the resume with the following sections: Contact Information, Professional Summary, Education, Skills, Experience, Projects/Coursework, Achievements, and Certificates.\n\n
        Skip a section like projects, experience or achievements if the input for it has not been provided.\n
        Always use a \ before %\n
        The resume should be created to get the role of a {job_role}\n
        {latex_template}\n\n
        
        **Contact Information**:\n
        - Name: {name}\n
        - Email: {email}\n
        - Phone: {phone}\n
        - Address: {address}\n
        
        **Professional Summary**: Write a concise summary highlighting key strengths, expertise, and career goals relevant to the job role.\n\n"
        **Education**: Provide details on the educational background, including degrees, institutions, graduation dates, and any honors or relevant coursework: {education_details}\n\n
        {skills_prompt}
        {experience_prompt}
        {project_coursework_prompt}
        **Achievements**: Highlight significant professional achievements or recognitions. Include details such as awards, recognitions, publications, or contributions that set you apart, put certificates in this section only: {achievement_details}\n\n
        {certificate_prompt}    
        """

    print(message_content, end = "\n\n\n\n\n\n\n")

    system_prompt = "Your task is to generate a professional resume using only the provided information. Format the resume strictly according to the sections mentioned and do not add any extra text, commentary, or conversation outside of the resume structure. The output should be a well-structured resume, directly ready for use, without any prefatory or explanatory comments."

    headers = {
        "Content-Type": "application/json",
        "api-key": azure_openai_api_key,
    }

    response = requests.post(
        f"{azure_openai_endpoint}openai/deployments/{azure_openai_deployment_name}/chat/completions?api-version={azure_openai_api_version}",
        headers=headers,
        json={
            "messages": [{"role" : "system", "content" : system_prompt}, {"role": "user", "content": message_content,}],
            "max_tokens": 1000,
            "temperature": 0.7
        }
    )
    print(response.json())
    resume_content = response.json().get("choices")[0].get("message").get("content")
    with open('files/hello.tex', "w") as file:
        file.write(resume_content)

    print(resume_content)
    return jsonify({"resume": resume_content})

if __name__ == '__main__':
    app.run(debug=True)