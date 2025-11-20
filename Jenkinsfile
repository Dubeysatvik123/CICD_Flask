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

        stage('Install Requirements') {
            steps {
                echo "Installing Python dependencies..."
                sh '''
                    # Ensure user bin is in PATH (in case pip was installed with --user in a previous build)
                    export PATH="$HOME/.local/bin:$PATH"
                    
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
                    
                    # Check if pip is available
                    if ! $PYTHON_CMD -m pip --version &> /dev/null; then
                        echo "pip not found. Attempting to install pip..."
                        
                        # Method 1: Try ensurepip (built-in to Python 3.4+)
                        if $PYTHON_CMD -m ensurepip --version &> /dev/null; then
                            echo "Installing pip using ensurepip..."
                            $PYTHON_CMD -m ensurepip --upgrade --default-pip || echo "ensurepip failed, trying alternative..."
                        fi
                        
                        # Method 2: Try using get-pip.py if ensurepip failed
                        if ! $PYTHON_CMD -m pip --version &> /dev/null; then
                            echo "Trying get-pip.py..."
                            if command -v curl &> /dev/null; then
                                curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py
                                # Try with --user first to avoid permission issues
                                $PYTHON_CMD get-pip.py --user || $PYTHON_CMD get-pip.py || echo "get-pip.py failed"
                                rm -f get-pip.py
                                # Add user local bin to PATH if --user was used
                                export PATH="$HOME/.local/bin:$PATH"
                            elif command -v wget &> /dev/null; then
                                wget -q https://bootstrap.pypa.io/get-pip.py -O get-pip.py
                                $PYTHON_CMD get-pip.py --user || $PYTHON_CMD get-pip.py || echo "get-pip.py failed"
                                rm -f get-pip.py
                                # Add user local bin to PATH if --user was used
                                export PATH="$HOME/.local/bin:$PATH"
                            fi
                        fi
                        
                        # Method 3: Try system package manager (if available with sudo)
                        if ! $PYTHON_CMD -m pip --version &> /dev/null; then
                            echo "Trying system package manager..."
                            if command -v apt-get &> /dev/null && command -v sudo &> /dev/null; then
                                sudo apt-get update && sudo apt-get install -y python3-pip || echo "apt-get install failed"
                            elif command -v yum &> /dev/null && command -v sudo &> /dev/null; then
                                sudo yum install -y python3-pip || echo "yum install failed"
                            fi
                        fi
                        
                        # Final check
                        if ! $PYTHON_CMD -m pip --version &> /dev/null; then
                            echo "ERROR: Failed to install pip. Please install pip manually."
                            exit 1
                        fi
                    fi
                    
                    # Verify pip is available
                    echo "pip is available:"
                    $PYTHON_CMD -m pip --version
                    
                    # Ensure user bin is in PATH (in case pip was installed with --user)
                    export PATH="$HOME/.local/bin:$PATH"
                    
                    # Upgrade pip (try with --user if regular install fails)
                    echo "Upgrading pip..."
                    $PYTHON_CMD -m pip install --upgrade pip || $PYTHON_CMD -m pip install --upgrade --user pip
                    
                    # Install requirements (try with --user if regular install fails)
                    echo "Installing requirements from requirements.txt..."
                    $PYTHON_CMD -m pip install -r requirements.txt || $PYTHON_CMD -m pip install --user -r requirements.txt
                    
                    echo "✅ Dependencies installed successfully"
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running unit tests..."
                sh '''
                    # Ensure user bin is in PATH
                    export PATH="$HOME/.local/bin:$PATH"
                    
                    # Detect Python command
                    if command -v python3 &> /dev/null; then
                        PYTHON_CMD=python3
                    elif command -v python &> /dev/null; then
                        PYTHON_CMD=python
                    else
                        echo "ERROR: Python not found!"
                        exit 1
                    fi
                    
                    # Install pytest if not already installed
                    $PYTHON_CMD -m pip install pytest || $PYTHON_CMD -m pip install --user pytest
                    
                    # Run tests
                    $PYTHON_CMD -m pytest -v test_project1.py
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
