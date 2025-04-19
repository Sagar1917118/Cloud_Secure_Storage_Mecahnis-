# 🔐 Cloud Secure Storage Mechanism (CSSM)

A secure, distributed cloud storage system that combines **AES encryption**, **Shamir’s Secret Sharing**, and **Flask-based API** to safely store and retrieve files in a **modular**, **scalable**, and **highly secure** environment. The backend leverages **Node.js**, **Python**, **Flask**, and **Amazon S3** for distributed storage.
![image](https://github.com/user-attachments/assets/e29e6731-acd0-4ba7-9625-54cf6e748bd5)

---

## 🚀 Features

- 🔒 AES-256 Encryption for file confidentiality
- 🪓 File Dispersion into multiple encrypted chunks
- 🔑 Key Management & Distribution using a Shamir-based secret sharing algorithm
- 🧩 User Password-Based Protection of key shares
- 🌐 RESTful API built with Flask for uploading and encrypting files
- ☁️ S3-Compatible Storage for scalable, cloud-based file storage
- ⚙️ Modular Code Structure (Python services split across AES, dispersion, and key management)

---

## 🧰 Tech Stack

| Layer            | Technology         |
|------------------|--------------------|
| API Server       | Python, Flask      |
| Encryption       | AES (PyCryptodome) |
| Key Distribution | Shamir's Secret Sharing |
| Cloud Storage    | Amazon S3 / S3-compatible API |
| Client Services  | Node.js (optional frontend or CLI) |
| Other Libs       | `hmac`, `hashlib`, `os`, `time`, `base64` |

---

## 🛠️ Setup Instructions

### ✅ Prerequisites
- Python 3.10+
- pip
- Node.js (optional)
- AWS CLI configured (or use MinIO for S3-compatible local storage)

### 📦 Python Dependencies
Install Python packages:

```bash
pip install -r requirements.txt
Example requirements.txt:

txt
Copy
Edit
Flask==2.3.2
pycryptodome==3.19.0
shamir-mnemonic==0.2.0  # or use a custom Shamir utility
📁 Project Structure
php
Copy
Edit
.
├── app.py                       # Flask API entrypoint
├── services/
│   ├── disperser.py             # Splits file into 5 parts
│   ├── aes_handler.py           # Encrypts file parts with AES
│   └── container_key_manager.py # Handles key generation + sharing
├── utils/
│   └── shamir_utils.py          # Secret sharing functions (if needed)
├── templates/                   # (Optional) Flask UI
├── static/                      # (Optional) Frontend assets
└── README.md
📤 API Usage
POST /upload
Form-Data:

file: File to upload

password: User password to encrypt secret shares

Response:

json
Copy
Edit
{
  "message": "File uploaded, encrypted, and shares generated successfully.",
  "base_filename": "file_1712727385",
  "encrypted_parts": [
    "file_1712727385_part1.enc",
    "file_1712727385_part2.enc",
    ...
  ],
  "object_key_file": "file_1712727385_object_keys.key",
  "container_key_encrypted": "file_1712727385_container_key.enc",
  "share_files": [
    "file_1712727385_share1.enc",
    "file_1712727385_share2.enc",
    ...
  ]
}
🔒 Security Highlights
Each file part is encrypted with a unique AES key

All AES keys are stored in an Object Key Box, encrypted with a Container Key

The Container Key is split using Shamir’s Secret Sharing (3-of-5)

The 5 secret shares are individually encrypted using keys derived from the user's password

🧪 To-Do / Future Additions
 Add decryption API endpoint

 Store file metadata in a database (MongoDB or PostgreSQL)

 Build a Node.js CLI for upload/download

 Add a frontend dashboard for secure file access

 Implement S3 auto-cleaning and logging

🧑‍💻 Author
Developed by Sagar Kumar — Cloud Security & Full-Stack Developer ☁️🔐
