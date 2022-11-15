import os
import git
import shutil
from time import sleep
# from atlassian import Bitbucket


# TODO read these config variables from a config file

repo = git.Repo
git_link = "https://dylanrsmith@bitbucket.org/dylanrsmith/paho.git"                    # Git link to clone repo from
path_to = "D:\\repos\\~test"                                                           # Path to initially download repo
final_destination = "C:\\Temp"                                                         # End location to post repo
project_key = "FEI"


# Get repo
# NOTE: path_to needs to be empty
repo.clone_from(git_link, path_to, config="http.proxy=farft01:fardnc01@proxy-us.cnhind.com:8080")

# Add license to correct files
with open("license.txt", "r+") as l:
    license = l.read()

for root,dirs,files in os.walk(path_to, topdown=True):
    for file in files:
        if file.endswith(".py") or file.endswith(".txt"):
            with open(os.path.join(root,file), "r+") as f:
                content = f.read()
                f.seek(0,0)
                f.write(license + "\n\n" + content)

# Move edited files to final destination
try:
    shutil.move(path_to, final_destination)
except PermissionError:
#    print("idx file?????")
    print(PermissionError)