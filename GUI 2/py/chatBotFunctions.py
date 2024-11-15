# chatBotFunctions.py
from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv()

# Global variable to store the loaded model
loaded_model = None

def load_ml_model(model_name):
    global loaded_model
    if model_name == "Dummy Model":
        global client, defaultMessage
        loaded_model = "ft:gpt-4o-mini-2024-07-18:personal::AJSd1eeZ"
        openai_key = os.getenv("OPENAPI_KEY")
        client = OpenAI(api_key = openai_key)
        defaultMessage = f"You are a factual chatbot which aims to replicate a simulated patient for use in training residents to become psychotherapists."
        defaultMessage += f"Your name is Bot1 and your age is between 60-70 with the mental illness: Major Depressive Disorder"
        
        print(f"{loaded_model} preloaded.")
        return(loaded_model)
    elif model_name == "Model 2":
        # ETC
        loaded_model = ""
        print(f"{model_name} preloaded.")
    else:
        # ETC
        loaded_model = ""
        print("Default model preloaded.")

def get_ml_response(user_message):
    if not loaded_model:
        return "Model is not loaded. Please load the model first."

    print("Getting input")
    
    if loaded_model == "ft:gpt-4o-mini-2024-07-18:personal::AJSd1eeZ":
        try:
            
            completion = client.chat.completions.create(
                model = loaded_model,
                messages=[
                    {"role":"system",'content':defaultMessage},
                    {'role':'user','content':user_message}
                ]
            ) 
            return completion.choices[0].message.content
        
        except Exception as e:
            return f"Error generating response: {str(e)}"