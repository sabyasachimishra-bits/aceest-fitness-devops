pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        APP_IMAGE = "aceest-fitness"
        CONTAINER_NAME = "aceest-jenkins-${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('Source Validation') {
            steps {
                sh '''
                docker run --rm \
                  -v "$WORKSPACE:/app" \
                  -w /app \
                  python:3.13-slim \
                  python -m compileall app.py tests
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                docker run --rm \
                  -v "$WORKSPACE:/app" \
                  -w /app \
                  python:3.13-slim \
                  sh -c "pip install --no-cache-dir -r requirements-dev.txt && python -m ruff check ."
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                docker run --rm \
                  -v "$WORKSPACE:/app" \
                  -w /app \
                  python:3.13-slim \
                  sh -c "pip install --no-cache-dir -r requirements-dev.txt && python -m pytest"
                '''
            }
        }

        stage('Docker Image Assembly') {
            steps {
                sh '''
                docker build \
                  --tag ${APP_IMAGE}:${BUILD_NUMBER} \
                  --tag ${APP_IMAGE}:latest \
                  .
                '''
            }
        }

        stage('Container Smoke Test') {
            steps {
                sh '''
                docker rm -f ${CONTAINER_NAME} >/dev/null 2>&1 || true

                docker run --rm -d \
                  --name ${CONTAINER_NAME} \
                  ${APP_IMAGE}:${BUILD_NUMBER}

                sleep 10

                docker logs ${CONTAINER_NAME}

                docker rm -f ${CONTAINER_NAME} || true
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f ${CONTAINER_NAME} || true'
        }

        success {
            echo 'ACEest Jenkins BUILD completed successfully.'
        }

        failure {
            echo 'ACEest Jenkins BUILD failed.'
        }
    }
}
