pipeline {
    agent any

    environment {
        DOCKERHUB = credentials('dockerhub')    // Jenkins credential ID for DockerHub
        DOCKER_USER = "${DOCKERHUB_USR}"
        DOCKER_PASS = "${DOCKERHUB_PSW}"
        DOCKER_NAMESPACE = "siddhant1178"
        FRONTEND_IMAGE = "${DOCKER_NAMESPACE}/fusionpact-frontend"
        BACKEND_IMAGE = "${DOCKER_NAMESPACE}/fusionpact-backend"
    }

    // Options for timestamps and colored logs (AnsiColor optional)
    options {
        timestamps()
        // Uncomment the next line ONLY if you installed the AnsiColor plugin
        // ansiColor('xterm')
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "📦 Cloning repository from GitHub..."
                checkout scm
            }
        }

        stage('Build Backend Image') {
            steps {
                dir('backend') {
                    sh '''
                    echo "🚧 Building backend Docker image..."
                    docker build -t $BACKEND_IMAGE:latest .
                    '''
                }
            }
        }

        stage('Build Frontend Image') {
            steps {
                dir('frontend') {
                    sh '''
                    echo "🚧 Building frontend Docker image..."
                    docker build -t $FRONTEND_IMAGE:latest .
                    '''
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh '''
                echo "📤 Pushing Docker images to DockerHub..."
                echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                docker push $BACKEND_IMAGE:latest
                docker push $FRONTEND_IMAGE:latest
                docker logout
                '''
            }
        }

        stage('Deploy on EC2') {
            steps {
                sh '''
                echo "🚀 Deploying application on EC2..."
                docker compose down || true
                docker compose pull || true
                docker compose up -d
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Deployment completed successfully!"
        }
        failure {
            echo "❌ Deployment failed! Check logs for errors."
        }
    }
}
