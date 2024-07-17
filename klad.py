import os
from typing import Union
from azure.keyvault.secrets import SecretClient
from azure.identity import ManagedIdentityCredential, InteractiveBrowserCredential

def get_credentials() -> Union[ManagedIdentityCredential, InteractiveBrowserCredential]:
    # Check if the code is running in the cloud (Azure App Service, Azure Functions, etc.)
    if "WEBSITE_SITE_NAME" in os.environ:
        credential = ManagedIdentityCredential()
    else:
        credential = InteractiveBrowserCredential(additionally_allowed_tenants = '9dee493d-2635-4f52-ac3e-96c0d02f6daf')
    return credential

def get_keyvault_connection(keyvault_url: str) -> SecretClient:
    credential = get_credentials()
    return SecretClient(keyvault_url, credential)

def main():
    keyvault_connection = get_keyvault_connection("https://al-4tg-kv-learningvnet.vault.azure.net/")
    my_secret = keyvault_connection.get_secret("MySecret").value
    print(my_secret)

if __name__ == '__main__':
    main()