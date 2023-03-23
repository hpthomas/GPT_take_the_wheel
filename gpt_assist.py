import openai
import subprocess
import json
import os
import argparse

def check_api_key_dotfile():
    if os.path.exists(".openai_api_key"):
        with open(".openai_api_key", "r") as keyfile:
            return keyfile.read().strip()
    return None

def set_api_key():
    api_key = os.environ.get("OPENAI_API_KEY") or check_api_key_dotfile()

    if not api_key:
        print("OPENAI_API_KEY not found in env var or .openai_api_key file.")
        exit(1)

    openai.api_key = api_key

def git_clean_state():
    uncommitted = subprocess.getoutput("git status --porcelain")
    return len(uncommitted.strip()) == 0

def system(msg):
    return {"role": "system", "content": msg}
def user(msg):
    return {"role": "user", "content": msg}
def assistant(msg):
    return {"role": "assistant", "content": msg}

BASE_MESSAGE = "You are an AI Programming Assistant. Your responses will be parsed by software, so you must follow the exact format requested. Be very careful not to deviate from the requested format."

START_CONVERSATION_PROMPT = """
Your goal is to complete the following user request:
{user_request}

These are the contents of the repository:
{repo_contents}

Which files would you like to request?
You must respond with only the file names, separated by whitespace.
If you do not need any files, please respond with only whitespace.
Be very careful to respond exactly as described. Do not include any comments - only the requested files.
"""

REQUEST_CHANGES_PROMPT = """
Here are the contents of the requested files:
{file_contents}

You must propose changes to exactly one file. 
Include only the file name, and the contents of the file.
Your response must be in the following format:
file_name.txt
< full new contents of the file you want to change >
"""

def repo_contents():
    return subprocess.getoutput("git ls-files | xargs ls -l")

class Conversation:
    def __init__(self, auto_overwrite=False, auto_confirm_send=False, base_message=BASE_MESSAGE, model="gpt-4"):
        self.model = model
        self.auto_overwrite = auto_overwrite
        self.auto_confirm_send = auto_confirm_send
        self.messages = [system(base_message)]
        self.total_tokens = 0
        
    def overwrite_file(self, file_name, changes):
        if file_name not in repo_contents():
            file_path = os.path.abspath(file_name)
            current_dir = os.path.abspath(os.getcwd())
            if not file_path.startswith(current_dir):
                print(f"{file_name} is not within working dir - will not write to this location.")
                return

            print(f"Will save new file {file_name}.")
        else:
            print(f"Will overwrite {file_name}")

        if self.auto_overwrite:
            with open(file_name, 'w') as f:
                f.write(changes)
            os.system('git diff')
            print(f"{file_name} has been overwritten with the proposed changes.")
        else:
            print(f"Proposed changes for {file_name}:\n{changes}")
            should_overwrite = input("Overwrite? Press type 'y' to continue.\n")
            if should_overwrite.strip().lower() not in ['y']:
                print(f"{file_name} has not been overwritten.")
            else:
                with open(file_name, 'w') as f:
                    f.write(changes)
                print(f"{file_name} has been overwritten with the proposed changes.")

    def confirm_or_abort(self):
        print(f"You have used {self.total_tokens} tokens in this session.")
        if self.auto_confirm_send:
            return

        val = input("Continue? Press Enter or type 'y' to continue, 'n' to exit: ")
        if val.strip().lower() not in ['', 'y']:
            exit(0)

    def chat(self):
        raw = json.dumps(self.messages).encode('utf-8')
        print(f"Going to send {len(raw)} bytes (about {len(raw) // 4} tokens) to OpenAI API")
        self.confirm_or_abort()

        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )
        self.total_tokens += completion['usage']['prompt_tokens'] + completion['usage']['completion_tokens']

        result_text = completion.choices[0].message.content
        self.messages.append(assistant(result_text))
        return result_text

    def remove_backticks(self, text):
        while text.startswith('```') and text.endswith('```'):
            text = text[3:-3]
        return text

    def file_contents(self, f):
        file_path = os.path.abspath(f)
        current_dir = os.path.abspath(os.getcwd())

        if not file_path.startswith(current_dir):
            print(f"{file_path} is not within the current working directory.")
            contents = f"GPT API not authorized to access {f}."
        else:
            print(f'GPT API is requesting {f}')
            if self.auto_confirm_send:
                contents = open(f).read()
            else:
                allow = input("Allow? Press Enter or type 'y' to continue.\n")
                if allow.strip().lower() not in ['', 'y']:
                    contents = "User has not authorized {f} to be sent to GPT API"
                    contents += input("Provide a reason:\n")
                else:
                    contents = open(f).read()
        return f"==BEGIN {f}==\n{contents}\n==END {f}=="

    def run(self, user_request):
        if self.auto_overwrite and not git_clean_state():
            print("You cannot start a conversation with --auto-overwrite on and uncommitted changes.")
            return

        prompt = START_CONVERSATION_PROMPT.format(user_request=user_request, repo_contents=repo_contents())
        self.messages.append(user(prompt))
        files_to_send = self.chat()

        filenames = files_to_send.split()
        file_data = '\n'.join(self.file_contents(filename) for filename in filenames)
        prompt = REQUEST_CHANGES_PROMPT.format(file_contents=file_data)
        self.messages.append(user(prompt))
        response = self.chat()

        file_name = response.split('\n')[0]
        new_file_contents = '\n'.join(response.split('\n')[1:])
        new_file_contents = self.remove_backticks(new_file_contents)
        self.overwrite_file(file_name, new_file_contents)

def main():
    set_api_key()
    parser = argparse.ArgumentParser(description="Run GPT Assistant")
    parser.add_argument("--auto-overwrite", "-a", help="Automatically overwrite files with changes", action="store_true")
    parser.add_argument("--auto-confirm-send", "-s", help="Automatically confirm sending ", action="store_true")
    args = parser.parse_args()
    conversation = Conversation(auto_overwrite=args.auto_overwrite, auto_confirm_send=args.auto_confirm_send, model="gpt-4")
    prompt = input("What do you want to do?\n")
    conversation.run(prompt)

def take_the_wheel():
    set_api_key()
    conversation = Conversation(auto_overwrite=True, auto_confirm_send=True, model="gpt-4")
    prompt = input("What do you want to do?\n")
    conversation.run(prompt)

if __name__ == "__main__":
    main()