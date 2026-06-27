import paramiko
import os
from dotenv import load_dotenv

def install_agent(hostname, user, os_type, port=22):
    load_dotenv()
    # connect with SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=port,  username=user, key_filename=os.environ.get("KEY_PATH"))


    install_dir = f"/home/{user}/overwatch-agent"
    setup_script = 'setup.sh'

    if os_type == "windows":
        install_dir = f'C:/overwatch-agent'
        setup_script = 'setup.ps1'

    local_dir = os.path.join(os.getcwd(), 'app/core/agent_manager/')
    print('installing', install_dir)
    # Copy src code
    with client.open_sftp() as sftp:
        try:
            print("making dir at", install_dir)
            sftp.mkdir(install_dir)
        except IOError:
            pass
        local = os.path.join(local_dir, 'agent.py')
        remote = f'{install_dir}/agent.py'
        print('added main')
        sftp.put(local, remote)
        remote = f'{install_dir}/{setup_script}'
        local = os.path.join(local_dir, setup_script)
        sftp.put(local, remote)
        print('added script')
        remote = f'{install_dir}/requirements.txt'
        local = os.path.join(local_dir, 'requirements.txt')
        sftp.put(local, remote)
        print('added requirements')
    # if os_type == "windows":
    #     # start agent
    #     cmd = f"""powershell "powershell -ExecutionPolicy Bypass -File {install_dir}/{setup_script}" """
    #     stdin, stdout, stderr = client.exec_command(cmd)

    #     print(stdout.read().decode())
    #     print(stderr.read().decode())
    client.close()