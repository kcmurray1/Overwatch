import { useState } from "react";
import { Card, Row, Col, Button, Modal, Form } from "react-bootstrap";
import { MdOutlineAdd, MdOutlineEdit } from "react-icons/md";



const AddMachineBtn = () => {
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    // open pop up to enter field values

    // submit form(POST to backend)

    // show alert if success or not

    return (
        <>
        <Button variant="outline-primary" onClick={handleShow}><MdOutlineAdd size={50}></MdOutlineAdd></Button>

            <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
            <Modal.Title>Add Machine</Modal.Title>
            </Modal.Header>
            <Modal.Body>
            <Form>
                <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                <Form.Label>Machine address</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="10.1.1.0"
                    autoFocus
                />
                </Form.Group>
                <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                <Form.Label>username</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="bobby-pc"
                    autoFocus
                />
                </Form.Group>
                <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                <Form.Label>Machine port</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="25565"
                    autoFocus
                />
                </Form.Group>
               
            </Form>
            </Modal.Body>
            <Modal.Footer>
            <Button variant="secondary" onClick={handleClose}>
                Close
            </Button>
            <Button variant="primary" onClick={handleClose}>
                Submit
            </Button>
            </Modal.Footer>
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