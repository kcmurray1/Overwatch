

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

export function MachineCard({address, os_type, user, cpu, port, model, manufacturer} : IMachine)
{
    return (
    <>
    <p>{model} {manufacturer}, signed in as {user}@{address}:{port}</p>
    </>
    )
}