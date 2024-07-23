import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Replace with your GitHub repository URL
GITHUB_URL = 'https://github.com/username/repository'
TARGET_DIR = 'downloaded_html_files'

def download_file(url, target_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(target_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {url}")
    else:
        print(f"Failed to download: {url}")

def download_html_files(repo_url, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    repo_url = repo_url.rstrip('/') + '/tree/main'  # Adjust for your repository structure
    response = requests.get(repo_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for link in soup.find_all('a'):
        href = link.get('href')
        if href.endswith('.html'):
            file_url = urljoin('https://raw.githubusercontent.com/', href.replace('/blob/', '/'))
            file_name = os.path.basename(file_url)
            download_file(file_url, os.path.join(target_dir, file_name))

if __name__ == "__main__":
    download_html_files(GITHUB_URL, TARGET_DIR)
