# GPT Take the Wheel
Inspired by [gpt-repository-loader](https://github.com/mpoon/gpt-repository-loader/blob/main/gpt_repository_loader.py) and a [comment on the HN thread about it](https://news.ycombinator.com/item?id=35191663). 

This is a CLI script which asks the user what they want, and sends the prompt + the output of `git ls-files` to the GPT-4 API. GPT says which files it wants to see the contents of, and this script sends the contents of those files to the API and asks for a change suggestion. At the moment, this only handles changes that span a single file. 

This can be run via `gpt_assist` or `gpt_take_the_wheel`. With `gpt_assist`, the AI will propose changes and you can review them before applying. In `gpt_take_the_wheel`, the AI will automatically apply changes without waiting for your review, and shows you the `git diff`.


# DANGER
- This will automatically send the content of files in your git repository to the OpenAI API
- If you run with `--auto-overwrite`, or use the `gpt_take_the_wheel` command, this will **automatically overwrite files in your repo** with whatever ChatGPT suggests
- The cost can add up quickly if you use it a lot
- The output will be often wrong, not what you wanted, or nonsense

# Notes / Limitations
- This only works on Unix-y systems at the moment. This is because it runs `git ls-files | xargs ls -l`, to include file sizes with the first API call. It might work about as well without file sizes, but it might work about as well without that
- This requires git, and only works from the root of a repo
- There's no way to continue a conversation at the moment: you write the prompt, send the files, and see the changes proposed

## Usage
### Requirements
To use GPT-Assist, you will need an OpenAI API key. This key should be placed in a file called `.openai_api_key` in the root directory of your repository. Alternatively, you can set the key as an environment variable with the name `OPENAI_API_KEY`.

You'll need access to GPT-4 for this to work well - if you don't have access, you can try to run it with `-m gpt-3.5-turbo`. I haven't had a lot of success with 3.5 but it's probably possible to tweak the prompts and get it to work better.

### Install 
```
pip install .
```

### Run
If you want to be prompted for confirmation
```
gpt_assist
```
If you want to be prompted before overwriting a file, but not before sending stuff to the API:
```
gpt_assist --auto-confirm-send
```
If you want to be prompted before sending stuff to the API, but not before overwriting:
```
gpt_assist --auto-overwrite
```

To not be prompted at all, pass both `--auto-overwrite` and `auto-confirm-send`, or just run:
```
gpt_take_the_wheel
```

## License

GPT-Assist is released under the MIT License.