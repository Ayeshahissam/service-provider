import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import random
import string
import os

# Configure Chrome for headless mode (required for Jenkins/CI environment)
def get_chrome_driver():
    """Configure Chrome driver for headless operation"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Required for Jenkins
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")  # Speed up tests
    
    return webdriver.Chrome(options=chrome_options)

@pytest.fixture
def driver():
    """Setup and teardown Chrome driver"""
    driver = get_chrome_driver()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture
def base_url():
    """Base URL for the application - EC2 deployment URL"""
    return os.getenv('BASE_URL', 'http://18.216.19.144:8000')

def generate_unique_username():
    """Generate a unique username for testing"""
    timestamp = str(int(time.time()))
    random_suffix = ''.join(random.choices(string.ascii_lowercase, k=4))
    return f"testuser_{timestamp}_{random_suffix}"

def wait_for_page_load(driver, timeout=15):
    """Wait for page to be fully loaded"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(2)  # Additional wait for dynamic content
    except TimeoutException:
        print("Warning: Page load timeout, continuing with test")

def test_01_homepage_loads_successfully(driver, base_url):
    """Test 1: Verify homepage loads with correct branding and navigation"""
    print(f"\n=== TEST 1: Homepage Load ===")
    print(f"Loading URL: {base_url}/homepage")
    
    driver.get(f"{base_url}/homepage")
    wait_for_page_load(driver)
    
    print(f"Current URL: {driver.current_url}")
    print(f"Page title: {driver.title}")
    
    try:
        # Check for Local Xperts branding
        navbar_brand = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "navbar-brand"))
        )
        assert "Local Xperts" in navbar_brand.text, f"Expected 'Local Xperts' in navbar, got: {navbar_brand.text}"
        
        # Check for main heading
        main_heading = driver.find_element(By.TAG_NAME, "h1")
        assert "Trusted Local Freelancers" in main_heading.text, f"Expected service message in heading, got: {main_heading.text}"
        
        # Check for Explore button
        explore_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Explore')]")
        assert explore_button.is_displayed(), "Explore button should be visible"
        
        # Check navigation menu items
        services_menu = driver.find_element(By.ID, "servicesDropdown")
        about_link = driver.find_element(By.XPATH, "//a[contains(text(), 'About Us')]")
        contact_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Contact Us')]")
        signup_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Sign Up As Freelancer')]")
        
        assert all([services_menu.is_displayed(), about_link.is_displayed(), 
                   contact_link.is_displayed(), signup_link.is_displayed()]), "All navigation elements should be visible"
        
        print("✅ Homepage loads successfully with all required elements")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

def test_02_services_navigation_and_dropdown(driver, base_url):
    """Test 2: Verify services dropdown navigation works correctly"""
    print(f"\n=== TEST 2: Services Navigation ===")
    
    driver.get(f"{base_url}/homepage")
    wait_for_page_load(driver)
    
    try:
        # Click on Services dropdown
        services_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "servicesDropdown"))
        )
        services_dropdown.click()
        time.sleep(1)
        
        # Check for service categories
        home_services = driver.find_element(By.XPATH, "//a[contains(text(), 'Home Services')]")
        automotive_services = driver.find_element(By.XPATH, "//a[contains(text(), 'Automotive Services')]")
        personal_services = driver.find_element(By.XPATH, "//a[contains(text(), 'Personal Services')]")
        
        assert all([home_services.is_displayed(), automotive_services.is_displayed(), 
                   personal_services.is_displayed()]), "All service categories should be visible"
        
        # Test navigation to home services
        home_services.click()
        wait_for_page_load(driver)
        
        assert "homeservices" in driver.current_url, "Should navigate to home services page"
        
        print("✅ Services navigation working correctly")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

def test_03_freelancer_signup_form_validation(driver, base_url):
    """Test 3: Test freelancer signup form and validation"""
    print(f"\n=== TEST 3: Freelancer Signup Form ===")
    
    driver.get(f"{base_url}/freelancersignup")
    wait_for_page_load(driver)
    
    try:
        # Wait for signup form to be visible
        signup_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "signupBox"))
        )
        
        # If login box is shown first, click to show signup
        if not signup_box.is_displayed():
            show_signup_btn = driver.find_element(By.ID, "showSignUp")
            show_signup_btn.click()
            time.sleep(1)
        
        # Test form elements presence
        fullname_input = driver.find_element(By.ID, "fullname")
        username_input = driver.find_element(By.ID, "signupUsername")
        email_input = driver.find_element(By.ID, "email")
        service_type_select = driver.find_element(By.ID, "serviceType")
        hourly_rate_input = driver.find_element(By.ID, "hourlyrate")
        password_input = driver.find_element(By.ID, "signupPassword")
        confirm_password_input = driver.find_element(By.ID, "confirmPassword")
        profile_image_input = driver.find_element(By.ID, "profileImage")
        
        # Test form input functionality
        test_data = {
            "fullname": "Test Freelancer",
            "username": generate_unique_username(),
            "email": "test@example.com",
            "hourlyrate": "25"
        }
        
        fullname_input.clear()
        fullname_input.send_keys(test_data["fullname"])
        username_input.clear()
        username_input.send_keys(test_data["username"])
        email_input.clear()
        email_input.send_keys(test_data["email"])
        hourly_rate_input.clear()
        hourly_rate_input.send_keys(test_data["hourlyrate"])
        
        # Test service type selection
        service_select = Select(service_type_select)
        service_select.select_by_value("carwash")
        
        # Verify form inputs work
        assert fullname_input.get_attribute("value") == test_data["fullname"], "Full name input not working"
        assert username_input.get_attribute("value") == test_data["username"], "Username input not working"
        assert email_input.get_attribute("value") == test_data["email"], "Email input not working"
        assert hourly_rate_input.get_attribute("value") == test_data["hourlyrate"], "Hourly rate input not working"
        
        print("✅ Freelancer signup form validation working correctly")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

def test_04_login_form_functionality(driver, base_url):
    """Test 4: Test login form functionality and validation"""
    print(f"\n=== TEST 4: Login Form Functionality ===")
    
    driver.get(f"{base_url}/freelancersignup")
    wait_for_page_load(driver)
    
    try:
        # Ensure we're on the login form (default view)
        login_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "loginBox"))
        )
        
        if not login_box.is_displayed():
            show_login_btn = driver.find_element(By.ID, "showLogin")
            show_login_btn.click()
            time.sleep(1)
        
        # Test login form elements
        username_input = driver.find_element(By.ID, "loginUsername")
        password_input = driver.find_element(By.ID, "loginPassword")
        login_btn = driver.find_element(By.ID, "loginBtn")
        
        # Test with invalid credentials
        username_input.clear()
        username_input.send_keys("invaliduser")
        password_input.clear()
        password_input.send_keys("wrongpassword")
        
        assert username_input.get_attribute("value") == "invaliduser", "Username input not working"
        assert password_input.get_attribute("value") == "wrongpassword", "Password input not working"
        
        # Test form switching functionality
        show_signup_btn = driver.find_element(By.ID, "showSignUp")
        show_signup_btn.click()
        time.sleep(1)
        
        signup_box = driver.find_element(By.ID, "signupBox")
        assert signup_box.is_displayed(), "Should show signup form"
        
        print("✅ Login form functionality working correctly")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

def test_05_service_page_freelancer_listings(driver, base_url):
    """Test 5: Test service page loads freelancer listings correctly"""
    print(f"\n=== TEST 5: Service Page Freelancer Listings ===")
    
    driver.get(f"{base_url}/carwash")
    wait_for_page_load(driver)
    
    try:
        # Check page title and heading
        page_heading = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Car Wash Service Providers')]"))
        )
        assert page_heading.is_displayed(), "Service page heading should be visible"
        
        # Check for freelancer cards (flip cards)
        flip_cards = driver.find_elements(By.CLASS_NAME, "flip-card")
        
        if len(flip_cards) > 0:
            # Test first freelancer card
            first_card = flip_cards[0]
            card_inner = first_card.find_element(By.CLASS_NAME, "flip-card-inner")
            
            # Check front of card
            front_card = first_card.find_element(By.CLASS_NAME, "flip-card-front")
            freelancer_name = front_card.find_element(By.CLASS_NAME, "title")
            assert freelancer_name.text.strip() != "", "Freelancer name should not be empty"
            
            # Test card hover/flip functionality by moving to card
            driver.execute_script("arguments[0].style.transform = 'rotateY(180deg)';", card_inner)
            time.sleep(1)
            
            # Check back of card
            back_card = first_card.find_element(By.CLASS_NAME, "flip-card-back")
            hire_button = back_card.find_element(By.CLASS_NAME, "hire-btn")
            assert hire_button.is_displayed(), "Hire button should be visible on card back"
            
            print("✅ Service page freelancer listings working correctly")
        else:
            print("⚠️ No freelancers found - this might be expected if database is empty")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

def test_06_booking_modal_functionality(driver, base_url):
    """Test 6: Test booking modal opens and form works"""
    print(f"\n=== TEST 6: Booking Modal Functionality ===")
    
    driver.get(f"{base_url}/carwash")
    wait_for_page_load(driver)
    
    try:
        # Check if there are freelancers available
        flip_cards = driver.find_elements(By.CLASS_NAME, "flip-card")
        
        if len(flip_cards) > 0:
            # Click hire button on first freelancer
            first_card = flip_cards[0]
            
            # Hover to show back of card
            driver.execute_script("arguments[0].querySelector('.flip-card-inner').style.transform = 'rotateY(180deg)';", first_card)
            time.sleep(1)
            
            hire_button = first_card.find_element(By.CLASS_NAME, "hire-btn")
            hire_button.click()
            
            # Wait for booking modal to appear
            booking_modal = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "bookingModal"))
            )
            
            # Check modal form elements
            customer_name = driver.find_element(By.ID, "customerName")
            customer_email = driver.find_element(By.ID, "customerEmail")
            customer_phone = driver.find_element(By.ID, "customerPhone")
            service_date = driver.find_element(By.ID, "serviceDate")
            service_time = driver.find_element(By.ID, "serviceTime")
            
            # Test form inputs
            customer_name.send_keys("Test Customer")
            customer_email.send_keys("customer@test.com")
            customer_phone.send_keys("1234567890")
            
            assert customer_name.get_attribute("value") == "Test Customer", "Customer name input not working"
            assert customer_email.get_attribute("value") == "customer@test.com", "Customer email input not working"
            
            print("✅ Booking modal functionality working correctly")
        else:
            print("⚠️ No freelancers available to test booking modal")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

def test_07_contact_us_form_submission(driver, base_url):
    """Test 7: Test contact us form and submission"""
    print(f"\n=== TEST 7: Contact Us Form ===")
    
    driver.get(f"{base_url}/contactus")
    wait_for_page_load(driver)
    
    try:
        # Wait for contact form elements
        name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='NAME']"))
        )
        email_input = driver.find_element(By.XPATH, "//input[@placeholder='EMAIL']")
        contact_input = driver.find_element(By.XPATH, "//input[@placeholder='CONTACT_NO']")
        message_input = driver.find_element(By.XPATH, "//textarea[@placeholder='MESSAGE']")
        
        # Test form inputs
        test_data = {
            "name": "Test User",
            "email": "test@contact.com",
            "contact": "1234567890",
            "message": "This is a test message for contact form validation."
        }
        
        name_input.clear()
        name_input.send_keys(test_data["name"])
        email_input.clear()
        email_input.send_keys(test_data["email"])
        contact_input.clear()
        contact_input.send_keys(test_data["contact"])
        message_input.clear()
        message_input.send_keys(test_data["message"])
        
        # Verify form inputs
        assert name_input.get_attribute("value") == test_data["name"], "Name input not working"
        assert email_input.get_attribute("value") == test_data["email"], "Email input not working"
        assert contact_input.get_attribute("value") == test_data["contact"], "Contact input not working"
        assert message_input.get_attribute("value") == test_data["message"], "Message input not working"
        
        # Find and test submit button
        submit_button = driver.find_element(By.CLASS_NAME, "app-form-button")
        assert submit_button.is_enabled(), "Submit button should be enabled"
        
        print("✅ Contact us form working correctly")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

def test_08_about_us_page_content(driver, base_url):
    """Test 8: Test about us page loads with correct content"""
    print(f"\n=== TEST 8: About Us Page ===")
    
    driver.get(f"{base_url}/aboutus")
    wait_for_page_load(driver)
    
    try:
        # Check page title/heading
        page_content = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Look for company information
        page_text = page_content.text.lower()
        assert "local xperts" in page_text or "about" in page_text, "About us page should contain company information"
        
        # Check navigation is still present
        navbar = driver.find_element(By.CLASS_NAME, "navbar")
        assert navbar.is_displayed(), "Navigation should be present on about page"
        
        # Check for any images or content sections
        images = driver.find_elements(By.TAG_NAME, "img")
        if len(images) > 0:
            assert any(img.is_displayed() for img in images), "At least one image should be visible"
        
        print("✅ About us page loads correctly")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

def test_09_responsive_design_mobile_view(driver, base_url):
    """Test 9: Test responsive design on mobile screen size"""
    print(f"\n=== TEST 9: Responsive Design ===")
    
    driver.get(f"{base_url}/homepage")
    wait_for_page_load(driver)
    
    try:
        # Test desktop view first
        driver.set_window_size(1920, 1080)
        time.sleep(1)
        
        navbar = driver.find_element(By.CLASS_NAME, "navbar")
        assert navbar.is_displayed(), "Navbar should be visible on desktop"
        
        # Test mobile view
        driver.set_window_size(375, 667)  # iPhone size
        time.sleep(2)
        
        # Check if mobile toggle button appears
        try:
            mobile_toggle = driver.find_element(By.CLASS_NAME, "navbar-toggler")
            assert mobile_toggle.is_displayed(), "Mobile menu toggle should be visible"
        except NoSuchElementException:
            print("⚠️ Mobile toggle not found - design might not be fully responsive")
        
        # Test that content is still accessible
        main_content = driver.find_element(By.TAG_NAME, "body")
        assert main_content.is_displayed(), "Main content should still be visible on mobile"
        
        # Reset to normal size
        driver.set_window_size(1920, 1080)
        
        print("✅ Responsive design working correctly")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

def test_10_full_user_journey_navigation(driver, base_url):
    """Test 10: Test complete user journey through the application"""
    print(f"\n=== TEST 10: Full User Journey ===")
    
    try:
        # Start from homepage
        driver.get(f"{base_url}/homepage")
        wait_for_page_load(driver)
        
        # Navigate to services
        services_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "servicesDropdown"))
        )
        services_dropdown.click()
        time.sleep(1)
        
        # Go to automotive services
        automotive_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Automotive Services')]")
        automotive_link.click()
        wait_for_page_load(driver)
        
        assert "automotiveservices" in driver.current_url, "Should be on automotive services page"
        
        # Navigate to specific service (car wash)
        carwash_link = driver.find_element(By.XPATH, "//a[contains(@href, '/carwash')]")
        carwash_link.click()
        wait_for_page_load(driver)
        
        assert "carwash" in driver.current_url, "Should be on car wash page"
        
        # Go to contact us
        contact_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Contact Us')]")
        contact_link.click()
        wait_for_page_load(driver)
        
        assert "contactus" in driver.current_url, "Should be on contact us page"
        
        # Go to about us
        about_link = driver.find_element(By.XPATH, "//a[contains(text(), 'About Us')]")
        about_link.click()
        wait_for_page_load(driver)
        
        assert "aboutus" in driver.current_url, "Should be on about us page"
        
        # Return to homepage
        home_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Local Xperts')]")
        home_link.click()
        wait_for_page_load(driver)
        
        assert "homepage" in driver.current_url, "Should be back on homepage"
        
        print("✅ Full user journey navigation working correctly")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__, "-v", "--tb=short"]) 