import socket
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
import binascii
import time
import sqlite3
 
############## SE GENERAN LLAVES CIFRADO RSA-PKCS8 Y SE ENVIA LL.PU POR SOCKET PARA RECIBIR MENSAJE Y DESCIFRAR CON LL.PR #######

#Genera llave privada y publica
private_key = RSA.generate(1024)
public_key = private_key.publickey()
print (private_key)
print (public_key)

#Socket
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 4444
mysocket.bind((host, port))
mysocket.listen(2)
c, addr = mysocket.accept()
encrypt_str = (b"encrypted_message=")


while True:
    #Espera a recibir los datos
    data = c.recv(1024)
    data = data.replace(b"\r\n", b'') #elimina nuevas lineas

    if data == b"Client: OK":
        print("Conectado con el cliente.")
        #time.sleep(2)
        c.send(public_key.exportKey( passphrase=None, pkcs=8))
        print ("Llave pública enviada al cliente...")

    elif encrypt_str in data: #Recibe mensajes cifrados y los descifra.

        data = data.replace(encrypt_str, b'')
        data = binascii.b2a_hex(data)
        print ("Recibido: mensaje cifrado es "+ data.decode())
        decryptor = PKCS1_OAEP.new(private_key)
        print (len(data.decode()))
        if len(data.decode()) == 256:
            decrypted = decryptor.decrypt(bytes.fromhex(data.decode()))
            print ("El mensaje descifrado es:\n " + decrypted.decode())
            c.send(b'Decrypted')
        else:
            continue

    elif data == b"Quit": break

#Parar el servidor
c.send(b"Server stopped\n")
print ("Servidor detenido")
c.close()

###############################################################################################################

############ LUEGO DE DESCIFRAR EL MENSAJE SE GUARDA EN BASE DE DATOS SQLITE ##################################
'''
conn = sqlite3.connect('PBKDF2DATABASE.db')
c = conn.cursor()

def create_table():
 c.execute("CREATE TABLE IF NOT EXISTS HashDB7(PasswordHasheada)")

def data_entry():
  c.execute("INSERT INTO HashDB7 VALUES("+decrypted.decode()+")")
 
  conn.commit()
  c.close()
  conn.close()
 
create_table()
data_entry()

###############################################################################################################
'''