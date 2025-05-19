import requests
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Đọc private key
with open("keys/private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Đọc file gửi
with open("file_to_send.txt", "rb") as f:
    data = f.read()

# Ký dữ liệu
signature = private_key.sign(
    data,
    padding.PKCS1v15(),
    hashes.SHA256()
)

# Gửi lên server
response = requests.post("http://127.0.0.1:5000/upload", files={
    'file': ("file_to_send.txt", data),
    'signature': ("signature.sig", signature)
})

print("📨 Phản hồi từ server:", response.text)
