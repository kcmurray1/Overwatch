import { observer } from 'mobx-react-lite';
import { useState } from 'react';
import { pageStore } from '../stores/PageStore';
import Nav from 'react-bootstrap/Nav';

export const MyNavBar: React.FC = () =>{
    return (
       <div className="d-flex flex-column vh-100 p-3 bg-light border-end">
            <h1>Overwatch</h1>
            
            <Nav variant="pills" className="flex-column mb-auto">
                <Nav.Item>
                    <Nav.Link href="/">Machines</Nav.Link>
                </Nav.Item>
                 <Nav.Item>
                    <Nav.Link href="/projects">Projects</Nav.Link>
                </Nav.Item>
                <Nav.Item>
                    <Nav.Link href="/services">Sevices</Nav.Link>
                </Nav.Item>
                 <Nav.Item>
                    <Nav.Link href="/proto">proto</Nav.Link>
                </Nav.Item>
            </Nav>
            
            <hr />
            <div className="text-muted small">v1.1.1</div>
        </div>
    );
}

const SettingsComponent = observer(() => {
    return (
        <>
        <p>Settings</p>
        </>
    )
})

export const SideBar = observer(() => {
    const [isExpanded, setIsExpanded] = useState(false);


    return (
        <div className="h-full flex z-40 pointer-events-none bg-primary-light">
            <div className="h-full w-16 flex flex-col items-center py-4 space-y-4 pointer-events-auto">
                <button
                    onClick={() => {pageStore.page = "home"}}
                >
                Home    
                </button>
                <button
                    onClick={() => {pageStore.page = "tools"}}
                >
                Tools    
                </button>                
                <button
                onClick={() => {setIsExpanded(!isExpanded)}}
                >
                Settings
                </button>
            </div>

            <div 
                className={`bg-primary-light h-full w-[400px] shadow-2xl flex flex-col pointer-events-auto ${
                    isExpanded ? "block" : "hidden"
                }`}
            >
               <SettingsComponent/>
            </div>

        </div>
    )
});

