import os 

from pathlib import Path
from typing import Dict, NoReturn


SUPPORTED_PROVIDERS = [
    "azure",
    "aws",
    "gcp",
    "ibmcloud",
]

AVAILABLE_PROVIDERS = [
    "azure",
]


def download_model_from_azure(config: Dict[str, str], download_dir: str) -> NoReturn:

    from azure.identity     import ClientSecretCredential
    from azure.storage.blob import BlobServiceClient

    credential = ClientSecretCredential(
        client_id     = config["client_id"],
        client_secret = config["client_secret"],
        tenant_id     = config["tenant_id"],
    )

    blob_service_client = BlobServiceClient(account_url=config["account_url"], credential=credential)
    container_client    = blob_service_client.get_container_client(config["container_name"])
    blob_client         = container_client.get_blob_client(config["name"])

    Path(download_dir).mkdir(parents=True, exist_ok=True)
    destination_path = os.path.join(Path(download_dir).resolve(), config["name"])

    with open(destination_path, "wb") as f:
        f.write(blob_client.download_blob().readall())


def download_model(
    provider: str,
    config: Dict[str, str],
    download_dir: str = '.',
    unzip: bool = False,
) -> NoReturn:
    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(f"Provider {provider} is not supported. Supported providers are: {SUPPORTED_PROVIDERS}")
    
    if provider not in AVAILABLE_PROVIDERS:
        raise ValueError(f"Provider {provider} is not yet available. Please choose from: {AVAILABLE_PROVIDERS}")
    
    if provider == "azure":
        download_model_from_azure(config, download_dir)

    if unzip:
        assert config["name"].endswith(".zip"), "Model must be a zip file to be unzipped"
        import zipfile

        with zipfile.ZipFile(os.path.join(download_dir, config["name"]), 'r') as zip_ref:
            zip_ref.extractall(download_dir)


def upload_model_to_azure(config: Dict[str, str], model_path: str) -> NoReturn:

    from azure.identity     import ClientSecretCredential
    from azure.storage.blob import BlobServiceClient

    credential = ClientSecretCredential(
        client_id     = config["client_id"],
        client_secret = config["client_secret"],
        tenant_id     = config["tenant_id"],
    )

    blob_service_client = BlobServiceClient(account_url=config["account_url"], credential=credential)
    container_client    = blob_service_client.get_container_client(config["container_name"])
    blob_client         = container_client.get_blob_client(config["name"])

    with open(model_path, "rb") as f:
        blob_client.upload_blob(f)


def upload_model(
    provider: str,
    config: Dict[str, str],
    model_path: str,
) -> NoReturn:
    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(f"Provider {provider} is not supported. Supported providers are: {SUPPORTED_PROVIDERS}")
    
    if provider not in AVAILABLE_PROVIDERS:
        raise ValueError(f"Provider {provider} is not yet available. Please choose from: {AVAILABLE_PROVIDERS}")
    
    if provider == "azure":
        upload_model_to_azure(config, model_path)
