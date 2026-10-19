import { observer } from "mobx-react-lite"
import { ToolBar } from "../containers/toolbar"
import { syncStore } from "../../stores/SyncStore"
import { useEffect } from "react"
import { MachinePage } from "../machines/MachinePage"
import { ContainerPage } from "../containers/ContainerPage"


export const Home = observer(() => {
    useEffect(() => {
        syncStore.poll();
        return () => syncStore.stopPolling(); // Cleanup on unmount
    }, []);
    return (
        <>
        <div className="flex bg-primary-light dark:bg-primary-dark p-2 rounded-lg">
            <ToolBar/>
        </div>
        <div className="py-4">
            <MachinePage />
        </div>
        <ContainerPage />
        </>
    )
})