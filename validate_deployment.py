#!/usr/bin/env python3
"""
Quick validation script to test if the Local Xperts application is accessible
and the test configuration is working correctly.
"""

import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://18.216.19.144:8000"

def test_application_accessibility():
    """Test if the application is accessible via HTTP requests"""
    print("🔍 Testing application accessibility...")
    
    test_urls = [
        f"{BASE_URL}/homepage",
        f"{BASE_URL}/freelancersignup", 
        f"{BASE_URL}/contactus",
        f"{BASE_URL}/aboutus",
        f"{BASE_URL}/carwash"
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {url} - Accessible (Status: {response.status_code})")
            else:
                print(f"⚠️ {url} - Unexpected status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {url} - Error: {str(e)}")

def test_selenium_setup():
    """Test if Selenium can successfully connect to the application"""
    print("\n🔍 Testing Selenium setup...")
    
    # Configure Chrome for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        
        # Test homepage
        print(f"📍 Loading: {BASE_URL}/homepage")
        driver.get(f"{BASE_URL}/homepage")
        
        # Wait for and check key elements
        navbar_brand = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "navbar-brand"))
        )
        
        if "Local Xperts" in navbar_brand.text:
            print("✅ Homepage loaded successfully")
            print(f"   - Page title: {driver.title}")
            print(f"   - Navbar brand: {navbar_brand.text}")
            
            # Test navigation elements
            nav_elements = driver.find_elements(By.XPATH, "//a[contains(text(), 'Services')]")
            if nav_elements:
                print("✅ Navigation elements found")
            
            # Test main heading
            try:
                main_heading = driver.find_element(By.TAG_NAME, "h1")
                print(f"✅ Main heading found: {main_heading.text[:50]}...")
            except:
                print("⚠️ Main heading not found")
                
        else:
            print("❌ Unexpected content on homepage")
            
    except Exception as e:
        print(f"❌ Selenium test failed: {str(e)}")
        
    finally:
        try:
            driver.quit()
        except:
            pass

def validate_test_endpoints():
    """Validate specific endpoints that will be tested"""
    print("\n🔍 Validating test endpoints...")
    
    test_endpoints = {
        "Homepage": f"{BASE_URL}/homepage",
        "Freelancer Signup": f"{BASE_URL}/freelancersignup",
        "Car Wash Service": f"{BASE_URL}/carwash",
        "Contact Us": f"{BASE_URL}/contactus",
        "About Us": f"{BASE_URL}/aboutus",
        "Home Services": f"{BASE_URL}/homeservices",
        "Automotive Services": f"{BASE_URL}/automotiveservices",
        "Personal Services": f"{BASE_URL}/personalservices"
    }
    
    accessible_count = 0
    total_count = len(test_endpoints)
    
    for name, url in test_endpoints.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {name}: Accessible")
                accessible_count += 1
            else:
                print(f"❌ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: Connection error")
    
    print(f"\n📊 Summary: {accessible_count}/{total_count} endpoints accessible")
    
    if accessible_count == total_count:
        print("🎉 All endpoints are accessible! Ready for testing.")
    elif accessible_count > total_count // 2:
        print("⚠️ Most endpoints accessible. Some tests may fail.")
    else:
        print("❌ Many endpoints inaccessible. Check application deployment.")

if __name__ == "__main__":
    print("🚀 Local Xperts Application Validation")
    print("=" * 50)
    print(f"Testing deployment at: {BASE_URL}")
    print()
    
    # Run all validation tests
    test_application_accessibility()
    test_selenium_setup()
    validate_test_endpoints()
    
    print("\n" + "=" * 50)
    print("✅ Validation complete!")
    print("\nNext steps:")
    print("1. If all tests passed, run: pytest test_service_provider.py -v")
    print("2. Or run individual test: pytest test_service_provider.py::test_01_homepage_loads_successfully -v")
    print("3. Generate HTML report: pytest test_service_provider.py --html=test-report.html --self-contained-html") 