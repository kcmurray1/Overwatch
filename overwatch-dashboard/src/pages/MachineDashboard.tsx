import { useEffect, useState } from 'react'
import { Container, Row, Col} from 'react-bootstrap'
import { fetchData, type APIResponse } from '../FetchAPI'
import { type IMachine, MachineCard } from '../components/MachineCard'
import { ControlCard } from '../components/ControlsCard'
export const MachineDashboard = () => {
  
  // Get machines from backend
  const [machines, setMachines] = useState<IMachine[] | null>(null);
  const [loading, setLoading] = useState(true);
  const[error, setError] = useState<string | null>(null);

  useEffect(()=>{
   const loadData = () => {
    fetchData<APIResponse<IMachine[]>>('http://127.0.0.1:5000/api/v1/status')
      .then((response) => {
        setMachines(response.data);
        setLoading(false);
      })
      .catch((err) => {
        setError((err as Error).message);
        setLoading(false);
      });
    };
    
    loadData();

    const intervalId = setInterval(loadData, 10000);

    return () => clearInterval(intervalId);
  }, [])

  if (loading) return <div>loading..</div>
  if (error) return <div>error: {error}</div>

  return (   
    <>
    <Container fluid>
      <Row>
       <Col md={4}>
        <ControlCard/>  
      </Col>
      {machines?.map((machine, key) => (
        <Col md={4} key={key}>
        <MachineCard machine={machine} />
        <br></br>
        </Col>
      )
      )}
      </Row>
    </Container>    
    </>
  );
}
