import pywinusb.hid as hid
import time
import psutil
import subprocess
import os
import win32api
import keyboard

def get_usb_drives():
    drives = []
    for partition in psutil.disk_partitions():
        if 'removable' in partition.opts or 'cdrom' in partition.opts:
            drives.append(partition.device)
    return drives

def get_volume_name(drive):
    try:
        volume_name = win32api.GetVolumeInformation(drive)[0]
        return volume_name   
    except Exception as e:
        print(f"Error getting volume name for {drive}: {str(e)}")
        return None

def main():
    # Set up USB device event handler
    all_hid_devices = hid.HidDeviceFilter().get_devices()
    all_hid_device_serials = {device.serial_number: None for device in all_hid_devices}

    all_usb_drives = get_usb_drives()
    
    while True:
        current_hid_devices = hid.HidDeviceFilter().get_devices()
        current_hid_device_serials = {device.serial_number: None for device in current_hid_devices}

        current_usb_drives = get_usb_drives()

        new_hid_devices = [serial for serial in current_hid_device_serials if serial not in all_hid_device_serials]
        new_usb_drives = [drive for drive in current_usb_drives if drive not in all_usb_drives]

        if new_hid_devices or new_usb_drives:
            print("USB Devices Added:")
            print("=" * 50)
            for serial in new_hid_devices:
                print(f"HID Device Serial Number: {serial}")
                print("-" * 50)
                # block_common_keys()  # Call the function to block keys
                subprocess.call(["python", "ActDetect.py", f"{serial}"])
                subprocess.call(["python", "Pattern.py"])

            for drive in new_usb_drives:
                print(f"Mass Storage Device: {drive}")
                label = get_volume_name(drive)
                print(f"Volume Name: {label}")
                print("-" * 50)
                # block_common_keys()  # Call the function to block keys
                subprocess.call(["python", "ActDetect.py", f"{label}"])
                subprocess.call(["python", "Pattern.py"])

        all_hid_device_serials = current_hid_device_serials
        all_usb_drives = current_usb_drives
        time.sleep(2)

if __name__ == "__main__":
    main()
