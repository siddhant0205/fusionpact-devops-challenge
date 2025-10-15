pipeline {
    agent any

    environment {
        DOCKERHUB = credentials('dockerhub')      // Jenkins credential ID for DockerHub
        DOCKER_USER = "${DOCKERHUB_USR}"
        DOCKER_PASS = "${DOCKERHUB_PSW}"
        GITHUB_CREDS = credentials('github')      // Jenkins credential ID for GitHub PAT
    }

    options {
        timestamps()
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "📦 Checking out repository..."
                git branch: 'main',
                    url: 'https://github.com/siddhant0205/fusionpact-devops-challenge.git',
                    credentialsId: 'github'
            }
        }

        stage('Build and Test') {
            steps {
                dir('backend') {
                    echo "🔧 Setting up Python Virtual Environment..."
                    sh '''
                        sudo apt update -y
                        sudo apt install -y python3 python3-pip python3-venv
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    echo "🐳 Building Backend Docker Image..."
                    dir('backend') {
                        sh "docker build -t ${DOCKER_USER}/fusionpact-backend:latest ."
                    }

                    echo "🌐 Building Frontend Docker Image..."
                    dir('frontend') {
                        sh "docker build -t ${DOCKER_USER}/fusionpact-frontend:latest ."
                    }
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    echo "🚀 Pushing Docker images to DockerHub..."
                    sh """
                        echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin
                        docker push ${DOCKER_USER}/fusionpact-backend:latest
                        docker push ${DOCKER_USER}/fusionpact-frontend:latest
                        docker logout
                    """
                }
            }
        }

        stage('Deploy Containers') {
            steps {
                script {
                    echo "📦 Deploying containers using Docker Compose..."
                    sh """
                        sudo apt install -y docker-compose-plugin || true
                        docker compose down || true
                        docker compose up -d
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful! Both containers are live."
        }
        failure {
            echo "❌ Deployment failed. Check logs for details."
        }
    }
}
