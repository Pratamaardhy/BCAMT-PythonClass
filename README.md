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

Cakupan test:
- `tests/unit/test_auth_service.py` — register, login, hash, token
- `tests/unit/test_auth_endpoints.py` — endpoint register/login + proteksi JWT via TestClient

## Soal Latihan

Tambahkan API **create, update, delete** untuk resource `bank_account`, lengkap dengan unit test-nya. Kerjakan mengikuti pola clean architecture yang sudah ada (controller → service → repository).

### Spesifikasi endpoint

| Method | Path                          | Auth | Body                                              | Response                             |
|--------|-------------------------------|------|---------------------------------------------------|--------------------------------------|
| POST   | `/api/v1/bank-accounts`       | Yes  | `account_number`, `account_name`, `bank_name`, `balance?` | `201` → `BankAccountResponse` |
| PUT    | `/api/v1/bank-accounts/{id}`  | Yes  | `account_name`, `bank_name`, `balance`             | `200` → `BankAccountResponse`        |
| DELETE | `/api/v1/bank-accounts/{id}`  | Yes  | -                                                 | `204` (tanpa body)                   |

### Aturan bisnis

- Semua endpoint wajib pakai `get_current_user` (JWT).
- Hanya **pemilik** akun yang boleh update/delete — akun user lain dianggap tidak ada (404).
- `account_number` harus unik → duplikat return `409 Conflict`.
- `balance` tidak boleh negatif → return `422` (pakai validasi Pydantic).
- `account_number` tidak boleh diubah lewat PUT (hanya `account_name`, `bank_name`, `balance`).
- Kalau id tidak ditemukan / bukan milik user → `404 Not Found`.

### Petunjuk pengerjaan

1. **Schemas** (`app/schemas/bank_account.py`): tambah `BankAccountCreate` dan `BankAccountUpdate` (pakai `Field(ge=0)` untuk balance).
2. **Repository** (`app/repos/bank_account_repo.py`): tambah method `get_by_account_number`, `create_account`, `update_account`, `delete_account`.
3. **Service** (`app/services/bank_account_service.py`): tambah `create_account`, `update_account`, `delete_account`. Business logic di sini — cek duplikat account_number → `ConflictError`, cek ownership/eksistensi → `NotFoundError`.
4. **Controller** (`app/controllers/bank_account_controller.py`): tambah 3 endpoint di atas.
5. Cek dengan curl / docs http://localhost:8000/docs.

### Unit test yang harus dibuat

Buat 2 file test baru (pola sama seperti file test yang sudah ada, pakai fixture `db_session` + `client` dari `tests/conftest.py`):

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

### Kriteria penerimaan

- [ ] `make test` → semua test pass (termasuk 16 test CRUD baru di atas).
- [ ] Kode mengikuti alur clean architecture (controller tidak menulis query, service tidak menulis SQL).
- [ ] Ownership check ada di **service**, bukan controller.
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
