import re
import os
import torch
from transformers import RobertaTokenizer, RobertaModel
import pickle

# Function to clean Java code
def clean_code(code):
    code = re.sub(r'\/\*[\s\S]*?\*\/', '', code)  # Remove multiline comments
    code = re.sub(r'\/\/.*', '', code)  # Remove single line comments
    code = re.sub(r'\s*\n\s*', '\n', code)  # Remove extra whitespace around newlines
    return code.strip()

# Function to label Java code (0 for safe, 1 for unsafe)
def label_code(snippet):
    unsafe_patterns = {
        'Runtime.getRuntime().exec': 'Command Execution',
        'ProcessBuilder': 'Command Execution',
        'FileOutputStream': 'File I/O',
        'FileInputStream': 'File I/O',
        'BufferedWriter': 'File I/O',
        'BufferedReader': 'File I/O',
        'ObjectInputStream': 'Deserialization',
        'ObjectOutputStream': 'Serialization',
        'setAccessible': 'Reflection',
        'getDeclaredField': 'Reflection',
        'getDeclaredMethod': 'Reflection',
        'URLClassLoader': 'URL Class Loading',
        'URLConnection': 'Network Communication',
        'Socket': 'Network Communication',
        'ServerSocket': 'Network Communication',
        'printStackTrace': 'Information Disclosure',
        'getSystemProperty': 'Information Disclosure',
        'System.loadLibrary': 'Library Loading',
        'Class.forName': 'Dynamic Class Loading',
        'Method.invoke': 'Reflection',
        'ObjectInputStream.readObject': 'Deserialization',
        'DriverManager.getConnection': 'SQL Injection',
        'Statement.execute': 'SQL Injection',
        'ResultSet.getString': 'SQL Injection',
        'MessageDigest.getInstance("MD5")': 'Insecure Hashing',
        'MessageDigest.getInstance("SHA1")': 'Insecure Hashing',
        'Random': 'Insecure Randomness',
        'Math.random': 'Insecure Randomness',
        'Cipher.getInstance("DES")': 'Insecure Encryption',
        'Cipher.getInstance("Blowfish")': 'Insecure Encryption',
        'SSLContext': 'SSL Context',
        'TrustManager': 'SSL Trust Management',
        'HostnameVerifier': 'SSL Hostname Verification',
        'new File': 'File Creation',
        'XStream': 'XML Serialization',
        'JavaSerializer': 'Java Serialization',
        'System.out.println': 'Information Disclosure'
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
model_path = os.path.join(script_dir, '../models/java_model.pkl')

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
