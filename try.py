import requests
import os
import json
from dotenv import load_dotenv
import chardet
load_dotenv()
import PyPDF2
import os

from groq import Groq
# Set your Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Define the JSON template
json_template = {
  "personalInfo": {
    "name": "",
    "email": "",
    "phone": "",
    "location": {
      "city": "",
      "state": "",
      "country": ""
    },
    "summary": ""
  },
  "links": {
    "linkedin": "",
    "github": "",
    "portfolio": "",
    "otherProfessionalLinks": []
  },
  "skills": [
    {
      "category": "",
      "skills": []
    }
  ],
  "workExperience": [
    {
      "company": "",
      "position": "",
      "location": "",
      "startDate": "",
      "endDate": "",
      "duration": "",
      "responsibilities": [],
      "achievements": []
    }
  ],
  "projects": [
    {
      "name": "",
      "description": "",
      "role": "",
      "startDate": "",
      "endDate": "",
      "duration": "",
      "technologies": [],
      "link": "",
      "achievements": []
    }
  ],
  "education": [
    {
      "institution": "",
      "degree": "",
      "fieldOfStudy": "",
      "graduationDate": "",
      "gpa": "",
      "relevantCoursework": []
    }
  ],
  "certifications": [
    {
      "name": "",
      "issuingOrganization": "",
      "issueDate": "",
      "expirationDate": "",
      "credentialId": ""
    }
  ],
  "languages": [
    {
      "language": "",
      "proficiency": ""
    }
  ],
  "awards": [
    {
      "title": "",
      "issuer": "",
      "date": "",
      "description": ""
    }
  ],
  "publications": [
    {
      "title": "",
      "publisher": "",
      "date": "",
      "link": ""
    }
  ]
}

# Function to read PDF content
def read_pdf(file_path):
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

# Function to parse resume using Groq LLM
def parse_resume(file_path):
    if file_path.endswith('.pdf'):
        resume_text = read_pdf(file_path)


    client = Groq(
        api_key=GROQ_API_KEY,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            {
                "role": "system",
                "content": "You are Resume Parser"
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": f"""Parse the following resume and fill in the JSON template:
                               Resume: {resume_text}
                               Template: {json_template}
                               Return only the filled JSON template as valid JSON.""",
            }
        ],
        model="llama-3.1-8b-instant",
    )

    # Print the completion returned by the LLM.
    # print(chat_completion.choices[0].message.content)
    
    
    return chat_completion.choices[0].message.content

# Process all resumes in the 'resumes' folder
resume_folder = 'resumes'
parsed_folder = 'parsed'


for resume_file in os.listdir(resume_folder):
    if resume_file.endswith('.txt') or resume_file.endswith('.pdf'):
        resume_path = os.path.join(resume_folder, resume_file)
        parsed_data = parse_resume(resume_path)
        
        text_file_name = os.path.splitext(resume_file)[0] + '.txt'
        text_file_path = parsed_folder + "/" + text_file_name
        
        with open(text_file_path, 'w' , encoding="utf-8") as text_file:
            text_file.write(parsed_data)

print("Resumes parsed and saved successfully.")
