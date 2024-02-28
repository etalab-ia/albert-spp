from pydantic import BaseModel


class ExpId(BaseModel):
    id: str


class ExpIdWithText(ExpId):
    text: str
