
interface hostMapping {
    HostIp: string
    HostPort: string
}

interface PortMap {
    [portProtocol : string]: hostMapping[]
}
interface deployed_machine {
    container_id: string
    id: number
    role: string
    address: PortMap

}

interface deployment_data {
    machines: deployed_machine[]
}


export interface AddProjectRequest {
    name: string
    template: string
    images: string[]
    machines: {id: number, role: string}[]
    env: {key: string, value: string}

}

export interface IProject {
    id: number
    name: string
    strategy_type: string
    config: deployment_data
    deployment_metadata: deployed_machine[]
    is_running: boolean
}

