from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

def fetch_metrics(limit=20):
    conn = sqlite3.connect('network_metrics.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, packets, arp_issues, avg_latency,
               tcp_packets, udp_packets, anomaly
        FROM metrics
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()
    return rows[::-1]

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/data')
def data():
    rows = fetch_metrics()

    timestamps = [row[0] for row in rows]
    packets = [row[1] for row in rows]
    arp_issues = [row[2] for row in rows]
    latency = [row[3] for row in rows]
    tcp_packets = [row[4] for row in rows]
    udp_packets = [row[5] for row in rows]
    anomalies = [row[6] for row in rows]

    return jsonify({
        'timestamps': timestamps,
        'packets': packets,
        'arp_issues': arp_issues,
        'latency': latency,
        'tcp_packets': tcp_packets,
        'udp_packets': udp_packets,
        'anomalies': anomalies
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')