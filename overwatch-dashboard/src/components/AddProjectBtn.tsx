import { useState } from "react"
import { DisplayFormBtn, type FormField } from "./DisplayFormBtn"
import { type AddProjectRequest, type IProject } from "../types/projects";
import { CustomApiRequest, type AddProjectResponse } from "../FetchAPI";


interface ProjectFormProps {
    projects: IProject[] | null
}

export const AddProjectBtn = ({projects} : ProjectFormProps) =>{
    const [error, setError] = useState<string | null>(null);
    const [formData, setFormData] = useState<AddProjectRequest>({
        name: "",
        recipe: "",
        env: [],
        images: [],
        machines: []
    })

    const projectOptions = projects?.map(project => ({label: project.name, value: project.name}));
    const AddProjectFormFields: FormField[] = [
        {name: "name", label: "Project Name", formType: "text", placeholder: "MyFirstProject"},
        {name: "recipe", label: "recipe", formType: "select", options: projectOptions, placeholder: "test"},
        {name: "env", label: "env", formType: "text", placeholder: "environment variables"},
        {name: "images", label:"images", formType: "text", placeholder: "docker images"},
        {name: "machines", label: "machines", formType: "text", placeholder :"machine(s) to deploy to"}
    ]

    const handleChange = (e: React.ChangeEvent<any>) => {
        const { name, value } = e.target;   
        setFormData(
            prev => ({
            ...prev,
            [name]: name === 'port' ?  parseInt(value) || 22 : value
            })
        );
    };

    const handleSubmit = (e : React.ChangeEvent<any>) =>
    {   
        e.preventDefault()
        CustomApiRequest<AddProjectResponse>('projects', formData, "POST")
        .then((response) =>{
            console.log("added project", response.data)
        })
        .catch((err) =>{
            setError((err as Error).message);
        });

    }

    return (<>
        <DisplayFormBtn title={"Add Project"} onSubmit={handleSubmit} error={error} onChange={handleChange} formFields={AddProjectFormFields}/>
    </>)
}