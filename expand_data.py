from flask import Flask, request, jsonify
import requests
import os
import json
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")


def enhance_json_with_chatgpt(data):
    """
    This function takes the initial JSON and sends it to ChatGPT to enhance the information.
    """
    # Create a system and user prompt to augment the data
    system_prompt = "You are a helpful assistant who augments resume sections with more information. Add relevant and realistic details to each section based on the information given."
    
    # Construct the user message with the provided JSON data
    user_message = f"Here is the initial resume data: {json.dumps(data)}. Please enhance each section with additional relevant information like skills, projects, experience, and more. Don't add any false information."

    # Setup request headers
    headers = {
        "Content-Type": "application/json",
        "api-key": azure_openai_api_key,
    }

    # Request body for ChatGPT
    request_body = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 1000,
        "temperature": 0.7  # Increase creativity slightly
    }

    # Send request to Azure OpenAI to enhance the resume data
    response = requests.post(
        f"{azure_openai_endpoint}/openai/deployments/{azure_openai_deployment_name}/chat/completions?api-version={azure_openai_api_version}",
        headers=headers,
        json=request_body
    )

    # Check response status
    if response.status_code == 200:
        enhanced_json = response.json().get("choices")[0].get("message").get("content")
        return json.loads(enhanced_json)
    else:
        raise Exception(f"Error from OpenAI: {response.text}")


@app.route('/enhance_resume', methods=['POST'])
def enhance_resume():
    """
    This function takes a JSON input, sends it to ChatGPT for enhancement, 
    and writes the enhanced JSON to a file called demo.json.
    """
    # Step 1: Get the initial JSON data from the request
    data = request.json
    print(data)
    # Step 2: Enhance the JSON with ChatGPT
    try:
        enhanced_data = enhance_json_with_chatgpt(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # Step 3: Write the enhanced JSON to a file named demo.json
    try:
        with open('demo.json', 'w') as f:
            json.dump(enhanced_data, f, indent=4)  # Write to file with pretty printing
    except Exception as e:
        return jsonify({"error": f"Failed to write file: {str(e)}"}), 500

    # Step 4: Return success message
    return jsonify({"message": "Enhanced JSON has been written to demo.json"})


if __name__ == '__main__':
    app.run(debug=True)
