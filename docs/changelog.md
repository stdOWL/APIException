# 📝 Changelog

All notable changes to APIException will be documented here.
This project uses *Semantic Versioning*.

## [v0.1.17] - 2025-08-11

✅ **Initial stable version**

- `RFC 7807` standard support for consistent error responses (`application/problem+json`)

- OpenAPI (Swagger) schema consistency: nullable fields are now explicitly shown for better compatibility

- `Poetry` support has been added for dependency management

- `uv` support has been added.

- extra logger message param has been added to `APIException` for more detailed logging

- `log_traceback` and `log_traceback_unhandled_exception` parameters have been added to `register_exception_handlers()` for more control over logging behavior

- `log_exception` parameter has been added to `APIException` for more control over logging behavior

- `log_message` parameter has been added to `APIException` for more control over logging behavior

- Logging now uses `add_file_handler()` to write logs to a file

- Logging improvements: now includes exception arguments in logs for better debugging

- Documentation has been updated.    

- Readme.md has been updated. 


## [v0.1.16] - 2025-07-22

- setup.py has been updated.

- Documentation has been updated. 

- Readme.md has been updated. 


## [v0.1.15] - 2025-07-22

- setup.py has been updated.

- Project name has been updated. Instead of `APIException` we will use `apiexception` to comply with `PEP 625`.

- Documentation has been updated. 

- Readme.md has been updated. 

## [v0.1.14] - 2025-07-22

- setup.py has been updated.

- Project name has been updated. Instead of `APIException` we will use `apiexception` to comply with `PEP 625`.


## [v0.1.13] - 2025-07-21

- /examples/fastapi_usage.py has been updated.

- 422 Pydantic error has been fixed in APIResponse.default()

- Documentation has been updated.

- Exception Args has been added to the logs.

- Readme has been updated. New gifs have been added.



## [0.1.12] - 2025-07-14

- Documentation has been added to the project.

- More examples has been added.

- `__all__` includes more methods.


## [0.1.11] - 2025-07-13

✅ Stable release!

- Global exception handlers with fallback middleware

- APIResponse for clean Swagger documentation

- Production-ready logging for all exceptions


## [0.1.0] - 2025-06-25

🚀 Prototype started!

- Project scaffolding

- `ResponseModel` has been added

- `APIException` has been added

- Defined base ideas for standardizing error handling
