import { makeAutoObservable } from "mobx";
import { machineStore } from "./MachineStore";
import { containerStore } from "./ContainerStore";

export class SyncStore {
    pollInterval = 5000
    intervalId: Number | null = null;

    constructor() {
        makeAutoObservable(this);
    }

    poll() {
        if(this.intervalId) return;
        this.intervalId = setInterval(() => {
            machineStore.loadMachines();
            containerStore.loadContainers();
        }, this.pollInterval)
    }
}
export const syncStore = new SyncStore();