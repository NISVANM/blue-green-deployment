
pipeline {
    agent any

    environment {
        DOCKER = '/Users/niswa/.docker/bin/docker'
        IMAGE = 'bluegreen-app:v1'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Test Application') {
            steps {
                sh '''
                    PYTHONPATH=. .venv/bin/pytest -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    ${DOCKER} build -t ${IMAGE} .
                '''
            }
        }

        stage('Deploy Green') {
            steps {
                sh '''
                    kubectl apply -f k8s/green-deployment.yaml
                    kubectl rollout status deployment/green-deployment --timeout=120s
                '''
            }
        }

        stage('Switch Traffic to Green') {
            steps {
                sh '''
                    kubectl patch service bluegreen-service \
                    -p '{"spec":{"selector":{"app":"bluegreen-app","version":"green"}}}'
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    kubectl get deployments
                    kubectl get pods
                    kubectl get svc
                '''
            }
        }
    }

    post {
        success {
            echo 'Blue-Green deployment completed successfully!'
        }
        failure {
            echo 'Deployment failed. Check Jenkins console output.'
        }
    }
}
