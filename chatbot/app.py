import os
import gradio as gr
import torch
import re
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load tokenizer and model for text generation
model_id = "microsoft/Phi-3-mini-4k-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id, token=os.environ.get('HF_TOKEN'))
model = AutoModelForCausalLM.from_pretrained(model_id, token=os.environ.get('HF_TOKEN'), torch_dtype=torch.bfloat16)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# Function to generate response based on transcribed text
def generate_response(transcription):
    try:
        messages = [
            {"role": "system", "content": "You are a chatbot who always responds in english speak!"},
            {"role": "user", "content": transcription},
        ]

        input_ids = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(device)

        terminators = [
            tokenizer.eos_token_id,
            tokenizer.convert_tokens_to_ids("")
        ]

        outputs = model.generate(
            input_ids,
            max_new_tokens=256,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )

        generated_text = tokenizer.decode(outputs[0][input_ids.shape[-1]:], skip_special_tokens=True)
        return find_last_sentence(generated_text)

    except Exception as e:
        print("Error during response generation:", e)
        return "Response generation error"

# Function to find last sentence in generated text
def find_last_sentence(text):
    sentence_endings = re.finditer(r'[.!?]', text)
    end_positions = [ending.end() for ending in sentence_endings]
    if end_positions:
        return text[:end_positions[-1]]
    return text

# Function to handle text input and generate response
def process_text(text_input):
    try:
        response = generate_response(text_input)
        return "", text_input, response
    except Exception as e:
        print("Error during text processing:", e)
        return "", "Error during text processing", str(e)

# Create Gradio interface
iface = gr.Interface(
    fn=process_text,
    inputs=[gr.Textbox(label="Text Input")],
    outputs=[
        gr.Textbox(label="Processed Audio"),
        gr.Textbox(label="Transcription"),
        gr.Textbox(label="Response")
    ],
    live=False
)

if __name__ == "__main__":
    iface.launch(share=True)
