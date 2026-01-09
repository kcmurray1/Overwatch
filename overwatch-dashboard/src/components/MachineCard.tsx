import { Button, Col, Row } from 'react-bootstrap';
import Card from 'react-bootstrap/Card';
import {FaWindows, FaLinux, FaDocker, FaPython} from "react-icons/fa"
import { MdDelete } from 'react-icons/md';
import {GrStatusUnknown} from "react-icons/gr"
import {type IconType } from 'react-icons';
import { VscVscode } from 'react-icons/vsc';
import {useNavigate } from 'react-router-dom';
import {CustomApiRequest, type APIResponse } from '../FetchAPI';

export interface IMachine {
    id: number
    address: string
    os_type: string
    os: string
    user: string
    cpu: string
    port: number
    model: string
    manufacturer: string
    is_online: boolean
}
interface MachineCardProps {
    machine : IMachine
}

interface payload {
    link: string
}

const OS_LOGO_SIZE=50;
const WATCHLIST_LOGO_SIZE = 40;

interface TopStackBtnProps {
    Icon: IconType
    onClick: () => void
    disabled: boolean
}

const TopStackBtn: React.FC<TopStackBtnProps> = ({Icon, onClick, disabled }) =>
{
    return (
         <Button disabled={disabled} style={{ position: 'relative', zIndex: 999 }}
            onClick={(e)=> {
                e.stopPropagation();
                onClick();
            }}
        ><Icon/></Button>
    )
}

export const MachineCard: React.FC<MachineCardProps> = ({machine}) =>
{
    const {address, os_type, user, cpu, port, model, manufacturer, is_online} = machine;
    var os_logo = <GrStatusUnknown size={OS_LOGO_SIZE}/>
    if(os_type == "windows")
    {
        os_logo = <FaWindows size={OS_LOGO_SIZE}/>
    }
    if(os_type == "linux")
    {
        os_logo = <FaLinux size={OS_LOGO_SIZE}/>
    }

    const card_border = is_online ? "success" : "danger";  
    
    const navigate = useNavigate()

    const handleCardClick = () => {
       navigate(`/machine-details/${machine.id}`, {
        state : {machine: machine}
       });
    }

    const handleDeleteMachine = () => {
        CustomApiRequest<APIResponse<payload>>(`http://localhost:5000/api/v1/machines/${machine.id}`, null, "DELETE")
            .catch((err) =>{
                console.log((err as Error).message);
            });
    }

    //used to open vscode in a new window nearhttps://github.com/microsoft/vscode-remote-release/issues/10650 
    const handleOpenVsCode = () => {
        CustomApiRequest<APIResponse<payload>>(`http://localhost:5000/api/v1/machines/${machine.id}/openvs`, null, "GET")
        .then((response) => {
            if (response.data != null)
            {   
                // window.location.href = `${response.data.link}/home/kmanstudios/dir?windowId=_blank`;
                window.location.href = response.data.link;
            }
            
        })
        .catch((err) => {
            console.log((err as Error).message);
        });
    }

    return (
    <Card border={card_border} className='border-3' onClick={handleCardClick} style={{position: 'relative'}}>
        <Card.Header>
            <Row>
                <Col xs={10}>
                {manufacturer} {model}
                <Card.Subtitle>{user}@{address}:{port}</Card.Subtitle>
                </Col>
                <Col xs={2}>
                {os_logo}
                </Col>
            </Row>
        </Card.Header>
        <Card.Body>
            <Card.Text>{cpu}</Card.Text>
            <h3>Watchlist Applications</h3>
            {/* Display row of application icons and whether they are runnnig */}
            <Row>
                <Col md={8}>
                    <FaDocker size={WATCHLIST_LOGO_SIZE}/> <FaPython size={WATCHLIST_LOGO_SIZE}/>
                </Col>
                <Col md={4}>
                   <TopStackBtn Icon={MdDelete} onClick={handleDeleteMachine} disabled={!is_online}/>
                   <TopStackBtn Icon={VscVscode} onClick={handleOpenVsCode} disabled={!is_online}/>
                </Col>
            </Row>
        </Card.Body>

    </Card>
    )
}