import type { IDockerContainer } from "../../types/machines";
import { CustomApiRequest, type MessageOnlyResponse } from "../../FetchAPI";
import { makeAutoObservable } from "mobx";


export class ObservableContainerModel implements IDockerContainer {
    id!: number;
    image!: string;
    config!: string;
    docker_id!: string;
    machine_id!: number;
    name!: string;
    state!: string;
    primary_url!: string;

    error: string | null = null;


    constructor(data: IDockerContainer) {
        Object.assign(this, data);

        makeAutoObservable(this, {
            id: false,
            docker_id: false,
            machine_id: false,
        })
    }

    get isRunning() {
        return this.state === "running";
    }


    async stop() {
        try{
            const response = await CustomApiRequest<MessageOnlyResponse>(`containers/${this.id}/stop`, null, "POST");        
    
        } catch(err) {
          
        }
    }

    async start() {
        try{
            const response = await CustomApiRequest<MessageOnlyResponse>(`containers/${this.id}/start`, null, "POST")

        } catch(err) {
            
        }
        
    }
}