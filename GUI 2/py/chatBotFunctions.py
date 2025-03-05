# chatBotFunctions.py
from dotenv import load_dotenv
from openai import OpenAI
import os
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting
from flask import Flask, jsonify, request
import traceback

load_dotenv()

# Global variable to store the loaded model
loaded_model = None

def load_ml_model(character,model):
    global loaded_model, client, defaultMessage, conversation_gemini
    if character == "Model 1":
        if model=="GPT":
            loaded_model = "ft:gpt-4o-2024-08-06:personal::AYGKLhoP"
            openai_key = os.getenv("OPENAPI_KEY")
            client = OpenAI(api_key = openai_key)
            defaultMessage = f"You are a factual chatbot which aims to replicate a simulated patient for use in training residents to become psychotherapists."
            defaultMessage += f"Your name is Abe and your age is 65 with the mental illness: Major Depressive Disorder."
            defaultMessage += f"This is a virtual therapy session with a new therapist, however, your personal experiences are the same."
            defaultMessage += f"This is a conversation with a new therapist, who you have not talked with prior, do not refer to prior sessions."
            print(f"{loaded_model} preloaded.")
            return(loaded_model)
        if model=="GPT-Mini":
            loaded_model = "ft:gpt-4o-mini-2024-07-18:personal::AJSd1eeZ"
            openai_key = os.getenv("OPENAPI_KEY")
            client = OpenAI(api_key = openai_key)
            defaultMessage = f"You are a factual chatbot which aims to replicate a simulated patient for use in training residents to become psychotherapists."
            defaultMessage += f"Your name is Abe and your age is  65 with the mental illness: Major Depressive Disorder."
            defaultMessage += f"This is a virtual therapy session with a new therapist, however, your personal experiences are the same."
            defaultMessage += f"This is a conversation with a new therapist, who you have not talked with prior, do not refer to prior sessions."
            print(f"{loaded_model} preloaded.")
            return(loaded_model)
        if model=="Gemini":
            loaded_model = "projects/903507590578/locations/us-east1/endpoints/4254410710097854464"
            vertexai.init(project=os.getenv("GOOGLE_PROJECT"),location="us-east1")
            client = GenerativeModel(loaded_model)
            conversation_gemini = client.start_chat()
            print(f"{loaded_model} preloaded.")
            return(loaded_model)
            

    elif character == "Model 2":
        if model=="GPT":
            loaded_model = "ft:gpt-4o-2024-08-06:personal::AlR6KFIV"
            openai_key = os.getenv("OPENAPI_KEY")
            client = OpenAI(api_key = openai_key)
            defaultMessage = f"You are a factual chatbot which aims to replicate a simulated patient for use in training residents to become psychotherapists."
            defaultMessage += f"Your name is Abe and your age is 50 with the mental illness: Generalized Anxiety Disorder"
            defaultMessage += f"This is a virtual therapy session with a new therapist, however, your personal experiences are the same."
            defaultMessage += f"This is a conversation with a new therapist, who you have not talked with prior, do not refer to prior sessions."
            print(f"{loaded_model} preloaded.")
            return(loaded_model)
        if model=="GPT-Mini":
            loaded_model = "ft:gpt-4o-mini-2024-07-18:personal::AlQaBHUm"
            openai_key = os.getenv("OPENAPI_KEY")
            client = OpenAI(api_key = openai_key)
            defaultMessage = f"You are a factual chatbot which aims to replicate a simulated patient for use in training residents to become psychotherapists."
            defaultMessage += f"Your name is Abe and your age is 50 with the mental illness: Generalized Anxiety Disorder"
            defaultMessage += f"This is a virtual therapy session with a new therapist, however, your personal experiences are the same."
            defaultMessage += f"This is a conversation with a new therapist, who you have not talked with prior, do not refer to prior sessions."
            print(f"{loaded_model} preloaded.")
            return(loaded_model)
        if model=="Gemini":
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

def preload_model():
    global loaded_model
    try:
        data = request.get_json()
        character = data['character']
        model = data['model']
        
        # Load the model and store it in the global variable
        loaded_model = load_ml_model(character,model)
        return jsonify({
            "message": f"Model {loaded_model} preloaded successfully",
            "model": loaded_model
            })
    except Exception as e:
        # Capture and log the exception
        error_message = str(e)
        traceback_str = traceback.format_exc()
        print(f"Error preloading model: {error_message}\n{traceback_str}")
        return jsonify({"error": f"Failed to preload model: {error_message}"}), 500

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
            generatedMessage = completion.choices[0].message.content
        
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
            generatedMessage = response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    if generatedMessage.lower().startswith("patient: "):
        generatedMessage = generatedMessage[len("patient: "):]
    if generatedMessage.lower().startswith("abe: "):
        generatedMessage = generatedMessage[len("abe: "):]
    return(generatedMessage)

def send_message():
    global loaded_model
    try:
        data = request.get_json()
        user_message = data['message']

        print("waiting..")
        print(user_message)
         
        # Check if a model has been loaded
        if not loaded_model:
            raise ValueError("Model not loaded. Please preload a model first.")

        # Pass the user's message to the loaded ML model and get a response
        bot_response = get_ml_response(user_message)
        print(bot_response)
        if bot_response[:4].lower()=="bot:":
            bot_response=bot_response[4:]
        print("its alive ",bot_response)
        return jsonify({"response": bot_response})
    except Exception as e:
        # Capture and log the exception
        error_message = str(e)
        traceback_str = traceback.format_exc()
        print(f"Error processing message: {error_message}\n{traceback_str}")
        return jsonify({"error": f"Failed to process message: {error_message}"}), 500
