import dns.resolver

def get_dns_records(domain):
    records = {}

    for rtype in ["A", "MX", "NS", "TXT"]:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            records[rtype] = [r.to_text() for r in answers]
        except Exception:
            records[rtype] = ["Not Found"]

    return records
