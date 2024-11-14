import pandas as pd
from transformers import GPTNeoForCausalLM, GPT2Tokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from transformers import AdamW
import torch
import os

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


df = pd.read_csv(os.path.join('Manual-BB3-Session-2-Annotated-Transcript.csv'))

print(df)

tokenizer = GPT2Tokenizer.from_pretrained('EleutherAI/gpt-neo-125M')
model = GPTNeoForCausalLM.from_pretrained('EleutherAI/gpt-neo-125M')

model.to(device)
tokenizer.pad_token = tokenizer.eos_token

def tokenize_texts(texts):
    return tokenizer(texts, padding='max_length', truncation=True, max_length=512, return_tensors='pt')

client_texts = df['ClientText'].tolist()
therapist_texts = df['TherapistText'].tolist()

client_tokens = tokenize_texts(client_texts)
therapist_tokens = tokenize_texts(therapist_texts)

assert client_tokens['input_ids'].shape == therapist_tokens['input_ids'].shape, "Tokenized input and target shapes do not match."


class Dataset(torch.utils.data.Dataset):
    def __init__(self, input_ids, attention_masks, labels):
        self.input_ids = input_ids
        self.attention_masks = attention_masks
        self.labels = labels

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return {
            'input_ids': self.input_ids[idx].to(device),
            'attention_mask': self.attention_masks[idx].to(device),
            'labels': self.labels[idx].to(device)
        }
        
dataset = Dataset(client_tokens['input_ids'], client_tokens['attention_mask'], therapist_tokens['input_ids'])

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    eval_dataset=dataset,
)


trainer.train()

def generate_response(therapist_input):
    inputs = tokenizer(therapist_input, return_tensors='pt').to(device)
    output = model.generate(inputs, max_length=100, num_return_sequences=1)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response


therapist_input = "How have you been feeling lately?"
client_response = generate_response(therapist_input)
print(f"Therapist: {therapist_input}")
print(f"Client: {client_response}")
