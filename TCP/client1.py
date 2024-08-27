import socket
import os


def send_file(filename, server_ip, server_port):
    file_size = os.path.getsize(filename)
    print(f"{filename} length of file: {file_size} byte")
    with open(filename, 'rb') as file:
        data = file.read()

    packets = [data[i:i + 256] for i in range(0, len(data), 256)]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, server_port))
        for i, packet in enumerate(packets, 1):
            s.sendall(packet)
            print(f"Sent packet {i}/{len(packets)}")


if __name__ == "__main__":
    send_file('large_file.bin', '127.0.0.1', 65432)
