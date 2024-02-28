from pydantic import BaseModel
from typing import Union, List


class ExpId(BaseModel):
    id: Union[str, None]


class ExpIdWithText(ExpId):
    text: str
