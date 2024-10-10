import time
from typing import Optional

from fastapi import FastAPI, Response
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


class EmbeddingRequest(BaseModel):
    # Ordered by official OpenAI API documentation
    # https://platform.openai.com/docs/api-reference/embeddings
    model: str
    input: list[int] | list[list[int]] | str | list[str]
    encoding_format: Optional[str] = Field("float", pattern="^(float|base64)$")
    dimensions: Optional[int] = None
    user: Optional[str] = None


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


class EmbeddingResponseData(BaseModel):
    index: int = -1
    object: str = "embedding"
    embedding: list[float] | str


class EmbeddingResponse(BaseModel):
    id: str = ""
    object: str = "list"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    data: list[EmbeddingResponseData]
    usage: UsageInfo = UsageInfo()


# endpoints


@app.get("/health")
async def healthcheck():
    return Response(status_code=200)


@app.post("/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    # Create a mock response
    mock_response = ChatCompletionResponse(choices=[ChatCompletionChoice(message=Message(role="assistant", content="This is a mocked response."))])

    return mock_response


@app.post("/embeddings", response_model=EmbeddingResponse)
async def embeddings(request: EmbeddingRequest):
    # Create a mock response
    mock_response = EmbeddingResponse(model=request.model, data=[EmbeddingResponseData(embedding=[-0.1, 0.1])])

    return mock_response
