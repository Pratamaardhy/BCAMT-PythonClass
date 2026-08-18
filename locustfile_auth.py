"""
Locust tests for the Java Auth API in your mini project 3.

Endpoints tested: POST /api/auth/register, POST /api/auth/login, POST /api/auth/logout
This version tries to fetch a CSRF token from /csrf (if exposed) and includes it
as `X-XSRF-TOKEN` header when present. It also logs response bodies on failures
to help debugging 403 responses from the server.
"""

import uuid
import random
from locust import HttpUser, task, between, SequentialTaskSet

REGISTER_ENDPOINT = "/api/auth/register"
LOGIN_ENDPOINT = "/api/auth/login"
LOGOUT_ENDPOINT = "/api/auth/logout"


def make_user_data():
    uid = uuid.uuid4().hex[:8]
    return {
        "name": f"user_{uid}",
        "email": f"user_{uid}@example.com",
        "password": "Password123!",
    }


class AuthFlow(SequentialTaskSet):
    def on_start(self):
        # create a unique user for this simulated user
        self.user_data = make_user_data()
        self.access_token = None
        self.csrf_header = None

    def fetch_csrf(self):
        try:
            resp = self.client.get("/csrf", name="Get CSRF", catch_response=False)
            # try JSON token first
            try:
                body = resp.json()
                token = body.get("token") or body.get("_csrf")
                header_name = body.get("headerName") or "X-XSRF-TOKEN"
                if token:
                    self.csrf_header = {header_name: token}
                    return
            except Exception:
                pass
            # fallback: look for cookie named XSRF-TOKEN
            cookie_token = None
            try:
                cookie_token = resp.cookies.get("XSRF-TOKEN")
            except Exception:
                cookie_token = None
            if cookie_token:
                self.csrf_header = {"X-XSRF-TOKEN": cookie_token}
        except Exception:
            self.csrf_header = None

    @task(1)
    def register(self):
        # fetch CSRF token if available
        self.fetch_csrf()
        headers = {}
        if self.csrf_header:
            headers.update(self.csrf_header)
        with self.client.post(REGISTER_ENDPOINT, json=self.user_data, headers=headers, name="AUTH Register", catch_response=True) as resp:
            if resp.status_code in (200, 201):
                resp.success()
            else:
                text = ""
                try:
                    text = resp.text
                except Exception:
                    text = "<no body>"
                resp.failure(f"register failed: {resp.status_code} - {text}")

    @task(2)
    def login(self):
        payload = {"email": self.user_data["email"], "password": self.user_data["password"]}
        # include csrf header if present
        headers = {}
        if self.csrf_header:
            headers.update(self.csrf_header)
        with self.client.post(LOGIN_ENDPOINT, json=payload, headers=headers, name="AUTH Login", catch_response=True) as resp:
            if resp.status_code == 200:
                try:
                    body = resp.json()
                    # try common token locations
                    self.access_token = body.get("accessToken") or body.get("token") or body.get("jwt")
                except Exception:
                    self.access_token = None
                resp.success()
            else:
                text = ""
                try:
                    text = resp.text
                except Exception:
                    text = "<no body>"
                resp.failure(f"login failed: {resp.status_code} - {text}")

    @task(1)
    def logout(self):
        headers = {}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        if self.csrf_header:
            headers.update(self.csrf_header)
        with self.client.post(LOGOUT_ENDPOINT, headers=headers, name="AUTH Logout", catch_response=True) as resp:
            if resp.status_code in (200, 204):
                resp.success()
            else:
                text = ""
                try:
                    text = resp.text
                except Exception:
                    text = "<no body>"
                resp.failure(f"logout failed: {resp.status_code} - {text}")


class AuthUser(HttpUser):
    tasks = [AuthFlow]
    wait_time = between(1, 3)


if __name__ == "__main__":
    print("Run with: locust -f locustfile_auth.py --host=http://localhost:8081")
