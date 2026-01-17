import customtkinter as ctk
import random
import pygame
import os

#config da janela
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("GAMBLE")
app.geometry("1280x720")

fonte_eu = ctk.CTkFont(
    family="Comic Sans MS",
    size=20
)

#telas do programa 
container = ctk.CTkFrame(app)
container.pack(fill="both", expand=True)

tela_jogo = ctk.CTkFrame(container)
tela_jogo.pack(fill="both", expand=True)

tela_status = ctk.CTkFrame(container)

#variaveis do painel
figuras = ["💎","🪙","👑"]
dinheiro = 10

#faixas de audio e correcao de path
pygame.mixer.init()
base_dir = os.path.dirname(os.path.abspath(__file__))

jackpot_sound = pygame.mixer.Sound(os.path.join(base_dir, "songs", "jackpot.wav"))
game_over_sound = pygame.mixer.Sound(os.path.join(base_dir, "songs", "game-over.wav"))

#variaveis do status
ganhos_status = 0
perdas_status = 0
giros_status = 0
giros_ganhos = 0
derrotas = 0
vitoria_normal = 0
jackpots = 0

#funcoes do programa 
def mostrar_status():
    tela_jogo.pack_forget()
    tela_status.pack(fill="both", expand=True)

    #atualiza os status
    label_saldo.configure(text=f"salto atual:  R${dinheiro:.2f}")
    label_ganhos.configure(text=f"ganhos totais:  R${ganhos_status:.2f}")
    label_perdas.configure(text=f"perdas totais:  R${perdas_status:.2f}")
    label_giros.configure(text=f"giros totais:  {giros_status}")

def mostrar_jogo():
    tela_status.pack_forget()
    tela_jogo.pack(fill="both", expand=True)

#funcao que verifica se tem audio rodando pra evitar spamm e de 
# quebra ainda roda o audio do argumento passado
def verifica_audio(audio):
    if pygame.mixer.get_busy():
        return None
    else:
        audio.play()

def gamble():
    global dinheiro
    global ganhos_status
    global perdas_status
    global giros_status
    global giros_ganhos
    global derrotas
    global vitoria_normal 
    global jackpots
    global ganho
    global dinheiro_i
    global dinheiro_f

    figuras_choice = []
    
    if dinheiro > 0:
                dinheiro_i = dinheiro
                giros_status += 1

                for _ in figuras:
                    figuras_choice.append(random.choice(figuras))
                
                contagem = set(figuras_choice)

                if len(contagem) == 3:
                    derrotas += 1
                    ganho = 3
                    perdas_status += ganho
                    dinheiro -= ganho
                    
                    dinheiro_f = dinheiro - ganho
                elif len(contagem) == 2:
                    vitoria_normal += 1
                    giros_ganhos += 1
                    ganho = 0.5
                    ganhos_status += ganho
                    dinheiro += ganho
                    
                    dinheiro_f = dinheiro + ganho
                else:
                    jackpots += 1
                    giros_ganhos += 1
                    ganho = 3
                    ganhos_status += ganho
                    dinheiro += ganho
                    
                    dinheiro_f = dinheiro + ganho

                    verifica_audio(jackpot_sound)

                #campos que devem sofrer edicao
                painel.configure(text=figuras_choice)
                label_dinheiro.configure(text=f"R${dinheiro:.2f}")
        
    if dinheiro <= 0:
        label_dinheiro.configure(text=f"R$quebrado filho")
        painel.configure(text="GAME OVER")

        verifica_audio(game_over_sound)

#tela do jogo
label_dinheiro = ctk.CTkLabel(
    tela_jogo,
    text=f"R${dinheiro:.2f}",
    font=ctk.CTkFont(size=30))
label_dinheiro.place(x=20,y=20)

painel = ctk.CTkLabel(tela_jogo,
                      text=figuras,
                      height=500,
                      font=ctk.CTkFont(size=150))
painel.pack()

btn_apostar = ctk.CTkButton(tela_jogo,
                            text="giro",
                            height=60,
                            command=gamble,
                            font=ctk.CTkFont(size=30),
                            corner_radius=50)
btn_apostar.place(x=700, y=660)

btn_status = ctk.CTkButton(tela_jogo,
                           text="status",
                           height=50, 
                           command=mostrar_status,
                           font=ctk.CTkFont(size=30))
btn_status.place(x=1380, y=20)

label_eu = ctk.CTkLabel(tela_jogo,
                        text="by andrixrcode",
                        font=fonte_eu)
label_eu.place(x=1380, y=755)





#tela status
label_saldo = ctk.CTkLabel(tela_status,
                           text="salto atual:  R$0",
                           font=ctk.CTkFont(size=30))
label_saldo.place(x=20, y=20)

label_ganhos = ctk.CTkLabel(tela_status,
                            text="ganhos totais:  R$0",
                            font=ctk.CTkFont(size=30))
label_ganhos.place(x=20, y=55)

label_perdas = ctk.CTkLabel(tela_status,
                            text="perdas totais:  R$0",
                            font=ctk.CTkFont(size=30))
label_perdas.place(x=20, y=90)

label_giros = ctk.CTkLabel(tela_status,
                           text="giros totais:  0",
                           font=ctk.CTkFont(size=30))
label_giros.place(x=20, y=125)

btn_voltar = ctk.CTkButton(tela_status,
                           text="voltar", 
                           height=50,
                           command=mostrar_jogo,
                           font=ctk.CTkFont(size=30))
btn_voltar.place(x=1380, y=20)

app.mainloop()