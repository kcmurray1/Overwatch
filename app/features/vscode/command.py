

def launch_vscode(host, address,user, os_type):
    """Open vscode-remote at user's directory"""
    user_dir = None
    if os_type == "windows":
        user_dir = f'C:/Users/{user}'
    if os_type == "linux":
        user_dir = f'home/{user}'
    # used to open vscode in a new window nearhttps://github.com/microsoft/vscode-remote-release/issues/10650 
    return f"""vscode://vscode-remote/ssh-remote+{host}@{address}/{user_dir}/dir?windowId=_blank"""