# SCP-Creds CLI

This project is a Python-based CLI tool and Web APP for securely sharing `.env` files and environment variable and general credentials. The tool allows users to upload `.env` or credential files or text, encrypt them, and generate access codes for secure download. It also supports downloading the encrypted files using the generated codes. Additionally, a Streamlit-based UI is available for users who prefer a graphical interface.

## Features
- **Upload Credential Files**: Upload a `.env` file to a secure server with a download limit and expiration time.
- **Upload Text Credentials**: Securely upload environment variables in text format.
- **Download Files**: Download previously uploaded `.env` or creds files using a download code and decryption key.
- **Expiration and Limits**: Set download limits and expiration times to ensure security.
- **Streamlit UI**: A web-based UI for uploading and managing environment files conveniently.

## Installation

### For Windows
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/scp-creds.git
   cd scp-creds
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the CLI with Python:
   ```bash
   python cli.py
   ```

### For Linux
1. Download the installer:
   ```bash
   git clone https://github.com/yourusername/scp-creds.git
   cd scp-creds
   ```
2. Make the installer executable:
   ```bash
   chmod +x installer.sh
   ```
3. Run the installer:
   ```bash
   ./installer.sh
   ```
4. After installation, use the CLI:
   ```bash
   scp-creds
   ```

## Usage
The CLI provides three main commands: `upload-file`, `upload-text`, and `download`.

### 1. Upload a `.env` File
Uploads a `.env` file to the secure server.
```bash
python cli.py upload-file --file <path_to_file> --limit <download_limit> --expire <expiration_time>
```
**Arguments:**
- `--file`: Path to the `.env` file to upload (required).
- `--limit`: Download limit for the file (default: 1).
- `--expire`: Expiration time in minutes (default: 5).

### 2. Upload Text Credentials
Uploads environment variable credentials as plain text.
```bash
python cli.py upload-text --text "<environment_variables>" --limit <download_limit> --expire <expiration_time>
```
**Arguments:**
- `--text`: Environment variables in text format (required).
- `--limit`: Download limit for the file (default: 1).
- `--expire`: Expiration time in minutes (default: 5).

### 3. Download a File
Downloads a `.env` file using a download code and decryption key.
```bash
python cli.py download --code <download_code> --key <decryption_key> --output <output_path>
```
**Arguments:**
- `--code`: Download code provided during upload (required).
- `--key`: Decryption key provided during upload (required).
- `--output`: Path to save the downloaded `.env` file (required).

## Streamlit UI
SCP-Creds also includes a Streamlit-based web application for users who prefer a graphical interface. The UI supports all the features of the CLI, including uploading `.env` files or text, setting expiration times, and downloading files.

### Running the Streamlit UI
1. Install Streamlit:
   ```bash
   pip install streamlit
   ```
2. Start the Streamlit app:
   ```bash
   streamlit run SecureCopyCreds.py
   ```
3. Open the provided URL in your browser to access the UI.

## Example Commands
- **Upload a file:**
  ```bash
  python cli.py upload-file --file my_env_file.env --limit 3 --expire 10
  ```
- **Upload text credentials:**
  ```bash
  scp-creds upload-text --text "API_KEY=12345\nSECRET_KEY=abcde" --limit 5 --expire 15
  ```
- **Download a file:**
  ```bash
  python cli.py download --code 123456 --key ABCDEF123 --output downloaded.env
  ```

## Requirements
- Python 3.7+
- `requests` library
- `tqdm` (optional, for progress bars)
- `streamlit` (optional, for the UI)

Install the dependencies with:
```bash
pip install -r requirements.txt
```

## Notes
- The server URL is set to `https://scp-env.onrender.com`. Update the `SERVER_URL` variable in the script if needed.
- The streamlit UI is available at `https://scp-creds.streamlit.app`
- Ensure that the server supports the endpoints `/upload`, `/upload_text`, and `/download/{code}` as required by the tool.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

## License
This project is licensed under the [MIT License](LICENSE).

---

Happy sharing securely!

