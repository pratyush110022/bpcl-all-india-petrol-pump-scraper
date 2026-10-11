# BPCL All India Petrol Pump Scraper

Python automation project for collecting and consolidating BPCL petrol pump locations across India.

## Overview

This repository contains the Python script used for the project.
The actual collection methods, geographic coverage, and output depend
on the implementation and source availability.

## Features

- Geographic grid-based searches across India
- Concurrent API requests
- Retry handling and access-token refresh
- Outlet deduplication and Excel export

## Technology Stack

- Python
- Data collection and processing
- Structured data handling
- Excel integration, where supported by the script

## Repository Structure

```
bpcl-all-india-petrol-pump-scraper/
|-- bpcl_all_india_scraper.py
|-- README.md
|-- requirements.txt
|-- .gitignore
```

## Setup

Use Python 3.10 or a compatible version supported by the script.

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run

```powershell
python "bpcl_all_india_scraper.py"
```

Review the script configuration before running it. If authentication
is required, use authorized credentials and keep secrets outside
the source code.

## Data and Usage Notes

- Data completeness depends on the source and collection process.
- Check the source provider's terms and permissions.
- Do not publish confidential data or credentials.
- Treat collected data as a snapshot unless freshness is verified.

## Author

**Pratyush Das**

GitHub: https://github.com/pratyush110022
