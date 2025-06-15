import serial
import serial.tools.list_ports
import time
import random

def get_two_available_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports[:2]]  # Take the first two

def main():
    ports = get_two_available_ports()
    if len(ports) < 2:
        print("Need at least two COM ports.")
        return

    print(f"Opening ports: {ports[0]} and {ports[1]}")

    try:
        ser1 = serial.Serial(ports[0], baudrate=9600, timeout=1)
        ser2 = serial.Serial(ports[1], baudrate=9600, timeout=1)

        while True:
            number = random.randint(1, 100_000_000)
            data = f"{number}\r\n"
            ser1.write(data.encode())
            ser2.write(data.encode())
            print(f"Sent to {ports[0]} and {ports[1]}: {data.strip()}")
            time.sleep(1)

    except KeyboardInterrupt:
        print("Transmission stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'ser1' in locals() and ser1.is_open:
            ser1.close()
            print(f"Port {ports[0]} closed.")
        if 'ser2' in locals() and ser2.is_open:
            ser2.close()
            print(f"Port {ports[1]} closed.")

if __name__ == "__main__":
    main()
