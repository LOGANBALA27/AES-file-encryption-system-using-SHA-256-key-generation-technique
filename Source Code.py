import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
alphabet2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def encrypt(password, encrypting_file, encode=True):
    with open(encrypting_file, 'rb') as fo:
        plaintext = fo.read()
    password_b = bytes(password, 'utf-8')
    key = SHA256.new(password_b).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(plaintext) % AES.block_size  # calculate needed padding
    plaintext += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = IV + encryptor.encrypt(plaintext)  # store the IV at the beginning and encrypt
    with open(encrypting_file + ".enc", 'wb') as fo:
        fo.write(data)
        fo.close()
    return base64.b64encode(data).decode("latin-1") if encode else data

def decrypt(password, decrypting_file, decode=True):
    password_b = bytes(password, 'utf-8')
    with open(decrypting_file, 'rb') as fo:
        ciphertext = fo.read()
    ciphertext_str = base64.b64encode(ciphertext).decode("latin-1") 
    if decode:
        ciphertext_str = base64.b64decode(ciphertext_str.encode("latin-1"))
    key = SHA256.new(password_b).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = ciphertext_str[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(ciphertext_str[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding]  # remove the padding

def ceaser(direction):
  text = input("Type your message:\n").lower()
  shift = int(input("Type the shift number:\n"))
  shift = shift % 26
  encrypted = ""
  if direction == 2:
    shift *= -1
  for i in text:
    if i in alphabet:
      pos = alphabet.index(i)
      newpos = pos + shift
      if (newpos>25): 
        newpos = newpos - 26
      encrypted += alphabet[newpos]
    else :
      encrypted += i
  print(f"The {direction}d message is: \n{encrypted}")


def ceaser_capital(direction):
  text = input("Type your message:\n").upper()
  shift = int(input("Type the shift number:\n"))
  shift = shift % 26
  encrypted = ""
  if direction == 2:
    shift *= -1
  for i in text:
    if i in alphabet2:
      pos = alphabet2.index(i)
      newpos = pos + shift
      if (newpos>25): 
        newpos = newpos - 26
      encrypted += alphabet2[newpos]
    else :
      encrypted += i
  print(f"The {direction}d message is: \n{encrypted}")


choose = int(input("1. Please enter 1 to encrypt file. \n2. Please enter 2 to decrypt file. \n3. Please enter 3 to encrypt or decrypt text.\n"))
if(choose == 1):
    file_name = (input("Enter name of file to encrypt: "))
    my_password = (input("Enter the password: "))
    encrypted = encrypt(my_password, file_name)
    print("The file has been encrypted successfully.")
elif(choose ==2 ):
    file_name1 = (input("Enter name of file to decrypt: "))
    my_password = (input("Enter the password: "))
    decrypted = decrypt(my_password, file_name1)
    with open(file_name1[:-4], 'wb') as fo:
            fo.write(decrypted)
    print("The file has been decrypted successfully.")
elif (choose == 3):
    directions = int(input("Type '1' to encrypt, type '2' to decrypt:\n"))
    if directions == 1 or directions == 2:
     letters = str(input("Enter 'Small' for small letter or Enter 'Capital' for capital letter:\n").lower())
     if letters == 'small' :
      ceaser(directions)
     elif letters == 'capital':
      ceaser_capital(directions)
     else:
      print("Error.")
    else:
     print("Error")
else:
    print("Invalid Number")
