import { observer } from "mobx-react-lite";
import { machineStore } from "../../stores/MachineStore";
import { MachineCard } from "./components/MachineCard";
import { MachineBar } from "./components/MachineBar/MachineBar";
import { ContainerRow } from "../containers/components/ContainerRow";
import { containerStore } from "../../stores/ContainerStore";


export const MachinePage = observer(() => {
    return (
    <div className="rounded-lg py-4 outline-1 dark:outline-secondary-dark"> 
        <MachineBar/>
        <div className="rounded-lg">
                {machineStore.loading ? <p>Machines...</p>
                : machineStore.machines.map((machine, key) => {
                    return <MachineCard machine={machine} key={key}>
                        {containerStore.getByMachine(machine.id).map((container) => {
                            return <ContainerRow key={container.id} container={container} />
                        })}
                    </MachineCard>
                })}
        </div>
    </div>
    );
});