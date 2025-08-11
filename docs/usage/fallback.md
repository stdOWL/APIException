# 🪓 Fallback Middleware

A global **fallback** ensures your API always returns a **predictable JSON response** — even when something goes wrong that **you didn’t catch**.

When you enable `use_fallback_middleware=True`, APIException adds an extra middleware layer to handle any unhandled exceptions like **database crashes**, **coding bugs**, or **third-party failures**.

---

## ✅ Why use it?

- No more raw `HTML 500 Internal Server Error` pages.
- *Logs* unexpected errors **automatically** — you get stack traces in logs, but your client gets a safe, clear JSON.
- Keeps your API response consistent no matter what goes wrong.


---
## ⚙️ How to enable

When you call `register_exception_handlers()`, just pass `use_fallback_middleware=True`.

```python
from fastapi import FastAPI
from api_exception import register_exception_handlers

app = FastAPI()

register_exception_handlers(
    app=app,
    use_fallback_middleware=True
)
```
Simple as that! 

---
## 📌 Example fallback response

Imagine your database goes down. Instead of an ugly HTML page, the fallback returns this:
```json
{
  "data": null,
  "status": "FAIL",
  "message": "Something went wrong.",
  "error_code": "ISE-500",
  "description": "An unexpected error occurred. Please try again later."
}
```
So frontend team can **always** handle errors the same way.

---

## ⚡ Tips

✅ By default, fallback middleware is **enabled** (True).

✅ You can disable it by passing `use_fallback_middleware=False`.

✅ Works perfectly alongside your custom APIException raises.

---

## 📚 Next

✔️ Want to integrate this with your Swagger docs?  
See **[📚 Swagger Integration](../advanced/swagger.md)**

✔️ Want to log exceptions in detail?  
Check **[🪵 Logging & Debug](../advanced/logging.md)**

✔️ New here? Start with **[🧩 Response Model](../usage/response_model.md)**


