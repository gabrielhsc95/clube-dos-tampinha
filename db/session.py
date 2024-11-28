import base64
import os
import tempfile
import zipfile

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, Session


def _load_local_env():
    from dotenv import load_dotenv

    load_dotenv()


def _create_temp_secure_connect_bundle():
    """
    Creates a temporary zip file containing the secure connect bundle.

    Returns:
      The path to the temporary zip file.
    """
    files = {
        "ca.crt": os.getenv("CA_CRT").replace("\\n", "\n"),
        "cert": os.getenv("CERT").replace("\\n", "\n"),
        "cert.pfx": base64.b64decode(os.getenv("CERT_PFX")),
        "config.json": os.getenv("CONFIG_JSON"),
        "cqlshrc": os.getenv("CQLSHRC").replace("\\n", "\n"),
        "identity.jks": base64.b64decode(os.getenv("IDENTITY_JKS")),
        "key": os.getenv("KEY").replace("\\n", "\n"),
        "trustStore.jks": base64.b64decode(os.getenv("TRUST_STORE_JKS")),
    }
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as temp_zip_file:
        with zipfile.ZipFile(temp_zip_file, "w") as zipf:
            for filename, content in files.items():
                zipf.writestr(filename, content)
        return temp_zip_file.name


def create_session() -> Session:
    if os.getenv("IS_LOCAL", "0") == "1":
        _load_local_env()

    auth_provider = PlainTextAuthProvider(
        os.getenv("CLIENT_ID"),
        os.getenv("CLIENT_SECRET"),
    )
    temp_secure_connect_bundle = _create_temp_secure_connect_bundle()

    cluster = Cluster(
        cloud={"secure_connect_bundle": temp_secure_connect_bundle},
        auth_provider=auth_provider,
    )
    session = cluster.connect()

    os.remove(temp_secure_connect_bundle)
    return session
