# Cloud AI Sentiment Analyzer Microservice ☁️🤖

An end-to-end cloud-native microservice application demonstrating containerization, Kubernetes orchestration, CI/CD automation, cloud security, and serverless AI model integration.

This repository fulfills the curriculum requirements for the **Cloud Computing Laboratory (210CMEPCC302)** at _D. Y. Patil College of Engineering & Technology, Kolhapur_.

---

## 📌 Project Overview

This project implements a scalable microservice architecture for real-time text sentiment analysis. The stack incorporates a Python Flask REST API backend, Docker containerization, Kubernetes cluster orchestration, GitHub Actions CI/CD pipeline automation, and Hugging Face NLP AI integration.

---

## 🎓 Academic Syllabus Mapping (6-Unit Coverage)

| Unit / Syllabus Module       | Lab Experiment Alignment                           | Technical Implementation                                                  |
| :--------------------------- | :------------------------------------------------- | :------------------------------------------------------------------------ |
| **Unit 1: Architecture**     | Client/Server & Microservices (Exp 1)              | Python Flask RESTful API (`app.py`) providing JSON endpoints.             |
| **Unit 2: Virtualization**   | Type 1/2 Hypervisors & Docker (Exp 2-4, 8, 9)      | Multi-stage `Dockerfile` and OS-level container isolation.                |
| **Unit 3: Orchestration**    | Infrastructure as a Service (Exp 5, 13)            | Kubernetes Deployment with 2 Pod Replicas & LoadBalancer Service.         |
| **Unit 4: DevOps Pipelines** | Public Cloud Deployment (Exp 10-12)                | Automated GitHub Actions CI/CD workflow (`.github/workflows/deploy.yml`). |
| **Unit 5: Cloud Security**   | Cloud Security & Credentials                       | Kubernetes Secrets (`ai-secret`) managing API authentication tokens.      |
| **Unit 6: Cloud Apps & AI**  | Software/Platform as a Service & UI (Exp 6, 7, 14) | Embedded HTML5 Web Dashboard connected to Hugging Face AI Inference API.  |

---

## 🛠️ Technology Stack

- **Language/Framework:** Python 3.9, Flask, Flask-CORS
- **Containerization:** Docker Desktop / Engine
- **Orchestration:** Kubernetes (kubectl), Docker Desktop K8s Node
- **CI/CD Pipeline:** GitHub Actions
- **AI Model Integration:** Hugging Face Serverless Inference API (DistilBERT SST-2)
- **Frontend UI:** HTML5, CSS3, JavaScript (Fetch API)

---

## 📁 Repository Structure

```text
cloud-ai-project/
│
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD Pipeline definition
├── app.py                      # Flask Microservice & Embedded Web UI
├── Dockerfile                  # Container build instructions
├── deployment.yaml             # Kubernetes Deployment & Service configurations
├── requirements.txt            # Python environment dependencies
└── README.md                   # Project documentation
```

---

## 🚀 Quick Start & Deployment Guide

### Prerequisites

- [Docker Desktop](https://www.docker.com/) with Kubernetes enabled.
- [Python 3.9+](https://www.python.org/)
- [Git](https://git-scm.com/)

---

### 1. Local Container Execution (Docker)

To build and run the application locally using Docker:

```bash
# Clone the repository
git clone https://github.com/Lonelylongroads/cloud-ai-project.git
cd cloud-ai-project

# Build the Docker image
docker build -t cloud-ai-app:latest .

# Run the container
docker run -d -p 5000:5000 --name cloud-ai-direct cloud-ai-app:latest
```

Open your browser and navigate to `http://localhost:5000` to access the dashboard.

---

### 2. Kubernetes Cluster Orchestration

To deploy the application to a local Kubernetes cluster with load balancing:

```bash
# Create Kubernetes Secret for Hugging Face API
kubectl create secret generic ai-secret --from-literal=HF_TOKEN=your_huggingface_token

# Apply Deployment and Service configurations
kubectl apply -f deployment.yaml

# Verify running Pods and Services
kubectl get pods
kubectl get services

# Expose service locally (Port Forwarding)
kubectl port-forward service/cloud-ai-service 5000:80
```

---

### 3. Automated CI/CD Pipeline

The repository includes a GitHub Actions pipeline (`.github/workflows/deploy.yml`). On every `git push` to the `main` branch, the pipeline automatically:

1. Checks out the code.
2. Sets up the Python environment.
3. Installs dependencies from `requirements.txt`.
4. Builds the Docker container image to verify application integrity.

---

## 📊 Sample API Usage

### Endpoints

- `GET /`: Renders the Web Dashboard interface.
- `POST /analyze`: Performs sentiment classification on incoming JSON text payload.

#### Request Example:

```bash
curl -X POST http://localhost:5000/analyze \
     -H "Content-Type: application/json" \
     -d '{"text": "This cloud computing project is awesome!"}'
```

#### Response Example:

```json
[
  [
    {
      "label": "POSITIVE",
      "score": 0.9852
    }
  ]
]
```

---

## 👤 Author

- **Student Name:** Sakshi Indrajeet Kamble
- **Department:** Computer Science and Engineering
- **GitHub:** [@Lonelylongroads](https://github.com/Lonelylongroads)
