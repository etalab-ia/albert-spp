import time
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI()


class BaseOpenAIModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class UsageInfo(BaseOpenAIModel):
    prompt_tokens: int = 0
    total_tokens: int = 0
    completion_tokens: Optional[int] = 0


# Request schemas


class Message(BaseOpenAIModel):
    role: str
    content: str


class ChatCompletionRequest(BaseOpenAIModel):
    model: str
    messages: list[Message]
    max_tokens: int | None = None
    temperature: float = 1


# Response schemas


class ChatCompletionChoice(BaseOpenAIModel):
    index: int = -1
    message: Message


class ChatCompletionResponse(BaseOpenAIModel):
    id: str = ""
    object: str = "chat.completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str = "mocked-model"
    choices: list[ChatCompletionChoice]
    usage: UsageInfo = UsageInfo()


# endpoints


@app.get("/healthcheck")
async def healthcheck():
    return "ok"


@app.post("/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    # Create a mock response
    response_content = "This is a mocked response."
    mock_response = ChatCompletionResponse(
        choices=[ChatCompletionChoice(message=Message(role="assistant", content=response_content))]
    )

    return mock_response
