import { observer } from "mobx-react-lite";
import { useEffect } from "react";
import { syncStore } from "../../stores/SyncStore";
import { machineStore } from "./MachineStore";
import { MachineCard } from "./components/MachineCard";
import { MachineBar } from "./components/MachineBar/MachineBar";
import { ContainerRow } from "../containers/components/ContainerRow";
import { containerStore } from "../containers/ContainerStore";

export const MachinePage = observer(() => {
    useEffect(() => {
        syncStore.poll();
        return () => syncStore.stopPolling();
    }, []);


    if (machineStore.loading) {
        return (
            <div className="flex items-center justify-center p-8 text-gray-400 text-sm">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Loading machine telemetry...
            </div>
        );
    }

    return (
        <div className="rounded-lg py-4 outline-1 bg-surface-card-light dark:bg-surface-card-dark dark:outline-secondary-dark"> 
            <MachineBar/>
            <div className="rounded-lg">
                    {machineStore.loading ? <p>Machines...</p>
                    : machineStore.machines.map((machine, key) => {
                        return <MachineCard machine={machine} key={key}>
                            {containerStore.getByMachine(machine.id).map((container) => {
                                return <ContainerRow key={container.id} container={container} disabled={!machine.is_online}/>
                            })}
                        </MachineCard>
                    })}
            </div>
        </div>
    );
});