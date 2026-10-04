from fastapi import APIRouter, Depends, Query
import threading
import psutil

router = APIRouter(
    prefix="/system",
    tags=["system"]
)


class ByteConverter:
    BYTE_BASE = 1000
    BIBYTE_BASE = 1024

    class decimal:
        SUFFIX = "B"

        @classmethod
        def to_terabyte(cls, byte_val: float) -> float:
            return byte_val / (ByteConverter.BYTE_BASE**4)

        @classmethod
        def to_gigabyte(cls, byte_val: float) -> float:
            return byte_val / (ByteConverter.BYTE_BASE**3)

    class binary:
        SUFFIX = "iB"

        @classmethod
        def to_tebibyte(cls, byte_val: float) -> float:
            return byte_val / (ByteConverter.BIBYTE_BASE**4)

        @classmethod
        def to_gibibyte(cls, byte_val: float) -> float:
            return byte_val / (ByteConverter.BIBYTE_BASE**3)


class UsageMonitor:
    _latest_stats: dict = {}

    @staticmethod
    def start_background_monitor():
        """Starts a daemon thread to update system stats every second."""
        thread = threading.Thread(target=UsageMonitor._update_usage, daemon=True)
        thread.start()

    @staticmethod
    def format_stat(usage_dict: dict, conversion_fn, precision: int = 2) -> dict:
        formatted = usage_dict.copy()
        for key, val in formatted.items():
            if key == "percent":
                formatted[key] = f"{val}%"
                continue
            if isinstance(val, (int, float)):
                conversion = conversion_fn(val)
                size = "TB"
                if conversion < 1:
                    conversion *= 1000
                    size = "GB"
                formatted[key] = f"{round(conversion, precision)}{size}"
        return formatted

    @classmethod
    def _update_usage(cls):
        while True:
            drives = []
            for disk in psutil.disk_partitions(all=False):
                try:
                    disk_usage = cls.format_stat(
                        psutil.disk_usage(disk.mountpoint)._asdict(),
                        ByteConverter.decimal.to_terabyte,
                    )
                    disk_usage["drive"] = disk.device
                    disk_usage["mountpoint"] = disk.mountpoint
                    drives.append(disk_usage)
                except Exception:
                    continue

            cls._latest_stats = {
                "cpu": psutil.cpu_percent(interval=1),
                "memory": cls.format_stat(
                    psutil.virtual_memory()._asdict(),
                    ByteConverter.binary.to_tebibyte,
                ),
                "drives": drives,
            }

    @classmethod
    def get_usage(cls) -> dict:
        return cls._latest_stats


@router.get("/usage")
def get_system_usage():
    """Returns the latest buffered system stats."""
    return UsageMonitor.get_usage()