import { useEffect, useState } from 'react'
import { Container, Row, Col} from 'react-bootstrap'
import { CustomApiRequest, type GetAllMachinesResponse,  } from '../FetchAPI'
import { MachineCard } from '../components/MachineCard'
import { type IMachine } from '../types/machines'
import { ControlCard } from '../components/ControlsCard'
export const MachineDashboard = () => {
  
  // Get machines from backend
  const [machines, setMachines] = useState<IMachine[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [machineCount, setMachineCount] = useState<number | null>(null);
  const[error, setError] = useState<string | null>(null);

  useEffect(()=>{
   const loadData = () => {
    CustomApiRequest<GetAllMachinesResponse>('machines', null, "GET")
      .then((response) => {
        setMachines(response.data);
        setMachineCount(response.data? response.data.length : 0);
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
       <Col md={12}>
        <ControlCard machineCount={machineCount}/>  
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
