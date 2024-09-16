# Bluetooth Remote Auto-Connect
import subprocess
import time

def connect_bluetooth(mac_address):
    try:
        # Start Bluetooth service
        subprocess.run(['sudo', 'systemctl', 'start', 'bluetooth'], check=True)
        subprocess.run(['sudo', 'systemctl', 'enable', 'bluetooth'], check=True)

        # Use bluetoothctl to connect and trust the device
        commands = [
            'connect {}'.format(mac_address),
            'trust {}'.format(mac_address),
            'exit'
        ]

        for cmd in commands:
            subprocess.run(['bluetoothctl', cmd], check=True)

        print("Bluetooth device connected successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main_pi_mac_address = 'D8:3A:DD:75:85:23'
    connect_bluetooth(main_pi_mac_address)

    # Keep the script running to maintain connection
    while True:
        time.sleep(60)