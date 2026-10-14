pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'krushna987/library-management-platform'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv .venv-ci'
                sh '.venv-ci/bin/pip install --no-cache-dir -r requirements.txt'
            }
        }

        stage('Code Quality') {
            steps {
                sh '.venv-ci/bin/flake8 app database tests run.py'
            }
        }

        stage('Run Tests') {
            steps {
                sh '.venv-ci/bin/pytest -q'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} -t ${DOCKER_IMAGE}:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_TOKEN')]) {
                    sh '''
                        echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}
                        docker push ${DOCKER_IMAGE}:latest
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl set image deployment/smart-library \
                      library-app=${DOCKER_IMAGE}:${BUILD_NUMBER}
                    kubectl rollout status deployment/smart-library --timeout=180s
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh 'kubectl get deployments,pods,services'
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the failed stage logs.'
        }
    }
}
