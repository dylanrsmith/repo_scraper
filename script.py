import os
import git
import shutil
from atlassian import Bitbucket
from time import sleep

#TODO read these config variables from a config file


# Connect to rogue network
# os.system(f'''cmd /c "netsh wlan connect name={"CNHAGAP"}"''')
# os.system(f'''cmd /c "netsh wlan show profiles"''')
# os.system(f'''cmd /c "netsh wlan connect name="CNHAGAP" interface="wi-fi"''')
# sleep(10)


bitbucket = Bitbucket(
    url="http://localhost:7990",
    username="dylanrsmith",
    password="ATBB8QqnhrB3vr8k8aMvq4hrJdUy56EB4A95",
)
repo = git.Repo

git_link = "https://dylanrsmith@bitbucket.org/dylanrsmith/paho.git"                    # Git link to clone repo from
path_to = "D:\\repos\\~test"                                                           # Path to initially download repo
final_destination = "C:\\Temp"                                                         # End location to post repo
project_key = "FEI"
repo_list = bitbucket.repo_list(project_key, limit=25)

# os.rmdir(path_to)
# os.rmdir(final_destination)

# Get repo
repo.clone_from(git_link, path_to, config="http.proxy=farft01:fardnc01@proxy-us.cnhind.com:8080")

# Add license to correct files
with open("license.txt", "r+") as l:
    license = l.read()

files_arr = []

#This part is acting iffy....grabs some files that seem irrelevant
for root,dirs,files in os.walk(path_to, topdown=True):
    for file in files:
    #     files_arr.append(os.path.join(root,name))

    # for file in files_arr: 
        if file.endswith(".py") or file.endswith(".txt"):
            with open(os.path.join(root,file), "r+") as f:
                content = f.read()
                f.seek(0,0)
                f.write(license + "\n\n" + content)

 
# Connect to CASE Network
# os.system(f'''cmd /c "netsh wlan conne6ct name={"CNHI-WiFi"}"''')
# sleep(10)

# Move edited files to final destination
try:
    shutil.move(path_to, final_destination)
except PermissionError:
    print("idx file?????")