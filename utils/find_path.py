import os, subprocess, platform

def find_path(filename: str):
    if filename.endswith(".exe"):
        filename = filename[:-4]
        
    system = platform.system()
    try:
        if system == 'Windows':
            command = f"where {filename}.exe"
        else:
            command = f"which {filename}"
        
        result = subprocess.run(
            command, 
            capture_output= True, 
            text= True
        )
    
        list_path = result.stdout.split("\n")
        file = list_path[0].strip()
        if file != '':
            if os.path.exists(file):
                return file
    except:
        pass
    
    if system == 'Windows':
        extentions = [".exe"]

        system_dirs = [
            os.environ.get("APPDATA"),
            os.environ.get("LOCALAPPDATA"),
            os.environ.get("PROGRAMFILES"),
            os.environ.get("PROGRAMFILES(X86)"),
            os.path.join(str(os.environ.get("SYSTEMROOT")), "System32")
        ]

    else:
        extentions = ["", ".app"]

        system_dirs = [
            "/usr/bin",
            "/usr/local/bin",
            "/Applications",
            os.path.expanduser("~/SmtFolder")
        ]

    for root_dir in system_dirs:
        root_dir = str(root_dir)

        if not os.path.exists(root_dir):
            continue

        for current_path, inside_dirs, files in os.walk(root_dir):
            for file in files:
                for extention in extentions:
                    if file.lower() == filename.lower() + extention:
                        return os.path.join(current_path, file)
            if current_path.count(os.sep) > root_dir.count(os.sep) + 3:
                inside_dirs.clear()
        
apps = [
    "telegram",
    "chrome",
    "code",
]

for app in apps:
    print(find_path(filename= app))


# find_path(filename= "python")
