# Importing the Necessary Libraries:

import os
import time
import google.generativeai as genai
from google.api_core import retry
from dotenv import load_dotenv
load_dotenv()

# Configuring the Gemini API:

genai.configure(api_key=os.getenv("GOOGLE_API_KEY1"))

instruction = "Behave like the best pdf reader. Answer all the questions asked in the prompt by the user. Answer all the questions only from the content present in the uploaded pdf. The final answer should match the content in the uploaded file. Navigate to all the pages in the pdf and find the answer strictly."

safety = {
    'HATE' : 'BLOCK_NONE',
    'HARASSMENT' : 'BLOCK_NONE',
    'SEXUAL' : 'BLOCK_NONE',
    'DANGEROUS' : 'BLOCK_NONE',
}

# Configuring the Gemini Model:

model = genai.GenerativeModel(model_name="gemini-1.5-flash",generation_config=genai.GenerationConfig(
    temperature=1,
    top_p=0.95,
    top_k=64,
    response_mime_type='text/plain',
    max_output_tokens=8192,
),system_instruction=instruction, safety_settings=safety,)

# Uploading the File to the Gemini:

file_path = input("Enter the file path: ")

def upload_to_gemini(file_path):
    file = genai.upload_file(file_path)
    print(f"File Name: {file.display_name}, File Uri: {file.uri} and File Mime: {file.mime_type}")
    return file

file_uploaded = upload_to_gemini(file_path)
print(file_uploaded)

uploaded_file_name = file_uploaded.name
print(uploaded_file_name)

# Getting the File:

def get_files(file_uploaded):
    get_file = genai.get_file(uploaded_file_name)
    print(get_file.name)
    print(get_file.display_name, get_file.uri)
    print(get_file.state.name)
    while get_file.state.name == "PROCESSING":
        print("The File is Still Processing...")
        time.sleep(10)
        get_file = genai.get_file(uploaded_file_name)
        print(get_file.name)
        print(get_file.display_name, get_file.uri)
        print(get_file.state.name)
    if get_file.state.name == "FAILED":
        raise ValueError(get_file.state.name)
    if get_file.state.name != "ACTIVE":
        raise Exception(f"File Name: {get_file.name} Not Processed")
    return "The File is Ready Now..."

file_state = get_files(file_uploaded)
print(file_state)

for file in genai.list_files():
    print(f"File Name: {file.display_name}  and File URI: {file.uri}")

# Getting the Response:

chat = model.start_chat(history=[])
print(chat)

response = chat.send_message([input("Enter the prompt: "),file_uploaded],request_options={'retry' : retry.Retry(predicate=retry.if_transient_error)})
print(response.text.replace("**","").replace("#",""))

response = chat.send_message([input("Enter the prompt: "),file_uploaded],request_options={'retry' : retry.Retry(predicate=retry.if_transient_error)})
print(response.text.replace("**","").replace("#",""))

response = chat.send_message([input("Enter the prompt: "),file_uploaded],request_options={'retry' : retry.Retry(predicate=retry.if_transient_error)})
print(response.text.replace("**","").replace("#",""))

print(chat.history)

for file in genai.list_files():
    print(f"File Name: {file.display_name}  and File URI: {file.uri}")
    print(f"The file to be deleted: {file.display_name}")
    genai.delete_file(file)

for file in genai.list_files():
    print(f"File Name: {file.display_name}  and File URI: {file.uri}")

print("File Deleted Successfully.")