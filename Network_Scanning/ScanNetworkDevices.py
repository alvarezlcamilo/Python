from scapy.all import ARP, Ether, srp, conf
import nmap


def network_discovery(ip_range):
    # For IPv6 use:
    # conf.L3socket = conf.L3socket6

    arp_request = ARP(pdst=ip_range)
    ether_broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_packet = ether_broadcast / arp_request
    answered_list = srp(arp_request_packet, timeout=2, verbose=False)[0]

    devices = []
    for sent, received in answered_list:
        ports = scan_ports(received.psrc)
        devices.append(
            {'ip': received.psrc, 'mac': received.hwsrc, 'ports': ports})

    return devices


def scan_ports(ip):
    nm = nmap.PortScanner()
    try:
        # nm.scan(ip, '1-1024', '-v')
        nm.scan(ip, '1-1024')
        ports = nm[ip]['tcp']
    except KeyError:
        ports = "No ports found or host is down"

    return ports


### Main block ###
if __name__ == "__main__":
    # IP range to scan
    IP_RANGE = "192.168.1.0/24"

    discovered_devices = network_discovery(IP_RANGE)

    for device in discovered_devices:
        print(f"IP Address: {device['ip']}, MAC Address: {
              device['mac']}\nPorts: {device['ports']}\n")
