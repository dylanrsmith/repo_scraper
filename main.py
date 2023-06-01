"""
    Still need to try to only overwrite repos in final destination,
    IF AND ONLY IF they are older than the newly cloned repo.
"""
import os
import git
import stat
import shutil
import json
import requests
import webbrowser
import openpyxl
from sync_folders import main
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
triggers = []

# AS OF 5/26/23
# Seems impossible to achieve onedrive connection without SPO License...

# These credentials will expire 5-17-2025
# # Dustin's gmail Domain
# client_id = "609f4e5c-c115-4f8f-af2e-1a2e53b047f9"
# client_secret = "N1j8Q~G1unW04A4H8U7HGtonMyK2wRB-i9JYscg4"
# redirect_uri = "http://localhost"
# tenant = "4866cf07-720e-4873-aa11-cbc6a098c334"
# user_id = "3437836b-6a0f-4849-9349-416d2dce36da"

# Dylan's fargoengineering Domain
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
    download_url = "https://graph.microsoft.com/v1.0/users/{user_id}/drive/items/root:/{0}:/content".format(
        onedrive_file_path
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
    }

    response = requests.get(download_url, headers=headers)

    if response.status_code in (200,201):
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
            os.chmod(filename, stat.S_IWRITE)
            shutil.remove(filename)
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


def get_config_txt():
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


def get_config():
    # read excel file
    wb = openpyxl.load_workbook(".\Sync.xlsx")
    sheet = wb.active

    excel_data = []
    i = 0
    for row in sheet.iter_rows(values_only=True):
        row_data = []

        for cell in row:
            row_data.append(cell)

        if row_data[0] != "Source" and row_data[0] != None:
            staging_spots.append(row_data[0])
        if row_data[1] != "Destination" and row_data[1] != None:
            final_spots.append(row_data[1])
        if row_data[2] != "Trigger" and row_data[2] != None:
            triggers.append(row_data[2])
        if row_data[3] != "Repository" and row_data[3] != None:
            repo_names.append(row_data[3])


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
    rmtree(path_to + "\\.git")
    change_permission(path_to)
    access_token = get_access_token(client_id, client_secret, tenant)
    upload_folder_to_onedrive(
        access_token,
        path_to,
        "Documents",
    )
    # shutil.move(path_to, final_destination)
    # main.sync(path_to, final_destination)


# Main Function
if __name__ == "__main__":
    start = datetime.now()
    get_config()

    for i in range(len(repo_names)):
        rmtree(final_spots[i])
        if os.path.exists(final_spots[i]) == False:
            clone(repo_names[i], staging_spots[i], final_spots[i])
        else:
            print("Path already exists: " + final_spots[i])

    end = datetime.now()
    time = end - start
    print("DONE @ " + str(time))
