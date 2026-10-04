import { makeAutoObservable, ObservableMap, runInAction } from "mobx";
import type { IDockerContainer } from "../types/machines";
import { ObservableContainerModel } from "../components/containers/ContainerModel";

export class ContainerStore {
    containerMap = new ObservableMap<Number, ObservableContainerModel>();
    loading = true;
    error: string | null = null;

    constructor() {
        makeAutoObservable(this);
    }


    setContainers(containers: IDockerContainer[]) {
        containers.forEach(container => {
            const model = new ObservableContainerModel(container);
            this.containerMap.set(model.id, model);
        })
    }


    async create(id: number) {

    }

    async delete(id: number) {

    }

    get containers(): ObservableContainerModel[] {
        return Array.from(this.containerMap.values());
    }

    getByMachine(machineId: number) {
        return Array.from(this.containerMap.values()).filter(
            (container) => container.machine_id === machineId
        )
    }


}

export const containerStore = new ContainerStore();