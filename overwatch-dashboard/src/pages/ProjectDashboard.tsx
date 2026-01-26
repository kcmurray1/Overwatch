import { useEffect, useState } from 'react'
import { Container, Row, Col, Table, Button, Card} from 'react-bootstrap'
import { CustomApiRequest, type GetAllProjectsResponse } from '../FetchAPI'
import type { IProject } from '../types/projects'
import { AddProjectBtn } from '../components/AddProjectBtn'


interface ProjectTableProps{
  projects: IProject[] | null
}

const ProjectTable = ({projects}: ProjectTableProps) => {

  return (
  <Table striped hover>
    <thead>
      <tr>
        <th>Name</th>
        <th>Strategy</th>
        <th>Command</th>
        <th>Command</th>
      </tr>
    </thead>
    <tbody>
      {projects?.map((project,key) =>
        <tr key={key}>
          <td>{project.name}</td>
          <td>{project.strategy_type}</td>
          
          <td> <div className="d-flex gap-3 align-items-center"><Button>Start</Button><Button>Restart</Button></div></td>
          <td>dummy</td>
        </tr>
      )}
    </tbody>
  </Table>
  )
}

export const ProjectDashboard = () => {
  const [projects, setProjects] = useState<IProject[] | null>(null);
  const [loading, setLoading] = useState(true);
  const[error, setError] = useState<string | null>(null);
  
  useEffect(()=>{

    const fetchData = async () =>{
      try {
        setLoading(true);
        const projects = await CustomApiRequest<GetAllProjectsResponse>('projects', null, "GET");

        setProjects(projects.data);
      } catch (err) {
        setError((err as Error).message)
      } finally {
        setLoading(false)
      }
    }
    fetchData();
  }, [])

  if (loading) return <div>loading..</div>
  if (error) return <div>error: {error}</div>

  return (   
    <>
    <Container fluid>
      <Row md={12}>
        <AddProjectBtn projects={projects}/>
      </Row>
      <Row>
      <ProjectTable projects={projects}/>
      </Row>
    </Container>    
    </>
  );
}
