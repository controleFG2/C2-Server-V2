import socket
import dns.message as dm
from common.protocolo import DNSprotocolo

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

    def handlePacket(self, dadosBrutos, endereco, socket):
        try:
            pacote = dm.from_wire(dadosBrutos)
            urlBruta = pacote.question[0].name.to_text()
            tipo, mensagem = DNSprotocolo.decodar(urlBruta, 'c2.local')
            print(tipo, mensagem)

            resposta = dm.make_response(pacote)
            dadosResposta = resposta.to_wire()

            socket.sendto(dadosResposta, endereco)
            
        except Exception as e:
            print(f"[-] Erro ao processar: {e}")

if __name__ == '__main__':
    listener = DNSlistener()
    listener.start()