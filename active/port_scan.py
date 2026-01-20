import socket

def scan_ports(domain):
    open_ports = []
    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 8080]

    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            if sock.connect_ex((domain, port)) == 0:
                open_ports.append(port)
            sock.close()
        except:
            pass

    return open_ports
