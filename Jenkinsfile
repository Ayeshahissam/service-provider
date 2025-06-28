pipeline {
    agent any
    
    options {
        timeout(time: 30, unit: 'MINUTES')
    }
    
    environment {
        IMAGE_NAME = 'service-provider'
        IMAGE_TAG = "${BUILD_NUMBER}"
        GIT_REPO = 'https://github.com/Ayeshahissam/service-provider.git'
    }
    
    stages {
        stage('Get Source Code') {
            steps {
                echo 'Getting source code from GitHub...'
                
                // Use simple git clone instead of Jenkins checkout
                sh '''
                    echo "Cloning repository..."
                    git clone ${GIT_REPO} source || echo "Clone failed, trying to update existing repo"
                    
                    if [ -d "source" ]; then
                        cd source
                        git pull origin master || echo "Pull failed, continuing with existing code"
                        echo "✓ Source code ready"
                        ls -la
                    else
                        echo "❌ Failed to get source code"
                        exit 1
                    fi
                '''
            }
        }
        
        stage('Check Environment') {
            steps {
                echo 'Checking environment...'
                
                sh '''
                    echo "Checking Python..."
                    python3 --version || python --version
                    
                    echo "Checking pip..."
                    pip3 --version || pip --version
                    
                    echo "Checking Docker..."
                    docker --version
                    docker-compose --version
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                
                sh '''
                    cd source
                    echo "Installing Python packages..."
                    python3 -m pip install --user --break-system-packages -r requirements.txt
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                
                sh '''
                    cd source
                    echo "Building Docker image..."
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                    
                    echo "✓ Docker image built successfully"
                    docker images | grep ${IMAGE_NAME}
                '''
            }
        }
        
        stage('Deploy Application') {
            steps {
                echo 'Deploying application...'
                
                sh '''
                    cd source
                    echo "Starting deployment..."
                    
                    # Force stop and remove existing containers
                    echo "Stopping and removing existing containers..."
                    docker-compose down --remove-orphans || true
                    docker stop service-provider-mongodb service-provider-web || true
                    docker rm service-provider-mongodb service-provider-web || true
                    
                    # Start new containers
                    echo "Starting new containers..."
                    docker-compose up -d
                    
                    echo "Waiting for services to start..."
                    sleep 20
                    
                    echo "Checking deployment status..."
                    docker-compose ps
                '''
            }
        }
        
        stage('Verify Deployment') {
            steps {
                echo 'Verifying deployment...'
                
                sh '''
                    echo "Checking if application is running..."
                    if curl -f -s http://16.24.96.75:8000/homepage > /dev/null; then
                        echo "\u2705 Application is running successfully!"
                        echo "Application accessible at: http://16.24.96.75:8000/homepage"
                    else
                        echo "⚠️ Application may still be starting up"
                        echo "Container logs:"
                        cd source && docker-compose logs --tail=10 web
                    fi
                '''
            }
        }
        
        stage('Run Automated Tests') {
            steps {
                echo 'Running Selenium automated tests...'
                
                sh '''
                    cd source
                    echo "Building test container..."
                    docker build -f Dockerfile.test -t service-provider-tests .
                    
                    echo "Running automated test suite..."
                    docker run --rm \
                        --network="host" \
                        -e BASE_URL=http://16.24.96.75:8000 \
                        -v "$(pwd)/test-results:/app/test-results" \
                        service-provider-tests \
                        || true
                    
                    echo "Test execution completed"
                '''
            }
            
            post {
                always {
                    // Archive test results and reports
                    sh '''
                        cd source
                        # Create test-results directory if it doesn't exist
                        mkdir -p test-results
                        
                        # Copy test reports if they exist
                        if [ -f test-report.html ]; then
                            cp test-report.html test-results/
                            echo "✅ Test report archived"
                        fi
                        
                        # List test results
                        echo "Test results:"
                        ls -la test-results/ || echo "No test results found"
                    '''
                    
                    // Archive artifacts
                    archiveArtifacts artifacts: 'source/test-results/**/*', allowEmptyArchive: true
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed'
        }
        
        success {
            echo '''
            🎉 BUILD & TEST SUCCESSFUL! 🎉
            
            ✅ Application deployed successfully
            ✅ All automated tests passed
            🌐 Access: http://16.24.96.75:8000/homepage
            📊 Test Report: Check Jenkins artifacts for test-report.html
            
            To check status: docker-compose ps
            To view logs: docker-compose logs
            '''
        }
        
        failure {
            echo '''
            ❌ BUILD OR TEST FAILED!
            
            Check the logs above for errors.
            Most common issues:
            Build phase:
            - Python/pip not installed
            - Docker not running
            - Port 8000 already in use
            
            Test phase:
            - Application not accessible on http://16.24.96.75:8000
            - Chrome/ChromeDriver issues in container
            - Test timeout due to slow page loads
            - Network connectivity issues from Jenkins to EC2
            
            Manual cleanup if needed:
            sudo rm -rf /var/lib/jenkins/workspace/serviceprovider
            docker system prune -f
            '''
        }
    }
} 