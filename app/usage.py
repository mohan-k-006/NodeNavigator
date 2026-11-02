import json
import time
from pathlib import Path
from threading import Lock

LOG_FILE = Path("data/usage.jsonl")
_lock = Lock()
_records: list[dict] = []


def estimate_cost(input_tokens: int, output_tokens: int, in_price: float, out_price: float) -> float:
    return (input_tokens * in_price + output_tokens * out_price) / 1_000_000


def record(model: str, input_tokens: int, output_tokens: int, cost_usd: float, latency_ms: float) -> None:
    row = {
        "ts": time.time(),
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": cost_usd,
        "latency_ms": round(latency_ms),
    }
    with _lock:
        _records.append(row)
        try:
            LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with LOG_FILE.open("a", encoding="utf-8") as f:
                f.write(json.dumps(row) + "\n")
        except OSError:
            pass


def summary() -> dict:
    with _lock:
        rows = list(_records)
    return {
        "requests": len(rows),
        "input_tokens": sum(r["input_tokens"] for r in rows),
        "output_tokens": sum(r["output_tokens"] for r in rows),
        "total_cost_usd": round(sum(r["cost_usd"] for r in rows), 6),
        "avg_latency_ms": round(sum(r["latency_ms"] for r in rows) / len(rows)) if rows else 0,
    }