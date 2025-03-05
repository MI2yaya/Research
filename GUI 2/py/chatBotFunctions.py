# chatBotFunctions.py
from dotenv import load_dotenv
from openai import OpenAI
import os
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting
from flask import jsonify, request
import traceback
import pandas as pd

load_dotenv()

# Global variable to store the loaded model
loaded_model = None

def load_csv_transcript(csv_file_path):
    """
    Reads a CSV file and formats the contents into a single text string.
    This text will be used as the default message for the simulated patient.
    """
    transcript = f"Attatched is a transcription of a therapy session as the patient, you are to replicate the behavior of the individual and represent their characteristics. This is to be used as a training tool.\n"
    try:
        # Read the CSV file using pandas (it will automatically handle encoding issues)
        df = pd.read_csv(csv_file_path, encoding='utf-8')  # You can change encoding if necessary
        
        # Check if the expected columns are in the DataFrame
        if 'MentalIllness' in df.columns and 'AgeRange' in df.columns:
            transcript += f"Name: Abe\nMental Illness: {df['MentalIllness'].iloc[0]}\nAge Range: {df['AgeRange'].iloc[0]}\n"
        
        # Iterate through the rows of the DataFrame to build the transcript
        for index, row in df.iterrows():
            client_text = row.get('ClientText', '').strip()
            therapist_text = row.get('TherapistText', '').strip()

            # Add patient and therapist conversation to the transcript
            if client_text:
                transcript += f"Patient: {client_text}\n"
            if therapist_text:
                transcript += f"Therapist: {therapist_text}\n\n"

        return transcript

    except Exception as e:
        print(f"Error reading CSV: {e}")
        return ""


def load_ml_model(character,tuned,model):
    global loaded_model, client, defaultMessage
    model_configs = {
        "Model 1": {
            'true':{
                "GPT": {
                    "loaded_model": "ft:gpt-4o-2024-08-06:personal::AYGKLhoP",
                    "default_message": "You are a factual chatbot which aims to replicate a simulated patient for use in training residents to become psychotherapists. Your name is Abe and your age is 65 with the mental illness: Major Depressive Disorder. This is a virtual therapy session with a new therapist, however, your personal experiences are the same. This is a conversation with a new therapist, do not refer to prior sessions."
                },
                "GPT-Mini": {
                    "loaded_model": "ft:gpt-4o-mini-2024-07-18:personal::AJSd1eeZ",
                    "default_message": "You are a factual chatbot which aims to replicate a simulated patient for use in training residents to become psychotherapists. Your name is Abe and your age is 65 with the mental illness: Major Depressive Disorder. This is a virtual therapy session with a new therapist, however, your personal experiences are the same. This is a conversation with a new therapist, do not refer to prior sessions."
                },
                "Gemini": {
                    "loaded_model": "projects/903507590578/locations/us-east1/endpoints/4254410710097854464",
                    "client_init": lambda: vertexai.init(project=os.getenv("GOOGLE_PROJECT"), location="us-east1"),
                    "conversation_init": lambda: GenerativeModel("projects/903507590578/locations/us-east1/endpoints/4254410710097854464").start_chat()
                }
            },
            'false':{
                "GPT": {
                    "loaded_model": "gpt-4o",
                    "transcript_file": "transcripts/model_1.csv"
                },
                "GPT-Mini": {
                    "loaded_model": "gpt-4o-mini",
                    "transcript_file": "transcripts/model_1.csv"
                },
                "Gemini":{
                    "loaded_model": "FigreThisOut!!!",
                    "transcript_file": "transcripts/model_1.csv"
                }
            }
        },
        "Model 2": {
            'true':{
                "GPT": {
                    "loaded_model": "ft:gpt-4o-2024-08-06:personal::AlR6KFIV",
                    "default_message": "You are a factual chatbot which aims to replicate a simulated patient for use in training residents to become psychotherapists. Your name is Abe and your age is 50 with the mental illness: Generalized Anxiety Disorder. This is a virtual therapy session with a new therapist, however, your personal experiences are the same. This is a conversation with a new therapist, do not refer to prior sessions."
                },
                "GPT-Mini": {
                    "loaded_model": "ft:gpt-4o-mini-2024-07-18:personal::AlQaBHUm",
                    "default_message": "You are a factual chatbot which aims to replicate a simulated patient for use in training residents to become psychotherapists. Your name is Abe and your age is 50 with the mental illness: Generalized Anxiety Disorder. This is a virtual therapy session with a new therapist, however, your personal experiences are the same. This is a conversation with a new therapist, do not refer to prior sessions."
                },
                "Gemini": {
                    "loaded_model": "projects/903507590578/locations/us-east1/endpoints/2611933852246999040",
                    "client_init": lambda: vertexai.init(project=os.getenv("GOOGLE_PROJECT"), location="us-east1"),
                    "conversation_init": lambda: GenerativeModel("projects/903507590578/locations/us-east1/endpoints/2611933852246999040").start_chat()
                }
            },
            'false':{
                "GPT": {
                    "loaded_model": "gpt-4o",
                    "transcript_file": "transcripts/model_2.csv"
                },
                "GPT-Mini": {
                    "loaded_model": "gpt-4o-mini",
                    "transcript_file": "transcripts/model_2.csv"
                },
                "Gemini":{
                    "loaded_model": "FigreThisOut!!!",
                    "transcript_file": "transcripts/model_2.csv"
                }
            }
        }
    }

    # Check if the character and model are valid
    if character in model_configs and tuned in model_configs[character] and model in model_configs[character][tuned]:
        config = model_configs[character][tuned][model]

        # Initialize the model based on the configuration
        loaded_model = config["loaded_model"]
        if "client_init" in config:
            config['init_client']
        elif "GPT" in model or "GPT-Mini" in model:
            client = OpenAI(api_key=os.getenv("OPENAPI_KEY"))
            
        if "conversation_init" in config:
            global conversation_gemini
            conversation_gemini = config["conversation_init"]()


        if "transcript_file" in config:
            # Read the CSV file and set as default_message
            transcript_path = config["transcript_file"]
            defaultMessage = load_csv_transcript(transcript_path)
            print(defaultMessage)
        else:
            # For tuned models, use the predefined default_message
            defaultMessage = config["default_message"]

        print(f"{loaded_model} preloaded.")
        return loaded_model
    else:
        print("Model not found.")
        return ""

def preload_model():
    global loaded_model, model
    print("preloading...")
    try:
        data = request.get_json()
        character = data['character']
        model = data['model']
        tuned = data['tuned']
        
        # Load the model and store it in the global variable
        loaded_model = load_ml_model(character,tuned,model)
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
    
     # Short-circuit to get response based on loaded model type
    if model.startswith("GPT"):
        try:
            completion = client.chat.completions.create(
                model=loaded_model,
                messages=[{"role": "system", 'content': defaultMessage}, {'role': 'user', 'content': user_message}]
            )
            generatedMessage = completion.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
    elif model.startswith("GEMINI"):
        try:
            generation_config = {
                "max_output_tokens": 8192,
                "temperature": 0.5,
            }

            safety_settings = [
                SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=SafetySetting.HarmBlockThreshold.OFF),
                SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=SafetySetting.HarmBlockThreshold.OFF),
                SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=SafetySetting.HarmBlockThreshold.OFF),
                SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=SafetySetting.HarmBlockThreshold.OFF)
            ]
            response = conversation_gemini.send_message(
                content=user_message,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            generatedMessage = response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    else:
        return "Invalid model type."

    
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
