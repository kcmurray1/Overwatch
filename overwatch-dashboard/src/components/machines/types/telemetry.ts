

interface MachineDrives {
    drive: string;
    mountpoint: string;
    total_gb: number;
    used_gb: number;
}

export interface MachineTelemetry {
    stats: {
        cpu: number;
        memory: {total_gb: number, used_gb: number};
        drives: MachineDrives[]
    }
    id: number
    name: string
}


export interface AggregateStats {
  avg_cpu_percent: number;
  total_ram_used_gb: number;
  total_ram_total_gb: number;
  total_storage_used_gb: number;
  total_storage_total_gb: number;
}