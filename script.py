import os
import git
import shutil
from atlassian import Bitbucket

#TODO read these config variables from a config file

bitbucket = Bitbucket(
    url="http://localhost:7990",
    username="dylanrsmith",
    password="ATBB8QqnhrB3vr8k8aMvq4hrJdUy56EB4A95",
)
repo = git.Repo

git_link = "https://dylanrsmith@bitbucket.org/dylanrsmith/paho.git"                    # Git link to clone repo from
path_to = "D:/repos/~test"                                                             # Path to initially download repo
final_destination = "D:/network-test"                                                  # End location to post repo
project_key = "FEI"
repo_list = bitbucket.repo_list(project_key, limit=25)


# Get repo
repo.clone_from(git_link, path_to)

# Add license to correct files
with open("license.txt", "r+") as l:
    license = l.read()

files_arr = []
for root,dirs,files in os.walk(path_to, topdown=False):
    for name in files:
        files_arr.append(os.path.join(root,name))

    for file in files_arr: 
        if file.endswith(".py") or file.endswith(".txt"):
            with open(file, "r+") as f:
                content = f.read()
                f.seek(0,0)
                f.write(license + "\n\n" + content)

# Move edited files to final destination
shutil.move(path_to, final_destination)
        