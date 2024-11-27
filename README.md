# Projeto Sistemas Operacionais 01
## Simulador de Rede de Entregas

Este projeto simula uma rede de entregas onde encomendas são transportadas por veículos de um ponto de redistribuição até outro. A sincronização entre os componentes é feita utilizando semáforos e variáveis de trava para assegurar a consistência dos dados.

## Descrição

O simulador modela:
- **Encomendas**: Cada encomenda tem um ponto de origem e um ponto de destino, além de registrar horários de carregamento e descarregamento.
- **Pontos de Redistribuição**: Organizados sequencialmente, esses pontos gerenciam as encomendas usando uma fila.
- **Veículos**: Responsáveis pelo transporte das encomendas entre os pontos de redistribuição. Cada veículo tem uma capacidade de carga limitada.

## Funcionalidades

- **Carregamento e Descarregamento**: Os veículos carregam encomendas no ponto de origem e as descarregam no ponto de destino.
- **Fila de Espera**: As encomendas ficam em uma fila no ponto de origem até serem carregadas por um veículo.
- **Monitoramento em Tempo Real**: Exibe o estado atual das encomendas e dos veículos em intervalos regulares.
- **Rastro das Encomendas**: Gera um arquivo de log para cada encomenda, contendo os detalhes de sua trajetória.

## Estrutura do Código

- **Encomenda**: Representa uma encomenda e seus atributos.
- **PontoRedistribuicao**: Gerencia a fila de encomendas e sincroniza o acesso através de semáforos.
- **Veiculo**: Gerencia o processo de carregamento, transporte e descarregamento das encomendas.
- **Funções Auxiliares**:
  - `salvar_rastro(encomenda)`: Salva os detalhes da encomenda em um arquivo.
  - `monitoramento_real(pontos, veiculos)`: Exibe o estado atual do sistema.
  - `limpar_console()`: Limpa a tela do console.
  - `todas_encomendas_entregues(encomendas)`: Verifica se todas as encomendas foram entregues.

## Como Executar

1. **Requisitos**:
   - Biblioteca padrão do Python (`threading`, `random`, `time`, `os`, `queue`)

2. **Passos**:
   - Clone o repositório.
   - Execute o script principal:
     ```bash
     python main.py
     ```
   - Forneça os parâmetros solicitados:
     - Número de pontos de redistribuição (S)
     - Número de veículos (C)
     - Número de encomendas (P)
     - Capacidade dos veículos (A)
   - A simulação iniciará e o monitoramento em tempo real será exibido no console.

## Exemplo de Uso

```bash
Número de pontos de redistribuição (S): 5
Número de veículos (C): 3
Número de encomendas (P): 10
Capacidade dos veículos (A): 2
Monitoramento em tempo real
------------------------------
Ponto 0 - Encomendas na fila: 2
Ponto 1 - Encomendas na fila: 0
...
Veículo 0 - Carga: [1 -> 2, 4 -> 3] - Ponto Atual: 0
Veículo 1 - Carga: [0 -> 3] - Ponto Atual: 1
...

