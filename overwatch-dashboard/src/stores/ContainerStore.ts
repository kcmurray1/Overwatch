import { makeAutoObservable, runInAction } from "mobx";
import { CustomApiRequest, type GetAllContainers } from "../FetchAPI";
import type { IDockerContainer } from "../types/machines";

export class ContainerStore {
    containerMap = new Map<Number, IDockerContainer>();
    loading = true;
    error: string | null = null;

    constructor() {
        makeAutoObservable(this);
    }


    setContainers(containers: IDockerContainer[]) {
        containers.forEach(container => {
            this.containerMap.set(container.id, container);
        })
    }

    async stopContainer(id: number) {
        const response = await CustomApiRequest<GetAllContainers>(`containers/${id}/stop`, null, "POST");
        
    }

    get containers(): IDockerContainer[] {
        return Array.from(this.containerMap.values());
    }


}

export const containerStore = new ContainerStore();