from typing import Callable

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from .logger import logger, add_file_handler
from .exception import APIException, set_default_http_codes, DEFAULT_HTTP_CODES
from custom_enum.enums import ExceptionCode, ExceptionStatus, BaseExceptionCode
from schemas.response_model import ResponseModel
from .response_utils import APIResponse
import traceback


__all__ = [
    "DEFAULT_HTTP_CODES",
    "APIException",
    "ExceptionCode",
    "BaseExceptionCode",
    "ExceptionStatus",
    "ResponseModel",
    "register_exception_handlers",
    "set_default_http_codes",
    "logger",
    "add_file_handler",
    "APIResponse"
]


def register_exception_handlers(app: FastAPI,
                                use_response_model: bool = True,
                                use_fallback_middleware: bool = True,
                                log_traceback: bool = True,
                                log_traceback_unhandled_exception: bool = True):
    """
    Attach APIException and fallback handlers to a FastAPI app.

    This ensures that any raised APIException will return a standardized response.
    Optionally, a fallback middleware can catch unhandled exceptions and return
    a consistent error structure.

    Also, it can log the exception details, including the traceback,
    request path, method, and client IP address, exception, exception args and so on.
    This is useful for debugging and monitoring purposes.
    By default, it automatically logs everything related to the exception described above.


    Parameters
    ----------
    app : FastAPI
        The FastAPI application instance.
    use_response_model : bool, default=True
        If True, uses the ResponseModel schema for error responses.
        If False, returns plain dictionaries.
    use_fallback_middleware : bool, default=True
        If True, catches ALL unhandled exceptions (runtime errors, etc.) and logs them.
    log_traceback : bool, default=True
        If True, logs traceback for APIException errors.
    log_traceback_unhandled_exception : bool, default=True
        If True, logs traceback for unhandled runtime exceptions.
    Examples
    --------
    **1️⃣ Basic usage (default setup):**
    ```python
    from fastapi import FastAPI
    from api_exception import register_exception_handlers

    app = FastAPI()
    register_exception_handlers(app)
    ```

    **2️⃣ Production setup – log to file, disable traceback for handled exceptions (but keep for crashes):**
    ```python
    from fastapi import FastAPI
    from api_exception import register_exception_handlers, add_file_handler, logger

    app = FastAPI()

    # Log to a file for production monitoring
    add_file_handler("prod_errors.log")

    # Only log tracebacks for unhandled runtime errors (not for expected APIExceptions)
    register_exception_handlers(
        app,
        log_traceback=False,
        log_traceback_unhandled_exception=True
    )

    # Increase verbosity for debugging
    logger.setLevel("DEBUG")
    ```

    **3️⃣ Lightweight setup for development – skip fallback middleware and return raw dicts (not ResponseModel):**
    ```python
    from fastapi import FastAPI
    from api_exception import register_exception_handlers

    app = FastAPI()

    register_exception_handlers(
        app,
        use_fallback_middleware=False,   # Let FastAPI's default error pages handle unhandled exceptions
        use_response_model=False         # Return plain dict responses for speed
    )
    ```

    **4️⃣ Full control setup – log to both console and file, tweak everything:**
    ```python
    from fastapi import FastAPI
    from api_exception import register_exception_handlers, add_file_handler, logger

    app = FastAPI()

    # Log to console (default) and also to file
    add_file_handler("detailed_logs.log")

    # Register with all customizations
    register_exception_handlers(
        app,
        use_response_model=True,
        use_fallback_middleware=True,
        log_traceback=True,
        log_traceback_unhandled_exception=False  # Don't log tracebacks for runtime errors and/or
                                                 #  any uncaught errors(db error, 3rd party etc.) (just the message)
    )

    # Set logger level to WARNING for cleaner production logs
    logger.setLevel("WARNING")
    ```
    """

    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):
        logger.error(f"Exception handled for path: {request.url.path}")
        logger.error(f"Method: {request.method}")
        logger.error(f"Client IP: {request.client.host if request.client else 'unknown'}")
        if log_traceback:
            tb = traceback.format_exc()
            logger.error(f"Traceback:\n{tb}")

        if use_response_model:
            content = exc.to_response_model().model_dump(exclude_none=False)
        else:
            content = exc.to_response()
        return JSONResponse(
            status_code=exc.http_status_code,
            content=content
        )

    if use_fallback_middleware:

        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request, exc):
            description = exc.errors()[0]["msg"].replace("Value error, ", "") if exc.errors()[0]["msg"].startswith(
                "Value error, ") else exc.errors()[0]["msg"]

            return JSONResponse(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                content=ResponseModel(
                    data=None,
                    status=ExceptionStatus.FAIL,
                    message="Validation Error",
                    error_code="VAL-422",
                    description=description,
                ).model_dump(exclude_none=False),
            )


        @app.middleware("http")
        async def fallback_exception_middleware(request: Request,
                                                call_next: Callable):
            """
            Middleware to catch unhandled exceptions and log them.
            This middleware acts as a fallback for any unhandled exceptions that occur
            during request processing.
            It logs the exception details and returns a standardized error response.
            This is useful for catching unexpected errors that are not explicitly handled
            by the APIException handler.
            Parameters:
            ----------
            -----------
            request: Request
                The incoming request object.
            call_next: Callable
                The next middleware or endpoint to call.
            -----------

            Args:
                request:
                call_next:

            Returns:
                JSONResponse: A standardized error response with status code 500.

            """
            try:
                return await call_next(request)
            except Exception as e:
                tb = traceback.format_exc()
                logger.error("⚡ Unhandled Exception Fallback ⚡")
                logger.error(f"📌 Path: {request.url.path}")
                logger.error(f"📌 Method: {request.method}")
                logger.error(f"📌 Client IP: {request.client.host if request.client else 'unknown'}")
                logger.error(f"📌 Exception Args: {e.args}")
                logger.error(f"📌 Exception: {str(e)}")

            if log_traceback_unhandled_exception:
                logger.error(f"📌 Traceback:\n{tb}")

                return JSONResponse(
                    status_code=500,
                    content=ResponseModel(
                        data=None,
                        status=ExceptionStatus.FAIL,
                        message="Something went wrong.",
                        error_code="ISE-500",
                        description="An unexpected error occurred. Please try again later."
                    ).model_dump(exclude_none=False)
                )
