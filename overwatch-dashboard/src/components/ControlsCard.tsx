import { useState } from "react";
import { Card, Button } from "react-bootstrap";
import { CustomApiRequest, type AddMachineResponse } from "../FetchAPI";
import {type AddMachineRequest} from "../types/machines"
import { DisplayFormBtn, type FormField } from "./DisplayFormBtn";


const AddMachineBtn = () => {
    const [formData, setFormData] = useState<AddMachineRequest>({
        address: '',
        user: '',
        port: 22,
    });

    const AddMachineFormFields: FormField[] = [
    {name: "address", label: "address", formType: 'text', placeholder: '10.0.3.43'},
    {name: "user", label: "user", formType: 'text', placeholder: 'bobby-pc'},
    {name: "port", label: "port", formType: 'text', placeholder: '80'},
    ]
    
    const[error, setError] = useState<string | null>(null);

    // build payload and make sure port value is a valid integer
    const handleChange = (e: React.ChangeEvent<any>) => {
        const { name, value } = e.target;   
        setFormData(
            prev => ({
            ...prev,
            [name]: name === 'port' ?  parseInt(value) || 22 : value
            })
        );
    };
    const clearError = ()=> setError(null);
    // Post to backend
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        return CustomApiRequest<AddMachineResponse>('machines', formData, "POST")
        .then((response) =>{
            console.log("added machine", response.data)
            return true
        })
        .catch((err) =>{
            setError((err as Error).message);
            return false
        });
    }

    return (
        <DisplayFormBtn formData={formData} title="Add Machine" onSubmit={handleSubmit} onChange={handleChange} formFields={AddMachineFormFields} error={error} clearError={clearError}/>
    )
}


export const ControlCard = ({machineCount} : {machineCount : number | null}) => {
    return (
        <Card className="mb-4 shadow-sm">
            <Card.Header>Machine Controls</Card.Header>
            <Card.Body>
                {/* d-flex: makes it a flex container */}
                {/* gap-3: adds consistent space between items */}
                {/* align-items-center: vertically centers the buttons */}
                <div className="d-flex gap-3 align-items-center">
                    <Button variant="outline-secondary">Restart All</Button>
                    <Button variant="outline-danger">Stop All</Button>
                    <AddMachineBtn />
                    {/* Use ms-auto (margin-start: auto) to push items to the far right */}
                    <div className="ms-auto text-muted small">
                        Total Machines: {machineCount}
                    </div>
                </div>
            </Card.Body>
        </Card>
    );
}