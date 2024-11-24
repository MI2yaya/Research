import pandas as pd
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from sklearn.model_selection import train_test_split
from huggingface_hub import login
from dotenv import load_dotenv
import psutil
import torch


load_dotenv()

print("HF_HOME:", os.getenv("HF_HOME"))
print("PyTorch version:", torch.__version__)
print("CUDA version:", torch.version.cuda)

total_memory = psutil.virtual_memory().total / 1e9 
available_memory = psutil.virtual_memory().available / 1e9 

print(f"Total Memory: {total_memory:.2f} GB")
print(f"Available Memory: {available_memory:.2f} GB")

#torch.cuda.init()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Number of GPUs:", torch.cuda.device_count())
if torch.cuda.is_available():
    total_memory = torch.cuda.get_device_properties(0).total_memory / 1e9  # Convert to GB
    available_memory = torch.cuda.memory_allocated(0) / 1e9  # Allocated memory in GB
    reserved_memory = torch.cuda.memory_reserved(0) / 1e9  # Reserved memory in GB
    
    print(f"Total GPU Memory: {total_memory:.2f} GB")
    print(f"Allocated GPU Memory: {available_memory:.2f} GB")
    print(f"Reserved GPU Memory: {reserved_memory:.2f} GB")
    print("GPU Name:", torch.cuda.get_device_name(0))
else:
    print("CUDA is not available.")

llama_key=os.getenv("LLAMA_KEY")
login(llama_key)



#This is for proof of concept.
#https://huggingface.co/meta-llama/Meta-Llama-3.1-405B
#https://huggingface.co/umd-zhou-lab/claude2-alpaca-7B

print("loading tokenizer")
LlamaTokenizer = AutoTokenizer.from_pretrained("D:/Models/huggingface/hub/models--meta-llama--Llama-3.1-8B/snapshots/11-20-24")
print('loading model')
LlamaModel = AutoModelForCausalLM.from_pretrained(
    "D:/Models/huggingface/hub/models--meta-llama--Llama-3.1-8B/snapshots/11-20-24",
    offload_folder="D:/Offload Cache",
    offload_state_dict=True,
    ignore_mismatched_sizes=True)

print('done')

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