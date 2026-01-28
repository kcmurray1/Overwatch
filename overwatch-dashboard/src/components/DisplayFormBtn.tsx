/**
 * Generic button that opens a form with fields specified by the config perop FormField
 * Other components should wrap around this to define OnSubmit, OnChange and desired fields for the form
 */
import { useState } from "react";
import { Button, Modal, Form, Container, Alert } from "react-bootstrap";
import Select from "react-select";
import { type AddProjectRequest } from "../types/projects";


// options field is use for the 'select' formType
export interface FormField{
    name: string
    label: string
    formType: 'text' | 'number' | 'select'
    isMultiSelectForm?: boolean
    placeholder: string
    options? : {label: string; value: string | number}[]
}

interface DisplayFormBtnProps{
    formFields: FormField[]
    formData: any
    title: string
    error: string | null
    onSubmit: (e: React.ChangeEvent<any>) => Promise<Boolean>
    onChange: (e: React.ChangeEvent<any>) => void
    clearError: () => void
}


interface MachineRole{
    name: string
    many: boolean
}

interface BlueprintStructure{
    machine_roles: MachineRole[]
}

export interface BlueprintProps {
    name: string
    struct: BlueprintStructure
}


interface DynamicProjectFieldProps{
    blueprintstructure: BlueprintStructure,
    machines: {label: string, value: number}[]
    onChange: (e: React.ChangeEvent<any>) => void
}

const DynamicProjectField = ({blueprintstructure, machines, onChange} : DynamicProjectFieldProps) =>
{   
    return (
        <>
        {
            blueprintstructure?.machine_roles.map((role, key) => {
                return <Form.Group className="mb-3" controlId={`DisplayFormBtn.${role.name}`} key={key}>                        
                        <Form.Label>{role.name}</Form.Label>
                        <Select
                                isMulti={role.many}
                                name={role.name}
                                options={machines}
                                className="react-select-container"
                                classNamePrefix="react-select"
                                onChange={(selected: any) => {
                                    const value = role.many
                                        ? selected.map((opt: any) => opt.value)
                                        : selected?.value;
                                    onChange({
                                        target: { name: role.name, value }
                                    } as any);
                                }}
                                />
                        
                </Form.Group>
            })
        }
        </>
    )
}

interface ProjectFormProps {
    blueprints: BlueprintProps[] | null
    machineOptions: {label: string, value: number}[] | null
    onSubmit: (e: React.ChangeEvent<any>, payload: any) => Promise<string|null>
}

export const ProjectForm = ({blueprints, machineOptions, onSubmit} : ProjectFormProps) =>{
    const [showForm, setShowForm] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [activeBlueprint, setActiveBlueprint] = useState<BlueprintProps | null>(null);
    const [formData, setFormData] = useState<AddProjectRequest>({
        name: "",
        recipe: "",
        env: {"key": "", "value":""},
        images: [],
        machines: []
    });

    const blueprintOptions = blueprints?.map(blueprint => ({label: blueprint.name, value: blueprint.name}));

    const handleClose = () => {
        setShowForm(false)
        setActiveBlueprint(null);
        setFormData({
        name: "",
        recipe: "",
        env: {"key": "", "value":""},
        images: [],
        machines: []
        });
    };
    
    const handleShowForm = () => setShowForm(true);

    const handleSubmit = async (e: React.FormEvent)=> {
        e.preventDefault()
        const payload = {
        name: formData.name,
        recipe: formData.recipe,
        env: formData.env,
        images: formData.images,
        machines: [] as any[]
        };
         
        activeBlueprint?.struct.machine_roles.forEach(role => {
            const valueInForm = (formData as any)[role.name];

            if(valueInForm) {
                if(Array.isArray(valueInForm)) {
                    const formattedMachine = valueInForm.map(id => ({
                        id: id,
                        role: role.name
                    }))
                    payload.machines.push(...formattedMachine)
                }
                else {
                    payload.machines.push({"id": valueInForm, role: role.name});
                }
                
            }
        })
        const error = await onSubmit(e, payload);
        if (error){
            setError(error);
        }
        else{
            handleClose();
            
        }


        
    } 

    const handleChange = (e: React.ChangeEvent<any>) => {
        const { name, value } = e.target; 
        console.log(name)  
        setFormData(
            prev => ({
            ...prev,
            [name]: value
            })
        );
    };
    return (<>
        <Container>
            <Button variant="outline-primary" onClick={handleShowForm}>sup</Button>
            
            <Modal show={showForm} onHide={handleClose}>
                {error && <Alert variant="danger" className="mt-3">{error}</Alert>}
                <Modal.Header>
                    <Modal.Title>Dynamic Form</Modal.Title>
                </Modal.Header>
                {/* Pick blueprint */}
                <Form onSubmit={handleSubmit}>
                    <Form.Group className="mb-3" controlId={`DynamicForm.test`}>
                    <Form.Label>Project Name</Form.Label>                        
                    <Form.Control
                        type='text'
                        name='name'
                        placeholder='project name'
                        onChange={handleChange}
                    />
                    </Form.Group>
                    <Select
                        name="blueprint"
                        options={blueprintOptions ? blueprintOptions : []}
                        className="react-select-container"
                        classNamePrefix="react-select"
                        onChange={(selected: any) => {
                            const found = blueprints?.find(b => b.name === selected.value);
                            if (found){
                                setActiveBlueprint(found);
                                setFormData(prev => ({
                                ...prev,
                                recipe: selected?.value || ""
                                }));
                            }           
                        }}
                    />
                    {activeBlueprint 
                        ? <DynamicProjectField blueprintstructure={activeBlueprint.struct} machines={machineOptions ? machineOptions : []} onChange={handleChange}/>
                        : null
                    }
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>Close</Button>
                    <Button variant="primary" type="submit">Submit</Button>
                </Modal.Footer>  
                </Form>
            </Modal>
        </Container>
       
    </>)
}

// inferred return type whereas explicit is the React.FC<> way
export const DisplayFormBtn = ({formData, formFields, title, onSubmit, onChange, error, clearError}: DisplayFormBtnProps) => {
    const [show, setShow] = useState(false);
    const handleClose = () => {
        setShow(false); 
        clearError()
    }
    const handleShow = () => setShow(true);
    
    const handleSubmit = async (e: React.FormEvent)=> {
        e.preventDefault()
    
        const isSuccess = await onSubmit(e)

        if (isSuccess) {
            handleClose()
        }
     
       
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
                            (<Select
                                isMulti={formField.isMultiSelectForm}
                                name={formField.name}
                                options={formField.options}
                                className="react-select-container"
                                classNamePrefix="react-select"
                                value={formField.options ? formField.options?.filter(option => 
                                    Array.isArray(formData[formField.name]) 
                                    ? formData[formField.name].includes(option.value)
                                    : formData[formField.name] === option.value
                                ) : []}
                                onChange={(selected: any) => {
                                    const value = formField.isMultiSelectForm
                                        ? selected.map((opt: any) => opt.value)
                                        : selected?.value;
                                    onChange({
                                        target: { name: formField.name, value }
                                    } as any);
                                }}
                                />
                            )
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