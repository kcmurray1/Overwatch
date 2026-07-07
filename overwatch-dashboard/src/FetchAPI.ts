import type { BlueprintProps } from "./components/DisplayFormBtn";
import {type  IMachine, type IMachineUsage } from "./types/machines";
import { type IProject } from "./types/projects";
// T represents the shape of data we expect to receive from backend
export interface APIResponse<T> {
    data: T | null;
    message: string;
}

export type VsCodeResponse = APIResponse<{link : string}>;
export type MessageOnlyResponse = APIResponse<string>;
export type GetAllMachinesResponse = APIResponse<IMachine[]>;
export type AddMachineResponse = APIResponse<IMachine>;
export type AddProjectResponse = APIResponse<IProject>;
export type GetAllProjectsResponse = APIResponse<IProject[]>;
export type GetProjectBlueprintsResponse = APIResponse<BlueprintProps[]>;
export type GetUsageResponse = APIResponse<IMachineUsage>;
// note use '/api/v2/' when containerize
const BASE_URL = "http://100.86.175.65:5000";

export async function CustomApiRequest<T>(endpoint: string, data: any | null, method: string) : Promise<T>
{
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

