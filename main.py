import socket
import signal
import sys
import threading
import os
from cli.arguments import parse_args
from utils.loggers import setup_logger
from utils.reports import generate_reports

from passive.dns_enum import get_dns_records
from passive.whois_enum import get_whois
from passive.subdomain_enum import enumerate_subdomains

from active.port_scan import scan_ports
from active.banner_grab import grab_banner
from active.tech_detect import detect_tech

logger = setup_logger()

RED = "\033[31m"
GREEN = "\033[32m"
BOLD = "\033[1m"
RESET = "\033[0m"
TICK = "\u2714"
YELLOW = "\033[33m"
GREEN  = "\033[32m"
BLUE   = "\033[34m"
RESET  = "\033[0m"
B_YELLOW = "\033[1;33m"
B_GREEN  = "\033[1;32m"
B_BLUE   = "\033[1;34m"

def arguments(args):
    print(f"{RED}{BOLD} TARGET: {YELLOW}{args.domain}")

    if args.verbose == 0:
        print(f"{RED}{BOLD} VERBOSITY LEVEL: {B_YELLOW}0{RESET}")
    elif args.verbose == 1:
        print(f"{RED}{BOLD} VERBOSITY LEVEL: {B_YELLOW}1{RESET}")
    elif args.verbose == 2:
        print(f"{RED}{BOLD} VERBOSITY LEVEL: {B_YELLOW}2{RESET}")

    if args.full:
        print(f"{RED}{BOLD} FULL SCAN: {GREEN}{TICK}{RESET}")
        return 0

    if args.dns:
        print(f"{RED}{BOLD} DNS ENUMERATION: {GREEN}{TICK}{RESET}")
    if args.whois:
        print(f"{RED}{BOLD} WHOIS LOOKUP: {GREEN}{TICK}{RESET}")
    if args.subdomains:
        print(f"{RED}{BOLD} SUBDOMAIN ENUMERATION: {GREEN}{TICK}{RESET}")
    if args.ports:
        print(f"{RED}{BOLD} PORT SCANING: {GREEN}{TICK}{RESET}")
    if args.tech:
        print(f"{RED}{BOLD} WEb FINGERPRINTING: {GREEN}{TICK}{RESET}")
    if args.banner:
        print(f"{RED}{BOLD} BNNER GRABBING : {GREEN}{TICK}{RESET}")


def main():
    args = parse_args()
    domain = args.domain
    verbose = args.verbose

    arguments(args)
    ip = socket.gethostbyname(domain)

    start(domain, "SCAN STARTED FOR")
    results = {}

    run_all = args.full

    if args.dns or run_all:
        results["DNS"] = get_dns_records(domain, verbose)

    if args.whois or run_all:
        results["WHOIS"] = get_whois(domain, verbose)

    if args.subdomains or run_all:
        results["SUBDOMAINS"] = enumerate_subdomains(domain, verbose)

    ports = []
    if args.ports or run_all:
        ports = scan_ports(domain, verbose)
        results["PORTS"] = ports

    if (args.banner or run_all) and ports:
        results["BANNERS"] = grab_banner(domain, ports, verbose)

    if args.tech or run_all:
        results["TECHNOLOGIES"] = detect_tech(domain, verbose)

    txt, html = generate_reports(domain, ip, results)

    print(" ")
    start(domain, "SCAN COMPLETED FOR")
    print(f"{RED}TXT Report: {RESET}{txt}")
    print(f"{RED}HTML Report: {RESET}{html}\n")

def banner():

    print(f"""{RED}
██████╗ ███████╗██████╗ ███████╗ ██████╗ ██████╗ ██╗   ██╗████████╗
██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔═══██╗██║   ██║╚══██╔══╝
██████╔╝█████╗  ██║  ██║███████╗██║     ██║   ██║██║   ██║   ██║   
██╔══██╗██╔══╝  ██║  ██║╚════██║██║     ██║   ██║██║   ██║   ██║   
██║  ██║███████╗██████╔╝███████║╚██████╗╚██████╔╝╚██████╔╝   ██║   
╚═╝  ╚═╝╚══════╝╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝   
{BOLD}
          REDscout Recon Framework
          Created By: {B_YELLOW} ITSOLERA (Team Theta) {RED}

{RESET}""")


def start(domain, prompt):
    RED = "\033[31m"
    YELLOW_BOLD = "\033[1;33m"
    RESET = "\033[0m"

    text = f"{prompt} {domain.upper()}"
    width = 66

    top = "╔" + "═" * width + "╗"
    bottom = "╚" + "═" * width + "╝"

    padding = (width - len(text)) // 2
    line = " " * padding + f"{YELLOW_BOLD}{text}{RESET}{RED}" + " " * (width - padding - len(text))

    print(f"\n{line}{RESET}")

stop_event = threading.Event()
exit_counter = 0

def handle_interrupt(sig, frame):
    global exit_counter
    exit_counter += 1

    if exit_counter == 1:
        print(f"\n{RED}{BOLD}[!] Interrupt detected — shutting down safely...{RESET}")
        stop_event.set()
        exit(0)

signal.signal(signal.SIGINT, handle_interrupt)

def safe_main():
    try:
        banner()
        main()

    except KeyboardInterrupt:
        stop_event.set()

    finally:
        stop_event.set()

        for t in threading.enumerate():
            if t is not threading.main_thread():
                t.join(timeout=2)
        sys.exit(0)


if __name__ == "__main__":
    safe_main()
    

