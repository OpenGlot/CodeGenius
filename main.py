import os
import yaml
from openai import OpenAI
import markdown2
from dotenv import load_dotenv

print("Packages are installed correctly.")

# Load environment variables from .env file
load_dotenv()

# OpenAI API key and other configurations from .env file
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ROOT_DIR = os.getenv('ROOT_DIR')
OUTPUT_DIR = os.getenv('OUTPUT_DIR')
PROJECT_TYPE = os.getenv('PROJECT_TYPE', 'dotnet')
CONFIG_FILE = os.getenv('CONFIG_FILE', 'config.yml')

# Function to load configuration
def load_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Load language-specific configuration based on project type
def load_language_config(config_file, project_type):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    language_config = config.get('languages', {}).get(project_type, {})
    return language_config

# Load configurations
config = load_config(CONFIG_FILE)
language_config = load_language_config('config.lang.yml', PROJECT_TYPE)

# Set relevant file types, exclude directories, and other settings
RELEVANT_FILE_TYPES = language_config.get('relevant_file_types', [])
EXCLUDE_DIRS = language_config.get('exclude_dirs', [])
APP_DESCRIPTION_FILE = os.getenv('APP_DESCRIPTION_FILE', config.get('app_description_file'))

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

client = OpenAI(api_key=OPENAI_API_KEY)

# Function to create file tree
def create_file_tree(root_dir):
    file_tree = {}
    for root, dirs, files in os.walk(root_dir):
        # Exclude specified directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if any(file.endswith(ext) for ext in RELEVANT_FILE_TYPES):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    relative_path = os.path.relpath(file_path, root_dir)
                    file_tree[relative_path] = content
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return file_tree

# Function to format file contents
def format_file_contents(file_tree):
    formatted_contents = ""
    for filename, contents in file_tree.items():
        formatted_contents += f"{filename}: {{StartOfFileMarker}}\n{contents}\n{{EndOfFileMarker}}\n\n"
    return formatted_contents

# Function to prompt ChatGPT and save responses
def prompt_chatgpt(file_tree, app_description, config, language_config):
    responses = {}
    instructions = config['instructions']
    pre_messages = language_config.get('pre_messages', []) +  config['pre'] 
    post_messages = config['post']
    messages = []

    # Add pre-messages to messages
    messages.extend(pre_messages)

    for filename, contents in file_tree.items():
        messages.append({
            "role": "user",
            "content": f"File: {filename}\n{contents}"
        })

    messages.extend(post_messages)

    messages.append({
        "role": "user",
        "content": f"App Description: {app_description}"
    })

    for instruction in instructions:
        if not instruction.get('enabled', True):
            continue
        
        output_file = instruction['output_file']

        overwrite = instruction.get('overwrite', False)
        exists = os.path.exists(os.path.join(OUTPUT_DIR, output_file))
        if not overwrite and exists:
            print(f"Skipping {output_file} as overwrite is set to False and the file already exists.")
            continue

        messages.append({
            "role": "user",
            "content": instruction['content']
        })

        print(f"Prompting: {instruction['content']}.")

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        responses[output_file] = response.choices[0].message.content.strip()
    
    return responses

# Function to save responses in markdown files
def save_responses(responses, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename, response in responses.items():
        md_filename = os.path.join(output_dir, filename.replace(os.sep, '_'))
        with open(md_filename, 'w', encoding="utf-8") as f:
            f.write(response)

def main():
    global ROOT_DIR, OUTPUT_DIR

    if not ROOT_DIR:
        ROOT_DIR = input("Enter the directory to analyze: ")
    if not OUTPUT_DIR:
        OUTPUT_DIR = input("Enter the directory to save responses: ")

    # Read application description from file
    if not APP_DESCRIPTION_FILE:
        raise ValueError("APP_DESCRIPTION_FILE is not set in the environment variables.")
        
    try:
        with open(APP_DESCRIPTION_FILE, 'r') as f:
            app_description = f.read()
    except Exception as e:
        raise ValueError(f"Error reading APP_DESCRIPTION_FILE: {e}")

    # Create file tree
    file_tree = create_file_tree(ROOT_DIR)

    # Prompt ChatGPT and get responses
    responses = prompt_chatgpt(file_tree, app_description, config, language_config)

    # Save responses in markdown files
    save_responses(responses, OUTPUT_DIR)

    print(f"Responses saved in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()