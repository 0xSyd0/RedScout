import whois

def get_whois(domain):
    try:
        data = whois.whois(domain)
        return dict(data)
    except Exception as e:
        return {"error": str(e)}
