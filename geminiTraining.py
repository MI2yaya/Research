
import os
from dotenv import load_dotenv
from generateJSON import generateJSON
import vertexai
from vertexai.tuning import sft
from vertexai.generative_models import GenerativeModel, SafetySetting

#https://console.cloud.google.com/welcome/new?walkthrough_id=vertex-pytorch-custom-training&inv=1&invt=AbiN7A&project=gen-lang-client-0291103620
#https://console.cloud.google.com/home/dashboard?inv=1&invt=AbiN7A&walkthrough_id=vertex-pytorch-custom-training&project=gen-lang-client-0291103620
#https://aistudio.google.com/tune

load_dotenv()



#df = pd.read_csv(os.path.join('processedData','Manual-BB3-Session-2-Annotated-Transcript-Final.csv'),usecols=["ID","MentalIllness","AgeRange",'ClientText',"TherapistText"])
#generateJSON(df,"vertex",'gemini-fine-tune')



vertexai.init(project=os.getenv("GOOGLE_PROJECT"),location="us-east1")
'''
sft_tuning_job = sft.train(
    source_model="gemini-1.5-pro-002",
    train_dataset="gs://gemini-fine-tuning-bucket/gemini-fine-tune.jsonl",
    tuned_model_display_name="tuned_gemini_1_5_pro",
)

'''
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
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
