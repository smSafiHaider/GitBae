import requests
import os

from dotenv import load_dotenv

load_dotenv()

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")


def get_repo_info(owner: str, repo: str):
    """
    Retrieves information about a GitHub repository.

    Args:
        owner (str): The username or organization name that owns the repository.
        repo (str): The name of the repository.

    Returns:
        dict: A dictionary containing information about the repository.
              The dictionary keys include 'name', 'description', 'owner', 'html_url', 'default_branch', and more.
              For detailed information, refer to the GitHub API documentation: https://docs.github.com/en/rest/reference/repos#get-a-repository
    """
    
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_repo_contents(owner: str, repo: str, path: str="", branch: str="main"):
    """
    Retrieves the contents of a file or directory in a GitHub repository.

    Args:
        owner (str): The username or organization name that owns the repository.
        repo (str): The name of the repository.
        path (str): The path to the file or directory in the repository.
        branch (str): The branch name. Default is 'main'.

    Returns:
        list: A list of dictionaries, where each dictionary represents a file or directory.
              The dictionary keys include 'name', 'path', 'type', 'download_url', and more.
              For detailed information, refer to the GitHub API documentation: https://docs.github.com/en/rest/reference/repos#get-repository-content
    """
    
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 401:
        print("Unauthorized: Check your GitHub token.")
    elif response.status_code == 403:
        print("Forbidden: The token might have the correct permissions but the request is being rate limited or access is restricted.")
    elif response.status_code == 404:
        print("Not Found: Check the repository details (owner/repo/path).")
    
    response.raise_for_status()
    return response.json()

def read_file_content(url: str):
    """
    Reads the content of a file from a URL.

    Args:
        url (str): The URL of the file to read.

    Returns:
        str: The content of the file.
    """
    
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.content.decode("utf-8")