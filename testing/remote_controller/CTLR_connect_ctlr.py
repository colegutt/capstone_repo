# Bluetooth Remote Auto-Connect
import subprocess
import time

def connect_bluetooth(mac_address):
    try:
        # Start Bluetooth service
        subprocess.run(['sudo', 'systemctl', 'start', 'bluetooth'], check=True)
        subprocess.run(['sudo', 'systemctl', 'enable', 'bluetooth'], check=True)

        # Prepare the commands to be run in bluetoothctl
        commands = f"""
        connect {mac_address}
        trust {mac_address}
        exit
        """

        # Use bluetoothctl with input commands
        process = subprocess.Popen(['bluetoothctl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(commands)
        
        if process.returncode == 0:
            print("Bluetooth device connected successfully.")
        else:
            print(f"Error connecting Bluetooth device: {stderr}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main_pi_mac_address = 'D8:3A:DD:75:85:23'
    connect_bluetooth(main_pi_mac_address)

    # Keep the script running to maintain connection
    while True:
        time.sleep(60)
