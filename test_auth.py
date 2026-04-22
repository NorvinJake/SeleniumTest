import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException

@pytest.fixture
def driver():
    service = Service("./chromedriver.exe")
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


def handle_alert(driver):
    try:
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Alert Text: {alert.text}")
        alert.accept()
    except NoAlertPresentException:
        pass


def test_login_valid(driver):
    driver.get("http://localhost:3000/login")
    wait = WebDriverWait(driver, 10)

    email = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Email']")))
    password = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Password']")

    email.send_keys("norvinjakecabutol@gmail.com")
    password.send_keys("123456")

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    handle_alert(driver)

    wait.until(EC.url_changes("http://localhost:3000/login"))

    if driver.current_url != "http://localhost:3000/login":
        print("✅ VALID LOGIN: PASS")
    else:
        print("❌ VALID LOGIN: FAIL")

    assert driver.current_url != "http://localhost:3000/login"


def test_login_invalid(driver):
    driver.get("http://localhost:3000/login")

    email = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Email']")
    password = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Password']")

    email.send_keys("wrong@email.com")
    password.send_keys("wrongpassword")

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    handle_alert(driver)

    if driver.current_url == "http://localhost:3000/login":
        print("✅ INVALID LOGIN BLOCKED: PASS")
    else:
        print("❌ INVALID LOGIN ALLOWED: FAIL")

    assert driver.current_url == "http://localhost:3000/login"