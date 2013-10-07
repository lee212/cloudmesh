'''simplifing data encryption'''
import os
from hashlib import sha256
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

def pad(data, bs):
    """ Pad data to the given blocksize, PKCS-5 style """
    return data + (bs - len(data) % bs) * chr(bs - len(data) % bs)

def unpad(data):
    """ Remove the padding characters """
    return data[0:-ord(data[-1])]

def keydigest(key):
    """ Easy way to get a 32-bit key """
    return sha256(key).digest()

def encrypt(data, password):
    """
    Encrypts the given data using the password.  

    Returns a concatenation of the initialiation vector and the
    encrypted data, base64 encoded so it can be easily stored as text

    """
    iv = os.urandom(16)
    key = keydigest(password)

    aes = AES.new(key, AES.MODE_CBC, iv)
    cypher = aes.encrypt(pad(data, 16))
    return b64encode(iv + cypher)

def decrypt(data64, password):
    """
    Decrypts the given data using the password.  

    The data should be the base64 encoded encrypted value created by the encrypt function.
    """
    data = b64decode(data64)
    iv = data[:16]
    cypher = data[16:]
    key = keydigest(password)
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(cypher))

if __name__ == "__main__":
    print "Easy to use data encryption functions"

    password_text = 'super secret'
    plain_text = 'Hello, world'
    encrypted_text = encrypt(plain_text, password_text)
    print plain_text, encrypted_text
    decrypted_text = decrypt(encrypted_text, password_text)
    print decrypted_text

    # Generate some password-like strings and verify that encryption/decryption works
    import string, random
    chars = string.letters + string.digits
    for i in range(0,100):
        length = random.randint(8,40)
        testdata = ''.join([random.choice(chars) for _ in range(length)])
        if testdata == decrypt(encrypt(testdata, password_text), password_text):
            print i,
        else:
            print testdata, "failed!"
            break