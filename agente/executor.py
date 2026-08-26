import subprocess

class commandExecutor:
    def __init__(self):
        pass

    def executaComando(self, comando: str) -> bytes:

        resultado = subprocess.run(comando, capture_output=True, shell=True)

        saida, erro = resultado.stdout, resultado.stderr

        return saida + erro

    #BLOCO EXECUTOR: executa os comandos no agente e retorna o output

if __name__ == '__main__':
    comando = 'whoami'
    executor = commandExecutor()
    print(executor.executaComando(comando))