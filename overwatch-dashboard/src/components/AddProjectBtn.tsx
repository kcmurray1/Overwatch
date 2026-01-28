import { ProjectForm, type BlueprintProps, type FormField } from "./DisplayFormBtn"
import { CustomApiRequest, type AddProjectResponse } from "../FetchAPI";
import type { IMachine } from "../types/machines";


interface ProjectFormProps {
    availableMachines: IMachine[] | null
    projectBlueprints: BlueprintProps[] | null
}

export const AddProjectBtn = ({availableMachines, projectBlueprints} : ProjectFormProps) =>{
    const machineOptions = availableMachines?.map(machine => ({label: machine.address, value: machine.id}))
    const AddProjectFormFields: FormField[] = [
        {name: "name", label: "Project Name", formType: "text", placeholder: "MyFirstProject"},
        // {name: "recipe", label: "recipe", formType: "select", options: projectOptions, placeholder: "test"},
        {name: "env", label: "env", formType: "text", placeholder: "environment variables"},
        {name: "images", label:"images", formType: "text", placeholder: "docker images"},
        {name: "machines", label: "machines", formType: "select", isMultiSelectForm: true, options: machineOptions, placeholder :"machine(s) to deploy to"}
    ]


    const handleSubmit = (e : React.ChangeEvent<any>, payload: any) =>
    {   
        e.preventDefault()
        return CustomApiRequest<AddProjectResponse>('projects', payload, "POST")
        .then((response) =>{
            console.log("added project", response.data)
            return null
        })
        .catch((err) =>{
            return (err as Error).message;
        });

    }

    return (<>
        {machineOptions && projectBlueprints
        ? <ProjectForm machineOptions={machineOptions} blueprints={projectBlueprints} onSubmit={handleSubmit}/>
        : <></>
        }
         
    </>)
}