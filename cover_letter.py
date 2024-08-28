from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

@app.route('/generate_coverletter', methods=['POST'])
def generate_coverletter():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    receiver = data.get('receiver')
    skills = data.get('skills')
    job_description = data.get('job_description')
    date = data.get('date')
    company = data.get('company')
    

    education = data.get('education', [])
    education_details = ""
    for edu in education:
        edu_type = edu.get('type')
        edu_name = edu.get('name')
        graduation_year = edu.get('graduation_year')
        education_details += f"\n- **{edu_type}**: {edu_name}, Graduation Year: {graduation_year}\n"


    experience = data.get('experience', [])
    experience_details = ""
    for exp in experience:
        exp_title = exp.get('title')
        exp_company = exp.get('company')
        exp_duration = exp.get('duration')
        exp_description = exp.get('description')
        experience_details += f"\n- **{exp_title}** at **{exp_company}** ({exp_duration}): {exp_description}\n"


    achievements = data.get('achievements', [])
    achievements_details = ""
    for achievement in achievements:
        achievements_details += f"\n- {achievement}\n"

    message_content = f"""
    Write a compelling and impactful cover letter in markdown based on the following information:

    **Name**: {name}
    **Email**: {email}
    **Phone**: {phone}
    **Date**: {date}
    **Recipient**: {receiver}
    **Company**: {company}
    **Job Description**: {job_description}
    **Skills**: {skills}
    **Education**: {education_details}
    **Experience**: {experience_details}
    **Achievements**: {achievements_details}

    The cover letter should follow these guidelines to stand out from others:

    1. **Greeting and Introduction**: Start with a professional greeting to the recipient and clearly state the position being applied for. Express genuine excitement about the opportunity and the company.

    2. **Enthusiasm for the Role and Company**: Highlight specific reasons for your interest in the role and the company. Mention aspects of the company’s mission, values, or recent achievements that align with your professional goals and values.

    3. **Relevant Background and Key Achievements**: Describe your professional background with a focus on relevant skills and experiences. Use specific, quantifiable achievements that showcase your abilities. For example, mention how you increased efficiency, improved processes, or contributed to team success. Quantify these achievements (e.g., "boosted team productivity by 20%" or "reduced operational costs by 15%").

    4. **Specific Examples Demonstrating Suitability**: Provide concrete examples and success stories that demonstrate your suitability for the role. Use data and metrics to highlight how your past work has led to successful outcomes. For instance, if applying for a management role, mention how you led a team to complete a project ahead of schedule or under budget.

    5. **Connection to the Company's Needs**: Clearly connect your skills and experiences with the specific needs of the company as outlined in the job description. Show how your background makes you an ideal fit to solve the company’s challenges or contribute to its goals.

    6. **Conclusion and Call to Action**: Reiterate your strong interest in the role and express enthusiasm about the possibility of contributing to the company's success. Invite the recipient to contact you for further discussion or to schedule an interview. Thank the recipient for their time and consideration.

    7. **Sign-off**: End with a professional sign-off and include your name.

    The cover letter should be persuasive, tailored, and demonstrate a deep understanding of the company and role. Use a confident tone and keep the content concise and impactful, ensuring it leaves a memorable impression on the recipient.
    """


    system_prompt = "Generate a professional cover letter that highlights the candidate's suitability for the role, following a structured and concise format. The response should contain only the cover letter text without any comments, explanations, or other extraneous text."


    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": message_content},
            {"role": "system", "content": system_prompt}
        ],
    )

    coverletter_content = response.choices[0].message.content
    print(coverletter_content)
    return jsonify({"cover_letter": coverletter_content})

if __name__ == '__main__':
    app.run(debug=True)
