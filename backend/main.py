import os
import random
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(current_dir, ".env"))

app = FastAPI(title="Bitcoin Lightning Paywall API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALBY_API_KEY = os.environ.get("ALBY_API_KEY")
ALBY_BASE_URL = "https://getalby.com"

INVOICE_DB = {}

@app.get("/")
def health_check():
    """System Health & DevOps Monitoring Endpoint"""
    return {
        "status": "healthy",
        "mode": "live" if ALBY_API_KEY else "simulation-fallback",
        "network": "bitcoin-lightning",
        "version": "1.0.0"
    }

@app.post("/generate-invoice")
def generate_invoice():
    """Attempts live network invoice generation; falls back to simulation on error."""
    if ALBY_API_KEY and ALBY_API_KEY != "PASTE_YOUR_ALBY_PERSONAL_ACCESS_TOKEN_HERE":
        try:
            url = f"{ALBY_BASE_URL}/invoices"
            headers = {
                "Authorization": f"Bearer {ALBY_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {"amount": 10, "memo": "SatGate Premium Unlock"}
            
            response = requests.post(url, json=data, headers=headers, timeout=5)
            
            if response.status_code == 200:
                res_json = response.json()
                return {
                    "invoice": res_json.get("payment_request"),
                    "checking_id": res_json.get("id"),
                    "type": "live"
                }
        except Exception:
            pass
    random_id = f"mock_id_{random.randint(100000, 999999)}"
    mock_ln_invoice = f"lnbc100n1p{random.randint(10,99)}xxxxxx_mock_invoice_for_testing"
    
    INVOICE_DB[random_id] = False 
    
    return {
        "invoice": mock_ln_invoice,
        "checking_id": random_id,
        "type": "simulation"
    }

@app.get("/check-payment/{checking_id}")
def check_payment(checking_id: str):
    """Verifies network state or simulates payment confirmation for local testing."""
    if not checking_id.startswith("mock_id_") and ALBY_API_KEY:
        try:
            url = f"{ALBY_BASE_URL}/invoices/{checking_id}"
            headers = {"Authorization": f"Bearer {ALBY_API_KEY}"}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                return {"paid": response.json().get("settled", False)}
        except Exception:
            raise HTTPException(status_code=500, detail="Unable to reach Lightning network daemon.")

    if checking_id not in INVOICE_DB:
        raise HTTPException(status_code=404, detail="Invoice identifier not found.")
        
    if INVOICE_DB[checking_id] == False:
        return {"paid": False}
    else:
        return {"paid": True}
