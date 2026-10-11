import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time
import os
# ============================================
# CONFIGURATION
# ============================================

TOKEN_URL = "https://api.cep.bpcl.in/authorizationserver/oauth/token"
SEARCH_URL = "https://api.cep.bpcl.in/retail/v2/bpcl/retail/rolocators"

CLIENT_ID = os.getenv("BPCL_CLIENT_ID")
CLIENT_SECRET = os.getenv("BPCL_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise RuntimeError(
        "Set BPCL_CLIENT_ID and BPCL_CLIENT_SECRET environment variables."
    )

RADIUS = 20000          # meters
GRID_STEP = 0.18        # about 20 km
MAX_WORKERS = 10

OUTPUT = "BPCL_All_India_Stations.xlsx"

# ============================================
# INDIA BOUNDARY
# ============================================

LAT_MIN = 6.0
LAT_MAX = 37.5

LON_MIN = 68.0
LON_MAX = 97.5

# ============================================
# TOKEN
# ============================================

def get_token():

    r = requests.post(
        TOKEN_URL,
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials",
        },
        timeout=30,
    )

    r.raise_for_status()

    return r.json()["access_token"]


TOKEN = get_token()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

# ============================================
# SEARCH FUNCTION
# ============================================

def search(lat, lon):

    global TOKEN
    global HEADERS

    params = {
        "latitude": lat,
        "longitude": lon,
        "radius": RADIUS,
        "amenities": "All_Amenities",
        "fuelStationCategory": "All",
        "channel": "Web",
        "accountId": ""
    }

    for attempt in range(3):

        try:

            r = requests.get(
                SEARCH_URL,
                headers=HEADERS,
                params=params,
                timeout=60,
            )

            if r.status_code == 401:
                TOKEN = get_token()
                HEADERS = {
                    "Authorization": f"Bearer {TOKEN}"
                }
                continue

            r.raise_for_status()

            return r.json().get("pointOfServices", [])

        except Exception:

            time.sleep(2)

    return []

# ============================================
# GRID
# ============================================

grid = []

lat = LAT_MIN

while lat <= LAT_MAX:

    lon = LON_MIN

    while lon <= LON_MAX:

        grid.append((round(lat, 5), round(lon, 5)))

        lon += GRID_STEP

    lat += GRID_STEP

print("Grid Points :", len(grid))

# ============================================
# DOWNLOAD
# ============================================

records = {}

def process(point):

    lat, lon = point

    data = search(lat, lon)

    return data


with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

    futures = [executor.submit(process, p) for p in grid]

    for future in tqdm(as_completed(futures), total=len(futures)):

        stations = future.result()

        for s in stations:

            roid = s.get("roId")

            if not roid:
                continue

            addr = s.get("address", {})
            geo = s.get("geoPoint", {})

            fuels = []

            for f in s.get("fuelAvailable", []):
                fuels.append(f)

            amenities = []

            for a in s.get("amenities", []):
                amenities.append(a)

            prices = []

            for p in s.get("weekDayFuelPriceList", []):

                prices.append(
                    f"{p.get('displayName')}={p.get('price')}"
                )

            records[roid] = {

                "RO_ID": roid,

                "Name": s.get("name"),

                "Display Name": s.get("displayName"),

                "Address": addr.get("formattedAddress"),

                "Line1": addr.get("line1"),

                "Line2": addr.get("line2"),

                "District": addr.get("district"),

                "Town": addr.get("town"),

                "State": addr.get("region", {}).get("name"),

                "PIN": addr.get("postalCode"),

                "Latitude": geo.get("latitude"),

                "Longitude": geo.get("longitude"),

                "Phone": s.get("telephone"),

                "Cell": addr.get("cellphone"),

                "Email": s.get("email"),

                "Fuel Available": ", ".join(fuels),

                "Amenities": ", ".join(amenities),

                "Fuel Prices": " | ".join(prices)

            }

print()

print("Stations Found :", len(records))

df = pd.DataFrame(records.values())

df = df.sort_values("State")

df.to_excel(OUTPUT, index=False)

print()

print("Saved :", OUTPUT)