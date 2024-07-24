import re
import os
import torch
from transformers import RobertaTokenizer, RobertaModel
import pickle

# Function to clean Python code
def clean_code(code):
    code = re.sub(r'\/\*[\s\S]*?\*\/', '', code)  # Remove multiline comments
    code = re.sub(r'\/\/.*', '', code)  # Remove single line comments
    code = re.sub(r'#.*', '', code)  # Remove python comments
    code = re.sub(r'\s*\n\s*', '\n', code)  # Remove extra whitespace around newlines
    return code.strip()

# Function to label Python code (0 for safe, 1 for unsafe)
def label_code(snippet):
    unsafe_patterns = {
        'eval(': 'Dynamic Code Execution',               # Avoid dynamic evaluation
        'exec(': 'Dynamic Code Execution',               # Avoid dynamic execution
        'subprocess.call(': 'Command Injection',          # Avoid executing external commands
        'subprocess.Popen(': 'Command Injection',         # Avoid opening subprocesses with dynamic input
        'input(': 'Unvalidated Input',                    # Avoid unsafe handling of user inputs
        'open(': 'File Handling',                         # Be cautious with file handling
        'os.system(': 'Command Injection',                # Avoid system calls
        'pickle.load(': 'Deserialization Vulnerability',  # Deserialization of potentially unsafe data
        'pickle.dumps(': 'Serialization Vulnerability',  # Serialization of potentially unsafe data
        'import(': 'Dynamic Import',                     # Potentially unsafe module import
        'os.getenv(': 'Environment Variable Exposure',    # Exposure through environment variables
        'glob.glob(': 'File Exposure',                    # File path exposure
        'shutil.copy(': 'File Handling',                  # Copying files, potentially unsafe
        'shutil.move(': 'File Handling',                  # Moving files, potentially unsafe
        'sqlite3.connect(': 'SQL Injection',              # Connection to SQLite with potential SQL injection
        'pymysql.connect(': 'SQL Injection',              # Connection to MySQL with potential SQL injection
        'psycopg2.connect(': 'SQL Injection',             # Connection to PostgreSQL with potential SQL injection
        'requests.get(': 'Potential Data Exposure',       # HTTP GET requests, potentially exposing data
        'requests.post(': 'Potential Data Exposure'       # HTTP POST requests, potentially exposing data
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
model_path = os.path.join(script_dir, '../models/python_model.pkl')

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
