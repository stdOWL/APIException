from locust import HttpUser, task, between

class BenchmarkTestApp(HttpUser):
    wait_time = between(0.1, 0.5)
    host = "http://test_app:8000"

    @task(3)
    def ok(self):
        self.client.get("/ok")

    @task(1)
    def error(self):
        self.client.get("/error")


'''


class BenchmarkControlApp(HttpUser):
    wait_time = between(0.1, 0.5)
    host = "http://control_app:8000"

    @task(3)
    def ok(self):
        self.client.get("/ok")

    @task(1)
    def error(self):
        self.client.get("/error")
'''
