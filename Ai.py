import os
from google.cloud import vision
from google import genai
import io

# Process uploaded file and extract its content
def process_uploaded_file(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content

# Analyze the image using Google Cloud Vision API
def analyze_image(image_path, json_path):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Service account file not found: {json_path}")

    client = vision.ImageAnnotatorClient.from_service_account_file(json_path)
   
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
   
    # Provides key words to describe image used for sorting
    label_response = client.label_detection(image=image) 
    labels = label_response.label_annotations
    label_descriptions = [label.description for label in labels]
   
    # Compares pre existing data and adds info to image
    web_response = client.web_detection(image=image)
    web_entities = web_response.web_detection.web_entities
    web_descriptions = [entity.description for entity in web_entities if entity.description]
   
    # Combine labels and web entities to create a description
    combined_descriptions = label_descriptions + web_descriptions
    unique_descriptions = list(set(combined_descriptions))  # Remove duplicates
    description = ', '.join(unique_descriptions)
   
    return description

# Integrate file content into the AI model request
def get_ai_response(file_content, question):
    client = genai.Client(api_key="AIzaSyB2arbikQESDp2vFElG3xuBjuvRRjYwfMQ")  # API key
   
    # Combine the file content with the user's question
    combined_content = f"{file_content}\n\n{question}"
   
    # Ensure the model name and API request are correct
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[combined_content]  # Wrap contents in a list to match API expectations
    )
   
    return response.text
