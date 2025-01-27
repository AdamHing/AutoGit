import ollama
import subprocess
import re
import git
import os



# class automate_assignments:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
    
#     def initiate():
    
#     def auto_git():
    
#     def hand_in():
        



    
    
def get_git_diff():
    try:
        return subprocess.check_output(['git', 'diff', '--cached', '--diff-algorithm=minimal']).decode('utf-8')
    except subprocess.CalledProcessError:
        return "No staged changes found."



def generate_commit_msg():
    
    
    diff = get_git_diff()
    
    if diff != "No staged changes found.":
        response = ollama.chat(model='deepseek-r1:7b',messages=[
            {
                'role': 'system',
                'content': "Generate a git commit message based on the change log of the file. Respond with ONLY the commit message. 30 words maximum. Be specific about what the change did."
            },
            {
                'role': 'user',
                'content': f"Generate a commit message for this diff:\n\n{diff}"
            }
        ])
        return re.sub(r"<think>.*?</think>", "", response['message']['content'], flags=re.DOTALL).strip()
    
    else:
        return "updated nothing."
    
    
    


    
cwd = os.getcwd()
print('cwd',cwd)

repo_path = "D:\Coding\Projects\AutoGit"
files_to_add = ['main.py']

repo = git.Repo() 

repo.index.add(files_to_add) # git add

print(get_git_diff()) # diff
print("============================================================")

response=generate_commit_msg() # get commit message
print(response)
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


