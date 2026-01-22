import whois
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import whois

RED = "\033[31m"
YELLOW_BOLD = "\033[1;33m"
RESET = "\033[0m"

MAX_TIMEOUT = 10   # seconds
RETRIES = 2


def _query_whois(domain):
    return whois.whois(domain)


def get_whois(domain, verbose):
    raw_text = f"PERFORMING WHOIS ENUMERATION FOR {RESET}{domain.upper()}"
    width = max(66, len(raw_text) + 2)
    top = "╔" + "═" * width + "╗"
    bottom = "╚" + "═" * width + "╝"
    padding = (width - len(raw_text)) // 2
    line = "║  " + " " * padding + f"{YELLOW_BOLD}{raw_text}{RESET}{RED}" + \
           " " * (width - padding - len(raw_text)) + "  ║"

    print(f"\n{RED}{top}")
    print(line)
    print(f"{bottom}{RESET}\n")
    
    socket.setdefaulttimeout(MAX_TIMEOUT)

    result = None

    with ThreadPoolExecutor(max_workers=1) as executor:

        for attempt in range(RETRIES + 1):

            try:
                future = executor.submit(_query_whois, domain)
                data = future.result(timeout=MAX_TIMEOUT)

                result = dict(data)

            except TimeoutError:
                if verbose >= 1:
                    print(f"{RED}[!] WHOIS Timeout — Retry {attempt+1}/{RETRIES}{RESET}")

            except Exception as e:
                if verbose >= 1:
                    print(f"{RED}[!] WHOIS Error: {e}{RESET}")
                return {"error": str(e)}

    if not result:
        return {"error": "WHOIS lookup failed"}

    cleaned_result = {}

    for key, value in result.items():

        if isinstance(value, list):
            cleaned_result[key] = [str(v) for v in value]

        elif isinstance(value, datetime):
            cleaned_result[key] = value.strftime("%Y-%m-%d %H:%M:%S")

        else:
            cleaned_result[key] = str(value)

    w = whois.whois(domain)
    raw_whois = w.text      # full raw output
    cleaned_result = w     # parsed fields

    if verbose == 0:
        important_keys = [
            "domain_name",
            "registrar",
            "creation_date",
            "expiration_date",
            "name_servers"
        ]

        for key in important_keys:
            if key in cleaned_result:
                print(f"{YELLOW_BOLD}{key}:{RESET} {cleaned_result[key]}")

    elif verbose == 1:
            # Summary output (cleaned)
            for key, value in cleaned_result.items():
                print(f"{YELLOW_BOLD}{key}:{RESET} {value}")
    elif verbose >= 2:
        for key, value in cleaned_result.items():
            print(f"{YELLOW_BOLD}{key}:{RESET} {value}")
        print("")
        print(raw_whois)

    return cleaned_result
