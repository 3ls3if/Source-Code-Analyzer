import re
import os
import torch
from transformers import RobertaTokenizer, RobertaModel
import pickle

# Function to clean JavaScript code
def clean_code(code):
    code = re.sub(r'\/\*[\s\S]*?\*\/', '', code)  # Remove multiline comments
    code = re.sub(r'\/\/.*', '', code)  # Remove single line comments
    code = re.sub(r'#.*', '', code)  # Remove python comments
    code = re.sub(r'\s*\n\s*', '\n', code)  # Remove extra whitespace around newlines
    return code.strip()

# Function to label JavaScript code (0 for safe, 1 for unsafe)
def label_code(snippet):
    unsafe_patterns = {
        'eval': 'Code Injection',                        # Executes code from a string
        'innerHTML': 'Cross-Site Scripting (XSS)',       # Inserts HTML content into an element
        'outerHTML': 'Cross-Site Scripting (XSS)',       # Similar to innerHTML but for the element itself
        'document.write': 'Cross-Site Scripting (XSS)',  # Writes directly to the HTML document
        'setTimeout': 'Potential Code Injection',        # Executes code after a delay
        'setInterval': 'Potential Code Injection',       # Repeatedly executes code at intervals
        'Function': 'Code Injection',                    # Creates new functions from strings
        'location.href': 'Open Redirect',                # Changes the URL of the current page
        'document.location': 'Open Redirect',            # Similar to location.href
        'XMLHttpRequest': 'Sensitive Data Exposure',     # Handles HTTP requests, can be misused
        '<script>': 'Cross-Site Scripting (XSS)',        # Directly injects JavaScript code
        'document.body.innerHTML': 'Cross-Site Scripting (XSS)'  # Sets the HTML content of the body element
    }

    unsafe_lines = []
    for line in snippet.split('\n'):
        for pattern, vuln_type in unsafe_patterns.items():
            if pattern in line:
                unsafe_lines.append((line.strip(), vuln_type))
    return unsafe_lines

# Load pre-trained model and tokenizer
tokenizer = RobertaTokenizer.from_pretrained('microsoft/codebert-base')
model = RobertaModel.from_pretrained('microsoft/codebert-base')

# Get the absolute path of the current script
script_dir = os.path.dirname(__file__)
model_path = os.path.join(script_dir, '../models/javascript_model.pkl')

# Load the trained model from the file
with open(model_path, 'rb') as model_file:
    clf = pickle.load(model_file)

def analyze_code(test_code):
    # Clean the code for embedding
    cleaned_test_code = clean_code(test_code)

    # Identify unsafe lines
    unsafe_lines = label_code(cleaned_test_code)

    # Tokenize and get embeddings for the cleaned test code
    test_inputs = tokenizer([cleaned_test_code], padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        test_outputs = model(**test_inputs)
    test_embeddings = test_outputs.last_hidden_state.mean(dim=1).numpy()

    # Predict with the trained classifier
    prediction = clf.predict(test_embeddings)
    
    return unsafe_lines, prediction
