# GPT Take the Wheel (GPT-Assist)
This is a Python script that uses OpenAI's GPT-4 API to complete user goals and modify files within a specified software repository. The user interface is a command line tool that facilitates interaction between the user and the AI.

There are two modes: `gpt_assist` and `gpt_take_the_wheel`. In `gpt_assist`, the AI will propose changes and you can review them before applying. In `gpt_take_the_wheel`, the AI will automatically apply changes without waiting for your review.

## Warnings

As the AI is powerful but not infallible, please exercise caution while using these modes. Always review the proposed changes before applying them, especially in `gpt_take_the_wheel` mode.

## API Key

To use GPT-Assist, you will need an OpenAI API key. This key should be placed in a file called `.openai_api_key` in the root directory of your repository. Alternatively, you can set the key as an environment variable with the name `OPENAI_API_KEY`.

## Usage

### Install 
```
pip install .
```

### Run
GPT-Assist - asks for confirmation before sending data to the API, and before overwriting any files.
```
gpt_assist
```
GPT Take the Wheel - doesn't ask for confirmation, 

After starting the script, you will be prompted to input your goal or task. Make sure to follow the correct format for the program to understand your request. The tool will then guide you through the process of modifying the necessary files.

### Command line options

You can use the following command line options:

- `--auto-overwrite`: Automatically overwrite files with the changes proposed by GPT-Assist.
- `--auto-confirm-send`: Automatically confirm sending messages and files to the OpenAI API.

The `gpt_take_the_wheel` script just passes in both of these flags for you.

## License

GPT-Assist is released under the MIT License.