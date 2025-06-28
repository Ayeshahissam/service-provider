#!/bin/bash

# Local Xperts - Test Execution Script
# This script runs the automated test suite against the deployed application

echo "🚀 Local Xperts - Automated Test Suite"
echo "======================================"
echo "Application URL: http://3.137.209.211:8000/homepage"
echo ""

# Check if test dependencies are installed
if ! command -v pytest &> /dev/null; then
    echo "⚠️ pytest not found. Installing test dependencies..."
    pip install -r test-requirements.txt
fi

# Set environment variables
export BASE_URL=http://3.137.209.211:8000

echo "🔍 Running pre-test validation..."
python validate_deployment.py

echo ""
echo "🧪 Running automated test suite..."
echo "Test URL: $BASE_URL"
echo ""

# Run tests with HTML report
pytest test_service_provider.py \
    -v \
    --html=test-report.html \
    --self-contained-html \
    --tb=short

# Check test results
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 All tests completed successfully!"
    echo "📊 Test report generated: test-report.html"
    echo ""
    echo "View results:"
    echo "- Open test-report.html in your browser"
    echo "- Check console output above for details"
else
    echo ""
    echo "❌ Some tests failed. Check the output above for details."
    echo "📊 Test report still generated: test-report.html"
fi

echo ""
echo "✅ Test execution complete!" 