import paramiko


class MachineManager:
    @staticmethod
    def get_uptime(ssh_client, machine=None):
        cmd = """systeminfo | find "System Boot Time" """
        return MachineManager._execute(ssh_client, cmd)
        



    def get_running_services(ssh_client, machine):
        pass

    def get_status(ssh_client : paramiko.SSHClient, machine=None):
        uptime = MachineManager.get_uptime(ssh_client)

        print(uptime, type(uptime))
        return {"uptime" : uptime}

    
    @staticmethod
    def _execute(client, command):
        stdin, stdout, stderr = client.exec_command(command)

        return stdout.read().decode().strip()


