#PARTE DEL CLIENTE
import threading
import socket

socket_cliente=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket_cliente.connect(("localhost",9999))





def enviarMensaje():
    aux=1
    while aux!=0:
        mensaje = input("Mensaje a enviar >> ")
    
        socket_cliente.send(mensaje.encode())
    
        if mensaje == "SALIR" or "salir" or "Salir":
            break

        aux=0
    
    print ("DESCONECTADO")    
    socket_cliente.close()

def recibirMensaje():
    try:        
        recibido=socket_cliente.recv(1024).decode()
        if (recibido):
            print("Mensaje Recibido: ")
            print(recibido)
    except:
        pass






enviar=threading.Thread(target=enviarMensaje())
enviar.start
recibir=threading.Thread(target=recibirMensaje())
recibir.start