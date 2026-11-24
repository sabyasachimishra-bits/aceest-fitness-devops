# ACEest Fitness & Gym DevOps Project

## Overview

ACEest Fitness & Gym is a Flask-based fitness management application developed as part of the BITS Pilani **Introduction to DevOps** coursework.

The project demonstrates the progressive implementation of modern DevOps practices across two assignments.

### Assignment 1

Assignment 1 established the Continuous Integration foundation using:

- Flask application development
- Git and GitHub version control
- Pytest unit testing
- Ruff static linting
- Docker containerization
- GitHub Actions CI pipeline
- Jenkins build pipeline
- GitHub Webhook-based Jenkins triggering

### Assignment 2

Assignment 2 extends the same application into an end-to-end CI/CD implementation using:

- Automated Pytest execution and test coverage
- SonarQube static code analysis
- SonarQube Quality Gate integration
- Multi-stage Docker builds
- Docker Hub image versioning and registry
- Kubernetes deployment using Minikube
- Rolling updates and rollback
- Blue-Green deployment
- Canary releases
- Shadow deployment
- A/B testing
- Jenkins-driven build, quality validation, image publishing and deployment

---

# Application Features

ACEest Fitness & Gym provides the following functionality:

- Fat Loss fitness program
- Muscle Gain fitness program
- Beginner fitness program
- Client registration
- Calorie requirement calculation
- SQLite-based persistence
- REST API endpoints
- Health-check endpoint
- Application version endpoint
- Deployment metadata for progressive deployment demonstrations

---

# Application Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | ACEest Fitness web interface |
| GET | `/health` | Application health check |
| GET | `/version` | Application version and deployment metadata |
| GET | `/api/programs` | Retrieve available fitness programs |
| POST | `/api/calories` | Calculate calorie requirements |
| POST | `/clients` | Register a client |
| GET | `/api/clients` | Retrieve registered clients |

The `/version` endpoint is particularly useful for Kubernetes deployment validation.

Example:

```json
{
  "application": "ACEest Fitness and Gym",
  "version": "v2.0.0",
  "deployment_color": "blue",
  "release_track": "stable"
}
```

The values are controlled through environment variables:

```text
APP_VERSION
DEPLOYMENT_COLOR
RELEASE_TRACK
```

This enables different Kubernetes deployments to identify themselves as stable, canary, blue, green, or another release version.

---

# Technology Stack

| Area | Technology |
|---|---|
| Application | Python / Flask |
| Database | SQLite |
| Version Control | Git |
| Source Repository | GitHub |
| Testing | Pytest |
| Coverage | pytest-cov |
| Linting | Ruff |
| Code Quality | SonarQube |
| CI/CD | Jenkins |
| Additional CI | GitHub Actions |
| Containerization | Docker |
| Container Registry | Docker Hub |
| Container Orchestration | Kubernetes |
| Local Kubernetes | Minikube |
| Webhook Connectivity | ngrok |

---

# Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── main.yml
│
├── jenkins/
│   ├── Dockerfile
│   └── plugins.txt
│
├── k8s/
│   ├── base/
│   ├── rolling/
│   ├── blue-green/
│   ├── canary/
│   ├── shadow/
│   └── ab-testing/
│
├── templates/
│   └── index.html
│
├── tests/
│   └── test_app.py
│
├── app.py
├── Dockerfile
├── docker-compose.yml
├── Jenkinsfile
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
├── sonar-project.properties
└── README.md
```

---

# Assignment 1: CI Foundation

## Git and GitHub

Git is used to track:

- Application development
- Unit tests
- Bug fixes
- Docker configuration
- Jenkins pipeline changes
- CI configuration
- Infrastructure changes

The repository follows meaningful commit conventions such as:

```text
feat: add deployment version metadata
test: add application endpoint tests
build: add multi-stage Docker image
ci: configure Jenkins pipeline
quality: configure SonarQube analysis
deploy: add Kubernetes manifests
docs: update project documentation
```

Feature branches are used to isolate development work before integration with the main branch.

---

# Python Environment

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

---

# Running the Application Locally

Start the Flask application:

```bash
python app.py
```

The application is available at:

```text
http://localhost:5000
```

Health check:

```bash
curl http://localhost:5000/health
```

Version information:

```bash
curl http://localhost:5000/version
```

---

# Unit Testing

Pytest is used for automated unit and API testing.

Run:

```bash
python -m pytest -v
```

Generate test coverage:

```bash
python -m pytest \
  --cov=app \
  --cov-report=term-missing
```

Generate reports for Jenkins and SonarQube:

```bash
python -m pytest \
  -v \
  --junitxml=test-results.xml \
  --cov=app \
  --cov-report=term-missing \
  --cov-report=xml:coverage.xml
```

Generated reports:

```text
test-results.xml
coverage.xml
```

`test-results.xml` is consumed by Jenkins for test reporting.

`coverage.xml` is consumed by SonarQube for coverage analysis.

---

# Code Linting

Ruff is used for Python code-quality validation.

Run:

```bash
python -m ruff check app.py tests
```

Linting is also performed automatically within the Jenkins pipeline.

---

# Docker Containerization

The project uses a multi-stage Dockerfile.

Two principal stages are provided:

```text
test
runtime
```

## Test Image

Build:

```bash
docker build \
  --target test \
  -t aceest-fitness:test \
  .
```

Run Pytest inside Docker:

```bash
docker run \
  --rm \
  aceest-fitness:test \
  python -m pytest -v
```

This validates that the application tests also execute correctly inside an isolated container environment.

## Runtime Image

Build:

```bash
docker build \
  --target runtime \
  -t aceest-fitness:latest \
  .
```

Run:

```bash
docker run \
  -d \
  --name aceest-fitness \
  -p 5000:5000 \
  aceest-fitness:latest
```

Test:

```bash
curl http://localhost:5000/health
```

## Docker Design

The runtime image provides:

- Python slim base image
- Runtime-only dependencies
- Non-root application user
- Gunicorn application server
- Docker health check
- Flask application templates
- Reduced final image contents

Development and testing packages are kept in the test stage instead of the final runtime image.

---

# GitHub Actions

GitHub Actions provides automated CI validation for repository changes.

The workflow is located at:

```text
.github/workflows/main.yml
```

The workflow validates operations such as:

```text
GitHub Push / Pull Request
          |
          v
      Checkout
          |
          v
   Source Validation
          |
          v
        Ruff
          |
          v
       Pytest
          |
          v
    Docker Build
```

This provides rapid feedback whenever source code changes are pushed to GitHub.

---

# Jenkins CI/CD Pipeline

Jenkins is used as the primary build automation platform.

The pipeline definition is version controlled in:

```text
Jenkinsfile
```

The pipeline is configured using:

```text
Pipeline script from SCM
```

This allows Jenkins to retrieve both the source code and pipeline definition directly from GitHub.

The Assignment 2 Jenkins pipeline performs:

```text
GitHub Push
      |
      v
Jenkins Webhook Trigger
      |
      v
Checkout
      |
      v
Source Validation
      |
      v
Dependency Installation
      |
      v
Ruff Linting
      |
      v
Pytest + Coverage
      |
      v
SonarQube Analysis
      |
      v
Docker Test Image
      |
      v
Pytest Inside Docker
      |
      v
Runtime Docker Image
      |
      v
Container Smoke Test
```

The pipeline publishes:

```text
JUnit test results
coverage.xml
test-results.xml
```

as Jenkins build artifacts.

---

# GitHub Webhook Integration

GitHub Webhooks are used to trigger Jenkins automatically.

For the lab environment, Jenkins is exposed through an ngrok HTTPS tunnel.

The workflow is:

```text
git push
   |
   v
GitHub Repository
   |
   v
GitHub Webhook
   |
   v
ngrok
   |
   v
Jenkins
   |
   v
Pipeline Execution
```

The Jenkins job enables:

```text
GitHub hook trigger for GITScm polling
```

This eliminates the requirement to start Jenkins builds manually after every push.

---

# Assignment 2: SonarQube Code Quality

SonarQube is integrated into Assignment 2 for static code analysis and quality validation.

Configuration is stored in:

```text
sonar-project.properties
```

The project key is:

```text
aceest-fitness
```

The scanner analyzes application source and uses:

```text
coverage.xml
```

to import Python test coverage.

The Jenkins pipeline executes SonarQube analysis after tests and coverage generation.

The expected SonarQube project dashboard provides information about:

- Quality Gate status
- Reliability issues
- Security findings
- Maintainability issues
- Code coverage
- Duplicated code
- Lines of code

The SonarQube project can be inspected from:

```text
Projects
→ ACEest Fitness
→ Overview
```

Analysis processing can be verified at:

```text
ACEest Fitness
→ Project Settings
→ Background Tasks
```

---

# SonarQube Quality Gate

The intended CI/CD flow treats code quality as a deployment gate:

```text
Code Change
    |
    v
Pytest
    |
    v
Coverage
    |
    v
SonarQube Analysis
    |
    v
Quality Gate
    |
    +---- FAIL → Pipeline stopped
    |
    +---- PASS
             |
             v
        Container Build
             |
             v
         Deployment
```

This ensures code that fails configured quality criteria does not proceed into the deployment workflow.

---

# Docker Hub Container Registry

Assignment 2 introduces Docker Hub as the central image repository.

Images use versioned tags rather than relying only on `latest`.

Example:

```text
<dockerhub-user>/aceest-fitness:v2.0.0
<dockerhub-user>/aceest-fitness:v2.1.0
<dockerhub-user>/aceest-fitness:build-10
<dockerhub-user>/aceest-fitness:latest
```

Versioned container images provide:

- Build traceability
- Release identification
- Kubernetes deployment control
- Rollback capability

Docker Hub credentials are stored securely as Jenkins credentials and are not included in source control.

---

# Kubernetes and Minikube

Assignment
