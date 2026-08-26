# C2 Server - V2 (DNS Tunneling)

Este projeto é a **Versão 2 (V2)** do meu estudo prático sobre infraestrutura de redes e comunicação oculta. A versão antiga (V1), focada no modelo linear básico, pode ser encontrada no meu perfil do GitHub. Nesta V2, o foco foi reestruturar completamente o sistema usando Orientação a Objetos, comunicação assíncrona paralela e controle de fragmentação de dados. Como o projeto foi desenvolvido exclusivamente para fins de portfólio pessoal e aprendizado, ele não visa o uso em produção, mas sim a consolidação de conceitos complexos de engenharia.

⚠️ **AVISO LEGAL:** Este projeto foi desenvolvido estritamente para fins de estudo, pesquisa e laboratório educacional. O uso de ferramentas de Command & Control (C2) sem autorização explícita e por escrito em sistemas de terceiros é ilegal e antiético.

---

## O que o projeto faz?

O framework estabelece um canal estável de Comando e Controle utilizando o protocolo **DNS (consultas do tipo TXT)**. Ele permite que um operador envie comandos remotamente através de um terminal interativo e receba a saída do sistema operacional alvo de forma assíncrona, quebrando qualquer tamanho de texto em múltiplos pacotes automáticos.

### Limitação de Escopo Proposital
Para manter o foco estrito no estudo de protocolos e formato binário de redes, **o projeto suporta apenas um agente conectado por vez**. Gerenciar múltiplos clientes simultâneos exigiria a implementação de concorrência massiva complexa, travamento de memória (*mutexes*) e bancos de dados transacionais, temas que fogem do objetivo central deste objeto de estudo específico.

---

## 🛠️ Estrutura do Projeto

```text
meu_c2/
│
├── common/              
│   ├── _init_.py 
│   └── protocolo.py     # Tradutor global: encoda, decoda e reconstrói o Base32 do DNS
│
├── servidor/            
│   ├── rede.py          # Listener UDP principal: gerencia sockets e roteia pacotes
│   └── painel.py        # Terminal interativo (CLI) dinâmico rodando em Thread paralela
│
└── agente/              
    ├── conexao.py       # Motor de Beacon: faz check-in e dispara rajadas de dados
    └── executor.py      # Executor local do SO: captura saídas brutas (stdout/stderr)
```

---

## Tecnologias Utilizadas

*   **Python 3** (Linguagem base do projeto)
*   **Biblioteca Sockets** (Comunicação UDP pura de baixo nível)
*   **dnspython** (Manipulação, parsing e geração de estruturas binárias DNS)
*   **Threading & Queue** (Execução assíncrona paralela e esteira de troca de dados)
*   **Subprocess** (Execução e captura de saídas do Sistema Operacional)

---

## Habilidades Adquiridas neste Projeto

A engenharia por trás do desenvolvimento e modelagem de pacotes de rede foi o pilar central de aprendizado deste projeto, consolidando as seguintes competências:

*   **Desenvolvimento de Pacotes de Rede via DNS Tunneling:** Criação e manipulação de uma camada de aplicação customizada para encapsular dados dentro de requisições DNS válidas, superando as limitações de tamanho do protocolo através de técnicas manuais de codificação e estruturação de dados.
*   **Arquitetura Orientada a Objetos (POO):** Eliminação de funções monolíticas pesadas através de divisão cirúrgica de responsabilidades (cada classe faz apenas uma função bem definida).
*   **Programação Concorrente Multithread:** Criação de arquiteturas paralelas onde a interface de usuário (Terminal/Input) não bloqueia o recebimento de dados da rede (Socket UDP/Listening).
*   **Gerenciamento de Estado Distribuído:** Uso de buffers estruturados baseados em chaves numéricas em dicionários para garantir o ordenamento correto de pacotes fragmentados que chegam via protocolo UDP sem estado (*stateless*).
*   **Tratamento Estrito de Tipagem:** Manipulação precisa de fluxos de dados convertendo e alinhando tipos de dados complexos entre Bytes, Strings e Inteiros na passagem de dados de rede.

---

## Melhorias Futuras & Roadmap

O desenvolvimento técnico gerou ideias maduras de otimização de escopo para próximas versões:

- [ ] **Remoção de Dependências Externas no Agente:** Substituir a biblioteca `dnspython` no lado do cliente pela biblioteca padrão `struct` do Python. O objetivo seria realizar a montagem binária dos pacotes de DNS manualmente, deixando o executável do agente extremamente leve para ambientes reais de simulação.
- [ ] **Resiliência a Perda de Pacotes (UDP ACK):** Criar um mecanismo simples de confirmação de entrega na camada da aplicação para identificar fragmentos corrompidos ou perdidos no meio do caminho e solicitar o reenvio automático.
- [ ] **Mecanismo de Desconexão Passiva:** Adicionar rotinas de timeout agressivas para que o agente se encerre silenciosamente caso o servidor pare de responder por uma janela de tempo específica.
