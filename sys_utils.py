import subprocess

def restart_network_service():
    try:
        subprocess.run(["sudo", "systemctl", "restart", "networking"], check=True)
        print("✅ Network service restarted.")
    except subprocess.CalledProcessError:
        print("❌ Failed to restart network service.")

def clear_arp_cache():
    try:
        subprocess.run(["sudo", "ip", "-s", "-s", "neigh", "flush", "all"], check=True)
        print("✅ ARP cache flushed.")
    except subprocess.CalledProcessError:
        print("❌ Failed to flush ARP cache.")

def block_ip(ip):
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        print(f"✅ Blocked IP: {ip}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to block IP: {ip}")