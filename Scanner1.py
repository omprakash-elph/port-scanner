import argparse
import socket
import threading
import time
from queue import Queue, Empty
from colorama import Fore, init

init(autoreset=True)

# ----------------------------
# Argument Parser
# ----------------------------
parser = argparse.ArgumentParser(description="Multithreaded Python Port Scanner")
parser.add_argument("-t", "--target", required=True, help="Target IP address")
parser.add_argument("-p", "--ports", required=True, help="Port range (example: 1-1000)")
parser.add_argument("-T", "--threads", default=100, type=int, help="Number of threads")
parser.add_argument("-o", "--output", default="scan_results.txt", help="Output file")
args = parser.parse_args()

target = args.target
start_port, end_port = map(int, args.ports.split("-"))
thread_count = args.threads
output_file = args.output

# ----------------------------
# Resolve hostname once
# ----------------------------
try:
    resolved_ip = socket.gethostbyname(target)
except socket.gaierror:
    print(Fore.RED + f"[!] Could not resolve host: {target}")
    exit(1)

# ----------------------------
# Setup
# ----------------------------
port_queue = Queue()
lock = threading.Lock()
start_time = time.time()

print(Fore.CYAN + f"\nScanning target: {target} ({resolved_ip})")
print(Fore.CYAN + f"Port range: {start_port}-{end_port}")
print(Fore.CYAN + f"Threads: {thread_count}\n")

# ----------------------------
# Port Scan Function
# ----------------------------
def scan_port(file_handle):
    while True:
        try:
            port = port_queue.get(timeout=1)  # Avoids empty() race condition
        except Empty:
            break

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex((resolved_ip, port)) == 0:
                    try:
                        service = socket.getservbyport(port, "tcp")
                    except OSError:
                        service = "unknown"

                    output = f"[+] Port {port:<5} ({service:<15}) OPEN"

                    # Banner grabbing
                    banner = ""
                    try:
                        s.send(b"HEAD / HTTP/1.0\r\n\r\n")  # Prompt a response
                        banner = s.recv(1024).decode(errors="ignore").strip()
                    except Exception:
                        pass

                    with lock:
                        print(Fore.GREEN + output)
                        file_handle.write(output + "\n")
                        if banner:
                            banner_line = f"    Banner: {banner[:100]}"  # Truncate long banners
                            print(Fore.YELLOW + banner_line)
                            file_handle.write(banner_line + "\n")
        except Exception as e:
            with lock:
                print(Fore.RED + f"[!] Error on port {port}: {e}")
        finally:
            port_queue.task_done()

# ----------------------------
# Fill Queue & Run
# ----------------------------
for port in range(start_port, end_port + 1):
    port_queue.put(port)

with open(output_file, "w") as results_file:
    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=scan_port, args=(results_file,), daemon=True)
        t.start()
        threads.append(t)

    port_queue.join()  # Cleaner than joining threads directly

end_time = time.time()
print(Fore.CYAN + "\nScan Complete.")
print(Fore.YELLOW + f"Results saved to: {output_file}")
print(Fore.MAGENTA + f"Time elapsed: {round(end_time - start_time, 2)}s")
