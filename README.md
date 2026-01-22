#  RedScout

<div align="center">
<img width="600" height="300" alt="image" src="https://github.com/user-attachments/assets/7f0aeeaa-a7e6-474c-9167-da5a2b3df913" />


**A Python-based modular reconnaissance framework for offensive security professionals**

Developed by **ITSOLERA – Theta Team** | Offensive Security & Penetration Testing Internship


</div>

---

##  Key Features

###  Passive Reconnaissance

- **WHOIS Lookup** - Domain registration and ownership information
- **DNS Enumeration** - A, MX, NS, TXT record discovery
- **Subdomain Enumeration** - Certificate transparency via `crt.sh`

###  Active Reconnaissance

- **TCP Port Scanning** - Common ports with safe connect scans
- **Banner Grabbing** - Service identification for discovered ports
- **Web Technology Detection** - Wappalyzer-based stack identification

###  Reporting

- **Dual Format Reports** - Both .txt and .html output
- **Comprehensive Data** - Target domain, resolved IP, timestamp, and section-wise results
- **Professional Formatting** - Clean, organized, and easy to parse

###  Modularity

- **Independent Modules** - Each reconnaissance task is a separate module
- **Flexible Execution** - Run individual modules or full reconnaissance
- **CLI-Driven** - Simple command-line interface with flags
- **Configurable Verbosity Levels** – Control output detail using --verbosity or -v, -vv flag:
  
###  Logging

- **Centralized System** - All operations logged to `logs/redscout.log`
- **Dual Output** - Console and file logging enabled
- **Debug Support** - Detailed execution tracking

---

##  Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/0xSyd0/RedScout.git
cd Redscout

# Install dependencies
pip install -r requirements.txt

# Make the file exucatable
chmod +x RedScout
```

### Dependencies

```
dnspython
python-whois
requests
aiodns
```

---

##  Usage

### Full Reconnaissance Scan With Very Verbosity

```bash
./Redscout -d example.com --full -vv
```

### Run Specific Modules

```bash
# DNS and WHOIS only
./Redscout -d example.com --dns --whois

# Subdomain enumeration
./Redscout -d example.com --subdomains

# Port scanning and banner grabbing
./Redscout -d example.com --ports --banner

# Web technology detection
./Redscout -d example.com --tech
```
##  Captures
### Screenshot
![RedScout Screenshot](Captures/image.png)

### Available Flags

| Flag | Description |
|------|-------------|
| `-d, --domain` | Target domain (required) |
| `--full` | Run all reconnaissance modules |
| `--dns` | DNS enumeration |
| `--whois` | WHOIS lookup |
| `--subdomains` | Subdomain enumeration |
| `--ports` | Port scanning |
| `--banner` | Banner grabbing |
| `--tech` | Technology detection |
| `-v, -vv` | Verbosity Mode |

---

##  Project Structure

```
RedScout/
│
├── main.py                 # Main entry point
├── subdomain.txt
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── cli/                   # Command-line interface
│   ├── __init__.py
│   └── arguments.py       # Argument parsing
│
├── passive/               # Passive reconnaissance modules
│   ├── dns_enum.py       # DNS enumeration
│   ├── whois_enum.py     # WHOIS lookup
│   └── subdomain_enum.py # Subdomain discovery
│
├── active/                # Active reconnaissance modules
│   ├── port_scan.py      # Port scanning
│   ├── banner_grab.py    # Banner grabbing
│   └── tech_detect.py    # Technology detection
│
├── utils/                 # Utility modules
│   ├── logger.py         # Logging system
│   └── reports.py        # Report generation
│
├── reports/               # Generated reports (auto-created)
└── logs/                  # Log files (auto-created)
```

---

##  Sample Output

### .txt Report Example

```
RedScout Recon Report
Target: google.com
IP: 142.250.202.14
Time: 20260120_172307

[DNS]
A: ['142.250.202.14']
MX: ['10 smtp.google.com.']
NS: ['ns4.google.com.', 'ns1.google.com.', 'ns3.google.com.', 'ns2.google.com.']
TXT: ['v=spf1 include:_spf.google.com ~all']

[WHOIS]
domain_name: GOOGLE.COM
registrar: MarkMonitor, Inc.
creation_date: 1997-09-15
expiration_date: 2028-09-14

[SUBDOMAINS]
- *.google.com.sg
- adwords.google.com.ar
- www.google.com

[PORTS]
- 80
- 443

[BANNERS]
80: HTTP/1.0 200 OK
Server: gws

[TECHNOLOGIES]
{'Google Web Server'}
```

Reports are automatically saved in the `reports/` directory with timestamps.

---


<div align="center">

**Made by ITSOLERA Theta Team**

⭐ Star this repository if you find it helpful!

</div>
