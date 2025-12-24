pipeline {
    agent any

    tools {
        sonarQubeScanner 'sonar-scanner'
    }


    environment {
        IMAGE_NAME = "saifudheenpv/notes-app"
        IMAGE_TAG = "1.0"
        DOCKER_CREDS = credentials('dockerhub-creds')
        SONAR_TOKEN = credentials('sonar-token')
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Saifudheenpv/DevOps-Ultimate-EndToEnd-Pipeline.git'
            }
        }

        stage('SonarQube Scan') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh '''
                    sonar-scanner \
                      -Dsonar.projectKey=notes-app \
                      -Dsonar.sources=app/backend \
                      -Dsonar.host.url=http://10.155.115.101:9000/ \
                      -Dsonar.login=$SONAR_TOKEN
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG ./app/backend'
            }
        }

        stage('Docker Login') {
            steps {
                sh 'echo $DOCKER_CREDS_PSW | docker login -u $DOCKER_CREDS_USR --password-stdin'
            }
        }

        stage('Push Image') {
            steps {
                sh 'docker push $IMAGE_NAME:$IMAGE_TAG'
            }
        }
    }
}
