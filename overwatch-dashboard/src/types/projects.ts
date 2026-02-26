
interface deployed_machine {
    container_id: string
    id: number
    role: string
}

interface deployment_data {
    machines: deployed_machine[] | null
}

export interface AddProjectRequest {
    name: string
    recipe: string
    images: string[]
    machines: {id: number, role: string}[]
    env: {key: string, value: string}

}

export interface IProject {
    id: number
    name: string
    strategy_type: string
    config: deployment_data
    is_running: boolean
}

