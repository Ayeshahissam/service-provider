pipeline {
    agent any

    environment {
        PROJECT_NAME = 'jenkins-service-app'
        COMPOSE_FILE = 'docker-compose-jenkins.yml'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/Ayeshahissam/service-provider.git'
            }
        }

        stage('Build and Run Containers') {
            steps {
                script {
                    sh "docker-compose -p $PROJECT_NAME -f $COMPOSE_FILE down || true"
                    sh "docker-compose -p $PROJECT_NAME -f $COMPOSE_FILE build"
                    sh "docker-compose -p $PROJECT_NAME -f $COMPOSE_FILE up -d"
                }
            }
        }
    }

    post {
        always {
            echo 'Build completed!'
        }
    }
}
