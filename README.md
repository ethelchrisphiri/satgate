# SatGate Core

A high-performance, full-stack Bitcoin Lightning Network micro-paywall application. This platform enables account-less, non-custodial monetization of digital media by streaming instant micropayments over Layer 2 primitives. Built with a decoupled architecture utilizing an asynchronous Python gateway and an event-driven vanilla client.

## Live Production Links
*   **Interactive API Portal:** [https://satgate-2x79.onrender.com/docs](https://onrender.com)
*   **Web Application Interface:** [https://satgate-git-main-ethel-phiri.vercel.app](https://vercel.app)



## Architecture & Technology Stack

The application is structured as a decoupled monorepo separating infrastructure logic from client presentation layers:

*   **Backend Engine (`/backend`):** Core application routing engineered with **FastAPI** to utilize native asynchronous event loops and request parsing. Hosted on **Render**.
*   **Network Client (`/frontend`):** Lightweight, semantic user viewport leveraging an embedded event-driven **Vanilla JavaScript** polling loop. Managed with minimal layout definitions and hosted on **Vercel**.
*   **Protocol Layer:** Programmatic channel state and invoice integration mapped to the **Alby Developer REST API** for standard BOLT-11 lightning network invoice processing.



## Core Engineering Highlight: Resilient Hybrid Architecture

To guarantee maximum application uptime and support frictionless, isolated integration testing, the backend implements a robust **Hybrid Failure-Fallback State Machine**:

```text
               [ Incoming POST /generate-invoice ]
                               |
                   Is ALBY_API_KEY present?
                     /                  \
                  (Yes)                 (No)
                   /                      \
      [ Try Alby Network Call ]     [ Trigger Local Simulator ]
             /          \                      |
       (HTTP 200)     (Error/Timeout)          |
           /              \                    |
 [ Return Live Invoice ] -> [ Fallback to Mock Engine Vault ]
                                               |
                                    [ Populate Mock lnbc String ]
                                    [ State: Unpaid -> Auto-Settle ]
```

1.  **Production Mode:** If valid environment credentials exist, the engine contacts the Lightning network daemon, returns a live invoice, and queries the settlement status.
2.  **Simulation Fallback:** If API keys are missing, expired, or remote servers experience downtime, the gateway intercepts the crash, switches modes automatically, and maps payment tracking to local stateless memory loops. This design guarantees recruiters can review a fully functional prototype without manual credential injection.



## Security Configuration & Environment Vaults

Production credential isolation is managed strictly using absolute-path variable mapping to protect infrastructure parameters:

*   Private API access strings are securely stored inside a localized, hidden `.env` file on host machines.
*   A strict repository `.gitignore` configuration blindfolds Git tracking to ensure keys (`.env`) and local build caching assets (`venv/`, `__pycache__/`) can never be exposed to public version control histories.



## Step-by-Step Local Deployment

Follow these commands to deploy the application stack inside an isolated local testing profile:

### 1. Initialize the Asynchronous Backend
```bash
cd backend
python3 -m venv env
source env/bin/activate
pip install fastapi uvicorn requests python-dotenv watchfiles
```

Configure your credential variables inside `backend/.env`:
```text
ALBY_API_KEY="your_personal_access_token_string"
```

Fire up the local application server:
```bash
fastapi dev main.py
```
*The interactive API documentation panel will initialize instantly at `http://127.0.0`.*

### 2. Launch the Network Client
Open `frontend/index.html` in your local browser environment. For localized testing profiles, configure the network client variable to intercept local traffic:
```javascript
const BACKEND_URL = "http://127.0.0.1:8000";
```
Upon verification, restore the public variable string to point to your live hosted web endpoint before code delivery pipelines execute.
