# BPCL Fuel Station Intelligence Scraper

Python automation for collecting BPCL retail fuel-station records through the BPCL API, using geographic grid searches, concurrent requests, token refresh, deduplication, and Excel export.

## How it works

1. Reads API credentials from environment variables and obtains an OAuth access token using the client-credentials flow.
2. Builds a latitude/longitude grid from the configured geographic bounds and grid step.
3. Sends concurrent station-search requests around grid points, using a configured search radius.
4. Refreshes the token if a request returns HTTP 401 and retries failed searches.
5. Deduplicates stations by the source roId and saves the resulting records to Excel.

## Data fields

The output includes fields when supplied by the API:

- Outlet IDs and names: RO_ID, Name, Display Name
- Address fields: formatted address, lines, district, town, state, and PIN
- Latitude, longitude, phone, cell, and email
- Fuel availability, amenities, and weekday fuel prices

## Requirements

- Python 3.10 or a compatible version
- Packages in requirements.txt
- openpyxl for Excel export

    python -m venv .venv
    .venv/Scripts/Activate.ps1
    pip install -r requirements.txt openpyxl

## Credentials

The script requires two environment variables. Set them in the current PowerShell session before starting the scraper:

    $env:BPCL_CLIENT_ID = "your_client_id"
    $env:BPCL_CLIENT_SECRET = "your_client_secret"

Use credentials issued for authorized API access. Do not hard-code secrets or commit them to the repository.

## Configuration and run

Review the constants near the top of bpcl_all_india_scraper.py:

- RADIUS — search radius in meters
- GRID_STEP — spacing between geographic grid points
- MAX_WORKERS — maximum concurrent workers
- LAT_MIN, LAT_MAX, LON_MIN, LON_MAX — search-grid bounds
- OUTPUT — output workbook filename

Run:

    python bpcl_all_india_scraper.py

The script writes BPCL_All_India_Stations.xlsx to the current working directory and prints the grid and station counts.

## Operational notes

- The grid provides approximate spatial coverage; completeness depends on API behavior, grid spacing, radius, and API permissions.
- High concurrency can increase request volume; adjust MAX_WORKERS and grid parameters responsibly.
- Fuel availability, amenity, and price data reflect the API response captured during the run and should not be treated as guaranteed current prices.

## Synthetic sample data

[`sample_synthetic_12_records.csv`](sample_synthetic_12_records.csv) contains **12 synthetic test records** using the scraper's output schema. These records were generated for schema inspection and portfolio/demo purposes; they were not collected from the source website or API. Names and addresses are fictional, contact details and example.com links are placeholders, coordinates are illustrative, and ratings/prices are not real or current. Do not use them for real-world navigation or pricing decisions.

## Sample workbook

[BPCL_Sample.xlsx](BPCL_Sample.xlsx) is the workbook sample included in this repository for reviewing the BPCL outlet data format. Check the workbook's sheets, source, and collection date before relying on its contents. Outlet details, fuel availability, amenities, and prices may be incomplete or out of date. Confirm you have permission to publish the workbook before redistributing it.
