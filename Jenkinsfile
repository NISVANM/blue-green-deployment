pipeline { agent any

environment {
    DOCKER = '/Users/niswa/.docker/bin/docker'
    DOCKER_IMAGE = 'bluegreen-app'
    DOCKER_TAG = 'v1'
    K8S_DEPLOYMENT = 'bluegreen-app'
    K8S_SERVICE = 'bluegreen-service'
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

                ${DOCKER} --version

                ${DOCKER} info

                echo "Checking Docker credential helper..."

                export PATH="/Applications/Docker.app/Contents/Resources/bin:/Users/niswa/.docker/bin:$PATH"

                which docker-credential-desktop

                echo "Docker is ready."
            '''
        }
    }

    stage('Build Docker Image') {
        steps {
            sh '''
                export PATH="/Applications/Docker.app/Contents/Resources/bin:/Users/niswa/.docker/bin:$PATH"

                ${DOCKER} build \
                -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
            '''
        }
    }

    stage('Verify Kubernetes') {
        steps {
            sh '''
                kubectl cluster-info
                kubectl get nodes
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
                kubectl patch service ${K8S_SERVICE} \
                -p '{"spec":{"selector":{"app":"bluegreen-app","version":"green"}}}'
            '''
        }
    }

    stage('Verify Deployment') {
        steps {
            sh '''
                echo "Checking deployments..."

                kubectl get deployments

                echo "Checking pods..."

                kubectl get pods -o wide

                echo "Checking services..."

                kubectl get services

                echo "Checking service endpoints..."

                kubectl get endpoints ${K8S_SERVICE}

                echo "Blue-Green deployment completed successfully!"
            '''
        }
    }
}

post {
    success {
        echo 'SUCCESS: Blue-Green deployment completed!'
    }

    failure {
        echo 'FAILED: Check Jenkins console output for errors.'
    }

    always {
        echo 'Pipeline execution finished.'
    }
}


}