# servidor.py (modelo cliente-servidor)
import sys 
import socket
import select
import signal

# Creacion del socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def error():
    server_socket.close()
    sys.exit(-1)

def signal_handler(signal, frame):
    server_socket.close()
    sys.exit(0)

#Funcion de reenvio a todos los clientes
def broadcast (sock, message):
    #No se envia el mensaje al creador del mensaje
    for socket in listaSocks:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                #Si el usuario no esta se finaliza el archivo
                socket.close()
                listaSocks.remove(socket)
def main():
    # CONTROL DE ARGUMENTOS
    if len(sys.argv) != 2:
        print("ERROR: Numero de argumentos incorrecto.")
	print("Uso: python servidor.py [Port_server]")
        error()
        
    portServer = int(sys.argv[1])

    addr = ('', portServer)
    print("Iniciando server %s --> puerto: %s" %addr)
    # Enlace del socket y puerto
    server_socket.bind(addr)
    # Escucha del socket (Hasta 10 conex)
    server_socket.listen(10)
    print("Socket enlazado correctamente\n")
    global listaSocks
    listaSocks = []
    listaSocks.append(server_socket)
    datos = []

    print("##### LOG SERVER CLIENTE-SERVIDOR #####")
    
    while 1:
        signal.signal(signal.SIGINT, signal_handler)
        read_sockets,write_sockets,error_sockets = select.select(listaSocks,[],[])
 
        for sock in read_sockets:
            # nueva conexion
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                listaSocks.append(sockfd)
                print ("CLIENTE (%s, %s) CONECTADO" %addr)
                 
                broadcast(sockfd, "[%s:%s] ha entrado en la sala\n" %addr)
             
            else: # Si recibimos msg de un cliente
                try:
                    data = sock.recv(4096)
                    if data: #enviamos al resto de clientes
                        broadcast(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)                 
                except:
                    broadcast(sock, "CLIENTE (%s, %s) DESCONECTADO" %addr)
                    print "CLIENTE (%s, %s) DESCONECTADO" %addr
                    sock.close()
                    listaSocks.remove(sock)
                    continue
     
    error()

if __name__ == "__main__":
    main()
