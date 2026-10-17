import { observer } from "mobx-react-lite";
import { BaseCard } from "../../common/BaseCard";
import { GrStatusGoodSmall, GrStatusUnknown, GrUpgrade } from "react-icons/gr";
import { FaLinux, FaTrash, FaWindows } from "react-icons/fa";
import { machineStore } from "../../../stores/MachineStore";
import type { IMachine } from "../../../types/machines";
import { useState } from "react";
import { VscVscode } from "react-icons/vsc";




const MachineInfo = observer(({machine}: {machine: IMachine}) => {
    
    return (
        <hgroup>
            <h1>{machine.user}</h1>
            <p>{machine.model}@{machine.address}</p>
        </hgroup>
    )
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