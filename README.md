# GPT Take the Wheel
Inspired by [gpt-repository-loader](https://github.com/mpoon/gpt-repository-loader/blob/main/gpt_repository_loader.py) and a [comment on the HN thread about it](https://news.ycombinator.com/item?id=35191663). 

This is a CLI script which asks the user what they want, and sends the prompt + the output of `git ls-files` to the GPT-4 API. GPT says which files it wants to see the contents of, and this script sends the contents of those files to the API and asks for a change suggestion. At the moment, this only handles changes that span a single file. 

This can be run via `gpt_assist` or `gpt_take_the_wheel`. With `gpt_assist`, the AI will propose changes and you can review them before applying. In `gpt_take_the_wheel`, the AI will automatically apply changes without waiting for your review, and shows you the `git diff`.

This requires git, and can only work from the root of a git repository. 

# DANGER
- This will automatically send the content of files in your git repository to the OpenAI API
- If you run with `--auto-overwrite`, or use the `gpt_take_the_wheel` command, this will **automatically overwrite files in your repo** with whatever ChatGPT suggests
- The cost can add up quickly if you use it a lot
- The output will be often wrong, not what you wanted, or nonsense

## Usage
### Requirements
To use GPT-Assist, you will need an OpenAI API key. This key should be placed in a file called `.openai_api_key` in the root directory of your repository. Alternatively, you can set the key as an environment variable with the name `OPENAI_API_KEY`.

You'll need access to GPT-4 for this to work well - if you don't have access, you can try to run it with `-m gpt-3.5-turbo`. I haven't had a lot of success with 3.5 but it's probably possible to tweak the prompts and get it to work better.

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