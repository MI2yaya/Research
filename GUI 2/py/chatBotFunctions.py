# chatBotFunctions.py
from dotenv import load_dotenv
from openai import OpenAI
import os
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting

load_dotenv()

# Global variable to store the loaded model
loaded_model = None

def load_ml_model(character,model):
    global loaded_model
    if character == "Model 1":
        if model=="GPT":
            global client, defaultMessage
            loaded_model = "ft:gpt-4o-2024-08-06:personal::AYGKLhoP"
            openai_key = os.getenv("OPENAPI_KEY")
            client = OpenAI(api_key = openai_key)
            defaultMessage = f"You are a factual chatbot which aims to replicate a simulated patient for use in training residents to become psychotherapists."
            defaultMessage += f"Your name is Bot1 and your age is between 65 with the mental illness: Major Depressive Disorder"
            print(f"{loaded_model} preloaded.")
            return(loaded_model)
        if model=="GPT-Mini":
            global client, defaultMessage
            loaded_model = "ft:gpt-4o-mini-2024-07-18:personal::AJSd1eeZ"
            openai_key = os.getenv("OPENAPI_KEY")
            client = OpenAI(api_key = openai_key)
            defaultMessage = f"You are a factual chatbot which aims to replicate a simulated patient for use in training residents to become psychotherapists."
            defaultMessage += f"Your name is Bot1 and your age is between 65 with the mental illness: Major Depressive Disorder"
            print(f"{loaded_model} preloaded.")
            return(loaded_model)
        if model=="Gemini":
            global generation_config, safety_settings, conversation_gemini
            loaded_model = "projects/903507590578/locations/us-east1/endpoints/4254410710097854464"
            vertexai.init(project=os.getenv("GOOGLE_PROJECT"),location="us-east1")
            client = GenerativeModel(loaded_model)
            conversation_gemini = client.start_chat()
            print(f"{loaded_model} preloaded.")
            return(loaded_model)
            

    elif character == "Model 2":
        if model=="GPT":
            global client, defaultMessage
            loaded_model = "ft:gpt-4o-2024-08-06:personal::AlR6KFIV"
            openai_key = os.getenv("OPENAPI_KEY")
            client = OpenAI(api_key = openai_key)
            defaultMessage = f"You are a factual chatbot which aims to replicate a simulated patient for use in training residents to become psychotherapists."
            defaultMessage += f"Your name is Bot1 and your age is 50 with the mental illness: Generalized Anxiety Disorder"
            print(f"{loaded_model} preloaded.")
            return(loaded_model)
        if model=="GPT-Mini":
            global client, defaultMessage
            loaded_model = "ft:gpt-4o-mini-2024-07-18:personal::AlQaBHUm"
            openai_key = os.getenv("OPENAPI_KEY")
            client = OpenAI(api_key = openai_key)
            defaultMessage = f"You are a factual chatbot which aims to replicate a simulated patient for use in training residents to become psychotherapists."
            defaultMessage += f"Your name is Bot1 and your age is 50 with the mental illness: Generalized Anxiety Disorder"
            print(f"{loaded_model} preloaded.")
            return(loaded_model)
        if model=="Gemini":
            global conversation_gemini
            loaded_model = "projects/903507590578/locations/us-east1/endpoints/2611933852246999040"
            vertexai.init(project=os.getenv("GOOGLE_PROJECT"),location="us-east1")
            client = GenerativeModel(loaded_model)
            conversation_gemini = client.start_chat()
            print(f"{loaded_model} preloaded.")
            return(loaded_model)
            
    else:
        # ETC
        loaded_model = ""
        print("Default model preloaded.")

def get_ml_response(user_message):
    if not loaded_model:
        return "Model is not loaded. Please load the model first."

    print("Getting input")
    
    gpts=["ft:gpt-4o-2024-08-06:personal::AYGKLhoP","ft:gpt-4o-mini-2024-07-18:personal::AJSd1eeZ","ft:gpt-4o-mini-2024-07-18:personal::AlQaBHUm"]
    geminis=["projects/903507590578/locations/us-east1/endpoints/4254410710097854464","projects/903507590578/locations/us-east1/endpoints/7719015829685141504"]
    if loaded_model in gpts:
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
    
    if loaded_model in geminis:
        try:
            generation_config = {
                "max_output_tokens": 8192,
                "temperature": 0.5,
            }

            safety_settings = [
                SafetySetting(
                    category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=SafetySetting.HarmBlockThreshold.OFF
                ),
                SafetySetting(
                    category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=SafetySetting.HarmBlockThreshold.OFF
                ),
                SafetySetting(
                    category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=SafetySetting.HarmBlockThreshold.OFF
                ),
                SafetySetting(
                    category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=SafetySetting.HarmBlockThreshold.OFF
                ),
            ]
            response = conversation_gemini.send_message(
                content = user_message,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            return(response.text)
        except Exception as e:
            return f"Error generating response: {str(e)}"