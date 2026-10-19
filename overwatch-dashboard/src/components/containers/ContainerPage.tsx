import { observer } from "mobx-react-lite"
import { containerStore } from "../../stores/ContainerStore"
import { FaPlay, FaPlus, FaStop } from "react-icons/fa"
import { ContainerRow } from "./components/ContainerRow"
import { ContainerModal } from "./components/ContainerModal"
import { useState } from "react"




const ContainerBar = observer(() => {
    const [isOpen, setIsOpen] = useState<boolean>(false);

    const ICON_CLASS = "w-8 h-8  hover:text-accent-light dark:hover:text-accent-dark transition-colors"

    return (
         <div className="flex justify-between w-full p-4 bg-surface-card-light dark:bg-surface-card-dark">
            <ContainerModal isOpen={isOpen} onClose={()=>setIsOpen(false)}/>
            <div className="flex flex-row gap-2">
                <h1>Containers</h1>
                <p>{containerStore.count}</p>
            </div>

            <div className="flex justify-between gap-3">
                <FaStop className={`${ICON_CLASS}`}/>
                <FaPlay className={`${ICON_CLASS}`}/>
                <FaPlus className={`${ICON_CLASS}`} onClick={()=> setIsOpen(true)}/>
            </div>
        </div>
    )
})

export const ContainerPage = observer(() => {

    return (  
    <div className="rounded-lg outline-1 dark:outline-secondary-dark">
        <ContainerBar/>
        <div className="flex flex-col gap-2 py-4 max-h-80 overflow-y-auto bg-surface-card-light dark:bg-surface-card-dark">
            {containerStore.loading ? <p>Loading</p>
            : containerStore.containers.map((container) => {
                return <ContainerRow key={container.id} container={container}/>
            })
            }
        </div>
    </div>
    )
})