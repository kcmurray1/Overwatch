import { useEffect, useState } from 'react'
import { Container, Row, Col} from 'react-bootstrap'
import { CustomApiRequest, type GetAllProjectsResponse } from '../FetchAPI'
import type { IProject } from '../types/projects'
import { AddProjectBtn } from '../components/AddProjectBtn'


export const ProjectDashboard = () => {
  const [projects, setProjects] = useState<IProject[] | null>(null);
  const [loading, setLoading] = useState(true);
  const[error, setError] = useState<string | null>(null);
  
  useEffect(()=>{
    CustomApiRequest<GetAllProjectsResponse>('projects', null, "GET")
      .then((response) => {
        setProjects(response.data);
        setLoading(false);
      })
      .catch((err) => {
        setError((err as Error).message);
        setLoading(false);
      });

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
       <Col md={12}>
        hello
      </Col>
      {projects?.map((project, key) => (
        <Col md={4} key={key}>
            {project.name}{project.id}
        <br></br>
        </Col>
        )
      )}
      </Row>
    </Container>    
    </>
  );
}
