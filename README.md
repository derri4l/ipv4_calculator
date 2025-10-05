# QuickNet - the Private IPv4 Subnet Calculator
A lightweight IPv4 subnet calculator + basic network planner for subnetting and IP management basics.

---
 ## How does it work
 - It first validates that the input is a private IPV4 subnet (10.x.x.x, 172.16–31.x.x, 192.168.x.x).
 - Shows network address, broadcast address, what hosts are usable and the default gateway.
 - Lets you plan simple networks allowing you to plan for:
    * Static IP's (manually or randomized)
    * DHCP ranges
    * VLANs (manually or randomized)
- Auto-saves all results to one CSV file per session.

## How do you run it
python main.py
