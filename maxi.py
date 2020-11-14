import socket
import os
import sys
import subprocess
import binascii


#P = os.system('python hash-id.py ' + hash)
print('Los archivos pertenecen a los siguientes hashes:\n')
for i in [0,1,2]:
	b=i+1
	b = str(b)
	n= ('Archivo/archivo_'+b)
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
			os.system('hashcat -a 0 -m 0 archivo_'+b+' Archivos/diccionario_1.dict Archivos/diccionario_2.dict -o fileFull --quiet')
			os.system("cat fileFull | " + "sed 's/:/ /g' | " + "awk '{print$2}'" + " > passFile")
		elif i == 1:
			os.system('hashcat -a 0 -m 10 archivo_'+b+' Archivos/diccionario_1.dict Archivos/diccionario_2.dict -o fileFull2 --quiet')
			os.system("cat fileFull2 | " + "sed 's/:/ /g' | " + "awk '{print$3}'" + " >> passFile")
		else:
			os.system('hashcat -a 0 -m 10 archivo_'+b+' Archivos/diccionario_1.dict Archivos/diccionario_2.dict -o fileFull3 --quiet')
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

		os.system('hashcat -a 0 -m 1000 Archivos/archivo_4 Archivos/diccionario_1.dict Archivos/diccionario_2.dict -o fileFull4 --quiet')
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
		os.system('hashcat -a 0 -m 1800 Archivos/archivo_5 Archivos/diccionario_1.dict Archivos/diccionario_2.dict -o fileFull5 --quiet')
		os.system("cat fileFull5 | " + "sed 's/:/ /g' | " + "awk '{print$2}'" + " >> passFile")

		print('archivo 5 = '+a.rstrip('\n'))




#firstFile()



#for line in mylist:
#	print line
#	hashcat = subprocess.check_output(['python','hash-id.py',line])
#file.close()	


#hashcat = subprocess.check_output(['python','hash-id.py','876c190d3994262a39d94a8c677fc386','|','grep -A1 Possible'])

#hashcat = subprocess.check_output(["python","hash-id.py", "876c190d3994262a39d94a8c677fc386", "|", "grep -A1 Possible", "|", "grep -v Hash" "|","awk '{print $2}'"], shell=True)
#command = ['python','hash-id.py','876c190d3994262a39d94a8c677fc386','|','grep -A1 Possible']




#pe = subprocess.call(["grep -A1 Possible"], stdin=hashcat.stdout)
#print (pe)

#P = os.system('python hash-id.py ' + '876c190d3994262a39d94a8c677fc386' + '|' + 'grep -A1 Possible' + '|' 'grep -v Possible')
#output = hashcat.stdout.read()



#grep -A1 Possible | grep -v Possibl
#print output  

#hola = '127.0.0.1'
#port = 8888

#try:
    # crea un socket INET de tipo STREAM
#	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ahora se conecta al servidor web en el puerto 80 (http)
#	s.connect((hola, 4444))
#	s.send(hola)

#except Exception as e:
#	#print "Error qlo"
#	print(sys.exc_value)