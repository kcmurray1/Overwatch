import { observer } from "mobx-react-lite";
import { useState } from "react";
import { FaPlay, FaPlus, FaStop } from "react-icons/fa";
import { AddMachineModal } from "./components/AddMachineModal";
import { machineStore } from "../../../../stores/MachineStore";

export const MachineBar = observer(() => {

    const [isOpen, setIsOpen] = useState(false);
    const ICON_CLASS = "w-8 h-8  hover:text-accent-light dark:hover:text-accent-dark transition-colors"
    return (
         <div className="flex justify-between w-full p-4">
            <AddMachineModal isOpen={isOpen} onClose={()=>setIsOpen(false)}/>
            <div className="flex flex-row gap-2">
                <h1>Machines</h1>
                <p>{machineStore.count}</p>
            </div>

            <div className="flex justify-between gap-3">
            <FaStop className={`${ICON_CLASS}`}/>
            <FaPlay className={`${ICON_CLASS}`}/>
            <FaPlus className={`${ICON_CLASS}`} onClick={() => setIsOpen(true)}/>
            </div>
        </div>
    )
})