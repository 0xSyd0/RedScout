import dns.resolver

RED = "\033[31m"
YELLOW_BOLD = "\033[1;33m"
RESET = "\033[0m"

def query_record(domain, rtype, resolver):
    try:
        answers = resolver.resolve(domain, rtype, lifetime=3)

        if rtype == "A":
            return [r.address for r in answers]
        elif rtype == "CNAME":
            return [r.target.to_text() for r in answers]
        elif rtype == "MX":
            return [f"{r.preference} {r.exchange.to_text()}" for r in answers]
        elif rtype == "NS":
            return [r.target.to_text() for r in answers]
        elif rtype == "TXT":
            return ["".join(s.decode() for s in r.strings) for r in answers]
        else:
            return [r.to_text() for r in answers]

    except Exception:
        return ["Not Found"]


def get_dns_records(domain, verbose):

    text = f"PERFORMING DNS ENUMERATION FOR {RESET}{domain.upper()}"
    width = 66

    top = "╔" + "═" * width + "╗"
    bottom = "╚" + "═" * width + "╝"

    padding = (width - len(text)) // 2
    line = "║  " + " " * padding + f"{YELLOW_BOLD}{text}{RESET}{RED}" + " " * (width - padding - len(text)) + "  ║"

    print(f"{RED}{top}")
    print(line)
    print(f"{bottom}{RESET}\n")

    records = {}
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['8.8.8.8', '1.1.1.1'] 

    records["A"] = query_record(domain, "A", resolver)
    records["CNAME"] = query_record(domain, "CNAME", resolver)

    parts = domain.split(".")
    root_domain = ".".join(parts[-2:]) 

    records["MX"] = query_record(root_domain, "MX", resolver)
    records["NS"] = query_record(root_domain, "NS", resolver)
    records["TXT"] = query_record(root_domain, "TXT", resolver)

    for rtype, recs in records.items():
        if verbose == 0:
            output = recs[0] if recs else "Not Found"
            print(f"{YELLOW_BOLD}[{rtype}] {RESET}{output}")
        elif verbose == 1:
            print(f"{YELLOW_BOLD}[{rtype}] Records for {domain if rtype in ['A','CNAME'] else root_domain}:{RESET}")
            for r in recs:
                print(f"  - {r}")
        elif verbose >= 2:
            print(f"{YELLOW_BOLD}[{rtype}] Records for {domain if rtype in ['A','CNAME'] else root_domain}:{RESET}")
            if recs == ["Not Found"]:
                print(f"  - No records found!")
            else:
                for r in recs:
                    print(f"  - {r}")
            print(f"  (Queried {rtype} record for {domain if rtype in ['A','CNAME'] else root_domain} using {resolver.nameservers})\n")

    return records
