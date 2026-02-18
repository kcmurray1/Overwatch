from abc import ABC, abstractmethod


class BaseOS(ABC):
    """Base class functionality that subclass operating systems must support"""
    COMMANDS = {
        "SYS_INFO",
        "PROCESSES",
        "UPTIME"
    }

    def __init_subclass__(cls):
        """Enforce subclass to implement basic commands"""
        subclass_Commands = getattr(cls, 'COMMANDS', {})
        

        # verify that subclass contains required commands
        missing_cmds = set(cls.COMMANDS) - set(subclass_Commands.keys())
        if missing_cmds:
            raise TypeError(f"{cls.__name__} missing commands: {missing_cmds}")
        
        return super().__init_subclass__()

    @abstractmethod
    def get_system_info(self, exec_func):
        """Report Hardware, OS, Network Devices, etc."""
        pass

    @abstractmethod
    def get_processes(self, exect_func):
        """Get running applications/services"""
        pass
    
    @abstractmethod
    def restart(self, exec_func):
        """Restart machine"""
        pass

    @abstractmethod
    def stop(self, exec_func):
        """Stop machine"""
        pass

    @abstractmethod
    def install_tailscale(self, exec_func, hostname, access_token):
        return NotImplementedError