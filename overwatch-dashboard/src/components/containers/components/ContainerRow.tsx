

import { observer } from "mobx-react-lite";
import { GrStatusGoodSmall } from "react-icons/gr";
import { BaseCard } from "../../common/BaseCard";
import type { ObservableContainerModel } from "../ContainerModel";
import { FaPause, FaPlay } from "react-icons/fa";
import { RiRestartLine } from "react-icons/ri";
import { TiDelete } from "react-icons/ti";

interface ContainerCardProps {
    container : ObservableContainerModel;
    disabled?: boolean
}

export const ContainerRow = observer(({ container, disabled = false} : ContainerCardProps) => {

    return (
        <BaseCard className={`bg-accent-light dark:bg-accent-dark transition-opacity ${disabled ? "opacity-50 pointer-events-none" : ""}`}>
            <div className="grid grid-cols-5 items-center p-2 text-lg ">
                <p className="truncate">{container.name}</p>
                <a className="truncate" href={`${container.primary_url}`}>{container.primary_url}</a>
                <div className="flex gap-5">
                    {container.isRunning ? <FaPause title="Pause Container" onClick={() => container.stop()}/> 
                    : <FaPlay title="Start Container" onClick={() => container.start()}/>}
                    <RiRestartLine onClick={() => container.restart()} />
                </div>
                <GrStatusGoodSmall className="shrink-0" color={container.state === "running" ? "green" : "red"}/>
                <div className="border-l-2 border-primary-dark pl-5 flex items-center">
                <TiDelete onClick={() => container.delete()}/>
                </div>
            </div>
        </BaseCard>
    )
})
