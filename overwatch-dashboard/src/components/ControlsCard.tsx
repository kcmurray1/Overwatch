import { useState } from "react";
import { Card, Row, Col, Button, Modal, Form, Alert } from "react-bootstrap";
import { MdOutlineAdd} from "react-icons/md";
import {type APIResponse, CustomApiRequest } from "../FetchAPI";

interface payload {
    address: string
    username: string
    port: number
}

const AddMachineBtn = () => {
    const [show, setShow] = useState(false);
    const [formData, setFormData] = useState<payload>({
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
        CustomApiRequest<APIResponse<payload>>('http://localhost:5000/api/v1/add-machine', formData, "POST")
        .then((response) =>{
            const idk = response.data;
            const msg = response.message;
            console.log(msg);
            console.log(idk);
            
            handleClose();
        })
        .catch((err) =>{
            setError((err as Error).message);
        });
    }

   
   

    return (
        <>
        <Button variant="outline-primary" onClick={handleShow}><MdOutlineAdd size={50}></MdOutlineAdd></Button>
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


export const ControlCard = () => {

    return (
        <Card>
            <Card.Header>Controls</Card.Header>
            <Row>
                <Col md={10}>
                    TBD
                </Col>
                <Col md={2}>
                    <AddMachineBtn />
                </Col>
            </Row>
        </Card>
    )
}