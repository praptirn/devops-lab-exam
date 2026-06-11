pipeline {
agent any

tools {
    jdk 'jdk-25'
}

environment {
    SCANNER_HOME = tool 'Sonar-scanner'
    PYTHON_HOME = 'D:\\Python312'
    PATH = "${PYTHON_HOME};${PYTHON_HOME}\\Scripts;${PATH}"
    DOCKERHUB_USERNAME = 'praptirn'
    BACKEND_IMAGE = "${DOCKERHUB_USERNAME}/taskflow-backend"
    FRONTEND_IMAGE = "${DOCKERHUB_USERNAME}/taskflow-frontend"
}

stages {

    stage('Checkout Code') {
        steps {
            git branch: 'main', url: 'https://github.com/praptirn/devops-lab-exam.git'
        }
    }

    stage('Git Version Check') {
        steps {
            bat 'git --version'
            bat 'git log -1 --oneline'
        }
    }

    stage('Install Dependencies') {
        steps {
            dir('backend') {
                bat 'python -m pip install -r requirements.txt'
            }

            dir('frontend') {
                bat 'npm install'
            }
        }
    }

    stage('Dependency Check') {
        steps {
            dir('frontend') {
                dependencyCheck additionalArguments: '--scan . --disableYarnAudit', odcInstallation: 'dp'
            }

            dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
        }
    }

    stage('Build') {
        steps {
            dir('frontend') {
                bat 'npm run build'
            }
        }
    }

    stage('Test') {
        steps {
            dir('backend') {
                bat 'python -m unittest discover'
            }

            dir('frontend') {
                bat 'npm test'
            }
        }
    }

    stage('Code Quality Check') {
        steps {
            script {
                withSonarQubeEnv('SonarQube-server') {

                    bat """
                    ${SCANNER_HOME}\\bin\\sonar-scanner ^
                    -Dsonar.projectKey=devops-lab-exam ^
                    -Dsonar.projectName=devops-lab-exam ^
                    -Dsonar.sources=backend,frontend/src ^
                    -Dsonar.exclusions=**/node_modules/**,**/__pycache__/**,**/dist/** ^
                    -Dsonar.python.coverage.reportPaths=backend/coverage.xml ^
                    -Dsonar.javascript.lcov.reportPaths=frontend/coverage/lcov.info ^
                    -Dsonar.sourceEncoding=UTF-8
                    """
                }
            }
        }
    }

    stage('Quality Gate') {
        steps {
            timeout(time: 10, unit: 'MINUTES') {
                waitForQualityGate abortPipeline: true
            }
        }
    }

    stage('Containerization') {
        steps {
            bat "docker build -t ${BACKEND_IMAGE}:${BUILD_NUMBER} -t ${BACKEND_IMAGE}:latest ./backend"
            bat "docker build -t ${FRONTEND_IMAGE}:${BUILD_NUMBER} -t ${FRONTEND_IMAGE}:latest ./frontend"
        }
    }

    stage('Host Image on Docker Hub') {
        steps {
            withCredentials([
                usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )
            ]) {
                bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'

                bat "docker push ${BACKEND_IMAGE}:${BUILD_NUMBER}"
                bat "docker push ${BACKEND_IMAGE}:latest"

                bat "docker push ${FRONTEND_IMAGE}:${BUILD_NUMBER}"
                bat "docker push ${FRONTEND_IMAGE}:latest"
            }
        }
    }

    stage('Deployment') {
        steps {
            bat '''
                docker-compose down --remove-orphans 2>nul
                for /f "tokens=1" %%i in ('docker ps -q --filter "publish=5000"') do docker stop %%i & docker rm %%i
                for /f "tokens=1" %%i in ('docker ps -q --filter "publish=5173"') do docker stop %%i & docker rm %%i
                exit /b 0
            '''
            bat 'docker-compose up --build -d'
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