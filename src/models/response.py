from pydantic import BaseModel

class HTTPResponse(BaseModel):
    host: str
    url: str
    path: str
    method: str
    headers: str
    response_status: int
    response_content_encoding: str
    response_content_type: str
    response_body: str