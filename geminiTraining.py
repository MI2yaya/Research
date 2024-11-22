import google.generativeai as genai 
import os
from dotenv import load_dotenv
import pandas as pd
from generateJSON import generateJSON
import time


#https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/tuning/supervised_finetuning_using_gemini.ipynb - ...????? uses a diff library
#https://aistudio.google.com/tune

load_dotenv()

google_key = os.getenv("GOOGLE_KEY")
print(google_key)

df = pd.read_csv(os.path.join('processedData','Manual-BB3-Session-2-Annotated-Transcript-Final.csv'),usecols=["ID","MentalIllness","AgeRange",'ClientText',"TherapistText"])
generateJSON(df,"gemini",'gemini-fine-tune')

with open('gemini-fine-tune.json') as f:
    training_data = f.read().splitlines()[0]

#print(training_data)

#raise ValueError

genai.configure(api_key=google_key)

operation = genai.create_tuned_model(
    # You can use a tuned model here too. Set `source_model="tunedModels/..."`
    source_model="models/gemini-1.5-pro-002",
    display_name="Dummy Model",
    training_data='gemini-fine-tune.json'
)

for status in operation.wait_bar():
    time.sleep(10)

result = operation.result()
print(result)
# # You can plot the loss curve with:
# snapshots = pd.DataFrame(result.tuning_task.snapshots)
# sns.lineplot(data=snapshots, x='epoch', y='mean_loss')

model = genai.GenerativeModel(model_name=result.name)
result = model.generate_content("Hello, tell me a little about yourself")
print(result.text)