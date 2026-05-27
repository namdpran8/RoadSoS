from __future__ import annotations

import asyncio
import logging
import threading
from collections.abc import AsyncIterator

try:
    import google.genai as genai
except Exception:  # pragma: no cover - optional dependency fallback
    genai = None

from app.core.config import GEMINI_API_KEY


logger = logging.getLogger(__name__)

GEMINI_MODEL = "gemini-1.5-flash"

client = genai.Client(api_key=GEMINI_API_KEY) if genai and GEMINI_API_KEY else None


async def generate_gemini_text(prompt: str, timeout_seconds: int = 8) -> str:
    if client is None:
        raise RuntimeError("GEMINI_API_KEY is not configured")

    def _call() -> str:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )
        return getattr(response, "text", "") or ""

    return await asyncio.wait_for(asyncio.to_thread(_call), timeout=timeout_seconds)


async def stream_gemini_text(prompt: str) -> AsyncIterator[str]:
    if client is None:
        raise RuntimeError("GEMINI_API_KEY is not configured")

    queue: asyncio.Queue[str | None] = asyncio.Queue()
    loop = asyncio.get_running_loop()

    def _worker() -> None:
        try:
            stream = client.models.generate_content_stream(
                model=GEMINI_MODEL,
                contents=prompt,
            )
            for chunk in stream:
                text = getattr(chunk, "text", None)
                if text:
                    asyncio.run_coroutine_threadsafe(queue.put(text), loop)
        except Exception as exc:  # pragma: no cover - network dependent
            logger.exception("Gemini streaming failed: %s", exc)
        finally:
            asyncio.run_coroutine_threadsafe(queue.put(None), loop)

    threading.Thread(target=_worker, daemon=True).start()

    while True:
        item = await queue.get()
        if item is None:
            break
        yield item