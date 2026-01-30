import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel

# Global variables for the model, loaded once
MODEL_NAME = "microsoft/codebert-base-mlm"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)
model.eval()

# Check for GPU and move model if available (crucial for performance)
if torch.cuda.is_available():
    model.to("cuda")
    print("CodeBERT loaded onto GPU (CUDA).")
else:
    print("CodeBERT loaded onto CPU.")

def embed_text(texts, batch_size=8):
    """
    Generates CodeBERT embeddings for a list of text strings (code chunks).
    """
    embs = []
    device = "cuda" if torch.cuda.is_available() else "cpu"

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        # Tokenize the batch
        enc = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=512)
        
        input_ids = enc["input_ids"].to(device)
        attention_mask = enc["attention_mask"].to(device)
        
        with torch.no_grad():
            # Get the output from the CodeBERT model
            out = model(input_ids=input_ids, attention_mask=attention_mask)
        
        last_hidden = out.last_hidden_state
        
        # Calculate mean pooling across tokens, accounting for padding
        mask = attention_mask.unsqueeze(-1).expand(last_hidden.size()).float()
        summed = (last_hidden * mask).sum(1)
        counts = mask.sum(1)
        pooled = (summed / counts.clamp(min=1e-9)).cpu().numpy()
        embs.append(pooled)
        
    return np.vstack(embs).astype("float32")
