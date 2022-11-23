import os
import git
import stat
import shutil
from time import sleep
from atlassian import Bitbucket

# TODO read these config variables from a config file
proxy_setting = 'http://farft01:fardnc01@proxy-us.cnhind.com:8080'
bitbucket = Bitbucket(
    url="http://localhost:7990",
    username="dylanrsmith",
    password="ATBB8QqnhrB3vr8k8aMvq4hrJdUy56EB4A95",
)
bitbucket._session.proxies = {'http':proxy_setting,'https':proxy_setting}

username="dylanrsmith"
password="ATBB8QqnhrB3vr8k8aMvq4hrJdUy56EB4A95"
repo = git.Repo

repo_name = "uts2018"
#git_link = f"https://{username}:{password}@bitbucket.org/fargoengineeringinc/{repo_name}.git"
path_to = "D:\repos\~test"                                                                        # Path to initially download repo
final_destination = "C:\Temp"                                                                      # End location to post repo
project_key = "FEI"

repo_names = []
staging_spots = []
final_spots = []

def rmtree(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWRITE)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)    

def get_config():
    lines = []
    options = []
    count = 0
    f = open("config.txt")
    lines = [word for word in f.read().split("\r")]
    for line in lines:
        options = [word for word in line.split()]
    for option in options:
        count+=1
        if count == 1:
            repo_names.append(option)
        elif count == 2:
            staging_spots.append(option)
        elif count == 3:
            final_spots.append(option)
            count = 0

    print("REPOS:")
    print(repo_names)
    print("STAGES:")
    print(staging_spots)
    print("FINALS:")
    print(final_spots)
    # END

def clone(repo_name,path_to,final_destination):
    # Get repo
    # NOTE: path_to needs to be empty
    try:
        shutil.rmtree(path_to, ignore_errors=True)
    except FileNotFoundError:
        print("Stage already empty")
    # Proxy works for this
    git_link = f"https://{username}:{password}@bitbucket.org/fargoengineeringinc/{repo_name}.git"
    repo.clone_from(git_link, path_to, config="http.proxy=farft01:fardnc01@proxy-us.cnhind.com:8080")
    # Add license to correct files
    with open("license.txt", "r+") as l:
        license = l.read()

    for root,dirs,files in os.walk(path_to, topdown=True):
        for file in files:
            if file.endswith(".cs"):
                with open(os.path.join(root,file), "r+", encoding="utf8") as f:
                    content = f.read()
                    f.seek(0,0)
                    f.write(license + "\n\n" + content)

    shutil.rmtree(final_destination, ignore_errors=True)
    shutil.move(path_to, final_destination, copy_function=shutil.copytree)

if __name__ == '__main__':
    get_config()
    for i in range(len(repo_names)):
        clone(repo_names[i],staging_spots[i],final_spots[i])
    print("DONE")