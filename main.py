from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

with open('data.json', 'r') as file:
    data = json.load(file)



name = data.get('name')
email = data.get('email')
phone = data.get('phone')
address = data.get('address')
college = data.get('college')
skills = data.get('skills')


experience = data.get('experience', [])
experience_details = ""
for exp in experience:
    exp_title = exp.get('title')
    exp_company = exp.get('company')
    exp_duration = exp.get('duration')
    exp_description = exp.get('description')
    experience_details += f"\n- **{exp_title}** at **{exp_company}** ({exp_duration}): {exp_description}\n"

message_content = (
    f"Create a professional resume based on the following information in markdown format, "
    f"make sure it is ATS compliant. Add more information to each experience section and make it sound very professional with the right keywords:\n\n"
    f"**Name**: {name}\n"
    f"**Email**: {email}\n"
    f"**Phone**: {phone}\n"
    f"**Address**: {address}\n"
    f"**College**: {college}\n"
    f"**Skills**: {skills}\n"
    f"**Experience**: {experience_details}"
)

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": message_content}],
    stream=True,
)
print()
with open('resume.md', 'w') as file:
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            file.write(chunk.choices[0].delta.content)
            #print(chunk.choices[0].delta.content, end="")
