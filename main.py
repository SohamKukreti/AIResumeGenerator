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

    latex_template = (
    "\\documentclass[letterpaper,11pt]{article}\n"
    "\\usepackage{latexsym}\n"
    "\\usepackage[empty]{fullpage}\n"
    "\\usepackage{titlesec}\n"
    "\\usepackage{marvosym}\n"
    "\\usepackage[usenames,dvipsnames]{color}\n"
    "\\usepackage{verbatim}\n"
    "\\usepackage{enumitem}\n"
    "\\usepackage[hidelinks]{hyperref}\n"
    "\\usepackage{fancyhdr}\n"
    "\\usepackage[english]{babel}\n"
    "\\usepackage{tabularx}\n"
    "\\input{glyphtounicode}\n"
    "\\pagestyle{fancy}\n"
    "\\fancyhf{}\n"
    "\\fancyfoot{}\n"
    "\\renewcommand{\\headrulewidth}{0pt}\n"
    "\\renewcommand{\\footrulewidth}{0pt}\n"
    "\\addtolength{\\oddsidemargin}{-0.5in}\n"
    "\\addtolength{\\evensidemargin}{-0.5in}\n"
    "\\addtolength{\\textwidth}{1in}\n"
    "\\addtolength{\\topmargin}{-.5in}\n"
    "\\addtolength{\\textheight}{1.0in}\n"
    "\\urlstyle{same}\n"
    "\\raggedbottom\n"
    "\\raggedright\n"
    "\\setlength{\\tabcolsep}{0in}\n"
    "\\titleformat{\\section}{\n"
    "  \\vspace{-4pt}\\scshape\\raggedright\\large\n"
    "}{}{0em}{}[\\color{black}\\titlerule \\vspace{-5pt}]\n"
    "\\pdfgentounicode=1\n"
    "\\newcommand{\\resumeItem}[1]{\n"
    "  \\item\\small{\n"
    "    {#1 \\vspace{-2pt}}\n"
    "  }\n"
    "}\n"
    "\\newcommand{\\resumeSubheading}[4]{\n"
    "  \\vspace{-2pt}\\item\n"
    "    \\begin{tabular*}{0.97\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}\n"
    "      \\textbf{#1} & #2 \\\\\n"
    "      \\textit{\\small#3} & \\textit{\\small #4} \\\\\n"
    "    \\end{tabular*}\\vspace{-7pt}\n"
    "}\n"
    "\\newcommand{\\resumeSubSubheading}[2]{\n"
    "    \\item\n"
    "    \\begin{tabular*}{0.97\\textwidth}{l@{\\extracolsep{\\fill}}r}\n"
    "      \\textit{\\small#1} & \\textit{\\small #2} \\\\\n"
    "    \\end{tabular*}\\vspace{-7pt}\n"
    "}\n"
    "\\newcommand{\\resumeProjectHeading}[2]{\n"
    "    \\item\n"
    "    \\begin{tabular*}{0.97\\textwidth}{l@{\\extracolsep{\\fill}}r}\n"
    "      \\small#1 & #2 \\\\\n"
    "    \\end{tabular*}\\vspace{-7pt}\n"
    "}\n"
    "\\newcommand{\\resumeSubItem}[1]{\\resumeItem{#1}\\vspace{-4pt}}\n"
    "\\renewcommand\\labelitemii{\\$\\vcenter{\\hbox{\\tiny$\\bullet$}}\\$}\n"
    "\\newcommand{\\resumeSubHeadingListStart}{\\begin{itemize}[leftmargin=0.15in, label={}]}\n"
    "\\newcommand{\\resumeSubHeadingListEnd}{\\end{itemize}}\n"
    "\\newcommand{\\resumeItemListStart}{\\begin{itemize}}\n"
    "\\newcommand{\\resumeItemListEnd}{\\end{itemize}\\vspace{-5pt}}\n"
    "\\begin{document}\n"
    "\\begin{center}\n"
    "    \\textbf{\\Huge \\scshape Your Name} \\\\ \\vspace{1pt}\n"
    "    \\small 0000000000 $|$ \\href{mailto:emailaddress}{\\underline{youremail}} $|$ \n"
    "    \\href{https://linkedin.com/in/linkedin}{\\underline{linkedin.com/in/linkedin}} $|$\n"
    "    \\href{https://github.com/github}{\\underline{github.com/github}}\n"
    "\\end{center}\n"
    "\\section{Education}\n"
    "  \\resumeSubHeadingListStart\n"
    "    \\resumeSubheading\n"
    "      {College}{City, Country}\n"
    "      {Course}{Expected Graduation:}\n"
    "  \\resumeSubHeadingListEnd\n"
    "\\section{Experience}\n"
    "  \\resumeSubHeadingListStart\n"
    "    \\resumeSubheading\n"
    "      {Experience 1} {Start and End date}\n"
    "      {Summary}{}\n"
    "      \\resumeItemListStart\n"
    "        \\resumeItem{Details about Experience}\n"
    "     \\resumeItemListEnd\n"
    "    \\resumeSubheading\n"
    "      {Experience 2}{Start and End date}\n"
    "      {Summary}{}\n"
    "      \\resumeItemListStart\n"
    "        \\resumeItem{Details about experience}\n"
    "    \\resumeItemListEnd\n"
    "  \\resumeSubHeadingListEnd\n"
    " \\section{Achievements}\n"
    " \\begin{itemize}[leftmargin=0.15in, label={}]\n"
    "    \\small{\\item{\n"
    "     \\textbf{Achievement 1}{: Details about achievement } \\\\\n"
    "     \\textbf{Achievement 2}{: Details about achievement} \\\\\n"
    "    }}\n"
    " \\end{itemize}\n"
    "\\section{Projects}\n"
    "    \\resumeSubHeadingListStart\n"
    "      \\resumeProjectHeading\n"
    "          {\\textbf{Project 1} $|$ \\emph{Languages and technologies}}{Date built}\n"
    "          \\resumeItemListStart\n"
    "            \\resumeItem{Details about project}\n"
    "          \\resumeItemListEnd\n"
    "    \\resumeSubHeadingListEnd\n"
    "\\section{Technical Skills}\n"
    " \\begin{itemize}[leftmargin=0.15in, label={}]\n"
    "    \\small{\\item{\n"
    "     \\textbf{Languages}{: languages here } \\\\\n"
    "     \\textbf{Frameworks}{: Frameworks here if there} \\\\\n"
    "     \\textbf{Developer Tools}{: } \\\\\n"
    "     \\textbf{Libraries}{: Libraries here if there} \\\\\n"
    "     \\textbf{Other Skills}{: Other skills}\n"
    "    }}\n"
    " \\end{itemize}\n"
    "\\section{Certificates}\n"
    " \\begin{itemize}[leftmargin=0.15in, label={}]\n"
    "    \\small{\\item{\n"
    "     \\textbf{Certificate 1}{: Details about Certificate } \\\\\n"
    "     \\textbf{Certificate 2}{: Details about Certificate} \\\\\n"
    "    }}\n"
    " \\end{itemize}\n"
    "\\end{document}\n"
    )

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


    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": message_content}],
    )

    resume_content = response.choices[0].message.content

    return jsonify({"resume": resume_content})

if __name__ == '__main__':
    app.run(debug=True)