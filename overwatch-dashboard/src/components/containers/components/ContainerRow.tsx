

import { observer } from "mobx-react-lite";
import type { IDockerContainer } from "../../../types/machines";
import { containerStore } from "../../../stores/ContainerStore";
import { GrStatusGoodSmall } from "react-icons/gr";
import { BaseCard } from "../../common/BaseCard";
import type { ObservableContainerModel } from "../ContainerModel";
import { FaPause, FaPlay } from "react-icons/fa";

interface ContainerCardProps {
    container : ObservableContainerModel;
}

export const ContainerRow = observer(({ container } : ContainerCardProps) => {

    return (
        <BaseCard className="bg-accent-light dark:bg-accent-dark">
            <div className="grid grid-cols-4">
                <p className="truncate">{container.name}</p>
                <a className="truncate" href={`${container.primary_url}`}>{container.primary_url}</a>

                {container.isRunning ? <FaPause onClick={() => container.stop()}/> 
                : <FaPlay onClick={() => container.start()}/>}
                
                <GrStatusGoodSmall className="shrink-0" color={container.state === "running" ? "green" : "red"}/>

            </div>
        </BaseCard>
    )
})
