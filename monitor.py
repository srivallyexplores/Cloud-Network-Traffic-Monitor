
from scapy.all import sniff, IP, TCP, UDP, ARP
import subprocess
import sys
import sqlite3
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
    avg_latency REAL,
    tcp_packets INTEGER,
    udp_packets INTEGER,
    anomaly INTEGER
)
''')
conn.commit()

# Track packets
packets = []
latency_samples = []
arp_issues = 0
tcp_packets = 0
udp_packets = 0


def process_packet(pkt):
    global arp_issues, tcp_packets, udp_packets

    packets.append(pkt)

    if pkt.haslayer(TCP):
        tcp_packets += 1

    if pkt.haslayer(UDP):
        udp_packets += 1

    if pkt.haslayer(ARP) and pkt[ARP].op == 2:
        if pkt[ARP].psrc == '0.0.0.0' or pkt[ARP].hwsrc == '00:00:00:00:00:00':
            arp_issues += 1

    elif pkt.haslayer(IP) and pkt.haslayer(TCP):
        if pkt[TCP].flags == 'A':
            latency_samples.append(pkt.time)


# Capture for 10 seconds
print("Capturing packets for 10 seconds...")
sniff(prn=process_packet, timeout=10)


# Calculate metrics
num_packets = len(packets)
avg_latency = 0

if len(latency_samples) >= 2:
    deltas = [
        t2 - t1
        for t1, t2 in zip(latency_samples[:-1], latency_samples[1:])
    ]
    avg_latency = sum(deltas) / len(deltas)


# Anomaly detection
PACKET_THRESHOLD = 500
LATENCY_THRESHOLD = 1.0

anomaly = 1 if (
num_packets > PACKET_THRESHOLD
or avg_latency > LATENCY_THRESHOLD
or arp_issues > 0
) else 0


# Save to database
cursor.execute(
    "INSERT INTO metrics VALUES (?, ?, ?, ?, ?, ?, ?)",
    (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        num_packets,
        arp_issues,
        avg_latency,
        tcp_packets,
        udp_packets,
        anomaly
    )
)

conn.commit()
conn.close()


print(f"Captured {num_packets} packets.")
print(f"TCP packets: {tcp_packets}")
print(f"UDP packets: {udp_packets}")
print(f"ARP issues: {arp_issues}")
print(f"Avg latency: {avg_latency:.4f} seconds")

if anomaly:
    print("WARNING: Traffic anomaly detected!")
else:
    print("Network traffic normal.")

subprocess.run([sys.executable, "cloud_upload.py"])
