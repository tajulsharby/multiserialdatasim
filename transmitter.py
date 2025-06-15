import serial
import serial.tools.list_ports
import time
import random

def list_available_ports():
    ports = serial.tools.list_ports.comports()
    port_list = [port.device for port in ports]
    print("Available COM Ports:")
    for i, p in enumerate(port_list):
        print(f"  [{i}] {p} - {ports[i].description}")
    return port_list

def get_user_selected_ports(port_list):
    while True:
        try:
            idx1 = int(input("Enter index for COM Port 1: "))
            idx2 = int(input("Enter index for COM Port 2: "))
            if idx1 == idx2:
                print("Please select two different COM ports.")
                continue
            return port_list[idx1], port_list[idx2]
        except (ValueError, IndexError):
            print("Invalid input. Try again.")

def main():
    port_list = list_available_ports()
    if len(port_list) < 2:
        print("At least two COM ports are required.")
        return

    port1, port2 = get_user_selected_ports(port_list)
    print(f"Selected ports: {port1}, {port2}")

    try:
        ser1 = serial.Serial(port1, baudrate=9600, timeout=1)
        ser2 = serial.Serial(port2, baudrate=9600, timeout=1)

        while True:
            data1 = f"{random.randint(1, 100_000_000)}\r\n"
            data2 = f"{random.randint(1, 100_000_000)}\r\n"

            ser1.write(data1.encode())
            ser2.write(data2.encode())

            print(f"Sent to {port1}: {data1.strip()}")
            print(f"Sent to {port2}: {data2.strip()}")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nTransmission stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'ser1' in locals() and ser1.is_open:
            ser1.close()
            print(f"{port1} closed.")
        if 'ser2' in locals() and ser2.is_open:
            ser2.close()
            print(f"{port2} closed.")

if __name__ == "__main__":
    main()
