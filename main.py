from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
import httpx

app = FastAPI()


ALTEA_ULTIMA_API_KEY = 'cde5731c16fd4c5480c3f54f59fdf064907c2ec772c741d989c1dcad03faeb4d'

# Your CloudCart API Key


BASE_URL = "https://alteamm.ultima.cloud/interchange/api/v1"

@app.get("/getunpaidinvoices", response_class=HTMLResponse)
async def get_unpaid_invoices(vat_number: str = Query(..., description="The VAT number to filter invoices")):
    """
    Fetch unpaid invoices for a specific VAT number and return them as an HTML table.
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

    # Create the HTML table
    table_html = """
    <table border="1" style="border-collapse: collapse; width: 100%; text-align: left;">
        <thead>
            <tr>
                <th>Invoice Number</th>
                <th>Date</th>
                <th>Due Date</th>
                <th>Customer Name</th>
                <th>Total Sale Value (With VAT)</th>
                <th>Total Unpaid</th>
            </tr>
        </thead>
        <tbody>
    """
    for invoice in filtered_invoices:
        table_html += f"""
            <tr>
                <td>{invoice['number']}</td>
                <td>{invoice['date']}</td>
                <td>{invoice['dueDate']}</td>
                <td>{invoice['customerName']}</td>
                <td>{invoice['totalSaleValueWithVAT']}</td>
                <td>{invoice['totalUnpaid']}</td>
            </tr>
        """

    table_html += """
        </tbody>
    </table>
    """

    # Wrap the table in a basic HTML structure
    html_content = f"""
    <html>
    <head>
        <title>Unpaid Invoices</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            table {{
                margin-top: 20px;
            }}
            th, td {{
                padding: 8px;
                border: 1px solid #ccc;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>Unpaid Invoices for VAT Number: {vat_number}</h1>
        {table_html}
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)
