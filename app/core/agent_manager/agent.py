import psutil
import os
import threading
import docker
import requests
class ByteConverter:
    BYTE_BASE = 1000
    BIBYTE_BASE = 1024

    class decimal:
        SUFFIX = "B"
        @classmethod
        def to_terabyte(cls, bytes):
            return bytes / (ByteConverter.BYTE_BASE**4)
        @classmethod
        def to_gigabyte(cls, bytes):
            return bytes / ByteConverter.BIBYTE_BASE**3
        
    class binary:
        SUFFIX = "iB"
        @classmethod
        def to_tebibyte(cls, bytes):
            return bytes / ByteConverter.BIBYTE_BASE**4
        @classmethod
        def to_gibibyte(cls, bytes):
            return bytes / ByteConverter.BIBYTE_BASE**3
    
  
    


class UsageMonitor:
    _latest_stats = {}

    @staticmethod
    def start_background_monitor():
        """Starts a daemon thread to update stats every second."""
        thread = threading.Thread(target=UsageMonitor._update_usage, daemon=True)
        thread.start()

    @staticmethod
    def format_stat(usage_dict, byte_converter: ByteConverter, precision=2):
        for key in usage_dict:
            if key == 'percent':
                usage_dict[key] = f"{usage_dict[key]}%"
                continue
            conversion = byte_converter(usage_dict[key])
            size = f"TB"
            if conversion < 1:
                conversion *= 1000
                size = "GB"
            conversion = round(conversion, precision)
            usage_dict[key] = f"{conversion}{size}"

        return usage_dict


    @staticmethod
    def _update_usage():
        while True:
            drives = []
            for disk in psutil.disk_partitions():
                try:
                    disk_usage = UsageMonitor.format_stat(psutil.disk_usage(disk.mountpoint)._asdict(), ByteConverter.decimal.to_terabyte)
                    disk_usage["drive"] = disk.device
                    drives.append(disk_usage)
                except:
                    continue

            UsageMonitor._latest_stats = {
                "cpu": psutil.cpu_percent(interval=1),
                "memory": UsageMonitor.format_stat(psutil.virtual_memory()._asdict(), ByteConverter.binary.to_tebibyte),
                "drives": drives
                
            }
    
    @staticmethod
    def get_usage():
        return UsageMonitor._latest_stats
    
CONTROL_PLANE_HOST = None
def watch_docker_events():
    global CONTROL_PLANE_HOST
    try:
        client = docker.from_env()  # Automatically picks up unix://var/run/docker.sock
        print("Started watching local Docker events...")
        
       
        # This loop blocks and waits for events natively from the local socket
        for event in client.events(decode=True):
            # send request to control plane host
            print('event triggered')
            if CONTROL_PLANE_HOST:
                try:
                    print('sending host udpated!')
                    requests.post(f"http://{CONTROL_PLANE_HOST}:5000/docker/event", json=event, timeout=3)
                except Exception as e:
                    print(f"error sending event {e}")
            
                
    except Exception as e:
        print(f"Docker event listener crashed: {e}")

def write_pid():
    pid = os.getpid()
    with open("agent.pid", "w") as f:
        f.write(str(pid))

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

# https://fastapi.tiangolo.com/advanced/events/#lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=watch_docker_events, daemon=True)
    thread.start()
    UsageMonitor.start_background_monitor()
    yield


write_pid()
app = FastAPI(lifespan=lifespan)

@app.get("/")
def usage(request: Request): 
    global CONTROL_PLANE_HOST
    print(request.client)
    if CONTROL_PLANE_HOST is None:
        print('updated host')
        CONTROL_PLANE_HOST = request.client.host

    return UsageMonitor.get_usage()
    


