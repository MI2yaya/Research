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

    cosSimList=[]
    softCosSimList=[]

    for _ in range(50):
        random_index = random.randint(0, len(df) - 2)
        msg = df['TherapistText'].iloc[random_index]
        output = df['ClientText'].iloc[random_index+1]

        print(f"\nInput info:\nModel: {model}\nMessage: {msg}\nExpected Output: {output}\n")

        #model dependent
        if model.lower()=='chatgpt':
            completion = client.chat.completions.create(
                model = "ft:gpt-4o-mini-2024-07-18:personal::AJSd1eeZ",
                messages=[
                    {"role":"system",'content':chatGPT4oDefaultMessage},
                    {'role':'user','content':msg}
                ]
            )
            modelOutput = completion.choices[0].message.content
        #add gemini, llama




        cosSim,softCosSim=metrics(modelOutput,output)
        cosSimList.append(cosSim)
        softCosSimList.append(softCosSim)

    print(f"\nOutput:\nAverage Cosine Similarity: {sum(cosSimList)/len(cosSimList)}\nAverage Soft Cosine Similarity: {sum(softCosSimList)/len(softCosSimList)}")
    
testing("chatgpt")