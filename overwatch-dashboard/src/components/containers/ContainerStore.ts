import { makeAutoObservable, ObservableMap, runInAction } from "mobx";
import type { IDockerContainer } from "../../types/machines";
import { ObservableContainerModel } from "./ContainerModel";
import type { ContainerConfig } from "./types/configs";
import { CustomApiRequest, type GetAllContainerConfigs, type MessageOnlyResponse } from "../../FetchAPI";

export class ContainerStore {
    containerMap = new ObservableMap<Number, ObservableContainerModel>();
    configMap = new ObservableMap<Number, ContainerConfig>();
    loading = true;
    error: string | null = null;

    constructor() {
        makeAutoObservable(this);
        this.loadConfigs();
    }


    loadConfigs = async () => {
        try {
            const response = await CustomApiRequest<GetAllContainerConfigs>('containers/configs', null, "GET");
            runInAction(()=>{
                console.log(response.data);
                if (response.data) {
                    
                    response.data.forEach((config => {
                        this.configMap.set(config.id, config);
                    }));



                }
                
                this.loading = false;
            });
        } catch(err) {
            runInAction(() => {
                this.error = (err as Error).message;
                this.loading = false;
            })
        }
    }
    


    setContainers(containers: IDockerContainer[]) {
        containers.forEach(container => {
            const model = new ObservableContainerModel(container);
            this.containerMap.set(model.id, model);
        })
        this.loading = false;
    }


    async delete(id: number) {
        try {
            await CustomApiRequest<MessageOnlyResponse>(`containers/${id}`, null, "DELETE");
            runInAction(() => {
                this.containerMap.delete(id);
            })
           
        } catch(err) {

        }
    }
    get containers(): ObservableContainerModel[] {
        return Array.from(this.containerMap.values());
    }

    get count(): number {
        return this.containerMap.size;
    }

    getByMachine(machineId: number) {
        return Array.from(this.containerMap.values()).filter(
            (container) => container.machine_id === machineId
        )
    }


}

export const containerStore = new ContainerStore();