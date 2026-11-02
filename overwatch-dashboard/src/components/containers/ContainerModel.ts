import type { IDockerContainer } from "../../types/machines";
import { CustomApiRequest, type MessageOnlyResponse } from "../../FetchAPI";
import { makeAutoObservable, runInAction } from "mobx";


export class ObservableContainerModel implements IDockerContainer {
    id!: number;
    image!: string;
    config!: string;
    docker_id!: string;
    machine_id!: number;
    name!: string;
    state!: string;
    address!: string;

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

    async updateAddress(newAddress: string) {
         try{
            await CustomApiRequest<MessageOnlyResponse>(`containers/${this.id}`, {address: newAddress}, "PATCH");        
            runInAction(() => {  
                this.address = newAddress;
            });
        } catch(err) {
           console.error('failed to update address', err);
        }

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

    async restart() {
        try{
            const response = await CustomApiRequest<MessageOnlyResponse>(`containers/${this.id}/restart`, null, "POST");

        } catch(err) {

        }
    }

    async delete() {
        try {
            const response = await CustomApiRequest<MessageOnlyResponse>(`containers/${this.id}`, null, "DELETE");
        } catch(err) {

        }
    }
}