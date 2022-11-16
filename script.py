import os
import git
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

# TODO proxy not working 
bucket_repos = bitbucket.get_repositories('FEI')

repo = git.Repo
repo_name = "uts2018"
git_link = f"https://{username}:{password}@bitbucket.org/fargoengineeringinc/{repo_name}.git"
path_to = "D:\\repos\\~test"                                                                        # Path to initially download repo
final_destination = "C:\\Temp"                                                                      # End location to post repo
project_key = "FEI"

# Get repo
# NOTE: path_to needs to be empty
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

# Move edited files to final destination
try:
    shutil.move(path_to, final_destination)
except PermissionError:
    print("[WinError5] Access is denied: .git\idx file")
except:
    print("Other Error :(")