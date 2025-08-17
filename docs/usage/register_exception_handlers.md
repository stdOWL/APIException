# 🛠 register_exception_handlers

`register_exception_handlers(app, ...)` gives your FastAPI app consistent error handling, optional fallback for unhandled exceptions, structured logging, and an OpenAPI tweak that keeps response shapes stable for clients.

---

## Function signature

```python
def register_exception_handlers(
    app: FastAPI,
    response_format: ResponseFormat = ResponseFormat.RESPONSE_MODEL,
    use_fallback_middleware: bool = True,
    log: bool = True,
    log_traceback: bool = True,
    log_traceback_unhandled_exception: bool = True,
    include_null_data_field_in_openapi: bool = True,
) -> None:
    ...
```
## Parameters

| Parameter                           | Type            | Required | Default                             | Effect                                                                                                      |
|-------------------------------------|-----------------|----------|-------------------------------------|-------------------------------------------------------------------------------------------------------------|
| `app`                               | `FastAPI`       | Yes      | —                                   | The FastAPI instance to patch with handlers and middleware.                                                  |
| `response_format`                   | `ResponseFormat`| No       | `ResponseFormat.RESPONSE_MODEL`     | Chooses how errors are serialized. Can be `RESPONSE_MODEL`, `RFC7807`, or `RESPONSE_DICTIONARY`.             |
| `use_fallback_middleware`           | `bool`          | No       | `True`                              | Adds a middleware that catches any unhandled exception and returns a safe 500 JSON response.                 |
| `log`                               | `bool`          | No       | `True`                              | **Global toggle** for all logging (handled + unhandled). If `False`, no logs are written at all.             |
| `log_traceback`                     | `bool`          | No       | `True`                              | If `True`, logs traceback for handled `APIException` errors. Useful in development, but can be noisy in prod. |
| `log_traceback_unhandled_exception` | `bool`          | No       | `True`                              | If `True`, logs traceback for unhandled runtime errors caught by the middleware.                             |
| `include_null_data_field_in_openapi`| `bool`          | No       | `True`                              | Ensures non-200 OpenAPI examples include `"data": null` for stable schemas in SDKs and validators.           |

### ResponseFormat options

| Enum | Description | Typical use |
|---|---|---|
| `RESPONSE_MODEL` | Uses your internal `ResponseModel` schema. | Default for product APIs that want one consistent shape. |
| `RFC7807` | Returns RFC 7807 Problem Details (`application/problem+json`). | Public APIs and standards-driven clients. |
| `RESPONSE_DICTIONARY` | Returns plain dictionaries without models. | Ultra lightweight responses or quick prototypes. |

---

## What is registered

1. **APIException handler**  
   Catches `APIException`, logs request metadata and optional traceback, then serializes using `response_format`.

2. **Validation handler** *(only when `use_fallback_middleware=True`)*  
   Catches `RequestValidationError` and returns 422 either as `ResponseModel` or RFC 7807.

3. **Fallback middleware** *(only when `use_fallback_middleware=True`)*  
   Wraps each request to catch unhandled exceptions and return a uniform 500 response with logging.

4. **OpenAPI patch** *(only when `include_null_data_field_in_openapi=True`)*  
   Modifies generated OpenAPI once to ensure non-200 examples include `"data": null` when missing.

---

## Response shapes

### RESPONSE_MODEL
```json
{
  "status": "fail",
  "message": "Permission denied",
  "description": "You cannot access this resource.",
  "error_code": "PER-403",
  "data": null
}
```

### RFC 7807
Header: `Content-Type: application/problem+json`
```json
{
  "title": "Permission denied",
  "description": "You cannot access this resource.",
  "status": 403,
  "type": "https://example.com/errors/forbidden",
  "instance": "/admin/panel"
}
```

### RESPONSE_DICTIONARY
```json
{
   "data": null,
   "status": "FAIL",
   "message": "Permission denied",
   "error_code": "PER-403",
   "description": "You cannot access this resource."
}
```

---

## Quick start

```python
from fastapi import FastAPI
from api_exception import register_exception_handlers

app = FastAPI()
register_exception_handlers(app)
```

---

## Usage patterns

### Minimal
```python
register_exception_handlers(app)
```

### Production with file logging and quieter handled errors
```python
from api_exception import register_exception_handlers, add_file_handler, logger

add_file_handler("prod_errors.log")
register_exception_handlers(
    app,
    log_traceback=False,
    log_traceback_unhandled_exception=True
)
logger.setLevel("WARNING")
```

### RFC 7807 outputs
```python
from api_exception import register_exception_handlers
from custom_enum.enums import ResponseFormat

register_exception_handlers(
    app,
    response_format=ResponseFormat.RFC7807,
    include_null_data_field_in_openapi=False
)
```

### No fallback middleware
```python
register_exception_handlers(
    app,
    use_fallback_middleware=False
)
```

### Lightweight dict responses
```python
from custom_enum.enums import ResponseFormat

register_exception_handlers(
    app,
    response_format=ResponseFormat.RESPONSE_DICTIONARY
)
```

### Disable all logging (global)
```python
register_exception_handlers(
    app,
    log=False
)
```

---

## Endpoint example

```python
from fastapi import FastAPI, Path
from pydantic import BaseModel
from api_exception import (
    APIException, register_exception_handlers, ResponseModel,
    BaseExceptionCode, APIResponse
)

app = FastAPI()
register_exception_handlers(app)

class UserResponse(BaseModel):
    id: int
    username: str

class CustomExceptionCode(BaseExceptionCode):
    USER_NOT_FOUND = ("USR-404", "User not found.", "The user ID does not exist.")
    PERMISSION_DENIED = ("PER-403", "Permission denied.", "You cannot access this resource.")

@app.get(
    "/user/{user_id}",
    response_model=ResponseModel[UserResponse],
    responses=APIResponse.custom(
        (403, CustomExceptionCode.PERMISSION_DENIED),
        (404, CustomExceptionCode.USER_NOT_FOUND),
    ),
)
async def get_user(user_id: int = Path(...)):
    if user_id == 1:
        raise APIException(error_code=CustomExceptionCode.USER_NOT_FOUND, http_status_code=404)

    return ResponseModel[UserResponse](
        data=UserResponse(id=2, username="Jane Doe"),
        description="User found successfully."
    )
```

---

## Validation errors

`RequestValidationError` is handled automatically and returns 422.

**ResponseModel mode**
```json
{
  "status": "fail",
  "message": "Validation Error",
  "description": "Field required",
  "error_code": "VAL-422",
  "data": null
}
```

**RFC 7807 mode**
```json
{
  "title": "Validation Error",
  "description": "Field required",
  "status": 422
}
```

---

## OpenAPI behavior

When `include_null_data_field_in_openapi=True`, the generator adds `"data": null` to non-200 examples that already include the standard error keys. This keeps SDKs and validators happy with a single, stable shape. The patched schema is cached on `app.openapi_schema`.

---

## Logging

- Every handled `APIException` logs path, method, client IP and optional traceback.
- Unhandled exceptions log a clear header block plus args and message.
- Use `add_file_handler(path)` to also write logs to a file.
- Tune verbosity with `logger.setLevel("DEBUG" | "INFO" | "WARNING" | "ERROR")`.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Swagger examples show no `data` field | OpenAPI example lacks `data` | Set `include_null_data_field_in_openapi=True` and restart the server. |
| Responses not in expected shape | Wrong `response_format` or endpoint `responses` override | Verify `response_format` and your `APIResponse.*` helper usage. |
| Logs are too noisy | `log_traceback=True` in prod | Set `log_traceback=False`, keep `log_traceback_unhandled_exception=True`. |
| 422 responses not standardized | Fallback disabled | Set `use_fallback_middleware=True`. |