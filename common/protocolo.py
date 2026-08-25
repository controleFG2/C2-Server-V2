import base64

class DNSprotocolo:

    @staticmethod
    def encodar(tipo: bytes, msg: bytes, dominio: str, numPacote: int = 0, totalPacotes:int = 0) -> str:
        msgBase32 = base64.b32encode(msg)

        msgBase32Filtrado = msgBase32.replace(b'=', b'')

        msgFinalizado = f'{tipo.decode("utf-8")}.{numPacote}.{totalPacotes}.{msgBase32Filtrado.decode("utf-8")}.{dominio}'

        return msgFinalizado.lower()

    @staticmethod
    def limparUrl(url: str, dominio: str) -> list:
        mensagemBruta = url.replace(f'.{dominio}', '').strip('.')
        mensagemSplit = mensagemBruta.split('.')

        tipo, mensagemCodificada = mensagemSplit[0], mensagemSplit[3].upper()

        mensagemCodificadaBytes = mensagemCodificada.encode('utf-8')
        
        return tipo, mensagemCodificadaBytes

    @staticmethod
    def traduzir(msg):
        mensagemCodificadaBytes = msg
        resto = len(mensagemCodificadaBytes) % 8
        
        if resto != 0:
            padding = 8 - resto
            mensagemCodificadaBytes = mensagemCodificadaBytes + (b'=' * padding)
        
        mensagemDecodificadaBytes = base64.b32decode(mensagemCodificadaBytes)

        return mensagemDecodificadaBytes