import serial
import serial.tools.list_ports
import time
import random
import sys

BAUDRATE = 9600
SEND_INTERVAL_SEC = 1.0  # seconds between transmissions
MIN_VAL = 1
MAX_VAL = 100_000_000


def list_available_ports():
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("No COM ports detected.")
        return []

    print("Available COM Ports:")
    for i, p in enumerate(ports):
        print(f"  [{i}] {p.device} - {p.description}")
    return ports


def get_user_selected_ports(ports):
    port_count = len(ports)

    while True:
        try:
            idx1 = int(input("Enter index for COM Port 1: "))
            idx2 = int(input("Enter index for COM Port 2: "))

            if idx1 == idx2:
                print("❌ Please select two different COM ports.\n")
                continue

            if not (0 <= idx1 < port_count and 0 <= idx2 < port_count):
                print("❌ Index out of range. Try again.\n")
                continue

            return ports[idx1].device, ports[idx2].device

        except ValueError:
            print("❌ Invalid input. Please enter a number.\n")


def main():
    ports = list_available_ports()
    if len(ports) < 2:
        print("At least two COM ports are required. Exiting.")
        sys.exit(1)

    port1, port2 = get_user_selected_ports(ports)
    print(f"\nSelected ports: {port1}, {port2}")
    print(f"Baudrate: {BAUDRATE}, interval: {SEND_INTERVAL_SEC}s\n")

    ser1 = ser2 = None

    try:
        ser1 = serial.Serial(port1, baudrate=BAUDRATE, timeout=1)
        ser2 = serial.Serial(port2, baudrate=BAUDRATE, timeout=1)
    except serial.SerialException as e:
        print(f"❌ Failed to open ports: {e}")
        if ser1 and ser1.is_open:
            ser1.close()
        if ser2 and ser2.is_open:
            ser2.close()
        sys.exit(1)

    print("▶ Starting transmission. Press Ctrl+C to stop.\n")

    try:
        while True:
            data1 = f"{random.randint(MIN_VAL, MAX_VAL)}\r\n"
            data2 = f"{random.randint(MIN_VAL, MAX_VAL)}\r\n"

            ser1.write(data1.encode("ascii"))
            ser2.write(data2.encode("ascii"))

            print(f"Sent to {port1}: {data1.strip()}")
            print(f"Sent to {port2}: {data2.strip()}")
            time.sleep(SEND_INTERVAL_SEC)

    except KeyboardInterrupt:
        print("\n⏹ Transmission stopped by user.")
    except Exception as e:
        print(f"\n❌ Error during transmission: {e}")
    finally:
        if ser1 and ser1.is_open:
            ser1.close()
            print(f"{port1} closed.")
        if ser2 and ser2.is_open:
            ser2.close()
            print(f"{port2} closed.")


if __name__ == "__main__":
    main()
