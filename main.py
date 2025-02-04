from fastapi import FastAPI
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

app = FastAPI()

TARGET_URL = "https://ajnas.mk/account"

@app.get("/extract-email")
async def extract_email():
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280x800")

    try:
        # Install & use WebDriver dynamically
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(TARGET_URL)
        driver.implicitly_wait(5)  # Wait for elements to load

        email_field = driver.find_element(By.ID, "contactInfoEmail")
        email = email_field.get_attribute("value")

        driver.quit()

        if email:
            return {"email": email}
        else:
            return {"error": "Email not found"}

    except Exception as e:
        driver.quit()
        return JSONResponse(content={"error": str(e)}, status_code=500)
