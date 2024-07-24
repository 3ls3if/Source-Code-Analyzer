#!/usr/bin/env python
# coding: utf-8

import sys
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from colorama import init, Fore, Style
import platform

# Initialize colorama
init(autoreset=True)

# Add the languages directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'languages'))

def get_analyze_code_function(language):
    try:
        if language == 'python':
            from python import analyze_code
        elif language == 'php':
            from php import analyze_code
        elif language == 'javascript':
            from javascript import analyze_code
        elif language == 'java':
            from java import analyze_code
        else:
            raise ValueError("Unsupported language")
        return analyze_code
    except ImportError as e:
        print(f"{Fore.RED}Import error: {e}")
        raise
    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
        raise

def save_results(file_path, results):
    # Ensure the results directory exists
    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    os.makedirs(results_dir, exist_ok=True)

    # Create a results file with the same name as the uploaded file
    base_name = os.path.basename(file_path)
    result_file_name = f"{base_name.replace('.', '_')}_results.txt"
    result_file_path = os.path.join(results_dir, result_file_name)

    with open(result_file_path, 'w') as result_file:
        result_file.write(results)

    return result_file_path

def upload_and_analyze(language):
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    file_types = {
        'python': [("Python Files", "*.py")],
        'php': [("PHP Files", "*.php")],
        'javascript': [("JavaScript Files", "*.js")],
        'java': [("Java Files", "*.java")]
    }

    file_path = filedialog.askopenfilename(
        title=f"Select a {language.capitalize()} Script",
        filetypes=file_types[language]
    )

    if file_path:
        try:
            # Read the contents of the uploaded file
            with open(file_path, 'r') as file:
                code = file.read()

            # Get the appropriate analyze_code function
            analyze_code = get_analyze_code_function(language)

            # Analyze the code snippet
            unsafe_lines, prediction = analyze_code(code)

            # Prepare results
            result_message = f"{Fore.YELLOW}Unsafe Lines of Code with Vulnerability Types:{Style.RESET_ALL}\n"
            if not unsafe_lines:
                result_message += f"\n{Fore.GREEN}No vulnerabilities found.{Style.RESET_ALL}\n"
            else:
                for line, vuln_type in unsafe_lines:
                    result_message += f"{Fore.RED}{line} - {vuln_type}{Style.RESET_ALL}\n"

            # Save results to file
            result_file_path = save_results(file_path, result_message)

            # Display results
            print(result_message)
            print(f"\n{Fore.CYAN}Results have been saved to {result_file_path}{Style.RESET_ALL}")

            input(f"\n{Fore.BLUE}[*] Press Enter to continue...{Style.RESET_ALL}\n")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading the file: {e}")

def main():
    while True:
        if platform.system() == 'Windows':
            os.system('cls')  # Command for Windows
        else:
            os.system('clear')  # Command for Unix-like systems
        
        
        print(f"{Fore.GREEN}*****************************************")
        print("*    Source Code Vulnerability Scanner  *")
        print("*****************************************{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}[1] Upload and Analyze Python Script{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[2] Upload and Analyze PHP Script{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[3] Upload and Analyze JavaScript Script{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[4] Upload and Analyze Java Script{Style.RESET_ALL}")
        print(f"{Fore.RED}[5] Exit{Style.RESET_ALL}")
        print(f"{Fore.GREEN}*****************************************{Style.RESET_ALL}")

        choice = input(f"\n{Fore.BLUE}[+] Enter your choice (1-5): {Style.RESET_ALL}")

        if choice == '5':
            print(f"{Fore.RED}[-] Exiting the program...{Style.RESET_ALL}")
            break

        language_map = {
            '1': 'python',
            '2': 'php',
            '3': 'javascript',
            '4': 'java'
        }

        if choice in language_map:
            upload_and_analyze(language_map[choice])
        else:
            print(f"\n{Fore.RED}[!] Invalid choice. Please enter a number between 1 and 5.{Style.RESET_ALL}\n")
            input(f"\n{Fore.BLUE}[*] Press Enter to continue...{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()
