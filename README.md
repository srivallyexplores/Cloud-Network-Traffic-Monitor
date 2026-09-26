# NetMonitor: Real-Time Network Performance Analyzer

## 📌 Project Overview
**NetMonitor** is a lightweight, Python-based network monitoring tool that captures, analyzes, and visualizes real-time TCP/IP traffic to identify issues like latency, packet loss, and ARP cache problems. It automates responses to bottlenecks and is suitable for both local development and cloud deployment.

---

## 🧰 Tech Stack
- **Backend**: Python (Flask, Scapy)
- **Frontend**: HTML, CSS, Chart.js
- **Database**: SQLite
- **Scripting**: Bash (Unix)
- **Deployment**: Docker, AWS EC2 (Ubuntu 22.04)

---

## 🖥️ Local Development (VS Code)

### 🔧 Prerequisites
- Python 3.10+
- pip
- VS Code with Python extension
- Git (optional)

### 📂 Project Structure
```
NETMONITOR/
├── app.py                 # Flask application
├── monitor.py             # Network packet analyzer
├── autofix.py             # Bottleneck resolution scripts
├── system_utils.py        # Utility functions for network/system operations
├── network_metrics.db     # SQLite database
├── templates/
│   └── dashboard.html     # Web interface
```

### 🪜 Setup Instructions
```bash
git clone https://github.com/your-username/netmonitor.git
cd netmonitor
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py  # Runs on http://localhost:5000
```

### ⚙️ Scripts for Testing
- `monitor.py` captures real-time network stats using Scapy
- `autofix.py` automates resolution of detected network issues
- `system_utils.py` supports low-level operations (e.g., clearing ARP cache, IP table management)

---

## ☁️ Deployment on AWS EC2

### 🔧 EC2 Setup
1. Launch EC2 instance (Ubuntu 22.04)
2. Allow inbound ports: `22 (SSH)`, `80 (HTTP)`, `5000 (Flask)`
3. Download the `.pem` key (e.g., `netmonitor-key.pem`)
4. Connect from VS Code:
```bash
chmod 400 netmonitor-key.pem
ssh -i "netmonitor-key.pem" ubuntu@<EC2-PUBLIC-IP>
```

### 📦 Install Docker on EC2
```bash
sudo apt update && sudo apt install docker.io -y
sudo systemctl start docker
sudo usermod -aG docker ubuntu
```

### 🐳 Docker Setup

#### Dockerfile
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y \
    tshark tcpdump net-tools iproute2 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

#### Build and Run
```bash
docker build -t netmonitor .
docker run -p 5000:5000 netmonitor
```
Access via `http://<EC2-PUBLIC-IP>:5000`

---

## 📦 requirements.txt
```text
Flask==2.2.5
scapy==2.5.0
```

---

## 📊 Features
- Real-time TCP/IP traffic capture
- Latency, ARP cache, packet loss metrics
- SQLite for persistent logging
- Automated responses to network issues
- Web dashboard with Chart.js
- Portable via Docker

---

## ✅ Future Improvements
- Role-based access for dashboard
- Export metrics to CSV/Excel
- Email alerts for anomalies
- Kubernetes deployment

---

## 🙌 Authors
- Ayushman Sharan
- Contributors welcome!

