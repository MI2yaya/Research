import pandas as pd
import os
import json
from openai import OpenAI
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
from io import StringIO
import chardet
import base64

from generateJSON import generateJSON

load_dotenv()

openai_key = os.getenv("OPENAPI_KEY")

df = pd.read_csv(os.path.join('processedData','Manual-BB3-Session-2-Annotated-Transcript-Final.csv'),usecols=["ID","MentalIllness","AgeRange",'ClientText',"TherapistText"])


print(df)
chatGPT4oDefaultMessage = generateJSON(df,"chatgpt",'chatGPT-fine-tune.json')
client = OpenAI(api_key = openai_key)

#client.files.create(file=open("chatGPT-fine-tuning.json", "rb"),purpose="fine-tune")
#client.fine_tuning.jobs.create(training_file="file-C59GMg7EDqlqcvLL5OL6EFgH",model="gpt-4o-mini-2024-07-18")

#show results
with open(os.path.join('results','chatGPT-4o','results.csv'), 'rb') as f:
    base64_encoded_data = f.read()
decoded_data = base64.b64decode(base64_encoded_data)
result = chardet.detect(decoded_data)
encoding = result['encoding']
decoded_text = decoded_data.decode(encoding)
df = pd.read_csv(StringIO(decoded_text))
print(df.tail())


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

