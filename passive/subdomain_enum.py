import requests

def enumerate_subdomains(domain, limit=50):
    subdomains = set()

    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                name = entry.get("name_value", "")
                for sub in name.split("\n"):
                    subdomains.add(sub.strip())
    except Exception as e:
        return [f"Error: {e}"]

    return list(subdomains)[:limit]
