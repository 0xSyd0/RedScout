import random
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

RED = "\033[31m"
YELLOW_BOLD = "\033[1;33m"
RESET = "\033[0m"

MAX_THREADS = 100   

def enumerate_subdomains(domain, verbose):
    raw_text = f"PERFORMING SUBDOMAIN ENUMERATION FOR {RESET}{domain.upper()}"

    width = max(66, len(raw_text) + 2)

    top = "╔" + "═" * width + "╗"
    bottom = "╚" + "═" * width + "╝"

    padding = (width - len(raw_text)) // 2

    line = "║  " + " " * padding + f"{YELLOW_BOLD}{raw_text}{RESET}{RED}" + \
           " " * (width - padding - len(raw_text)) + "  ║"

    print(f"\n{RED}{top}")
    print(line)
    print(f"{bottom}{RESET}\n")
    
    result = []
    with open("subdomain.txt", "r", encoding="utf-8", errors="ignore") as f:
        words = [line.strip() for line in f if line.strip()]
    sample_size = min(800, len(words))
    random_words = random.sample(words, sample_size)

    def check_subdomain(word):
        subdomain = f"{word}.{domain}"
        try:
            ip = socket.gethostbyname(subdomain)
            return subdomain, ip
        except socket.gaierror:
            return None
        
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:

        futures = [executor.submit(check_subdomain, word) for word in random_words]

        for future in as_completed(futures):
            result_data = future.result()

            if result_data:
                subdomain, ip = result_data

                if verbose == 0:
                    print(f"{RESET}{subdomain}")
                elif verbose == 1:
                    print(f"{YELLOW_BOLD}{subdomain} -> {RESET}{ip}")
                elif verbose >= 2:
                    print(f"{RESET}{subdomain}{YELLOW_BOLD} resolved to {RESET}{ip}")

                result.append({
                    "subdomain": subdomain,
                    "ip": ip
                })

    return result
