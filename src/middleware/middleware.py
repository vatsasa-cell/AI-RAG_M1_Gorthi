import logging
import time
from fastapi import Request


logger = logging.getLogger("eka")


async def logging_middleware(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    logger.info("%s %s -> %s (%sms)", request.method, request.url.path, response.status_code, elapsed_ms)
    return response


async def cost_tracking_middleware(request: Request, call_next):
    # M1 has no LLM call, so cost is intentionally zero. This hook is retained
    # for the real RAG/LLM integration in the next phase.
    response = await call_next(request)
    response.headers["X-EKA-Cost-USD"] = "0.000000"
    return response
