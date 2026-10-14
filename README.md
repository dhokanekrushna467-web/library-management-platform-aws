# 📚 Enterprise Smart Library Management Platform

An enterprise-oriented library management application built with Python and Flask. The project demonstrates software development and DevOps practices, including automated testing, code quality checks, Docker containerization, and Jenkins CI/CD pipeline integration.

## 🚀 Project Overview

The Enterprise Smart Library Management Platform is designed to simplify library operations through a web-based application. It provides an API for library-related operations and demonstrates how an application can be tested, packaged, and prepared for deployment using DevOps tools.

## ✨ Key Features

- **REST API:** Flask-based API for library management operations.
- **Book Management:** Supports library book-related operations.
- **User Management:** Includes library user information.
- **Health Check:** Provides an API endpoint to check application status.
- **Automated Testing:** Uses Pytest to validate application functionality.
- **Code Quality:** Uses Flake8 for Python code analysis.
- **Docker Support:** Packages the application into a Docker image.
- **CI/CD Integration:** Includes a Jenkins declarative pipeline for automating build and testing stages.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Application development |
| Flask 3.0 | Web framework and API development |
| Pytest | Automated testing |
| Flake8 | Code quality checks |
| Gunicorn | WSGI application server |
| Git and GitHub | Version control and source code management |
| Jenkins | CI/CD pipeline automation |
| Docker | Application containerization |
| AWS EC2 | Cloud hosting environment |

## 🏗️ Project Structure

```text
library-management-platform-aws/
├── app/
│   ├── __init__.py
│   ├── routes/
│   ├── services/
│   ├── models/
│   └── templates/
├── database/
│   └── db.py
├── tests/
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
├── run.py
└── README.md
```

*Note: The structure above describes the intended project layout. Adjust it if your repository differs.*

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.11
- Git
- pip
- Docker (optional, for containerization)

### 1. Clone the Repository

```bash
git clone https://github.com/dhokanekrushna467-web/library-management-platform-aws.git
cd library-management-platform-aws
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it on Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python run.py
```

The application should start on the configured host and port.

## 🧪 Testing

Run the automated test suite with:

```bash
pytest -q
```

Run the code quality checks with:

```bash
flake8 app database tests run.py
```

## 🐳 Docker

Build the Docker image:

```bash
docker build -t library-management-platform:latest .
```

Run the container:

```bash
docker run -d --name library-app -p 5000:5000 library-management-platform:latest
```

Check running containers:

```bash
docker ps
```

## 🔄 Jenkins CI/CD Pipeline

The repository includes a `Jenkinsfile` defining a declarative pipeline with the following stages:

1. **Checkout:** Retrieves the project source code.
2. **Install Dependencies:** Creates a Python virtual environment and installs required packages.
3. **Code Quality:** Runs Flake8.
4. **Run Tests:** Executes the Pytest test suite.
5. **Build Docker Image:** Builds the Docker image.

The pipeline is designed to automate validation and image building. Successful execution should be confirmed in Jenkins before describing the pipeline as fully operational.

## ☁️ AWS Deployment

AWS EC2 provides the cloud environment for setting up and running the application and its DevOps tools.

The application can be deployed to an EC2 instance after configuring its runtime dependencies, network access, and application server.

## 🎯 Project Objectives

- Apply DevOps principles to a Python web application.
- Automate testing and code quality checks.
- Demonstrate Docker-based containerization.
- Integrate source control with Jenkins.
- Explore cloud-based application hosting using AWS EC2.

## 🔮 Future Enhancements

- Integrate a persistent database.
- Add authentication and role-based access control.
- Automate application deployment through Jenkins.
- Add monitoring and centralized logging.
- Deploy the application using Kubernetes.
- Implement HTTPS and production security configurations.

## 👨‍💻 Author

**Krushna Dhokane**

GitHub: [dhokanekrushna467-web](https://github.com/dhokanekrushna467-web)

## 📄 License

This project is intended for educational and demonstration purposes. Add a license file if you intend to distribute the project under a specific open-source license.

## CI/CD Automation Test

Testing automatic Jenkins pipeline trigger from GitHub.

Automatic Jenkins Trigger Test - October 14, 2026
