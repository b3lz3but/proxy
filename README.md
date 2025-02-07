# 🚀 Enterprise Proxy Manager v6.0

## 📖 Overview

Enterprise Proxy Manager v6.0 is a **fully automated, scalable, and AI-powered proxy solution** designed for **enterprise-level proxy management**. It includes:

- **Multi-Cloud Deployment** (AWS, GCP, DigitalOcean, Kubernetes)
- **AI-Based Proxy Rotation & Load Balancing**
- **High-Security Firewall & Fail2Ban Protection**
- **Web Dashboard & REST API for Management**
- **Kubernetes Auto-Scaling**
- **Real-Time Analytics & Monitoring**
- **Optimized for Performance & Security**

---

## 📂 Folder Structure

```
enterprise-proxy-v6/
│── docker-compose.yml
│── Dockerfile
│── proxy_manager.py
│── squid/
│   ├── squid.conf
│── haproxy/
│   ├── haproxy.cfg
│── web-dashboard/
│   ├── index.html
│── config/
│   ├── settings.json
│── logs/
│   ├── proxy_usage.log
│── scripts/
│   ├── auto_scale.sh
│   ├── log_cleaner.sh
│── terraform/
│   ├── aws.tf
│── kubernetes/
│   ├── proxy-deployment.yaml
```

---

## 🏗 Installation

### 📥 **1. Clone Repository**

```sh
git clone https://github.com/your-repo/enterprise-proxy-manager.git
cd enterprise-proxy-manager
```

### 🐳 **2. Install Docker & Docker-Compose**

```sh
sudo apt update && sudo apt install -y docker docker-compose
```

### 🚀 **3. Start Services**

```sh
docker-compose up --build -d
```

### ✅ **4. Check Running Containers**

```sh
docker ps
```

---

## 🎛 **Usage**

### 📡 **1. Access Web Dashboard**

Visit: **http://localhost:8081**  

### 🛠 **2. Use API Endpoints**

#### **List Active Proxies**

```sh
curl -X GET http://localhost:5000/api/v1/proxies
```

#### **Enable Firewall Rules**

```sh
curl -X POST http://localhost:5000/api/firewall -H "Content-Type: application/json" -d '{"action": "ALLOW"}'
```

#### **View Proxy Analytics**

```sh
curl -X GET http://localhost:5000/api/v1/analytics
```

#### **Auto-Scale Proxy Instances**

```sh
curl -X POST http://localhost:5000/api/v1/autoscale -H "Content-Type: application/json" -d '{"instances": 3}'
```

---

## 🏆 **Features**

✅ **AI-Based Proxy Rotation & Scaling**  
✅ **Zero-Trust Security (Firewall + Fail2Ban)**  
✅ **FastAPI for High Performance**  
✅ **WebSocket Support for Faster API Calls**  
✅ **Real-Time Analytics & Monitoring**  
✅ **Automated Log Cleaning & Performance Tuning**  
✅ **Docker & Kubernetes Ready**  
✅ **Terraform Deployment for Multi-Cloud Support**  

---

## 🏗 **Deployment to Kubernetes**

### 📌 **1. Install kubectl & Helm**

```sh
sudo apt install kubectl helm
```

### 📌 **2. Deploy to Kubernetes**

```sh
kubectl apply -f kubernetes/proxy-deployment.yaml
```

---

## 🔥 **Automation Scripts**

### **Auto-Scale Proxies**

```sh
bash scripts/auto_scale.sh
```

### **Log Cleanup**

```sh
bash scripts/log_cleaner.sh
```

---

## 🛡 Security Enhancements

✔ **Fail2Ban Protection**  
✔ **Firewall Auto-Configuration**  
✔ **Authentication for Proxy Access**  

---

## 🏆 **Contributions**

Feel free to **contribute, report issues, or suggest improvements!** 🚀  

---

## 📜 **License**

This project is **open-source** under the MIT License.
