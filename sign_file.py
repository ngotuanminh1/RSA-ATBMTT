from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

with open("keys/private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

with open("file_to_send.txt", "rb") as f:
    data = f.read()

signature = private_key.sign(
    data,
    padding.PKCS1v15(),
    hashes.SHA256()
)

with open("signature.sig", "wb") as f:
    f.write(signature)

print("✅ Đã tạo file chữ ký: signature.sig")
