import { makeAutoObservable, runInAction } from "mobx";
import { CustomApiRequest, type GetAllContainers } from "../FetchAPI";
import type { IDockerContainer } from "../types/machines";

export class ContainerStore {
    containerMap = new Map<Number, IDockerContainer>();
    loading = true;
    error: string | null = null;

    constructor() {
        makeAutoObservable(this);
        this.loadContainers();
    }


    loadContainers = async () => {
        try {
            const response = await CustomApiRequest<GetAllContainers>('containers', null, "GET");
            runInAction(()=>{ 
                console.log(response.data);
                response.data?.forEach((container => {
                    this.containerMap.set(container.id, container);
                }));

            });

            this.loading = false;
        } catch(err) {
            this.error = (err as Error).message;

            this.loading = false;
        }
    }

    get containers(): IDockerContainer[] {
        return Array.from(this.containerMap.values());
    }


}

export const containerStore = new ContainerStore();