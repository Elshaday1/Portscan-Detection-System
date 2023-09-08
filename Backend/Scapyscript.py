import psutil

def count_connections_by_port():
    connections = psutil.net_connections()
    port_counts = {}

    for conn in connections:
        if conn.status == 'ESTABLISHED':
            port = conn.laddr.port
            if port in port_counts:
                port_counts[port] += 1
            else:
                port_counts[port] = 1

    return port_counts

# Example usage
connection_counts = count_connections_by_port()
for port, count in connection_counts.items():
    print(f"Port {port}: {count} connections")
