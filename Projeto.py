import random


class Jogador:

    def __init__(self, nome, pontuacao=0):
        self.nome = nome
        self.mao = []  
        self.pontuacao = pontuacao

    def adicionar_carta(self, carta):
        self.mao.append(carta)

    def retirar_carta(self):
        if not self.mao:
            return None
        return self.mao.pop()
    
    def __str__(self):
        return f"Jogador: {self.nome} | Pontuação: {self.pontuacao} | Mão: {self.mao}"


def quicksort(arr, inicio, fim):
    if inicio < fim:
        pivo_idx = particionar(arr, inicio, fim)
        quicksort(arr, inicio, pivo_idx - 1)
        quicksort(arr, pivo_idx + 1, fim)

def particionar(arr, inicio, fim):
    pivo = arr[fim].pontuacao
    i = inicio - 1
    for j in range(inicio, fim):
        if arr[j].pontuacao > pivo:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[fim] = arr[fim], arr[i + 1]
    return i + 1

def ordenar_ranking(ranking):
    n = len(ranking)
    if n > 1:
        quicksort(ranking, 0, n - 1)

def avaliar_mao(mao):
    mao.sort(reverse=True)
    
    if mao[0] == mao[1] == mao[2]:
        print(f"Mão: {mao} -> Trinca de {mao[0]}")
        return (3, mao[0], 0)
    
    if mao[0] == mao[1]:
        print(f"Mão: {mao} -> Par de {mao[0]}")
        return (2, mao[0], mao[2])
    if mao[1] == mao[2]:
        print(f"Mão: {mao} -> Par de {mao[1]}")
        return (2, mao[1], mao[0])
        
    print(f"Mão: {mao} -> Carta Alta ({mao[0]})")
    return (1, mao[0], 0)

def iniciar_rodada(ranking):
    if len(ranking) < 2:
        print("É preciso de pelo menos 2 jogadores para iniciar uma rodada.")
        return

    baralho = [valor for valor in range(1, 14)] * 4
    random.shuffle(baralho)

    print("\n--- INICIANDO NOVA RODADA ---")
    
    for jogador in ranking:
        mao = [baralho.pop() for _ in range(3)]
        jogador.mao = mao 
        print(f"Mão de {jogador.nome}: {jogador.mao}")

    melhor_mao = (0, 0, 0) 
    vencedor = None
    
    for jogador in ranking:
        mao_avaliada = avaliar_mao(jogador.mao)
        
        if mao_avaliada > melhor_mao:
            melhor_mao = mao_avaliada
            vencedor = jogador

    if vencedor:
        print(f"\nO vencedor da rodada é: {vencedor.nome} com a mão {melhor_mao}!")
        vencedor.pontuacao += 100
        print(f"Pontuação de {vencedor.nome} atualizada para: {vencedor.pontuacao}")
    else:
        print("\nNenhum vencedor foi declarado nesta rodada.")
    
    for jogador in ranking:
        jogador.mao.clear()
    print("Mãos limpas para a próxima rodada.")

def adicionar_jogador(ranking):
    nome = input("Digite o nome do novo jogador: ")
    pontuacao = 0
    try:
        pontuacao = int(input("Digite a pontuação inicial (padrão: 0): ") or 0)
    except ValueError:
        print("Pontuação inválida, usando 0.")
    novo_jogador = Jogador(nome, pontuacao)
    ranking.append(novo_jogador)
    print(f"Jogador '{novo_jogador.nome}' adicionado com sucesso!")

def alterar_pontuacao(ranking):
    if not ranking:
        print("Não há jogadores para alterar.")
        return
    print("--- Jogadores Disponíveis ---")
    for i, jogador in enumerate(ranking):
        print(f"[{i+1}] {jogador.nome}")
        
    try:
        escolha = int(input("Selecione o número do jogador para alterar a pontuação: "))
        if 1 <= escolha <= len(ranking):
            jogador = ranking[escolha - 1]
            nova_pontuacao = int(input(f"Digite a nova pontuação para {jogador.nome} (atual: {jogador.pontuacao}): "))
            jogador.pontuacao = nova_pontuacao
            print(f"Pontuação de {jogador.nome} alterada para {jogador.pontuacao}.")
        else:
            print("Número inválido. Tente novamente.")
    except (ValueError, IndexError):
        print("Entrada inválida.")


if __name__ == "__main__":
    print("--- Simulador de Jogo de Cartas Interativo ---")

    ranking = [
        Jogador("GJ", 350),
        Jogador("Breno", 500),
        Jogador("PK", 280)
    ]

    while True:
        print("\n" + "="*30)
        print("MENU PRINCIPAL")
        print("1. Adicionar novo jogador")
        print("2. Alterar pontuação de um jogador")
        print("3. Mostrar ranking atual")
        print("4. Iniciar uma nova rodada do jogo")
        print("5. Sair")
        print("="*30)
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            adicionar_jogador(ranking)
        elif escolha == '2':
            alterar_pontuacao(ranking)
        elif escolha == '3':
            if not ranking:
                print("Não há jogadores no ranking para exibir.")
                continue
            
            print("\n--- Ranking de Jogadores ---")
            ordenar_ranking(ranking)
            for i, jogador in enumerate(ranking):
                print(f"{i+1}º Lugar: {jogador}")
        elif escolha == '4':
            iniciar_rodada(ranking)
        elif escolha == '5':
            print("Saindo do simulador. Até mais!")
            break
        else:
            print("Opção inválida. Por favor, escolha uma das opções do menu.")