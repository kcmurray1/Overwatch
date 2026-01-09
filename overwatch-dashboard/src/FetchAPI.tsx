// T represents the shape of data we expect to receive from backend
export interface APIResponse<T> {
    data: T | null;
    message: string;
}

export async function fetchData<T>(url : string) : Promise<T>
{   
    const res = await fetch(url)
    
    if(!res.ok)
    {
        throw new Error("There was an error fetching url" + url);
    }

    return (await res.json()) as T
}

export async function CustomApiRequest<T>(url: string, data: any | null, method: string) : Promise<T>
{
    console.log(data);
    const response = await fetch(
        url,
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