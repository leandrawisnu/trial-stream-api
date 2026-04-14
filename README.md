# Trial Stream API

Flask API untuk streaming data people dari PostgreSQL.

## Setup

1. Buat virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install flask flask-cors psycopg2-binary
```

3. Pastikan PostgreSQL berjalan dan database `stream-api` ada.

## Run

```bash
python api.py
```

Buka `http://localhost:5000` untuk melihat streaming data.