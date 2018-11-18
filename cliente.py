#PARTE DEL CLIENTE
import threading
import socket

socket_cliente=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket_cliente.connect(("localhost",9999))





def enviarMensaje():

        while True:
                mensaje = input("ENVIAR MENSAJE => ")
                print ("\n")    
                socket_cliente.send(mensaje.encode())
    
                if (mensaje == "SALIR" or mensaje == "Salir" or mensaje == "salir"):
                        print ("DESCONECTANDO")
                        socket_cliente.close()
                        break
        

      
          
        
    

def recibirMensaje():
    try:        
        recibido=socket_cliente.recv(1024).decode()
        if (recibido):
            print("Mensaje Recibido: ")
            print(recibido)
    except:
        pass





enviar=threading.Thread(target=enviarMensaje())
enviar.start()

#recibir=threading.Thread(target=recibirMensaje())
#recibir.start()
