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

git_link = "https://dylanrsmith@bitbucket.org/dylanrsmith/paho.git"  # Git link to clone repo from
path_to = "D:/repos/~test"  # Path to initially download repo
new_path = "D:/network-test"  # End location to post repo
project_key = "FEI"
repo_list = bitbucket.repo_list(project_key, limit=25)

# Function to prepend line to file:
def line_prepender(filename, line):
    """
    filename [string]: file to be edited
    line [string]: content to be added

    need to filter by file type
    only prepend to .cs and .h
    """
    for file in os.listdir(path_to):
        if file.endswith(".py") or file.endswith(".txt"):  # Filter by file type

            # with open(filename, "r+") as f:                                             # Open file and write text
            with open(file, "r+") as f:
                content = f.read()
                f.seek(0, 0)
                f.write(line.rstrip("\r\n") + "\n" + content)


def write_license():
    files_arr = []
    for root, dirs, files in os.walk(path_to, topdown=False):
        for name in files:
            files_arr.append(os.path.join(root, name))
    for file in files_arr:
        if file.endswith(".py") or file.endswith(".txt"):  # Filter by file type
            with open(file, "r+") as f:
                content = f.read()
                f.seek(0, 0)
                # f.write(line.rstrip("\r\n") + "\n" + content)                           # line is content to write
                f.write("LICENSE#322224222" + "\n" + content)


def get_config():
    """
    first step
    """
    f = open("config.txt")
    l = open("license.txt")
    license = l.read()
    lines = [word for word in f.read().split("\r")]
    for parameter in lines:
        options = [word for word in parameter.split()]
    for i in options:  # Assign config variables
        print(i)

    return license


def clone_fei_repo():
    # Clone remote repository from bitbucket
    repo.clone_from(git_link, path_to)

    # TODO: Open Files and add License Doc to top of each...
    # Filter by files that contain ".cs" or ".h":

    directory = os.scandir(path_to)
    entries = [it.name for it in directory]
    # need_license = [it.name for it in directory if it.endswith(('.cs','.h'))]
    # need_license = [it.name for it in directory if not it.endswith(".py")]
    print(entries)
    # print(need_license)

    # Move cloned repo to network location
    shutil.move(path_to, new_path)


if __name__ == "__main__":
    print("hello")
    license = get_config()
    line_prepender(path_to, license)
