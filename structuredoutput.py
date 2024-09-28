from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional
import os
from flask import Flask, request
load_dotenv()

app = Flask(__name__)

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

class PersonalInfo(BaseModel):
    name : str
    email : str
    phone : str
    address : str

class Education(BaseModel):
    type : str
    name : str
    graduation_year : str
    couse : str
    gpa : str

class Experience(BaseModel):
    title : str
    organization : str
    date : str
    description : str

class Project(BaseModel):
    title : str
    description : str

class Certificate(BaseModel):
    title : str
    link : str

class Achievement(BaseModel):
    title : str
    description : str

class Coursework(BaseModel):
    title : str
    description : str

class ResumeResponse(BaseModel):
    personal_information : PersonalInfo
    education : list[Education]
    coursework: Optional[list[Coursework]]
    experience : Optional[list[Experience]]
    projects : list[Project]
    achievements : Optional[list[Achievement]]
    skills : str
    certificates : Optional[list[Certificate]]

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

    questions = data.get('questions', [])
    qna_details = ""    
    for q in questions:
        question = q.get('question')
        answer = q.get('answer')
        qna_details += f"\n- **{question}**: {answer}\n"

    project_coursework_prompt = ""
    experience_prompt = ""
    certificate_prompt = ""   

    if project_details:
        project_coursework_prompt = f"**Projects**: Detail key projects with their objectives, your role, technologies used, and the outcomes or impact. Use quantifiable metrics to demonstrate success: {project_details}\n\n"

    elif coursework_details:
        project_coursework_prompt = f"**Coursework**: Give a 1 line summary describing the relevant coursework that showcases your knowledge and skills in the field. Include the course name, topics covered, and any practical applications or projects completed. Mention any notable outcomes, presentations, or research work that demonstrates your expertise and commitment: {coursework_details}\n\n"
    
    if experience_details:
        experience_prompt = f"""**Experience**: Describe past work experience in at least 30 words, including job titles, company names, locations, dates of employment, and bullet points detailing responsibilities and achievements. Focus on using action verbs and quantifiable results to showcase impact: {experience_details}\n\n
                            Add points like : Gained valuable experience working within a specific industry, applying learned concepts directly into relevant work situations.
                            , Explored new technologies and approaches to streamline processes.
                            , Developed organizational skills through managing multiple tasks simultaneously while adhering to strict deadlines.
                            , Contributed to a positive team environment by collaborating with fellow interns on group projects and presentations.
                            , Utilized strong communication abilities during presentations which led to increased understanding among colleagues regarding project goals and objectives.
                            , etc.
                            """

    if certificate_details:
        certificate_prompt = f"**Certificates**: List any certifications or courses completed that are relevant to the job role. Include the issuing organization and completion date: {certificate_details}\n"
    
    if skills:
        skills_prompt = f"**Skills**: List key skills (both hard and soft skills) relevant to the job role. Use bullet points and include proficiency levels or years of experience where possible: {skills} add more skills you feel relevant based on the other information.3\n\n"
    else:
        skills_prompt = "Write as many soft and hard skills as possible based on the rest of the data provided in the prompt you can mention related skills based on the major taken by the user and experience too.\n\n"

    message_content =  f"""Create a professional, ATS-compliant resume using only the information provided. 
        Ensure the resume is tailored to increase the chances of being selected by recruiters by using industry-relevant keywords and quantifiable metrics where applicable. It needs to get a high ATS score.
        Do not add any new details or assumptions beyond what is given. Structure the resume with the following sections: Contact Information, Professional Summary, Education, Skills, Experience, Projects/Coursework, Achievements, and Certificates.\n\n
        The user has also answered specific questions that provide additional context about their experience, accomplishments, and skills. Please use this information to build a stronger and more personalized resume:\n
        {qna_details}\n\n
        Skip any section like projects, experience, or achievements if no corresponding information has been provided.\n
        The resume should be designed for the role of a {job_role}.\n

        **Contact Information**:\n
        - Name: {name}\n
        - Email: {email}\n
        - Phone: {phone}\n
        - Address: {address}\n
        
        **Professional Summary**: Write a concise summary highlighting key strengths, relevant expertise, and career goals in alignment with the job role.\n\n"
        **Education**: Provide details on the educational background, including degrees, institutions, graduation dates, and any honors or relevant coursework: {education_details}\n\n
        {skills_prompt}
        {experience_prompt}
        {project_coursework_prompt}
        **Achievements**: List any significant professional achievements, such as awards, recognitions, publications, or contributions. If applicable, certificates should also be included here: {achievement_details}\n\n
        {certificate_prompt}    
        """

    print(message_content, end = "\n\n\n\n\n\n\n")


    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "Your task is to generate a professional ATS compliant resume using only the provided information. The Resume should have a high ATS score."},
            {"role": "user", "content": message_content}
        ],
        response_format=ResumeResponse,
    )

    #research_paper = completion.choices[0].message.parsed
    cost = (completion.usage.completion_tokens * 0.0000006 + completion.usage.prompt_tokens * 0.00000015)
    print("Cost to run this model is : " + str(cost))
    output = completion.choices[0].message.content
    with open("demo.json", "w") as f:
        f.write(output)
    return output

if __name__ == '__main__':
    app.run(debug=True)