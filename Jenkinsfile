pipeline {
    agent any

    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch to build')
    }

    stages {
        stage('Checkout') {
            steps {
                sh """
                    git fetch origin
                    git checkout ${params.BRANCH}
                    git pull origin ${params.BRANCH}
                """
            }
        }
        stage('Build') {
            steps {
                sh '''
                    python3 -m venv env
                    . env/bin/activate
                    pip install -r requirements.txt
                    pip install pytest
                    pytest test_project1.py
                '''
            }
        }
        
        stage('Docker Build') {
            steps {
                script {
                    def tag = "${params.BRANCH}-${env.BUILD_NUMBER}"
                    sh """
                        docker build -t cicd_flask_app:${tag} -f Dockerfile .
                        docker run -d -p 7860:7860 --name cicd_flask_${BUILD_NUMBER} cicd_flask_app:${tag}
                    """
                }
            }
        }
    }
}
