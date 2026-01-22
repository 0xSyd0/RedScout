import socket
import concurrent.futures

RED = "\033[31m"
YELLOW_BOLD = "\033[1;33m"
RESET = "\033[0m"


def scan_ports(domain, verbose):
    
    raw_text = f"PERFORMING PORT SCAN FOR {RESET}{domain.upper()}"
    width = max(66, len(raw_text) + 2)
    top = "╔" + "═" * width + "╗"
    bottom = "╚" + "═" * width + "╝"
    padding = (width - len(raw_text)) // 2
    line = "║ " + " " * padding + f"{YELLOW_BOLD}{raw_text}{RESET}{RED}" + \
        " " * (width - padding - len(raw_text)) + "   ║"
    print(f"\n{RED}{top}")
    print(line)
    print(f"{bottom}{RESET}\n")

    common_ports = [21, 22, 23, 25, 53, 80, 110, 143,
                    443, 445, 3306, 8080]

    open_ports = []

    def _scan_port(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)

            if verbose >= 2:
                print(f"{RED}[DEBUG]{RESET} Scanning port {port}")

            result = sock.connect_ex((domain, port))
            sock.close()

            if result == 0:
                return port

        except Exception as e:
            if verbose >= 2:
                err = str(e).lower()
                if "timed out" in err:
                    state = "Filtered (no response)"
                elif "refused" in err:
                    state = "Closed (connection refused)"
                elif "unreachable" in err:
                    state = "Host/Network unreachable"
                elif "permission" in err:
                    state = "Permission denied (insufficient privileges)"
                else:
                    state = "Unknown error"

                print(f"{RED}[DEBUG] Port {port} ->{RESET} {state}")


        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(_scan_port, p) for p in common_ports]

        for future in concurrent.futures.as_completed(futures):
            port = future.result()

            if port:
                open_ports.append(port)

                if verbose == 0:
                    print(f"{YELLOW_BOLD}{port}{RESET} open")

                elif verbose == 1:
                    print(f"{YELLOW_BOLD}[OPEN]{RESET} Port {YELLOW_BOLD}{port}{RESET}")

                elif verbose >= 2:
                    print(f"{YELLOW_BOLD}[OPEN]{RESET} Port {YELLOW_BOLD}{port}{RESET} | State: Open | Method: TCP Connect")

    return sorted(open_ports)
