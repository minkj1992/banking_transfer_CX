import json

from locust import HttpUser, SequentialTaskSet, between, task


class CertificateBehavior(SequentialTaskSet):
    certificate_id = None

    @task
    def create_certificate(self):
        data = {
            "user": {
                "name": "Test User",
                "bank_name": "KB",
                "bank_account": "123-456-789",
            },
            "transfers": ["T0001", "T0002", "T0003"],
        }
        with self.client.post(
            "/api/v1/certificates/", json=data, catch_response=True
        ) as response:
            if response.status_code == 201:
                response_data = json.loads(response.text)
                self.certificate_id = response_data["id"]
            else:
                response.failure("Failed to create certificate")

    @task
    def download_certificate(self):
        if self.certificate_id:
            self.client.get(
                f"/api/v1/certificates/{self.certificate_id}/download/?type=pdf",
                name="Download Certificate",
            )

    @task
    def view_certificate_ui(self):
        if self.certificate_id:
            self.client.get(
                f"/ui/certificates/{self.certificate_id}/", name="View Certificate UI"
            )


class CertificateUser(HttpUser):
    tasks = [CertificateBehavior]
    wait_time = between(0.5, 1)
