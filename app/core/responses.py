from fastapi.responses import JSONResponse

def response_template(status: int, message: str, data=None):
    return JSONResponse(
        status_code=status,
        content={"message": message, "data": data}
    )