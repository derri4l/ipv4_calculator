import ipaddress
import csv
import random 

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
        "Usable Hosts": net.num_addresses - 2 if net.num_addresses > 2 else net.num_addresses,      #minus network and broadcast for usable hosts
        "Default Gateway": str(next(net.hosts())) if net.num_addresses > 2 else "N/A",              #first usable IP as default gateway 
    }
    return details

def save_to_csv(data, filename='subnet_details.csv'):
    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow(data)


def main():
    filename = 'quicknet_session.csv'
    print("Welcome to QuickNet - the Private IPv4 Subnet Calculator!")
    print("Input eg: 192.168.10.0/24\n(Use ctrl+C to exit anytime)\n")

    while True:
        try:
            ip_cidr = input("Enter your private IPV4 subnet. (eg. 192.168.10.0/24): ").strip()
            if not is_private_ipv4(ip_cidr):
                print("Invalid input. Please enter a valid private IPv4 subnet in CIDR notation.")
                continue    

            info = subnet_details(ip_cidr)
            print("\nSubnet Details:")
            for k, v in info.items():                                                               #key and value from dict
                print(f"{k}: {v}")

            choice = input("\nSave to CSV? (y/n): ").strip().lower()
            if choice == 'y':
                save_to_csv(info, filename)
                print(f"Subnet details saved to {filename}")

            pmn = input("Continue to Plan My Network? (y/n): ").strip().lower()
            if pmn == 'y':
                plan_my_network(ip_cidr, filename)
                break
            elif pmn == 'n':
                print("Exiting...")
                break
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

# Plan my network
def plan_my_network(ip_cidr, session_file):
    net = ipaddress.ip_network(ip_cidr, strict=False)
    all_hosts = list(net.hosts())

    print("\nWelcome to Plan My Network")
    print("Enter 0 for none or type 'randomize' where available.\n")

    # Static assignments
    static_choice = input("To assign static IPs, do: (eg. 192.168.1.5,192.168.1.8 OR '0' OR randomize): ")
    if static_choice == "0":
        static_ips = []
    elif static_choice.lower() == "randomize":
        static_ips = random.sample(all_hosts, min(10, len(all_hosts)))  # random 10 static IPs
    else:
        static_ips = [ipaddress.ip_address(ip.strip()) for ip in static_choice.split(',')]
    
    # Dynamic assignments
    dhcp_choice = input("To assign dynamic IPs, do: (eg. 10.0.0.100-150 OR '0' OR randomize):")
    if dhcp_choice == "0":
        dhcp_range = []
    else:
        try:
            base, rng = dhcp_choice.split(".")[:-1], dhcp_choice.split(".")[-1]
            start, end = map(int, rng.split('-'))
            prefix = ".".join(base)
            dhcp_range = [ipaddress.ip_address(f"{prefix}.{i}") for i in range(start, end + 1)]
        except:
            print("Invalid range format. Skipping DHCP range.")
            dhcp_range = []

    # VLANs
    vlan_choice = input("VLANs (eg. 10,20,30, OR '0' OR randomize): ").strip()
    vlans = []
    if vlan_choice == "0":
        vlans = []
    elif vlan_choice.lower() == "randomize":
        vlans = random.sample(range(1, 255), 3)  # random 3 VLANs
    else:
        vlans = [int(v.strip()) for v in vlan_choice.split(",")]

    data = {
        "Subnet": str(net),
        "Static IPs": ", ".join(map(str, static_ips)) if static_ips else "None",
        "DHCP Range": ", ".join(map(str, dhcp_range)) if dhcp_range else "None",
        "VLANs": ", ".join(map(str, vlans)) if vlans else "None"
    }
    
    # Save to CSV and display results
    save_to_csv(data, session_file)
    print("\nNetwork Plan:")
    for k, v in data.items():
        print(f"{k}: {v}")
    print(f"\nNetwork plan saved to {session_file}")

if __name__ == "__main__":
    main()


