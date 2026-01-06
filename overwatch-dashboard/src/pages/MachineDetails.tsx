import { useLocation, useParams } from "react-router-dom"

export const MachineDetails  = () =>
{
    const machineFromState = useLocation().state?.machine;

    const {id} = useParams();

    // Check if state exists otherwise make backend request
    return (
        <>
        <h1>{machineFromState ? machineFromState.manufacturer : `have to load machine ${id} data`}</h1>
        </>
    )
}