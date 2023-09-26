import pywinusb.hid as hid
import time
import psutil
import win32api
import tkinter as tk
from tkinter import scrolledtext

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

def update_usb_devices_text():
    current_hid_devices = hid.HidDeviceFilter().get_devices()
    current_hid_device_serials = {device.serial_number: None for device in current_hid_devices}

    current_usb_drives = get_usb_drives()

    new_hid_devices = [serial for serial in current_hid_device_serials if serial not in all_hid_device_serials]
    new_usb_drives = [drive for drive in current_usb_drives if drive not in all_usb_drives]

    if new_hid_devices or new_usb_drives:
        result_text.delete(1.0, tk.END)  # Clear the previous content
        result_text.insert(tk.END, "USB Devices Added:\n")
        result_text.insert(tk.END, "=" * 50 + "\n")
        for serial in new_hid_devices:
            result_text.insert(tk.END, f"HID Device Serial Number: {serial}\n")
            result_text.insert(tk.END, "-" * 50 + "\n")

        for drive in new_usb_drives:
            result_text.insert(tk.END, f"Mass Storage Device: {drive}\n")
            label = get_volume_name(drive)
            result_text.insert(tk.END, f"Volume Name: {label}\n")
            result_text.insert(tk.END, "-" * 50 + "\n")

    all_hid_device_serials.clear()
    all_hid_device_serials.update(current_hid_device_serials)
    all_usb_drives.clear()
    all_usb_drives.extend(current_usb_drives)

    # Schedule the function to run again after 2 seconds
    root.after(2000, update_usb_devices_text)

def main():
    global root, result_text, all_hid_device_serials, all_usb_drives
    root = tk.Tk()
    root.title("USB Device Monitor")

    result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
    result_text.pack()

    all_hid_device_serials = set()
    all_usb_drives = []

    update_usb_devices_text()

    root.mainloop()

if __name__ == "__main__":
    main()
