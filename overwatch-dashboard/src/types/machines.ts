export interface IMachine {
    id: number
    address: string
    os_type: string
    os: string
    user: string
    cpu: string
    port: number
    model: string
    manufacturer: string
    is_online: boolean
}


export interface ICapcityStats {
    total: string
    used: string
    free: string
    percent: string
}

interface IMemory extends ICapcityStats {
    available: string
}

interface IDrive extends ICapcityStats {
    drive: string
}

export interface IMachineUsage {
    cpu: number
    memory: IMemory
    drives: IDrive[]
}

export interface AddMachineRequest {
    address: string
    user: string
    port: number
}
