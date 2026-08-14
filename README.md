# fastapi-auth-bank

Starter project FastAPI dengan **Clean Architecture** (repository → service → controller), ORM **SQLAlchemy 2.x**, auth **JWT** (register + login), dan resource **bank_account** (get all + get by id).

## Struktur Project

```
fastapi-auth-bank/
├── app/
│   ├── main.py              # app factory, exception handler, router
│   ├── deps.py              # get_db, get_current_user (JWT dependency)
│   ├── core/                # config, database, security (bcrypt + JWT), exceptions
│   ├── models/              # SQLAlchemy models: User, BankAccount
│   ├── schemas/             # Pydantic schemas (request/response)
│   ├── repos/               # data access layer (SQL)
│   ├── services/            # business logic layer
│   └── controllers/         # HTTP layer (FastAPI routers)
├── alembic/                 # database migrations
├── tests/                   # pytest unit + endpoint tests
├── docker-compose.yml       # PostgreSQL lokal
└── Makefile                 # command shortcut
```

Alur: **Controller → Service → Repository → DB**. Service pegang business logic, repository pegang query SQL, controller pegang HTTP.

## Requirements

- Python 3.10+
- PostgreSQL (atau jalankan `make db-up` untuk docker)
- Docker (opsional, untuk PostgreSQL)

## Setup

```bash
# 1. buat venv + install dependency
make setup

# 2. (opsional) jalanin PostgreSQL via docker
make db-up

# 3. buat .env dari contoh
cp .env.example .env
# lalu isi SECRET_KEY dengan string acak panjang, dan pastikan DATABASE_URL benar

# 4. buat + jalankan migration
make migrate-auto
make migrate

# 5. jalankan server
make run
```

Docs API otomatis: http://localhost:8000/docs

## Endpoints

| Method | Path                            | Auth | Keterangan                        |
|--------|---------------------------------|------|-----------------------------------|
| POST   | `/api/v1/auth/register`         | -    | Register user baru                |
| POST   | `/api/v1/auth/login`            | -    | Login, dapat `access_token` (JWT) |
| GET    | `/api/v1/bank-accounts`         | Yes  | Semua bank account user login     |
| GET    | `/api/v1/bank-accounts/{id}`    | Yes  | Bank account by id (milik user)   |
| GET    | `/health`                       | -    | Health check                      |

Contoh flow:

```bash
# register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"supersecret"}'

# login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"supersecret"}'
# -> {"access_token":"eyJ...","token_type":"bearer"}

# get all bank accounts (pakai token dari login)
curl http://localhost:8000/api/v1/bank-accounts \
  -H "Authorization: Bearer eyJ..."
```

Catatan: endpoint `/bank-accounts` baru punya GET (get all + get by id). Fitur create/update/delete ada di **Soal Latihan** di bawah — data untuk testing bisa diisi langsung via database/migration atau dari hasil mengerjakan soal.

## Test

Unit test memakai **SQLite in-memory**, jadi tidak butuh PostgreSQL jalan.

```bash
make test
```

Atau langsung:

```bash
.venv/bin/python -m pytest -v
```

Cakupan test: belum ada test file — semua test dibuat lewat **Soal Latihan** di bawah (fixture `db_session` + `client` sudah siap di `tests/conftest.py`). Catatan: sebelum ada test file, `pytest` akan bilang `no tests ran` dengan exit code 5 — itu normal, bukan error.

## Soal Latihan

Ada 3 latihan: **unit test auth**, **API CRUD bank_account + test-nya**, dan **entity `user_accounts` + CRUD + test-nya**. Kerjakan berurutan.

### Latihan 1: Unit test untuk Auth (register + login + JWT)

Fitur auth sudah jadi di `app/services/auth_service.py` dan `app/controllers/auth_controller.py`. Tugasmu: tulis unit test-nya dari nol, pakai fixture yang sudah ada.

Buat 2 file test baru:

**`tests/unit/test_auth_service.py`** — service layer (`AuthService` + `UserRepository` + `db_session`):
- `register` sukses → user tersimpan, `id` terisi, `hashed_password` ≠ password plain, `is_active` true
- `register` dengan email huruf besar → tersimpan lowercase
- `register` email duplikat → `ConflictError`
- `authenticate` kredensial benar → user kembali
- `authenticate` password salah → `InvalidCredentialsError`
- `authenticate` email tidak dikenal → `InvalidCredentialsError`
- `issue_token` lalu `get_user_from_token` → token valid, `id` cocok
- `get_user_from_token` dengan token invalid → error (401)

**`tests/unit/test_auth_endpoints.py`** — endpoint layer via `client` (TestClient):
- `POST /api/v1/auth/register` → `201`, response berisi email benar, `hashed_password` **tidak bocor**
- register email duplikat → `409`
- register password pendek (`< 8` char) → `422`
- `POST /api/v1/auth/login` → `200`, body punya `access_token` + `token_type: "bearer"`
- login password salah → `401`
- `GET /api/v1/bank-accounts` tanpa token → `401` (proteksi JWT)

Kriteria penerimaan:
- [ ] `make test` → semua test auth pass.
- [ ] Test service tidak butuh HTTP (langsung instansiasi service).
- [ ] Test memakai fixture `db_session` / `client`, bukan koneksi PostgreSQL.

### Latihan 2: API CRUD bank_account + unit test

Tambahkan API **create, update, delete** untuk resource `bank_account`, lengkap dengan unit test-nya. Kerjakan mengikuti pola clean architecture yang sudah ada (controller → service → repository).

#### Spesifikasi endpoint

| Method | Path                          | Auth | Body                                              | Response                             |
|--------|-------------------------------|------|---------------------------------------------------|--------------------------------------|
| POST   | `/api/v1/bank-accounts`       | Yes  | `account_number`, `account_name`, `bank_name`, `balance?` | `201` → `BankAccountResponse` |
| PUT    | `/api/v1/bank-accounts/{id}`  | Yes  | `account_name`, `bank_name`, `balance`             | `200` → `BankAccountResponse`        |
| DELETE | `/api/v1/bank-accounts/{id}`  | Yes  | -                                                 | `204` (tanpa body)                   |

#### Aturan bisnis

- Semua endpoint wajib pakai `get_current_user` (JWT).
- Hanya **pemilik** akun yang boleh update/delete — akun user lain dianggap tidak ada (404).
- `account_number` harus unik → duplikat return `409 Conflict`.
- `balance` tidak boleh negatif → return `422` (pakai validasi Pydantic).
- `account_number` tidak boleh diubah lewat PUT (hanya `account_name`, `bank_name`, `balance`).
- Kalau id tidak ditemukan / bukan milik user → `404 Not Found`.

#### Petunjuk pengerjaan

1. **Schemas** (`app/schemas/bank_account.py`): tambah `BankAccountCreate` dan `BankAccountUpdate` (pakai `Field(ge=0)` untuk balance).
2. **Repository** (`app/repos/bank_account_repo.py`): tambah method `get_by_account_number`, `create_account`, `update_account`, `delete_account`.
3. **Service** (`app/services/bank_account_service.py`): tambah `create_account`, `update_account`, `delete_account`. Business logic di sini — cek duplikat account_number → `ConflictError`, cek ownership/eksistensi → `NotFoundError`.
4. **Controller** (`app/controllers/bank_account_controller.py`): tambah 3 endpoint di atas.
5. Cek dengan curl / docs http://localhost:8000/docs.

#### Unit test yang harus dibuat

Buat 2 file test baru, pakai fixture `db_session` + `client` dari `tests/conftest.py`:

**`tests/unit/test_bank_account_service_crud.py`** — service layer:
- `create` sukses → data tersimpan, `account_number` benar
- `create` dengan `account_number` duplikat → `ConflictError`
- `update` sukses → field berubah
- `update` akun milik user lain → `NotFoundError`
- `update` id tidak ada → `NotFoundError`
- `delete` sukses → akun hilang dari list
- `delete` akun milik user lain → `NotFoundError`

**`tests/unit/test_bank_account_crud_endpoints.py`** — endpoint layer via `TestClient`:
- `POST` create → `201`, response berisi data benar, `hashed_password` tidak bocor
- `POST` create duplikat → `409`
- `POST` create tanpa token → `401`
- `PUT` update → `200`, field berubah
- `PUT` update akun user lain → `404`
- `PUT` dengan `balance` negatif → `422`
- `DELETE` → `204`
- `DELETE` akun user lain → `404`

#### Kriteria penerimaan

- [ ] `make test` → semua test pass (termasuk 16 test CRUD baru di atas).
- [ ] Kode mengikuti alur clean architecture (controller tidak menulis query, service tidak menulis SQL).
- [ ] Ownership check ada di **service**, bukan controller.
- [ ] Tidak ada test yang butuh PostgreSQL berjalan.

### Latihan 3: Entity `user_accounts` (user mendaftarkan bank account) + CRUD + unit test

> Prasyarat: selesaikan **Latihan 2** dulu, karena `user_accounts` mereferensikan `bank_accounts`. Untuk keperluan test, data `BankAccount` bisa dibuat langsung via `db_session` tanpa harus lewat API.

Buat entity baru **`user_accounts`** — tempat user **mendaftarkan bank account** ke profile mereka. Setiap baris = satu registrasi: user + bank_account + info tambahan (label, primary, status).

#### Spesifikasi entity (tabel `user_accounts`)

| Kolom            | Tipe                         | Keterangan                                         |
|------------------|------------------------------|----------------------------------------------------|
| `id`             | int PK autoincrement         |                                                    |
| `user_id`        | FK `users.id` (CASCADE)      | index                                              |
| `bank_account_id`| FK `bank_accounts.id` (CASCADE) | index                                           |
| `label`          | varchar(255) nullable        | nama panggilan, mis. "Gaji"                        |
| `is_primary`     | boolean default `False`      | maksimal 1 `True` per user                         |
| `status`         | varchar(20) default `active` | hanya `active` / `inactive`                        |
| `created_at` / `updated_at` | pakai `TimestampMixin` |                                     |

Tambahkan **`UniqueConstraint(user_id, bank_account_id)`** — user tidak boleh daftarkan bank account yang sama dua kali.

#### Spesifikasi endpoint

| Method | Path                            | Auth | Body                                       | Response                              |
|--------|---------------------------------|------|--------------------------------------------|---------------------------------------|
| POST   | `/api/v1/user-accounts`         | Yes  | `bank_account_id`, `label?`, `is_primary?` | `201` → `UserAccountResponse`         |
| GET    | `/api/v1/user-accounts`         | Yes  | -                                          | `200` → `list[UserAccountResponse]`   |
| GET    | `/api/v1/user-accounts/{id}`    | Yes  | -                                          | `200` → `UserAccountResponse`         |
| PUT    | `/api/v1/user-accounts/{id}`    | Yes  | `label?`, `is_primary?`, `status?`         | `200` → `UserAccountResponse`         |
| DELETE | `/api/v1/user-accounts/{id}`    | Yes  | -                                          | `204` (tanpa body)                    |

#### Aturan bisnis

- Semua endpoint wajib pakai `get_current_user` (JWT).
- Hanya **pemilik** yang boleh lihat/update/delete — registrasi user lain dianggap tidak ada (404).
- `bank_account_id` harus ada **dan milik user** — kalau tidak ada / milik user lain → `404`.
- Daftarkan bank account yang sama dua kali → `409 Conflict` (cek di service + `UniqueConstraint` di DB).
- `status` hanya `active` / `inactive` → selain itu `422` (pakai `Literal` di Pydantic).
- `is_primary` di-set `true` → otomatis set `is_primary=false` untuk registrasi lain milik user yang sama (hanya 1 primary per user).
- Kalau id tidak ditemukan / bukan milik user → `404 Not Found`.

#### Petunjuk pengerjaan

1. **Model** (`app/models/user_account.py`): class `UserAccount`, relasi `User.user_accounts` dan `BankAccount.user_accounts` (back_populates), `UniqueConstraint`. Daftarkan di `app/models/__init__.py`.
2. **Migration**: `make db-up` lalu `make migrate-auto` dan `make migrate` (butuh PostgreSQL jalan).
3. **Schemas** (`app/schemas/user_account.py`): `UserAccountCreate`, `UserAccountUpdate` (semua field optional, `status: Literal["active", "inactive"]`), `UserAccountResponse` (`from_attributes=True`).
4. **Repository** (`app/repos/user_account_repo.py`): `UserAccountRepository` — `list_by_user`, `get_by_id_for_user`, `get_by_user_and_bank_account` (cek duplikat), `create_account`, `update_account`, `delete_account`.
5. **Service** (`app/services/user_account_service.py`): `UserAccountService` — business logic di sini (cek eksistensi/ownership bank account → 404, cek duplikat → 409, logika `is_primary`).
6. **Controller** (`app/controllers/user_account_controller.py`): router prefix `/user-accounts`, daftarkan di `app/main.py`.
7. Cek dengan curl / docs http://localhost:8000/docs.

#### Unit test yang harus dibuat

Buat 2 file test baru, pakai fixture `db_session` + `client` dari `tests/conftest.py`:

**`tests/unit/test_user_account_service.py`** — service layer:
- `create` sukses → tersimpan, relasi `user_id` + `bank_account_id` benar
- `create` dengan `bank_account_id` milik user lain → `NotFoundError`
- `create` dengan `bank_account_id` tidak ada → `NotFoundError`
- `create` bank account yang sudah didaftarkan user yang sama → `ConflictError`
- `create` dengan `is_primary=true` → registrasi lain milik user itu jadi `is_primary=false`
- `list` → hanya milik user, tidak bocor punya user lain
- `get` by id sukses
- `get` by id milik user lain → `NotFoundError`
- `update` `label` / `status` / `is_primary` sukses → field berubah
- `update` milik user lain → `NotFoundError`
- `delete` sukses → hilang dari list
- `delete` milik user lain → `NotFoundError`

**`tests/unit/test_user_account_endpoints.py`** — endpoint layer via `client` (TestClient):
- `POST` create → `201`, response berisi `bank_account_id` + `status: "active"`
- `POST` tanpa token → `401`
- `POST` dengan `bank_account_id` milik user lain → `404`
- `POST` duplikat → `409`
- `GET` list → `200`, hanya registrasi milik user
- `GET` by id → `200`
- `GET` by id milik user lain → `404`
- `PUT` update `label` → `200`, label berubah
- `PUT` dengan `status` invalid → `422`
- `DELETE` → `204`
- `DELETE` milik user lain → `404`

#### Kriteria penerimaan

- [ ] `make test` → semua test pass (termasuk 23 test `user_accounts` di atas).
- [ ] `UniqueConstraint(user_id, bank_account_id)` ada di model + migration.
- [ ] Logika "hanya 1 `is_primary` per user" ada di service, bukan controller.
- [ ] Kode mengikuti alur clean architecture (controller tidak menulis query, service tidak menulis SQL).
- [ ] Tidak ada test yang butuh PostgreSQL berjalan.


## Config Environment (`.env`)

| Variabel                        | Default                                                    | Keterangan                     |
|---------------------------------|------------------------------------------------------------|--------------------------------|
| `DATABASE_URL`                  | `postgresql+psycopg2://postgres:postgres@localhost:5432/bank_db` | Connection string DB        |
| `SECRET_KEY`                    | (wajib ganti di production)                                | Secret signing JWT             |
| `ALGORITHM`                     | `HS256`                                                    | Algoritma JWT                  |
| `ACCESS_TOKEN_EXPIRE_MINUTES`   | `60`                                                       | Umur token (menit)             |

## Migration dengan Alembic

```bash
# generate migration dari model (butuh DB jalan)
.venv/bin/alembic revision --autogenerate -m "init"

# apply
.venv/bin/alembic upgrade head
```

## Keamanan

- Password di-hash dengan **bcrypt** (bukan plain text).
- Token JWT HS256, expired otomatis per `ACCESS_TOKEN_EXPIRE_MINUTES`.
- Bank account ter-isolasi per user — user tidak bisa akses account milik user lain (404).
- **Jangan pernah** commit `.env` (sudah di `.gitignore`). Ganti `SECRET_KEY` sebelum production.
