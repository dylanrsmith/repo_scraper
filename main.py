"""
    Still need to try to only overwrite repos in final destination,
    IF AND ONLY IF they are older than the newly cloned repo.
"""
import os
import git
import stat
import shutil
from datetime import datetime
from atlassian import Bitbucket

# Bitbucket-python
# TODO read these config variables from a config file
proxy_setting1 = "http://farft01:fardnc01@proxy-us.cnhind.com:8080"
proxy_setting2 = "https://farft01:fardnc01@proxy-us.cnhind.com:8080"
basic_auth = ("dylanrsmith", "ATBB8QqnhrB3vr8k8aMvq4hrJdUy56EB4A95")
bitbucket = Bitbucket(
    url="http://localhost:7990",
    username="dylanrsmith",
    password="ATBB8QqnhrB3vr8k8aMvq4hrJdUy56EB4A95",
)
bitbucket._session.proxies = {"http": proxy_setting1, "https": proxy_setting2}


############
# python-git
username = "dylanrsmith"
password = "ATBB8QqnhrB3vr8k8aMvq4hrJdUy56EB4A95"
repo = git.Repo()
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
    try:
        os.rmdir(top)
    except FileNotFoundError:
        pass


def change_permission(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWRITE)


def get_config():
    lines = []
    options = []
    count = 0
    f = open("config.txt")
    lines = [word for word in f.read().split("\r")]
    for line in lines:
        options = [word for word in line.split()]
    for option in options:
        count += 1
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


def clone(repo_name, path_to, final_destination):
    # NOTE: path_to needs to be an empty directory
    # Delete directory if it exists
    try:
        rmtree(path_to)
        rmtree(final_destination)
    except FileNotFoundError:
        print("Stage already empty")
    # Proxy works for this
    # NOTE repo_name must belong to fargoengineeringinc workspace
    git_link = f"https://{username}:{password}@bitbucket.org/fargoengineeringinc/{repo_name}.git"
    cloned_repo = repo.clone_from(
        git_link, path_to, config="http.proxy=farft01:fardnc01@proxy-us.cnhind.com:8080"
    )

    # Append license to correct files
    with open("license.txt", "r") as l:
        license = l.read()
    for root, dirs, files in os.walk(path_to, topdown=True):
        for file in files:
            if file.endswith(".cs"):
                with open(os.path.join(root, file), "r", encoding="utf-8-sig") as f:
                    try:
                        content = f.read()
                    except UnicodeDecodeError:
                        continue
                with open(os.path.join(root, file), "wb") as f:
                    f.seek(0, 0)
                    new_content = (license + "\n\n" + format(content)).encode("utf-8")
                    f.write(new_content)

    rmtree(final_destination)
    change_permission(path_to)
    shutil.move(path_to, final_destination)


# Main Function
if __name__ == "__main__":
    start = datetime.now()
    get_config()

    for i in range(len(repo_names)):
        if os.path.exists(final_spots[i]) == False:
            clone(repo_names[i], staging_spots[i], final_spots[i])
        else:
            print("Path already exists: " + final_spots[i])

    end = datetime.now()
    time = end - start
    print("DONE @ " + str(time))
