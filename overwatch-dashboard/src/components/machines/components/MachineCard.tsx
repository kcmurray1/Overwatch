import { observer } from "mobx-react-lite";
import { BaseCard } from "../../common/BaseCard";
import { GrStatusGoodSmall } from "react-icons/gr";
import { FaMinusCircle } from "react-icons/fa";
import { machineStore } from "../../../stores/MachineStore";
import type { IMachine } from "../../../types/machines";
import { useState } from "react";


interface MachineCardProps {
    machine: IMachine
    children?: React.ReactNode
}

export const MachineCard = observer(({machine, children}: MachineCardProps) => {

    const [isOpen, setIsOpen] = useState(false);
    return (
        <div>
            <div onClick={() => setIsOpen(!isOpen)}>
            <BaseCard>
                <p>{machine.user}@{machine.address}</p>
                <GrStatusGoodSmall className="shrink-0" color={machine.is_online ? "green" : "red"}/>
                <FaMinusCircle onClick={() => machineStore.delete(machine.id)}/>
            </BaseCard>
            </div>
            {isOpen && (children)}
        </div>
    )
});