import asyncio

from azure.identity import ClientSecretCredential
from kiota_abstractions.api_error import APIError
from kiota_authentication_azure.azure_identity_authentication_provider import (
    AzureIdentityAuthenticationProvider,
)
from msgraph import GraphRequestAdapter, GraphServiceClient

# (Optional) Set the event loop policy for Windows
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Create authentication provider object. Used to authenticate request
credential = ClientSecretCredential(
    tenant_id="b982fbe0-f860-4be8-b974-25005ff5aba4",
    client_id="5421bf2a-f352-4a3d-a647-0a8ded1e96d7",
    client_secret="~_C8Q~t8K-gFvszz7r5sRu-IlBWDnJ~Pa2W10aBu",
)
scopes = ["https://graph.microsoft.com/.default"]
auth_provider = AzureIdentityAuthenticationProvider(credential, scopes=scopes)

# Initialize a request adapter with the auth provider.
request_adapter = GraphRequestAdapter(auth_provider)

# Create an API client with the request adapter.
client = GraphServiceClient(request_adapter)


async def get_drives():
    try:
        drives = await client.drives.get()
        if drives and drives.value:
            for drive in drives.value:
                print(
                    drive.id,
                    drive.drive_type,
                    drive.name,
                    drive.description,
                    drive.web_url,
                )
    except APIError as e:
        print(e.error.message)


async def get_drive_items():
    try:
        items = await client.drives.by_drive_id(
            "b!NvwQaCejzEq_SqSblwsxEuqeMUYiFCdHmL6zxaqZyBQR7AVjz3K7Rahkq_koagVu"
        ).items.get(filter="size gt 0")
        if items and items.value:
            for item in items.value:
                print(item.id, item.name, item.size, item.folder, item.file)
                print("\n")
    except APIError as e:
        print(e.error.message)


if __name__ == "__main__":
    asyncio.run(get_drive_items())
    # asyncio.run(get_drives())
