import base64
import pickle
import sys
from os import urandom
from Crypto.Hash import SHAKE256

sys.path.append('/falcon')
from falcon import falcon

# Constants
FALCON_PARAM = 512
SECRET_KEY_FILE = "falcon_sk.pem"
PUBLIC_KEY_FILE = "falcon_pk.pem"
SIGNATURE_FILE = "falcon_sig.pem"
PDF_FILE = "C:\\Users\\Admin\\.vscode\\Python\\NT219-Project\\Scripts\\input.pdf"

def save_pem(filename, data, type):
    try:
        pem_data = f"-----BEGIN {type}-----\n"
        pem_data += base64.encodebytes(data).decode('utf-8')
        pem_data += f"-----END {type}-----\n"
        with open(filename, 'w') as f:
            f.write(pem_data)
    except Exception as e:
        print(f"Failed to save PEM file {filename}: {e}")

def load_pem(filename, type):
    try:
        with open(filename, 'r') as f:
            pem_data = f.read()
        header = f"-----BEGIN {type}-----"
        footer = f"-----END {type}-----"
        data = pem_data.replace(header, "").replace(footer, "").strip()
        return base64.decodebytes(data.encode('utf-8'))
    except Exception as e:
        print(f"Failed to load PEM file {filename}: {e}")
        return None

class SerializableSecretKey(falcon.SecretKey):
    def to_bytes(self):
        return pickle.dumps(self)

    @classmethod
    def from_bytes(cls, data):
        return pickle.loads(data)

class SerializablePublicKey(falcon.PublicKey):
    def to_bytes(self):
        return pickle.dumps(self)

    @classmethod
    def from_bytes(cls, data):
        return pickle.loads(data)

def generate_keys():
    try:
        sk = SerializableSecretKey(FALCON_PARAM)
        pk = SerializablePublicKey(sk)
        
        save_pem(SECRET_KEY_FILE, sk.to_bytes(), "FALCON PRIVATE KEY")
        save_pem(PUBLIC_KEY_FILE, pk.to_bytes(), "FALCON PUBLIC KEY")
        print("Keys generated and saved successfully.")
    except Exception as e:
        print(f"Failed to generate keys: {e}")

def sign_pdf(pdf_path, owner, date, place):
    try:
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()

        additional_info = f"{owner}{date}{place}".encode('utf-8')
        pdf_data += additional_info

        sk_data = load_pem(SECRET_KEY_FILE, "FALCON PRIVATE KEY")
        if sk_data is None:
            return
        sk = SerializableSecretKey.from_bytes(sk_data)

        hash_func = SHAKE256.new()
        hash_func.update(pdf_data)
        hash_value = hash_func.read(64)

        signature = sk.sign(hash_value)
        save_pem(SIGNATURE_FILE, signature, "FALCON SIGNATURE")
        print("PDF signed and signature saved successfully.")
    except Exception as e:
        print(f"Failed to sign PDF: {e}")

def verify_pdf(pdf_path, owner, date, place):
    try:
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()

        # Add the same additional information that was added during signing
        additional_info = f"{owner}{date}{place}".encode('utf-8')
        pdf_data += additional_info

        pk_data = load_pem(PUBLIC_KEY_FILE, "FALCON PUBLIC KEY")
        if pk_data is None:
            return False
        pk = SerializablePublicKey.from_bytes(pk_data)

        signature = load_pem(SIGNATURE_FILE, "FALCON SIGNATURE")
        if signature is None:
            return False

        hash_func = SHAKE256.new()
        hash_func.update(pdf_data)
        hash_value = hash_func.read(64)

        is_valid = pk.verify(hash_value, signature)
        return is_valid
    except Exception as e:
        print(f"Failed to verify PDF: {e}")
        return False

# Main execution
generate_keys()

owner = input("Enter the owner's name: ")
date = input("Enter the date: ")
place = input("Enter the place: ")
sign_pdf(PDF_FILE, owner, date, place)

is_valid = verify_pdf(PDF_FILE, owner, date, place)
print(f"Signature is valid: {is_valid}")
