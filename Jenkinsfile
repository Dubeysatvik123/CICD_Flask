pipeline {
    agent any
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'staging', 'production'],
            description: 'Select deployment environment'
        )
        extendedChoice(
            name: 'DEPLOYMENT_TARGETS',
            type: 'PT_CHECKBOX',
            value: 'Docker,AWS_ECS,AWS_EC2,AWS_ElasticBeanstalk',
            description: 'Select deployment targets',
            multiSelectDelimiter: ','
        )
        string(
            name: 'DOCKER_TAG',
            defaultValue: "${BUILD_NUMBER}",
            description: 'Docker image tag version'
        )
        booleanParam(
            name: 'RUN_TESTS',
            defaultValue: true,
            description: 'Execute pytest test suite'
        )
        booleanParam(
            name: 'PUSH_TO_ECR',
            defaultValue: false,
            description: 'Push Docker image to AWS ECR'
        )
        string(
            name: 'BUILD_METADATA',
            defaultValue: 'automated-build',
            description: 'Build metadata (internal use)'
        )
    }
    
    options {
        ansiColor('xterm')
        timestamps()
        buildDiscarder(logRotator(
            numToKeepStr: '30',
            daysToKeepStr: '90',
            artifactNumToKeepStr: '10'
        ))
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
    }
    
    environment {
        APP_NAME = 'flask-cicd-app'
        PYTHON_VERSION = '3.9'
        DOCKER_REGISTRY = "${env.AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com"
        IMAGE_NAME = "${APP_NAME}"
        IMAGE_TAG = "${params.DOCKER_TAG}"
        SLACK_CHANNEL = '#flask-deployments'
        AWS_DEFAULT_REGION = 'us-east-1'
        FLASK_ENV = "${params.ENVIRONMENT}"
    }
    
    triggers {
        // GitHub webhook trigger
        githubPush()
        // Scheduled build
        cron(env.ENVIRONMENT == 'production' ? 'H 2 * * 1-5' : '')
    }
    
    stages {
        stage('🚀 Initialize Pipeline') {
            steps {
                script {
                    echo "=" * 80
                    echo "Flask CI/CD Pipeline Started"
                    echo "=" * 80
                    echo "Build Number: ${BUILD_NUMBER}"
                    echo "Environment: ${params.ENVIRONMENT}"
                    echo "Docker Tag: ${params.DOCKER_TAG}"
                    echo "Deployment Targets: ${params.DEPLOYMENT_TARGETS}"
                    echo "=" * 80
                    
                    // Set build display name
                    currentBuild.displayName = "#${BUILD_NUMBER}-${params.ENVIRONMENT}"
                    currentBuild.description = "Flask App - ${params.ENVIRONMENT} deployment"
                }
            }
        }
        
        stage('📦 Checkout Code') {
            steps {
                script {
                    // Git plugin with advanced options
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: '*/main']],
                        doGenerateSubmoduleConfigurations: false,
                        extensions: [
                            [$class: 'CleanBeforeCheckout'],
                            [$class: 'CloneOption', depth: 1, noTags: false, reference: '', shallow: true],
                            [$class: 'CheckoutOption', timeout: 10]
                        ],
                        userRemoteConfigs: [[
                            url: 'git@github.com:Dubeysatvik123/CICD_Flask.git',
                            credentialsId: 'github-ssh-credentials'
                        ]]
                    ])
                    
                    // Get git commit info
                    env.GIT_COMMIT_SHORT = sh(
                        script: "git log -n 1 --pretty=format:'%h'",
                        returnStdout: true
                    ).trim()
                    
                    env.GIT_AUTHOR = sh(
                        script: "git log -n 1 --pretty=format:'%an'",
                        returnStdout: true
                    ).trim()
                    
                    env.GIT_COMMIT_MSG = sh(
                        script: "git log -n 1 --pretty=format:'%s'",
                        returnStdout: true
                    ).trim()
                    
                    echo "Commit: ${env.GIT_COMMIT_SHORT}"
                    echo "Author: ${env.GIT_AUTHOR}"
                    echo "Message: ${env.GIT_COMMIT_MSG}"
                }
            }
        }
        
        stage('🐍 Setup Python Environment') {
            steps {
                script {
                    // Using PyEnv pipeline plugin
                    withPythonEnv("python${PYTHON_VERSION}") {
                        sh '''
                            echo "Setting up Python environment..."
                            python --version
                            pip --version
                            
                            echo "Creating virtual environment..."
                            python -m venv venv || true
                            . venv/bin/activate
                            
                            echo "Upgrading pip..."
                            pip install --upgrade pip setuptools wheel
                            
                            echo "Installing dependencies..."
                            pip install -r requirements.txt
                            
                            echo "Installed packages:"
                            pip list
                        '''
                    }
                }
            }
        }
        
        stage('🔍 Code Quality & Security Checks') {
            parallel {
                stage('Linting') {
                    steps {
                        withPythonEnv("python${PYTHON_VERSION}") {
                            sh '''
                                . venv/bin/activate
                                echo "Running flake8 linter..."
                                pip install flake8
                                flake8 project1.py test_project1.py --max-line-length=120 --statistics || true
                            '''
                        }
                    }
                }
                
                stage('Security Scan') {
                    steps {
                        withPythonEnv("python${PYTHON_VERSION}") {
                            sh '''
                                . venv/bin/activate
                                echo "Running security checks..."
                                pip install bandit safety
                                bandit -r . -f json -o bandit-report.json || true
                                safety check --json || true
                            '''
                        }
                    }
                }
                
                stage('Dependency Check') {
                    steps {
                        withPythonEnv("python${PYTHON_VERSION}") {
                            sh '''
                                . venv/bin/activate
                                echo "Checking for outdated packages..."
                                pip list --outdated
                            '''
                        }
                    }
                }
            }
        }
        
        stage('🧪 Run Tests') {
            when {
                expression { params.RUN_TESTS == true }
            }
            steps {
                withPythonEnv("python${PYTHON_VERSION}") {
                    sh '''
                        . venv/bin/activate
                        echo "Installing test dependencies..."
                        pip install pytest pytest-cov pytest-html pytest-xdist
                        
                        echo "Running pytest with coverage..."
                        pytest test_project1.py \
                            --verbose \
                            --junit-xml=test-results/pytest-report.xml \
                            --html=test-results/pytest-report.html \
                            --self-contained-html \
                            --cov=. \
                            --cov-report=html:coverage-report \
                            --cov-report=xml:coverage.xml \
                            --cov-report=term-missing
                        
                        echo "Test execution completed!"
                    '''
                }
            }
            post {
                always {
                    // JUnit plugin for test results
                    junit(
                        testResults: 'test-results/*.xml',
                        allowEmptyResults: true,
                        healthScaleFactor: 1.0
                    )
                    
                    // Publish HTML reports
                    publishHTML([
                        reportDir: 'test-results',
                        reportFiles: 'pytest-report.html',
                        reportName: 'Pytest Report',
                        keepAll: true,
                        alwaysLinkToLastBuild: true,
                        allowMissing: false
                    ])
                    
                    publishHTML([
                        reportDir: 'coverage-report',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report',
                        keepAll: true,
                        alwaysLinkToLastBuild: true,
                        allowMissing: false
                    ])
                }
            }
        }
        
        stage('🐳 Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    
                    // Docker workflow plugin
                    def customImage = docker.build(
                        "${IMAGE_NAME}:${IMAGE_TAG}",
                        "--build-arg ENVIRONMENT=${params.ENVIRONMENT} " +
                        "--build-arg BUILD_DATE=\$(date -u +'%Y-%m-%dT%H:%M:%SZ') " +
                        "--build-arg VCS_REF=${env.GIT_COMMIT_SHORT} " +
                        "--build-arg BUILD_NUMBER=${BUILD_NUMBER} " +
                        "--label 'maintainer=DevOps Team' " +
                        "--label 'app=${APP_NAME}' " +
                        "--label 'environment=${params.ENVIRONMENT}' " +
                        "."
                    )
                    
                    // Tag with multiple tags
                    customImage.tag("${IMAGE_TAG}")
                    customImage.tag("${params.ENVIRONMENT}")
                    if (params.ENVIRONMENT == 'production') {
                        customImage.tag('latest')
                    }
                    
                    echo "Docker image built successfully: ${IMAGE_NAME}:${IMAGE_TAG}"
                    
                    // Run quick container test
                    sh """
                        echo "Testing Docker container..."
                        docker run --rm -d -p 5001:5000 --name test-flask-app ${IMAGE_NAME}:${IMAGE_TAG}
                        sleep 5
                        curl -f http://localhost:5001/ || exit 1
                        docker stop test-flask-app
                        echo "Container test passed!"
                    """
                }
            }
        }
        
        stage('🔐 AWS Authentication & ECR Push') {
            when {
                expression { params.PUSH_TO_ECR == true }
            }
            steps {
                script {
                    withAWS(credentials: 'aws-credentials', region: env.AWS_DEFAULT_REGION) {
                        // AWS ECR login
                        sh '''
                            echo "Logging into AWS ECR..."
                            aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | \
                                docker login --username AWS --password-stdin ${DOCKER_REGISTRY}
                        '''
                        
                        // Push to ECR
                        docker.withRegistry("https://${DOCKER_REGISTRY}", 'ecr:us-east-1:aws-credentials') {
                            def image = docker.image("${IMAGE_NAME}:${IMAGE_TAG}")
                            
                            echo "Pushing image to ECR..."
                            image.push("${IMAGE_TAG}")
                            image.push("${params.ENVIRONMENT}")
                            
                            if (params.ENVIRONMENT == 'production') {
                                image.push('latest')
                            }
                            
                            echo "Image pushed to ECR: ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
                        }
                    }
                }
            }
        }
        
        stage('🚢 Deploy to AWS') {
            when {
                expression { params.DEPLOYMENT_TARGETS.contains('AWS') }
            }
            parallel {
                stage('Deploy to ECS') {
                    when {
                        expression { params.DEPLOYMENT_TARGETS.contains('AWS_ECS') }
                    }
                    steps {
                        withAWS(credentials: 'aws-credentials', region: env.AWS_DEFAULT_REGION) {
                            script {
                                sh """
                                    echo "Deploying to ECS..."
                                    aws ecs update-service \
                                        --cluster flask-app-cluster \
                                        --service flask-app-service-${params.ENVIRONMENT} \
                                        --force-new-deployment \
                                        --region ${AWS_DEFAULT_REGION}
                                    
                                    echo "Waiting for service to stabilize..."
                                    aws ecs wait services-stable \
                                        --cluster flask-app-cluster \
                                        --services flask-app-service-${params.ENVIRONMENT} \
                                        --region ${AWS_DEFAULT_REGION}
                                    
                                    echo "ECS deployment completed!"
                                """
                            }
                        }
                    }
                }
                
                stage('Deploy to EC2') {
                    when {
                        expression { params.DEPLOYMENT_TARGETS.contains('AWS_EC2') }
                    }
                    steps {
                        withAWS(credentials: 'aws-credentials', region: env.AWS_DEFAULT_REGION) {
                            script {
                                sh """
                                    echo "Deploying to EC2 instances..."
                                    
                                    # Get EC2 instance IDs with specific tag
                                    INSTANCE_IDS=\$(aws ec2 describe-instances \
                                        --filters "Name=tag:Environment,Values=${params.ENVIRONMENT}" \
                                                  "Name=tag:App,Values=flask-cicd" \
                                                  "Name=instance-state-name,Values=running" \
                                        --query 'Reservations[*].Instances[*].InstanceId' \
                                        --output text)
                                    
                                    echo "Target instances: \$INSTANCE_IDS"
                                    
                                    # Deploy using SSM Run Command
                                    for INSTANCE_ID in \$INSTANCE_IDS; do
                                        aws ssm send-command \
                                            --instance-ids \$INSTANCE_ID \
                                            --document-name "AWS-RunShellScript" \
                                            --parameters commands='[
                                                "aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${DOCKER_REGISTRY}",
                                                "docker pull ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}",
                                                "docker stop flask-app || true",
                                                "docker rm flask-app || true",
                                                "docker run -d -p 5000:5000 --name flask-app --restart unless-stopped ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
                                            ]'
                                    done
                                    
                                    echo "EC2 deployment initiated!"
                                """
                            }
                        }
                    }
                }
                
                stage('Deploy to Elastic Beanstalk') {
                    when {
                        expression { params.DEPLOYMENT_TARGETS.contains('AWS_ElasticBeanstalk') }
                    }
                    steps {
                        withAWS(credentials: 'aws-credentials', region: env.AWS_DEFAULT_REGION) {
                            script {
                                sh """
                                    echo "Deploying to Elastic Beanstalk..."
                                    
                                    # Create Dockerrun.aws.json
                                    cat > Dockerrun.aws.json <<EOF
{
  "AWSEBDockerrunVersion": "1",
  "Image": {
    "Name": "${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}",
    "Update": "true"
  },
  "Ports": [
    {
      "ContainerPort": 5000,
      "HostPort": 80
    }
  ]
}
EOF
                                    
                                    # Create application version
                                    zip -r flask-app-${BUILD_NUMBER}.zip Dockerrun.aws.json
                                    
                                    aws s3 cp flask-app-${BUILD_NUMBER}.zip \
                                        s3://my-elasticbeanstalk-bucket/flask-app-${BUILD_NUMBER}.zip
                                    
                                    aws elasticbeanstalk create-application-version \
                                        --application-name flask-cicd-app \
                                        --version-label v${BUILD_NUMBER} \
                                        --source-bundle S3Bucket="my-elasticbeanstalk-bucket",S3Key="flask-app-${BUILD_NUMBER}.zip"
                                    
                                    # Deploy to environment
                                    aws elasticbeanstalk update-environment \
                                        --application-name flask-cicd-app \
                                        --environment-name flask-${params.ENVIRONMENT} \
                                        --version-label v${BUILD_NUMBER}
                                    
                                    echo "Elastic Beanstalk deployment completed!"
                                """
                            }
                        }
                    }
                }
            }
        }
        
        stage('🔍 Post-Deployment Verification') {
            when {
                expression { params.DEPLOYMENT_TARGETS != '' }
            }
            steps {
                script {
                    echo "Running post-deployment health checks..."
                    
                    // HTTP Request plugin for health checks
                    httpRequest(
                        url: "http://your-app-url-${params.ENVIRONMENT}.com/health",
                        httpMode: 'GET',
                        acceptType: 'APPLICATION_JSON',
                        timeout: 30,
                        validResponseCodes: '200'
                    )
                    
                    echo "Health check passed!"
                }
            }
        }
        
        stage('📊 Archive Artifacts') {
            steps {
                script {
                    // File operations plugin
                    fileOperations([
                        folderCreateOperation(folderPath: 'artifacts'),
                        fileCopyOperation(
                            includes: 'Dockerfile,requirements.txt,*.py',
                            targetLocation: 'artifacts/'
                        )
                    ])
                    
                    // Archive artifacts
                    archiveArtifacts(
                        artifacts: 'artifacts/**,test-results/**,*.xml,*.json',
                        allowEmptyArchive: true,
                        fingerprint: true,
                        onlyIfSuccessful: false
                    )
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "Pipeline execution completed!"
                
                // Workspace cleanup
                cleanWs(
                    deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true,
                    patterns: [
                        [pattern: 'venv/**', type: 'INCLUDE'],
                        [pattern: '.pytest_cache/**', type: 'INCLUDE'],
                        [pattern: '__pycache__/**', type: 'INCLUDE']
                    ]
                )
            }
        }
        
        success {
            script {
                echo "✅ Pipeline completed successfully!"
                
                // Slack notification
                slackSend(
                    channel: env.SLACK_CHANNEL,
                    color: 'good',
                    message: """
                        ✅ *SUCCESS* - Flask CI/CD Pipeline
                        *Job:* ${env.JOB_NAME}
                        *Build:* ${env.BUILD_NUMBER}
                        *Environment:* ${params.ENVIRONMENT}
                        *Commit:* ${env.GIT_COMMIT_SHORT} by ${env.GIT_AUTHOR}
                        *Message:* ${env.GIT_COMMIT_MSG}
                        *Duration:* ${currentBuild.durationString}
                        *URL:* ${env.BUILD_URL}
                    """.stripIndent()
                )
            }
        }
        
        failure {
            script {
                echo "❌ Pipeline failed!"
                
                // Slack notification
                slackSend(
                    channel: env.SLACK_CHANNEL,
                    color: 'danger',
                    message: """
                        ❌ *FAILED* - Flask CI/CD Pipeline
                        *Job:* ${env.JOB_NAME}
                        *Build:* ${env.BUILD_NUMBER}
                        *Environment:* ${params.ENVIRONMENT}
                        *Commit:* ${env.GIT_COMMIT_SHORT}
                        *Duration:* ${currentBuild.durationString}
                        *URL:* ${env.BUILD_URL}
                        *Action Required:* Please check the build logs
                    """.stripIndent()
                )
            }
        }
        
        unstable {
            script {
                echo "⚠️ Pipeline is unstable!"
                
                slackSend(
                    channel: env.SLACK_CHANNEL,
                    color: 'warning',
                    message: """
                        ⚠️ *UNSTABLE* - Flask CI/CD Pipeline
                        *Job:* ${env.JOB_NAME}
                        *Build:* ${env.BUILD_NUMBER}
                        *Environment:* ${params.ENVIRONMENT}
                        *URL:* ${env.BUILD_URL}
                    """.stripIndent()
                )
            }
        }
    }
}
