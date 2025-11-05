from google import genai

GEMINI_API_KEY = "AIzaSyB2arbikQESDp2vFElG3xuBjuvRRjYwfMQ"

# Takes in a prompt to the gemini api and returns a string of the AIs response
# @param: the prompt for the AI to respond to
# @pre: none
# @post: get_ai_response = string containing the AIs response
# @returns: a string of the AIs response
def get_ai_response(prompt):
    client = genai.Client(api_key= GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt, "hi"]
    )
   
    return response.text
