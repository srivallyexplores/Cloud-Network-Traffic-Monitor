import sqlite3
from sys_utils import restart_network_service, clear_arp_cache

LATENCY_THRESHOLD = 0.15  # seconds
ARP_ISSUE_THRESHOLD = 2   # per 10s window

def analyze_and_fix():
    conn = sqlite3.connect('network_metrics.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 1")
    latest = cursor.fetchone()

    if latest:
        _, packets, arp_issues, avg_latency = latest

        if avg_latency > LATENCY_THRESHOLD:
            print("⚠️ High latency detected. Restarting network service...")
            restart_network_service()

        if arp_issues > ARP_ISSUE_THRESHOLD:
            print("⚠️ Too many ARP issues. Flushing ARP cache...")
            clear_arp_cache()
    else:
        print("No data found.")

    conn.close()

if __name__ == "__main__":
    analyze_and_fix()