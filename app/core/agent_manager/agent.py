import psutil
import os
import threading

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
    

def write_pid():
    pid = os.getpid()
    with open("agent.pid", "w") as f:
        f.write(str(pid))

from fastapi import FastAPI
from contextlib import asynccontextmanager
# https://fastapi.tiangolo.com/advanced/events/#lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    UsageMonitor.start_background_monitor()
    yield


write_pid()
app = FastAPI(lifespan=lifespan)

@app.get("/")
def usage():
    return UsageMonitor.get_usage()
    


