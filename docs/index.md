<link rel="icon" type="image/x-icon" href="favicon/favicon.ico">

# APIException: Standardised Exception Handling for FastAPI


---

## ⚡ Quick Installation
Download the package from PyPI and install it using pip:
```bash
pip install apiexception
```

![Installing the APIException for FastAPI](assets/pip-install-apiexception-1.gif)


Just import the `register_exception_handlers` function from `APIException` and call it with your FastAPI app instance to set up global exception handling:
```python
from APIException import register_exception_handlers
from fastapi import FastAPI
app = FastAPI()
register_exception_handlers(app=app)
```
That’s it — copy, paste, and you’re good to go. So easy, isn't it? 


Now all your endpoints will return consistent `success` and `error` responses, and your Swagger docs will be beautifully documented.
Exception handling will be logged, and unexpected errors will return a clear JSON response instead of FastAPI’s default HTML error page.

---
## 🔍 **See It in Action!**

```python
from fastapi import FastAPI, Path
from APIException import APIException, ExceptionStatus, register_exception_handlers, ResponseModel, APIResponse, BaseExceptionCode
from pydantic import BaseModel

app = FastAPI()

# Register exception handlers globally to have the consistent
# error handling and response structure
register_exception_handlers(app=app)

# Create the validation model for your response
class UserResponse(BaseModel):
    id: int
    username: str
    
# Define your custom exception codes extending BaseExceptionCode
class CustomExceptionCode(BaseExceptionCode):
    USER_NOT_FOUND = ("USR-404", "User not found.", "The user ID does not exist.")
    INVALID_API_KEY = ("API-401", "Invalid API key.", "Provide a valid API key.")
    PERMISSION_DENIED = ("PERM-403", "Permission denied.", "Access to this resource is forbidden.")


@app.get("/user/{user_id}",
    response_model=ResponseModel[UserResponse],
    responses=APIResponse.default()
)
async def user(user_id: int = Path()):
    if user_id == 1:
        raise APIException(
            error_code=CustomExceptionCode.USER_NOT_FOUND,
            http_status_code=401,
        )
    data = UserResponse(id=1, username="John Doe")
    return ResponseModel[UserResponse](
        data=data,
        description="User found and returned."
    )
```

When you run your FastAPI app and open **Swagger UI** (`/docs`),  
your endpoints will display **clean, predictable response schemas** like this:


![Consistent Swagger Responses](_user_{user_id}.gif)


#### - Successful API Response? 
```json
{
  "data": {
    "id": 7,
    "username": "John Doe"
  },
  "status": "SUCCESS",
  "message": "Operation completed successfully.",
  "error_code": null,
  "description": "User fetched successfully."
}
```
#### - Error API Response? 
```json
{
  "data": null,
  "status": "FAIL",
  "message": "User not found.",
  "error_code": "USR-404",
  "description": "The user ID does not exist."
}
```
In both cases, the response structure is **consistent**.


- 🟢 **200**: Success responses are clearly documented with your data model.
- 🔑 **401/403**: Custom error codes & messages show exactly what clients should expect.
- 🔍 No more guesswork — your consumers, frontend teams, and testers see exactly how your API behaves for success **and** error cases.
- ✅ Bonus: Even **`unexpected server-side issues`** — like database errors, unhandled exceptions, or third-party failures — still return a consistent JSON response that follows your ResponseModel schema.
No more raw HTML 500 pages! Every error is logged automatically so you always have a clear trail of what went wrong.

This is how **APIException** helps you build trustable, professional APIs from day one!

## 👥 Who should use this?

✅ FastAPI developers who want consistent success & error responses.  
✅ Teams building multi-client or external APIs.  
✅ Projects where Swagger/OpenAPI docs must be clear and human-friendly.  
✅ Teams that need extensible error code management.

If you’re tired of:

- Inconsistent response structures,

- Confusing Swagger docs,

- Messy exception handling,

- Finding yourself while trying to find the exception that isn't logged

- Backend teams asking *“What does this endpoint return?”*,

- Frontend teams asking *“What does this endpoint return in error?”*,

then this library is **for you**.

## 🎯 **Why did I build this?**

After **4+ years** as a FastAPI backend engineer, I’ve seen how **crucial a clean, predictable response model** is.  
When your API serves multiple frontends or external clients, having different JSON shapes, missing status info, or undocumented error codes turns maintenance into chaos.

So, this library:

✅ Standardizes **all** success & error responses,  
✅ Documents them **beautifully** in Swagger,  
✅ Provides a robust **ExceptionCode** pattern,  
✅ Adds an optional **global fallback** for unexpected crashes — all while keeping FastAPI’s speed.

---

## ✨ Core Principles

•	🔒 Consistency: Success and error responses always follow the same format.

•	📊 Clear Docs: OpenAPI/Swagger stays clean and human-friendly.

•	🪶 Zero Boilerplate: Register once, use everywhere.

•	⚡ Extensible: Fully customizable error codes & handlers.

---

## 📚 Next Steps

Ready to integrate?
Check out:
- 🚀 [**Installation**](installation.md) — How to set up APIException.

- ⚡  [**Quick Start**](usage/quick_start.md) — Add it to your project in minutes.

- 🧩 [**Usage**](usage/response_model.md) — [Response models](usage/response_model.md), [custom codes](usage/custom_codes.md), and [fallback middleware](usage/fallback.md).

- 📚 [**Advanced**](advanced/swagger.md) — [Swagger integration](advanced/swagger.md), [logging](advanced/logging.md), debugging.

- 🔗 [**API Reference**](reference/api.md) — Full reference docs.

