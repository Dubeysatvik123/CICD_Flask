pipeline {
    agent {
        docker {
            image 'python:3.10'
            args '-u'
        }
    }

    options {
        skipDefaultCheckout(false)  // needed for multibranch
    }

    stages {

        stage('Install Dependencies') {
            steps {
                sh '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    pip install pytest
                    pytest -q
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def imgName = "gradio-app:${env.BRANCH_NAME}"
                    sh "docker build -t ${imgName} ."
                    echo "Docker image built: ${imgName}"
                }
            }
        }

        stage('Run App (Optional)') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                echo "Launching Gradio App..."
                python project1.py &
                sleep 10
                echo "App started"
                '''
            }
        }
    }

    post {
        always {
            echo "Build completed for branch: ${env.BRANCH_NAME}"
        }
    }
}
