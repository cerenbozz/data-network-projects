import struct
import datetime
import os
import time


EXIST = 0b000
NOT_EXIST = 0b001
DIRECTORY_NEEDED = 0b110
CHANGED = 0b010
NOT_CHANGED = 0b011
SUCCESS = 0b111


def pack_header(message_type, query_type, message_id, timestamp, status_code, body_length):
    header = (message_type << 63) | (query_type << 61) | (message_id << 56) | (timestamp << 24) | (status_code << 21) | body_length
    return struct.pack("!Q", header)


def print_response(response):
    header = int.from_bytes(response[0], byteorder='big')
    print("\nResponse Header Hex:", hex(header))
    print("Response Message ID:", response[1])
    print("Message Type:", (header >> 63) & 0b1)
    print("Query Type:", (header >> 61) & 0b11)
    print("Status Name:", get_status_name((header >> 21) & 0b111))
    print("Response Body:", response[2])
    print("Response Timestamp:", datetime.datetime.fromtimestamp(response[3]))


def get_status_name(status_code):
    status_names = {
        EXIST: "EXIST",
        NOT_EXIST: "NOT EXIST",
        DIRECTORY_NEEDED: "DIRECTORY NEEDED",
        CHANGED: "CHANGED",
        NOT_CHANGED: "NOT CHANGED",
        SUCCESS: "SUCCESS"
    }
    return status_names.get(status_code, "UNKNOWN")


print("SQRP 1.1 Client Started!")


query_type = int(input("Enter query type (0/1/2/3): "))


leased_ids = set()


def lease_message_id(message_id):
    if message_id not in leased_ids:
        leased_ids.add(message_id)
        return True
    else:
        return False


if query_type == 0:
    directory_path = input("Enter directory path: ")
    if os.path.exists(directory_path):
        status_code = EXIST
    else:
        status_code = NOT_EXIST
    header = pack_header(1, 0, 0, 0, status_code, 0)
    print_response((header, 0, "", 0))

elif query_type == 1:
    directory_path = input("Enter directory path: ")
    if os.path.exists(directory_path):
        status_code = EXIST
        file_name = input("Enter file name: ")
        if os.path.exists(os.path.join(directory_path, file_name)):
            status_code = EXIST
        else:
            status_code = NOT_EXIST
    else:
        status_code = DIRECTORY_NEEDED
    header = pack_header(1, 1, 0, 0, status_code, 0)
    print_response((header, 0, "", 0))

elif query_type == 2:
    directory_path = input("Enter directory path: ")
    if os.path.exists(directory_path):
        file_name = input("Enter file name: ")
        if os.path.exists(os.path.join(directory_path, file_name)):
            modification_time = os.path.getmtime(os.path.join(directory_path, file_name))
            status_code = CHANGED
        else:
            status_code = NOT_EXIST
    else:
        status_code = NOT_EXIST
    header = pack_header(1, 2, 0, 0, status_code, 0)
    print_response((header, 0, "", 0))

elif query_type == 3:
    directory_path = input("Enter directory path: ")
    if os.path.exists(directory_path):
        extension = input("Enter file extension: ")
        timestamp = int(time.time())
        status_code = SUCCESS
        file_name = os.path.basename(directory_path)


        response_body = f"{file_name}-{datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')}"
    else:
        status_code = DIRECTORY_NEEDED
        response_body = ""
    header = pack_header(1, 3, 0, 0, status_code, len(response_body))
    print_response((header, 0, response_body, timestamp))

else:
    print("Invalid query type. Please enter a valid query type.")