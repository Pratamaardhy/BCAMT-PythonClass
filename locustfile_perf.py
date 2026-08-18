"""Tes alur autentikasi Locust untuk Mini Project 3.

File ini menjalankan urutan autentikasi terhadap endpoint berikut:
    POST /api/auth/register
    POST /api/auth/login
    POST /api/auth/logout

Cara kerja (ringkasan):
 - `AuthFlow.on_start` membuat user uji dengan memanggil endpoint register.
 - `login` mengirim kredensial dan mencoba mengekstrak token bearer dari
     respons JSON (kunci umum: `access_token`, `token`, `jwt`). Jika ditemukan,
     permintaan logout berikutnya mengirim header `Authorization: Bearer <token>`.
 - `logout` memanggil endpoint logout menggunakan header auth yang tersimpan.

Instruksi cepat untuk pengujian:
 - Jalankan API Anda sehingga menerima request pada host yang akan dipakai
     oleh Locust (mis. `http://localhost:8089`).
 - Untuk menjalankan UI Locust dan memulai pengujian manual:

        powershell
        & "c:/path/to/venv/Scripts/python.exe" -m locust -f locustfile_perf.py --host=http://localhost:8089

    lalu buka http://localhost:8089 di browser.

 - Untuk menjalankan tanpa UI (headless) contoh: 50 user, spawn rate 5, 1 menit:

        powershell
        & "c:/path/to/venv/Scripts/python.exe" -m locust -f locustfile_perf.py --headless -u 50 -r 5 --run-time 1m --host=http://localhost:8089

Sesuaikan `--host` agar mengarah ke API Anda. Lihat komentar di dalam kode
untuk penjelasan per-bagian.
"""

import random
import uuid
from locust import HttpUser, task, between, SequentialTaskSet

# Auth endpoints
REGISTER_ENDPOINT = "/api/auth/register"
LOGIN_ENDPOINT = "/api/auth/login"
LOGOUT_ENDPOINT = "/api/auth/logout"


def make_user_payload():
    uid = uuid.uuid4().hex[:8]
    return {
        # `username`/`email`/`password`/`phone_number`: field umum yang
        # biasanya diperlukan oleh controller autentikasi. Ubah nama kunci
        # jika API Anda memakai nama berbeda (mis. `user` bukan `username`).
        "username": f"user_{uid}",
        "email": f"user_{uid}@example.com",
        "password": "Password123!",
        "phone_number": f"0812{random.randint(1000000,9999999)}",
    }


class AuthFlow(SequentialTaskSet):
    def on_start(self):
        self.user_payload = make_user_payload()
        self.auth_headers = {}
        # attempt register on start
        # Permintaan register boleh gagal (mis. user sudah ada). Kita log gagalannya
        # namun tetap melanjutkan sehingga Locust dapat tetap menguji login/logout.
        with self.client.post(REGISTER_ENDPOINT, json=self.user_payload, name="register", catch_response=True) as resp:
            if resp.status_code in (200, 201):
                resp.success()
            else:
                try:
                    print("register failed:", resp.status_code, resp.text)
                except Exception:
                    pass

    @task(3)
    def login(self):
        creds = {"username": self.user_payload["username"], "password": self.user_payload["password"]}
        # Login: jika berhasil, parsing respons JSON untuk mencari token.
        # Banyak API mengembalikan `{ "access_token": "..." }` atau field
        # `token`/`jwt`. Jika ditemukan, simpan header `Authorization` untuk
        # dipakai pada permintaan berikutnya.
        with self.client.post(LOGIN_ENDPOINT, json=creds, name="login", catch_response=True) as resp:
            if resp.status_code in (200, 201):
                try:
                    body = resp.json()
                    token = body.get("access_token") or body.get("token") or body.get("jwt")
                    if token:
                        self.auth_headers = {"Authorization": f"Bearer {token}"}
                except Exception:
                    # jika body tidak JSON atau token tidak ada — tetap lanjut
                    pass
                resp.success()
            else:
                try:
                    print("login failed:", resp.status_code, resp.text)
                except Exception:
                    pass

    @task(1)
    def logout(self):
        # try logout using auth header if available
        # Logout: kirim header auth yang tersimpan jika ada. Jika endpoint logout
        # membutuhkan CSRF atau cookie, contoh ini perlu disesuaikan (mis. ekstrak
        # cookie dari respons login).
        with self.client.post(LOGOUT_ENDPOINT, headers=self.auth_headers or None, name="logout", catch_response=True) as resp:
            if resp.status_code in (200, 204):
                resp.success()
            else:
                try:
                    print("logout failed:", resp.status_code, resp.text)
                except Exception:
                    pass


class AuthUser(HttpUser):
    tasks = [AuthFlow]
    wait_time = between(1, 3)


if __name__ == "__main__":
    # Pesan singkat saat menjalankan file langsung dari Python.
    print("Jalankan dengan: locust -f locustfile_perf.py --host=http://localhost:8089")
