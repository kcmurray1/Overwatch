import { observer } from "mobx-react-lite";
import type { IDockerContainer } from "../../types/machines";
import { containerStore } from "../../stores/ContainerStore";
import { GrStatusGoodSmall } from "react-icons/gr";
import { BaseCard } from "../common/BaseCard";

interface ContainerCardProps {
    container : IDockerContainer;
}

export const ContainerCard = observer(({ container } : ContainerCardProps) => {


    return (
        <BaseCard>
            <div className="flex justify-between">
                <p className="truncate">{container.name}</p>
                <p className="truncate">{container.image}</p>
                <GrStatusGoodSmall className="shrink-0" color={container.state === "running" ? "green" : "red"}/>

            </div>
        </BaseCard>
    )
})
