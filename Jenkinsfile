pipeline {
    agent any

    environment {
        DOCKERHUB = credentials('dockerhub')
        DOCKER_USER = "${DOCKERHUB_USR}"
        DOCKER_PASS = "${DOCKERHUB_PSW}"
        GITHUB_CREDS = credentials('github')
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
                    dir('backend') {
                        sh "docker build -t ${DOCKER_USER}/fusionpact-backend:latest ."
                    }
                    dir('frontend') {
                        sh "docker build -t ${DOCKER_USER}/fusionpact-frontend:latest ."
                    }
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
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
                    sh """
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
