import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="RedScout - Modular Reconnaissance Tool"
    )

    parser.add_argument("-d", "--domain", required=True, help="Target domain")

    parser.add_argument("--dns", action="store_true", help="DNS Enumeration")
    parser.add_argument("--whois", action="store_true", help="WHOIS Lookup")
    parser.add_argument("--subdomains", action="store_true", help="Subdomain Enumeration")
    parser.add_argument("--ports", action="store_true", help="Port Scanning")
    parser.add_argument("--banner", action="store_true", help="Banner Grabbing")
    parser.add_argument("--tech", action="store_true", help="Technology Detection")

    parser.add_argument("--full", action="store_true", help="Run Full Recon")

    return parser.parse_args()
