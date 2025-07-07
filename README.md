# News App Project

This project consists of a Python-based server and a client for interacting with news articles, user authentication, notifications, and more.

## Prerequisites

- Python 3.10+
- Git

## Setup Instructions

### 1. Create and Activate a Virtual Environment

On Windows:

```
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:

```
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Requirements

```
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and fill in the required values (see below for example).

### 4. Database Setup

- The server uses SQLite by default. The schema is in `server/schema.sql`.
- To initialize the database, run the server once or use the provided scripts if available.

## Running the Server

Navigate to the project root and run:

```
uvicorn server.main:app
```

## Running the Client

Navigate to the project root and run:

```
python client/main.py
```

## Folder Structure

- `server/` - Backend API, database, and business logic
- `client/` - Command-line client interface

## Example .env

```
OPENAI_API_KEY="sk-proj-pDb-uluMKyLaCctid6PJe9kmPUbspa74GQA"
NEWS_API_KEY="f32547eb306"
THENEWS_API_KEY="VzEIM0fpYJB0R3zfH"
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=anmolamil.com
SMTP_PASSWORD=ojaf
FROM_EMAIL=anmogmail.com
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---
