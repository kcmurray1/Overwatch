import { makeAutoObservable, runInAction } from "mobx";
import { CustomApiRequest, type AddMachineResponse, type GetAllMachinesResponse, type MessageOnlyResponse } from "../FetchAPI";
import type { IMachine } from "../types/machines";

export class MachineStore {
    machineMap = new Map<Number, IMachine>();
    loading = true;
    error: string | null = null;
    pollInterval = 5000
    intervalId: Number | null = null;

    constructor() {
        makeAutoObservable(this);
        this.loadMachines();
    }


    loadMachines = async () => {
        try {
            const response = await CustomApiRequest<GetAllMachinesResponse>('machines', null, "GET");
            runInAction(()=>{
                console.log(response.data);
                response.data?.forEach((machine => {
                    this.machineMap.set(machine.id, machine);
                }));
                this.loading = false;
            });
        } catch(err) {
            runInAction(() => {
                this.error = (err as Error).message;
                this.loading = false;
            })
        }
    }

    get machines(): IMachine[] {
        return Array.from(this.machineMap.values());
    }

    poll() {
        if(this.intervalId) return;
        this.loadMachines();
        this.intervalId = setInterval(() => this.loadMachines(), this.pollInterval)
    }


    delete = async (id: number) => {
        try {
            await  CustomApiRequest<MessageOnlyResponse>(`machines/${id}`, null, "DELETE")
        } catch (err) {
            console.log((err as Error).message);
        }
    }

    add = async (address: string, user: string, port: string) => {
        try {
            let formData = {
                address: address,
                user: user,
                port: port,
            }
            const res = await CustomApiRequest<AddMachineResponse>('machines', formData, "POST");
            console.log(res);
        } catch (err) {
            console.log((err as Error).message);
        }
    }



}


export const machineStore = new MachineStore();