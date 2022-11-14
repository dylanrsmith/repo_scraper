import os
import git
import shutil
from atlassian import Bitbucket

bitbucket = Bitbucket(
    url="http://localhost:7990",
    username="dylanrsmith",
    password="ATBB8QqnhrB3vr8k8aMvq4hrJdUy56EB4A95",
)
repo = git.Repo

path_from = "https://dylanrsmith@bitbucket.org/dylanrsmith/paho.git"                    # Git link to clone repo from
path_to = "D:/repos/~test"                                                              # Path to initially download repo
new_path = "D:/network-test"                                                            # End location to post repo
project_key = "FEI"
repo_list = bitbucket.repo_list(project_key, limit=25)

# Function to prepend line to file:
def line_prepender(filename, line):
    """
    filename [string]: file to be edited
    line [string]: content to be added
    """
    with open(filename, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip("\r\n") + "\n" + content)


def get_config():
    f = open('config.txt')
    lines = [word for word in f.read().split('\r')]
    for parameter in lines:
        options = [word for word in parameter.split()]
    for i in options:
        print(i)


def clone_fei_repo():
    # Clone remote repository from bitbucket
    repo.clone_from(path_from, path_to)

    # TODO: Open Files and add License Doc to top of each...
    # Filter by files that contain ".cs" or ".h":

    directory = os.scandir(path_to)
    entries = [it.name for it in directory]
    # need_license = [it.name for it in directory if it.endswith(('.cs','.h'))]
    need_license = [it.name for it in directory if not it.endswith(".py")]
    print(entries)
    print(need_license)
    # Move cloned repo to network location
    shutil.move(path_to, new_path)

if __name__ == "__main__":
    print("hello")
    get_config()