#PARTE DEL SERVIDOR
import socket
import threading


print ("***BIENVENIDO AL PRGRAMA PyChat***")

#CONTROLARÁ EL CIERRE DEL SERVIDOR (EN EL MENU QUE SE PUEDA ACCEDER CON PERMISO DE ADMIN EN CUALQUIER CLIENTE))
STOP=1

socket_servidor=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket_servidor.bind(("localhost",9999))
socket_servidor.listen(10)
id_cliente=1

mutex=threading.Lock()



class Cliente (threading.Thread):
    def __init__(self,socket_cliente, ip_cliente, puerto_cliente, id_cliente):
        threading.Thread.__init__(self)
        self.sc=socket_cliente
        self.ip_cliente=ip_cliente
        self.puerto_cliente=puerto_cliente
        self.id_cliente=id_cliente

    def __run__(self): 
        continuar=True
        self.sc.send("BIENVENIDOS".encode())
        while continuar:
            peticion=self.sc.recv(1024).decode()
            mensaje=self.sc.recv(1024).decode()
            print ("mensaje recibido del cliente: ", mensaje)
            print ("IP del Cliente: "+str(self.id_cliente)+str(self.ip_cliente)+ " envio un mensaje")
            print  (peticion)

            mutex.acquire()
            self.añadirLog(peticion)
            mutex.release()

            self.sc.send("RECIBIDO".encode())

            if (peticion=="SALIR" or peticion=="salir"):
                self.sc.close()
                continuar=False

    def añadirLog(self,texto):
        
        f=open("log.txt", "a", encoding="utf8")
        f.write(texto)
        f.close
        


            


while 1:
    socket_cliente, ((ip_cliente,puerto_cliente))= socket_servidor.accept()
    
    hilo=Cliente(socket_cliente,ip_cliente,puerto_cliente,id_cliente)
    hilo.start
    id_cliente=id_cliente+1

    
    #print ("conectado "+str(datos_cliente))
   # mensaje=socket_cliente.recv(1024).decode()
    #print ("mensaje recibido del cliente: ", mensaje)

    

    socket_servidor.close

