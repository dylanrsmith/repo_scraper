import msal
import os
import tempfile
from os.path import isfile, join
from office365.graph_client import GraphClient
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File


def acquire_token_func():
    """
    Acquire authentication token via MSAL
    """
    authority_url = (
        "https://login.microsoftonline.com/b982fbe0-f860-4be8-b974-25005ff5aba4"
    )
    app = msal.ConfidentialClientApplication(
        authority=authority_url,
        client_id="5421bf2a-f352-4a3d-a647-0a8ded1e96d7",
        client_credential="~_C8Q~t8K-gFvszz7r5sRu-IlBWDnJ~Pa2W10aBu",
    )
    token = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )
    return token


def download_files(remote_folder, local_path):
    drive_items = remote_folder.children.get().execute_query()
    for drive_item in drive_items:
        if drive_item.file is not None:  # is file?
            # download file content
            with open(os.path.join(local_path, drive_item.name), 'wb') as local_file:
                drive_item.download(local_file).execute_query()     # 404?
                


def download_file():
    client = GraphClient(acquire_token_func)
    # retrieve drive properties 
    file_item = client.users["dsmith@fargo"].drive.root.get_by_path("Documents/test.xlsx").get().execute_query()

    with tempfile.TemporaryDirectory() as local_path:
        with open(os.path.join(local_path, file_item.name), 'wb') as local_file:
            file_item.download_session(local_file, chunk_size=1024*512).execute_query()
        print("File '{0}' has been downloaded to {1}".format(file_item.name, local_file.name))




def upload_files(remote_drive, local_root_path):
    """
    Uploads files from local folder into OneDrive drive

    :type remote_drive: Drive
    :type local_root_path: str
    """
    for name in os.listdir(local_root_path):
        path = join(local_root_path, name)
        if isfile(path):
            with open(path, "rb") as local_file:
                content = local_file.read()
            uploaded_drive_item = remote_drive.root.upload(
                name, content
            ).execute_query()
            print(
                "File '{0}' uploaded into {1}".format(
                    path, uploaded_drive_item.web_url
                ),
                path,
            )


def list_drives():
    tenant_name = "fargoengineering.com"
    client = GraphClient(acquire_token_func)
    drives = client.drives.get().execute_query()
    for drive in drives:
        print("Drive url: {0}".format(drive.web_url))
        print("\n")
    # users = client.users.get().execute_query()
    # for user in users:
    #     print(user)
    #     print("\n")




if __name__ == "__main__":
    token = acquire_token_func()
    print(token)

    # Dylan's Domain - fargo engineering.
    site_url = "https://fargoengineering-my.sharepoint.com/personal/dsmith_fargoengineering_com"
    client_id = "5421bf2a-f352-4a3d-a647-0a8ded1e96d7"
    client_secret = "~_C8Q~t8K-gFvszz7r5sRu-IlBWDnJ~Pa2W10aBu"
    tenant = "b982fbe0-f860-4be8-b974-25005ff5aba4"
    redirect_uri = "http://localhost"
    user_id = "dsmith@fargoengineering.com"
    context_auth = AuthenticationContext(url=site_url)
    context_auth.acquire_token_for_app(client_id, client_secret)
    ctx = ClientContext(site_url, context_auth)

    list_drives()

    download_file()

