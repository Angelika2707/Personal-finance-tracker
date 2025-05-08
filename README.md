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

#### **1. Documentation Coverage**  
**Tool**: `docstr-coverage`     
**Purpose**: Verify docstring presence for classes/methods (excluding properties and module-level docs)     
**Threshold**: Minimum 90% required     
```bash
> poetry run docstr-coverage
...
Total coverage: 91.2%  -  Grade: Great
```

#### **2. Test Coverage**  
**Tool**: `pytest-cov`      
**Purpose**: Measure code coverage      
**Threshold**: Minimum 60% required     
```bash
> poetry run pytest src/tests/ --cov=src/app/ --cov-branch --cov-report=term-missing --cov-fail-under=60
...
Required test coverage of 60% reached. Total coverage: 85.65%
```

#### **3. PEP8 Compliance**  
**Tool**: `flake8`      
**Purpose**: Enforce Python style guide adherence       
**Threshold**: Number of flake8 errors should be zero       
```bash
> poetry run flake8 src/
...   # empty output, no errors and warnings
```

### Reliability
#### **Error rate for API responses in the application**
**Tool**:                 
**Threshold**: <= 1%                    

![Error rate](/error_rate.png)

### Performance
Performance tests were conducted using Apache Benchmark (ab) with the following parameters:
- **Number of requests:** 1000 (-n 1000)
- **Concurrency level:** 10 simultaneous connections (-c 10)
- **Tested endpoints:** GET https://127.0.0.1:8000/financial_records/, GET https://127.0.0.1:8000/categories/, POST https://127.0.0.1:8000/users/register

**Threshold:** Less than 300 milliseconds for 95% of API requests    
  
**1. Checking GET on financial_records**
```bash
> ab -n 1000 -c 10 https://127.0.0.1:8000/financial_records/
Document Path:          /financial_records/
Document Length:        30 bytes

Concurrency Level:      10
Time taken for tests:   8.550 seconds
Complete requests:      1000
Failed requests:        0
Non-2xx responses:      1000
Total transferred:      184000 bytes
HTML transferred:       30000 bytes
Requests per second:    116.95 [#/sec] (mean)
Time per request:       85.505 [ms] (mean)
Time per request:       8.550 [ms] (mean, across all concurrent requests)
Transfer rate:          21.01 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:       18   67  31.6     61     371
Processing:     2   18  16.2     14     266
Waiting:        1   17  13.6     14     192
Total:         22   85  36.1     75     401

Percentage of the requests served within a certain time (ms)
  50%     75
  66%     81
  75%     89
  80%     95
  90%    114
  95%    141
  98%    178
  99%    323
 100%    401 (longest request)
```
**2. Checking GET on categories**
```bash
> ab -n 1000 -c 10 https://127.0.0.1:8000/categories/
Document Path:          /categories
Document Length:        0 bytes

Concurrency Level:      10
Time taken for tests:   8.897 seconds
Complete requests:      1000
Failed requests:        0
Non-2xx responses:      1000
Total transferred:      173000 bytes
HTML transferred:       0 bytes
Requests per second:    112.40 [#/sec] (mean)
Time per request:       88.971 [ms] (mean)
Time per request:       8.897 [ms] (mean, across all concurrent requests)
Transfer rate:          18.99 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:       16   70  37.3     62     272
Processing:     2   18  13.3     16     150
Waiting:        1   17  13.0     15     150
Total:         18   88  39.8     76     284

Percentage of the requests served within a certain time (ms)
  50%     76
  66%     84
  75%     92
  80%     96
  90%    131
  95%    185
  98%    232
  99%    270
 100%    284 (longest request)
```
**3. Checking POST on user/register**
```bash
> ab -n 1000 -c 10 -p test_input.json -T application/json https://127.0.0.1:8000/users/register
Document Path:          /users/register
Document Length:        0 bytes

Concurrency Level:      10
Time taken for tests:   8.395 seconds
Complete requests:      1000
Failed requests:        0
Non-2xx responses:      1000
Total transferred:      177000 bytes
Total body sent:        220000
HTML transferred:       0 bytes
Requests per second:    119.12 [#/sec] (mean)
Time per request:       83.947 [ms] (mean)
Time per request:       8.395 [ms] (mean, across all concurrent requests)
Transfer rate:          20.59 [Kbytes/sec] received
                        25.59 kb/s sent
                        46.18 kb/s total

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:       29   65  24.1     61     205
Processing:     2   17  15.3     13     171
Waiting:        2   16  14.8     13     171
Total:         43   82  28.3     73     259

Percentage of the requests served within a certain time (ms)
  50%     73
  66%     82
  75%     90
  80%     95
  90%    109
  95%    141
  98%    182
  99%    202
 100%    259 (longest request)
```  


### Security
#### **1. Bandit Security Scan**  
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
#### **2. Authentication Protection**
**Purpose**: Prevent brute-force attacks        
**Threshold**: Temporarily lock a user account after 5 consecutive failed login attempts. A notification is sent to the user upon lockout       
**Result**: Implemented in the application logic        
