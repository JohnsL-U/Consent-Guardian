from locust import HttpUser, between, task

class WebsiteUser(HttpUser):
    host = ""

    wait_time = between(1, 2)

    @task
    def index_page(self):
        # This will hit the homepage!
        self.client.get("")
