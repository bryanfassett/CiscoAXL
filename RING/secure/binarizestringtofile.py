import os
from cryptography.fernet import Fernet

def genkey():
    return Fernet.generate_key()

def binstrtofile(str2bin,filename, key = ""):
    # Generate a crypto key
    if not key == "":
        key = genkey()

    # encrypt str2bin and write to a bin file
    cipher_suite = Fernet(key)
    str2bin = str.encode(str2bin)
    ciphered_text = cipher_suite.encrypt(str2bin)

    # get directory
    dirpath = os.path.dirname(os.path.realpath(__file__))
    filename = f"{dirpath}\{filename}.bin"

    with open(filename, 'wb') as f:  f.write(ciphered_text)
    return key

def binfiletostr(key, filename):
    dirpath = os.path.dirname(os.path.realpath(__file__))
    filename = f"{dirpath}\{filename}.bin"
    with open(filename, 'rb') as f:
        for line in f:
            encryptedpwd = line
        
        print(encryptedpwd)
        cipher_suite = Fernet(key)
        uncipher_str = (cipher_suite.decrypt(encryptedpwd))
        plain_text = bytes(uncipher_str).decode("utf-8") #convert to string
        return plain_text