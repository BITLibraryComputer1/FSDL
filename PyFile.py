import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pyperclip

# Replace with your GitHub repository URL
GITHUB_URL = 'https://github.com/BITLibraryComputer1/FSDL/tree/main'
TARGET_DIR = 'downloaded_html_files'

def download_file(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to download: {url}")
        return None

def download_html_files(repo_url, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    response = requests.get(repo_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for link in soup.find_all('a'):
        href = link.get('href')
        if href.endswith('.html'):
            file_url = urljoin('https://raw.githubusercontent.com/', href.replace('/blob/', '/'))
            file_name = os.path.basename(file_url)
            file_contents = download_file(file_url)
            if file_contents:
                # Save the file locally (optional)
                with open(os.path.join(target_dir, file_name), 'w', encoding='utf-8') as file:
                    file.write(file_contents)
                # Copy the contents to the clipboard
                pyperclip.copy(file_contents)
                print(f"Copied to clipboard: {file_name}")

if __name__ == "__main__":
    download_html_files(GITHUB_URL, TARGET_DIR)
