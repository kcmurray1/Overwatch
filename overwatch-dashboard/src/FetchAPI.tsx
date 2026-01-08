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

export async function PostData<T>(url : string, data : any) : Promise<T>
{   
    const res = await fetch(
        url, 
        {
            method: "POST",
            headers: {'Content-Type' : 'application/json'},
            body: JSON.stringify(data)
        }
    )

    const result = await res.json();
    
    if(!res.ok)
    {
        throw new Error(result.message);
    }

    return (result) as T
}