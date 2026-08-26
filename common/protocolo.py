import base64

class DNSprotocolo:

    @staticmethod
    def encodar(tipo: bytes, msg: bytes, dominio: str, numPacote: int = 0, totalPacotes:int = 0) -> str:

        msgBase32Filtrado = msg.replace(b'=', b'')

        msgFinalizado = f'{tipo.decode("utf-8")}.{numPacote}.{totalPacotes}.{msgBase32Filtrado.decode("utf-8")}.{dominio}'

        return msgFinalizado.lower()
    
        # BLOCO ENCODAR: Converte dados em bytes para Base32, remove os caracteres de preenchimento '=' e monta a string de subdomínios padronizada.

    @staticmethod
    def limparUrl(url: str, dominio: str) -> list:
        mensagemBruta = url.replace(f'.{dominio}', '').strip('.')
        mensagemSplit = mensagemBruta.split('.')

        tipo, mensagemCodificada, numPacote, totalPacotes = mensagemSplit[0], mensagemSplit[3].upper(), int(mensagemSplit[1]), int(mensagemSplit[2])

        mensagemCodificadaBytes = mensagemCodificada.encode('utf-8')
        
        return tipo, mensagemCodificadaBytes, numPacote, totalPacotes
    
        # BLOCO LIMPARURL: Remove o domínio alvo e pontos extras da URL, separa os metadados usando fatiamento por pontos e retorna os bytes do Base32 limpos.

    @staticmethod
    def traduzir(msg:bytes) -> bytes:
        mensagemCodificadaBytes = msg
        resto = len(mensagemCodificadaBytes) % 8
        
        if resto != 0:
            padding = 8 - resto
            mensagemCodificadaBytes = mensagemCodificadaBytes + (b'=' * padding)
        
        mensagemDecodificadaBytes = base64.b32decode(mensagemCodificadaBytes)

        return mensagemDecodificadaBytes
    
        # BLOCO TRADUZIR: Recebe a string Base32 incompleta, calcula e adiciona o preenchimento '=' faltante usando a regra dos múltiplos de 8 e faz a decodificação final.

    @staticmethod
    def fatiador(msg: bytes) -> bytes:
        msgCodificada = base64.b32encode(msg).replace(b'=', b'')

        tamanho = 45

        pedacos = [msgCodificada[i:i+tamanho] for i in range(0, len(msgCodificada), tamanho)]

        return pedacos

        # BLOCO FATIADOR: Recebe uma string em bytes, encoda para base32 e divide em tamanhos iguais

    @staticmethod
    def juntaString(msg: dict, total: int) -> bytes:
        msgFinal = b''

        for i in range(total):
            msgFinal += msg[i]
            
        return msgFinal