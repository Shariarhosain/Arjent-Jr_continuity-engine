from pydantic import BaseModel

class IdentityContext(BaseModel):
    tenant_id: str
    user_id: str
    session_id: str
