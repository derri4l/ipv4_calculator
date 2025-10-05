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
    filename = 'network_session.csv'
    print("Welcome to the Private IPv4 Subnet Calculator!")
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
                print("\nStarting Plan My Network...")
                break
            elif pmn == 'n':
                print("Exiting...")
                break
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
