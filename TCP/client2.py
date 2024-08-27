import socket


def receive_file(server_ip, server_port, output_filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, server_port))
        with open(output_filename, 'wb') as file:
            packet_count = 0
            while True:
                packet = s.recv(256)
                if not packet:
                    break
                if packet == b'TERMINATE':
                    break
                file.write(packet)
                packet_count += 1
                print(f"Received packet {packet_count}")
                s.sendall(b'ACK')
                print("ACK sent to server")


if __name__ == "__main__":
    receive_file('127.0.0.1', 65432, 'received_file.bin')
