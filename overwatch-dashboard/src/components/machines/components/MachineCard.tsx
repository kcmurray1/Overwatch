import { observer } from "mobx-react-lite";
import { BaseCard } from "../../common/BaseCard";
import { GrStatusGoodSmall, GrStatusUnknown, GrUpgrade } from "react-icons/gr";
import { FaLinux, FaPray, FaTrash, FaWindows } from "react-icons/fa";
import { machineStore } from "../../../stores/MachineStore";
import type { IMachine } from "../../../types/machines";
import { useState } from "react";
import { VscVscode } from "react-icons/vsc";
import { syncStore } from "../../../stores/SyncStore";
import { MachineTelemetry } from "./telemetry";

export const MachineInfo = observer(({ machine }: { machine: IMachine }) => {
    return (
        <div className="flex flex-col min-w-0">
            <span className="text-xs uppercase truncate">
                {machine.user}
            </span>
            <span className="truncate text-sm">
                {machine.model}
            </span>
            <span className="text-xs font-mono truncate" title={machine.cpu}>
                {machine.cpu}
            </span>
        </div>
    );
});

const MachineNetwork = observer(({machine}: {machine: IMachine}) => {
    const [copiedText, setCopiedText] = useState<string| null>(null);

    const handleCopy = (e: React.MouseEvent, text:string, label: string) => {
        e.stopPropagation();
        navigator.clipboard.writeText(text);
        setCopiedText(label)
        setTimeout(() => setCopiedText(null), 2000);
    }

    return (
        <div className="flex flex-col gap-2 min-w-0 text-sm">
            <div
                onClick={(e) => handleCopy(e, machine.tailscale_ip, 'ts')} 
                className="flex gap-1.5 cursor-pointer hover:text-accent-light transition-colors" title="Copy">
                <span className="text-[10px] font-semibold px-1 py-0.5 rounded bg-surface-card-light/60 dark:bg-surface-card-dark/60">TS</span>
                <span className="truncate">
                    {machine.tailscale_ip}
                </span>
                {copiedText === 'ts' && (
                        <span className="text-[10px] text-emerald-400 font-sans ml-auto">Copied</span>
                    )}
            </div>
            <div
                onClick={(e) => handleCopy(e, machine.address, 'lan')}  
                className="flex gap-1.5 cursor-pointer hover:text-accent-light transition-colors" title="Copy">
                <span className="text-[10px] font-semibold px-1 py-0.5 rounded bg-surface-card-light/60 dark:bg-surface-card-dark/60">LAN</span>
                <span className="truncate">
                     {machine.address}
                </span>
                {copiedText === 'lan' && (
                        <span className="text-[10px] text-emerald-400 font-sans ml-auto">Copied</span>
                    )}
            </div>
        </div>
    );
})

const MachineStatsCard = observer(({machine} : {machine: IMachine}) => {
    const stats = syncStore.individualMap.get(machine.id);

    const formatStorage = (gb: number) => {
        if (gb >= 1000) {
            return `${(gb / 1000).toFixed(2)}TB`;
        }
        return `${gb.toFixed(1)}GB`;
    };

    return (<>
       {stats && <div className="grid grid-cols-2 p-2">
        <MachineTelemetry 
        avg_cpu_percent={stats.stats.cpu}  
        total_ram={stats.stats.memory.total_gb}
        used_ram={stats.stats.memory.used_gb}
        />
        <div>
            <div className="grid grid-cols-3 items-center gap-3">
                <span className="text-blue-400">Mount</span>
                <span>Device</span>
                <span>Capacity</span>

            </div>
            {stats.stats.drives.map((drive, index) => {
                return <div className="grid grid-cols-3 items-center gap-3" key={index}>
                    <span className="font-mono font-medium text-blue-400 text-sm">{drive.mountpoint}</span>
                    <span className="font-mono truncate max-w-[150px]" title={drive.drive}>
                        {drive.drive}
                    </span>
                    <div className="flex items-center">
                    <p>{formatStorage(drive.used_gb)}/{formatStorage(drive.total_gb)}</p>
                    <span className="text-xs text-gray-400 ml-1">({Math.round((drive.used_gb/drive.total_gb) * 100)}%)</span>
                    </div>
                </div>
            })}
        </div>
        </div>}
    </>)
})


interface MachineCardProps {
    machine: IMachine
    children?: React.ReactNode
}

export const MachineCard = observer(({machine, children}: MachineCardProps) => {
    const [isOpen, setIsOpen] = useState(false);
    const OS_LOGO_SIZE = 50;
    const ICON_CLASS = "w-8 h-8 text-slate-200 hover:text-accent-light transition-colors"
    return (
        <div className="border-10 border-primary-dark">
            <div onClick={() => setIsOpen(!isOpen)}>
            <BaseCard className="grid grid-cols-7 bg-primary-light dark:bg-primary-dark">
                <MachineInfo machine={machine}/>
                <MachineNetwork machine={machine}/>
                {machine.os_type === "windows" ? <FaWindows size={OS_LOGO_SIZE} /> 
                : machine.os_type === "linux" ? <FaLinux size={OS_LOGO_SIZE} /> 
                : <GrStatusUnknown className={`${ICON_CLASS}`}/>}
                <div className="flex flex-row">
                    <VscVscode className={`${ICON_CLASS}`}
                    onClick={(e) => {e.stopPropagation(); machineStore.openVSCode(machine.id);}}/>
                    <GrUpgrade className={`${ICON_CLASS}`} onClick={(e) => {e.stopPropagation();machineStore.updateMachine(machine)}}/>
                </div>
                <GrStatusGoodSmall className="w-8 h-8 shrink-0" color={machine.is_online ? "green" : "red"}/>
                <FaTrash className={`${ICON_CLASS}`} onClick={(e) =>{e.stopPropagation(); machineStore.delete(machine.id)}}/>
                
            </BaseCard>
            <div className="bg-surface-dark">
                {isOpen && <MachineStatsCard machine={machine} />}
            </div>
            </div>
            {isOpen && (children)}
        </div>
    )
});