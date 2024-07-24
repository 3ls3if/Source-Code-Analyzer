import re
import os
import torch
from transformers import RobertaTokenizer, RobertaModel
import pickle

# Function to clean PHP code
def clean_code(code):
    code = re.sub(r'\/\*[\s\S]*?\*\/', '', code)  # Remove multiline comments
    code = re.sub(r'\/\/.*', '', code)  # Remove single line comments
    code = re.sub(r'#.*', '', code)  # Remove shell comments (if any)
    code = re.sub(r'\s*\n\s*', '\n', code)  # Remove extra whitespace around newlines
    return code.strip()

# Function to label PHP code (0 for safe, 1 for unsafe)
def label_code(snippet):
    unsafe_patterns = {
        'eval(': 'Dynamic Code Execution',               # Avoid dynamic evaluation
        'exec(': 'Command Injection',                     # Command execution
        'shell_exec(': 'Command Injection',               # Command execution
        'system(': 'Command Injection',                   # Command execution
        'popen(': 'Command Injection',                    # Command execution
        'fopen(': 'File Handling',                        # File handling
        'file_get_contents(': 'File Handling',            # File handling
        'include(': 'File Inclusion',                     # File inclusion
        'require(': 'File Inclusion',                     # File inclusion
        'include_once(': 'File Inclusion',                # File inclusion
        'require_once(': 'File Inclusion',                # File inclusion
        'mysqli_query(': 'SQL Injection',                 # SQL query
        'PDO->query(': 'SQL Injection',                   # SQL query
        'unserialize(': 'Deserialization Vulnerability',  # Unserialization
        'base64_decode(': 'Potential Data Exposure',      # Data encoding/decoding
        'preg_replace(': 'Regular Expression Injection',  # Regular expression
        'assert(': 'Dynamic Code Execution',              # Assert function
        'create_function(': 'Dynamic Code Execution'      # Create function
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
model_path = os.path.join(script_dir, '../models/php_model.pkl')

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

