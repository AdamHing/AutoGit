import ollama
import subprocess
import re
import git
    
def get_git_diff():
    try:
        return subprocess.check_output(['git', 'diff', '--cached', '--diff-algorithm=minimal']).decode('utf-8')
    except subprocess.CalledProcessError:
        return "No staged changes found."


def generate_commit_msg():
    diff = get_git_diff()
    
    if diff != "No staged changes found.":
        response = ollama.chat(model='deepseek-r1:1.5b',keep_alive=0,messages=[
             {
            'role': 'system',
            'content': 'You are a helpful assistant tasked with creating concise and meaningful Git commit messages. Your responses must fit within 15 words and describe the exact nature and purpose of the code changes.'
        },
        {
            'role': 'user',
            'content': f"Analyze the following diff and generate a descriptive Git commit message. Be specific about the change and its impact:\n\n{diff}"
        }
        ])
        
        return re.sub(r"<think>.*?</think>", "", response['message']['content'], flags=re.DOTALL).strip()

    else:
        return "updated nothing."
    
    
    

repo = git.Repo() 

print(get_git_diff()) # diff
print("============================================================")

response=generate_commit_msg() # get commit message
print("commit message: ",response)
repo.index.commit(response) # git commmit -m ""

repo.remote(name='origin').push() # git push
log = repo.git.log() #git log

print(log)



# call back
# program sits in the repo 
# has modes for setup, code, hand-in
#setup: make folder structure, 
#code: git commands
#hand-in: build recipe. manual confirm. zipup and name 
#


