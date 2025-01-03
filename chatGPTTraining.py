import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv
from io import StringIO
import chardet
import base64
from generateJSON import generateJSON

#https://platform.openai.com/chat-completions

load_dotenv()

openai_key = os.getenv("OPENAPI_KEY")

df = pd.read_csv(os.path.join('processedData','Manual-BB3-Session-10-Annotated-Transcript-Final.csv'),usecols=["ID","MentalIllness","AgeRange",'ClientText',"TherapistText"])


print(df)
chatGPT4oDefaultMessage = generateJSON(df,"chatgpt",'chatGPT-fine-tune-2')
client = OpenAI(api_key = openai_key)

#client.files.create(file=open("chatGPT-fine-tune-2.json", "rb"),purpose="fine-tune")

client.fine_tuning.jobs.create(training_file="file-VMd8q5DZi7VG9WmFFnbZia",model="gpt-4o-2024-08-06")
raise ValueError
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

