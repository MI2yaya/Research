
import os
from dotenv import load_dotenv
from generateJSON import generateJSON
import vertexai
from vertexai.tuning import sft
from vertexai.generative_models import GenerativeModel, SafetySetting
import pandas as pd
from sklearn.model_selection import train_test_split
from google.cloud import storage

#https://console.cloud.google.com/welcome/new?walkthrough_id=vertex-pytorch-custom-training&inv=1&invt=AbiN7A&project=gen-lang-client-0291103620
#https://console.cloud.google.com/home/dashboard?inv=1&invt=AbiN7A&walkthrough_id=vertex-pytorch-custom-training&project=gen-lang-client-0291103620
#https://aistudio.google.com/tune

load_dotenv()

def upload(bucket_name, source_file_name, destination_blob_name):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    # Create a blob (file in the bucket) and upload the file
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

df = pd.read_csv(os.path.join('processedData','Manual-BB3-Session-2-Annotated-Transcript-Final.csv'),usecols=["ID","MentalIllness","AgeRange",'ClientText',"TherapistText"])

train_df, eval_df = train_test_split(df, test_size=0.2, random_state=42)  # 80-20 split
train_df = train_df.reset_index(drop=True)
eval_df = eval_df.reset_index(drop=True)
'''
generateJSON(train_df, "vertex", "gemini-fine-tune-train")
generateJSON(eval_df, "vertex", "gemini-fine-tune-eval")
generateJSON(df, "vertex", "gemini-fine-tune-all)
upload(
    bucket_name="gemini-fine-tuning-bucket",
    source_file_name="gemini-fine-tune-train.jsonl",
    destination_blob_name="gemini-fine-tune-train.jsonl"
)
upload(
    bucket_name="gemini-fine-tuning-bucket",
    source_file_name="gemini-fine-tune-eval.jsonl",
    destination_blob_name="gemini-fine-tune-eval.jsonl"
)


generateJSON(df, "vertex", "gemini-fine-tune-all")
upload(
    bucket_name="gemini-fine-tuning-bucket",
    source_file_name="gemini-fine-tune-all.jsonl",
    destination_blob_name="gemini-fine-tune-all.jsonl"
)
vertexai.init(project=os.getenv("GOOGLE_PROJECT"),location="us-east1")

sft_tuning_job = sft.train(
    source_model="gemini-1.5-pro-002",
    train_dataset="gs://gemini-fine-tuning-bucket/gemini-fine-tune-train.jsonl",
    validation_dataset="gs://gemini-fine-tuning-bucket/gemini-fine-tune-eval.jsonl",
    tuned_model_display_name="tuned_gemini_1_5_pro_5"
)
'''
vertexai.init(project=os.getenv("GOOGLE_PROJECT"),location="us-east1")
sft_tuning_job = sft.train(
    source_model="gemini-1.5-pro-002",
    train_dataset="gs://gemini-fine-tuning-bucket/gemini-fine-tune-all.jsonl",
    tuned_model_display_name="tuned_gemini_1_5_pro_8",
    learning_rate_multiplier=2.0
)

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

'''

model = GenerativeModel("projects/903507590578/locations/us-east1/endpoints/427617664228130816")




chat = model.start_chat()

response = chat.send_message(content="Hello, world!")
print("Response:", response.text)

while True:
    response = chat.send_message(
            content=input("enter msg"),
            generation_config = generation_config,
            safety_settings=safety_settings,
        )

    # Print the response
    print("Response:", response.text)
'''