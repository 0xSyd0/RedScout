import requests
import re
from requests.exceptions import ConnectTimeout, ReadTimeout, RequestException


RED = "\033[31m"
GREEN = "\033[32m"
YELLOW_BOLD = "\033[1;33m"
RESET = "\033[0m"


def detect_tech(domain, verbose):

    raw_text = f"PERFORMING TECHNOLOGY DETECTION FOR {RESET}{domain.upper()}"
    width = max(66, len(raw_text) + 2)
    top = "╔" + "═" * width + "╗"
    bottom = "╚" + "═" * width + "╝"
    padding = (width - len(raw_text)) // 2
    line = "║  " + " " * padding + f"{YELLOW_BOLD}{raw_text}{RESET}{RED}" + \
        " " * (width - padding - len(raw_text)) + "  ║"
    print(f"\n{RED}{top}")
    print(line)
    print(f"{bottom}{RESET}\n")

    url = f"http://{domain}"

    headers_out = {}
    tech_found = set()

    try:
        r = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0 ReconScanner"})

        headers = r.headers
        body = r.text.lower()

        if verbose >= 2:
            print(f"\n{YELLOW_BOLD}[INFO] HTTP Status:{RESET} {r.status_code}")
            print(f"{YELLOW_BOLD}[INFO] Response Headers:{RESET}")
            for k, v in headers.items():
                print(f"  {k}: {v}")
            print()

        server = headers.get("Server")
        if server:
            tech_found.add(server)

            if verbose == 1:
                print(f"{GREEN}[SERVER]{RESET} {server}")
            elif verbose >= 2:
                print(f"{GREEN}[SERVER]{RESET} {server} (Header: Server)")

        powered = headers.get("X-Powered-By")
        if powered:
            tech_found.add(powered)

            if verbose == 1:
                print(f"{GREEN}[BACKEND]{RESET} {powered}")
            elif verbose >= 2:
                print(f"{GREEN}[BACKEND]{RESET} {powered} (Header: X-Powered-By)")


        if "cloudflare" in headers.get("CF-Ray", "").lower():
            tech_found.add("Cloudflare")

            if verbose == 1:
                print(f"{GREEN}[CDN]{RESET} Cloudflare")
            elif verbose >= 2:
                print(f"{GREEN}[CDN]{RESET} Cloudflare (Detected via CF-Ray header)")


        cookies = headers.get("Set-Cookie", "").lower()

        if "php" in cookies:
            tech_found.add("PHP")

            if verbose == 1:
                print(f"{GREEN}[LANG]{RESET} PHP")
            elif verbose >= 2:
                print(f"{GREEN}[LANG]{RESET} PHP (Detected via Set-Cookie)")

        if "asp.net" in cookies:
            tech_found.add("ASP.NET")

            if verbose == 1:
                print(f"{GREEN}[LANG]{RESET} ASP.NET")
            elif verbose >= 2:
                print(f"{GREEN}[LANG]{RESET} ASP.NET (Detected via Set-Cookie)")

        if "wordpress" in cookies:
            tech_found.add("WordPress")

            if verbose == 1:
                print(f"{GREEN}[CMS]{RESET} WordPress")
            elif verbose >= 2:
                print(f"{GREEN}[CMS]{RESET} WordPress (Detected via Cookie)")


        signatures = {
            "wordpress": "WordPress",
            "wp-content": "WordPress",
            "drupal": "Drupal",
            "joomla": "Joomla",
            "react": "React",
            "vue": "Vue.js",
            "angular": "Angular",
            "jquery": "jQuery",
            "bootstrap": "Bootstrap",
            "shopify": "Shopify",
            "magento": "Magento",
            "nextjs": "Next.js",
            "gtag": "Google Analytics",
            "googletagmanager": "Google Tag Manager"
        }

        for sig, name in signatures.items():
            if sig in body:
                if name not in tech_found:
                    tech_found.add(name)

                    if verbose == 1:
                        print(f"{GREEN}[TECH]{RESET} {name}")
                    elif verbose >= 2:
                        print(f"{GREEN}[TECH]{RESET} {name} (Signature: '{sig}')")

        if verbose == 0:
            if tech_found:
                print(f"{', '.join(sorted(tech_found))}")
            else:
                print("None")

        elif verbose >= 2:
            print(f"\n{YELLOW_BOLD}[SUMMARY]{RESET}")
            print(f"Total Technologies Detected: {len(tech_found)}")

        result = {
            "url": url,
            "technologies": sorted(list(tech_found))
        }

        if not tech_found and verbose >= 1:
            print(f"{RED}No technologies detected{RESET}")

        return result
    except ConnectTimeout:
        print("[ERROR] Connection timed out (host did not respond)")
        return {"error": "connect timeout"}

    except ReadTimeout:
        print("[ERROR] Server took too long to respond")
        return {"error": "read timeout"}

    except RequestException as e:
        print(f"[ERROR] Request failed: {e}")
        return {"error": "request failed"}

    except Exception as e:

        if verbose >= 1:
            print(f"{RED}{e}{RESET}")

        return {"error": str(e)}
