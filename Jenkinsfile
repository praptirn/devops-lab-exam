pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                echo 'Repository cloned successfully'
            }
        }

        stage('Install Dependencies') {
            steps {

                echo 'Installing backend dependencies...'

                bat '''
                    cd backend
                    pip install -r requirements.txt
                '''

                echo 'Installing frontend dependencies...'

                bat '''
                    cd frontend
                    npm install
                '''
            }
        }

        stage('Build') {
            steps {

                echo 'Building frontend application...'

                bat '''
                    cd frontend
                    npm run build
                '''
            }
        }

        stage('Test') {
            steps {

                echo 'Running backend tests...'

                bat '''
                    cd backend
                    python -m unittest discover
                '''

                echo 'Running frontend tests...'

                bat '''
                    cd frontend
                    npm test
                '''
            }
        }

        stage('Deploy') {
            steps {

                echo 'Deploying application using Docker Compose...'

                bat '''
                    docker-compose up --build -d
                '''
            }
        }
    }

    post {

        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed.'
        }
    }
}
