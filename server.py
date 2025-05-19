from flask import Flask, request, render_template_string
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

app = Flask(__name__)

with open("keys/public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

HTML_FORM = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Upload File Có Ký Số</title>
  <style>
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      padding: 0;
      height: 100vh;
      background: linear-gradient(135deg, #667eea, #764ba2);
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .container {
      background: rgba(255, 255, 255, 0.15);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      padding: 40px;
      border-radius: 20px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
      width: 100%;
      max-width: 460px;
      color: #ffffff;
      text-align: center;
    }

    h2 {
      margin-bottom: 25px;
      font-size: 28px;
      font-weight: 700;
    }

    .custom-file {
      position: relative;
      margin: 20px 0;
    }

    .custom-file input[type="file"] {
      opacity: 0;
      width: 100%;
      height: 48px;
      position: absolute;
      left: 0;
      top: 0;
      cursor: pointer;
      z-index: 3;
    }

    .custom-file label {
      display: block;
      width: 100%;
      padding: 12px;
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.85);
      color: #333;
      font-weight: 500;
      text-align: center;
      cursor: pointer;
      transition: background 0.3s ease;
      z-index: 2;
      position: relative;
    }

    .custom-file label:hover {
      background: rgba(255, 255, 255, 0.95);
    }

    button {
      margin-top: 25px;
      width: 100%;
      padding: 14px;
      background: #ffffff;
      color: #4a00e0;
      border: none;
      border-radius: 10px;
      font-weight: bold;
      font-size: 16px;
      cursor: pointer;
      transition: background-color 0.3s ease;
      box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }

    button:hover {
      background: #f0f0f0;
    }

    .message {
      margin-top: 30px;
      padding: 15px;
      border-radius: 12px;
      font-weight: 600;
    }

    .success {
      background-color: #d4edda;
      color: #155724;
      border: 1px solid #c3e6cb;
    }

    .error {
      background-color: #f8d7da;
      color: #721c24;
      border: 1px solid #f5c6cb;
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>📄 Upload File Có Ký Số</h2>
    <form method="POST" enctype="multipart/form-data">
      <div class="custom-file">
        <input type="file" name="file" id="file" required onchange="updateFileName(this, 'fileNameDisplay')" />
        <label for="file">📎 Chọn file dữ liệu</label>
        <div id="fileNameDisplay" class="file-name">Chưa có tệp nào được chọn</div>
      </div>

      <div class="custom-file">
        <input type="file" name="signature" id="signature" required onchange="updateFileName(this, 'sigNameDisplay')" />
        <label for="signature">✍️ Chọn file chữ ký</label>
        <div id="sigNameDisplay" class="file-name">Chưa có tệp nào được chọn</div>
      </div>

      <button type="submit">📤 Gửi lên server</button>
    </form>

    {% if message %}
      <div class="message {% if 'không hợp lệ' in message %}error{% else %}success{% endif %}">
        {{ message }}
      </div>
    {% endif %}
  </div>

  <script>
    function updateFileName(input, targetId) {
      const fileDisplay = document.getElementById(targetId);
      if (input.files.length > 0) {
        fileDisplay.textContent = input.files[0].name;
      } else {
        fileDisplay.textContent = "Chưa có tệp nào được chọn";
      }
    }
  </script>
</body>
</html>
'''


@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    if request.method == "POST":
        if 'file' not in request.files or 'signature' not in request.files:
            message = "❌ Thiếu file hoặc chữ ký."
            return render_template_string(HTML_FORM, message=message)

        file = request.files['file'].read()
        signature = request.files['signature'].read()

        try:
            public_key.verify(
                signature,
                file,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            message = "✅ Chữ ký hợp lệ. File an toàn."
        except Exception as e:
            message = f"❌ Chữ ký không hợp lệ: {str(e)}"

    return render_template_string(HTML_FORM, message=message)

if __name__ == "__main__":
    app.run(debug=True)
