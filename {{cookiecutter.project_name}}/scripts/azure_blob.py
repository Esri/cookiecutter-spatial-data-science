import argparse
import os
from pathlib import Path
import re
import shutil
import tempfile
from zipfile import ZipFile

from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv, find_dotenv
    
# load environment variables from .env
load_dotenv(find_dotenv())


def make_name_compliant(name:str)->str:
    """Make names string compliant with Azure Container rules. While Blob Names can use mixed case, for consistency, 
    this function makes names all lowercase."""

    # must be lowercase
    name = name.lower()
    
    # contain only letters numbers, and hyphens
    name = re.sub(r'[^a-z0-9\-]', '', name)

    # ensure starting with a letter or number
    name = re.sub(r'^(?:\D\W)*', '', name)

    # between 3 and 63 characters
    if len(name) < 3:
        name = name.zfill(3)
    elif len(name) > 63:
        name = name[:63]
        
    return name

    
def push_data(overwrite:bool=False)->bool:
    """Push project data to Azure Blob storage"""

    # if not overwriting
    if not overwrite and [c.name for c in blob_svc_client.list_containers()]:
        raise Exception('Data appears to already be stored in Azure Blob Storage')

    # create a client to interact with the container
    container_client = blob_svc_client.get_container_client(container_name)

    # if the container does not exist, create it
    if container_name not in [c.name for c in blob_svc_client.list_containers()]:
        container_client.create_container()
    
    # put the contents of the data directory into a temporary archive
    data_archive = shutil.make_archive(
        base_name=Path(tempfile.gettempdir())/container_name, 
        format='zip',
        root_dir=data_dir
    )

    # upload the blob
    with open(data_archive, 'rb') as data_stream:
        container_client.upload_blob(name=Path(data_archive).name, data=data_stream, overwrite=True)
        
    return True


def get_data(overwrite:bool=False)->bool:
    """Get project data from Azure Blob Storage"""

    # if the container does not exist, raise Exception
    if container_name not in [c.name for c in blob_svc_client.list_containers()]:
        raise Exception('The project data does not appear to be stored in Azure Blob Storage.')

    # if the data diretory exists, and we want to overwrite, get rid of what is already there
    if data_dir.exists() and overwrite == True:
        shutil.rmtree(data_dir)
        data_dir.mkdir()

    # if the data directory is there, and we do NOT want to overwrite, bomb out
    elif data_dir.exists():
        raise Exception('Data directory already exists.')
        
    # download the contents from the blob to the temp directory
    data_archive_pth = Path(tempfile.gettempdir())/f'{container_name}.zip'

    # create a client to interact with the container
    container_client = blob_svc_client.get_container_client(container_name)
    
    with open(data_archive_pth, "wb") as az_blob:
        blob_data = container_client.download_blob(data_archive_pth.name)
        blob_data.readinto(az_blob)

    # exract the contents of the zipfile to the data directory
    with ZipFile(data_archive_pth) as zip_file:
        zip_file.extractall(data_dir)
        
    return True


if __name__ == '__main__':

    # set up command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('method', help='[push | get] Push or get data from Azure Blob Storage.')
    parser.add_argument('project_dir', help='Path to project directory.')
    parser.add_argument('-o', '--overwrite', help='Overwrite data in destiation.', action='store_true')

    # get input command line arguments
    args = parser.parse_args()

    # paths to resources
    project_parent = Path(args.project_dir)
    data_dir = project_parent/'data'

    # get the project name from the path
    project_name = project_parent.name

    # load the blob configuration from the environment file
    az_account_name = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
    az_key = os.getenv('AZURE_STORAGE_ACCOUNT_KEY')

    # create a blob service client for interacting with the blob container
    blob_svc_client = BlobServiceClient.from_connection_string(
        f'DefaultEndpointsProtocol=https;AccountName={az_account_name};AccountKey={az_key};EndpointSuffix=core.windows.net'
    )

    # create an azure compliant container name from the project name
    container_name = make_name_compliant(project_name)

    # implement the correct method
    if args.method == 'push':
        push_data(args.overwrite)
    elif args.method == 'get':
        get_data(args.overwrite)
    else:
        raise Exception(f'Method must either be push or get, NOT {args.method}')
