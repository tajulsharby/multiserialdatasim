import serial
import serial.tools.list_ports
import time
import random

def get_first_available_port():
    ports = serial.tools.list_ports.comports()
    return ports[0].device if ports else None

def main():
    port = get_first_available_port()
    if not port:
        print("No COM port available.")
        return

    print(f"Opening port: {port}")
    try:
        ser = serial.Serial(port, baudrate=9600, timeout=1)
        while True:
            random_number = random.randint(1, 100_000_000)
            data = f"{random_number}\n"
            ser.write(data.encode())
            print(f"Sent: {data.strip()}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Transmission stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Port closed.")

if __name__ == "__main__":
    main()
