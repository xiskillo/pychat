#PARTE DEL CLIENTE
import threading
import socket

socket_cliente=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket_cliente.connect(("localhost",9999))





def enviarMensaje():
    aux=4
    while (aux>0):
        mensaje = input("ENVIAR MENSAJE => ")
        print ("\n")
    
        socket_cliente.send(mensaje.encode())
    
        if (mensaje == "SALIR" or "salir" or "Salir"):
            print ("DESCONECTANDO")
            socket_cliente.close()
            break

      
          
        
        aux=aux-1
    
    

def recibirMensaje():
    try:        
        recibido=socket_cliente.recv(1024).decode()
        if (recibido):
            print("Mensaje Recibido: ")
            print(recibido)
    except:
        pass




#recibir=threading.Thread(target=recibirMensaje())
#recibir.start
enviar=threading.Thread(target=enviarMensaje())
enviar.start
