from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from datasets import Dataset
from sklearn.metrics import accuracy_score
import pandas as pd
import os
import torch
from dotenv import load_dotenv
from huggingface_hub import login

load_dotenv()

llama_key = os.getenv("LLAMA_KEY")
login(llama_key)

# Load dataset
df = pd.read_csv(
    os.path.join('processedData', 'Manual-BB3-Session-10-Annotated-Transcript-Final.csv'),
    usecols=["ID", "MentalIllness", "AgeRange", 'ClientText', "TherapistText"]
)
df['input_text'] = df['TherapistText'] + " </s> " + df['ClientText']
df.dropna(subset=['TherapistText', 'ClientText'], inplace=True)

# Convert to Dataset
dataset = Dataset.from_pandas(df[['input_text']])
train_test_split = dataset.train_test_split(test_size=0.1)

# Load tokenizer and model
mother_series = "meta-llama"
model_name = "Llama-3.2-1B"
combined_name = mother_series+"/"+model_name
tokenizer = AutoTokenizer.from_pretrained(combined_name)
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': tokenizer.eos_token})
model = AutoModelForCausalLM.from_pretrained(
    combined_name,
    ignore_mismatched_sizes=True
)
model.gradient_checkpointing_enable()

# Tokenize dataset
def tokenize_function(examples):
    tokenized = tokenizer(
        examples['input_text'],
        padding="max_length",
        truncation=True,
        max_length=128
    )
    tokenized["labels"] = tokenized["input_ids"]
    return tokenized

tokenized_datasets = train_test_split.map(tokenize_function, batched=True)
tokenized_datasets = tokenized_datasets.remove_columns(["input_text"])

# Define training arguments
training_args = TrainingArguments(
    output_dir=f'results/{model_name}-T2',
    num_train_epochs=3,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=4,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    fp16=True
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['test'],
    tokenizer=tokenizer
)

# Train model
trainer.train()

# Save model
model.save_pretrained(f"results/{model_name}-T2")
tokenizer.save_pretrained(f"results/{model_name}-T2")
