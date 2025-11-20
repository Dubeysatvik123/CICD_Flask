pipeline {
    agent any

    parameters {
        gitParameter(
            name: 'BRANCH_NAME',
            type: 'PT_BRANCH',
            defaultValue: 'main',
            branchFilter: '.*',
            selectedValue: 'DEFAULT',
            sortMode: 'ASCENDING',
            description: 'Select Git branch to build'
        )
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out branch: ${params.BRANCH_NAME}"
                checkout([$class: 'GitSCM',
                          branches: [[name: "*/${params.BRANCH_NAME}"]],
                          userRemoteConfigs: [[url: 'https://github.com/Dubeysatvik123/CICD_Flask.git']]])
            }
        }

        stage('Install Requirements') {
            steps {
                sh '''
                  python3 -m pip install --upgrade pip
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
                  def imageTag = "cicd_flask_app:${params.BRANCH_NAME}"
                  sh "docker build -t ${imageTag} ."
                  echo "Docker image built: ${imageTag}"
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline completed for branch ${params.BRANCH_NAME}"
        }
    }
}
