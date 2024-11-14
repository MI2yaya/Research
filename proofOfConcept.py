import pandas as pd
import os
import json
from openai import OpenAI
from transformers import AutoModelForCausalLM, AutoTokenizer
from sklearn.model_selection import train_test_split
from huggingface_hub import login
from dotenv import load_dotenv
from io import StringIO
import chardet
import base64

load_dotenv()

llama_key=os.getenv("LLAMA_KEY")
openai_key = os.getenv("OPENAPI_KEY")

login(llama_key)

print("HF_HOME:", os.getenv("HF_HOME"))

#This is for proof of concept.
#https://huggingface.co/meta-llama/Meta-Llama-3.1-405B
#https://huggingface.co/umd-zhou-lab/claude2-alpaca-7B


df = pd.read_csv(os.path.join('processedData','Manual-BB3-Session-2-Annotated-Transcript-Final.csv'),usecols=["ID","MentalIllness","AgeRange",'ClientText',"TherapistText"])

X_train, X_test, y_train, y_test = train_test_split(
    df['TherapistText'],df['ClientText'], test_size=0.2, random_state=42)



LlamaTokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-405B") #- errr download model
LlamaModel = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-405B") #- download model pt. 2.

#ClaudeTokenizer = AutoTokenizer.from_pretrained("umd-zhou-lab/claude2-alpaca-7B")
#ClaudeModel = AutoModelForCausalLM.from_pretrained("umd-zhou-lab/claude2-alpaca-7B")


print(df)
def generateJSON(df):
    
    with open("fine-tuning.json", "w") as outfile:
        outfile.write("")
    
    defaultMessage = f"You are a factual chatbot which aims to replicate a simulated patient for use in training residents to become psychotherapists."
    defaultMessage+=f"Your name is Bot1 and your age is between {df['AgeRange'][0]} with the mental illness: {df['MentalIllness'][0]}"
    
    for index in range(len(df)-1):
        
        messageList=[]
        tempMessageDict = {"role": "system", "content": defaultMessage}
        messageList.append(tempMessageDict)
    
        
        tempMessageDict = {"role": "user", "content": df['TherapistText'][index]}
        if df['TherapistText'][index]=="X":
            tempMessageDict['weight']=0
        messageList.append(tempMessageDict)
        tempMessageDict = {"role": "assistant", "content": df['ClientText'][index+1]}
        if df['ClientText'][index+1]=="X":
            tempMessageDict['weight']=0
        messageList.append(tempMessageDict)
        
        openaiMessage = {"messages":messageList}
        with open("fine-tuning.json", "a") as outfile: 
            outfile.write(json.dumps(openaiMessage) + "\n")
    return(defaultMessage)
chatGPT4oDefaultMessage = generateJSON(df)

client = OpenAI(api_key = openai_key)

#client.files.create(file=open("fine-tuning.json", "rb"),purpose="fine-tune")
#client.fine_tuning.jobs.create(training_file="file-C59GMg7EDqlqcvLL5OL6EFgH",model="gpt-4o-mini-2024-07-18")


with open('step_metrics.csv', 'rb') as f:
    base64_encoded_data = f.read()
decoded_data = base64.b64decode(base64_encoded_data)
result = chardet.detect(decoded_data)
encoding = result['encoding']
decoded_text = decoded_data.decode(encoding)
df = pd.read_csv(StringIO(decoded_text))
print(df.tail())

def cosine_sim(df,message):
    print("not done")

raise ValueError
while True:
    userMessage = input("Enter Message: ")
    completion = client.chat.completions.create(
        model = "ft:gpt-4o-mini-2024-07-18:personal::AJSd1eeZ",
        messages=[
            {"role":"system",'content':chatGPT4oDefaultMessage},
            {'role':'user','content':userMessage}
        ]
    )
    print(completion.choices[0].message)

raise ValueError

'''

prompt = "Hey, are you conscious? Can you talk to me?"

inputs = LlamaTokenizer(prompt, return_tensors="pt").input_ids


generate_ids = LlamaModel.generate(inputs, max_length=30)
output = LlamaTokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
print(output)

'''