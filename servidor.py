#PARTE DEL SERVIDOR
import socket
import threading


print ("***BIENVENIDO AL PRGRAMA PyChat***")

#CONTROLARÁ EL CIERRE DEL SERVIDOR (EN EL MENU QUE SE PUEDA ACCEDER CON PERMISO DE ADMIN EN CUALQUIER CLIENTE))
STOP=1

socket_servidor=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket_servidor.bind(("localhost",9999))
socket_servidor.listen(1)
id_cliente=1

mutex=threading.Lock()



class Cliente (threading.Thread):
    def __init__(self,socket_cliente, datos_cliente, id_cliente):
        threading.Thread.__init__(self)
        self.socket_cliente=socket_cliente
        self.datos_cliente=datos_cliente
        self.id_cliente=id_cliente

    def __run__(self): 
        continuar=True
        self.socket_cliente.send("BIENVENIDOS".encode())
        while continuar:
            peticion=self.socket_cliente.recv(1024).decode()
            mensaje=socket_cliente.recv(1024).decode()
            print ("mensaje recibido del cliente: ", mensaje)
            print ("Cliente "+str(self.codigo_cliente)+str(self.datos_cliente)+ " envio un mensaje")
            print  (peticion)

            mutex.acquire()
            self.añadirLog(peticion)
            mutex.release()

            self.socket_cliente.send("RECIBIDO".encode())

            if (peticion=="SALIR" or peticion=="salir"):
                socket_cliente.close()
                continuar=False

    def añadirLog(self,texto):
        
        f=open("log.txt", "a", encoding="utf8")
        f.write(texto)
        f.close
        


            


while 1:
    socket_cliente, datos_cliente= socket_servidor.accept()
    print ("conectado "+str(datos_cliente))
    hilo=Cliente(socket_cliente,datos_cliente,id_cliente)
    hilo.start
    id_cliente=id_cliente+1

    
    
    mensaje=socket_cliente.recv(1024).decode()
    print ("mensaje recibido del cliente: ", mensaje)

    

    socket_servidor.close

