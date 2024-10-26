import json
import random

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# List of code examples
code_data = None
with open('code_completion_examples.json', 'r') as f:
    code_data = json.load(f)



def split_code(example):
    prefix = example[0]
    middle = example[1]
    suffix = example[2]

    return {
        "prefix": prefix,
        "middle": middle,
        "suffix": suffix
    }


# Split each example into prefix, middle, and suffix
split_data = [split_code(example) for example in code_data]

# Load the Tiny StarCoder model and tokenizer
checkpoint = "bigcode/tiny_starcoder_py"
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)


# Function to get model completion with Fill-in-the-Middle support
def get_completion_fim(prefix, suffix):
    # Format the input with FIM tokens
    input_text = f"<fim_prefix>{prefix}<fim_suffix>{suffix}<fim_middle>"

    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to(device)
    attention_mask = inputs['attention_mask'].to(device)
    outputs = model.generate(inputs['input_ids'].to(device), attention_mask=attention_mask,
                             max_length=len(inputs['input_ids'][0]) + 10,
                             pad_token_id=tokenizer.eos_token_id)
    completion_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    middle_generated = completion_text[len(prefix) + len(suffix):]

    ######

    return middle_generated.strip()


# Run completions on each example
for i, example in enumerate(split_data):
    prefix = example["prefix"]
    suffix = example["suffix"]
    model_completion = get_completion_fim(prefix, suffix)
    example["model_completion"] = model_completion
    print(f'Processed example number:{i}')

# Save updated dataset with model completions
with open('completed_code_dataset_fim.json', 'w') as f:
    json.dump(split_data, f, indent=4)

print("Dataset with model completions saved as completed_code_dataset_fim.json")
