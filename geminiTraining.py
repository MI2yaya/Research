import google.generativeai as genai # pip install -q -U google-generativeai
import os
from dotenv import load_dotenv
import pandas as pd
from generateJSON import generateJSON


#https://aistudio.google.com/tune

load_dotenv()

google_key = os.getenv("GOOGLE_KEY")


df = pd.read_csv(os.path.join('processedData','Manual-BB3-Session-2-Annotated-Transcript-Final.csv'),usecols=["ID","MentalIllness","AgeRange",'ClientText',"TherapistText"])
generateJSON(df,"gemini",'gemini-fine-tune.json')

with open('gemini-fine-tune.json') as f:
    json = f.read().splitlines()

print(json)

#genai.configure(api_key=google_key)
