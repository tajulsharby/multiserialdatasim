import serial
import serial.tools.list_ports
import threading
import time

def list_com_ports(limit=4):
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports][:limit]

def read_from_port(ser):
    print(f"Listening on {ser.port}...")
    buffer = []
    try:
        while True:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            if line:
                buffer.append(line)
                if len(buffer) == 4:
                    print(f"[{ser.port}] Received block:")
                    for i, row in enumerate(buffer):
                        print(f"  Line {i+1}: {row}")
                    buffer.clear()
    except serial.SerialException as e:
        print(f"[{ser.port}] Serial error: {e}")
    except Exception as e:
        print(f"[{ser.port}] Unexpected error: {e}")
    finally:
        ser.close()
        print(f"[{ser.port}] Closed.")

def main():
    ports = list_com_ports()
    if not ports:
        print("No COM ports found.")
        return

    print(f"Receiving on ports: {ports}")

    threads = []
    for port in ports:
        try:
            ser = serial.Serial(port, baudrate=9600, timeout=1)
            t = threading.Thread(target=read_from_port, args=(ser,))
            t.daemon = True
            t.start()
            threads.append(t)
        except Exception as e:
            print(f"Failed to open {port}: {e}")

    try:
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        print("\nStopping receiver...")

if __name__ == "__main__":
    main()
