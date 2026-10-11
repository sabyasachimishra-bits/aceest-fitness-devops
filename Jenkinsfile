pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        APP_IMAGE = "aceest-fitness"
        CONTAINER_NAME = "aceest-fitness-${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Source Validation') {
            steps {
                sh '''
                python3 -m compileall app.py tests
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                python3 -m pip install --break-system-packages -r requirements-dev.txt
                python3 -m ruff check .
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                python3 -m pytest
                '''
            }
        }

        stage('Docker Image Assembly') {
            steps {
                sh '''
                docker build \
                  -t ${APP_IMAGE}:${BUILD_NUMBER} \
                  -t ${APP_IMAGE}:latest \
                  .
                '''
            }
        }

        stage('Container Smoke Test') {
            steps {
                sh '''
                docker rm -f ${CONTAINER_NAME} >/dev/null 2>&1 || true

                docker run -d \
                  --name ${CONTAINER_NAME} \
                  -p 5000:5000 \
                  ${APP_IMAGE}:${BUILD_NUMBER}

                sleep 15

                curl --fail http://localhost:5000/health

                docker logs ${CONTAINER_NAME}

                docker stop ${CONTAINER_NAME}
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f ${CONTAINER_NAME} >/dev/null 2>&1 || true'
        }

        success {
            echo 'ACEest Jenkins BUILD completed successfully.'
        }

        failure {
            echo 'ACEest Jenkins BUILD failed.'
        }
    }
}
