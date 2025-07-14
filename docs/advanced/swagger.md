# 📚 Swagger Integration

One of the best parts of **APIException** is how cleanly it integrates with `Swagger (OpenAPI)`.

Your success and error responses get documented with clear, predictable schemas — so your consumers, frontend teams, and testers know exactly what to expect.

--- 
## ✅ How it works

Use the `response_model` parameter for your success schema,
and `APIResponse.default()` or `APIResponse.custom()` to document **expected error cases**.

---

## ⚙️ Example: `APIResponse.default()`

This documents your success response plus the default errors (400, 401, 403, 404, 422, 500).

```python
from APIException import APIResponse, ResponseModel
@app.get("/user",
    response_model=ResponseModel[UserResponse],
    responses=APIResponse.default()
)
```

When you open **Swagger UI**, it will show all the possible success and error cases:

![APIResponse.default()](img_3.png)

---

## ⚙️ Example: `APIResponse.custom()`

Want more control?

Use `APIResponse.custom()` to add your own specific error codes for each endpoint.

```python
from APIException import ResponseModel, APIResponse
@app.get("/user",
    response_model=ResponseModel[UserResponse],
    responses=APIResponse.custom(
        (401, CustomExceptionCode.INVALID_API_KEY),
        (403, CustomExceptionCode.PERMISSION_DENIED)
    )
)
```
In **Swagger UI**, your custom error cases will show up clearly alongside your success model:

![APIResponse.custom()](img_3.png)

---

## ⚡ Tips

✅ APIResponse.default() is perfect for general endpoints that follow standard error codes.

✅ APIResponse.custom() gives you precise control for business-specific exceptions.

No more incomplete or confusing Swagger docs!

---

## 📚 Next

✔️ Learn how to log exceptions properly:  
Check [🪵 Logging & Debug](logging.md)

✔️ Not using ResponseModel yet?  
See [✅ Response Model](../usage/response_model.md)

✔️ Want to add fallback error handling?  
See [🪓 Fallback Middleware](../usage/fallback.md)