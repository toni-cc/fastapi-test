from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

TARGET_URL = "https://ajnas.mk/account"

@app.get("/extract-email")
async def extract_email():
    async with httpx.AsyncClient() as client:
        response = await client.get(TARGET_URL)

        if response.status_code != 200:
            return JSONResponse(content={"error": "Failed to fetch page"}, status_code=500)

        soup = BeautifulSoup(response.text, "html.parser")
        email_field = soup.find("input", {"id": "contactInfoEmail"})

        if email_field and "value" in email_field.attrs:
            email = email_field["value"]
            return {"email": email}
        else:
            return {"error": "Email not found"}

