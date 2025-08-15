# PixCrypt – Hide & Recover Files in Images

## Overview

PixCrypt is a Python + Flask-based application that allows you to **securely hide entire files or folders inside image files** and later **recover them**.  
It is designed for scenarios where sensitive data needs to be **hidden in plain sight** using steganography.

## Features

- **Encrypt Files & Folders** into PNG images.
- **Decrypt & Recover** hidden files/folders from images.
- **Preserve Original Directory Structure** during encryption and decryption.
- **Password Protection** for enhanced security.
- **Simple Web Interface** for easy usage.
- **Cross-Platform Support** (Windows, macOS, Linux).

## Technologies Used

- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS
- **Libraries:** `Pillow`, `pyzipper`, `werkzeug`
- **Platform:** Cross-platform (runs locally or can be deployed)

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- pip (Python package installer)
- Git

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # On Linux/Mac:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   flask run
   ```

5. Open your browser and visit:

   ```
   http://127.0.0.1:5000
   ```

## Project Structure

```
project/
│
├── app/
│   ├── routes/              # Flask route handlers
│   ├── static/              # CSS & static assets
│   ├── templates/           # HTML templates
│   ├── uploads/             # Uploaded & processed files
│   ├── stego_tools.py       # Encryption logic
│   ├── reverse_tools.py     # Decryption logic
│   └── __init__.py          # App initialization
│
├── requirements.txt         # Python dependencies
├── .gitignore               # Ignored files/folders
├── run.py                   # Application entry point
└── README.md                # Documentation
```

## Usage

1. Open the tool in your browser.
2. **To Encrypt**:

   - Choose a file or folder.
   - Select an image to embed the data.
   - Enter a password.
   - Download the generated encrypted image.

3. **To Decrypt**:

   - Upload the encrypted image.
   - Enter the password.
   - Download the recovered folder.

## Security Notes

- Use strong passwords to protect your hidden data.
- This tool is intended for legal and ethical use only.
- Always verify the integrity of recovered files.

## Contribution Guidelines

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit changes with meaningful messages.
4. Submit a pull request with a clear explanation.

```

---


```

```

```
