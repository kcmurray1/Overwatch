

import { observer } from "mobx-react-lite";
import { GrStatusGoodSmall } from "react-icons/gr";
import { BaseCard } from "../../common/BaseCard";
import type { ObservableContainerModel } from "../ContainerModel";
import { FaEdit, FaPause, FaPlay } from "react-icons/fa";
import { RiRestartLine } from "react-icons/ri";
import { TiDelete } from "react-icons/ti";
import { useState } from "react";
import { CiSquareCheck, CiSquareRemove } from "react-icons/ci";
import { containerStore } from "../ContainerStore";

interface ContainerAddressProps {
    initialAddress: string | null;
    onUpdate: (newAddress: string) => void;
}

const ContainerAddress = observer(({initialAddress, onUpdate}: ContainerAddressProps) => {
    const [isEditing, setIsEditing] = useState(false);
    const [address, setAddress] = useState(initialAddress || '');
    const [loading, setLoading] = useState(false);

    const handleSave = async () => {
        try {
        setLoading(true);
        await onUpdate(address);
        setIsEditing(false);
        } catch (err) {
        console.error('Failed to update address', err);
        } finally {
        setLoading(false);
        }
    };

    const handleCancel = () => {
        setAddress(initialAddress || '');
        setIsEditing(false);
    };

    if (isEditing) {
        return (
        <div className="flex justify-around">
            <input
            type="text"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            placeholder="http://100.x.x.x:8080"
            className="px-2 py-1 text-xs bg-slate-900 rounded focus:outline-none focus:border-slate-50 w-48"
            autoFocus
            />
            <button
            onClick={handleSave}
            disabled={loading}
            className="p-1 text-emerald-400 hover:text-emerald-300 transition-colors"
            title="Save"
            >
            <CiSquareCheck/>
            </button>
            <button
            onClick={handleCancel}
            disabled={loading}
            className="p-1 text-rose-400 hover:text-slate-300 transition-colors"
            title="Cancel"
            >
             <CiSquareRemove/>
            </button>
        </div>
        );
    }

    return (
        <div className="group flex gap-2">
        {initialAddress ? (
            <a
            href={initialAddress}
            target="_blank"
            rel="noreferrer"
            className="text-sm hover:underline truncate max-w-[200px]"
            title={initialAddress}
            >
            {initialAddress}
            </a>
        ) : (
            <span className="text-xs text-slate-500 italic">No link set</span>
        )}
        <button
            onClick={() => setIsEditing(true)}
            className="opacity-0 group-hover:opacity-100 p-1 hover:text-slate-200 transition-opacity"
            title="Edit address"
        >
            <FaEdit />
        </button>
        </div>
    );
})

interface ContainerCardProps {
    container : ObservableContainerModel;
    disabled?: boolean
}

export const ContainerRow = observer(({ container, disabled = false} : ContainerCardProps) => {


    return (
        <BaseCard className={`bg-accent-light dark:bg-accent-dark transition-opacity ${disabled ? "opacity-50 pointer-events-none" : ""}`}>
            <div className="grid grid-cols-5 items-center p-2 text-lg ">
                <p className="truncate">{container.name}</p>
                {/* <a className="truncate" href={`${container.address}`}>{container.address}</a> */}
                <ContainerAddress initialAddress={container.address} onUpdate={(value) => container.updateAddress(value) }/>
                <div className="flex gap-5">
                    {container.isRunning ? <FaPause title="Pause Container" onClick={() => container.stop()}/> 
                    : <FaPlay title="Start Container" onClick={() => container.start()}/>}
                    <RiRestartLine onClick={() => container.restart()} />
                </div>
                <GrStatusGoodSmall className="shrink-0" color={container.state === "running" ? "green" : "red"}/>
                <div className="border-l-2 border-primary-dark pl-5 flex items-center">
                <TiDelete onClick={() => containerStore.delete(container.id)}/>
                </div>
            </div>
        </BaseCard>
    )
})
