import {type  IMachine } from "./types/machines";

// T represents the shape of data we expect to receive from backend
export interface APIResponse<T> {
    data: T | null;
    message: string;
}

export type VsCodeResponse = APIResponse<{link : string}>;
export type MessageOnlyResponse = APIResponse<string>;
export type GetAllMachinesResponse = APIResponse<IMachine[]>;
export type AddMachineResponse = APIResponse<IMachine>;

const BASE_URL = "http://localhost:5000/api/v1";

export async function CustomApiRequest<T>(endpoint: string, data: any | null, method: string) : Promise<T>
{
    // console.log(data);
    const response = await fetch(
       `${BASE_URL}/${endpoint}`,
        {
            method: method,
            headers: {'Content-Type': 'application/json'},
            ...(data && {body: JSON.stringify(data)})
             
        }
    )

    const result = await response.json();

    if(!response.ok)
    {
        throw new Error(result.message);
    }

    return (result) as T;
}

