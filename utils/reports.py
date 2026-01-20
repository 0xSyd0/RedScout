import os
from datetime import datetime

def generate_reports(domain, ip, results):
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    txt = f"reports/scan_{domain}_{timestamp}.txt"
    html = f"reports/scan_{domain}_{timestamp}.html"

    # TXT
    with open(txt, "w") as f:
        f.write(f"RedScout Recon Report\n")
        f.write(f"Target: {domain}\nIP: {ip}\nTime: {timestamp}\n\n")

        for section, data in results.items():
            f.write(f"[{section}]\n")
            if isinstance(data, dict):
                for k, v in data.items():
                    f.write(f"{k}: {v}\n")
            elif isinstance(data, list):
                if not data:
                    f.write("No data found\n")
                for item in data:
                    f.write(f"- {item}\n")
            else:
                f.write(str(data))
            f.write("\n")

    # HTML
    with open(html, "w") as f:
        f.write("<html><body>")
        f.write(f"<h1>RedScout Recon Report</h1>")
        f.write(f"<p><b>Target:</b> {domain}</p>")
        f.write(f"<p><b>IP:</b> {ip}</p>")
        f.write(f"<p><b>Time:</b> {timestamp}</p><hr>")

        for section, data in results.items():
            f.write(f"<h2>{section}</h2><ul>")
            if isinstance(data, dict):
                for k, v in data.items():
                    f.write(f"<li><b>{k}</b>: {v}</li>")
            elif isinstance(data, list):
                if not data:
                    f.write("<li>No data found</li>")
                for item in data:
                    f.write(f"<li>{item}</li>")
            else:
                f.write(f"<li>{data}</li>")
            f.write("</ul>")

        f.write("</body></html>")

    return txt, html
