import time

from fastapi import Request

from app.core.config import log


async def measure_execution_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.2f} s"  # noqa: E231

    log_dict = {
        "url": request.url.path,
        "method": request.method,
        "process_time": process_time,
    }
    log.info(log_dict, extra=log_dict)

    return response
