# Simple Fraud

This project aims to provide tools and scripts for detecting and analyzing fraudulent activities. 

## Features

- Fraud detection algorithms
- Data preprocessing
- Reporting and visualization

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/simple-fraud.git
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the main script:
   ```
   python main.py
   ```

## Folder Structure

- `src/` - Source code
- `data/` - Sample datasets
- `tests/` - Unit tests

## License

MIT License

## Contact

For questions or support, please contact [your.email@example.com](mailto:your.email@example.com).

// filepath: d:\Projects\New Work Prep\Simple fraud\README.md

# MicroSentinel: Anti-Fraud Transaction Monitoring System

## 1. Project Overview
**MicroSentinel** is a high-performance microservice designed for real-time transaction monitoring to detect fraudulent activities. The system ingests transaction data, analyzes it against a set of predefined rules, and returns a security verdict.

## 2. Goals and Objectives
* Develop a scalable REST API for high-throughput transaction processing.
* Implement **Velocity Checks** using an In-memory data store (Redis).
* Ensure reliable data persistence for transaction history and user profiles.
* Create an analytical layer for reporting suspicious activities.

## 3. Technology Stack
* **Language:** Python 3.12+ (Asyncio-based)
* **Web Framework:** FastAPI
* **In-Memory Store:** Redis (Counters, Rate Limiting)
* **Primary Database:** PostgreSQL (Raw SQL via `asyncpg` for maximum performance)
* **Infrastructure:** Docker, Docker Compose
* **Testing:** Pytest

---

## 4. Functional Requirements

### 4.1. Transaction Ingestion
The service provides a REST API endpoint `POST /v1/transactions` that accepts:
* `user_id`, `amount`, `currency`, `card_details`, `ip_address`, `geo_location`.

### 4.2. Rule Engine
Every transaction is processed through a pipeline of logic filters:
1.  **Velocity Check:** Verifies if the number of transactions exceeds the limit of $N$ per time window.
2.  **High-Amount Check:** Checks if the transaction amount exceeds a specific threshold for the user.
3.  **Geo-Mismatch:** Compares the current transaction's country with the user's registered home country.

### 4.3. Decision Making
The system returns one of the following statuses:
* `APPROVE`: Passed all security checks.
* `DECLINE`: Violated critical rules (e.g., Velocity limit).
* `REVIEW`: Suspicious activity flagged for manual inspection.

---

## 5. Data Architecture

### 5.1. Redis (Hot Data)
* Keys formatted as `velocity:{user_id}` with sliding/fixed window TTL.
* Atomic increments (`INCR`) to ensure thread-safe counting.

### 5.2. PostgreSQL (Cold Data)
* `users` table: Stores security profiles and baseline settings.
* `transactions` table: Audit log for all processed requests.
* **Note:** The system uses optimized **Raw SQL** queries for low-latency database interactions.

---

## 6. Non-Functional Requirements
* **Performance:** Target latency for a single transaction check is < 100ms.
* **Reliability:** Data integrity ensured via PostgreSQL ACID compliance.
* **Scalability:** Stateless design to allow horizontal scaling across multiple containers.

## 7. Roadmap (MVP)
1.  [ ] Setup Docker environment (Python + Redis + Postgres).
2.  [ ] Initialize database schema via SQL scripts.
3.  [ ] Implement Redis-based Velocity Check logic.
4.  [ ] Develop FastAPI endpoints and integrate the Rule Engine.
5.  [ ] Achieve 80%+ test coverage with Pytest.