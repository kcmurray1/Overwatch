import paramiko
import os
from dotenv import load_dotenv
from app.serializer import Machine

class AgentManager:
    @staticmethod
    def get_installation_info(os_type, user):
        if os_type == "windows":
            return (
                f'C:/overwatch-agent',
                'setup.ps1'
            )
        elif os_type == "linux":
            return (
                f"/home/{user}/overwatch-agent",
                'setup.sh'
            )
        

    @staticmethod
    def install(machine_model: Machine):
        """
        Install local hardware reporting agent to target machine
        NOTE: Linux Machines require manual run of setup.sh to approve installation of dependencies
        """
        load_dotenv()

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=machine_model.address, port=machine_model.port,username=machine_model.user, key_filename=os.environ.get("KEY_PATH"))

        # move agent files to machine
        install_dir, setup_script = AgentManager.get_installation_info(machine_model.os_type, machine_model.user)


        local_dir = os.path.join(os.getcwd(), 'app/core/agent_manager/')
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

            if machine_model.os_type == "windows":
                # start agent
                cmd = f"""powershell "powershell -ExecutionPolicy Bypass -File {install_dir}/{setup_script}" """
                stdin, stdout, stderr = client.exec_command(cmd)

                print(stdout.read().decode())
                print(stderr.read().decode())
        client.close()
    