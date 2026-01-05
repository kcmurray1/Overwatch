import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import { ListGroup } from 'react-bootstrap'
import { fetchData, type APIResponse } from './FetchAPI'
import { type IMachine, MachineCard } from './components/MachineCard'
import './App.css'

function App() {
  
  // Get machines from backend
  const [machines, setMachines] = useState<IMachine[] | null>(null);
  const [loading, setLoading] = useState(true);
  const[error, setError] = useState<string | null>(null);

  useEffect(()=>{
    fetchData<APIResponse<IMachine[]>>('http://localhost:5000/api/v1/status')
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
    <>
    <div>
      <ListGroup>
      {machines?.map((machine, key) => (
        <ListGroup.Item key={key}>
        <MachineCard address={machine.address} cpu={machine.cpu} id={machine.id} 
        is_online={machine.is_online} manufacturer={machine.manufacturer} 
        model={machine.model} os={machine.os} os_type={machine.os_type}
        port={machine.port} user={machine.user}
        />
        </ListGroup.Item>
      )
      )}
      </ListGroup>
    </div>    
    </>
  )
}

export default App
