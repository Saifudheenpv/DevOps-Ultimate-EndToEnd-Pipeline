pipeline {
    agent any

    environment {
        IMAGE_NAME = "saifudheenpv/notes-app"
        IMAGE_TAG = "1.0"
        DOCKER_CREDS = credentials('dockerhub-creds')
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Saifudheenpv/DevOps-Ultimate-EndToEnd-Pipeline.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG ./app/backend'
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    sh 'echo $DOCKER_CREDS_PSW | docker login -u $DOCKER_CREDS_USR --password-stdin'
                }
            }
        }

        stage('Push Image') {
            steps {
                script {
                    sh 'docker push $IMAGE_NAME:$IMAGE_TAG'
                }
            }
        }
    }
}
