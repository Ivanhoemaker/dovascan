import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

def scan_ports(ip, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        s.close()
    return open_ports

def start_scan():
    ip = ip_entry.get()
    try:
        start_port = int(start_port_entry.get())
        end_port = int(end_port_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid port numbers. THANK YOU.")
        return

    output_text.delete(1.0, tk.END)
    if not ip or start_port < 1 or end_port > 65535 or start_port > end_port:
        messagebox.showerror("Input Error", "Please enter a CORRECT IP address OR port range.")
        return
    
    output_text.insert(tk.END, f"Scanning {ip} from port {start_port} to {end_port}... Please wait")
    thread = threading.Thread(target=run_scan, args=(ip, start_port, end_port))
    thread.start()

def run_scan(ip, start_port, end_port):
    open_ports = scan_ports(ip, start_port, end_port)
    output_text.insert(tk.END, "n")
    if open_ports:
        output_text.insert(tk.END, f"Open ports: {', '.join(map(str, open_ports))}n")
    else:
        output_text.insert(tk.END, "Sorry, could not find open ports; host seems down.")

root = tk.Tk()
root.title("DOVASCAN")
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

tk.Label(root, text="Insert IP Address:", bg="#32CD32").grid(row=0, column=0, sticky="ew")
ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1, sticky="ew")

tk.Label(root, text="Start Port:", bg="#90EE90").grid(row=1, column=0, sticky="ew")
start_port_entry = tk.Entry(root)
start_port_entry.grid(row=1, column=1, sticky="ew")

tk.Label(root, text="End Port:", bg="#d0e7f9").grid(row=2, column=0, sticky="ew")
end_port_entry = tk.Entry(root)
end_port_entry.grid(row=2, column=1, sticky="ew")
scan_button = tk.Button(root, text="SCAN", command=start_scan, bg="#32CD32", fg="white")
scan_button.grid(row=3, columnspan=2, sticky="ew")

output_text = scrolledtext.ScrolledText(root, width=60, height=20, bg="#32CD32")
output_text.grid(row=4, columnspan=2, sticky="nsew")

root.mainloop()
