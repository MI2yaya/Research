from transformers import AutoTokenizer, TFAutoModelForCausalLM,AutoConfig
import os

TF_ENABLE_ONEDNN_OPTS=0

checkpoint = 'model-0'
model_dir = os.path.join("results",checkpoint)

tokenizer = AutoTokenizer.from_pretrained(os.path.join(model_dir,'tokenizer'))
model = TFAutoModelForCausalLM.from_pretrained(os.path.join(model_dir,'model'))
config = AutoConfig.from_pretrained(os.path.join(model_dir,'model'))

max_length = config.max_position_embeddings

model.config.pad_token_id = model.config.eos_token_id

def generate_response(input_text):
    inputs = tokenizer(input_text, return_tensors='tf', padding=True, truncation=True, max_length=max_length)
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']
    print(inputs)
    output = model.generate(
        input_ids,
        attention_mask = attention_mask,
        max_length=max_length,
        num_return_sequences=1,
        temperature=1,
        do_sample = True  
    )
    print(output)

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

while True:
    therapist_input = input("\nEnter text: ")
    client_response = generate_response(therapist_input)
    print(f"Therapist: {therapist_input}")
    print(f"Client: {client_response}")
