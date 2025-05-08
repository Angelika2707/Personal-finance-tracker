# Personal-finance-tracker
## Project description

Personal Finance Tracker is a simple web app for managing personal finances. 
Users can log incomes and expenses, categorize them, visualize spending patterns, and export data.

**Presentation:** [SQR_presentation](https://docs.google.com/presentation/d/1_ds7obSj6HQm796wyK8OcAuuLBzb5KHryja8f3HFAm4/edit?usp=sharing)

### Features
- Secure login and personal account
- Add, edit, delete financial records
- Categorize transactions (predefined & custom)
- Dashboard with information about financial records by period
- Export data (CSV or PDF)

### Tech Stack
- Python 3.12
- Poetry
- FastAPI
- SQLite
- Asynchronous SQLAlchemy 2.0
- Pydantic
- Alembic
- Streamlit
- Redis
- Pytest

## What Was Done
Features Implemented
- User registration and login (JWT token) - Anzhelika Akhmetova
- Add/edit/delete income and expense records - Anzhelika Akhmetova
- Add/edit/delete categories - Olesia Grediushko
- Categorize records - Olesia Grediushko
- Dashboard with analysis - Liubov Smirnova
- Export financial records to CSV or PDF - Liubov Smirnova

## Usage
### 1. Cloning a repository
```bash
git clone https://github.com/Angelika2707/Personal-finance-tracker
cd personal-finance-tracker
```
### 2. Dependency installation
```bash
poetry install
```

### 3. Application of migrations
```bash
alembic upgrade head
```
### 4. Generation of self-signed certificates and keys for JWTs

#### 4.1 SSL-certificate generation

You need to create a folder in the root of the project

```bash
mkdir "certs"
cd "certs"
```

Generate self-signed certificate and key for HTTPS

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -config openssl.cnf
```

- key.pem - private key for SSL/TLS connection
- cert.pem - self-signed certificate for HTTPS

#### 4.2 Key generation for JWT signature and verification

```bash
# Private key generation for JWT
openssl genpkey -algorithm RSA -out jwt-private.pem -pkeyopt rsa_keygen_bits:2048

# Generating a public key for the JWT
openssl rsa -pubout -in jwt-private.pem -out jwt-public.pem
```

- jwt-private.pem - private key for JWT signature
- jwt-public.pem - public key for JWT verification

### 5. Running Redis

```bash
docker compose -f redis-docker-compose.yml up -d
```

### 6. Running the backend (FastAPI)
Start the FastAPI server using the following command:

```bash
poetry run uvicorn src.app.api.main:app --host 127.0.0.1 --ssl-keyfile=certs/key.pem --ssl-certfile=certs/cert.pem --reload
```
Once started, the server will be available at: http://127.0.0.1:8000

API documentation will be available at the following links:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### 7. Running the frontend with Streamlit
```bash
poetry run streamlit run src/app/frontend/main.py
```

## Achieved quality metrics

### Maintainability

### **1. Documentation Coverage**  
**Tool**: `docstr-coverage`     
**Purpose**: Verify docstring presence for classes/methods (excluding properties and module-level docs)     
**Threshold**: Minimum 90% required     
```bash
> poetry run docstr-coverage
...
Total coverage: 91.2%  -  Grade: Great
```

### **2. Test Coverage**  
**Tool**: `pytest-cov`      
**Purpose**: Measure code coverage      
**Threshold**: Minimum 60% required     
```bash
> poetry run pytest src/tests/ --cov=src/app/ --cov-branch --cov-report=term-missing --cov-fail-under=60
...
Required test coverage of 60% reached. Total coverage: 85.65%
```

### **3. PEP8 Compliance**  
**Tool**: `flake8`      
**Purpose**: Enforce Python style guide adherence       
**Threshold**: Number of flake8 errors should be zero       
```bash
> poetry run flake8 src/
...   # empty output, no errors and warnings
```

### Reliability

### Performance

### Security
### **1. Bandit Security Scan**  
**Tool**: `bandit`     
**Purpose**: Identify common security vulnerabilities             
**Threshold**: Bandit report should not contain critical vulnerabilities          
```bash
> poetry run bandit -r src/app -x tests
...
Test results:
        No issues identified.

Code scanned:
        Total lines of code: 1697
        Total lines skipped (#nosec): 0

Run metrics:
        Total issues (by severity):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 0
        Total issues (by confidence):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 0
Files skipped (0):
```
### **2. Authentication Protection**
**Purpose**: Prevent brute-force attacks        
**Threshold**: Temporarily lock a user account after 5 consecutive failed login attempts. A notification is sent to the user upon lockout       
**Result**: Implemented in the application logic        