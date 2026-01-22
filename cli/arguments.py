import argparse
import re

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
    parser.add_argument("-v","--verbose",action="count",default=0,help="Increase verbosity level (-v, -vv)")

    args = parser.parse_args()
    validate = input_validation(args.domain)

    if not validate:
        print("Invalid URL\n")
        exit(0)

    return parser.parse_args()

def input_validation(value):

    ipv4_pattern = r'^((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}' \
                   r'(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$'

    domain_pattern = r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'

    targets = re.split(r'[,\s]+', value.strip())

    cleaned_targets = []

    for target in targets:

        target = target.strip().lower()

        if not target:
            continue

        target = re.sub(r'^https?://', '', target)

        target = target.split('/')[0]

        parts = target.split('.')

        if len(parts) > 2:
            target = '.'.join(parts[-2:])

        if re.fullmatch(ipv4_pattern, target):
            cleaned_targets.append(target)
            continue

        if re.fullmatch(domain_pattern, target):
            cleaned_targets.append(target)
            continue

        return False

    return cleaned_targets


            