import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { MachineDashboard } from './pages/MachineDashboard'
import { MyNavBar } from './components/MyNavBar'
import { MachineDetails } from './pages/MachineDetails';
import { Row, Col, Container } from 'react-bootstrap';
function App() {
  return (
    <BrowserRouter>
    <Container fluid className="p-0 vh-100">
    <Row className="g-0 h-00">
      <Col md={2}><MyNavBar/></Col>
      <Col md={10} className="vh-100 overflow-auto">
        <Routes>
          <Route path="/" element={<MachineDashboard/>} />
          <Route path="/machine-details/:id" element={<MachineDetails/>} />
        </Routes>
      </Col>
    </Row>
    </Container>
    </BrowserRouter>
    
  )
}

export default App
