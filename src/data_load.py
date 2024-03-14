import os, uuid
import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

def connect_to_azure_storage(account_name, account_key, container_name):
    """
    Connects to Azure Blob Storage using the provided credentials.

    Parameters:
        account_name (str): The Azure Storage account name.
        account_key (str): The Azure Storage account key.
        container_name (str): The name of the container in Azure Blob Storage.

    Returns:
        blob_service_client: The BlobServiceClient object for interacting with Blob Storage.
    """
    connect_str = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container_name)
    return container_client

def download_and_save_files(container_client, destination_folder='../data/'):
    """
    Downloads files from Azure Blob Storage and saves them locally.

    Parameters:
        container_client: The ContainerClient object for the container in Azure Blob Storage.
        destination_folder (str): The folder path where the files will be saved locally.
    """
    blob_list = [blob.name for blob in container_client.list_blobs()]
    print("Data in Azure:", blob_list)
    
    for blob_name in blob_list:
        sas_url = generate_blob_sas(account_name=account_name,
                                    container_name=container_name,
                                    blob_name=blob_name,
                                    account_key=account_key,
                                    permission=BlobSasPermissions(read=True),
                                    expiry=datetime.utcnow() + timedelta(hours=1))
        sas_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_url}"
        
        if 'csv' in sas_url:
            df = pd.read_csv(sas_url, sep='|', encoding='utf-8', on_bad_lines='skip')
            df.to_csv(f"{destination_folder}{blob_name}", sep='|', index=False)
            print(f"Saved CSV file '{blob_name}' in '{destination_folder}'")
        elif 'parquet' in sas_url:
            df = pd.read_parquet(sas_url)
            df.to_parquet(f"{destination_folder}{blob_name[:-4]}")
            print(f"Saved Parquet file '{blob_name[:-4]}' in '{destination_folder}'")
        else:
            print("No files in storage")

# Azure Storage account credentials, read from a csv
credentials_df = pd.read_csv('../data/credenciales.csv', header=0)
account_name = credentials_df['account_name'][0]
account_key = credentials_df['account_key'][0]
container_name = credentials_df['account_key'][0]

# Connect to Azure Storage
container_client = connect_to_azure_storage(account_name, account_key, container_name)

# Download and save files locally
download_and_save_files(container_client)
