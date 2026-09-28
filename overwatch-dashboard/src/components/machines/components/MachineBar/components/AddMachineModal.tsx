import { observer } from "mobx-react-lite";
import { useState } from "react";
import { machineStore } from "../../../../../stores/MachineStore";
import { BaseModal, type BaseModalProps } from "../../../../common/BaseModal";

export const AddMachineModal = observer(({isOpen, onClose}: BaseModalProps) => {
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

