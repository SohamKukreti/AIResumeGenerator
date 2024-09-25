import json

# Function to add multiple entries
def add_multiple_entries(prompt_message, add_function):
    entries = []
    while True:
        entries.append(add_function())
        another = input(f"Do you want to add another {prompt_message}? (yes/no): ").strip().lower()
        if another != 'yes':
            break
    return entries

# Functions to get different sections
def get_education():
    return {
        "type": input("Enter the type (University/High School): "),
        "name": input("Enter the name of the institution: "),
        "graduation_year": input("Enter the graduation year: "),
        "course": input("Enter your course (if applicable, otherwise leave blank): "),
        "GPA": input("Enter your GPA/percentage: ")
    }

def get_experience():
    return {
        "title": input("Enter your experience title: "),
        "company": input("Enter the company: "),
        "duration": input("Enter the duration (e.g., May-July 2024): "),
        "description": input("Enter the description: ")
    }

def get_project():
    return {
        "title": input("Enter the title of your project: "),
        "description": input("Enter the description of your project: ")
    }

def get_achievement():
    return {
        "title": input("Enter the title of your achievement: "),
        "description": input("Enter the description of your achievement: ")
    }

def get_certificate():
    return {
        "title": input("Enter the title of your certificate: "),
        "link": input("Enter the link to your certificate: ")
    }

# Function to take input from user and store in dictionary
def get_resume_data():
    resume = {
        "name": input("Enter your name: "),
        "email": input("Enter your email: "),
        "phone": input("Enter your phone number: "),
        "address": input("Enter your address: "),
        "role": input("Enter your desired role: "),
        "Education": add_multiple_entries("education entry", get_education),
        "experience": add_multiple_entries("experience", get_experience),
        "projects": add_multiple_entries("project", get_project),
        "Achievements": add_multiple_entries("achievement", get_achievement),
        "certificates": add_multiple_entries("certificate", get_certificate),
        "skills": input("Enter your skills (separated by commas): ")
    }
    return resume

# Function to save data to a JSON file
def save_resume_to_json(resume):
    with open("resume.json", "w") as json_file:
        json.dump(resume, json_file, indent=4)
    print("Your resume has been saved to 'resume.json'.")

# Main logic
if __name__ == "__main__":
    resume_data = get_resume_data()
    save_resume_to_json(resume_data)
