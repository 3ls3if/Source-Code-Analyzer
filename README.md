# Source Code Vulnerability Scanner

## Overview

The `menu.py` script is a command-line utility for analyzing source code files for potential vulnerabilities. It supports multiple programming languages, including Python, PHP, JavaScript, and Java. The script allows users to upload and analyze code files, identifying unsafe lines and providing detailed results.

## Features

- **Multi-language Support**: Analyze code written in Python, PHP, JavaScript, and Java.
- **File Upload**: Use a graphical file dialog to select source code files for analysis.
- **Code Analysis**: Detect and report potential vulnerabilities in the code based on predefined patterns.
- **Result Storage**: Save analysis results to a `results` directory with a formatted filename.
- **Interactive Output**: Display analysis results in the terminal with colored output for better readability.

## Requirements

**Note:** Requires python version 3.10

Ensure you have the necessary Python packages installed. Create a `requirements.txt` file with the following content:

```plaintext
numpy==1.2.2
torch
transformers
scikit-learn==1.2.2
colorama

```

### Install the required packages using pip:

```
pip install -r requirements.txt

pip3 install -r requirements.txt

```

### Usage 

#### 1. Running the Script:

```
python3 menu.py

python menu.py
```

#### 2. Selecting an Option:


- Enter the number corresponding to the language you want to analyze.

#### Uploading and Analyzing:

- A file dialog will open, allowing you to select a code file.
- After selecting a file, the script will analyze it and display the results in the terminal.


#### Viewing Results:

- Results are printed in the terminal and saved to a file in the results directory.
- The result file will be named according to the format filename_results.txt where filename is the name of the uploaded code file (with its extension replaced).


### Example

To analyze a Python file named `example.py`:

1. **Run the script**:

    ```bash
    python menu.py
    ```

2. **Select option `[1]` for Python**.

3. **Choose `example.py` from the file dialog**.

4. **View the analysis results in the terminal and find the results file named `example_py_results.txt` in the `results` directory**.


### Troubleshooting

- Import Errors: Ensure all required packages are installed.
- Missing results Directory: The script will create the results directory if it does not exist. Ensure the script has permission to create directories and files.


### License

- This project is licensed under the MIT License. See the LICENSE file for details.

