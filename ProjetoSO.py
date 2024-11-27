# Projeto Desenvolvido por:
# Amanda Reis
# Eduardo Costa Araujo

import threading
import random
import time
import os
from queue import Queue

# Classe para representar encomendas
class Encomenda:
    def __init__(self, id, origem, destino):
        self.id = id
        self.origem = origem
        self.destino = destino
        self.chegada_origem = None
        self.carregada_em = None
        self.descarregada_em = None
        self.veiculo_id = None

# Classe para representar pontos de redistribuição
class PontoRedistribuicao(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id


        self.fila = Queue()  # Usando Queue para gestão da fila
        self.lock = threading.Lock()

    def adicionar_encomenda(self, encomenda):
        self.fila.put(encomenda)  # Adiciona encomenda à fila
        encomenda.chegada_origem = time.time()

    def retirar_encomenda(self):
        if not self.fila.empty():
            return self.fila.get()  # Retira encomenda da fila
        return None

    def run(self):
        while encomendas_ativas.is_set():
            time.sleep(0.1)  # Simula o funcionamento contínuo do ponto
        print(f"Ponto {self.id} finalizou suas operações.")

# Classe para representar os veículos
class Veiculo(threading.Thread):
    def __init__(self, id, pontos, capacidade):
        super().__init__()
        self.id = id
        self.pontos = pontos
        self.capacidade = capacidade
        self.carga = []
        self.ponto_atual = random.choice(self.pontos)  # Começa em um ponto aleatório

    def carregar_encomendas(self):
        while len(self.carga) < self.capacidade:
            encomenda = self.ponto_atual.retirar_encomenda()
            if encomenda:
                encomenda.carregada_em = time.time()
                encomenda.veiculo_id = self.id
                self.carga.append(encomenda)
            else:
                break

    def descarregar_encomendas(self):
        entregues = []
        for encomenda in self.carga:
            if encomenda.destino == self.ponto_atual.id:
                time.sleep(random.uniform(0.5, 1.5))  # Simula tempo de descarregamento
                encomenda.descarregada_em = time.time()
                salvar_rastro(encomenda)
                entregues.append(encomenda)
        # Remove as encomendas entregues da carga
        for encomenda in entregues:
            self.carga.remove(encomenda)

    def run(self):
        while encomendas_ativas.is_set() or any(p.fila.qsize() > 0 for p in self.pontos):
            self.descarregar_encomendas()
            self.carregar_encomendas()

            # Move para o próximo ponto
            proximo_ponto_id = (self.ponto_atual.id + 1) % len(self.pontos)
            self.ponto_atual = self.pontos[proximo_ponto_id]
            time.sleep(random.uniform(1, 3))  # Tempo de viagem

# Função para salvar rastro da encomenda
def salvar_rastro(encomenda):
    filename = f"encomenda_{encomenda.id}.txt"
    with open(filename, "w") as f:
        f.write(f"Encomenda ID: {encomenda.id}\n")
        f.write(f"Origem: {encomenda.origem}\n")
        f.write(f"Destino: {encomenda.destino}\n")
        f.write(f"Chegada ao ponto de origem: {time.ctime(encomenda.chegada_origem)}\n")
        f.write(f"Carregada no veículo {encomenda.veiculo_id}: {time.ctime(encomenda.carregada_em)}\n")
        f.write(f"Descarregada no destino: {time.ctime(encomenda.descarregada_em)}\n")

# Função para monitorar o sistema
def monitoramento_real(pontos, veiculos):
    while encomendas_ativas.is_set():
        limpar_console()
        print("Monitoramento em tempo real")
        print("-" * 30)
        for ponto in pontos:
            print(f"Ponto {ponto.id} - Encomendas na fila: {ponto.fila.qsize()}")
        for veiculo in veiculos:
            cargas = [f"{e.id} -> {e.destino}" for e in veiculo.carga]
            print(f"Veículo {veiculo.id} - Carga: {cargas} - Ponto Atual: {veiculo.ponto_atual.id}")
        time.sleep(5)

# Função para limpar o console
def limpar_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Verifica se todas as encomendas foram entregues
def todas_encomendas_entregues(encomendas):
    return all(e.descarregada_em is not None for e in encomendas)

# Função principal
if __name__ == "__main__":
    # Solicitação das entradas com validação de P > A > C
    while True:
        S = int(input("Número de pontos de redistribuição (S): "))
        C = int(input("Número de veículos (C): "))
        P = int(input("Número de encomendas (P): "))
        A = int(input("Capacidade dos veículos (A): "))

        if P > A > C:
            break
        else:
            print("Erro: Certifique-se de que P > A > C. Tente novamente.\n")

    # Inicializando o evento para controle de execução das threads
    encomendas_ativas = threading.Event()

    # Inicializando os pontos de redistribuição (mas sem iniciar suas threads ainda)
    pontos = [PontoRedistribuicao(i) for i in range(S)]

    # Inicializando as encomendas com origem e destino aleatórios
    encomendas = [
        Encomenda(i, random.randint(0, S - 1), random.randint(0, S - 1))
        for i in range(P)
    ]

    # Inicializando os veículos com capacidade e pontos de redistribuição
    veiculos = [Veiculo(i, pontos, A) for i in range(C)]

    # Adiciona as encomendas nos pontos de origem
    for encomenda in encomendas:
        ponto_origem = pontos[encomenda.origem]
        ponto_origem.adicionar_encomenda(encomenda)

    # Inicializa as threads dos pontos de redistribuição após as encomendas serem alocadas
    for ponto in pontos:
        ponto.start()

    # Inicializa as threads dos veículos após todas as encomendas serem alocadas
    for veiculo in veiculos:
        veiculo.start()

    # Inicializa o evento de execução das threads
    encomendas_ativas.set()

    # Agora que todos os objetos estão criados e as threads foram iniciadas,iniciamos o monitoramento
    monitoramento_thread = threading.Thread(target=monitoramento_real, args=(pontos, veiculos))
    monitoramento_thread.start()

    # Aguarda até que todas as encomendas sejam entregues
    while not todas_encomendas_entregues(encomendas):
        time.sleep(1)

    # Finaliza as operações
    encomendas_ativas.clear()
    for ponto in pontos:
        ponto.join()
    for veiculo in veiculos:
        veiculo.join()

    print("Todas as encomendas foram entregues.")

