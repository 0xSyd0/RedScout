import socket
import time

RED = "\033[31m"
YELLOW_BOLD = "\033[1;33m"
RESET = "\033[0m"


def grab_banner(domain, ports, verbose):

    text = f"PERFORMING BANNER GRABBING FOR {RESET}{domain.upper()}"
    width = 66
    top = "╔" + "═" * width + "╗"
    bottom = "╚" + "═" * width + "╝"
    padding = (width - len(text)) // 2
    line = "║  " + " " * padding + f"{YELLOW_BOLD}{text}{RESET}{RED}" + \
           " " * (width - padding - len(text)) + "  ║"

    print(f"\n{RED}{top}")
    print(line)
    print(f"{bottom}{RESET}\n")

    banners = {}

    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)

            if verbose >= 2:
                print(f"{RED}[INFO]{RESET} Connecting to {domain}:{port}")

            sock.connect((domain, port))

            if port == 80:
                sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")

                if verbose >= 2:
                    print(f"{RED}[INFO]{RESET} HTTP HEAD request sent")

            full_data = b""

            while True:
                try:
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    full_data += chunk
                except socket.timeout:
                    break

            text = full_data.decode(errors="ignore").strip()
            banners[port] = text

            lines = text.split("\n")
            preview = lines[0] if lines else "Empty response"

            if verbose == 0:
                print(f"{YELLOW_BOLD}[{port}]{RESET} {preview[:80]}")

            elif verbose == 1:
                to_show = "\n".join(lines[:2])
                print(f"{YELLOW_BOLD}[PORT {port}]{RESET} {to_show[:200]}")

            elif verbose >= 2:
                to_show = "\n".join(lines[:3])
                print(f"{YELLOW_BOLD}[PORT {port}]{RESET}")
                print(to_show[:400])
                print(f"{RED}[INFO]{RESET} Bytes received: {len(full_data)}\n")

        except Exception as e:
            banners[port] = "No banner"

            if verbose == 0:
                print(f"{YELLOW_BOLD}[{port}]{RESET} No response")

            elif verbose == 1:
                print(f"{YELLOW_BOLD}[PORT {port}]{RESET} No banner")

            elif verbose >= 2:
                print(f"{YELLOW_BOLD}[PORT {port}]{RESET} Error: {e}")

        finally:
            try:
                sock.close()
            except:
                pass

    return banners
