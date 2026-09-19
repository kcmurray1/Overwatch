import { observer } from "mobx-react-lite"
import { machineStore } from "../../stores/MachineStore"
import { containerStore } from "../../stores/ContainerStore"
import { ContainerCard } from "./ContainerCard"
import { FaPlay, FaPlus, FaStop } from "react-icons/fa"




const ContainerBar = observer(() => {



    return (
         <div className="flex justify-between w-full p-4">
            
            <div>
                <h1>Containers</h1>
            </div>

            <div className="flex justify-between gap-3">
                <FaStop/>
                <FaPlay/>
                <FaPlus/>
            </div>
        </div>
    )
})

export const ContainerGrid = observer(() => {

    return (  
    <div className="rounded-lg outline-1 dark:outline-secondary-dark">
        <ContainerBar/>
        <div className="grid grid-cols-3 gap-2 py-4 ">
          
            {machineStore.loading && containerStore.loading ? <p>Loading</p>
            : containerStore.containers.map((container) => {
                return <ContainerCard key={container.id} container={container}/>
            })
            }
        </div>
    </div>
    )
})