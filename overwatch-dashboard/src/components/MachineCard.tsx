import { Button, Col, Row } from 'react-bootstrap';
import Card from 'react-bootstrap/Card';
import {FaWindows, FaLinux} from "react-icons/fa"
import { MdDelete, MdOutlineRestartAlt } from 'react-icons/md';
import {GrStatusUnknown} from "react-icons/gr"
import {type IconType } from 'react-icons';
import { VscVscode } from 'react-icons/vsc';
import {useNavigate } from 'react-router-dom';
import {CustomApiRequest, type MessageOnlyResponse, type VsCodeResponse} from '../FetchAPI';
import { type IMachine } from '../types/machines';

interface MachineCardProps {
    machine : IMachine
}


const OS_LOGO_SIZE=50;

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
    const {address, os_type, user, cpu, port, model, manufacturer, is_online, os} = machine;
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
        CustomApiRequest<MessageOnlyResponse>(`machines/${machine.id}`, null, "DELETE")
            .catch((err) =>{
                console.log((err as Error).message);
            });
    }

    const handleOpenVsCode = () => {
        CustomApiRequest<VsCodeResponse>(`machines/${machine.id}/openvs`, null, "GET")
        .then((response) => {
            if (response.data != null)
            {   
                window.location.href = response.data.link;
            }
            
        })
        .catch((err) => {
            console.log((err as Error).message);
        });
    }

    const handleRestartMachine = () => {
        CustomApiRequest<MessageOnlyResponse>(`machines/${machine.id}/restart`, null, "POST")
        .then((response)=> {
            console.log(response.data);
        })
        .catch((err) => {
            console.log((err as Error).message);
        })
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
            <Card.Text><p>{cpu}|{os}</p></Card.Text>
            <Row>
               
                <Col md={4}>
                   <TopStackBtn Icon={MdDelete} onClick={handleDeleteMachine} disabled={false}/>
                   <TopStackBtn Icon={VscVscode} onClick={handleOpenVsCode} disabled={!is_online}/>
                   <TopStackBtn Icon={MdOutlineRestartAlt} onClick={handleRestartMachine} disabled={!is_online}/>
                </Col>
            </Row>
        </Card.Body>

    </Card>
    )
}