import tarfile
import requests
import os
from typing import IO

import rsa

import json
import requests

from medux.core.models import DataPack
from medux.preferences.cached_preferences import CachedPreferences
from medux.preferences.definitions import Scope
from semantic_version import Version


def load_datapack_information_from_server(request):
    """Loads a list of available update packs from the server and saves it into
    DataPack models"""

    response = requests.get(
        CachedPreferences(request).get(
            "core", "datapack_update_server_url", Scope.VENDOR
        )
    )
    # TODO: error handling
    data = json.loads(response.json())  # [{model:"foo", version: "1.0.0"}, ...]

    for datapack in DataPack.objects.all():
        for model, new_version in data:
            if datapack.model == model:
                if Version(new_version) >= Version(datapack.version):
                    pass
                    # download new version

    # instance = DataPack()
    # for field in ["uuid","name","title","description", "license", "version", "experimental",
    #               "publisher","language", "model",],
    # instance.uuid = data.uuid



def download_datapack(request, model: str, version: str) -> IO:

    url = "http://example.com/path/to/file.zip"

    # Set the credentials for the server (if necessary)
    # If the server does not require credentials, you can skip this step
    username = "your_username"
    password = "your_password"

    # Send a request to the server to download the file
    response = requests.get(url, auth=(username, password))

    # Check that the request was successful
    if response.status_code == 200:
        # Save the contents of the response to a file
        with open("file.zip", "wb") as f:
            f.write(response.content)
    else:
        print("Failed to download file. HTTP status code:", response.status_code)


# Open the .tgz file and extract its contents
tar = tarfile.open("data.tgz")
tar.extractall()
tar.close()

# Read in the public key from a file
with open("public_key.pem", "rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

# Read in the signature from a file
with open("signature.sig", "rb") as f:
    signature = f.read()

# Read in the data that was extracted from the .tgz file
with open("data.txt", "rb") as f:
    data = f.read()

# Use the rsa library to verify the signature
try:
    rsa.verify(data, signature, public_key)
    print("The signature is valid!")
except rsa.pkcs1.VerificationError:
    print("The signature is not valid!")

# Clean up by deleting the extracted data and signature
os.remove("data.txt")
os.remove("signature.sig")
