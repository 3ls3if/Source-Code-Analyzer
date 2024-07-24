#!/usr/bin/env python
# coding: utf-8

import re
import json
import os
import numpy as np
import torch
from transformers import RobertaTokenizer, RobertaModel
from sklearn.ensemble import RandomForestClassifier
import pickle

# Function to clean PHP code
def clean_code(code):
    code = re.sub(r'\/\*[\s\S]*?\*\/', '', code)  # Remove multiline comments
    code = re.sub(r'\/\/.*', '', code)  # Remove single line comments
    code = re.sub(r'#.*', '', code)  # Remove shell comments (if any)
    code = re.sub(r'\s*\n\s*', '\n', code)  # Remove extra whitespace around newlines
    return code.strip()

# Load pre-trained model and tokenizer
tokenizer = RobertaTokenizer.from_pretrained('microsoft/codebert-base')
model = RobertaModel.from_pretrained('microsoft/codebert-base')

# Get the absolute path of the current script
script_dir = os.path.dirname(__file__)
json_file_path = os.path.join(script_dir, '../datasets/php.json')

# Load existing preprocessed dataset
with open(json_file_path, 'r') as f:
    data = json.load(f)

# Tokenize and get embeddings for the code snippets
inputs = tokenizer([clean_code(d['code']) for d in data], padding=True, truncation=True, return_tensors='pt')
with torch.no_grad():
    outputs = model(**inputs)
embeddings = outputs.last_hidden_state.mean(dim=1).numpy()

# Create labels
labels = np.array([d['label'] for d in data])

# Train a simple classifier
clf = RandomForestClassifier()
clf.fit(embeddings, labels)

# Save the trained model to a file
model_path = os.path.join(script_dir, '../models/php_model.pkl')
with open(model_path, 'wb') as model_file:
    pickle.dump(clf, model_file)

print("Training complete. Model saved to:", model_path)
