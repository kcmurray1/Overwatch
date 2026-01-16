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


export interface AddMachineRequest {
    address: string
    username: string
    port: number
}
