from fastapi import FastAPI, HTTPException, Query
import httpx

app = FastAPI()


ALTEA_ULTIMA_API_KEY = 'cde5731c16fd4c5480c3f54f59fdf064907c2ec772c741d989c1dcad03faeb4d'

# Your CloudCart API Key


BASE_URL = "https://alteamm.ultima.cloud/interchange/api/v1"

@app.get("/getunpaidinvoices")
async def get_unpaid_invoices(vat_number: str = Query(..., description="The VAT number to filter invoices")):
    """
    Fetch unpaid invoices for a specific VAT number.
    """
    headers = {
        "Authorization": ALTEA_ULTIMA_API_KEY  # Authentication
    }

    # Construct the request URL
    url = f"{BASE_URL}/getunpaidinvoices"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    # Handle errors
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail={"message": "Error fetching invoices", "error": response.json()},
        )

    # Get all invoices from the API response
    invoices = response.json()

    # Filter invoices by the provided VAT number
    filtered_invoices = [invoice for invoice in invoices if invoice["vatNumber"] == vat_number]

    # If no invoices are found, return a 404 error
    if not filtered_invoices:
        raise HTTPException(
            status_code=404,
            detail=f"No unpaid invoices found for VAT number {vat_number}",
        )

    # Return the filtered invoices
    return filtered_invoices
