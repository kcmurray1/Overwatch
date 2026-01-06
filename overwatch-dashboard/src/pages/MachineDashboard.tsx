import { useEffect, useState } from 'react'
import { Container, Row, Col} from 'react-bootstrap'
import { fetchData, type APIResponse } from '../FetchAPI'
import { type IMachine, MachineCard } from '../components/MachineCard'

export const MachineDashboard = () => {
  
  // Get machines from backend
  const [machines, setMachines] = useState<IMachine[] | null>(null);
  const [loading, setLoading] = useState(true);
  const[error, setError] = useState<string | null>(null);

  useEffect(()=>{
    fetchData<APIResponse<IMachine[]>>('http://localhost:5000/api/v1/status-debug/10')
    .then((response) =>{
      const idk = response.data;
      console.log(idk);
      setMachines(idk);
      setLoading(false);
    })
    .catch((err) =>{
      setError((err as Error).message);
      setLoading(false);
    })
  }, [])

  if (loading) return <div>loading..</div>
  if (error) return <div>error: {error}</div>

  return (   
    <Container fluid>
      <Row>
      {machines?.map((machine, key) => (
        <Col md={4} key={key}>
        <MachineCard machine={machine} />
        <br></br>
        </Col>
      )
      )}
      </Row>
    </Container>    
  );
}
