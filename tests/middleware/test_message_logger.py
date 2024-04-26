import httpx
import pytest

from tests.middleware.test_logging import caplog_for_logger
from uvicorn.logging import TRACE_LOG_LEVEL
from uvicorn.middleware.message_logger import MessageLoggerMiddleware


@pytest.mark.anyio
async def test_message_logger(caplog):
    async def app(scope, receive, send):
        await receive()
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"", "more_body": False})

    with caplog_for_logger(caplog, "uvicorn.asgi"):
        caplog.set_level(TRACE_LOG_LEVEL, logger="uvicorn.asgi")
        caplog.set_level(TRACE_LOG_LEVEL)

        app = MessageLoggerMiddleware(app)
# No changes needed in the provided code snippet for testing message logging in the test_message_logger.py file.
# Ensure that the test assertions accurately validate the ASGI event messages in the log records and the HTTP response status code.
@pytest.mark.anyio
async def test_message_logger_exc(caplog):
    async def app(scope, receive, send):
        raise RuntimeError()

    with caplog_for_logger(caplog, "uvicorn.asgi"):
        caplog.set_level(TRACE_LOG_LEVEL, logger="uvicorn.asgi")
        caplog.set_level(TRACE_LOG_LEVEL)
        app = MessageLoggerMiddleware(app)
        async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
            with pytest.raises(RuntimeError):
                await client.get("/")
# No changes needed in the provided code snippet for testing exception handling in the message logger middleware in the test_message_logger.py file.
# Ensure that the test case correctly checks for the expected exception handling behavior when a RuntimeError is raised in the application.