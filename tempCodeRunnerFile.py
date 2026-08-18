"""
Locust performance test for a Java backend API.

Edit the endpoint constants below to match your API paths.

Run locally:
    pip install locust
    locust -f locustfile_perf.py --host=http://localhost:8080

Then open http://localhost:8089 in a browser to start the test (web UI),
or run headless like:
    locust -f locustfile_perf.py --headless -u 100 -r 10 --run-time 1m --host=http://localhost:8080

This file defines tasks for: GET List, GET Single, POST, PUT.
"""

import random
import uuid
from locust import HttpUser, task, between, SequentialTaskSet

# ====== Configure these to match your API ======
LIST_ENDPOINT = "/api/items"            # GET list and POST new
SINGLE_ENDPOINT = "/api/items/{id}"     # GET single and PUT update
# =============================================


def make_payload(counter=None):
    uid = uuid.uuid4().hex[:8]
    return {
        "username": f"user_{uid}",
        "email": f"user_{uid}@example.com",
        "phone_number": f"0812{random.randint(1000000,9999999)}",
        "password": "Password123!",
        "user_type": "CUSTOMER",
    }


class APITestFlow(SequentialTaskSet):
    def on_start(self):
        # Try to create one resource on start so we have a valid id for PUT/GET single
        payload = make_payload(counter=1)
        with self.client.post(LIST_ENDPOINT, json=payload, name="POST", catch_response=True) as resp:
            try:
                if resp.status_code in (200, 201):
                    body = resp.json()
                    self.resource_id = body.get("id") or body.get("_id") or None
                else:
                    self.resource_id = None
                    try:
                        print("Initial create failed:", resp.status_code, resp.text)
                    except Exception:
                        pass
            except Exception:
                self.resource_id = None

    @task(4)
    def get_list(self):
        self.client.get(LIST_ENDPOINT, name="GET List")

    @task(3)
    def get_single(self):
        # prefer created resource id, otherwise try random ids
        if getattr(self, "resource_id", None):
            id = self.resource_id
        else:
            id = random.randint(1, 50)
        self.client.get(SINGLE_ENDPOINT.format(id=id), name="GET Single")

    @task(2)
    def create_item(self):
        payload = make_payload()
        with self.client.post(LIST_ENDPOINT, json=payload, name="POST", catch_response=True) as resp:
            if resp.status_code in (200, 201):
                try:
                    body = resp.json()
                    self.resource_id = body.get("id") or body.get("_id") or self.resource_id
                except Exception:
                    pass
            else:
                try:
                    print("Create failed:", resp.status_code, resp.text)
                except Exception:
                    pass

    @task(1)
    def update_item(self):
        if not getattr(self, "resource_id", None):
            # no id available; skip
            return
        payload = make_payload()
        self.client.put(SINGLE_ENDPOINT.format(id=self.resource_id), json=payload, name="PUT")


class APIPerfUser(HttpUser):
    tasks = [APITestFlow]
    wait_time = between(1, 3)


if __name__ == "__main__":
    print("Run with: locust -f locustfile_perf.py --host=http://localhost:8080")
