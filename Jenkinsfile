pipeline {
    agent any

    options {
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
                sh 'docker build -t library-management-platform:latest .'
            }
        }
    }

    post {
        success {
            echo 'CI pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the stage logs.'
        }
    }
}
