import { observer } from "mobx-react-lite"
import { machineStore } from "../stores/MachineStore"
import { containerStore } from "../stores/ContainerStore"
import { ContainerCard } from "./ContainerCard"


export const HomePage = observer(() => {


    return (  
    <>
    <div className="flex bg-primary-light dark:bg-primary-dark p-2 rounded-lg">
        <p>Controls</p>
    </div>
    <div className="grid grid-cols-3 gap-2">
        {machineStore.loading && containerStore.loading ? <p>Loading</p>
        : containerStore.containers.map((container) => {
            return <ContainerCard key={container.id} container={container}/>
        })
        }
    </div>
    </>
    )
})