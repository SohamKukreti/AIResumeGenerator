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

    latex_template = """
    \\documentclass[letterpaper,11pt]{article}
    \\usepackage{latexsym}
    \\usepackage[empty]{fullpage}
    \\usepackage{titlesec}
    \\usepackage{marvosym}
    \\usepackage[usenames,dvipsnames]{color}
    \\usepackage{verbatim}
    \\usepackage{enumitem}
    \\usepackage[hidelinks]{hyperref}
    \\usepackage{fancyhdr}
    \\usepackage[english]{babel}
    \\usepackage{tabularx}
    \\input{glyphtounicode}
    \\pagestyle{fancy}
    \\fancyhf{}
    \\fancyfoot{}
    \\renewcommand{\\headrulewidth}{0pt}
    \\renewcommand{\\footrulewidth}{0pt}
    \\addtolength{\\oddsidemargin}{-0.5in}
    \\addtolength{\\evensidemargin}{-0.5in}
    \\addtolength{\\textwidth}{1in}
    \\addtolength{\\topmargin}{-.5in}
    \\addtolength{\\textheight}{1.0in}
    \\urlstyle{same}
    \\raggedbottom
    \\raggedright
    \\setlength{\\tabcolsep}{0in}
    \\titleformat{\\section}{
    \\vspace{-4pt}\\scshape\\raggedright\\large
    }{}{0em}{}[\\color{black}\\titlerule \\vspace{-5pt}]
    \\pdfgentounicode=1
    \\newcommand{\\resumeItem}[1]{
    \\item\\small{
        {#1 \\vspace{-2pt}}
    }
    }
    \\newcommand{\\resumeSubheading}[4]{
    \\vspace{-2pt}\\item
        \\begin{tabular*}{0.97\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}
        \\textbf{#1} & #2 \\\\
        \\textit{\\small#3} & \\textit{\\small #4} \\\\
        \\end{tabular*}\\vspace{-7pt}
    }
    \\newcommand{\\resumeSubSubheading}[2]{
        \\item
        \\begin{tabular*}{0.97\\textwidth}{l@{\\extracolsep{\\fill}}r}
        \\textit{\\small#1} & \\textit{\\small #2} \\\\
        \\end{tabular*}\\vspace{-7pt}
    }
    \\newcommand{\\resumeProjectHeading}[2]{
        \\item
        \\begin{tabular*}{0.97\\textwidth}{l@{\\extracolsep{\\fill}}r}
        \\small#1 & #2 \\\\
        \\end{tabular*}\\vspace{-7pt}
    }
    \\newcommand{\\resumeSubItem}[1]{\\resumeItem{#1}\\vspace{-4pt}}
    \\renewcommand\\labelitemii{\\$\\vcenter{\\hbox{\\tiny$\\bullet$}}\\$}
    \\newcommand{\\resumeSubHeadingListStart}{\\begin{itemize}[leftmargin=0.15in, label={}]}
    \\newcommand{\\resumeSubHeadingListEnd}{\\end{itemize}}
    \\newcommand{\\resumeItemListStart}{\\begin{itemize}}
    \\newcommand{\\resumeItemListEnd}{\\end{itemize}\\vspace{-5pt}}
    \\begin{document}
    \\begin{center}
        \\textbf{\\Huge \\scshape Your Name} \\\\ \\vspace{1pt}
        \\small 0000000000 $|$ \\href{mailto:emailaddress}{\\underline{youremail}} $|$ 
        \\href{https://linkedin.com/in/linkedin}{\\underline{linkedin.com/in/linkedin}} $|$
        \\href{https://github.com/github}{\\underline{github.com/github}}
    \\end{center}
    \\section{Education}
    \\resumeSubHeadingListStart
        \\resumeSubheading
        {College}{City, Country}
        {Course}{Expected Graduation:}
    \\resumeSubHeadingListEnd
    \\section{Experience}
    \\resumeSubHeadingListStart
        \\resumeSubheading
        {Experience 1} {Start and End date}
        {Summary}{}
        \\resumeItemListStart
            \\resumeItem{Details about Experience}
        \\resumeItemListEnd
        \\resumeSubheading
        {Experience 2}{Start and End date}
        {Summary}{}
        \\resumeItemListStart
            \\resumeItem{Details about experience}
        \\resumeItemListEnd
    \\resumeSubHeadingListEnd
    \\section{Achievements}
    \\begin{itemize}[leftmargin=0.15in, label={}]
        \\small{\\item{
        \\textbf{Achievement 1}{: Details about achievement } \\\\
        \\textbf{Achievement 2}{: Details about achievement} \\\\
        }}
    \\end{itemize}
    \\section{Projects}
        \\resumeSubHeadingListStart
        \\resumeProjectHeading
            {\\textbf{Project 1} $|$ \\emph{Languages and technologies}}{Date built}
            \\resumeItemListStart
                \\resumeItem{Details about project}
            \\resumeItemListEnd
        \\resumeSubHeadingListEnd
    \\section{Technical Skills}
    \\begin{itemize}[leftmargin=0.15in, label={}]
        \\small{\\item{
        \\textbf{Languages}{: languages here } \\\\
        \\textbf{Frameworks}{: Frameworks here if there} \\\\
        \\textbf{Developer Tools}{: } \\\\
        \\textbf{Libraries}{: Libraries here if there} \\\\
        \\textbf{Other Skills}{: Other skills}
        }}
    \\end{itemize}
    \\section{Certificates}
    \\begin{itemize}[leftmargin=0.15in, label={}]
        \\small{\\item{
        \\textbf{Certificate 1}{: Details about Certificate } \\\\
        \\textbf{Certificate 2}{: Details about Certificate} \\\\
        }}
    \\end{itemize}
    \\end{document}
    """


    message_content = (
        f"Use the following LaTeX template to create a professional, ATS-friendly resume with the given information. "
        f"Ensure the resume has a high chance of getting selected by recruiters by using industry-relevant keywords and quantifiable metrics where applicable. "
        f"Do not invent any details not provided in this prompt. Structure the resume with the following sections: Contact Information, Professional Summary, Skills, Education, Experience, Projects, Achievements, and Certificates.\n\n"
        
        f"{latex_template}\n\n"
        
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

    system_prompt = "Your task is to generate a professional resume using only the provided information. Format the resume strictly according to the sections mentioned and avoid adding any extra text, commentary, or conversation outside of the resume structure. The output should be a well-structured resume, directly ready for use, without any prefatory or explanatory comments."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": message_content}, {"role": "system", "content": system_prompt}],
    )

    resume_content = response.choices[0].message.content

    return jsonify({"resume": resume_content})

if __name__ == '__main__':
    app.run(debug=True)