import os, json, webbrowser, subprocess

from utils.voice_answers import run_voice

def find_chrome_bookmarks():
    path = os.path.join(
        os.environ["LOCALAPPDATA"],
        "Google",
        "Chrome",
        "User Data",
        "Default",
        "Bookmarks"
    )

    if not os.path.exists(path):
        raise FileNotFoundError("Bookmarks file not found")

    return path


def load_bookmarks():
    path = find_chrome_bookmarks()
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_all_folders():
    data = load_bookmarks()
    folders = []

    def walk(node, path=""):
        if node.get("type") == "folder":
            current = f"{path}/{node['name']}" if path else node["name"]
            folders.append(current)

            for child in node.get("children", []):
                walk(child, current)

    for root in data["roots"].values():
        walk(root)

    return folders


def open_folder(folder_name):
    run_voice(f"Відкриваю папку: {folder_name}")
    data = load_bookmarks()

    def find(node):
        if node.get("type") == "folder" and node.get("name") == folder_name:
            return node

        for child in node.get("children", []):
            result = find(child)
            if result:
                return result

        return None

    for root in data["roots"].values():
        folder = find(root)
        if folder:
            for item in folder.get("children", []):
                if item["type"] == "url":
                    webbrowser.open_new_tab(item["url"])
            return

    print("Folder not found")


def open_site_in_profile(profile_name="Default", url_name: str = "https://"):   
    if "." in url_name:
        run_voice(f"Відкриваю сайт: {url_name.split(".")[-2]}") 
    else:
        run_voice(f"Відкриваю профіль: {profile_name}") 
    user_data_dir = os.path.join(
        os.environ["LOCALAPPDATA"],
        "Google",
        "Chrome",
        "User Data"
    )

    profile_path = os.path.join(user_data_dir, profile_name)
    
    if not os.path.exists(profile_path):
        raise FileNotFoundError(f"Профіля {profile_name} не знайдено")

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    url = url_name

    subprocess.Popen([chrome_path, f'--user-data-dir={user_data_dir}', f'--profile-directory={profile_name}', url])

