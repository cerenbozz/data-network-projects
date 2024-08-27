def create_large_file(filename, size_in_kb):
    with open(filename, 'wb') as f:
        f.write(b'a' * size_in_kb * 1024)

if __name__ == "__main__":
    create_large_file('large_file.bin', 101)  #create a file length of 101 KB


# DO NOT RUN THIS CODE BECAUSE YOU ALREADY HAVE large_file.bin