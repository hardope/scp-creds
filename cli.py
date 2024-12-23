import argparse
import requests
import os
import sys

def upload_env_file(file_path, download_limit, expiration_time):
    SERVER_URL = "https://scp-env.onrender.com"
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)

    try:
        with open(file_path, 'rb') as file:
            response = requests.post(
                f"{SERVER_URL}/upload",
                files={"file": file},
                data={"download_limit": download_limit, "expiration_time": expiration_time}
            )
    except Exception as e:
        print(f"Unable to Upload file: {str(e)}")
        sys.exit(1)

    try:
        if response.status_code == 200:
            data = response.json()
            print("File uploaded successfully!")
            print(f"Download Code: {data.get('download_code')}")
            print(f"Decryption Key: {data.get('decryption_key')}")
        else:
            print(f"Error uploading file: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def upload_env_text(env_text, download_limit, expiration_time):
    SERVER_URL = "https://scp-env.onrender.com"
    try:
        response = requests.post(
            f"{SERVER_URL}/upload_text",
            data={"file_content": env_text, "download_limit": download_limit, "expiration_time": expiration_time}
        )

        if response.status_code == 200:
            data = response.json()
            print("Credentials uploaded successfully!")
            print(f"Download Code: {data.get('download_code')}")
            print(f"Decryption Key: {data.get('decryption_key')}")
        else:
            print(f"Error uploading Credentials: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Unable to upload Credentials: {str(e)}")

def download_env_file(code, decryption_key, output_path):
    SERVER_URL = "https://scp-env.onrender.com"
    try:
        response = requests.get(f"{SERVER_URL}/download/{code}", params={"decryption_key": decryption_key})

        if response.status_code == 200:
            with open(output_path, 'wb') as file:
                file.write(response.content)
            print(f"File downloaded successfully to '{output_path}'.")
        else:
            print(f"Error downloading file: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Unable to download file: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="CLI for securely sharing .env files.")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Upload file command
    upload_file_parser = subparsers.add_parser("upload-file", help="Upload a .env file.")
    upload_file_parser.add_argument("--file", required=True, help="Path to the .env file to upload.")
    upload_file_parser.add_argument("--limit", type=int, default=1, help="Download limit for the file.")
    upload_file_parser.add_argument("--expire", type=int, default=5, help="Expiration time (in minutes) for the file.")

    # Upload text command
    upload_text_parser = subparsers.add_parser("upload-text", help="Upload Credentials as text.")
    upload_text_parser.add_argument("--text", required=True, help="Credentials in text format.")
    upload_text_parser.add_argument("--limit", type=int, default=1, help="Download limit for the file.")
    upload_text_parser.add_argument("--expire", type=int, default=5, help="Expiration time (in minutes) for the file.")

    # Download file command
    download_parser = subparsers.add_parser("download", help="Download a .env file.")
    download_parser.add_argument("--code", required=True, help="Download code for the file.")
    download_parser.add_argument("--key", required=True, help="Decryption key for the file.")
    download_parser.add_argument("--output", required=True, help="Path to save the downloaded .env file.")

    args = parser.parse_args()

    if args.command == "upload-file":
        upload_env_file(args.file, args.limit, args.expire)
    elif args.command == "upload-text":
        upload_env_text(args.text, args.limit, args.expire)
    elif args.command == "download":
        download_env_file(args.code, args.key, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
