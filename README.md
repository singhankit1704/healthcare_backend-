# Healthcare Backend API

A RESTful backend for a healthcare application built with Django, Django REST Framework, PostgreSQL, and JWT authentication.

---

## Tech Stack

- **Django 4.2** + **Django REST Framework**
- **PostgreSQL** (via psycopg2)
- **JWT Authentication** (djangorestframework-simplejwt)
- **python-dotenv** for environment config

---

## Project Structure

```
healthcare_backend/
├── healthcare_backend/   # Project config (settings, urls)
├── authentication/       # Register & login
├── patients/             # Patient CRUD
├── doctors/              # Doctor CRUD
├── mappings/             # Patient-Doctor assignments
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup Instructions

### 1. Clone & create virtual environment
```bash
git clone <repo-url>
cd healthcare_backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your values
```

**.env example:**
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_NAME=healthcare_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### 3. Create PostgreSQL database
```sql
CREATE DATABASE healthcare_db;
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Start the server
```bash
python manage.py runserver
```

---

## API Reference

### Authentication

#### `POST /api/auth/register/`
Register a new user.

**Request body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "password2": "SecurePass123"
}
```

**Response `201`:**
```json
{
  "message": "User registered successfully.",
  "user": { "id": 1, "name": "John Doe", "email": "john@example.com" }
}
```

---

#### `POST /api/auth/login/`
Login and receive JWT tokens.

**Request body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response `200`:**
```json
{
  "message": "Login successful.",
  "user": { "id": 1, "name": "John Doe", "email": "john@example.com" },
  "tokens": {
    "access": "<JWT_ACCESS_TOKEN>",
    "refresh": "<JWT_REFRESH_TOKEN>"
  }
}
```

> All subsequent requests require the header:
> `Authorization: Bearer <access_token>`

---

### Patient Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/patients/` | Add a new patient |
| `GET` | `/api/patients/` | Get all patients (created by you) |
| `GET` | `/api/patients/<id>/` | Get a specific patient |
| `PUT` | `/api/patients/<id>/` | Update a patient (partial update supported) |
| `DELETE` | `/api/patients/<id>/` | Delete a patient |

**Patient fields:**
```json
{
  "name": "Jane Smith",
  "age": 35,
  "gender": "F",
  "blood_group": "O+",
  "contact_number": "9876543210",
  "email": "jane@example.com",
  "address": "123 Main St, Bengaluru",
  "medical_history": "Diabetes Type 2"
}
```

**Gender values:** `M`, `F`, `O`  
**Blood group values:** `A+`, `A-`, `B+`, `B-`, `AB+`, `AB-`, `O+`, `O-`

---

### Doctor Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/doctors/` | Add a new doctor |
| `GET` | `/api/doctors/` | Get all doctors |
| `GET` | `/api/doctors/<id>/` | Get a specific doctor |
| `PUT` | `/api/doctors/<id>/` | Update a doctor (partial update supported) |
| `DELETE` | `/api/doctors/<id>/` | Delete a doctor |

**Doctor fields:**
```json
{
  "name": "Dr. Arjun Mehta",
  "specialization": "cardiologist",
  "email": "arjun@hospital.com",
  "contact_number": "9876500001",
  "license_number": "MH-2024-1234",
  "experience_years": 10,
  "qualification": "MBBS, MD (Cardiology)",
  "hospital": "Apollo Hospitals",
  "is_available": true
}
```

**Specializations:** `cardiologist`, `neurologist`, `orthopedic`, `pediatrician`, `dermatologist`, `psychiatrist`, `oncologist`, `radiologist`, `general`, `other`

**Optional query filters:**
- `GET /api/doctors/?specialization=cardiologist`
- `GET /api/doctors/?available=true`

---

### Patient-Doctor Mappings

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/mappings/` | Assign a doctor to a patient |
| `GET` | `/api/mappings/` | Get all mappings |
| `GET` | `/api/mappings/<patient_id>/` | Get all doctors for a patient |
| `DELETE` | `/api/mappings/delete/<id>/` | Remove a mapping |

**Assign doctor to patient:**
```json
{
  "patient_id": 1,
  "doctor_id": 2,
  "notes": "Referred for cardiac evaluation"
}
```

---

## Error Handling

All errors return descriptive JSON:

```json
{ "errors": { "email": ["A user with this email already exists."] } }
{ "error": "Invalid credentials. Please check your email and password." }
```

HTTP status codes used: `200`, `201`, `400`, `401`, `403`, `404`

---

## Security Notes

- Passwords are hashed using Django's PBKDF2 algorithm
- JWT access tokens expire in **24 hours**; refresh tokens in **7 days**
- Patients can only be viewed/edited/deleted by their creator
- Doctors can be viewed by all authenticated users, but edited/deleted only by their creator
- Never commit `.env` to version control
