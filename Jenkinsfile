pipeline {
    agent any

    environment {
        DOCKERHUB = credentials('dockerhub')
        DOCKER_USER = "${DOCKERHUB_USR}"
        DOCKER_PASS = "${DOCKERHUB_PSW}"
    }

    options {
        timestamps()
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', credentialsId: 'github',
                    url: 'https://github.com/siddhant0205/fusionpact-devops-challenge.git'
            }
        }

        stage('Build Backend Image') {
            steps {
                dir('backend') {
                    sh '''
                    echo "Building Backend Docker Image..."
                    docker build -t ${DOCKER_USER}/fusionpact-backend:latest .
                    '''
                }
            }
        }

        stage('Build Frontend Image') {
            steps {
                dir('frontend') {
                    sh '''
                    echo "Building Frontend Docker Image..."
                    docker build -t ${DOCKER_USER}/fusionpact-frontend:latest .
                    '''
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                sh '''
                echo "Pushing Docker Images to DockerHub..."
                echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                docker push ${DOCKER_USER}/fusionpact-backend:latest
                docker push ${DOCKER_USER}/fusionpact-frontend:latest
                docker logout
                '''
            }
        }

        stage('Deploy Containers on EC2') {
            steps {
                sh '''
                echo "Deploying containers on EC2..."
                docker compose down || true
                docker compose up -d
                docker ps
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline executed successfully! Visit http://<EC2-PUBLIC-IP>"
        }
        failure {
            echo "Pipeline failed! Check console output for errors."
        }
    }
}

