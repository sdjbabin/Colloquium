import gradio as gr
from transformers import pipeline
import torch
import langid

# Initialize the translation pipeline
translator = pipeline(task="translation", model="facebook/nllb-200-distilled-600M", torch_dtype=torch.bfloat16)
torch.backends.cuda.enable_mem_efficient_sdp(False)
torch.backends.cuda.enable_flash_sdp(False)

# Function to detect language
def detect_language(text):
    language, _ = langid.classify(text)
    return language

# Function to translate text to English using MarianMT
def translate_to_english(text, src_lang):
    translated_text = list((translator(text, src_lang="ben_Beng", tgt_lang="eng_Latn")[0]).values())[0]
    return translated_text

# Function to translate text from English to target language using MarianMT
def translate_from_english(text, tgt_lang):
    translated_text = list((translator(text, src_lang="eng_Latn", tgt_lang="ben_Beng", max_length=500)[0]).values())[0]
    return translated_text

# Function to generate response using the HuggingFaceH4/zephyr-7b-beta model
def generate_response(prompt):
    pipe = pipeline("text-generation", model="microsoft/Phi-3-mini-4k-instruct", torch_dtype=torch.bfloat16, device_map="auto")
    messages = [
        {
            "role": "",
            "content": "",
        },
        {"role": "user", "content": prompt},
    ]
    chat_prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(chat_prompt, max_new_tokens=512, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    return outputs[0]["generated_text"]

# Gradio interface function
def gradio_interface(user_input):
    detected_lang = detect_language(user_input)

    # Translate to English if not already in English
    if detected_lang != 'en':
        translated_input = translate_to_english(user_input, detected_lang)
    else:
        translated_input = user_input

    # Generate response in English
    response_in_english = generate_response(translated_input)

    # Translate response back to detected language if needed
    if detected_lang != 'en':
        response_in_detected_lang = translate_from_english(response_in_english, detected_lang)
        return detected_lang, translated_input, response_in_english, response_in_detected_lang
    else:
        return detected_lang, translated_input, response_in_english, response_in_english

# Creating the Gradio interface
interface = gr.Interface(
    fn=gradio_interface,
    inputs=gr.Textbox(lines=2, placeholder="Enter your prompt..."),
    outputs=[
        gr.Textbox(label="Detected Language"),
        gr.Textbox(label="Translated Input"),
        gr.Textbox(label="Response in English"),
        gr.Textbox(label="Response in Detected Language"),
    ],
    title="Language Translation and Response Generator",
    description="This application detects the language of the input text, translates it to English, generates a response, and then translates the response back to the original language."
)

# Launch the Gradio app
interface.launch()
