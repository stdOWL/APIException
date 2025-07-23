<p align="center">
  <img src="https://raw.githubusercontent.com/akutayural/APIException/main/assets/logo.png" alt="APIException Logo" width="450"/>
</p>
<p align="center"><b><i>Standardising FastAPI responses with clarity, consistency, and control.</i></b></p>

# APIException: Standardised Exception Handling for FastAPI
[![PyPI version](https://img.shields.io/pypi/v/APIException?cacheSeconds=60)](https://pypi.org/project/APIException/)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://akutayural.github.io/APIException/)
[![Downloads](https://pepy.tech/badge/APIException)](https://pepy.tech/project/APIException)
[![Python Versions](https://img.shields.io/pypi/pyversions/APIException.svg)](https://pypi.org/project/APIException/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**APIException** is a robust, production-ready Python library for FastAPI that simplifies exception handling and ensures consistent, well-structured API responses. Designed for developers who want to eliminate boilerplate error handling and improve Swagger/OpenAPI documentation, APIException makes your FastAPI projects cleaner and easier to maintain.

- 🔒 Consistent JSON responses for **both** success and errors.
- 📚 Beautiful Swagger/OpenAPI documentation with clear error cases.
- ⚙️ Customizable error codes with `BaseExceptionCode`.
- 🔗 Global fallback for unhandled server-side errors.
- 🗂️ Use with **multiple FastAPI apps**.
- 📜 Automatic logging of every exception detail.
- ✔️ Production-ready with unit test examples.

· [**View on PyPI**](https://pypi.org/project/APIException) 

· [**Full Documentation**](https://akutayural.github.io/APIException/)

Reading the [full documentation](https://akutayural.github.io/APIException/) is **highly recommended** — it’s clear, thorough, and helps you get started in minutes.

---

## 📦 Installation via pip

```bash
pip install apiexception
```

![pip-install-apiexception-1.gif](pip-install-apiexception-1.gif)

---

 ## ⚡ Quickstart: How to Integrate APIException

**1️⃣ Register the Handler**

```python
from APIException import register_exception_handlers
from fastapi import FastAPI

app = FastAPI()
register_exception_handlers(app)  # uses ResponseModel by default

# Use raw dict instead:
# register_exception_handlers(app, use_response_model=False)
```

---

 ## 🔍 Example: Error Handling with Custom Codes

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
    responses=APIResponse.custom(
        (401, CustomExceptionCode.INVALID_API_KEY),
        (403, CustomExceptionCode.PERMISSION_DENIED)
    )
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

![_user_{user_id}.gif](_user_{user_id}.gif)

---



**2️⃣ Raise an Exception**

```python
from APIException import APIException, ExceptionCode, register_exception_handlers
from fastapi import FastAPI
app = FastAPI()

register_exception_handlers(app)

@app.get("/login")
async def login(username: str, password: str):
    if username != "admin" or password != "admin":
        raise APIException(
            error_code=ExceptionCode.AUTH_LOGIN_FAILED,
            http_status_code=401
        )
    return {"message": "Login successful!"}
```

---

**3️⃣ Use ResponseModel for Success Responses**

```python
from APIException import ResponseModel, register_exception_handlers
from fastapi import FastAPI
app = FastAPI()

register_exception_handlers(app)

@app.get("/success")
async def success():
    return ResponseModel(
        data={"foo": "bar"},
        message="Everything went fine!"
    )
```

**_Response Model In Abstract:_**


![response_model.gif](response_model.gif)


---

## 🧩 Custom Error Codes

Always extend BaseExceptionCode — don’t subclass ExceptionCode directly!

```python
from APIException import BaseExceptionCode

class CustomExceptionCode(BaseExceptionCode):
    USER_NOT_FOUND = ("USR-404", "User not found.", "User does not exist.")
    INVALID_API_KEY = ("API-401", "Invalid API key.", "Key missing or invalid.")
```

And use it:

```python
from APIException import APIException

raise APIException(
    error_code=CustomExceptionCode.USER_NOT_FOUND,
    http_status_code=404
)
```

---

## ⚙️ Override Default HTTP Status Codes

```python
from APIException import set_default_http_codes

set_default_http_codes({
    "FAIL": 422,
    "WARNING": 202
})
```

---

## 🌐 Multiple Apps Support
```python
from fastapi import FastAPI
from APIException import register_exception_handlers

mobile_app = FastAPI()
admin_app = FastAPI()
merchant_app = FastAPI()

register_exception_handlers(mobile_app)
register_exception_handlers(admin_app)
register_exception_handlers(merchant_app)
```

---

## 📝 Automatic Logging

Every APIException automatically logs:

- File name & line number

- Error code, status, message, description

Or use the built-in logger:

```python
from APIException import logger

logger.info("Custom info log")
logger.error("Custom error log")
```

---

## ✅ Testing Example

```python
import unittest
from APIException import APIException, ExceptionCode, ResponseModel

class TestAPIException(unittest.TestCase):
    def test_api_exception(self):
        exc = APIException(error_code=ExceptionCode.AUTH_LOGIN_FAILED)
        self.assertEqual(exc.status.value, "FAIL")

    def test_response_model(self):
        res = ResponseModel(data={"foo": "bar"})
        self.assertEqual(res.status.value, "SUCCESS")

if __name__ == "__main__":
    unittest.main()
```

**Run the Tests**
- To run the tests, you can use the following command in your terminal:

```bash
python -m unittest discover -s tests
```

---

## 🔗 Full Documentation

Find detailed guides and examples in the [official docs](https://akutayural.github.io/APIException/).

---

## 📜 Changelog

**v0.1.16 (2025-07-22)**

✅ **Initial stable version**

- setup.py has been updated.

- Project name has been updated. Instead of `APIException` we will use `apiexception` to comply with `PEP 625`.

- Documentation has been updated. 

- Readme.md has been updated. 

**v0.1.15 (2025-07-22)**

- setup.py has been updated.

- Project name has been updated. Instead of `APIException` we will use `apiexception` to comply with `PEP 625`.

- Documentation has been updated. 

- Readme.md has been updated. 


**v0.1.14 (2025-07-22)**

- setup.py has been updated.

- Project name has been updated. Instead of `APIException` we will use `apiexception` to comply with PEP 625.

**v0.1.13 (2025-07-21)**

- /examples/fastapi_usage.py has been updated.

- 422 Pydantic error has been fixed in APIResponse.default()

- Documentation has been updated.

- Exception Args has been added to the logs.

- Readme has been updated. New gifs have been added.


**v0.1.12 (2025-07-14)**

- /examples/fastapi_usage.py has been updated.

- 422 Pydantic error has been handled in register_handler

- Documentation has been added.

- `use_fallback_middleware` has been added.

**v0.1.11 (2025-07-13)**

- Added CLI entrypoint (api_exception-info)

- Stable test suite with FastAPI TestClient

- Multiple app support

- Raw dict or Pydantic output

- Automatic logging improvements


**v0.1.0 (2025-06-25)**


🚀 Prototype started!

- Project scaffolding

- `ResponseModel` has been added

- `APIException` has been added

- Defined base ideas for standardizing error handling

---

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.
If you like this library and find it useful, don’t forget to give it a ⭐ on GitHub!

## Contact
If you have any questions or suggestions, please feel free to reach out at [ahmetkutayural.dev](https://ahmetkutayural.dev/#contact)

---

## 📖 Learn More

📰 **Read the full article** explaining the motivation, features, and examples:  
👉 [Tired of Messy FastAPI Responses? Standardise Them with APIException](https://medium.com/@ahmetkutayural/tired-of-messy-fastapi-responses-standardise-them-with-apiexception-528b92f5bc4f)

📚 **Full APIException Documentation**  
https://akutayural.github.io/APIException/

🐍 **PyPI**  
https://pypi.org/project/apiexception/

💻 **Author Website**  
https://ahmetkutayural.dev
