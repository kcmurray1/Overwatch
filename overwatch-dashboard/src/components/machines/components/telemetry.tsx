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

    // const memPercent = total_storage > 0 
    // ? Math.round((used_storage / total_storage) * 100) 
    // : 0;

    const formatStorage = (gb: number) => {
        if (gb >= 1000) {
            return `${(gb / 1000).toFixed(2)}TB`;
        }
        return `${gb.toFixed(1)}GB`;
    };
    
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
                
                {/* <div className="flex items-center gap-2">
                    <span className="text-gray-400">Storage Used:</span>
                    <span className="font-medium">
                        {total_storage ?? 0}GB/{formatStorage(total_storage ?? 0)}
                        <span className="text-xs text-gray-400 ml-1">({memPercent}%)</span>
                    </span>
                </div> */}
            </div>
    )
})