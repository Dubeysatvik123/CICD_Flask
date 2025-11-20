pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh '''
                    python3 -m venv env
                    source env/bin/activate
                    pip install -r requirements.txt
                    pip install pytest
                    pytest test_project1.py
                '''
            }
        }
        
        stage('Docker Build') {
            steps {
                script {
                    def tag = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
                    sh "docker build -t cicd_flask_app:${tag} .
                        docker run -p 7860:7860 cicd_flask_app:${tag}"
                }
            }
        }
    }
}
