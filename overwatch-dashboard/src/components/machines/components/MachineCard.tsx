import { observer } from "mobx-react-lite";
import { BaseCard } from "../../common/BaseCard";
import { GrStatusGoodSmall, GrStatusUnknown } from "react-icons/gr";
import { FaLinux, FaMinusCircle, FaWindows } from "react-icons/fa";
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
    return (
        <div>
            <div onClick={() => setIsOpen(!isOpen)}>
            <BaseCard className="grid grid-cols-6">
                <MachineInfo machine={machine}/>
                <VscVscode size={OS_LOGO_SIZE} onClick={(e) => {e.stopPropagation(); machineStore.openVSCode(machine.id);}}/>
                
                {machine.os_type === "windows" ? <FaWindows size={OS_LOGO_SIZE} /> 
                : machine.os_type === "linux" ? <FaLinux size={OS_LOGO_SIZE} /> 
                : <GrStatusUnknown size={OS_LOGO_SIZE}/>}
                <GrStatusGoodSmall className="shrink-0" color={machine.is_online ? "green" : "red"}/>
                <FaMinusCircle onClick={(e) =>{e.stopPropagation(); machineStore.delete(machine.id)}}/>
            </BaseCard>
            </div>
            {isOpen && (children)}
        </div>
    )
});