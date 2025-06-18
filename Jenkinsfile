pipeline {
    agent any
    
    environment {
        // Docker registry and image configuration
        DOCKER_REGISTRY = 'docker.io'
        IMAGE_NAME = 'service-provider'
        IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKER_IMAGE = "${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
        DOCKER_LATEST = "${DOCKER_REGISTRY}/${IMAGE_NAME}:latest"
        
        // Application configuration
        APP_PORT = '8000'
        MONGO_PORT = '27017'
        
        // Git repository
        GIT_REPO = 'https://github.com/Ayeshahissam/service-provider.git'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Fetching source code from GitHub repository...'
                
                // Clean workspace first
                deleteDir()
                
                // Checkout with explicit configuration
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/master']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [
                        [$class: 'CleanBeforeCheckout'],
                        [$class: 'CloneOption', depth: 0, noTags: false, reference: '', shallow: false]
                    ],
                    submoduleCfg: [],
                    userRemoteConfigs: [[url: "${GIT_REPO}"]]
                ])
                
                echo 'Source code fetched successfully'
                sh '''
                    echo "=== Repository structure ==="
                    ls -la
                    echo "=== Templates directory ==="
                    ls -la templates/ || echo "Templates directory not found!"
                    echo "=== Static directory ==="
                    ls -la static/ || echo "Static directory not found!"
                    echo "=== Total file count ==="
                    find . -type f | wc -l
                '''
            }
        }
        
        stage('Environment Setup') {
            steps {
                echo 'Setting up build environment...'
                
                // Verify Python installation
                sh 'python3 --version || python --version'
                sh 'pip3 --version || pip --version'
                
                // Verify Docker installation
                sh 'docker --version'
                sh 'docker-compose --version'
                
                echo 'Environment setup completed'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                
                script {
                    try {
                        // Try pip3 first, fallback to pip
                        sh '''
                            if command -v pip3 >/dev/null 2>&1; then
                                pip3 install --user -r requirements.txt
                            else
                                pip install --user -r requirements.txt
                            fi
                        '''
                    } catch (Exception e) {
                        echo "Failed to install dependencies: ${e}"
                        error "Dependency installation failed"
                    }
                }
                
                echo 'Dependencies installed successfully'
            }
        }
        
        stage('Build Application') {
            steps {
                echo 'Building FastAPI application...'
                
                // Validate Python syntax
                sh '''
                    echo "Validating Python syntax..."
                    python3 -m py_compile main.py || python -m py_compile main.py
                    python3 -m py_compile db.py || python -m py_compile db.py
                '''
                
                // Check if required files exist
                sh '''
                    echo "Checking required files..."
                    test -f main.py && echo "✓ main.py found" || { echo "✗ main.py missing"; exit 1; }
                    test -f db.py && echo "✓ db.py found" || { echo "✗ db.py missing"; exit 1; }
                    test -f requirements.txt && echo "✓ requirements.txt found" || { echo "✗ requirements.txt missing"; exit 1; }
                    test -f Dockerfile && echo "✓ Dockerfile found" || { echo "✗ Dockerfile missing"; exit 1; }
                    test -f docker-compose.yml && echo "✓ docker-compose.yml found" || { echo "✗ docker-compose.yml missing"; exit 1; }
                    test -d templates && echo "✓ templates directory found" || { echo "✗ templates directory missing"; exit 1; }
                    test -d static && echo "✓ static directory found" || { echo "✗ static directory missing"; exit 1; }
                    
                    echo "Checking critical template files..."
                    test -f templates/homepage.html && echo "✓ homepage.html found" || { echo "✗ homepage.html missing"; exit 1; }
                    test -f templates/signup.html && echo "✓ signup.html found" || { echo "✗ signup.html missing"; exit 1; }
                    test -f templates/admin_dashboard.html && echo "✓ admin_dashboard.html found" || { echo "✗ admin_dashboard.html missing"; exit 1; }
                    
                    echo "Template files count: $(find templates/ -name "*.html" | wc -l)"
                    echo "Static files count: $(find static/ -type f | wc -l)"
                '''
                
                echo 'Application build completed successfully'
            }
        }
        
        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'
                
                script {
                    try {
                        // Build Docker image
                        sh """
                            docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                            docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                        """
                        
                        // Verify image was built
                        sh "docker images | grep ${IMAGE_NAME}"
                        
                    } catch (Exception e) {
                        echo "Docker build failed: ${e}"
                        error "Docker image build failed"
                    }
                }
                
                echo 'Docker image built successfully'
            }
        }
        
        stage('Docker Build Verification') {
            steps {
                echo 'Verifying Docker image contains all necessary files...'
                
                script {
                    try {
                        // Check if the built image contains all required files
                        sh """
                            echo "=== Verifying files in Docker image ==="
                            docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} ls -la /app/
                            
                            echo "=== Checking templates in Docker image ==="
                            docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} ls -la /app/templates/ || echo "Templates directory missing in image!"
                            
                            echo "=== Checking static files in Docker image ==="
                            docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} ls -la /app/static/ || echo "Static directory missing in image!"
                            
                            echo "=== Checking critical files ==="
                            docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} test -f /app/main.py && echo "✓ main.py in image"
                            docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} test -f /app/templates/homepage.html && echo "✓ homepage.html in image"
                            docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} test -f /app/templates/signup.html && echo "✓ signup.html in image"
                        """
                    } catch (Exception e) {
                        echo "Docker image verification failed: ${e}"
                        error "Docker image does not contain all required files"
                    }
                }
                
                echo 'Docker image verification completed'
            }
        }
        
        stage('Docker Compose Validation') {
            steps {
                echo 'Validating Docker Compose configuration...'
                
                // Validate docker-compose.yml syntax
                sh 'docker-compose config'
                
                echo 'Docker Compose validation completed'
            }
        }
        
        stage('Security Scan') {
            steps {
                echo 'Performing basic security checks...'
                
                // Check for sensitive files
                sh '''
                    echo "Checking for sensitive files..."
                    if find . -name "*.env" -o -name ".env*" -o -name "*.key" -o -name "*.pem"; then
                        echo "Warning: Found potential sensitive files"
                    else
                        echo "✓ No obvious sensitive files found"
                    fi
                '''
                
                // Check Dockerfile security
                sh '''
                    echo "Checking Dockerfile security..."
                    if grep -q "USER" Dockerfile; then
                        echo "✓ Non-root user found in Dockerfile"
                    else
                        echo "Warning: Consider adding non-root user to Dockerfile"
                    fi
                '''
                
                echo 'Security scan completed'
            }
        }
        
        stage('Prepare Deployment') {
            steps {
                echo 'Preparing deployment artifacts...'
                
                // Create deployment directory with all necessary files
                sh '''
                    mkdir -p deployment-artifacts
                    
                    # Copy core application files
                    cp docker-compose.yml deployment-artifacts/
                    cp Dockerfile deployment-artifacts/
                    cp requirements.txt deployment-artifacts/
                    cp main.py deployment-artifacts/
                    cp db.py deployment-artifacts/
                    
                    # Copy complete directories with their structure
                    cp -r templates/ deployment-artifacts/
                    cp -r static/ deployment-artifacts/
                    
                    # Copy any additional HTML files in root
                    cp *.html deployment-artifacts/ 2>/dev/null || echo "No additional HTML files in root"
                    
                    # Verify deployment artifacts
                    echo "=== Deployment artifacts structure ==="
                    find deployment-artifacts/ -type f | sort
                    echo "=== Template files in artifacts ==="
                    find deployment-artifacts/templates/ -name "*.html" | wc -l
                '''
                
                // Create deployment script
                sh '''
                    cat > deployment-artifacts/deploy.sh << EOF
#!/bin/bash
echo "Starting Service Provider Application Deployment..."

# Pull latest images
docker-compose pull

# Stop existing containers
docker-compose down

# Start services
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 30

# Check service health
if docker-compose ps | grep "Up"; then
    echo "✓ Deployment successful - Services are running"
    echo "✓ Application should be available at http://localhost:8000"
    echo "✓ MongoDB should be available at localhost:27017"
else
    echo "✗ Deployment failed - Services are not running properly"
    docker-compose logs
    exit 1
fi
EOF
                    chmod +x deployment-artifacts/deploy.sh
                '''
                
                echo 'Deployment artifacts prepared'
            }
        }
        
        stage('Archive Artifacts') {
            steps {
                echo 'Archiving build artifacts...'
                
                // Archive important files
                archiveArtifacts artifacts: 'deployment-artifacts/**/*', 
                               fingerprint: true,
                               allowEmptyArchive: false
                
                // Save Docker image (optional)
                sh """
                    docker save ${IMAGE_NAME}:${IMAGE_TAG} | gzip > deployment-artifacts/${IMAGE_NAME}-${IMAGE_TAG}.tar.gz
                """
                
                echo 'Artifacts archived successfully'
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline execution completed'
            
            // Clean up workspace
            sh '''
                echo "Cleaning up..."
                docker system prune -f --volumes || true
            '''
        }
        
        success {
            echo '''
            ╔══════════════════════════════════════════════════════════════╗
            ║                    🎉 BUILD SUCCESSFUL! 🎉                   ║
            ╠══════════════════════════════════════════════════════════════╣
            ║                                                              ║
            ║  ✅ Source code fetched from repository                      ║
            ║  ✅ Dependencies installed successfully                      ║
            ║  ✅ Application built and validated                          ║
            ║  ✅ Docker image created successfully                        ║
            ║  ✅ Security checks completed                                ║
            ║  ✅ Deployment artifacts ready                               ║
            ║                                                              ║
            ║  🚀 Ready for deployment!                                    ║
            ║                                                              ║
            ║  Next steps:                                                 ║
            ║  1. Use deployment-artifacts/deploy.sh to deploy            ║
            ║  2. Access application at http://localhost:8000              ║
            ║  3. MongoDB available at localhost:27017                    ║
            ║                                                              ║
            ╚══════════════════════════════════════════════════════════════╝
            '''
        }
        
        failure {
            echo '''
            ╔══════════════════════════════════════════════════════════════╗
            ║                     ❌ BUILD FAILED! ❌                      ║
            ╠══════════════════════════════════════════════════════════════╣
            ║                                                              ║
            ║  Please check the build logs for detailed error information ║
            ║  Common issues:                                              ║
            ║  - Missing dependencies                                      ║
            ║  - Docker daemon not running                                 ║
            ║  - Syntax errors in Python files                            ║
            ║  - Network connectivity issues                               ║
            ║                                                              ║
            ╚══════════════════════════════════════════════════════════════╝
            '''
            
            // Capture logs for debugging
            sh '''
                echo "Capturing system information for debugging..."
                docker --version || echo "Docker not available"
                python3 --version || python --version || echo "Python not available"
                pip3 --version || pip --version || echo "Pip not available"
            '''
        }
        
        unstable {
            echo 'Build completed with warnings - please review the logs'
        }
        
        cleanup {
            echo 'Performing final cleanup...'
        }
    }
} 