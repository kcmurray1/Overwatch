import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { MachineDashboard } from './pages/MachineDashboard'
import { MyNavBar } from './components/MyNavBar'
import { MachineDetails } from './pages/MachineDetails';

function App() {
  return (
    <BrowserRouter>
    <MyNavBar />
    <Routes>
      <Route path="/" element={<MachineDashboard/>} />
      <Route path="/machine-details/:id" element={<MachineDetails/>} />
    </Routes>
    </BrowserRouter>
  )
}

export default App
