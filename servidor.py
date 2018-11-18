#PARTE DEL SERVIDOR
import socket
import threading
import random


#HAZ QUE ESCRIBA LA HORA DEL MENSAJE

x=open("pepe",'a')
x.write("RAYYY")
x.close()

#CONTROLARÁ EL CIERRE DEL SERVIDOR (EN EL MENU QUE SE PUEDA ACCEDER CON PERMISO DE ADMIN EN CUALQUIER CLIENTE))
STOP=1

socket_servidor=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket_servidor.bind(("localhost",9999))
socket_servidor.listen(10)
id_cliente=1

mutex=threading.Lock()

aleatorio=random.randint(1,10)
aux=3

def juego(seleccion):
    a=int(seleccion)
    b=aleatorio
    print ("JUEGO AZAROSO\n")
    
    if (a==b):
        print("ACERTASTE, EL NUMERO: {} ERA EL GANADOR".format(aleatorio))
        return True
    else:
        print("DIFERENTES")


def añadirLog(texto):
    f=open("C:\log.txt", 'w')
    f.write(texto)
    f.close

class Cliente (threading.Thread):
    def __init__(self,socket_cliente, ip_cliente, puerto_cliente, id_cliente):
        threading.Thread.__init__(self)
        self.sc=socket_cliente
        self.ip_cliente=ip_cliente
        self.puerto_cliente=puerto_cliente
        self.id_cliente=id_cliente

    def run(self): 
        print ("***BIENVENIDO CLIENTE: '{}' AL PRGRAMA PyChat & GAME***\n".format(self.id_cliente))
        print ("Si quieres jugar a 'Adivinar Numero' escribe JUGAR")
        continuar=True
        self.sc.send("BIENVENIDOS".encode())
        while continuar:
            peticion=self.sc.recv(1024).decode()
            
            
            print ("Identificador del Cliente: "+str(self.id_cliente)+ "IP del cliente: " + str(self.ip_cliente)+ " envio un mensaje")
            print ("mensaje recibido del cliente: ", peticion)
            mutex.acquire()
            if (peticion=="JUGAR"):
                print("ESCRIBE UN NUMERO DEL 1 al 10: ")
                
                seleccion=self.sc.recv(1024).decode()
                
                if(juego(seleccion)):
                    print ("EL CLIENTE {} ES EL GANADOR".format(self.id_cliente))
            mutex.release()   

            mutex.acquire()
            añadirLog(peticion)
            mutex.release()

            #self.sc.send("RECIBIDO".encode())

            if (peticion=="SALIR" or peticion=="salir"):
                self.sc.close()
                continuar=False

        


            


while 1:
    socket_cliente, ((ip_cliente,puerto_cliente))= socket_servidor.accept()
    
    hilo=Cliente(socket_cliente,ip_cliente,puerto_cliente,id_cliente)
    hilo.start()
    id_cliente=id_cliente+1

    
    #print ("conectado "+str(datos_cliente))
   # mensaje=socket_cliente.recv(1024).decode()
    #print ("mensaje recibido del cliente: ", mensaje)

    

    socket_servidor.close

