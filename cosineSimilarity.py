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
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
import time


tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

random.seed(42)

def getEmbeddings(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
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




df = pd.read_csv(os.path.join('processedData','Manual-BB3-Session-2-Annotated-Transcript-Final.csv'),usecols=["ID","MentalIllness","AgeRange",'ClientText',"TherapistText"])

load_dotenv()

#chatgpt

def testing(model):
    #setup
    if model.lower()=="chatgpt":
        openai_key = os.getenv("OPENAPI_KEY")
        client = OpenAI(api_key = openai_key)
        chatGPT4oDefaultMessage = generateJSON(df,"chatgpt",'chatGPT-fine-tune')

    if model.lower()=="gemini":
        vertexai.init(project=os.getenv("GOOGLE_PROJECT"),location="us-east1")
        gemini = GenerativeModel(
            "projects/903507590578/locations/us-east1/endpoints/4254410710097854464"
        )
        generation_config = {
            "max_output_tokens": 8192,
            "temperature": 1
        }
        chat = gemini.start_chat(response_validation=False)
        
    cosSimList=[]
    softCosSimList=[]

    for _ in range(50):
        error=False
        random_index = random.randint(0, len(df) - 2)
        msg = df['TherapistText'].iloc[random_index]
        output = df['ClientText'].iloc[random_index+1]

        print(f"\nInput info:\nModel: {model}\nSelected Message: {msg}\nExpected Output: {output}\n")

        #model dependent
        if model.lower()=='chatgpt':
            completion = client.chat.completions.create(
                model = "ft:gpt-4o-2024-08-06:personal::AYGKLhoP",
                messages=[
                    {"role":"system",'content':chatGPT4oDefaultMessage},
                    {'role':'user','content':msg}
                ]
            )
            modelOutput = completion.choices[0].message.content
        #add gemini, llama
        if model.lower()=='gemini':
            try:
                response = chat.send_message(
                    content=msg,
                    generation_config = generation_config
                )
                modelOutput = response.text
            except IndexError:
                print("err")
                error=True
            except Exception as e:
                error=True
                time.sleep(5)
        if not error:
            print("Response:", modelOutput)
            cosSim,softCosSim=metrics(modelOutput,output)
            cosSimList.append(cosSim)
            softCosSimList.append(softCosSim)
        else:
            _ -=1
        time.sleep(1)



    print(f"\nOutput:\nAverage Cosine Similarity: {sum(cosSimList)/len(cosSimList)}\nAverage Soft Cosine Similarity: {sum(softCosSimList)/len(softCosSimList)}")
    
testing("gemini")