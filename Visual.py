import random
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

class Jogador:
    def __init__(self, nome, pontuacao=0):
        self.nome = nome
        self.mao = []
        self.pontuacao = pontuacao

    def __str__(self):
        return f"Jogador: {self.nome} | Pontos: {self.pontuacao} | Mão: {self.mao}"

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
        return (3, mao[0], 0)
    if mao[0] == mao[1]:
        return (2, mao[0], mao[2])
    if mao[1] == mao[2]:
        return (2, mao[1], mao[0])
    
    return (1, mao[0], 0)

class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Jogo de Cartas")
        self.geometry("800x600")

        self.ranking = [
            Jogador("GJ", 350),
            Jogador("Breno", 500),
            Jogador("PK", 280)
        ]

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        actions_frame = ttk.LabelFrame(main_frame, text="Ações do Jogo", padding="10")
        actions_frame.pack(fill=tk.X, pady=10)

        start_round_button = ttk.Button(actions_frame, text="Iniciar Nova Rodada", command=self.start_round)
        start_round_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        add_player_button = ttk.Button(actions_frame, text="Adicionar Jogador", command=self.show_add_player_dialog)
        add_player_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        show_ranking_button = ttk.Button(actions_frame, text="Mostrar Ranking", command=self.update_display)
        show_ranking_button.pack(side=tk.LEFT, padx=5, pady=5)

        ranking_frame = ttk.LabelFrame(main_frame, text="Ranking de Jogadores", padding="10")
        ranking_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.ranking_text = scrolledtext.ScrolledText(ranking_frame, wrap=tk.WORD, height=10)
        self.ranking_text.pack(fill=tk.BOTH, expand=True)
        self.ranking_text.config(state=tk.DISABLED)

        log_frame = ttk.LabelFrame(main_frame, text="Log do Jogo", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)

    def update_display(self):
        ordenar_ranking(self.ranking)
        self.ranking_text.config(state=tk.NORMAL)
        self.ranking_text.delete(1.0, tk.END)
        self.ranking_text.insert(tk.END, "--- RANKING ATUAL ---\n")
        for i, jogador in enumerate(self.ranking):
            self.ranking_text.insert(tk.END, f"{i+1}º Lugar: {jogador}\n")
        self.ranking_text.config(state=tk.DISABLED)

    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def start_round(self):
        if len(self.ranking) < 2:
            messagebox.showwarning("Aviso", "É preciso de pelo menos 2 jogadores para iniciar uma rodada.")
            return

        self.log_message("\n--- INICIANDO NOVA RODADA ---")
        baralho = [valor for valor in range(1, 14)] * 4
        random.shuffle(baralho)

        for jogador in self.ranking:
            mao = [baralho.pop() for _ in range(3)]
            jogador.mao = mao
            self.log_message(f"Mão de {jogador.nome}: {jogador.mao}")

        melhor_mao = (0, 0, 0)
        vencedor = None
        
        for jogador in self.ranking:
            mao_avaliada = avaliar_mao(jogador.mao)
            self.log_message(f"-> {jogador.nome} avaliou a mão: {mao_avaliada}")
            
            if mao_avaliada > melhor_mao:
                melhor_mao = mao_avaliada
                vencedor = jogador

        if vencedor:
            self.log_message(f"\nO vencedor da rodada é: {vencedor.nome}!")
            vencedor.pontuacao += 100
            self.log_message(f"Pontuação de {vencedor.nome} atualizada para: {vencedor.pontuacao}")
        else:
            self.log_message("\nNenhum vencedor foi declarado nesta rodada.")
        
        for jogador in self.ranking:
            jogador.mao.clear()
        
        self.log_message("Mãos limpas para a próxima rodada.")
        self.update_display()

    def show_add_player_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Adicionar Jogador")
        
        ttk.Label(dialog, text="Nome do Jogador:").pack(padx=10, pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.pack(padx=10, pady=5)
        
        ttk.Label(dialog, text="Pontuação Inicial (opcional):").pack(padx=10, pady=5)
        score_entry = ttk.Entry(dialog)
        score_entry.pack(padx=10, pady=5)
        
        def add_and_close():
            name = name_entry.get()
            score_str = score_entry.get()
            
            if not name:
                messagebox.showerror("Erro", "O nome do jogador não pode ser vazio.")
                return

            score = 0
            if score_str:
                try:
                    score = int(score_str)
                except ValueError:
                    messagebox.showerror("Erro", "A pontuação deve ser um número inteiro.")
                    return
            
            novo_jogador = Jogador(name, score)
            self.ranking.append(novo_jogador)
            self.log_message(f"Jogador '{novo_jogador.nome}' adicionado com sucesso!")
            self.update_display()
            dialog.destroy()
            
        ttk.Button(dialog, text="Adicionar", command=add_and_close).pack(pady=10)


if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
