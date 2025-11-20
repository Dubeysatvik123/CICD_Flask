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
                    // In multibranch pipelines, checkout scm is already done automatically
                    // This stage is mainly for logging branch information
                    echo "Workspace: ${env.WORKSPACE}"
                }
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                echo "Setting up Python virtual environment..."
                sh '''
                    # Detect Python command
                    if command -v python3 &> /dev/null; then
                        PYTHON_CMD=python3
                    elif command -v python &> /dev/null; then
                        PYTHON_CMD=python
                    else
                        echo "ERROR: Python not found!"
                        exit 1
                    fi
                    
                    echo "Using Python: $PYTHON_CMD"
                    $PYTHON_CMD --version
                    
                    # Create virtual environment (venv module is built-in to Python 3.3+)
                    # On some systems, python3-venv package may need to be installed separately
                    echo "Creating virtual environment..."
                    if ! $PYTHON_CMD -m venv venv; then
                        echo "ERROR: Failed to create virtual environment."
                        echo "The venv module may not be available. On Ubuntu/Debian, install with:"
                        echo "  sudo apt-get install python3-venv"
                        echo "Or ensure the Jenkins agent has python3-venv installed."
                        exit 1
                    fi
                    
                    # Activate virtual environment
                    echo "Activating virtual environment..."
                    source venv/bin/activate
                    
                    # Verify pip is available in venv
                    echo "pip version in virtual environment:"
                    pip --version
                    
                    # Upgrade pip
                    echo "Upgrading pip..."
                    pip install --upgrade pip
                    
                    echo "✅ Virtual environment setup complete"
                '''
            }
        }

        stage('Install Requirements') {
            steps {
                echo "Installing Python dependencies..."
                sh '''
                    # Activate virtual environment
                    source venv/bin/activate
                    
                    # Install requirements
                    echo "Installing requirements from requirements.txt..."
                    pip install -r requirements.txt
                    
                    echo "✅ Dependencies installed successfully"
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running unit tests..."
                sh '''
                    # Activate virtual environment
                    source venv/bin/activate
                    
                    # Install pytest if not already installed (should be in requirements.txt, but just in case)
                    pip install pytest
                    
                    # Run tests
                    pytest -v test_project1.py
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
                    # Activate virtual environment
                    source venv/bin/activate
                    
                    # Run app with timeout (if available)
                    if command -v timeout &> /dev/null; then
                        timeout 15 python project1.py || echo "App start skipped"
                    else
                        python project1.py &
                        sleep 15
                        pkill -f project1.py || echo "App process ended"
                    fi
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
