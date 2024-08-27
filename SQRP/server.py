import socket
import struct

class SQRPMessage:
    def __init__(self, message_type, query_type, message_id, timestamp, status_code, body):
        self.message_type = message_type
        self.query_type = query_type
        self.message_id = message_id
        self.timestamp = timestamp
        self.status_code = status_code
        self.body = body

    def pack(self):
        if self.body:
            body_length = len(self.body.encode('ascii'))
        else:
            body_length = 0

        header = (self.message_type << 63) | (self.query_type << 61) | (self.message_id << 56) | (
                    self.status_code << 21) | (body_length << 8)
        return struct.pack("!QIHBBHH256s", header, self.timestamp, body_length, 0, 0, 0, 0, self.body.encode('ascii'))

    @classmethod
    def unpack(cls, data):
        unpacked_data = struct.unpack("!QIHBBHH256s", data)
        message_type = (unpacked_data[0] >> 63) & 0x1
        query_type = (unpacked_data[0] >> 61) & 0x3
        message_id = (unpacked_data[0] >> 56) & 0x1F
        status_code = (unpacked_data[0] >> 21) & 0x7
        body_length = (unpacked_data[0] >> 8) & 0xFF
        timestamp = unpacked_data[1]
        body = unpacked_data[6][:body_length].decode('ascii')
        return cls(message_type, query_type, message_id, timestamp, status_code, body)

class SQRPProtocolServer:
    def __init__(self):
        self.directory_exists = False
        self.file_exists = False
        self.file_changed = False
        self.directory = ""
        self.filename = ""
        self.timestamp = 0
        self.extension = ""

    def process_query(self, query_type, body):
        response_status_code = None
        response_body = None

        if query_type == 0:
            self.directory = body
            if self.directory_exists:
                response_status_code = 0b000  # EXIST
            else:
                response_status_code = 0b001  # NOT EXIST

        elif query_type == 1:
            self.filename = body
            if self.directory_exists:
                if self.file_exists:
                    response_status_code = 0b000  # EXIST
                else:
                    response_status_code = 0b001  # NOT EXIST
            else:
                response_status_code = 0b110  # DIRECTORY NEEDED

        elif query_type == 2:
            if self.directory_exists and self.file_exists:
                if self.file_changed:
                    response_status_code = 0b010  # CHANGED
                    response_body = str(self.timestamp)
                else:
                    response_status_code = 0b011  # NOT CHANGED
                    response_body = str(self.timestamp)
            else:
                response_status_code = 0b001  # NOT EXIST

        elif query_type == 3:
            if self.directory_exists:
                if self.file_exists and self.file_changed:
                    response_status_code = 0b111  # SUCCESS
                    response_body = ','.join([self.filename, str(self.timestamp)])
                else:
                    response_status_code = 0b001  # NOT EXIST
            else:
                response_status_code = 0b110  # DIRECTORY NEEDED

        return response_status_code, response_body

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 31369))
    server_socket.listen(1)

    print("Server is listening...")

    while True:
        connection, client_address = server_socket.accept()
        print("Connection from:", client_address)

        try:
            data = connection.recv(1024)
            if data:
                print("Received data:", data)
                unpacked_message = SQRPMessage.unpack(data)
                print("Unpacked message:", unpacked_message.__dict__)

                response_status_code, response_body = server.process_query(unpacked_message.query_type, unpacked_message.body)

                response_message = SQRPMessage(1, unpacked_message.query_type, unpacked_message.message_id, unpacked_message.timestamp, response_status_code, response_body)
                packed_response = response_message.pack()

                print("Sending response:", packed_response)
                connection.sendall(packed_response)

        finally:
            connection.close()

if __name__ == "__main__":
    server = SQRPProtocolServer()
    start_server()