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
    
    # Extract information from JSON
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    college = data.get('college')
    skills = data.get('skills')

    # Prepare experience details
    experience = data.get('experience', [])
    experience_details = ""
    for exp in experience:
        exp_title = exp.get('title')
        exp_company = exp.get('company')
        exp_duration = exp.get('duration')
        exp_description = exp.get('description')
        experience_details += f"\n- **{exp_title}** at **{exp_company}** ({exp_duration}): {exp_description}\n"

    # Create the message content
    message_content = (
        f"Create a professional resume based on the following information, "
        f"make sure it is ATS compliant. Also at the end give some pointers on how to make the resume more ATS compliant:\n\n"
        f"**Name**: {name}\n"
        f"**Email**: {email}\n"
        f"**Phone**: {phone}\n"
        f"**Address**: {address}\n"
        f"**College**: {college}\n"
        f"**Skills**: {skills}\n"
        f"**Experience**: {experience_details}"
    )

    # Request OpenAI to generate the resume
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message_content}],
    )

    # Extract the resume content from the response
    resume_content = response.choices[0].message.content

    return jsonify({"resume": resume_content})

if __name__ == '__main__':
    app.run(debug=True)
