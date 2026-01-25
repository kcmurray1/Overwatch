/**
 * Generic button that opens a form with fields specified by the config perop FormField
 * Other components should wrap around this to define OnSubmit, OnChange and desired fields for the form
 */
import { useState } from "react";
import { Button, Modal, Form, Container, Alert } from "react-bootstrap";

// options field is use for the 'select' formType
export interface FormField{
    name: string
    label: string
    formType: 'text' | 'number' | 'select'
    placeholder: string
    options? : {label: string; value: string}[]
}

interface DisplayFormBtnProps{
    formFields: FormField[]
    title: string
    error: string | null
    onSubmit: (e: React.ChangeEvent<any>) => void
    onChange: (e: React.ChangeEvent<any>) => void
}

// inferred return type whereas explicit is the React.FC<> way
export const DisplayFormBtn = ({ formFields, title, onSubmit, onChange, error}: DisplayFormBtnProps) => {
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    
    const handleSubmit = async (e: React.FormEvent)=> {
        e.preventDefault()
        onSubmit(e)
        error ? handleShow() : {}
    }

    return (
        <>
        <Container>
        <Button variant="outline-primary" onClick={handleShow}>{title}</Button>
        
        <Modal show={show} onHide={handleClose}>
            {error && <Alert variant="danger" className="mt-3">{error}</Alert>}
            <Modal.Header closeButton>
            <Modal.Title>{title}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
            <Form onSubmit={handleSubmit}>
                {formFields?.map((formField, key) => 
                    <Form.Group className="mb-3" controlId={`DisplayFormBtn.${formField.name}`} key={key}>                        
                        <Form.Label>{formField.label}</Form.Label>
                        {formField.formType == 'select' ? 
                            (<Form.Select name={formField.name} onChange={onChange}>
                                <option>Please select</option>
                                {formField.options?.map((formOption, key) =>
                                    <option key={key} value={formOption.value}>{formOption.label}</option>
                                )}
                            </Form.Select>) 
                            : 
                            (<Form.Control
                            type={formField.formType}
                            name={formField.name}
                            placeholder={formField.placeholder}
                            onChange={onChange}
                            />)
                        }
                    </Form.Group>
                    )}
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>Close</Button>
                    <Button variant="primary" type="submit">Submit</Button>
                </Modal.Footer>  
            </Form>
            </Modal.Body>
            
        </Modal>   
        </Container>
        </>
    )
}