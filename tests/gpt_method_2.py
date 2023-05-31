import os
import requests
import msal
from msal import ConfidentialClientApplication


def authenticate():
    """
    Acquire authentication token via MSAL
    """
    authority_url = (
        "https://login.microsoftonline.com/4866cf07-720e-4873-aa11-cbc6a098c334"
    )
    app = msal.ConfidentialClientApplication(
        authority=authority_url,
        client_id="609f4e5c-c115-4f8f-af2e-1a2e53b047f9",
        client_credential="N1j8Q~G1unW04A4H8U7HGtonMyK2wRB-i9JYscg4",
    )
    token = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )
    return token


def upload_file(access_token, file_path, onedrive_path):
    file_name = os.path.basename(file_path)
    upload_url = f"https://graph.microsoft.com/v1.0/drive/root:/{onedrive_path}/{file_name}:/content"

    headers = {"Authorization": f"Bearer {access_token}"}
    data = open(file_path, "rb").read()

    response = requests.put(upload_url, headers=headers, data=data)
    response.raise_for_status()


def upload_directory(access_token, directory_path, onedrive_path):
    for entry in os.scandir(directory_path):
        if entry.is_file():
            upload_file(access_token, entry.path, onedrive_path)
        elif entry.is_dir():
            new_onedrive_path = f"{onedrive_path}/{entry.name}"
            upload_directory(access_token, entry.path, new_onedrive_path)


def run(client_id, client_secret, tenant_id, local_folder_path, onedrive_folder_path):
    access_token = authenticate()
    upload_directory(access_token, local_folder_path, onedrive_folder_path)


if __name__ == "__main__":
    local_folder_path = "D:\\repos\\arduino-sketches\\FEI_MEGA\\MEGA_ESP_3.1"
    onedrive_folder_path = "FEI_SHARED/test"

    tenant = "b982fbe0-f860-4be8-b974-25005ff5aba4"
    # Drogne
    client_id = "609f4e5c-c115-4f8f-af2e-1a2e53b047f9"
    client_secret = "N1j8Q~G1unW04A4H8U7HGtonMyK2wRB-i9JYscg4"

    # Dsmith
    # client_id = "5421bf2a-f352-4a3d-a647-0a8ded1e96d7"
    # client_secret = "~_C8Q~t8K-gFvszz7r5sRu-IlBWDnJ~Pa2W10aBu"

    print(authenticate())

    run(client_id, client_secret, tenant, local_folder_path, onedrive_folder_path)
