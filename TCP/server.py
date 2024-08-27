import socket
from threading import Thread
from queue import Queue

BUFFER_SIZE = 12 * 256

class TCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.buffer = Queue(maxsize=12)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        print("Server listening on port", self.port)

        self.client1_conn, _ = self.server_socket.accept()
        print("TCPClient1 connected")

        self.client2_conn, _ = self.server_socket.accept()
        print("TCPClient2 connected")

        Thread(target=self.handle_client1).start()
        Thread(target=self.handle_client2).start()

    def handle_client1(self):
        packet_count = 0
        while True:
            packet = self.client1_conn.recv(256)
            if not packet:
                break
            packet_count += 1
            print(f"Packet {packet_count} received from Client 1 and queued for Client 2.")
            while self.buffer.full():
                pass  # Wait until buffer has space
            self.buffer.put(packet)
            print("Packet sent to Client 2.")

    def handle_client2(self):
        ack_count = 0
        while True:
            if not self.buffer.empty():
                packet = self.buffer.get()
                self.client2_conn.sendall(packet)
                ack_count += 1
                print(f"ACK {str(ack_count).zfill(8)} received from Client 2.")
            else:
                pass


if __name__ == "__main__":
    server = TCPServer('127.0.0.1', 65432)
    server.start_server()

