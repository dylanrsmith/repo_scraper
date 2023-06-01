import os
import git
import stat
import shutil
import json
import requests
import openpyxl
import pandas
from sync_folders import main
from datetime import datetime
from atlassian import Bitbucket


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
repo_names = []         # repo ID BB
repo_staging_spots = []
repo_onedrive_spots = []
###
#staging_spots = []      # local_path
plant_server_spots = []        # server path
plant_onedrive_spots = []     # onedrive path
triggers = []           # 'W' or 'X'
repository = []


# fargoengineering domain
client_id = "5421bf2a-f352-4a3d-a647-0a8ded1e96d7"
client_secret = "~_C8Q~t8K-gFvszz7r5sRu-IlBWDnJ~Pa2W10aBu"
tenant = "b982fbe0-f860-4be8-b974-25005ff5aba4"
redirect_uri = "http://localhost:8080"
user_id = "dsmith@fargoengineering.com"


def get_access_token(client_id, client_secret, tenant):
    token_url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
    token_data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials",
    }
    token_response = requests.post(token_url, data=token_data)
    access_token = token_response.json().get("access_token")
    return access_token


def download_file_from_onedrive(access_token, onedrive_file_path, local_file_path):
    download_url = "https://graph.microsoft.com/v1.0/users/"+user_id+"/drive/items/root:/{0}:/content".format(
        onedrive_file_path
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
    }

    response = requests.get(download_url, headers=headers)

    if response.status_code in (200,201,202,204):
        with open(local_file_path, "wb") as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print("Error downloading file:", response.content)


def upload_folder_to_onedrive(access_token, local_folder_path, onedrive_folder_path):
    for root, dirs, files in os.walk(local_folder_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, local_folder_path)
            onedrive_file_path = onedrive_folder_path + "/" + relative_path
            upload_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/items/root:/{onedrive_file_path}:/content"
            headers = {
                "Content-Type": "text/plain",
                "Authorization": "Bearer " + access_token,
            }
            with open(local_file_path, "rb") as file:
                response = requests.put(upload_url, headers=headers, data=file)
                if response.status_code in (200,201,202,204):
                    print(f"File {local_file_path} uploaded successfully.")
                else:
                    print(f"Error uploading file {local_file_path}:", response.content)         #item not found?


def rmtree(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            try:
                os.chmod(filename, stat.S_IWRITE)
                os.remove(filename)
            except PermissionError as e:
                print("UNABLE TO DELETE FILE: "+filename+"\n Something is locking the file....")
                print(e.winerror)
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
    access_token = get_access_token(client_id, client_secret, tenant)
    download_file_from_onedrive(access_token,"Documents/Sync.xlsx","./Config/Sync.xlsx")
    # read excel file
    wb = openpyxl.load_workbook(".\Config\Sync.xlsx")
    plant_sheets = []
    #sheet = wb.active
    print(wb.sheetnames)
    for sheet in wb.sheetnames:
        if sheet == "BitBucket Repos":
            repo_sheet = wb[sheet]
        else:
            plant_sheets.append(wb[sheet])

    # Parse Repository Sheet First:
    for row in repo_sheet.iter_rows(values_only=True):
        row_data = []

        for cell in row:
            row_data.append(cell)

        if row_data[0] != "Name" and row_data[0] != None:
            repo_names.append(row_data[0])
        if row_data[1] != "Local Path" and row_data[1] != None:
            repo_staging_spots.append(row_data[1])
        if row_data[2] != "Destination Path" and row_data[2] != None:
            repo_onedrive_spots.append(row_data[2])        

    # Parse Each Plant Sheet Next:
    for sheet in plant_sheets:
        for row in sheet.iter_rows(values_only=True):
            row_data = []

            for cell in row:
                row_data.append(cell)

            if row_data[0] != "Source" and row_data[0] != None:
                plant_onedrive_spots.append(row_data[0])
            if row_data[1] != "Destination" and row_data[1] != None:
                plant_server_spots.append(row_data[1])
            if row_data[2] != "Trigger":
                triggers.append(row_data[2])
            if row_data[3] != "Repository":
                repository.append(row_data[3])

    df = pandas.read_excel('./Config/Sync.xlsx')
    df.replace('X','',inplace=True)
    df.to_excel('./Config/Sync.xlsx',index=False)
    
    upload_folder_to_onedrive(access_token,"./Config/Sync.xlsx", "FEI_SHARED/Repository/Sync.xlsx")


def repo_sync(repo_name, path_to, final_destination):
    # NOTE: path_to needs to be an empty directory
    # Delete directory if it exists
    try:
        rmtree(path_to)
        #rmtree(final_destination)
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
            if file.endswith(".cs") or file.endswith(".ino") or file.endswith(".h"): 
                with open(os.path.join(root, file), "r", encoding="utf-8-sig") as f:
                    try:
                        content = f.read()
                    except UnicodeDecodeError as e:
                        print("ADD LICENSE: Unable to parse target file: "+e)
                with open(os.path.join(root, file), "wb") as f:
                    f.seek(0, 0)
                    new_content = (license + "\n\n" + format(content)).encode("utf-8")
                    f.write(new_content)

    #rmtree(final_destination)
    rmtree(path_to + "\\.git")
    change_permission(path_to)
    access_token = get_access_token(client_id, client_secret, tenant)
    upload_folder_to_onedrive(
        access_token,
        path_to,
        "Documents/"+repo_name,
    )
    # shutil.move(path_to, final_destination)
    # main.sync(path_to, final_destination)


# Main Function
if __name__ == "__main__":
    start = datetime.now()
    get_config()
    print("CONFIG MODIFIED SUCCESFULLY")


    for i in range(len(repo_names)):
        # rmtree(final_spots[i])
        # if os.path.exists(final_spots[i]) == False:
        repo_sync(repo_names[i], repo_staging_spots[i], repo_onedrive_spots[i])         # Will sync bitbucket and onedrive repos, but not additional schematics etc..
        # else:
            # print("Path already exists: " + final_spots[i])

    end = datetime.now()
    time = end - start
    print("DONE @ " + str(time))
