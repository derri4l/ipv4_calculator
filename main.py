import ipaddress
import csv

# Function to check if an IP address is a private IPv4 address
def is_private_ipv4(ip_cidr): 
    try:
        net = ipaddress.ip_network(ip_cidr, strict=False)
        return net.version == 4 and net.is_private
    except ValueError:
        return False
    
def subnet_details(ip_cidr):
    net = ipaddress.ip_network(ip_cidr, strict=False)
    details = {
        "Network": str(net.network_address),
        "Broadcast": str(net.broadcast_address),
        "Usable Hosts": net.num_addresses - 2 if net.num_addresses > 2 else net.num_addresses,
        "Default Gateway": str(next(net.hosts())) if net.num_addresses > 2 else "N/A",
    }

