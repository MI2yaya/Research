import pandas as pd
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from sklearn.model_selection import train_test_split
from huggingface_hub import login
from dotenv import load_dotenv
from cosineSimilarity import cosine_similarity
import psutil
import torch

load_dotenv()

print("CUDA_HOME:", os.getenv("CUDA_HOME"))
print("HF_HOME:", os.getenv("HF_HOME"))

total_memory = psutil.virtual_memory().total / 1e9 
available_memory = psutil.virtual_memory().available / 1e9 

print(f"Total Memory: {total_memory:.2f} GB")
print(f"Available Memory: {available_memory:.2f} GB")

#torch.cuda.init()

print("CUDA Available:", torch.cuda.is_available())
print("Number of GPUs:", torch.cuda.device_count())
if torch.cuda.is_available():
    print("GPU Name:", torch.cuda.get_device_name(0))


llama_key=os.getenv("LLAMA_KEY")
login(llama_key)



#This is for proof of concept.
#https://huggingface.co/meta-llama/Meta-Llama-3.1-405B
#https://huggingface.co/umd-zhou-lab/claude2-alpaca-7B



LlamaTokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-405B") 
LlamaModel = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-405B",) 

#test model
while True:
    prompt = input("Msg: ")

    inputs = LlamaTokenizer(prompt, return_tensors="pt").input_ids

    generate_ids = LlamaModel.generate(inputs, max_length=30)
    output = LlamaTokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    print(output)


df = pd.read_csv(os.path.join('processedData','Manual-BB3-Session-2-Annotated-Transcript-Final.csv'),usecols=["ID","MentalIllness","AgeRange",'ClientText',"TherapistText"])

X_train, X_test, y_train, y_test = train_test_split(
    df['TherapistText'],df['ClientText'], test_size=0.2, random_state=42)