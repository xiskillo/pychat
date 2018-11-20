import socket, threading, os,time,random,webbrowser
from datetime import datetime


#DEFINO UN CANDADO PARA GESTIONAR LA EXCLUSION MUTUA
mutexUtilidades=threading.Lock()

#INICIALIZO UN SEMAFORO PARA EVITAR LAS CONEXIONES SIMULTANEAS HASTA UN LIMITE
semaforo=threading.Semaphore(10)

#EL NUMERO ALEATORIO NECESARIO EN EL JUEGO AZAROSO ES NECESARIO QUE ESTE CREADO FUERA DEL HILO A REPLICAR PARA QUE NO CAMBIE DE VALOR
aleatorio=random.randint(1,10)

#PARA QUE EL LOG PUEDA SER ACCEDIDO DESDE DIFERENTES HILOS ES NECESARIO QUE ESTE FUERA DE LA CLASE HEREDADA DE THREAD
def añadirLog(texto,cliente):
    f=open("log_utilidades.txt", 'a')
    reloj=time.strftime("%H:%M:%S")
    calendario=time.strftime("%d/%m/%y")
    log=calendario + " " + reloj + " Cliente "+ str(cliente) + ": " + texto + "\n"
    f.write(log)
    f.close

#CLASES A HEREDAR DE THREAD DONDE SE CREARA EL MULTIPROCESO PARA CONEXIONES SIMULTANEAS
class Cliente(threading.Thread):
    global clientes
    global mutex
    global logFile

    def __init__(self, soc, datos, id):
        super().__init__()
        self.socket = soc
        self.datos = datos
        self.id = id
        self.name = ""

    def __str__(self):
        return "Client '{}' with ID {}".format(self.datos, self.id)

    # Decidí implementar esta función, ya que evitaría repetir código en el método run(), tanto para 
    # "anunciar" que alguien se unió o abandonó el chat, como para hacer broadcast de los mensajes 
    # a los demás clientes. De esta manera, el código quedaría más organizado y , de ser necesario algún cambio,
    # tan solo tendría que cambiar la lógica en esta función en lugar de en varias partes del método run().
    def retransmision(self, msg):
        for c in clientes:
            if self.id != c.id:
                c.socket.send("{} {}".format(self.name, msg).encode())

    def logging(self, msg):
        with open(logFile, 'a') as file:
            file.write("{} ({})\n".format(msg, datetime.now().strftime("%X")))

    def run(self):
        print("{} connected".format(self))
        self.logging("{} connected".format(self))

        self.socket.send("You joined the chat room with {} ID\nType 'quit' to leave the room\n\
Also, write an alias you want to use in chat room".format(self.id).encode())
        self.name = self.socket.recv(1024).decode()
        self.logging("{} is using '{}' alias".format(self, self.name))
        self.socket.send("Welcome, {}".format(self.name).encode())
        self.retransmision("joined the room")
        self.logging("{} joined the room".format(self.name))
        
        while True: 
            incomingMssg = self.socket.recv(1024).decode()
            if incomingMssg.lower() != "quit":
                self.logging("Message by {} : '{}'".format(self.name, incomingMssg))
                self.retransmision("wrote: {}".format(incomingMssg))

            else:
                self.logging("{} has disconnected".format(self.name))
                self.socket.send("You have been successfully disconnected".encode())

                mutex.acquire()
                for c in clientes[:]:
                    if self.id == c.id:
                        clientes.remove(c)
                    else:
                        pass
                # mutex.release()

                self.retransmision("has disconnected")
                mutex.release()
                self.socket.close()
                break

class ClienteUtilidades (threading.Thread):
    def __init__(self,socket_cliente, ip_cliente, puerto_cliente, id_cliente):
        threading.Thread.__init__(self)
        self.sc=socket_cliente
        self.ip_cliente=ip_cliente
        self.puerto_cliente=puerto_cliente
        self.id_cliente=id_cliente
    
    def navegar(self):
        print("SE RECIBIRÁ UNA DIRECCIÓN WEB") 
        #SE ESPERA OTRO MENSAJE DE ENTRADA CON LA DIRECCION WEB               
        seleccion=self.sc.recv(1024).decode()                
        webbrowser.open_new(seleccion)    

    def juego(self,seleccion):
        a=int(seleccion)
        b=aleatorio
        print ("JUEGO AZAROSO\n")
        print("SE ESCRIBIRÁ UN NUMERO DEL 1 al 10: ")
        
        if (a==b):
            print("ACERTASTE, EL NUMERO: {} ERA EL GANADOR".format(aleatorio))
            return True
        else:
            if(a<b):
                print("EL NUMERO QUE SE BUSCA ES MAYOR")
            if(a>b):
                print("EL NUMERO QUE SE BUSCA ES MENOR")

    def run(self):
        semaforo.acquire() 
        print ("***BIENVENIDO CLIENTE: '{}' \n".format(self.id_cliente))
        print ("Si quieres jugar a 'Azaroso' escribe 'Jugar'\n")
        print ("Si quieres abrir una WEB escribe 'Navegar'\n")
        continuar=True
        self.sc.send("BIENVENIDO\n".encode())

        while continuar:
            peticion=self.sc.recv(1024).decode()
            
            
            print ("Identificador del Cliente: "+str(self.id_cliente))
            print ("IP del cliente: " + str(self.ip_cliente)+ " Puerto del Cliente: {}".format(str(self.puerto_cliente)))
            print ("MENSAJE RECIBIDO: {}\n".format(peticion))

            #PARA JUGAR
            mutexUtilidades.acquire()
            if (peticion.lower()=="jugar"):
                                
                seleccion=self.sc.recv(1024).decode()
                
                if(self.juego(seleccion)):
                    print ("EL CLIENTE {} ES EL GANADOR".format(self.id_cliente))
                    self.sc.send("¡ACERTASTE EL NÚMERO!".encode())
                else:
                    self.sc.send("¡FALLASTE, JUEGA DE NUEVO!".encode())

            mutexUtilidades.release() 

            #PARA ABRIR UNA WEB
            
            mutexUtilidades.acquire()
            if (peticion.lower()=="navegar"):
                self.navegar()            
            mutexUtilidades.release()  

            mutexUtilidades.acquire()
            if (peticion.lower()=="stop"):
                continuar=False         
            mutexUtilidades.release()  


            #SE ESCRIBIRAN LOS LOGS
            mutexUtilidades.acquire()
            añadirLog(peticion,id_cliente)
            mutexUtilidades.release()       
            
            

            if (peticion.lower()=="salir"):
                self.sc.close()
                semaforo.release()
                continuar=False
        semaforo.release()






if __name__ == "__main__":
    print ("\n\n***BIENVENIDO CLIENTE AL PROGRAMA PyChat & GAME & WEB***\n\n")
    print ("Introduce que tipo de servidor quieres lanzar")
    print ("1-Servidor de Chat Global")
    print ("2-Servidor de Utilidades & Juego")
    print ("3-Salir")
    opcion=input ("Selecciona una opción numérica: ")

    if(opcion=="1"):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("", 9999))
        server.listen(10)
        clientes = []
        cont = 0
        logFile = "log_chat.txt"
        mutex = threading.Lock()
        id = 1
        print("Waiting Clients\n")

        while cont < 10:
            # Chat para diez personas, pero podríamos incrementar el contador, permitiendo más usuarios simultáneos
            soc, datos = server.accept()

            c = Cliente(soc, datos, id)
            clientes.append(c)
            c.start()
            id += 1
            cont += 1

        for c in clientes:
            while c.isAlive():
                pass

        server.close()
    
    if (opcion=="2"):
        #DEFINICIONES NECESARIAS PARA LA CONECTIVIDAD

        server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind(("",9999))
        server.listen(10)
        id_cliente=1
        print("Esperando Clientes")

        while 1:
            socket_cliente, ((ip_cliente,puerto_cliente))= server.accept()            
            
            hilo=ClienteUtilidades(socket_cliente,ip_cliente,puerto_cliente,id_cliente)
            hilo.start()           

            id_cliente=id_cliente+1    

            server.close



    if (opcion=="3"):
        print("Hasta más ver")

        



