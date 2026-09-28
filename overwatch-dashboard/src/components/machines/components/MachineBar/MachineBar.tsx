import { observer } from "mobx-react-lite";
import { useState } from "react";
import { FaPlay, FaPlus, FaStop } from "react-icons/fa";
import { AddMachineModal } from "./components/AddMachineModal";

export const MachineBar = observer(() => {

    const [isOpen, setIsOpen] = useState(false);

    return (
         <div className="flex justify-between w-full p-4">
            <AddMachineModal isOpen={isOpen} onClose={()=>setIsOpen(false)}/>
            <div>
                <h1>Machines</h1>
            </div>

            <div className="flex justify-between gap-3">
            <FaStop/>
            <FaPlay/>
            <FaPlus onClick={() => setIsOpen(true)}/>
            </div>
        </div>
    )
})