from serial.tools.list_ports_common import ListPortInfo
from datetime import date
from datetime import datetime


import serial
import serial.tools.list_ports
import time
import random
import sys

BAUDRATE = 9600
SEND_INTERVAL_SEC = 1.0  # seconds between transmissions
MIN_VAL = 1
MAX_VAL = 100_000_000
MIN_UTM_EASTING_VAL = 100000.00
MAX_UTM_EASTING_VAL = 999999.99
MIN_UTM_NORTHING_VAL = 1000000.000
MAX_UTM_NORTHING_VAL = 9999999.999
MIN_HEADING_VAL = 0.00
MAX_HEADING_VAL = 359.99
MIN_DEPTH_VAL = 0.00
MAX_DEPTH_VAL = 500.00
MIN_CP_VAL = -1.5
MAX_CP_VAL = 1.1
EASTING_DECIMAL_PLACES = 2
NORTHING_DECIMAL_PLACES = 3
HEADING_DECIMAL_PLACES = 2
CP_DECIMAL_PLACES = 2

current_depth = MIN_DEPTH_VAL
next_depth = current_depth + 0.1

current_utm_easting = MIN_UTM_EASTING_VAL
next_utm_easting = current_utm_easting + 0.1

current_utm_northing = MIN_UTM_NORTHING_VAL
next_utm_northing = current_utm_northing + 0.1

def list_available_ports():
    ports = list[ListPortInfo](serial.tools.list_ports.comports())
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

# Get current system date, paramater accept format, default is YYYY-MM-DD
def get_current_system_date():
    today = date.today()
    return today

# Get current system time
def get_current_system_time():
    now = datetime.now().strftime("%H:%M:%S")
    return now


# Generate easting value
def generate_easting_value():
    if next_utm_easting > MAX_UTM_EASTING_VAL:
        # reset to minimum easting
        current_utm_easting = MIN_UTM_EASTING_VAL
        next_utm_easting = current_utm_easting + 0.1
    else:
        # increment easting
        next_utm_easting += 0.1
    return round(current_utm_easting, EASTING_DECIMAL_PLACES)

# Generate northing value
def generate_northing_value():
    if next_utm_northing > MAX_UTM_NORTHING_VAL:
        # reset to minimum northing
        current_utm_northing = MIN_UTM_NORTHING_VAL
        next_utm_northing = current_utm_northing + 0.1
    else:
        # increment northing
        next_utm_northing += 0.1
    return round(current_utm_northing, NORTHING_DECIMAL_PLACES)

# Generate random heading
def generate_random_heading_value():
    return round(random.randint(MIN_HEADING_VAL, MAX_HEADING_VAL))

# Generate depth value
def generate_depth_value():
    if next_depth > MAX_DEPTH_VAL:
        # reset to minimum depth
        current_depth = MIN_DEPTH_VAL
        next_depth = current_depth + 0.1
    else:
        # increment depth
        next_depth += 0.1
    return current_depth

# Generate CP value
def generate_cp_value():
    return round(random.uniform(MIN_CP_VAL, MAX_CP_VAL), CP_DECIMAL_PLACES)

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
            # heading,easting,northing,random int
            data1 = f"{generate_random_heading_value()},{generate_easting_value()},{generate_northing_value()}\r\n"
            # CP
            data2 = f"{generate_cp_value()}\r\n"

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