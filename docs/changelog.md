# 📝 Changelog

All notable changes to APIException will be documented here.
This project uses *Semantic Versioning*.

## [0.1.20] - 2025-08-18
✅ Stable release!
✅ **Initial stable and suggested version**

#### Changed
- Refactored `__init__.py` to use relative imports (`from .module import ...`) for cleaner packaging and better IDE compatibility.
- Unified and simplified `__all__` so developers can import everything directly from `api_exception` (e.g. `from api_exception import ResponseModel, APIException`).

#### Fixed
- Resolved IDE red import warnings when using the library in external projects.
- Improved top-level import resolution and consistency across modules.


## [0.1.19] - 2025-08-18

#### Added
- Unified import interface: all core classes and functions can now be imported directly from `api_exception` (e.g. `from api_exception import ResponseModel, APIException`).
- Cleaner `__init__.py` exports with `__all__`.

#### Changed
- Internal imports refactored, simplified folder structure for `enums.py`, `response_model.py`, `rfc7807_model.py`.

#### Fixed
- Example and README imports updated to use new unified style.


## [0.1.18] - 2025-08-17


### Added
- Global logging control (`set_global_log`) with `log` param in `register_exception_handlers`.
- RFC7807 full support with `application/problem+json` responses.
- Automatic injection of `data: null` in OpenAPI error examples.

### Changed
- Dependency pins relaxed (`>=` instead of strict `==`).
- Docstrings and examples updated (`use_response_model` → `response_format`).
- Unified error logging (no logs when `log=False`).

### Fixed
- Fallback middleware now returns HTTP 500 instead of 422 for unexpected errors.
- Traceback scope bug fixed in handlers.

## [v0.1.17] - 2025-08-11

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

- Global exception handlers with fallback middleware

- APIResponse for clean Swagger documentation

- Production-ready logging for all exceptions


## [0.1.0] - 2025-06-25

🚀 Prototype started!

- Project scaffolding

- `ResponseModel` has been added

- `APIException` has been added

- Defined base ideas for standardizing error handling
