import { makeAutoObservable, runInAction } from "mobx";
import { machineStore } from "./MachineStore";
import { containerStore } from "./ContainerStore";
import type { IMachine } from "../types/machines";
import { CustomApiRequest, type GetAllMachinesResponse } from "../FetchAPI";
export class SyncStore {

    pollInterval = 5000
    intervalId: number | null = null;
    error: string | null = null;

    constructor() {
        makeAutoObservable(this);
    }

    async fetchDashboardData() {

        try {
            const response = await CustomApiRequest<GetAllMachinesResponse>('machines', null, "GET");
            const machines = response.data || [];
            console.log(response.data);
            runInAction(()=>{
                machineStore.setMachines(machines);
                const allContainers = machines.flatMap((m: IMachine) => m.containers || []);
                containerStore.setContainers(allContainers);

            });
        } catch(err) {
            runInAction(() => {
                this.error = (err as Error).message;
            })
        }
    }

    poll() {
        if (this.intervalId) return;

        this.fetchDashboardData(); // Initial load immediately
        this.intervalId = setInterval(() => {
        this.fetchDashboardData();
        }, this.pollInterval);
    }

    stopPolling() {
        if (this.intervalId) {
        clearInterval(this.intervalId);
        this.intervalId = null;
        }
    }
}
export const syncStore = new SyncStore();