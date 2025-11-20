pipeline {
    agent any

    environment {
        // Use BRANCH_NAME for multibranch pipelines - automatically set by Jenkins
        IMAGE_NAME = "cicd_flask_app:${env.BRANCH_NAME ?: 'unknown'}"
        // Sanitize branch name for Docker tag (remove special characters)
        DOCKER_TAG = "${env.BRANCH_NAME ?: 'unknown'}-${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "Building branch: ${env.BRANCH_NAME}"
                    echo "Build number: ${env.BUILD_NUMBER}"
                    // In multibranch pipelines, checkout scm automatically checks out the current branch
                    checkout scm
                }
            }
        }

        stage('Install Requirements') {
            steps {
                echo "Installing Python dependencies..."
                sh '''
                    python3 --version || python --version
                    python3 -m pip install --upgrade pip || python -m pip install --upgrade pip
                    pip3 install -r requirements.txt || pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running unit tests..."
                sh '''
                    pip3 install pytest || pip install pytest
                    pytest -v test_project1.py || pytest test_project1.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Sanitize branch name for Docker tag (Docker tags can't have certain characters)
                    def branchName = env.BRANCH_NAME ?: 'unknown'
                    def sanitizedBranch = branchName.replaceAll(/[^a-zA-Z0-9._-]/, '-').toLowerCase()
                    def dockerImage = "cicd_flask_app:${sanitizedBranch}-${env.BUILD_NUMBER}"
                    env.IMAGE_NAME = dockerImage
                    
                    echo "Building Docker image: ${dockerImage}"
                    sh """
                        docker --version || echo "Warning: Docker not available"
                        docker build -t ${dockerImage} .
                        docker tag ${dockerImage} cicd_flask_app:${sanitizedBranch}-latest
                        echo "Successfully built and tagged image: ${dockerImage}"
                    """
                }
            }
        }

        stage('Optional: Run Flask/Gradio App') {
            when {
                anyOf {
                    branch 'main'
                    branch 'master'
                }
            }
            steps {
                echo "Starting app (only on main/master branch)"
                sh '''
                    timeout 15 python3 project1.py || timeout 15 python project1.py || echo "App start skipped"
                '''
            }
        }
    }

    post {
        always {
            script {
                echo "========================================="
                echo "Pipeline Summary:"
                echo "Branch: ${env.BRANCH_NAME}"
                echo "Build Number: ${env.BUILD_NUMBER}"
                echo "Docker Image: ${env.IMAGE_NAME ?: 'N/A'}"
                echo "========================================="
            }
        }
        success {
            echo "✅ Pipeline succeeded for branch: ${env.BRANCH_NAME}"
        }
        failure {
            echo "❌ Pipeline failed for branch: ${env.BRANCH_NAME}"
            echo "Check the logs above for error details"
        }
        unstable {
            echo "⚠️ Pipeline is unstable for branch: ${env.BRANCH_NAME}"
        }
    }
}
