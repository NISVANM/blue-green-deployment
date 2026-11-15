pipeline { agent any

environment {
    DOCKER = "/Users/niswa/.docker/bin/docker"
    KUBECTL = "/Applications/Docker.app/Contents/Resources/bin/kubectl"
    DOCKER_HELPER_PATH = "/Applications/Docker.app/Contents/Resources/bin:/Users/niswa/.docker/bin:/usr/bin:/bin:/usr/sbin:/sbin"

    IMAGE_NAME = "bluegreen-app:v1"
    DEPLOYMENT_NAME = "green-deployment"
    SERVICE_NAME = "bluegreen-service"
    APP_URL = "http://localhost:30081"
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

                export PATH="$DOCKER_HELPER_PATH"

                "$DOCKER" --version
                "$DOCKER" info

                which docker-credential-desktop

                echo "Docker is ready."
            '''
        }
    }

    stage('Build Docker Image') {
        steps {
            sh '''
                export PATH="$DOCKER_HELPER_PATH"

                echo "Building Docker image..."

                "$DOCKER" build -t "$IMAGE_NAME" .

                echo "Docker image built successfully."
            '''
        }
    }

    stage('Verify Kubernetes') {
        steps {
            sh '''
                export PATH="$DOCKER_HELPER_PATH"

                echo "Checking kubectl..."

                "$KUBECTL" version --client

                echo "Checking Kubernetes cluster..."

                "$KUBECTL" cluster-info

                "$KUBECTL" get nodes
            '''
        }
    }

    stage('Deploy Green') {
        steps {
            sh '''
                export PATH="$DOCKER_HELPER_PATH"

                echo "Deploying Green environment..."

                "$KUBECTL" apply -f k8s/green-deployment.yaml

                "$KUBECTL" rollout restart deployment/green-deployment

                "$KUBECTL" rollout status deployment/green-deployment --timeout=180s

                echo "Green environment deployed successfully."
            '''
        }
    }

    stage('Switch Traffic to Green') {
        steps {
            sh '''
                export PATH="$DOCKER_HELPER_PATH"

                echo "Switching traffic to Green..."

                "$KUBECTL" patch service "$SERVICE_NAME" \
                -p '{"spec":{"selector":{"app":"bluegreen-app","version":"green"}}}'

                echo "Traffic switched to Green."
            '''
        }
    }

    stage('Verify Deployment') {
        steps {
            sh '''
                export PATH="$DOCKER_HELPER_PATH"

                echo "Checking deployments..."

                "$KUBECTL" get deployments

                echo "Checking pods..."

                "$KUBECTL" get pods -o wide

                echo "Checking service..."

                "$KUBECTL" get service "$SERVICE_NAME"

                echo "Checking active service selector..."

                "$KUBECTL" get service "$SERVICE_NAME" -o jsonpath='{.spec.selector}'

                echo ""

                echo "Checking application health..."

                for i in $(seq 1 15); do
                    if curl -fsS "$APP_URL/health"; then
                        echo ""
                        echo "Application is healthy."
                        exit 0
                    fi

                    echo "Waiting for application..."
                    sleep 5
                done

                echo "Application health check failed."

                exit 1
            '''
        }
    }
}

post {
    success {
        echo '''
        SUCCESS: Blue-Green deployment completed!

        Active Environment: GREEN
        Application URL: http://localhost:30081
        '''
    }

    failure {
        echo 'FAILED: Check Jenkins console output for errors.'
    }

    always {
        echo 'Pipeline execution finished.'
    }
}


}