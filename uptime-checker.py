import requests
import pandas as pd
import time

# Load endpoints from CSV
df = pd.read_csv("sample-data/endpoints-sheet.csv")

def parse_headers(header_str):
    headers = {}
    if pd.notna(header_str):
        for item in header_str.split(";"):
            if ":" in item:
                key, value = item.split(":", 1)
                headers[key.strip()] = value.strip()
    return headers

for index, row in df.iterrows():
    url = row["URL"]
    method = row["Method"]
    headers = parse_headers(row["Headers"])
    expected_code = int(row["ExpectedCode"])
    max_latency = int(row["MaxLatencyMs"])

    try:
        start = time.time()
        response = requests.request(method, url, headers=headers)
        latency = int((time.time() - start) * 1000)

        status_ok = response.status_code == expected_code
        latency_ok = latency <= max_latency

        print(f"🔍 Checking {url}")
        print(f"   → Status: {response.status_code} (Expected: {expected_code})")
        print(f"   → Latency: {latency}ms (Max: {max_latency}ms)")

        if not status_ok or not latency_ok:
            print("🚨 ALERT: Issue detected!")
        else:
            print("✅ Healthy")

    except Exception as e:
        print(f"❌ Error checking {url}: {e}")
