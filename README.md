Sure! Here is a `README.md` file for your tool:

```markdown
# ChatGPT Code Assistant

This Python console application assists in code analysis and review by generating insights using OpenAI's GPT-4. It scans a specified directory, extracts and formats the contents of relevant files, and then uses the configuration defined in a YAML file to prompt ChatGPT. The results are saved in markdown files.

## Features

- Generates a file tree of a specified directory.
- Extracts and formats contents of relevant files based on project type.
- Configurable via a YAML file for instructions, file types, and excluded directories.
- Automates prompts to ChatGPT and saves responses in specified markdown files.
- Supports project types such as Python and .NET.

## Requirements

- Python 3.6+
- `openai` package
- `markdown2` package
- `python-dotenv` package
- `pyyaml` package

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/chatgpt-code-assistant.git
   cd chatgpt-code-assistant
   ```

2. **Create a `.env` file in the project directory with the following content:**

   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   ROOT_DIR=path_to_your_root_directory (optional)
   OUTPUT_DIR=path_to_your_output_directory (optional)
   PROJECT_TYPE=your_project_type (python or dotnet)
   CONFIG_FILE=path_to_your_config.yml (optional, default is config.yml)
   APP_DESCRIPTION_FILE=path_to_your_app_description_file
   ```

   - `OPENAI_API_KEY`: Your OpenAI API key.
   - `ROOT_DIR`: (Optional) Path to the directory you want to analyze.
   - `OUTPUT_DIR`: (Optional) Path to the directory where you want to save the responses.
   - `PROJECT_TYPE`: (Optional) Your project type (e.g., `python` or `dotnet`).
   - `CONFIG_FILE`: (Optional) Path to your configuration YAML file (default is `config.yml`).
   - `APP_DESCRIPTION_FILE`: Path to the file containing your application description.

3. **Create a `config.yml` file in the project directory with the following content:**

   ```yaml
   instructions:
     - content: "Please analyze the provided code and give a summary."
       output_file: "summary.md"
     - content: "Identify potential improvements in the code."
       output_file: "improvements.md"
     - content: "Highlight any security vulnerabilities."
       output_file: "security_vulnerabilities.md"
   pre:
     - role: system
       content: "You are a helpful assistant."
     - role: user
       content: "This is the initial context message."
   post:
     - role: user
       content: "This is the final context message after the files."
   relevant_file_types:
     python: ['.py', '.md']
     dotnet: ['.cs', '.md', '.json', 'Dockerfile']
   exclude_dirs:
     python: ['venv', '__pycache__']
     dotnet: ['bin', 'obj']
   app_description_file: "path_to_your_app_description_file"
   ```

4. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the script:**

   ```bash
   python main.py
   ```

   - If `ROOT_DIR` and `OUTPUT_DIR` are not set in the `.env` file, you will be prompted to enter them.

2. **The script will:**

   - Create a file tree of the specified directory.
   - Extract and format the contents of relevant files.
   - Include application description and file contents.
   - Prompt ChatGPT with the defined instructions and save the responses in specified markdown files in the output directory.

## Docker Usage

1. **Build the Docker image:**

   ```bash
   docker build -t chatgpt-code-assistant .
   ```

2. **Run the Docker container:**

   ```bash
   docker run -it --rm --name chatgpt-code-assistant-container chatgpt-code-assistant
   ```

## Customization

- **Relevant File Types and Exclude Directories:** Modify the `relevant_file_types` and `exclude_dirs` in `config.yml` to include the file extensions and directories you consider relevant for your project type.
- **Instructions:** Update the `instructions` array in `config.yml` to add or modify the instructions and their corresponding output files.

## Example

```plaintext
.env file:

OPENAI_API_KEY=your_openai_api_key
PROJECT_TYPE=python
APP_DESCRIPTION_FILE=path_to_your_app_description_file

Running the script:

Enter the directory to analyze: /path/to/your/project
Enter the directory to save responses: /path/to/save/responses

Output:

Responses saved in /path/to/save/responses
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements

- [OpenAI](https://www.openai.com/) for the GPT-4 model.
- [Python-Markdown2](https://github.com/trentm/python-markdown2) for the markdown conversion library.
- [python-dotenv](https://github.com/theskumar/python-dotenv) for loading environment variables from a `.env` file.
- [PyYAML](https://pyyaml.org/) for the YAML parser and emitter for Python.
```

Feel free to adjust any sections to better fit your specific project details or preferences.