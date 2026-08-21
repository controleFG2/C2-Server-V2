import base64

class DNSprotocolo:

    @staticmethod
    def encodar(tipo: bytes, msg: bytes, dominio: str) -> str:
        msgBase32 = base64.b32encode(msg)

        msgBase32Filtrado = msgBase32.replace(b'=', b'')

        msgFinalizado = f'{tipo.decode('utf-8')}.{msgBase32Filtrado.decode('utf-8')}.{dominio}'

        return msgFinalizado.lower()

    @staticmethod
    def decodar(url: str, dominio: str) -> list:
        mensagemBruta = url.replace(f'.{dominio}', '')

        tipo, mensagemCodificada = mensagemBruta.split('.')[0], mensagemBruta.split('.')[1].upper()

        mensagemCodificadaBytes = mensagemCodificada.encode('utf-8')

        resto = len(mensagemCodificadaBytes) % 8

        if resto != 0:
            padding = 8 - resto
            mensagemCodificadaBytes = mensagemCodificadaBytes + (b'='*padding)

        mensagemDecodificada = base64.b32decode(mensagemCodificadaBytes)
        
        return tipo, mensagemDecodificada