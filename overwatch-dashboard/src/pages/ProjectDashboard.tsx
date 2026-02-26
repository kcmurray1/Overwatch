import { useEffect, useState } from 'react'
import { Container, Row, Table, Button} from 'react-bootstrap'
import { CustomApiRequest, type GetAllMachinesResponse, type GetAllProjectsResponse, type GetProjectBlueprintsResponse } from '../FetchAPI'
import type { IProject } from '../types/projects'
import { AddProjectBtn } from '../components/AddProjectBtn'
import { type IMachine } from '../types/machines'
import type { BlueprintProps } from '../components/DisplayFormBtn'


interface ProjectTableProps{
  projects: IProject[] | null
  onUpdate: () => void
}

interface MyProps {
  id: number
  isRunning: boolean
  onUpdate: () => void
}


const ProjectRowControls = ({id, isRunning, onUpdate}: MyProps) => {
  const startProjectBtn = async () => {
    try{
       const result = await CustomApiRequest<GetAllProjectsResponse>(`projects/${id}/start`, null, "POST");
       if (result.message === "OK")
       {
         onUpdate();
       }
    } catch(err) {

    }
  }

  const stopProjectBtn = async () => {
    try{
       const result = await CustomApiRequest<GetAllProjectsResponse>(`projects/${id}/stop`, null, "POST");
       if (result.message === "OK")
       {
        onUpdate();
       }
    } catch(err) {

    }
  }

  const removeProject = async () => {
     try{
       const result = await CustomApiRequest<GetAllProjectsResponse>(`projects/${id}`, null, "DELETE");
       onUpdate();
       console.log(result);
    } catch(err) {

    }
  }

  return (<>
    <div className="d-flex gap-3 align-items-center">
      {isRunning ? <Button onClick={stopProjectBtn}>stop</Button> : <Button onClick={startProjectBtn}>start</Button>}
      <Button onClick={removeProject}>delete</Button>
    </div>
  </>);
}

const ProjectTable = ({projects, onUpdate}: ProjectTableProps) => {
  return (
  <Table striped hover>
    <thead>
      <tr>
        <th>Name</th>
        <th>Strategy</th>
        <th>Command</th>
      </tr>
    </thead>
    <tbody>
      {projects?.map((project,key) =>
        <tr key={key}>
          <td>{project.name}</td>
          <td>{project.strategy_type}</td>
          
          <td> <ProjectRowControls id={project.id} isRunning={project.is_running} onUpdate={onUpdate} /></td>
        </tr>
      )}
    </tbody>
  </Table>
  )
}

export const ProjectDashboard = () => {
  const [projects, setProjects] = useState<IProject[] | null>(null);
  const [projectBlueprints, setProjectBlueprints] = useState<BlueprintProps[]| null>(null);
  const[machines, setMachines] = useState<IMachine[]|null>(null); 
  const [loading, setLoading] = useState(true);
  const[error, setError] = useState<string | null>(null);
  
  const fetchData = async () =>{
    try {
      console.log("fetching...")
      const projects = await CustomApiRequest<GetAllProjectsResponse>('projects', null, "GET");
      const projectBlueprints = await CustomApiRequest<GetProjectBlueprintsResponse>('blueprints', null, "GET");
      const machines = await CustomApiRequest<GetAllMachinesResponse>('machines', null,"GET");
      setProjects(projects.data);
      setProjectBlueprints(projectBlueprints.data)
      setMachines(machines.data)
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setLoading(false)
    }
  }
  useEffect(()=>{
    fetchData();
  }, [])

  if (loading) return <div>loading..</div>
  if (error) return <div>error: {error}</div>

  return (   
    <>
    <Container fluid>
      <Row md={12}>
        <AddProjectBtn projectBlueprints={projectBlueprints} availableMachines={machines}/>
  
      </Row>
      <Row>
      <ProjectTable projects={projects} onUpdate={fetchData}/>
      </Row>
    </Container>    
    </>
  );
}
