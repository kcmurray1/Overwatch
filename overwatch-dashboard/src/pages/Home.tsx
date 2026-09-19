import { observer } from "mobx-react-lite"
import { ToolBar } from "../components/containers/toolbar"
import { MachineContainer } from "../components/machines/MachineContainer"
import { ContainerGrid } from "../components/containers/ContainerGrid"


export const Home = observer(() => {
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
