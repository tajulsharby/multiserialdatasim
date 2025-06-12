import serial
import serial.tools.list_ports
import time
import random
from datetime import datetime

def list_com_ports(limit=4):
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports][:limit]

def generate_cp_data():
    # Simulate Cathodic Protection voltage (-0.850V to -1.200V)
    return f"CP: {round(random.uniform(-1.2, -0.85), 3)}V"

def generate_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_rov_data():
    easting = round(random.uniform(100000, 200000), 2)
    northing = round(random.uniform(500000, 600000), 2)
    depth = round(random.uniform(5.0, 50.0), 2)
    return f"{easting},{northing},{depth}"

def generate_random_value():
    return str(random.randint(1, 100000))

def main():
    ports = list_com_ports()
    if len(ports) < 1:
        print("No COM ports available.")
        return

    print(f"Transmitting to ports: {ports}")

    serial_connections = []
    for port in ports:
        try:
            ser = serial.Serial(port, baudrate=9600, timeout=1)
            serial_connections.append(ser)
        except Exception as e:
            print(f"Failed to open {port}: {e}")

    try:
        while True:
            lines = [
                generate_cp_data(),
                generate_datetime(),
                generate_rov_data(),
                generate_random_value()
            ]
            for ser in serial_connections:
                for line in lines:
                    ser.write((line + "\n").encode())
                print(f"Sent to {ser.port}: {lines}")
            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping transmission...")
    finally:
        for ser in serial_connections:
            ser.close()
        print("All ports closed.")

if __name__ == "__main__":
    main()
