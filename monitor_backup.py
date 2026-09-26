from scapy.all import sniff, IP, TCP, ARP
import sqlite3
import time
from datetime import datetime

# Connect to SQLite
conn = sqlite3.connect('network_metrics.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS metrics (
    timestamp TEXT,
    packets INTEGER,
    arp_issues INTEGER,
    avg_latency REAL
)
''')
conn.commit()

# Track packets
packets = []
latency_samples = []
arp_issues = 0

def process_packet(pkt):
    global arp_issues
    packets.append(pkt)

    if pkt.haslayer(ARP) and pkt[ARP].op == 2:  # ARP reply
        # check for invalid MAC mapping
        if pkt[ARP].psrc == '0.0.0.0' or pkt[ARP].hwsrc == '00:00:00:00:00:00':
            arp_issues += 1

    elif pkt.haslayer(IP) and pkt.haslayer(TCP):
        if pkt[TCP].flags == 'A':  # ACK packet
            latency_samples.append(pkt.time)

# Capture for 10 seconds
print("Capturing packets for 10 seconds...")
sniff(prn=process_packet, timeout=10)

# Calculate metrics
num_packets = len(packets)
avg_latency = 0
if len(latency_samples) >= 2:
    deltas = [t2 - t1 for t1, t2 in zip(latency_samples[:-1], latency_samples[1:])]
    avg_latency = sum(deltas) / len(deltas)

# Save to DB
cursor.execute("INSERT INTO metrics VALUES (?, ?, ?, ?)", (
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    num_packets,
    arp_issues,
    avg_latency
))
conn.commit()
conn.close()

print(f"Captured {num_packets} packets.")
print(f"ARP issues: {arp_issues}")
print(f"Avg latency: {avg_latency:.4f} seconds")