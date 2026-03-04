import { useLocation, useParams } from "react-router-dom"
import { Row, Col, Card } from "react-bootstrap";
import { useState, useEffect } from "react";
import {type GetUsageResponse, CustomApiRequest } from "../FetchAPI";
import {type IMachineUsage } from "../types/machines";

interface UsageCardProps {
    title: string
    value: string | number
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
    const [usage, setUsage] = useState<IMachineUsage | null>(null);
    const [loading, setLoading] = useState(true);
    const[error, setError] = useState<string | null>(null);
    useEffect(()=>{
       const loadData = () => {
        CustomApiRequest<GetUsageResponse>(`machines/${id}/usage`, null, "GET")
          .then((response) => {
            console.log(response.data)
            setUsage(response.data)
            setLoading(false);
          })
          .catch((err) => {
            console.log(err.message);
            setError((err as Error).message);
            setLoading(false);
          });
        };
        
        loadData();
    
        const intervalId = setInterval(loadData, 1500);
    
        return () => clearInterval(intervalId);
      }, [])

    // Check if state exists otherwise make backend request
    if (loading) return <div>loading..</div>
    if (error) return <div>error: {error}</div>

    const cpuUsage = usage?.cpu ?? "0%"
   

    return (
        <>
        <h1>{machineFromState ? machineFromState.manufacturer: `have to load machine ${id} data`}</h1>
        <Row >
            <Col md={4}>
                
                <UsageCard title={"CPU Usage"} value={cpuUsage}/>
            
            </Col>
            <Col md={4}>
             <UsageCard title={"Memory Usage"} value={`${usage?.memory.used}/${usage?.memory.total}`}/>
            </Col>
            <Col md={4}>
              {usage?.drives.map((drive, key) => (
                    <UsageCard title={"Storage"} value={`${drive.used}/${drive.total}`} key={key}/>
                  )
                  )}
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