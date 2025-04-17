from locust import HttpUser, task, between

class DeviceStatsUser(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def add_user(self):
        self.client.post("/users/", json={"name": "TestUser", "device_id": "device1"})

    @task(2)
    def add_device_stats(self):
        self.client.post("/devices/device1/stats", json={"x": 1.0, "y": 2.0, "z": 3.0})

    @task(3)
    def get_device_analytics(self):
        self.client.get("/devices/device1/analytics")

    @task(1)
    def get_user_analytics(self):
        self.client.get("/users/1/analytics")