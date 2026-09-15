import { observer } from "mobx-react-lite";
import type { IDockerContainer } from "../types/machines";
import { containerStore } from "../stores/ContainerStore";

interface ContainerCardProps {
    container : IDockerContainer;
}

export const ContainerCard = observer(({ container } : ContainerCardProps) => {


    return (
        <div className="relative rounded-lg p-4 bg-accent-light text-white dark:bg-primary-dark dark:text-fuchsia-100">
            <div className="flex space-between grid-cols-3 gap-2">
                <p>{container.name}</p>
                <p>{container.image}</p>
                {container.state}

            </div>
        </div>
    )
})
