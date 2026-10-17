class ContainerUtils:
    """Methods to parse Docker Container attributes
    NOTE: for reference these are the keys for container attributes
    ['Id', 'Created', 'Path', 'Args', 'State', 'Image', 'ResolvConfPath', 'HostnamePath', 
     'HostsPath', 'LogPath', 'Name', 'RestartCount', 'Driver', 'Platform', 'MountLabel', 
     'ProcessLabel', 'AppArmorProfile', 'ExecIDs', 'HostConfig', 'Storage', 'Mounts', 'Config', 
     'NetworkSettings', 'ImageManifestDescriptor']
    """
    @staticmethod
    def get_published_ports(container_attrs):
        ports_binding = container_attrs.get("NetworkSettings")
        if ports_binding:
        
            for port, hosts in ports_binding.get("Ports").items():
                if not hosts:
                    continue
                # print(port, hosts)
                for host in hosts:
                    if host.get('HostIp') == '0.0.0.0':
                        return host.get('HostPort')
        
        
        return None
    @staticmethod
    def get_url(container_attr, host):
        return f"http://{host}:{ContainerUtils.get_published_ports(container_attrs=container_attr)}"
        
        