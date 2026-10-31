import { observer } from "mobx-react-lite";
import React, { useEffect, useState } from "react";
import { FaPlay, FaPlus, FaStop } from "react-icons/fa";
import { CustomApiRequest, type APIResponse } from "../../FetchAPI";

interface AggregateStats {
  avg_cpu_percent: number;
  total_ram_used_gb: number;
  total_ram_total_gb: number;
  total_storage_used_gb: number;
  total_storage_total_gb: number;
}

export const ToolBar = observer (() => {
    const [aggregate, setAggregate] = useState<AggregateStats | null>(null);

    useEffect(() => {
        const fetchStats = async () => {
        try {
            const res = await CustomApiRequest<APIResponse<{individual: number, aggregate: AggregateStats}>>("machines/stats", null, "GET");
            if (res.data) {
                setAggregate(res.data.aggregate);
            }
            
        } catch (err) {
            console.error("Failed to fetch cluster telemetry", err);
        }
        };

        fetchStats();
        const interval = setInterval(fetchStats, 3000); // poll every 3s
        return () => clearInterval(interval);
    }, []);

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
            
            <div className="flex items-center gap-2">
                <span className="text-gray-400">CPU:</span>
                <span className="font-medium">{aggregate?.avg_cpu_percent ?? 0}%</span>
            </div>
            
            <div className="flex items-center gap-2">
                <span className="text-gray-400">Memory:</span>
                <span className="font-medium">
                    {aggregate?.total_ram_used_gb ?? 0}GB / {aggregate?.total_ram_total_gb ?? 0}GB 
                    <span className="text-xs text-gray-400 ml-1">({ramPercent}%)</span>
                </span>
            </div>
            
            <div className="flex items-center gap-2">
                <span className="text-gray-400">Storage Used:</span>
                <span className="font-medium">
                    {aggregate?.total_storage_used_gb ?? 0}GB/{formatStorage(aggregate?.total_storage_total_gb ?? 0)}
                    <span className="text-xs text-gray-400 ml-1">({memPercent}%)</span>
                </span>
            </div>
            </div>

        </div>
    )
});