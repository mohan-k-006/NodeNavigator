import json
import time
from app import usage
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse

from app.config import Settings, get_settings
from app.llm.errors import LLMConfigurationError, LLMUnavailable
from app.llm.factory import create_provider
from app.llm.reliable import AsyncReliableLLM
from app.llm.types import LLMRequest, Message
from app.schemas import ChatRequest

app = FastAPI(title="Examate RAG starter", version="0.1.0")

SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_llm(settings: SettingsDep) -> AsyncReliableLLM:
    return create_provider(settings)


LLMDep = Annotated[AsyncReliableLLM, Depends(get_llm)]

@app.get("/hello")
def say_hello():
    return "hello"

@app.get("/")
def say_root():
    return "You are on root page"

@app.get("/health")
def health(settings: SettingsDep) -> dict:
    """Liveness: the process is up. Must be fast and must not call the LLM or the DB."""
    return {"status": "ok", "app": settings.app_name, "environment": settings.environment}


def sse(data: dict, event: str | None = None) -> str:
    prefix = f"event: {event}\n" if event else ""
    return f"{prefix}data: {json.dumps(data)}\n\n"


@app.post("/chat")
async def chat(request: ChatRequest, provider: LLMDep, settings: SettingsDep) -> StreamingResponse:
    model_name = request.model or settings.llm_model
    llm_request = LLMRequest(
        messages=tuple(Message(role=message.role, content=message.content) for message in request.messages),
        model=model_name,
    )

    async def event_stream() -> AsyncIterator[str]:
        started = time.perf_counter()
        usage_obj = None
        failed = False
        try:
            async for chunk in provider.stream(llm_request):
                if chunk.text:
                    yield sse({"delta": chunk.text})
                if chunk.usage is not None:
                    usage_obj = chunk.usage
        except (LLMUnavailable, LLMConfigurationError) as error:
            failed = True
            yield sse({"error": str(error)}, event="error")
        usage_data = usage_obj or {"input_tokens": 0, "output_tokens": 0, "estimated": False}
        if hasattr(usage_data, "__dict__"):
            usage_data = usage_data.__dict__
        tokens_in = int(usage_data.get("input_tokens", 0))
        tokens_out = int(usage_data.get("output_tokens", 0))
        cost = usage.estimate_cost(
            tokens_in, tokens_out, settings.llm_input_price_per_million, settings.llm_output_price_per_million
        )
        latency_ms = (time.perf_counter() - started) * 1000
        if not failed:
            usage.record(model_name, tokens_in, tokens_out, cost, latency_ms)
        yield sse({"usage": usage_data, "cost_usd": cost, "latency_ms": round(latency_ms)}, event="done")

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.get("/usage")
def get_usage() -> dict:
    return usage.summary()