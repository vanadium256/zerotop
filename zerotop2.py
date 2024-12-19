import os
import time
import subprocess
import json
import platform
import psutil
from colorama import init, Fore, Style

init(autoreset=True)

def display_ascii_art():
    ascii_art = r"""
███████╗███████╗██████╗  ██████╗ ████████╗ ██████╗ ██████╗ ██████╗ 
╚══███╔╝██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝██╔═══██╗██╔══██╗╚════██╗
  ███╔╝ █████╗  ██████╔╝██║   ██║   ██║   ██║   ██║██████╔╝ █████╔╝
 ███╔╝  ██╔══╝  ██╔══██╗██║   ██║   ██║   ██║   ██║██╔═══╝ ██╔═══╝ 
███████╗███████╗██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║     ███████╗
╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝     ╚══════╝  
    """
    print(Fore.CYAN + ascii_art)

def get_cpu_info():
    cpu_info = platform.processor()
    return cpu_info if cpu_info else "Sorry, idk."

def system_info():
    print(Fore.YELLOW + "\n=== System Information ===")
    print(f"System Name: {os.uname().sysname}")
    print(f"Kernel Version: {os.uname().release}")
    print(f"CPU Architecture: {os.uname().machine}")
    print(f"CPU: {get_cpu_info()}")
    print(f"Memory: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB")
    print(f"GPU: {os.popen('lspci | grep -i vga').read().strip()}")
    print(Style.RESET_ALL + "==============================")

def cpu_usage():
    print(Fore.GREEN + "\n=== CPU Usage ===")
    print(f"{psutil.cpu_percent(interval=1)}%")

def memory_usage():
    print(Fore.BLUE + "\n=== Memory Usage ===")
    mem = psutil.virtual_memory()
    print(f"{round(mem.used / (1024 ** 3), 2)} GB / {round(mem.total / (1024 ** 3), 2)} GB ({mem.percent}%)")

def disk_usage():
    print(Fore.MAGENTA + "\n=== Disk Usage ===")
    disk = psutil.disk_usage('/')
    print(f"{round(disk.used / (1024 ** 3), 2)} GB / {round(disk.total / (1024 ** 3), 2)} GB ({disk.percent}%)")

def list_processes():
    print(Fore.RED + "\n=== Process List ===")
    try:
        output = subprocess.check_output(["ps", "-eo", "pid,comm,%mem,%cpu"], universal_newlines=True)
        lines = output.strip().split('\n')
        for line in lines[:16]:  
            print(line)
    except Exception as e:
        print(f"Error retrieving process list: {e}")

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def network_connections():
    config = load_config()
    max_connections = config.get("max_connections", 16) 
    print(Fore.YELLOW + "\n=== Network Connections ===")
    connections = psutil.net_connections(kind='inet')
    
    if connections:
        for conn in connections[:max_connections]:
            print(f"PID: {conn.pid}, Local Address: {conn.laddr}, Remote Address: {conn.raddr}, Status: {conn.status}")
    else:
        print("No network connections found.")

def terminate_process(pid):
    try:
        subprocess.run(["kill", str(pid)], check=True) 
        print(Fore.GREEN + f"Process {pid} has been terminated.")
    except subprocess.CalledProcessError:
        print(Fore.RED + f"Error terminating process {pid}: {e}")

def main():
    print("Press 'q' to quit the program at any time.")
    
    while True:
        os.system('clear')  # cls for Windows
        display_ascii_art()  
        system_info()
        cpu_usage()
        memory_usage()
        disk_usage()
        list_processes()
        network_connections()
        print(Style.RESET_ALL + "=========================")

        pid_input = input("Enter PID to terminate (or press Enter to skip): ")
        if pid_input:
            try:
                pid = int(pid_input)
                terminate_process(pid)
            except ValueError:
                print(Fore.RED + "Invalid PID. Please enter a valid number.")

        if input("Press 'q' to quit or any other key to continue: ") == 'q':
            print("Exiting the program...")
            break

        time.sleep(5)

if __name__ == "__main__":
    main()

