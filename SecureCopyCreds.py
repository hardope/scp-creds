import streamlit as st
import requests

API_BASE_URL = "https://scp-env.onrender.com"  # Update with your FastAPI URL

st.title("Secure Credentials File Sharing")

# Main menu
option = st.selectbox("Choose an option", ["Select Action Upload / Download","Create Credential File", "Download Credential File"])

if option == "Create Credential File":
    # Upload Section
    st.header("Upload Credential File")
    uploaded_file = st.file_uploader("Choose your file", type=["env", "txt", "*", "json"])

    download_limit = st.number_input("Download Limit", value=1, min_value=1, step=1)
    expiration_time = st.number_input("Expiration Time (in minutes)", value=5, min_value=1, step=1)

    if uploaded_file is not None:
        if st.button("Upload File"):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                response = requests.post(f"{API_BASE_URL}/upload", files=files, data = {
                    "download_limit": download_limit,
                    "expiration_time": expiration_time
                })
                if response.status_code == 200:
                    result = response.json()
                    download_code = result.get("download_code")
                    decryption_key = result.get("decryption_key")
                    st.success(f"File uploaded successfully! Find your download code and decryption key below.")
                    st.write("Download Code")
                    st.code(download_code, language="plaintext")
                    st.write("Decryption Key")
                    st.code(decryption_key, language="plaintext")
                    st.info("Save this decryption key securely. You will need it to download your file.")
                else:
                    st.error(f"Failed to upload file: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    # Upload Text Section
    st.header("Upload Credentials Text Content")
    env_text_content = st.text_area("Enter your credentials file content here")

    if env_text_content:
        if st.button("Upload Text Content"):
            try:
                response = requests.post(f"{API_BASE_URL}/upload_text", data={
                    "file_content": env_text_content,
                    "download_limit": download_limit,
                    "expiration_time": expiration_time

                })
                if response.status_code == 200:
                    result = response.json()
                    download_code = result.get("download_code")
                    decryption_key = result.get("decryption_key")
                    st.success(f"File uploaded successfully! Find your download code and decryption key below.")
                    st.write("Download Code")
                    st.code(download_code, language="plaintext")
                    st.write("Decryption Key")
                    st.code(decryption_key, language="plaintext")
                    st.info("Save this decryption key securely. You will need it to download your file.")
                else:
                    st.error(f"Failed to upload text content: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

elif option == "Download Credential File":
    # Download Section
    st.header("Download Credential File")
    download_code = st.text_input("Enter your download code")
    decryption_key = st.text_input("Enter your decryption key")

    if st.button("Download File"):
        if download_code and decryption_key:
            try:
                params = {"decryption_key": decryption_key}
                response = requests.get(f"{API_BASE_URL}/download/{download_code}", params=params, stream=True)
                if response.status_code == 200:
                    st.success("File downloaded successfully!")
                    st.download_button(
                        label="Download Credemtials file",
                        data=response.content,
                        file_name="credentials.txt",
                        mime="application/octet-stream"
                    )
                else:
                    st.error(f"Failed to download file: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.error("Please enter both a valid download code and decryption key.")

else:

    st.header("Select Action Upload / Download")
    st.write("This web app allows you to securely share env files or credentials with others. "
             "You can either upload a file or enter the content directly, and you will receive a download code and decryption key. "
             "To download a file, provide the download code and decryption key.")