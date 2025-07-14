# 🧩 Using `ResponseModel`

A **clean, predictable response structure** is the heart of a stable API.

The `ResponseModel` in **APIException** makes sure every success **and** error response always has the same JSON format — easy to document, easy to parse, and friendly for frontend teams.

---

## ✅ How It Works

Every API response includes:

- `data`: your actual payload  
- `status`: one of `SUCCESS`, `WARNING`, `FAIL`  
- `message`: a short summary of the outcome  
- `error_code`: only filled if there’s an error  
- `description`: extra context for debugging

👉 **How to interpret:**

- If `data` is populated and `error_code` is null → treat as **success**

- If `error_code` is filled → treat as **fail**

- Your frontend can **always** rely on the `status` field to drive logic

---

## 📌 Example

### ✅ Import and Use

```python
from fastapi import FastAPI
from APIException import ResponseModel
from pydantic import BaseModel

app = FastAPI()

class UserResponse(BaseModel):
    id: int
    username: str

@app.get("/user")
async def get_user():
    user = UserResponse(id=1, username="John Doe")
    return ResponseModel[UserResponse](
        data=user,
        description="User fetched successfully."
    )
```
### ✅ Successful Response

```json
{
    "data": {
        "id": 1,
        "username": "John Doe"
    },
    "status": "SUCCESS",
    "message": "Operation completed successfully.",
    "error_code": null,
    "description": "User fetched successfully."
}
```

### ❌ Error Response

```json
{
  "data": null,
  "status": "FAIL",
  "message": "User not found.",
  "error_code": "USER_NOT_FOUND",
  "description": "No user with ID 1 exists."
}
```

---

No matter what happens — **same shape, same fields, always predictable.**

## ⚡ Why Use It?

✔️ Frontend teams can build once and trust the schema.

✔️ No more scattered response shapes across endpoints.

✔️ Swagger/OpenAPI docs stay clear and self-explanatory.

✔️ Debugging becomes easy with `description` and `error_code`.

---
## 📚 Next

✔️ Ready to define your own error codes?  
Check out [🗂️ Custom Exception Codes](custom_codes.md)

✔️ Want to handle unexpected crashes globally?  
Learn about [🪓 Fallback Middleware](fallback.md)

✔️ Want to see how this shows up in Swagger?  
Head over to [📚 Swagger Integration](../advanced/swagger.md)
