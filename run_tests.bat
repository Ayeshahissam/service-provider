@echo off
REM Local Xperts - Test Execution Script (Windows)
REM This script runs the automated test suite against the deployed application

echo 🚀 Local Xperts - Automated Test Suite
echo ======================================
echo Application URL: http://18.216.19.144:8000/homepage
echo.

REM Check if pytest is available
pytest --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ pytest not found. Installing test dependencies...
    pip install -r test-requirements.txt
)

REM Set environment variables
set BASE_URL=http://18.216.19.144:8000

echo 🔍 Running pre-test validation...
python validate_deployment.py

echo.
echo 🧪 Running automated test suite...
echo Test URL: %BASE_URL%
echo.

REM Run tests with HTML report
pytest test_service_provider.py -v --html=test-report.html --self-contained-html --tb=short

if %errorlevel% equ 0 (
    echo.
    echo 🎉 All tests completed successfully!
    echo 📊 Test report generated: test-report.html
    echo.
    echo View results:
    echo - Open test-report.html in your browser
    echo - Check console output above for details
) else (
    echo.
    echo ❌ Some tests failed. Check the output above for details.
    echo 📊 Test report still generated: test-report.html
)

echo.
echo ✅ Test execution complete!
pause 