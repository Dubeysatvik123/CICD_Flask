pipeline {
    agent any

    parameters {
        string(
            name: 'BRANCH_TO_BUILD',
            defaultValue: 'main',
            description: 'Enter the Git branch to build'
        )
    }

    environment {
        REPO_URL = 'https://github.com/Dubeysatvik123/CICD_Flask.git'
        IMAGE_NAME = "cicd_flask_app:${params.BRANCH_TO_BUILD}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Checking out branch: ${params.BRANCH_TO_BUILD}"
                git branch: "${params.BRANCH_TO_BUILD}", url: "${env.REPO_URL}"
            }
        }

        stage('Install Requirements') {
            steps {
                echo "Installing Python dependencies..."
                sh '''
                    python3 -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running unit tests..."
                sh '''
                    pip install pytest
                    pytest -q
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${env.IMAGE_NAME}"
                sh "docker build -t ${env.IMAGE_NAME} ."
            }
        }

        stage('Optional: Run Flask/Gradio App') {
            when {
                branch 'main'
            }
            steps {
                echo "Starting app (only on main branch)"
                sh '''
                    python project1.py &
                    sleep 10
                    echo "App started"
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline finished for branch ${params.BRANCH_TO_BUILD}"
        }
    }
}
