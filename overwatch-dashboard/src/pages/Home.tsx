import { observer } from "mobx-react-lite"
import { ToolBar } from "../components/containers/toolbar"
import { MachineContainer } from "../components/machines/MachineContainer"
import { ContainerGrid } from "../components/containers/ContainerGrid"
import { syncStore } from "../stores/SyncStore"


export const Home = observer(() => {
    syncStore.poll();
    return (
        <>
        <div className="flex bg-primary-light dark:bg-primary-dark p-2 rounded-lg">
            <ToolBar/>
        </div>
        <div className="py-4">
        <MachineContainer/>
        </div>
        <ContainerGrid/>
        </>
    )
})
