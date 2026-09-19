import { observer } from "mobx-react-lite";
import { machineStore } from "../../stores/MachineStore";
import type { IMachine } from "../../types/machines";
import { GrStatusGoodSmall } from "react-icons/gr";
import { BaseCard } from "../common/BaseCard";
import { FaPlay, FaPlus, FaStop, FaMinusCircle} from "react-icons/fa";
import { useState } from "react";
import { BaseModal, type BaseModalProps,  } from "../common/BaseModal";

interface MachineCardProps {
    machine: IMachine
}
const AddMachineModal = observer(({isOpen, onClose}: BaseModalProps) => {
    const [address, setAddress] = useState("");
    const [user, setUser] = useState("");
    const [port, setPort] = useState("");


    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        machineStore.add(address,user, port);
        setAddress("");
        setUser("");
        setPort("");
        onClose();
    }

    return (
        <BaseModal isOpen={isOpen} onClose={onClose}>
            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-xs font-medium mb-1 text-zinc-600 dark:text-zinc-400">
                    User
                    </label>
                    <input
                    type="text"
                    required
                    value={user}
                    onChange={(e) => setUser(e.target.value)}
                    placeholder="username"
                    className="w-full px-3 py-2 text-sm rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                    <label className="block text-xs font-medium mb-1 text-zinc-600 dark:text-zinc-400">
                    Machine IP or Address
                    </label>
                    <input
                    type="text"
                    required
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    placeholder="e.g. 192.168.1.10"
                    className="w-full px-3 py-2 text-sm rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                     <label className="block text-xs font-medium mb-1 text-zinc-600 dark:text-zinc-400">
                    Port
                    </label>
                    <input
                    type="text"
                    required
                    value={port}
                    onChange={(e) => setPort(e.target.value)}
                    placeholder="e.g. 8000"
                    className="w-full px-3 py-2 text-sm rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                </div>

                <div className="flex justify-end gap-2 pt-2">
                    <button
                    type="submit"
                    className="px-3 py-1.5 text-xs font-medium bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg transition"
                    >
                    Add Machine
                    </button>
                </div>
                </form>

        </BaseModal>
    )
});

const MachineCard = observer(({machine}: MachineCardProps) => {
    return (
        <BaseCard>
            <p>{machine.user}@{machine.address}</p>
            <GrStatusGoodSmall className="shrink-0" color={machine.is_online ? "green" : "red"}/>
            <FaMinusCircle onClick={() => machineStore.delete(machine.id)}/>
        </BaseCard>
    )
});

const MachineBar = observer(() => {

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


export const MachineContainer = observer(() => {
    machineStore.poll();
    return (
    <div className="rounded-lg py-4 outline-1 dark:outline-secondary-dark"> 
    <MachineBar/>
    <div className="rounded-lg grid grid-cols-4 gap-2 ">
          
            {machineStore.loading ? <p>Machines...</p>
            : machineStore.machines.map((machine, key) => {
                return <MachineCard machine={machine} key={key}/>
            })
            
            }
    </div>
    </div>
    );
});