import { observer } from "mobx-react-lite";
import { syncStore } from "../../stores/SyncStore";
import { FaMemory } from "react-icons/fa";
import { LuCpu } from "react-icons/lu";
import { GrStorage } from "react-icons/gr";
export const ToolBar = observer (() => {
    const aggregate = syncStore.aggregate;

    const ramPercent = aggregate && aggregate.total_ram_total_gb > 0 
    ? Math.round((aggregate.total_ram_used_gb / aggregate.total_ram_total_gb) * 100) 
    : 0;

    const memPercent = aggregate && aggregate.total_storage_total_gb > 0 
    ? Math.round((aggregate.total_storage_used_gb / aggregate.total_storage_total_gb) * 100) 
    : 0;

    const formatStorage = (gb: number) => {
        if (gb >= 1000) {
            return `${(gb / 1000).toFixed(2)}TB`;
        }
        return `${gb.toFixed(1)}GB`;
    };
    
    return (
        <div className="flex justify-between w-full p-4">
            <div>
                <input type="search" placeholder="Search..."></input>
            </div>

            <div className="flex justify-between gap-3">
            
                <div className="flex items-center gap-2" title="CPU Usage">
                    <LuCpu/>
                    <span className="font-medium">{aggregate?.avg_cpu_percent ?? 0}%</span>
                </div>
                
                <div className="flex items-center gap-2" title="Memory">
                    <FaMemory/>
                    <span className="font-small">
                        {aggregate?.total_ram_used_gb ?? 0}GB/{aggregate?.total_ram_total_gb ?? 0}GB 
                        <span className="text-xs text-gray-400 ml-1">({ramPercent}%)</span>
                    </span>
                </div>
                
                <div className="flex items-center gap-2" title="Storage">
                    <GrStorage/>
                    <span className="font-small">
                        {aggregate?.total_storage_used_gb ?? 0}GB/{formatStorage(aggregate?.total_storage_total_gb ?? 0)}
                        <span className="text-xs text-gray-400 ml-1">({memPercent}%)</span>
                    </span>
                </div>
            </div>

        </div>
    )
});