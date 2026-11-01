import { makeAutoObservable, ObservableMap, runInAction } from "mobx";
import { machineStore } from "./MachineStore";
import { containerStore } from "./ContainerStore";
import type { IMachine } from "../types/machines";
import { CustomApiRequest, type APIResponse, type GetAllMachinesResponse } from "../FetchAPI";
import type { AggregateStats, MachineTelemetry } from "../components/machines/types/telemetry";
export class SyncStore {
    aggregate: AggregateStats | null = null;
    individualMap = new ObservableMap<Number, MachineTelemetry>();
    pollInterval = 5000
    intervalId: number | null = null;
    telemetryIntervalId: number | null = null;
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

    async fetchTelemetryData() {
         try {
            const res = await CustomApiRequest<APIResponse<{individual: MachineTelemetry[], aggregate: AggregateStats}>>("machines/stats", null, "GET");
            runInAction(() => {
                if (res.data) {
                    this.aggregate = res.data.aggregate;
                    res.data.individual.forEach((machine) => {
                        this.individualMap.set(machine.id, machine);
                    })

                }
            })
           
            
        } catch (err) {
             runInAction(() => {
                this.error = (err as Error).message;
            })
        }
    }

    telemetry() {
        if (this.telemetryIntervalId) return;
        this.telemetryIntervalId = setInterval(() => {
            this.fetchTelemetryData();
        }, 3000);
              
    }

    stopTelemetry() {
        if(this.telemetryIntervalId) {
            clearInterval(this.telemetryIntervalId);
            this.telemetryIntervalId = null;
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