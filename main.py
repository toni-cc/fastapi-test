from fastapi import FastAPI
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

app = FastAPI()

TARGET_URL = "https://ajnas.mk/account"

@app.get("/extract-email")
async def extract_email():
    # Configure Selenium (headless mode)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # No GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
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

