pipeline {
    agent any

    environment {
        IMAGE_NAME = "saifudheenpv/notes-app"
        IMAGE_TAG  = "1.0"

        DOCKER_CREDS = credentials('dockerhub-creds')
        SONAR_TOKEN  = credentials('sonar-token')

        SONAR_HOST_URL = "http://10.155.115.101:9000"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Saifudheenpv/DevOps-Ultimate-EndToEnd-Pipeline.git'
            }
        }

        stage('SonarQube Scan (Docker)') {
            steps {
                sh '''
                docker run --rm \
                  -e SONAR_HOST_URL=${SONAR_HOST_URL} \
                  -v "$PWD:/usr/src" \
                  sonarsource/sonar-scanner-cli \
                  -Dsonar.projectKey=notes-app \
                  -Dsonar.sources=app/backend \
                  -Dsonar.host.url=${SONAR_HOST_URL} \
                  -Dsonar.login=${SONAR_TOKEN}
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build \
                  -t ${IMAGE_NAME}:${IMAGE_TAG} \
                  ./app/backend
                '''
            }
        }

        stage('Docker Login') {
            steps {
                sh '''
                echo $DOCKER_CREDS_PSW | docker login \
                  -u $DOCKER_CREDS_USR \
                  --password-stdin
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                docker push ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }
    }

    post {
        success {
            echo "✅ CI Pipeline completed successfully"
        }
        failure {
            echo "❌ CI Pipeline failed"
        }
    }
}
