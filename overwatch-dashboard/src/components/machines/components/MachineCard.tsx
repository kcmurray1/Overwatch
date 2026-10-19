import { observer } from "mobx-react-lite";
import { BaseCard } from "../../common/BaseCard";
import { GrStatusGoodSmall, GrStatusUnknown, GrUpgrade } from "react-icons/gr";
import { FaLinux, FaTrash, FaWindows } from "react-icons/fa";
import { machineStore } from "../../../stores/MachineStore";
import type { IMachine } from "../../../types/machines";
import { useState } from "react";
import { VscVscode } from "react-icons/vsc";

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


interface MachineCardProps {
    machine: IMachine
    children?: React.ReactNode
}

export const MachineCard = observer(({machine, children}: MachineCardProps) => {
    const [isOpen, setIsOpen] = useState(false);
    const OS_LOGO_SIZE = 50;
    const ICON_CLASS = "w-8 h-8 text-slate-200 hover:text-accent-light transition-colors"
    return (
        <div>
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
                    <GrUpgrade className={`${ICON_CLASS}`} onClick={() => machineStore.updateMachine(machine)}/>
                </div>
                <GrStatusGoodSmall className="w-8 h-8 shrink-0" color={machine.is_online ? "green" : "red"}/>
                <FaTrash className={`${ICON_CLASS}`} onClick={(e) =>{e.stopPropagation(); machineStore.delete(machine.id)}}/>
            
            </BaseCard>
            </div>
            {isOpen && (children)}
        </div>
    )
});