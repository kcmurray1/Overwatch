import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { MachineDashboard } from './pages/MachineDashboard'
import { MyNavBar } from './components/MyNavBar'
import { MachineDetails } from './pages/MachineDetails';
import { Row, Col, Container } from 'react-bootstrap';
import { ProjectDashboard } from './pages/ProjectDashboard';
import { ServiceDashboard } from './pages/ServiceDashboard';
import { ProtoBoard } from './pages/ProtoBoard';
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
          <Route path="/projects" element={<ProjectDashboard/>} />
          <Route path="/services" element={<ServiceDashboard/>} />
          <Route path="/proto" element={<ProtoBoard/>} />
        </Routes>
      </Col>
    </Row>
    </Container>
    </BrowserRouter>
    
  )
}

export default App
