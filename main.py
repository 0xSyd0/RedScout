import socket
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

def main():
    args = parse_args()
    domain = args.domain
    ip = socket.gethostbyname(domain)

    logger.info(f"Scan started for {domain}")
    results = {}

    run_all = args.full

    if args.dns or run_all:
        results["DNS"] = get_dns_records(domain)

    if args.whois or run_all:
        results["WHOIS"] = get_whois(domain)

    if args.subdomains or run_all:
        results["SUBDOMAINS"] = enumerate_subdomains(domain)

    ports = []
    if args.ports or run_all:
        ports = scan_ports(domain)
        results["PORTS"] = ports

    if (args.banner or run_all) and ports:
        results["BANNERS"] = grab_banner(domain, ports)

    if args.tech or run_all:
        results["TECHNOLOGIES"] = detect_tech(domain)

    txt, html = generate_reports(domain, ip, results)

    logger.info("Scan completed successfully")
    print("\nScan Completed")
    print(f"TXT Report: {txt}")
    print(f"HTML Report: {html}")

if __name__ == "__main__":
    main()
