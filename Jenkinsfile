pipeline {
    agent any

    environment {
        // Safe branch naming for Docker tag
        SANITIZED_BRANCH = "${env.BRANCH_NAME ?: 'unknown'}"
        IMAGE_TAG = "${env.SANITIZED_BRANCH}-${env.BUILD_NUMBER}"
        IMAGE_NAME = "cicd_flask_app:${env.IMAGE_TAG}"
    }

    stages {

        stage('Checkout Info') {
            steps {
                script {
                    echo """
                    ===== CHECKOUT DETAILS =====
                    Branch       : ${env.BRANCH_NAME}
                    Build Number : ${env.BUILD_NUMBER}
                    Workspace    : ${env.WORKSPACE}
                    =============================
                    """
                }
            }
        }


        stage('Install Requirements') {
            steps {
                echo "Installing Python dependencies..."
                sh '''
                     
                    python3-pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running unit tests..."
                sh '''
                     
                   python3-pip install pytest
                    pytest -v test_project1.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Sanitize branch name
                    def sanitized = (env.BRANCH_NAME ?: 'unknown')
                                    .replaceAll(/[^a-zA-Z0-9._-]/, '-')
                                    .toLowerCase()

                    env.IMAGE_TAG = "${sanitized}-${env.BUILD_NUMBER}"
                    env.IMAGE_NAME = "cicd_flask_app:${env.IMAGE_TAG}"

                    echo "Building Docker image: ${env.IMAGE_NAME}"

                    sh """
                        docker build -t ${env.IMAGE_NAME} .
                        docker tag ${env.IMAGE_NAME} cicd_flask_app:${sanitized}-latest
                    """

                    echo "Docker build completed → ${env.IMAGE_NAME}"
                }
            }
        }

        stage('Run Flask/Gradio App (main/master only)') {
            when {
                anyOf {
                    branch 'main'
                    branch 'master'
                }
            }
            steps {
                echo "Starting application (main/master)..."
                sh '''
                     
                    cd CICD_Flask
                    python project1.py
                '''
            }
        }
    }

    post {
        always {
            echo """
            =========================================
                 PIPELINE SUMMARY
            -----------------------------------------
            Branch       : ${env.BRANCH_NAME}
            Build Number : ${env.BUILD_NUMBER}
            Docker Image : ${env.IMAGE_NAME ?: 'N/A'}
            =========================================
            """
        }
        success {
            echo "✅ Pipeline succeeded for branch: ${env.BRANCH_NAME}"
        }
        failure {
            echo "❌ Pipeline FAILED for branch: ${env.BRANCH_NAME}"
        }
        unstable {
            echo "⚠️ Pipeline is UNSTABLE for branch: ${env.BRANCH_NAME}"
        }
    }
}
