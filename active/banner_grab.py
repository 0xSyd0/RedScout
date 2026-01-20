import socket

def grab_banner(domain, ports):
    banners = {}

    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((domain, port))
            sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
            banners[port] = sock.recv(1024).decode(errors="ignore").strip()
        except:
            banners[port] = "No banner"
        finally:
            try:
                sock.close()
            except:
                pass

    return banners
