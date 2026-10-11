# BPCL All India Petrol Pump Scraper

A Python automation project that collects BPCL retail outlet information
using the BPCL retail locator API.

## Features
- Geographic grid-based search across India
- Concurrent API requests
- Retry handling and access-token refresh
- Duplicate removal using retail outlet IDs
- Excel export with state-wise sorting

## Technology
Python, Requests, Pandas, ThreadPoolExecutor, tqdm, OpenPyXL

## Installation
Create a virtual environment and install dependencies:

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt

## Credentials
Set authorized API credentials in PowerShell:

    $env:BPCL_CLIENT_ID = "your_client_id"
    $env:BPCL_CLIENT_SECRET = "your_client_secret"

## Run

    python bpcl_all_india_scraper.py

## Output
BPCL_All_India_Stations.xlsx

Coverage and results depend on API access, response availability,
and the configured search grid. Use the API in accordance with
the provider's applicable terms.
