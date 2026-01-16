import Nav from 'react-bootstrap/Nav';

export const MyNavBar: React.FC = () =>{
    return (
       <div className="d-flex flex-column vh-100 p-3 bg-light border-end">
            <h1>Overwatch</h1>
            
            <Nav variant="pills" className="flex-column mb-auto">
                <Nav.Item>
                    <Nav.Link href="/">Machines</Nav.Link>
                </Nav.Item>
            </Nav>
            
            <hr />
            <div className="text-muted small">v0.1</div>
        </div>
    );
}

