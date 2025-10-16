# Microservices Image Processing with Flask and Redis

This project implements a **microservices-based image processing system** using **Python Flask** and **Redis** for caching.
The system accepts image uploads, generates a unique hash-based ID for each image, stores it in Redis, and performs multiple checks via independent microservices in parallel.

---

## Features

- Upload images via HTTP POST requests.
- Generate **MD5 hash-based IDs** for images.
- Cache images and results in **Redis** for faster responses.
- Perform multiple checks via **parallel microservice calls**:
  - Type Check
  - Resolution Check
  - Bandwidth Check
- Return results immediately if cached.
- Fail fast: returns failure if any microservice fails.

---

## Requirements

- Python 3.9+
- Flask
- Redis
- Requests library
- Concurrent Futures (comes with Python standard library)
- Redis server running locally or in Docker

---

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/souvik0602/Microservices-using-Python-Flask-Redis.git
cd Microservices-using-Python-Flask-Redis
