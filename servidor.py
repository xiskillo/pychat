#PARTE DEL SERVIDOR
import socket
import threading


print ("hola")

#CONTROLARÁ EL CIERRE DEL SERVIDOR (EN EL MENU QUE SE PUEDA ACCEDER CON PERMISO DE ADMIN EN CUALQUIER CLIENTE))
STOP=1

socket_servidor=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket_servidor.bind(("localhost",9999))
socket_servidor.listen(1)
codigo_cliente=1

mutex=threading.Lock



class Cliente (threading.Thread):
    def __init__(self,socket_cliente, datos_cliente, id_cliente):
        threading.Thread.__init__(self)
        self.socket_cliente=socket_cliente
        self.datos_cliente=datos_cliente
        self.codigo_cliente=id_cliente

    def __run__(self): 
        continuar=True
        self.socket_cliente.send("BIENVENIDOS".encode())
        while 1:
            peticion=self.socket_cliente.recv(1024).decode()
            print ("Cliente "+str(self.codigo_cliente)+str(self.datos_cliente)+ " envio un mensaje")
            print  (peticion)
            self.socket_cliente.send("RECIBIDO".encode())

            if (peticion=="SALIR" or peticion=="salir"):
                socket_cliente.close()
                continuar=False

            


while 1:
    socket_cliente, datos_cliente= socket_servidor.accept()
    print ("conectado "+str(datos_cliente))
    hilo=Cliente(socket_cliente,datos_cliente,codigo_cliente)
    hilo.start
    codigo_cliente=codigo_cliente+1

    
    
    

