from fastapi import FastAPI
from api_exception import APIException, register_exception_handlers, ExceptionStatus, BaseExceptionCode

app = FastAPI()
register_exception_handlers(app)


class TestExceptionCode(BaseExceptionCode):
    FAIL_CASE = ("FAIL-500", "Failure", "Something failed.")


@app.get("/ok")
async def ok():
    return {"message": "ok"}


@app.get("/error")
async def error():
    raise APIException(
        error_code=TestExceptionCode.FAIL_CASE,
        http_status_code=500,
        status=ExceptionStatus.FAIL
    )


"""
# Once dockerdan build alip docker composer i ayaga kaldirmak gerekiyor
docker-compose build --no-cache
docker-compose up                         

# test icin bu kodu kullanabilirsiniz
docker-compose run --user root locust \
  -f /mnt/locustfile.py \
  --headless -u 200 -r 10 --run-time 2m \
  --host http://test_app:8000 \
  --html /mnt/test_report.html

# control icin bu kodu kullanabilirsiniz
docker-compose run --user root locust -f /mnt/locustfile.py \
  --headless -u 200 -r 10 --run-time 2m --html /mnt/control_report.html
"""