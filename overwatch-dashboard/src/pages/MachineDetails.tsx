import { useLocation, useParams } from "react-router-dom"
import { Row, Col, Card } from "react-bootstrap";


interface UsageCardProps {
    title: string
    value: string
}

const UsageCard: React.FC<UsageCardProps> = ({title, value}) =>
{
    return (
        <Card>
            <Card.Title>{title}</Card.Title>
            <Card.Subtitle>{value}</Card.Subtitle>
        </Card>
    )
}

export const MachineDetails  = () =>
{
    const machineFromState = useLocation().state?.machine;

    const {id} = useParams();

    // Check if state exists otherwise make backend request
    return (
        <>
        <h1>{machineFromState ? machineFromState.manufacturer: `have to load machine ${id} data`}</h1>
        <Row >
            <Col md={4}>
                <UsageCard title={"CPU Usage"} value={'41%'}/>
            
            </Col>
            <Col md={4}>
             <UsageCard title={"Memory Usage"} value={'4.1/16GB'}/>
            </Col>
            <Col md={4}>
                 <UsageCard title={"Storage"} value={'492/1TB'}/>
            </Col>
        </Row>
        <Row>
            <Col>
                Actions
            </Col>
            <Col>
                Connection Info
            </Col>
        </Row>
      
        </>
    )
}