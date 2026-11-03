import { observer } from "mobx-react-lite";
interface MachineTelemetryProps {
    avg_cpu_percent: number;
    total_ram: number;
    used_ram: number;
    total_storage?: number;
    used_storage?: number;
}

export const MachineTelemetry = observer(({avg_cpu_percent, total_ram, used_ram, total_storage, used_storage}: MachineTelemetryProps) => {

    const ramPercent = total_ram > 0 
    ? Math.round((used_ram / total_ram) * 100) 
    : 0;

    
    return (
        <div className="flex flex-col justify-between gap-3">
            
                <div className="flex items-center gap-2">
                    <span className="text-gray-400">CPU:</span>
                    <span className="font-medium">{avg_cpu_percent ?? 0}%</span>
                </div>
                
                <div className="flex items-center gap-2">
                    <span className="text-gray-400">Memory:</span>
                    <span className="font-medium">
                        {used_ram ?? 0}GB / {total_ram ?? 0}GB 
                        <span className="text-xs text-gray-400 ml-1">({ramPercent}%)</span>
                    </span>
                </div>
            </div>
    )
})