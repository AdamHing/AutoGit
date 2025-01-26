import ollama
import subprocess
import re


def get_git_diff():
    try:
        return subprocess.check_output(['git', 'diff', '--cached', '--diff-algorithm=minimal']).decode('utf-8')
    except subprocess.CalledProcessError:
        return "No staged changes found."


print(get_git_diff())
print("============================================================")

def generate_commit_msg():
    diff = get_git_diff()
    response = ollama.chat(model='deepseek-r1:8b',messages=[
        {
            'role': 'system',
            'content': "Generate a git commit message. Respond with ONLY the message. 15 words maximum."
        },
        {
            'role': 'user',
            'content': f"Generate a commit message for this diff:\n\n{diff}"
        }
    ])

    return response['message']['content']


response=generate_commit_msg()
response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
print(response)
