import { makeAutoObservable, runInAction } from "mobx";
import { CustomApiRequest, type GetAllMachinesResponse } from "../FetchAPI";
import type { IMachine } from "../types/machines";

export class MachineStore {
    machineMap = new Map<Number, IMachine>();
    loading = true;
    error: string | null = null;

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


}


export const machineStore = new MachineStore();