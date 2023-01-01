import os
from datetime import datetime
from os.path import dirname, join

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.queue import QueueClient
from dotenv import load_dotenv

# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

# 認証に必要なキーとトークン
HOT_PEPPER_API_KEY = os.environ['HOT_PEPPER_API_KEY']
GOOGLE_MAPS_API_KEY = os.environ['GOOGLE_MAPS_API_KEY']

HOT_PEPPER_API_URL = os.environ['HOT_PEPPER_API_URL']
GEOCODING_API_URL = os.environ['GEOCODING_API_URL']
GOOGLE_MAPS_API_URL = os.environ['GOOGLE_MAPS_API_URL']

# credential = DefaultAzureCredential()
# key_vault_url = os.environ["KEY_VAULT_URL"]
# keyvault_client = SecretClient(vault_url=key_vault_url, credential=credential)
# api_secret_name = os.environ["THIRD_PARTY_API_SECRET_NAME"]
# vault_secret = keyvault_client.get_secret(api_secret_name)

# # The "secret" from Key Vault is an object with multiple properties. The key we
# # want for the third-party API is in the value property.
# access_key = vault_secret.value

# queue_url = os.environ["STORAGE_QUEUE_URL"]
# queue_client = QueueClient.from_queue_url(queue_url=queue_url, credential=credential)
