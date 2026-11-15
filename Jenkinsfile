
pipeline {
    agent any

    environment {
        DOCKER = '/Users/niswa/.docker/bin/docker'

        KUBECTL = '/Applications/Docker.app/Contents/Resources/bin/kubectl'

        PATH = "/Applications/Docker.app/Contents/Resources/bin:/Users/niswa/.docker/bin:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

        IMAGE_NAME = 'bluegreen-app'
        IMAGE_TAG = 'v1'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt
                    .venv/bin/pip install pytest httpx
                '''
            }
        }

        stage('Test Application') {
            steps {
                sh '''
                    PYTHONPATH=. .venv/bin/python -m pytest -v
                '''
            }
        }

        stage('Check Docker') {
            steps {
                sh '''
                    echo "Checking Docker..."

                    $DOCKER --version
                    $DOCKER info

                    echo "Checking Docker credential helper..."

                    which docker-credential-desktop

                    echo "Docker is ready."
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Building Docker image..."

                    $DOCKER build -t ${IMAGE_NAME}:${IMAGE_TAG} .

                    echo "Docker image built successfully."
                '''
            }
        }

        stage('Verify Kubernetes') {
            steps {
                sh '''
                    echo "Checking kubectl..."

                    $KUBECTL version --client

                    echo "Checking Kubernetes cluster..."

                    $KUBECTL cluster-info

                    echo "Checking Kubernetes nodes..."

                    $KUBECTL get nodes
                '''
            }
        }

        stage('Deploy Green') {
            steps {
                sh '''
                    echo "Deploying Green environment..."

                    $KUBECTL apply -f k8s/green-deployment.yaml

                    $KUBECTL rollout status deployment/green-deployment
                '''
            }
        }

        stage('Switch Traffic to Green') {
            steps {
                sh '''
                    echo "Switching traffic to Green..."

                    $KUBECTL patch service bluegreen-service \
                    -p '{"spec":{"selector":{"app":"bluegreen-app","version":"green"}}}'

                    echo "Traffic successfully switched to Green."
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    echo "Checking deployments..."

                    $KUBECTL get deployments

                    echo "Checking pods..."

                    $KUBECTL get pods -o wide

                    echo "Checking service..."

                    $KUBECTL get service bluegreen-service

                    echo "Checking active service selector..."

                    $KUBECTL get service bluegreen-service \
                    -o jsonpath='{.spec.selector}'

                    echo ""

                    echo "Blue-Green deployment completed."
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Blue-Green deployment completed successfully!'
        }

        failure {
            echo 'FAILED: Check Jenkins console output for errors.'
        }

        always {
            echo 'Pipeline execution finished.'
        }
    }
}
