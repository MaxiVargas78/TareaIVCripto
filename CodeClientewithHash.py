import socket
import os
import sys
import subprocess
from Crypto.Protocol.KDF import PBKDF2
import binascii
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time
import asyncio


########### CON HashID RECONOCE LOS HASHES Y LUEGO LOS CRACKEA CON HASHCAT, CREANDO UN ARCHIVO CON LAS PASSWORD CRACKEADAS ########

print('Los archivos pertenecen a los siguientes hashes:\n')
for i in [0,1,2]:
	b=i+1
	b = str(b)
	n= ('Archivos/archivo_'+b)
	with open(n) as f:
		hola = f.read().splitlines()
		hash1 = hola[0]

		comilla = "'"
		hash2 = comilla + hash1 + comilla
		command = "python hash-id.py " 
		command2 = hash1 
		command3 = " | grep -A1 Possible | grep -v Hash | awk '{print $2}'"
		command4 = command + command2 + command3
		hashcat = subprocess.Popen(command4,shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		a = hashcat.communicate()[0].decode()
		if i == 0:
			os.system('time hashcat -a 0 -m 0 Archivos/archivo_'+b+' Archivos/diccionario_1.dict Archivos/diccionario_2.dict -o fileFull --quiet')
			os.system("cat fileFull | " + "sed 's/:/ /g' | " + "awk '{print$2}'" + " > passFile")
		elif i == 1:
			os.system('time hashcat -a 0 -m 10 Archivos/archivo_'+b+' Archivos/diccionario_1.dict Archivos/diccionario_2.dict -o fileFull2 --quiet')
			os.system("cat fileFull2 | " + "sed 's/:/ /g' | " + "awk '{print$3}'" + " >> passFile")
		else:
			os.system('time hashcat -a 0 -m 10 Archivos/archivo_'+b+' Archivos/diccionario_1.dict Archivos/diccionario_2.dict -o fileFull3 --quiet')
			os.system("cat fileFull3 | " + "sed 's/:/ /g' | " + "awk '{print$3}'" + " >> passFile")

		print('archivo '+b+ ' = '+a.rstrip('\n'))

with open('Archivos/archivo_4') as f:
		hola = f.read().splitlines()
		hash1 = hola[0]

		comilla = "'"
		hash2 = comilla + hash1 + comilla
		command = "python hash-id.py " 
		command2 = hash1 
		command3 = " | grep -A2 Least| awk 'NR==3' | grep -v Hash | awk '{print $2}'"
		command4 = command + command2 + command3

		hashcat = subprocess.Popen(command4,shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		a = hashcat.communicate()[0].decode()

		os.system('time hashcat -a 0 -m 1000 Archivos/archivo_4 Archivos/diccionario_1.dict Archivos/diccionario_2.dict -o fileFull4 --quiet')
		os.system("cat fileFull4 | " + "sed 's/:/ /g' | " + "awk '{print$2}'" + " >> passFile")

		print('archivo 4 = '+a.rstrip('\n'))

with open('Archivos/archivo_5') as f:
		hola = f.read().splitlines()
		hash1 = hola[1]
		comilla = "'"
		hash2 = comilla + hash1 + comilla
		command = "python hashid.py " 
		command2 = hash2 
		command3 = " | grep -v Analyzing | awk '{print $2 $3}' "
		command4 = command + command2 + command3

		hashcat = subprocess.Popen(command4,shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		a = hashcat.communicate()[0].decode()
		os.system('time hashcat -a 0 -m 1800 Archivos/archivo_5 Archivos/diccionario_1.dict Archivos/diccionario_2.dict -o fileFull5 --quiet')
		os.system("cat fileFull5 | " + "sed 's/:/ /g' | " + "awk '{print$2}'" + " >> passFile")

		print('archivo 5 = '+a.rstrip('\n'))
########################################################################################################################

######### SE HASHEAN LAS PASSWORD CON PBKDF2 Y CREA UN ARCHIVO DONDE GUARDA LAS PASS HASHEADAS ##########################

O = open ('PassNewHash.txt', 'w')
with open('passFile', 'r') as g:
	hola = g.read().splitlines()
	j = 0
	while True:
		if j < len(hola):
			hola1 = hola[j]
			x =  PBKDF2( hola1,'hola', 16, 1000, None)
			y = binascii.b2a_hex(x)
			#print (y.decode())
			O.write(y.decode()+'\n')
			j = j+1
		else:
			break
O.close()
g.close()
#########################################################################################################################


######## MEDIANTE SOCKET SE RECIBE LLAVE PÚBLICA, SE CIFRA EL MENSAJE Y SE ENVÍA AL "SERVIDOR" ##########################

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 4444

x = "passFile"
#x = "PassNewHash.txt" # archivo con pass hasheadas en punto anterior
server.connect((host, port))


#Llama al servidor para confirmar conexion
server.sendall(b"Client: OK")

#Recibe llave publica del servidor
#server_string = server.recv(1024)
server_string = server.recv(1024)


#Remueve caracteres extras
#print (server_string)
#server_string = server_string.replace(b"Llave publica=", b'')
#server_string = server_string.replace(b"\r\n", b'')


#Convierte la cadena en llave
server_public_key = RSA.importKey(server_string)

#Cifra el mensaje y lo envia


with open (x, 'rb') as m:
	encryptor = PKCS1_OAEP.new(server_public_key)
	message = m.read().splitlines() #archivo a enviar
	l = 0
	while True:
		time.sleep(0.5)
		if l < len(message):
			hi = message[l]
			encrypted = encryptor.encrypt(hi)
			print (hi)
			notificacion = b"encrypted_message="
			server.sendall(notificacion + encrypted)
			l=l+1
			print("Mensaje cifrado enviado...")
		else:
			break


#Respuesta del server

server_response = server.recv(2048)
server_response = server_response.replace(b"\r\n", b'')
if server_response == b"Server: OK":
	print ("Servidor descifra mensaje correctamente!")

#LLama al servidor para finalizar conexion
server.sendall(b"Quit")
#print(server.recv(1024)) #Quit server response
print("Sesion finalizada")
server.close()

############################################################################################################################

