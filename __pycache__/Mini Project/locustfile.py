import random
from locust import HttpUser, task, between

class KaryawanUser(HttpUser):
    # Jeda waktu (dalam detik) antar request yang dilakukan oleh setiap simulated user (virtual user)
    wait_time = between(1, 3)

    # Variabel untuk menyimpan ID yang dibuat saat POST, agar bisa dipakai untuk GET Single dan PUT
    created_id = None

    @task(3)
    def get_list_karyawan(self):
        """Menguji endpoint GET List Karyawan (/api/karyawan)"""
        with self.client.get("/api/karyawan", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                # Jika data ada, kita bisa ambil salah satu ID secara random untuk diuji di GET Single
                try:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        random_item = random.choice(data)
                        self.last_fetched_id = random_item.get("id")
                except Exception:
                    pass
            else:
                response.failure(f"Gagal GET List: Status code {response.status_code}")

    @task(2)
    def get_single_karyawan(self):
        """Menguji endpoint GET Single Karyawan (/api/karyawan/{id})"""
        # Gunakan ID yang baru dibuat, atau fallback ke ID 1 jika belum ada
        target_id = self.created_id if self.created_id else 1
        
        with self.client.get(f"/api/karyawan/{target_id}", catch_response=True) as response:
            if response.status_code in [200, 404]:
                # 404 dianggap valid jika ID belum ada di database saat test awal
                response.success()
            else:
                response.failure(f"Gagal GET Single ID {target_id}: Status code {response.status_code}")

    @task(1)
    def post_karyawan(self):
        """Menguji endpoint POST Karyawan (/api/karyawan)"""
        random_num = random.randint(1000, 9999)
        payload = {
            "nama": f"User LoadTest {random_num}",
            "alamat": f"Jl. Sudirman No. {random_num}, Jakarta",
            "dob": "1995-05-12",
            "status": "Active",
            "avatar": "default.png",
            "username": f"user_load_{random_num}",
            "password": "password123",
            "role": "ROLE_USER"
        }
        
        with self.client.post("/api/karyawan", json=payload, catch_response=True) as response:
            if response.status_code in [200, 201]:
                response.success()
                try:
                    data = response.json()
                    # Simpan ID yang baru di-generate server untuk digunakan pada method PUT
                    if "id" in data:
                        self.created_id = data["id"]
                except Exception:
                    pass
            else:
                response.failure(f"Gagal POST Karyawan: Status code {response.status_code}")

    @task(1)
    def put_karyawan(self):
        """Menguji endpoint PUT Karyawan (/api/karyawan/{id})"""
        # Hanya jalankan PUT jika sudah ada ID yang pernah dibuat lewat POST
        if not self.created_id:
            return

        random_num = random.randint(1000, 9999)
        payload = {
            "nama": f"User Update {random_num}",
            "alamat": f"Jl. HR Rasuna Said No. {random_num}, Jakarta",
            "dob": "1995-05-12",
            "status": "Active",
            "avatar": "updated.png",
            "username": f"user_load_up_{random_num}",
            "password": "newpassword123",
            "role": "ROLE_USER"
        }

        with self.client.put(f"/api/karyawan/{self.created_id}", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Gagal PUT Karyawan ID {self.created_id}: Status code {response.status_code}")