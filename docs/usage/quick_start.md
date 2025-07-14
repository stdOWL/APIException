# ⚡ Quick Start

Get up and running with APIException in just a few minutes!

## ✅ Install the Package

If you haven't done it yet, Let's first start by installing APIException from PyPI:
```bash
pip install APIException
```

## ✅ Register Exception Handlers
Add the register_exception_handlers to your FastAPI app to automatically handle and standardize your responses:

```python
from APIException import register_exception_handlers
from fastapi import FastAPI

app = FastAPI()

register_exception_handlers(app=app)
```
That’s it!
Your API now returns consistent success & error responses, and unexpected server errors are automatically logged with a clear JSON output.

## ✅ Example Endpoint

Here’s a minimal example:
```python
from fastapi import FastAPI, Path
from APIException import APIException, register_exception_handlers, ResponseModel, APIResponse, BaseExceptionCode
from pydantic import BaseModel

app = FastAPI()
register_exception_handlers(app=app)

class UserResponse(BaseModel):
    id: int
    username: str

class CustomExceptionCode(BaseExceptionCode):
    USER_NOT_FOUND = ("USR-404", "User not found.", "The user ID does not exist.")

@app.get("/user/{user_id}",
    response_model=ResponseModel[UserResponse],
    responses=APIResponse.default()
)
async def get_user(user_id: int = Path()):
    if user_id == 1:
        raise APIException(error_code=CustomExceptionCode.USER_NOT_FOUND, http_status_code=404)

    data = UserResponse(id=user_id, username="John Doe")
    return ResponseModel[UserResponse](data=data)
```
The below image demonstrates what actually the example code does.

![APIResponse.default()](img_3.png)

`Swagger UI` will be well structured. 

## 📚 Next

✔️ Want to learn how to customize your responses?  
Check out
[🧩 Usage](../usage/response_model.md) for [response models](../usage/response_model.md), [custom exception codes](../usage/custom_codes.md), and [fallback middleware](../usage/fallback.md).

✔️ Need to fine-tune Swagger docs?  
See [📚 Advanced](../advanced/swagger.md) for better [documentation](../advanced/swagger.md) & [logging tips](../advanced/logging.md).