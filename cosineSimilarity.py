import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI
from generateJSON import generateJSON
import random
import vertexai
from vertexai.generative_models import GenerativeModel
import time
from transformers import AutoTokenizer, AutoModelForCausalLM

bertTokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bertModel = BertModel.from_pretrained('bert-base-uncased')

random.seed(42)

def getEmbeddings(text):
    inputs = bertTokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = bertModel(**inputs)
    return outputs.last_hidden_state.squeeze(0).numpy()

def metrics(modelOutput,dfMessage):

    modelEmbedding = getEmbeddings(modelOutput)
    dfMessageEmbedding = getEmbeddings(dfMessage)
    
    modelEmbedding_cls = modelEmbedding[0]
    dfMessageEmbedding_cls = dfMessageEmbedding[0]
    
    cosineSim = cosine_similarity([modelEmbedding_cls], [dfMessageEmbedding_cls])[0][0]
    
    matrix = cosine_similarity(modelEmbedding,dfMessageEmbedding)
    softCosineSim = np.sum(matrix) / (modelEmbedding.shape[0] * dfMessageEmbedding.shape[0])
    
    print(f"Cosine Similarity: {cosineSim}")
    print(f"Soft Cosine Similarity: {softCosineSim}")
    
    return(cosineSim,softCosineSim)


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

file_name='Manual-BB3-Session-10-Annotated-Transcript-Final.csv'

df = pd.read_csv(os.path.join('processedData',file_name),usecols=["ID","MentalIllness","AgeRange",'ClientText',"TherapistText"])

load_dotenv()

#chatgpt

def testing(model,tuned):
    #setup
    if model.lower()=="chatgpt":
        openai_key = os.getenv("OPENAPI_KEY")
        client = OpenAI(api_key = openai_key)
        if tuned:
            chatGPT4oDefaultMessage = generateJSON(df,"chatgpt",'chatGPT-fine-tune')
        else:
            print("using untuned")
            chatGPT4oDefaultMessage = load_csv_transcript(f"processedData\{file_name}")

    if model.lower()=="gemini":
        if tuned:
            vertexai.init(project=os.getenv("GOOGLE_PROJECT"),location="us-east1")
            gemini = GenerativeModel(
                "projects/903507590578/locations/us-east1/endpoints/2611933852246999040"
            )
            generation_config = {
                "max_output_tokens": 8192,
                "temperature": 1
            }
            geminiChat = gemini.start_chat(response_validation=False)
        else:
            print("using untuned Gemini")
            vertexai.init(project=os.getenv("GOOGLE_PROJECT"),location="us-east1",api_endpoint="us-east1-aiplatform.googleapis.com")
            gemini = GenerativeModel(
                "gemini-1.5-pro-002",
            )
            geminiDefaultMessage=load_csv_transcript(f"processedData\{file_name}")
            generation_config = {
                "max_output_tokens": 8192,
                "temperature": 1
            }
            geminiChat = gemini.start_chat(response_validation=False)
        
    if model.lower()=='llama':
        model_name = "Llama-3.2-1B-T2"
        model_path = f"results/{model_name}"

        tokenizer = AutoTokenizer.from_pretrained(model_path)
        llamaModel = AutoModelForCausalLM.from_pretrained(model_path)

        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
    cosSimList=[]
    softCosSimList=[]

    for _ in range(50):
        print(f"Indexxxxxx {_+1}")
        error=False
        random_index = random.randint(0, len(df) - 2)
        msg = df['TherapistText'].iloc[random_index]
        output = df['ClientText'].iloc[random_index+1]

        print(f"\nInput info:\nModel: {model}\nSelected Message: {msg}\nExpected Output: {output}\n")

        #model dependent
        if model.lower()=='chatgpt':
            if tuned:
                completion = client.chat.completions.create(
                    model = "ft:gpt-4o-2024-08-06:personal::AlR6KFIV",
                    messages=[
                        {"role":"system",'content':chatGPT4oDefaultMessage},
                        {'role':'user','content':msg}
                    ]
                )
            else:
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", 'content': chatGPT4oDefaultMessage}, {'role':'user','content':msg}]
                )
                
            modelOutput = completion.choices[0].message.content
        if model.lower()=='gemini':
            if tuned:
                try:
                    response = geminiChat.send_message(
                        msg,
                        generation_config = generation_config
                    )
                    modelOutput = response.text
                except IndexError:
                    print("err")
                    error=True
                except Exception as e:
                    print(e)
                    error=True
                    time.sleep(15)
            else:
                try:
                    response = geminiChat.send_message(
                        geminiDefaultMessage+'\n'+msg,
                        generation_config = generation_config
                    )
                    modelOutput = response.text
                except IndexError:
                    print("err")
                    error=True
                except Exception as e:
                    print(e)
                    error=True
                    time.sleep(15)
        if model.lower()=='llama':
            try:
                inputs = tokenizer(msg,return_tensors="pt",padding=True,truncation=True)
                response = llamaModel.generate(
                    input_ids = inputs["input_ids"],
                    attention_mask=inputs["attention_mask"],
                    max_length=100
                )
                modelOutput = tokenizer.decode(response[0], skip_special_tokens=True)
            except Exception as e:
                print(f"ERRRR: {e}")
                
        if not error:
            print("Response:", modelOutput)
            cosSim,softCosSim=metrics(modelOutput,output)
            cosSimList.append(cosSim)
            softCosSimList.append(softCosSim)
        else:
            _ -=1
        time.sleep(1)



    print(f"\nOutput:\nAverage Cosine Similarity: {sum(cosSimList)/len(cosSimList)}\nAverage Soft Cosine Similarity: {sum(softCosSimList)/len(softCosSimList)}")
    
testing("gemini",False)