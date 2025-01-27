import ollama
import subprocess
import re
import git



repo =git.Repo("D:\Coding\Projects\AutoGit")
repo.index.add(['main.py'])

def get_git_diff():
    try:
        return subprocess.check_output(['git', 'diff', '--cached', '--diff-algorithm=minimal']).decode('utf-8')
    except subprocess.CalledProcessError:
        return "No staged changes found."

print(get_git_diff())
print("============================================================")

def generate_commit_msg():
    diff = get_git_diff()
    
    if diff != "No staged changes found.":
        response = ollama.chat(model='deepseek-r1:8b',messages=[
            {
                'role': 'system',
                'content': "Generate a git commit message based on the change log of the file. Respond with ONLY the commit message. 30 words maximum. Outline the changes made."
            },
            {
                'role': 'user',
                'content': f"Generate a commit message for this diff:\n\n{diff}"
            }
        ])

        return response['message']['content']
    
    else:
        return "updated nothing."


response=generate_commit_msg()
response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
print(response)

repo.index.commit(response)
origin = repo.remote(name='origin')
origin.push()
log = repo.git.log()
print(log)