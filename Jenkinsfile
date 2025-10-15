pipeline {
    agent any

    environment {
        DOCKERHUB = credentials('dockerhub')
        GITHUB_CREDS = credentials('github')
        DOCKER_USER = "${DOCKERHUB_USR}"
        DOCKER_PASS = "${DOCKERHUB_PSW}"
        BACKEND_IMAGE = "siddhant1178/fusionpact-backend"
        FRONTEND_IMAGE = "siddhant1178/fusionpact-frontend"
    }

    options { timestamps() }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', credentialsId: 'github',
                    url: 'https://github.com/siddhant0205/fusionpact-devops-challenge.git'
            }
        }

        stage('Build and Test') {
            steps {
                dir('backend') {
                    sh '''
                    pip install -r requirements.txt
                    pytest --maxfail=1 --disable-warnings -q
                    '''
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                parallel (
                    "Backend": {
                        dir('backend') {
                            sh 'docker build -t $BACKEND_IMAGE:latest .'
                        }
                    },
                    "Frontend": {
                        dir('frontend') {
                            sh 'docker build -t $FRONTEND_IMAGE:latest .'
                        }
                    }
                )
            }
        }

        stage('Push to DockerHub') {
            steps {
                sh '''
                echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                docker push $BACKEND_IMAGE:latest
                docker push $FRONTEND_IMAGE:latest
                docker logout
                '''
            }
        }

        stage('Deploy Containers') {
            steps {
                sh '''
                docker compose down || true
                docker compose up -d
                docker ps
                '''
            }
        }
    }

    post {
        success { echo "✅ Deployment completed successfully." }
        failure { echo "❌ Deployment failed." }
    }
}
