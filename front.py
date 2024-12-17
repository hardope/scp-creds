import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"  # Update with your FastAPI URL

st.title("Secure .env File Sharing")

# Upload Section
st.header("Upload .env File")
uploaded_file = st.file_uploader("Choose your file", type=["env", "py", "txt", "*"])

if uploaded_file is not None:
    if st.button("Upload File"):
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            response = requests.post(f"{API_BASE_URL}/upload", files=files)
            if response.status_code == 200:
                result = response.json()
                download_code = result.get("download_code")
                decryption_key = result.get("decryption_key")
                st.success(f"File uploaded successfully! Your download code is: {download_code}")
                st.code(decryption_key, language="plaintext")
                st.info("Save this decryption key securely. You will need it to download your file.")
            else:
                st.error(f"Failed to upload file: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Upload Text Section
st.header("Upload .env Text Content")
env_text_content = st.text_area("Enter your .env file content here")

if env_text_content:
    if st.button("Upload Text Content"):
        try:
            response = requests.post(f"{API_BASE_URL}/upload_text", data={"file_content": env_text_content})
            if response.status_code == 200:
                result = response.json()
                download_code = result.get("download_code")
                decryption_key = result.get("decryption_key")
                st.success(f"Text content uploaded successfully! Your download code is: {download_code}")
                st.code(decryption_key, language="plaintext")
                st.info("Save this decryption key securely. You will need it to download your file.")
            else:
                st.error(f"Failed to upload text content: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Download Section
st.header("Download .env File")
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
                    label="Download .env file",
                    data=response.content,
                    file_name="env_file.env",
                    mime="application/octet-stream"
                )
            else:
                st.error(f"Failed to download file: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please enter both a valid download code and decryption key.")
