import { useState } from "react";
import { Card, Button, Modal, Form, Alert } from "react-bootstrap";
import { MdOutlineAdd} from "react-icons/md";
import { CustomApiRequest, type AddMachineResponse } from "../FetchAPI";
import {type AddMachineRequest} from "../types/machines"

const AddMachineBtn = () => {
    const [show, setShow] = useState(false);
    const [formData, setFormData] = useState<AddMachineRequest>({
        address: '',
        username: '',
        port: 22,
    });
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    
    const[error, setError] = useState<string | null>(null);

    const handleChange = (e: React.ChangeEvent<any>) => {
        const { name, value } = e.target;
        
        setFormData(
            prev => ({
            ...prev,
            // make sure port value is a valid integer
            [name]: name === 'port' ?  parseInt(value) || 22 : value
            })
        );
    };

    // submit form(POST to backend)
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        CustomApiRequest<AddMachineResponse>('machines', formData, "POST")
        .then((response) =>{
            console.log("added machine", response.data)
            // only close if successful
            handleClose();
        })
        .catch((err) =>{
            setError((err as Error).message);
        });
    }

   
   

    return (
        <>
        <Button variant="outline-primary" onClick={handleShow}><MdOutlineAdd size={20}></MdOutlineAdd>Add Machine</Button>
            <Modal show={show} onHide={handleClose}>
                {error && <Alert variant="danger" className="mt-3">{error}</Alert>}
            <Modal.Header closeButton>
            <Modal.Title>Add Machine</Modal.Title>
            </Modal.Header>
            <Modal.Body>
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                <Form.Label>Machine address</Form.Label>
                <Form.Control
                    type="text"
                    name="address"
                    placeholder="10.1.1.0"
                    onChange={handleChange}
                />
                </Form.Group>
                <Form.Group className="mb-3" controlId="exampleForm.ControlInput2">
                <Form.Label>username</Form.Label>
                <Form.Control
                    type="text"
                    name="username"
                    placeholder="bobby-pc"
                    onChange={handleChange}
                />
                </Form.Group>
                <Form.Group className="mb-3" controlId="exampleForm.ControlInput3">
                <Form.Label>Machine port</Form.Label>
                <Form.Control
                    type="text"
                    name="port"
                    placeholder="25565"
                    onChange={handleChange}
                />
                </Form.Group>
                  <Modal.Footer>
                       <Button variant="secondary" onClick={handleClose}>
                    Close
                </Button>
                <Button variant="primary" type="submit">
                    Submit
                </Button>
            </Modal.Footer>  
            </Form>
            </Modal.Body>
          
        </Modal>
        </>
    )


}





interface testPropP{
    machineCount : number | null
}

export const ControlCard: React.FC<testPropP> = ({machineCount}) => {

    

    return (
        <Card className="mb-4 shadow-sm">
            <Card.Header>Controls</Card.Header>
            <Card.Body>
                {/* d-flex: makes it a flex container */}
                {/* gap-3: adds consistent space between items */}
                {/* align-items-center: vertically centers the buttons */}
                <div className="d-flex gap-3 align-items-center">
                  
                    
                    {/* Now you can just drop in more buttons easily */}
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