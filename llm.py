# llm.py
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# --- Choose your model ---
# You can switch 'flan-t5-small' to 'flan-t5-base' for better quality
MODEL_NAME = "google/flan-t5-large"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def summarize_text(prompt: str, max_length: int = 256) -> str:
    """
    Generate a concise summary using local Flan-T5 model.
    """
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(device)
    output_ids = model.generate(
        **inputs,
        max_new_tokens=max_length,
        do_sample=True,
        temperature=0.7,
        top_p=0.9
    )
    summary = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return summary.strip()

 

